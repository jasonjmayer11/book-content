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


# ====================================================================== shared helpers
RED, DIM = (255, 96, 80), (70, 86, 112)
def _grid():
    if "grid" not in _cache:
        im = Image.new("RGB", (DW, DH), NAVY); d = ImageDraw.Draw(im)
        for x in range(0, DW, 80): d.line([(x, 0), (x, DH)], fill=GRID, width=2)
        for y in range(0, DH, 80): d.line([(0, y), (DW, y)], fill=GRID, width=2)
        _cache["grid"] = im
    return _cache["grid"].copy()
def _dots(d, path, t, n, speed, r, fill, frac=1.0):
    L = _len(path) * frac
    if L <= 1: return
    for i in range(n):
        x, y = _along(path, (t * speed + i * L / n) % L); d.ellipse([x - r, y - r, x + r, y + r], fill=fill)
def _txt(im, font, text, xy, color=LINE, size=56, center=False):
    t = text_layer(text, font, size, color, tracking=0.1); x = xy[0] - (t.width // 2 if center else 0)
    im.paste(t, (int(x), int(xy[1])), t)


# ====================================================================== main water shutoff
SP = [(0, 1500), (520, 1500), (760, 1500), (980, 1500), (980, 520), (1500, 520), (1500, 820)]
BURST, VALVE, METER = (1260, 520), (760, 1500), (520, 1500)
def shutoff(state, t, dur, font):
    """state: burst | locate | close | tag"""
    im = _grid(); d = ImageDraw.Draw(im); hud, hud_c = None, YEL
    d.rectangle([0, 1380, 360, DH], fill=(26, 34, 44))                                    # soil outside
    for x in range(-200, 360, 70): d.line([(x, DH), (x + 380, 1380)], fill=(44, 56, 70), width=5)
    d.line([(360, 380), (360, 1640), (1720, 1640), (1720, 380)], fill=LINE, width=16)       # walls + floor
    d.line([(300, 380), (1040, 110), (1780, 380), (300, 380)], fill=LINE, width=16)         # roof
    closing = 0.0
    if state == "close": closing = ease_in_out(min(1.0, max(0.0, t - dur * 0.35) / 0.9))
    if state == "tag": closing = 1.0 - ease_in_out(min(1.0, max(0.0, t - 0.5) / 0.9)) if t < dur * 0.5 else ease_in_out(min(1.0, (t - dur * 0.5) / 0.9)) * 0 
    if state == "tag": closing = 1.0 if t < 0.5 else max(0.0, 1.0 - ease_in_out((t - 0.5) / 0.9))
    is_open = closing < 0.5
    burst_on = state in ("burst", "locate") or (state == "close" and is_open)
    d.line(SP, fill=LINE, width=84); [d.ellipse([x - 42, y - 42, x + 42, y + 42], fill=LINE) for x, y in SP[1:-1]]
    d.line(SP, fill=NAVY, width=56); [d.ellipse([x - 28, y - 28, x + 28, y + 28], fill=NAVY) for x, y in SP[1:-1]]
    up = SP[:3]; down = SP[2:]
    d.line(up, fill=WATER, width=56)
    if state != "close" or closing < 1.0 or True:
        col = WATER if is_open else tuple(int(NAVY[i] + (WATER[i] - NAVY[i]) * max(0.0, 1 - (t - dur * 0.35 - 0.9) / 1.2 if state == "close" else 0.0)) for i in range(3))
        d.line(down, fill=col, width=56); [d.ellipse([x - 28, y - 28, x + 28, y + 28], fill=col) for x, y in down[1:-1]]
    if is_open:
        flow = SP[:5] + [BURST] if burst_on else SP
        _dots(d, flow, t, 16, 700, 11, (205, 235, 255))
    # faucet stub + the split pipe
    d.line([(1440, 820), (1560, 820)], fill=LINE, width=20)
    bx, by = BURST
    if state != "tag": d.polygon([(bx - 40, by + 44), (bx, by + 8), (bx + 40, by + 44)], fill=NAVY)
    if burst_on:
        leaked = t * 6.0 + (dur * 0.0)
        for i in range(26):
            p = (t * 1.3 + i / 26) % 1; a = -0.9 + 1.8 * ((i * 37) % 26) / 26
            x = bx + 260 * a * p; y = by + 40 + 1040 * p * p + 60 * p; r = 13 * (1 - 0.4 * p)
            d.ellipse([x - r, y - r, x + r, y + r], fill=WATER)
        pw = min(620, 160 + 60 * t) if state == "burst" else 620
        d.ellipse([bx - pw, 1596, bx + pw, 1650], fill=WATER)
        if state == "burst": hud, hud_c = f"MINUTE {int(t) + 1}  ·  {5 * (int(t) + 1)} GAL ON THE FLOOR", RED
    elif state != "tag":
        d.ellipse([bx - 620, 1602, bx + 620, 1646], fill=(40, 110, 180))
    # meter + valve
    mx, my = METER; d.ellipse([mx - 74, my - 74, mx + 74, my + 74], fill=NAVY, outline=LINE, width=12)
    a = t * (5 if is_open else 0); d.line([(mx, my), (mx + 50 * math.cos(a), my + 50 * math.sin(a))], fill=YEL, width=10)
    vx, vy = VALVE; d.ellipse([vx - 58, vy - 58, vx + 58, vy + 58], fill=LINE)
    ang = closing * math.pi / 2; hx, hy = 150 * math.cos(ang), -150 * math.sin(ang)
    hc = YEL if state != "burst" else LINE
    d.line([(vx, vy - 40), (vx + hx, vy - 40 + hy)], fill=hc, width=34); d.ellipse([vx - 24, vy - 64, vx + 24, vy - 16], fill=hc)
    pulse = 0.5 + 0.5 * math.sin(t * 5)
    if state == "locate":
        k = ease_in_out(min(1.0, t / (dur * 0.6))); hp = _upto(SP[:3], _len(SP[:3]) * k)
        if len(hp) > 1: d.line([(x, y - 110) for x, y in hp], fill=YEL, width=10)
        x, y = hp[-1]; d.polygon([(x + 34, y - 110), (x - 10, y - 140), (x - 10, y - 80)], fill=YEL)
        _txt(im, font, "STREET SIDE", (40, 1290), (150, 180, 215), 50)
        if t > dur * 0.35: _label(im, font, "WATER METER", (400, 1150), (mx, my - 84), LINE, 54, a=t)
        if t > dur * 0.6:
            r = 110 + 20 * pulse; d.ellipse([vx - r, vy - r - 20, vx + r, vy + r - 20], outline=YEL, width=12)
            _label(im, font, "MAIN SHUTOFF", (560, 1672), (vx, vy + 64), YEL, 64, a=t)
    if state == "close":
        _label(im, font, "MAIN SHUTOFF", (560, 1672), (vx, vy + 64), YEL, 64, a=t)
        if closing > 0.99: hud, hud_c = "WATER OFF", (120, 220, 120)
        elif t > dur * 0.2:
            d.arc([vx - 210, vy - 250, vx + 210, vy + 170], 270, 350, fill=YEL, width=12)
    if state == "tag":
        tg = ease_out(min(1.0, max(0.0, t - dur * 0.45) / 0.5))
        if tg > 0:
            sw = 14 * math.sin(t * 3); x0, y0 = vx + sw, vy + 70
            d.line([(vx, vy + 50), (x0, y0 + 40)], fill=LINE, width=6)
            d.rounded_rectangle([x0 - 130, y0 + 40, x0 + 130, y0 + 40 + int(120 * tg)], radius=16, fill=YEL)
            if tg > 0.9: _txt(im, font, "MAIN", (x0, y0 + 62), (10, 10, 10), 64, center=True)
        hud = "TURN IT ONCE, NOW" if t < dur * 0.45 else "THEN LABEL IT"
    return im, hud, hud_c


# ====================================================================== GFCI outlet
OX, OY = 520, 760
HOT = [(OX + 190, OY - 190), (1180, OY - 190), (1440, OY - 190)]
NEU = [(1440, OY + 190), (1180, OY + 190), (OX + 190, OY + 190)]
LEAK = [(1660, OY), (1760, OY), (1760, 1120)]
DOWN = [(OX, OY + 400), (OX, 1500), (1500, 1500)]
def _outlet(d, x, y, s, live, font_im=None):
    c = LINE if live else DIM
    d.rounded_rectangle([x - 190 * s, y - 330 * s, x + 190 * s, y + 330 * s], radius=int(50 * s), outline=c, width=max(4, int(14 * s)))
    for yy in (y - 190 * s, y + 190 * s):
        d.rounded_rectangle([x - 78 * s, yy - 54 * s, x - 46 * s, yy + 34 * s], radius=4, fill=c)
        d.rounded_rectangle([x + 46 * s, yy - 44 * s, x + 78 * s, yy + 34 * s], radius=4, fill=c)
        d.ellipse([x - 22 * s, yy + 44 * s, x + 22 * s, yy + 88 * s], fill=c)
def gfci(state, t, dur, font):
    """state: normal | leak | trip | reset | chain"""
    im = _grid(); d = ImageDraw.Draw(im); hud, hud_c = None, YEL
    trip_t = {"trip": 0.5, "chain": 0.0}.get(state)
    tripped = (state == "trip" and t > 0.5) or state == "chain" or (state == "reset" and t < dur * 0.5)
    live = not tripped
    leak = state == "leak" or (state == "trip" and t <= 0.5)
    wc = YEL if live else DIM
    d.line(HOT, fill=wc, width=18); d.line(NEU, fill=(LINE if live else DIM), width=18)
    d.line(DOWN, fill=(LINE if live else DIM), width=14)
    # appliance (hair dryer) at the end of the cord
    d.rounded_rectangle([1340, OY - 260, 1660, OY + 260], radius=40, outline=LINE, width=14)
    for i in range(4): d.line([(1400 + i * 66, OY - 150), (1400 + i * 66, OY + 150)], fill=(LINE if live else DIM), width=10)
    _txt(im, font, "HAIR DRYER", (1500, OY + 290), LINE, 50, center=True)
    _outlet(d, OX, OY, 1.0, True)
    # TEST / RESET buttons: RESET pops out when tripped
    d.rounded_rectangle([OX - 80, OY - 62, OX + 80, OY - 8], radius=10, fill=(40, 40, 40), outline=LINE, width=6)
    pop = 16 if tripped else 0
    if state == "reset" and t >= dur * 0.5 - 0.25: pop = int(16 * max(0.0, 1 - (t - (dur * 0.5 - 0.25)) / 0.25))
    d.rounded_rectangle([OX - 80 - pop // 2, OY + 8 - pop // 2, OX + 80 + pop // 2, OY + 62 + pop // 2], radius=10, fill=(RED if tripped else (120, 30, 30)), outline=LINE, width=6)
    _txt(im, font, "TEST", (OX, OY - 54), LINE, 30, center=True); _txt(im, font, "RESET", (OX, OY + 16), (255, 255, 255), 30, center=True)
    d.ellipse([OX + 110, OY - 14, OX + 138, OY + 14], fill=((120, 220, 120) if live else (60, 60, 60)))
    if live:
        _dots(d, HOT, t, 6, 420, 16, (255, 240, 150))
        _dots(d, NEU, t, 6 if not leak else 4, 420, 16, (255, 255, 255))
        _dots(d, DOWN, t, 6, 360, 10, (255, 240, 150))
    # downstream outlets on the same protected line
    for i, name in enumerate(("BATHROOM", "GARAGE", "OUTSIDE")):
        x = 820 + i * 300; d.line([(x, 1500), (x, 1440)], fill=(LINE if live else DIM), width=10)
        _outlet(d, x, 1330, 0.3, live); _txt(im, font, name, (x, 1540), (LINE if live else DIM), 36, center=True)
    if leak or (state == "trip" and t < 1.2):
        d.line(LEAK, fill=WATER, width=12)
        for i in range(3):                                           # water on the dryer
            yy = OY - 640 + ((t * 300 + i * 90) % 260); d.ellipse([1400 + i * 90 - 12, yy - 16, 1400 + i * 90 + 12, yy + 16], fill=WATER)
        if live: _dots(d, LEAK, t, 3, 380, 16, RED)
        d.line([(1690, 1120), (1830, 1120)], fill=LINE, width=10); d.line([(1715, 1150), (1805, 1150)], fill=LINE, width=10); d.line([(1740, 1180), (1780, 1180)], fill=LINE, width=10)
        _label(im, font, "LEAK", (1500, 1200), (1750, 1080), RED, 60, a=t)
    out_a, back_a = "5.000", ("4.994" if leak else "5.000")
    if not live: out_a = back_a = "0.000"
    _txt(im, font, f"OUT  {out_a} A", (760, OY - 300), YEL if live else DIM, 56)
    _txt(im, font, f"BACK {back_a} A", (760, OY + 230), (RED if leak else (LINE if live else DIM)), 56)
    if state == "normal": hud = "OUT = BACK"
    if state == "leak": hud, hud_c = "SOME IS MISSING", RED
    if state == "trip": hud, hud_c = ("SOME IS MISSING", RED) if t <= 0.5 else ("POWER CUT", (120, 220, 120))
    if state == "chain": hud, hud_c = "ALL OF THESE GO DEAD", RED
    if state == "reset":
        hud, hud_c = ("PRESS RESET", YEL) if t < dur * 0.5 else ("BACK ON", (120, 220, 120))
        if t < dur * 0.5:
            r = 120 + 26 * math.sin(t * 6); d.ellipse([OX - r, OY + 35 - r * 0.6, OX + r, OY + 35 + r * 0.6], outline=YEL, width=12)
    return im, hud, hud_c


# ====================================================================== furnace filter
FY0, FY1, FX = 560, 1160, 760
def airfilter(state, t, dur, font):
    """state: clean | clog | strain | swap"""
    im = _grid(); d = ImageDraw.Draw(im); hud, hud_c = None, YEL
    clog = 0.0
    if state == "clog": clog = ease_in_out(min(1.0, t / (dur * 0.8)))
    if state == "strain": clog = 1.0
    swap = ease_in_out(min(1.0, max(0.0, t - 0.4) / 1.0)) if state == "swap" else 0.0
    newin = ease_in_out(min(1.0, max(0.0, t - 1.5) / 1.0)) if state == "swap" else 0.0
    if state == "swap": clog = 1.0 if newin < 1 else 0.0
    flow = 1.0 - 0.62 * clog if not (state == "swap" and newin < 1.0) else 0.38
    if state == "swap" and newin >= 1.0: flow = 1.0
    d.line([(0, FY0), (1240, FY0)], fill=LINE, width=16); d.line([(0, FY1), (1240, FY1)], fill=LINE, width=16)   # return duct
    d.rounded_rectangle([1240, 380, 1760, 1340], radius=30, outline=LINE, width=16)                               # furnace cabinet
    d.line([(1400, 380), (1400, 0)], fill=LINE, width=16); d.line([(1620, 380), (1620, 0)], fill=LINE, width=16)  # supply up
    _txt(im, font, "FURNACE", (1500, 1370), LINE, 54, center=True); _txt(im, font, "AIR FROM YOUR ROOMS", (40, FY1 + 40), (150, 180, 215), 46)
    bx, by = 1500, 860; strain = state == "strain" or (state == "clog" and clog > 0.7)
    bc = RED if strain and math.sin(t * 9) > -0.2 else LINE
    d.ellipse([bx - 190, by - 190, bx + 190, by + 190], outline=bc, width=16)
    for i in range(6):
        a = t * (9 * flow + 1.5) + i * math.pi / 3
        d.line([(bx + 40 * math.cos(a), by + 40 * math.sin(a)), (bx + 160 * math.cos(a + 0.5), by + 160 * math.sin(a + 0.5))], fill=bc, width=18)
    # airflow streaks
    n = int(3 + 9 * flow)
    for i in range(n):
        y = FY0 + 70 + (FY1 - FY0 - 140) * i / max(1, n - 1); x = ((t * 900 * flow + i * 173) % 1200)
        d.line([(x, y), (x + 90 * flow + 20, y)], fill=(200, 225, 255), width=10)
    for i in range(max(2, int(8 * flow))):
        x = 1430 + (i % 3) * 80; y = 360 - ((t * 700 * flow + i * 97) % 360); d.line([(x, y), (x, y - 60 * flow - 12)], fill=(255, 190, 120), width=10)
    # dust riding in, stopping at the filter
    for i in range(16):
        p = (t * 0.5 + i / 16) % 1; x = FX - 30 - 760 * (1 - p); y = FY0 + 60 + ((i * 131) % (FY1 - FY0 - 120))
        d.ellipse([x - 12, y - 12, x + 12, y + 12], fill=(190, 150, 100))
    # the filter: pleated slab that slides out / in
    def slab(yoff, dirt, alpha_new=False):
        x0, x1 = FX - 34, FX + 34; y0, y1 = FY0 + 8 + yoff, FY1 - 8 + yoff
        base = tuple(int(245 - (245 - 95) * dirt) if j == 0 else int(245 - (245 - 75) * dirt) if j == 1 else int(240 - (240 - 55) * dirt) for j in range(3))
        d.rectangle([x0, y0, x1, y1], fill=base, outline=LINE, width=6)
        for yy in range(int(y0), int(y1) - 20, 40): d.line([(x0, yy), (x1, yy + 20), (x0, yy + 40)], fill=(150, 150, 150) if dirt < 0.5 else (60, 45, 30), width=5)
    if state == "swap":
        if swap < 1.0 or newin <= 0: slab(-760 * swap, 1.0)
        if swap >= 1.0 or newin > 0: slab(-760 * (1 - newin), 0.0)
    else: slab(0, clog)
    d.line([(FX - 60, FY0), (FX + 60, FY0)], fill=NAVY, width=18)                                              # the slot
    pulse = 0.5 + 0.5 * math.sin(t * 5)
    if state == "clean":
        _label(im, font, "FILTER", (FX - 110, 300), (FX, FY0 + 30), YEL, 70, a=t)
        _label(im, font, "BLOWER", (1300, 1150), (bx - 60, by + 150), LINE, 54, a=t)
        hud = "AIRFLOW 100%"
    if state == "clog": hud, hud_c = f"MONTH {1 + int(8 * clog)}  ·  AIRFLOW {int(100 * flow)}%", (RED if clog > 0.6 else YEL)
    if state == "strain":
        hud, hud_c = "WORKING HARDER", RED
        r = 240 + 30 * pulse; d.ellipse([bx - r, by - r, bx + r, by + r], outline=RED, width=10)
        k = ease_out(min(1.0, t / (dur * 0.7)))
        d.rounded_rectangle([200, 180, 760, 420], radius=24, outline=LINE, width=10)
        _txt(im, font, "ENERGY BILL", (480, 205), LINE, 50, center=True); _txt(im, font, f"${int(140 + 62 * k)}", (480, 280), RED, 110, center=True)
    if state == "swap":
        if newin >= 1.0:
            hud, hud_c = "EVERY 1 TO 3 MONTHS", (120, 220, 120)
            _label(im, font, "SIZE IS PRINTED ON THE EDGE", (120, 300), (FX - 20, FY0 + 60), YEL, 52, a=t)
        else: hud = "SLIDE THE OLD ONE OUT"
    return im, hud, hud_c

DIAGRAMS.update({"shutoff": shutoff, "gfci": gfci, "filter": airfilter})
