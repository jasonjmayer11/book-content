"""Book reels: storyboard JSON -> 1080x1920 MP4 + cover.jpg + caption.txt.

Reuses the DealCaddie engine (reelkit primitives, original music, SFX, loudnorm) with a book brand:
black canvas, cover yellow, cream type. Every video opens on its designed cover for 0.5 s (TikTok's
cover_timestamp points there), is readable muted, and ends on the book + "Search ... on Amazon".

Voice: if Kokoro is installed (GitHub Actions) each scene's "voice" line is synthesised and the scene is
held to exactly that length. Without Kokoro the video is built silent-voiced with estimated timing.
"""
import datetime, glob, json, math, os, re, subprocess, sys, wave, zlib
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reelkit import (W, H, FPS, font, text_layer, wrap, fit_size, stack, rounded, place, enter,
                     ease_out, ease_in_out, with_alpha)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F_BIG = os.path.join(ROOT, "fonts", "HerosCn-Bold.otf")
F_SEMI = os.path.join(ROOT, "fonts", "Inter-SemiBold.otf")
F_MED = os.path.join(ROOT, "fonts", "Inter-Medium.otf")
F_DISP = os.path.join(ROOT, "fonts", "InterDisplay-Bold.otf")
CX = W // 2
BLACK, YELLOW, CREAM, GOLD, GREY = (6, 6, 6), (252, 211, 3), (252, 238, 201), (232, 197, 92), (150, 146, 134)
SAFE_L, SAFE_R = 70, 1010
SR = 44100
COVER_LEAD = 0.5


# ------------------------------------------------------------------ brand canvas
def canvas():
    bg = Image.new("RGB", (W, H), BLACK)
    glow = Image.new("L", (W, H), 0)
    ImageDraw.Draw(glow).ellipse([-200, 300, W + 200, 1500], fill=46)
    glow = glow.filter(ImageFilter.GaussianBlur(220))
    bg.paste(Image.new("RGB", (W, H), (60, 48, 0)), (0, 0), glow)
    return bg
BG = canvas()

def stripes(t, alpha=255):
    """Thin hazard-tape bars top and bottom that slide: constant motion, even on a held frame."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    off = int((t * 60) % 80)
    for y0 in (0, H - 26):
        d.rectangle([0, y0, W, y0 + 26], fill=YELLOW + (alpha,))
        for x in range(-160 + off, W + 80, 80):
            d.polygon([(x, y0 + 26), (x + 26, y0), (x + 52, y0), (x + 26, y0 + 26)], fill=BLACK + (alpha,))
    return im


# ------------------------------------------------------------------ text
def norm(w): return re.sub(r"[^a-z0-9$]", "", w.lower())

def word_block(text, path, size, max_w, color=CREAM, accent=(), accent_color=YELLOW, upper=False, lh=1.06, tracking=-0.01):
    """Lay out words centred over several lines. Returns (width, height, [(layer, x, y)]) in block coords."""
    if upper: text = text.upper()
    acc = {norm(a) for a in accent}
    f = font(path, size); space = f.getlength(" ")
    lines = wrap(text, path, size, max_w)
    line_h = int(size * lh); out = []; bw = 0
    for li, line in enumerate(lines):
        ws = line.split()
        lays = [text_layer(w, path, size, accent_color if norm(w) in acc else color, tracking=tracking) for w in ws]
        lw = sum(l.width for l in lays) + space * (len(lays) - 1); bw = max(bw, lw)
        x = -lw / 2
        for l in lays:
            out.append((l, x, li * line_h)); x += l.width + space
    return bw, line_h * len(lines), out

def fit_block(text, path, size, max_w, max_h, min_size=44, **kw):
    while True:
        b = word_block(text, path, size, max_w, **kw)
        if (b[1] <= max_h and b[0] <= max_w) or size <= min_size: return b
        size -= 6

def draw_words(frame, block, cx, y, t, t0, span, alpha=1.0, pop=0.16):
    """Words appear one by one across `span` seconds starting at t0 (first word is there at t0)."""
    _, _, items = block; n = max(1, len(items))
    for i, (l, x, yy) in enumerate(items):
        a = min(1.0, (t - (t0 + span * i / n)) / pop + (1.0 if i == 0 and t0 <= 0 else 0))
        if a <= 0: continue
        a = ease_out(a)
        frame.alpha_composite(with_alpha(l, a * alpha), (int(cx + x), int(y + yy + 22 * (1 - a))))

def chunks(text):
    """2-6 word caption chunks, never a stranded single word."""
    out, cur = [], []
    for w in text.split():
        cur.append(w)
        if len(cur) >= 6 or (w.endswith((".", "?", ":", ",", "!")) and len(cur) >= 2):
            out.append(" ".join(cur)); cur = []
    if cur:
        if len(cur) == 1 and out: out[-1] += " " + cur[0]
        else: out.append(" ".join(cur))
    return out

def pill(text, size=30, fg=BLACK, bg=YELLOW, padx=30, pady=14):
    t = text_layer(text, F_SEMI, size, fg, tracking=0.14)
    im = Image.new("RGBA", (t.width + padx * 2, t.height + pady * 2), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle([0, 0, im.width - 1, im.height - 1], radius=im.height // 2, fill=bg + (255,))
    im.alpha_composite(t, (padx, pady)); return im

def shadowed(im, radius=0, blur=40, dy=30, strength=150):
    im = rounded(im, radius) if radius else im.convert("RGBA")
    pad = blur * 2 + 20
    out = Image.new("RGBA", (im.width + pad * 2, im.height + pad * 2), (0, 0, 0, 0))
    sh = Image.new("RGBA", out.size, (0, 0, 0, 0))
    sh.paste((0, 0, 0, strength), (pad, pad + dy), im.getchannel("A"))
    out.alpha_composite(sh.filter(ImageFilter.GaussianBlur(blur))); out.alpha_composite(im, (pad, pad))
    return out, pad


# ------------------------------------------------------------------ the book
def cover_img(book): return Image.open(os.path.join(ROOT, book["cover"])).convert("RGB")

def _coeffs(dst, src):
    A = []
    for (x, y), (u, v) in zip(dst, src):
        A.append([x, y, 1, 0, 0, 0, -u * x, -u * y]); A.append([0, 0, 0, x, y, 1, -v * x, -v * y])
    return np.linalg.solve(np.array(A, float), np.array(src, float).reshape(8)).tolist()

def book3d(book, h=900):
    """Front cover + spine in a simple two-point perspective, with a floor shadow."""
    cov = cover_img(book); cw = int(h * cov.width / cov.height)
    cov = cov.resize((cw, h), Image.LANCZOS)
    sw = max(40, int(h * 0.048))
    spine = Image.new("RGB", (h, sw), (16, 16, 16))
    st = text_layer(book["spine"].upper(), F_BIG, int(sw * 0.56), YELLOW, tracking=0.04)
    spine.paste(st, ((h - st.width) // 2, (sw - st.height) // 2), st)
    spine = spine.rotate(-90, expand=True)
    sx, fx = int(sw * 0.75), int(cw * 0.93); dl, dr = int(h * 0.035), int(h * 0.055)
    Wt, Ht = sx + fx, h
    out = Image.new("RGBA", (Wt, Ht), (0, 0, 0, 0))
    for im, quad in ((spine, [(0, dl), (sx, 0), (sx, h), (0, h - dl)]), (cov, [(sx, 0), (Wt, dr), (Wt, h - dr), (sx, h)])):
        src = [(0, 0), (im.width, 0), (im.width, im.height), (0, im.height)]
        lay = im.convert("RGBA").transform((Wt, Ht), Image.PERSPECTIVE, _coeffs(quad, src), Image.BICUBIC)
        m = Image.new("L", (Wt, Ht), 0); ImageDraw.Draw(m).polygon(quad, fill=255)
        out.paste(lay, (0, 0), m)
    sheen = Image.new("RGBA", (Wt, Ht), (0, 0, 0, 0))
    ImageDraw.Draw(sheen).polygon([(sx, 0), (sx + 10, 0), (sx + 10, h), (sx, h)], fill=(255, 255, 255, 46))
    out.alpha_composite(sheen)
    return shadowed(out, blur=46, dy=44, strength=200)


# ------------------------------------------------------------------ scenes: each returns frame(t) -> RGBA layer on BG
def sc_hook(s, book, dur, speak):
    blk = fit_block(s["text"], F_BIG, s.get("size", 170), 920, 900, accent=s.get("accent", ()), upper=True, lh=0.98)
    sub = fit_block(s["sub"], F_SEMI, 46, 900, 200, color=CREAM) if s.get("sub") else None
    tag = pill(s["label"]) if s.get("label") else None
    total = blk[1] + (sub[1] + 50 if sub else 0)
    y0 = 860 - total // 2
    def frame(t):
        f = BG.copy().convert("RGBA"); f.alpha_composite(stripes(t))
        z = 1.0 + 0.03 * ease_in_out(t / dur)
        if tag: place(f, tag, CX, y0 - 110, min(1, t / 0.2 + 0.4))
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        draw_words(lay, blk, CX, y0, t, 0, min(speak, dur) * 0.75)
        if sub: draw_words(lay, sub, CX, y0 + blk[1] + 50, t, min(speak, dur) * 0.75, 0.5)
        zw, zh = int(W * z), int(H * z)
        f.alpha_composite(lay.resize((zw, zh), Image.BILINEAR).crop(((zw - W) // 2, (zh - H) // 2, (zw - W) // 2 + W, (zh - H) // 2 + H)))
        return f
    return frame

PW, PH, PY = 920, 880, 330
def sc_page(s, book, dur, speak):
    path = os.path.join(ROOT, "pages", book["slug"], f"p-{int(s['page']):03d}.png")
    pg = Image.open(path).convert("RGB")
    hl = None
    if s.get("highlight"):
        x0, y0, x1, y1 = s["highlight"]
        tint = Image.new("RGB", pg.size, (255, 255, 255))
        ImageDraw.Draw(tint).rectangle([x0 * pg.width, y0 * pg.height, x1 * pg.width, y1 * pg.height], fill=(255, 226, 60))
        hl = ImageChops.multiply(pg, tint)
    a, b = s.get("from", [0.5, 0.5, 1.0]), s["focus"]
    mask = Image.new("L", (PW, PH), 0); ImageDraw.Draw(mask).rounded_rectangle([0, 0, PW - 1, PH - 1], radius=28, fill=255)
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([80, PY + 30, 80 + PW, PY + PH + 30], radius=28, fill=(252, 211, 3, 60))
    sh = sh.filter(ImageFilter.GaussianBlur(50))
    lab = pill(s.get("label", f"FROM THE BOOK  ·  PAGE {s.get('page_no', '')}".rstrip(" ·")), size=26)
    caps = chunks(s["text"]); tot = sum(len(c) for c in caps) or 1
    cap_l = [fit_block(c, F_DISP, 68, 940, 240, accent=s.get("accent", ()), lh=1.12) for c in caps]
    spans, t0 = [], 0.1
    for c in caps:
        d = max(0.5, (speak - 0.1) * len(c) / tot); spans.append((t0, t0 + d)); t0 += d
    hl_at = s.get("highlight_at", dur * 0.35)
    def crop(src, k):
        cx, cy, w = (a[i] + (b[i] - a[i]) * k for i in range(3))
        cw = w * src.width; ch = cw * PH / PW
        x = min(max(cx * src.width - cw / 2, 0), src.width - cw); y = min(max(cy * src.height - ch / 2, 0), src.height - ch)
        return src.resize((PW, PH), Image.BICUBIC, box=(x, y, x + cw, y + ch))
    def frame(t):
        f = BG.copy().convert("RGBA"); f.alpha_composite(stripes(t)); f.alpha_composite(sh)
        k = ease_in_out(min(1.0, t / max(0.1, dur - 0.2)))
        im = crop(pg, k)
        if hl is not None and t > hl_at:
            im = Image.blend(im, crop(hl, k), ease_out((t - hl_at) / 0.5))
        f.paste(im, (80, PY), mask)
        place(f, lab, CX, PY - lab.height - 22, 1.0)
        for (c0, c1), blk in zip(spans, cap_l):
            if c0 <= t < c1 or (blk is cap_l[-1] and t >= c1):
                al = min(1.0, (t - c0) / 0.12 + 0.3)
                for l, x, yy in blk[2]:
                    f.alpha_composite(with_alpha(l, al), (int(CX + x), int(1370 - blk[1] / 2 + yy)))
        return f
    return frame

def sc_quote(s, book, dur, speak):
    lab = pill(s.get("label", "FROM THE BOOK"), size=30)
    blk = fit_block(s["text"], F_DISP, s.get("size", 84), 900, 820, accent=s.get("accent", ()), lh=1.16)
    num = text_layer(s["count"], F_SEMI, 30, GREY, tracking=0.2) if s.get("count") else None
    y0 = 860 - blk[1] // 2
    bar = Image.new("RGBA", (120, 10), YELLOW + (255,))
    def frame(t):
        f = BG.copy().convert("RGBA"); f.alpha_composite(stripes(t))
        p, dy = enter(t, 0.0, dur=0.35, rise=26)
        place(f, lab, CX, y0 - 150 + dy, max(p, 0.35))
        draw_words(f, blk, CX, y0, t, 0.0, min(speak, dur - 0.6) * 0.8)
        place(f, bar, CX, y0 + blk[1] + 46, min(1, t / 0.4), 1.0)
        if num: place(f, num, CX, y0 + blk[1] + 86, min(1, t / 0.4))
        return f
    return frame

def sc_book(s, book, dur, speak):
    b3, pad = book3d(book, h=s.get("book_h", 860))
    head = fit_block(s["text"], F_BIG, s.get("size", 118), 940, 330, accent=s.get("accent", ()), upper=True, lh=0.98)
    sub = fit_block(s["sub"], F_SEMI, 44, 920, 130, color=CREAM) if s.get("sub") else None
    chips = [pill(c, size=28, fg=YELLOW, bg=(38, 34, 20)) for c in s.get("chips", [])]
    y_head = 270; y_sub = y_head + head[1] + 26
    y_book = y_sub + (sub[1] if sub else 0) + 30 - pad
    def frame(t):
        f = BG.copy().convert("RGBA"); f.alpha_composite(stripes(t))
        draw_words(f, head, CX, y_head, t, 0.0, min(1.2, speak * 0.5))
        if sub: draw_words(f, sub, CX, y_sub, t, 0.5, 0.6)
        p, dy = enter(t, 0.0, dur=0.8, rise=120)
        bob = 10 * math.sin(t * 1.6)
        place(f, b3, CX, y_book + dy + bob, max(p, 0.25), 0.94 + 0.06 * p + 0.012 * ease_in_out(t / dur))
        if chips:
            tw = sum(c.width for c in chips) + 18 * (len(chips) - 1); x = CX - tw / 2
            for i, c in enumerate(chips):
                p, dy = enter(t, 0.6 + i * 0.12)
                if p > 0: f.alpha_composite(with_alpha(c, p), (int(x), int(1470 + dy)))
                x += c.width + 18
        return f
    return frame

def sc_end(s, book, dur, speak):
    cov = cover_img(book); cw = 500; cov = cov.resize((cw, int(cw * cov.height / cov.width)), Image.LANCZOS)
    cl, pad = shadowed(cov, radius=10, blur=44, dy=34, strength=210)
    search = text_layer("SEARCH ON AMAZON", F_SEMI, 32, CREAM, tracking=0.2)
    t1 = stack([text_layer(l, F_BIG, fit_size(l, F_BIG, 72, 940, 48), YELLOW) for l in book["search_lines"]], 2)
    btn = pill(s.get("cta", "PAPERBACK + KINDLE"), size=30, padx=44, pady=22)
    def frame(t):
        f = BG.copy().convert("RGBA"); f.alpha_composite(stripes(t))
        p, dy = enter(t, 0.0, dur=0.6, rise=40)
        place(f, cl, CX, 280 - pad + dy, max(p, 0.3), 0.96 + 0.04 * p + 0.01 * ease_in_out(t / dur))
        p, dy = enter(t, 0.15); place(f, search, CX, 1090 + dy, p)
        p, dy = enter(t, 0.25); place(f, t1, CX, 1150 + dy, p)
        p, dy = enter(t, 0.4); place(f, btn, CX, 1150 + t1.height + 36 + dy, p)
        return f
    return frame

def sc_diagram(s, book, dur, speak):
    from diagrams import DIAGRAMS
    draw = DIAGRAMS[s["diagram"]]; state = s["state"]
    mask = Image.new("L", (PW, PH), 0); ImageDraw.Draw(mask).rounded_rectangle([0, 0, PW - 1, PH - 1], radius=28, fill=255)
    edge = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(edge).rounded_rectangle([78, PY - 2, 82 + PW, PY + PH + 2], radius=30, outline=YELLOW + (150,), width=3)
    lab = pill(s.get("label", "HOW IT WORKS"), size=26)
    caps = chunks(s["text"]); tot = sum(len(c) for c in caps) or 1
    cap_l = [fit_block(c, F_DISP, 68, 940, 240, accent=s.get("accent", ()), lh=1.12) for c in caps]
    spans, t0 = [], 0.1
    for c in caps:
        d = max(0.5, (speak - 0.1) * len(c) / tot); spans.append((t0, t0 + d)); t0 += d
    def frame(t):
        f = BG.copy().convert("RGBA"); f.alpha_composite(stripes(t))
        f.paste(draw(state, t, dur, F_SEMI), (80, PY), mask); f.alpha_composite(edge)
        place(f, lab, CX, PY - lab.height - 22, 1.0)
        for (c0, c1), blk in zip(spans, cap_l):
            if c0 <= t < c1 or (blk is cap_l[-1] and t >= c1):
                al = min(1.0, (t - c0) / 0.12 + 0.3)
                for l, x, yy in blk[2]:
                    f.alpha_composite(with_alpha(l, al), (int(CX + x), int(1370 - blk[1] / 2 + yy)))
        return f
    return frame

SCENES = {"diagram": sc_diagram, "hook": sc_hook, "page": sc_page, "quote": sc_quote, "book": sc_book, "end": sc_end}


# ------------------------------------------------------------------ designed cover (grid thumbnail)
def make_cover(story, book):
    cv = BG.copy().convert("RGBA"); cv.alpha_composite(stripes(0))
    head = fit_block(story["cover"], F_BIG, 170, 800, 420, accent=story.get("cover_accent", ()), upper=True, lh=0.97, color=(255, 255, 255))
    y = 290                                     # everything stays inside the centre 3:4 (y 240-1680, x 0-1080)
    for l, x, yy in head[2]: cv.alpha_composite(l, (int(CX + x), int(y + yy)))
    y += head[1] + 48
    if story.get("cover_sub"):
        st = text_layer(story["cover_sub"], F_SEMI, fit_size(story["cover_sub"], F_SEMI, 46, 820, 30), GOLD)
        cv.alpha_composite(st, (CX - st.width // 2, y)); y += st.height + 30
    if story.get("hero"):
        from diagrams import DIAGRAMS
        hd, hs = story["hero"]; hero = DIAGRAMS[hd](hs, 2.0, 4.0, F_SEMI); hh = min(PH, 1640 - y - 20); hw = int(PW * hh / PH)
        hero = rounded(hero.resize((hw, hh), Image.LANCZOS), 26)
        ImageDraw.Draw(hero).rounded_rectangle([1, 1, hw - 2, hh - 2], radius=26, outline=YELLOW + (255,), width=5)
        cv.alpha_composite(hero, (CX - hw // 2, y + 10))
        b3, pad = book3d(book, h=330); cv.alpha_composite(b3, (CX + hw // 2 - b3.width + pad - 10, y + hh - b3.height + pad + 30))
    else:
        b3, pad = book3d(book, h=min(900, 1650 - y))
        cv.alpha_composite(b3, (CX - b3.width // 2, y - pad + 10))
    return cv.convert("RGB")


# ------------------------------------------------------------------ voice (Kokoro if present)
def synth(lines, voice, speed):
    try:
        from kokoro import KPipeline
    except Exception:
        return None
    pipe = KPipeline(lang_code="a"); out = []
    for text in lines:
        if not text: out.append(None); continue
        parts = []
        for gs, ps, a in pipe(text, voice=voice, speed=speed):
            print(f"  phonemes: {ps}")
            parts.append(a.numpy() if hasattr(a, "numpy") else np.asarray(a))
        out.append(np.concatenate(parts).astype(np.float32) if parts else None)
    return out


# ------------------------------------------------------------------ audio
def _decode(path):
    raw = subprocess.check_output(["ffmpeg", "-loglevel", "error", "-i", path, "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"])
    return np.frombuffer(raw, dtype=np.float32).reshape(-1, 2).copy()

def page_flip():
    n = int(0.38 * SR); t = np.arange(n) / SR; rng = np.random.default_rng(7)
    x = rng.standard_normal(n); x = np.convolve(x, np.ones(9) / 9, mode="same") - np.convolve(x, np.ones(90) / 90, mode="same")
    env = np.exp(-((t - 0.11) / 0.07) ** 2) + 0.6 * np.exp(-((t - 0.26) / 0.04) ** 2)
    y = x * env; y /= np.abs(y).max()
    return np.stack([y, y[::-1] * 0.0 + y], 1).astype(np.float32)

def pick_track(title, used=()):
    tracks = sorted(glob.glob(os.path.join(ROOT, "music", "*.m4a")))
    want = os.environ.get("MUSIC_TRACK", "").strip()
    hit = [t for t in tracks if want and os.path.basename(t).startswith(want)]
    if hit: return hit[0]
    i = zlib.crc32((title + datetime.date.today().isoformat()).encode()) % len(tracks)   # title + date, never date alone
    while tracks[i] in used: i = (i + 1) % len(tracks)
    return tracks[i]

def soundtrack(silent, out_mp4, starts, kinds, total, track, voice_clips):
    n = int(total * SR) + 1; t = np.arange(n) / SR
    music = _decode(track)
    if len(music) < n: music = np.tile(music, (n // len(music) + 1, 1))
    has_voice = bool(voice_clips)
    mix = music[:n] * (0.11 if has_voice else 0.8)
    mix *= np.clip(t / 0.3, 0, 1)[:, None]; mix *= np.clip((total - t) / 1.6, 0, 1)[:, None]
    sfx = os.path.join(ROOT, "assets", "sfx")
    whoosh, landing, flip = _decode(os.path.join(sfx, "whoosh.wav")), _decode(os.path.join(sfx, "landing.wav")), page_flip()
    g = 0.5 if has_voice else 1.0
    def put(sig, at, gain):
        i = max(0, int(at * SR)); j = min(n, i + len(sig))
        if j > i: mix[i:j] += sig[: j - i] * gain
    for s, k in list(zip(starts, kinds))[1:]:
        if k == "end": put(landing, s + 0.15, 0.32 * g)
        elif k == "page": put(flip, s - 0.12, 0.5 * g)
        else: put(whoosh, s - 0.22, 0.30 * g)
    for at, clip, sr in voice_clips:                          # voice: high-passed + compressed by ffmpeg below
        idx = np.linspace(0, len(clip) - 1, int(len(clip) * SR / sr)); v = np.interp(idx, np.arange(len(clip)), clip)
        v = v / (np.abs(v).max() or 1) * 0.9
        put(np.stack([v, v], 1).astype(np.float32), at, 1.0)
    mix = np.tanh(mix * 1.2) / np.tanh(1.2)
    wav = out_mp4 + ".wav"
    with wave.open(wav, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(mix, -1, 1) * 32767).astype("<i2").tobytes())
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", silent, "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "192k", "-af", "loudnorm=I=-15:TP=-2.5:LRA=9", "-shortest", "-movflags", "+faststart",
                    out_mp4], check=True)
    os.remove(wav)


# ------------------------------------------------------------------ build one story
def build(story_path, out_dir, used_tracks=()):
    story = json.load(open(story_path)); slug = story["slug"]
    book = json.load(open(os.path.join(ROOT, "books", story["book"] + ".json")))
    os.makedirs(out_dir, exist_ok=True)
    voice, speed = os.environ.get("VOICE") or book.get("voice", "af_heart"), float(os.environ.get("VOICE_SPEED") or 1.05)
    scenes = story["scenes"]
    clips = synth([s.get("voice") for s in scenes], voice, speed) if any(s.get("voice") for s in scenes) else None
    timeline = []
    for i, s in enumerate(scenes):
        words = len((s.get("voice") or s.get("text") or "").split())
        speak = (len(clips[i]) / 24000) if clips and clips[i] is not None else words / 2.7 + 0.3
        dur = s.get("dur") or max(s.get("min", 2.2), speak + 0.5 + s.get("hold", 0.3))
        if clips and clips[i] is not None: dur = speak + 0.45      # hold the scene to exactly the spoken line
        timeline.append((SCENES[s["type"]](s, book, dur, speak), dur, s["type"]))
    cover = make_cover(story, book); cover_path = os.path.join(out_dir, f"{slug}-cover.jpg"); cover.save(cover_path, quality=93)
    silent = os.path.join(out_dir, f"{slug}.silent.mp4")
    enc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                            "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", silent], stdin=subprocess.PIPE)
    starts, kinds, voice_clips, t0, prev, sheet = [], [], [], COVER_LEAD - 0.3, cover, []
    first = timeline[0][0]
    for i in range(int(COVER_LEAD * FPS)):                     # cover holds 0.2 s with a slow push, then dissolves into scene 1
        t = i / FPS; z = 1 + 0.02 * t / COVER_LEAD; zw, zh = int(W * z), int(H * z)
        c = cover.resize((zw, zh), Image.BILINEAR).crop(((zw - W) // 2, (zh - H) // 2, (zw - W) // 2 + W, (zh - H) // 2 + H))
        k = max(0.0, (t - 0.2) / 0.3)
        fr = Image.blend(c, first(max(0.0, t - 0.2)).convert("RGB"), ease_in_out(k)) if k > 0 else c
        enc.stdin.write(fr.tobytes())
        if i == 0: sheet.append(fr.copy())
    for si, (fn, dur, kind) in enumerate(timeline):
        n = int(round(dur * FPS)); off = 0.3 if si == 0 else 0.0
        starts.append(t0); kinds.append(kind)
        if clips and clips[si] is not None: voice_clips.append((t0 + 0.12, clips[si], 24000))
        for i in range(int(off * FPS), n):
            fr = fn(i / FPS).convert("RGB")
            if si and i < 6: fr = Image.blend(prev, fr, (i + 1) / 7)
            enc.stdin.write(fr.tobytes())
            if i in (int(n * 0.45), n - 2): sheet.append(fr.copy())
        prev = fr; t0 += (n - int(off * FPS)) / FPS
    enc.stdin.close()
    if enc.wait() != 0: sys.exit("ffmpeg failed")
    track = pick_track(story["title"], used_tracks)
    out_mp4 = os.path.join(out_dir, f"{slug}.mp4")
    soundtrack(silent, out_mp4, starts, kinds, t0, track, voice_clips); os.remove(silent)
    # contact sheet for QA
    sheet = sheet[:10]; tw = 270; th = 480
    cs = Image.new("RGB", (tw * len(sheet), th), BLACK)
    for i, fr in enumerate(sheet): cs.paste(fr.resize((tw, th), Image.LANCZOS), (i * tw, 0))
    cs.save(os.path.join(out_dir, f"{slug}-sheet.jpg"), quality=88)
    c = story["caption"]
    open(os.path.join(out_dir, f"{slug}-caption.txt"), "w", encoding="utf-8").write(
        f"{c['hook']}\n\n{c['feel']}\n\n{c['shows']}\n\n💬 {c['ask']}\n📌 {c.get('save', 'Save this, or send it to someone who just got their keys.')}\n\n"
        f"{book['cta']}\n\n{c['tags']}\n")
    json.dump({"slug": slug, "title": story["title"], "duration": round(t0, 2), "track": os.path.basename(track),
               "voice": voice if voice_clips else None, "cover_timestamp_ms": 0}, open(os.path.join(out_dir, f"{slug}-meta.json"), "w"), indent=1)
    print(f"built {slug}: {t0:.1f}s, track {os.path.basename(track)}, voice {'on' if voice_clips else 'off (Kokoro not installed)'}")
    return track

if __name__ == "__main__":
    used = []
    for sp in sys.argv[2:]:
        used.append(build(sp, sys.argv[1], used))
