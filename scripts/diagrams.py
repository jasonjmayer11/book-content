"""Animated engineering diagrams (blueprint style) for 'how it works' explainer reels.
Drawn at 2x so the camera can push in on the part being talked about and stay sharp."""
import math
from PIL import Image, ImageDraw, ImageFilter
from reelkit import text_layer, ease_in_out, ease_out

NAVY, GRID, LINE, WATER, GAS, YEL = (10, 22, 40), (24, 44, 74), (252, 238, 201), (58, 160, 255), (170, 220, 60), (252, 211, 3)
DW, DH = 1840, 1760
TX, RX, BY, AY, R, TOPY = 760, 1080, 1200, 900, 160, 500       # tailpiece x, riser x, bend centre y, arm y, bend radius, drain y
PIPE, INNER, WALL = 152, 116, DW - 120
WEIR, CROWN, DRY = AY + INNER // 2, BY + R - INNER // 2, BY + R + 30

def _path(n=60):
    pts = [(TX, TOPY), (TX, BY)]
    pts += [(TX + R - R * math.cos(math.pi * i / n), BY + R * math.sin(math.pi * i / n)) for i in range(1, n + 1)]
    pts += [(RX, AY), (WALL, AY)]
    return pts
PATH = _path()
def _len(pts): return sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:]))
def _along(pts, s):
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        L = math.hypot(x1 - x0, y1 - y0)
        if s <= L: return x0 + (x1 - x0) * s / L, y0 + (y1 - y0) * s / L
        s -= L
    return pts[-1]
def _upto(pts, s):
    out = [pts[0]]
    for a, b in zip(pts, pts[1:]):
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        if s >= L: out.append(b); s -= L
        else: out.append((a[0] + (b[0] - a[0]) * s / L, a[1] + (b[1] - a[1]) * s / L)); break
    return out
PLEN = _len(PATH)
def _stroke(d, pts, w, fill):
    if len(pts) < 2: return
    d.line(pts, fill=fill, width=w)
    for x, y in pts[1:-1]: d.ellipse([x - w / 2, y - w / 2, x + w / 2, y + w / 2], fill=fill)

_cache = {}
def _base(pipe=True):
    if pipe in _cache: return _cache[pipe]
    im = Image.new("RGB", (DW, DH), NAVY); d = ImageDraw.Draw(im)
    for x in range(0, DW, 80): d.line([(x, 0), (x, DH)], fill=GRID, width=2)
    for y in range(0, DH, 80): d.line([(0, y), (DW, y)], fill=GRID, width=2)
    d.rectangle([WALL, 0, DW, DH], fill=(20, 36, 62))
    for y in range(-120, DH, 72): d.line([(WALL, y + 120), (DW, y)], fill=(44, 70, 110), width=6)
    d.polygon([(TX - 500, 260), (TX + 500, 260), (TX + 340, TOPY), (TX - 340, TOPY)], outline=LINE, width=16)
    d.rectangle([TX - 600, 224, TX + 600, 260], fill=LINE)
    d.line([(TX + 400, 224), (TX + 400, 80), (TX + 80, 80), (TX + 80, 140)], fill=LINE, width=32, joint="curve")
    if pipe:
        _stroke(d, PATH, PIPE, LINE); _stroke(d, PATH, INNER, NAVY)
        d.rectangle([TX - INNER // 2, TOPY - 12, TX + INNER // 2, TOPY + 20], fill=NAVY)
    _cache[pipe] = im
    return im
def _watermask():
    if "w" not in _cache:
        w = Image.new("L", (DW, DH), 0); _stroke(ImageDraw.Draw(w), PATH[:-1], INNER, 255); _cache["w"] = w
    return _cache["w"]
GAS_OPEN = list(reversed(PATH)) + [(TX, 120)]

def _label(im, font, text, xy, anchor, color=LINE, size=64, a=1.0):
    if a <= 0.02: return
    d = ImageDraw.Draw(im); t = text_layer(text, font, size, color, tracking=0.12)
    tx = xy[0] if anchor[0] > xy[0] + t.width else xy[0]
    end = (xy[0] + (t.width + 16 if anchor[0] > xy[0] else -16), xy[1] + t.height // 2)
    d.line([anchor, end], fill=color, width=6)
    r = 14 + 6 * math.sin(a * 9); d.ellipse([anchor[0] - r, anchor[1] - r, anchor[0] + r, anchor[1] + r], fill=color)
    im.paste(Image.new("RGB", (t.width + 36, t.height + 20), NAVY), (xy[0] - 18, xy[1] - 10)); im.paste(t, xy, t)

def ptrap(state, t, dur, font):
    """state: intro | fill | seal | dry | refill. Returns (RGB panel DW x DH, hud text or None, hud colour)."""
    k = min(1.0, t / max(0.1, dur)); hud, hud_c = None, YEL
    level = WEIR; draw_p = 1.0
    if state == "intro":
        draw_p = ease_in_out(min(1.0, t / 1.3))
        level = DRY + (WEIR - DRY) * ease_out(min(1.0, max(0.0, t - 1.2) / 0.9))
    if state == "dry":
        ev = ease_in_out(min(1.0, max(0.0, t - 0.4) / (dur * 0.5))); level = WEIR + (DRY - WEIR) * ev
        hud = f"DAY {1 + int(44 * ev)}  ·  DRAIN UNUSED"
    if state == "refill": level = DRY + (WEIR - DRY) * ease_in_out(min(1.0, max(0.0, t - 0.7) / (dur * 0.4)))
    tap = (state == "fill" and t > 0.25) or (state == "refill" and 0.4 < t < dur * 0.75)
    if draw_p < 1.0:
        im = _base(False).copy(); d = ImageDraw.Draw(im); part = _upto(PATH, PLEN * draw_p)
        _stroke(d, part, PIPE, LINE); _stroke(d, part, INNER, NAVY)
        x, y = part[-1]; d.ellipse([x - 26, y - 26, x + 26, y + 26], fill=YEL)
    else:
        im = _base(True).copy()
    w = _watermask().copy(); dw = ImageDraw.Draw(w); dw.rectangle([0, 0, DW, int(level)], fill=0)
    if draw_p < 1.0: w = Image.new("L", (DW, DH), 0); dw = ImageDraw.Draw(w)
    if tap:
        wob = 8 * math.sin(t * 18)
        dw.line([(TX + 80, 150), (TX + 80, TOPY - 130), (TX, TOPY)], fill=255, width=int(36 + wob), joint="curve")
        _stroke(dw, PATH[:2], int(INNER * 0.5), 255)
        if level <= WEIR + 4: dw.line([(RX, AY + INNER // 4), (WALL, AY + INNER // 4)], fill=255, width=INNER // 2)
    im.paste(Image.new("RGB", (DW, DH), WATER), (0, 0), w)
    d = ImageDraw.Draw(im)
    if tap:                                                    # flow dashes riding the current + splashes at the drain
        for i in range(14):
            s = (t * 620 + i * PLEN / 14) % PLEN; x, y = _along(PATH, s)
            if im.getpixel((int(min(DW - 1, x)), int(y)))[2] > 200: d.ellipse([x - 12, y - 12, x + 12, y + 12], fill=(200, 232, 255))
        for i in range(5):
            a = t * 9 + i * 1.3; r = 30 + 40 * ((t * 2 + i * 0.2) % 1)
            d.ellipse([TX + r * math.cos(a) - 7, TOPY - 30 - abs(r * math.sin(a)) * 0.6 - 7, TX + r * math.cos(a) + 7, TOPY - 30 - abs(r * math.sin(a)) * 0.6 + 7], fill=(160, 210, 255))
    elif draw_p >= 1.0 and level < DRY - 8:                    # resting surface shimmer
        for x in (TX, RX):
            d.line([(x - INNER // 2 + 8, level + 4 * math.sin(t * 5 + x)), (x + INNER // 2 - 8, level + 4 * math.cos(t * 5 + x))], fill=(200, 230, 255), width=8)
    if state == "dry" and WEIR + 6 < level < DRY - 2:          # evaporation wisps rising off both surfaces
        v = Image.new("RGBA", (DW, DH), (0, 0, 0, 0)); vd = ImageDraw.Draw(v)
        for x in (TX, RX):
            for i in range(4):
                p = (t * 0.7 + i / 4) % 1; yy = level - 30 - 260 * p; xx = x + 26 * math.sin(p * 7 + i)
                vd.arc([xx - 22, yy - 22, xx + 22, yy + 22], 200, 340, fill=(190, 225, 255, int(220 * (1 - p))), width=8)
        im.paste(v, (0, 0), v)
    open_ = level > CROWN + 12
    if state in ("seal", "dry", "refill"):
        path = GAS_OPEN if open_ else [(WALL, AY), (RX, AY), (RX, max(AY + 40, level - 44))]
        L = _len(path); n = 11 if open_ else 6
        g = Image.new("RGBA", (DW, DH), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
        for i in range(n):
            s = (t * 300 + i * L / n) % L; x, y = _along(path, s); r = 26 + 9 * math.sin(t * 6 + i)
            fade = 1.0 if open_ else min(1.0, (L - s) / 120); x += 18 * math.sin(t * 4 + i * 2)
            gd.ellipse([x - r, y - r, x + r, y + r], fill=GAS + (int(220 * fade),))
        if open_:                                              # it reaches the room: stink waves above the basin
            for i in range(3):
                p = (t * 0.8 + i / 3) % 1; yy = 200 - 150 * p; xx = TX - 160 + i * 160
                gd.arc([xx - 40, yy - 40, xx + 40, yy + 40], 250, 20, fill=GAS + (int(230 * (1 - p)),), width=12)
                gd.arc([xx - 40, yy - 110, xx + 40, yy - 30], 70, 200, fill=GAS + (int(230 * (1 - p)),), width=12)
        g = g.filter(ImageFilter.GaussianBlur(4)); im.paste(g, (0, 0), g)
        if state == "dry" and open_: hud, hud_c = "SEWER GAS IN THE ROOM", (255, 96, 80)
    pulse = 0.5 + 0.5 * math.sin(t * 5)
    if state == "intro" and t > 1.3:
        r = R + PIPE // 2 + 44 + 18 * pulse
        d.arc([TX + R - r, BY - r, TX + R + r, BY + r], 0, 180, fill=YEL, width=14)
        _label(im, font, "P-TRAP", (400, 1490), (TX + R - 60, BY + R + 80), YEL, 84, a=t - 1.3)
    sealed = level <= WEIR + 8
    if state in ("fill", "seal") and t > 0.5 or (state == "refill" and sealed):
        _label(im, font, "WATER SEAL", (TX + R - 215, 1480), (TX + R, BY + R - 30), WATER, 62, a=t)
    if state in ("seal", "dry", "refill") and t > 0.3:
        _label(im, font, "SEWER GAS", (1180, 650), (1440, AY - 12), GAS, 62, a=t)
    if state == "dry" and open_:
        _label(im, font, "NO WATER = NO SEAL", (TX + R - 360, 1490), (TX + R, BY + R - 16), YEL, 62, a=t)
    if (state == "seal" and t > 0.8) or (state == "refill" and sealed):
        x, y = RX, AY + 124; s = 52 + 8 * pulse
        d.line([(x - s, y - s), (x + s, y + s)], fill=YEL, width=18); d.line([(x - s, y + s), (x + s, y - s)], fill=YEL, width=18)
    if state == "refill" and sealed: hud, hud_c = "SEALED AGAIN", (120, 220, 120)
    t2 = text_layer("TO SEWER", font, 44, (120, 150, 190), tracking=0.14); im.paste(t2, (WALL - t2.width - 28, AY + 104), t2)
    return im, hud, hud_c
DIAGRAMS = {"ptrap": ptrap}
