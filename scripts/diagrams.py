"""Animated engineering diagrams (blueprint style) for 'how it works' explainer reels."""
import math
from PIL import Image, ImageDraw, ImageFilter
from reelkit import text_layer, ease_in_out, ease_out

NAVY, GRID, LINE, WATER, GAS, YEL = (10, 22, 40), (24, 44, 74), (252, 238, 201), (58, 160, 255), (170, 220, 60), (252, 211, 3)
PW, PH = 920, 880
TX, RX, BY, AY, R, TOPY = 380, 540, 600, 450, 80, 250         # tailpiece x, riser x, bend centre y, arm y, bend radius, drain y
PIPE, INNER = 76, 58
WEIR, CROWN, DRY = AY + INNER // 2, BY + R - INNER // 2, BY + R + 12

def _path(n=40):
    pts = [(TX, TOPY), (TX, BY)]
    pts += [(TX + R - R * math.cos(math.pi * i / n), BY + R * math.sin(math.pi * i / n)) for i in range(1, n + 1)]
    pts += [(RX, AY), (PW - 60, AY)]
    return pts
PATH = _path()
def _stroke(d, pts, w, fill):
    d.line(pts, fill=fill, width=w)
    for x, y in pts[1:-1]: d.ellipse([x - w / 2, y - w / 2, x + w / 2, y + w / 2], fill=fill)
def _along(pts, s):
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        L = math.hypot(x1 - x0, y1 - y0)
        if s <= L: return x0 + (x1 - x0) * s / L, y0 + (y1 - y0) * s / L
        s -= L
    return pts[-1]
def _len(pts): return sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:]))

def _base():
    im = Image.new("RGB", (PW, PH), NAVY); d = ImageDraw.Draw(im)
    for x in range(0, PW, 40): d.line([(x, 0), (x, PH)], fill=GRID, width=1)
    for y in range(0, PH, 40): d.line([(0, y), (PW, y)], fill=GRID, width=1)
    d.rectangle([PW - 60, 0, PW, PH], fill=(20, 36, 62))                       # wall
    for y in range(-60, PH, 36): d.line([(PW - 60, y + 60), (PW, y)], fill=(44, 70, 110), width=3)
    d.polygon([(TX - 250, 130), (TX + 250, 130), (TX + 170, TOPY), (TX - 170, TOPY)], outline=LINE, width=8)   # basin
    d.rectangle([TX - 300, 112, TX + 300, 130], fill=LINE)                                         # counter
    d.line([(TX + 200, 112), (TX + 200, 40), (TX + 40, 40), (TX + 40, 70)], fill=LINE, width=16, joint="curve")   # faucet
    _stroke(d, PATH, PIPE, LINE); _stroke(d, PATH, INNER, NAVY)
    d.rectangle([TX - INNER // 2, TOPY - 6, TX + INNER // 2, TOPY + 10], fill=NAVY)
    return im
BASE = None
GASPATH_OPEN = list(reversed(PATH)) + [(TX, 60)]

def _label(im, text, xy, anchor_xy, color=LINE, size=34):
    d = ImageDraw.Draw(im); t = text_layer(text, FONT, size, color, tracking=0.12)
    d.line([anchor_xy, (xy[0] + (0 if anchor_xy[0] < xy[0] else t.width), xy[1] + t.height // 2)], fill=color, width=3)
    d.ellipse([anchor_xy[0] - 7, anchor_xy[1] - 7, anchor_xy[0] + 7, anchor_xy[1] + 7], fill=color)
    bg = Image.new("RGB", (t.width + 20, t.height + 10), NAVY); im.paste(bg, (xy[0] - 10, xy[1] - 5)); im.paste(t, xy, t)
FONT = None

def ptrap(state, t, dur, font_path):
    """state: intro | fill | seal | dry | refill. Returns an RGB panel PW x PH."""
    global BASE, FONT
    FONT = font_path
    if BASE is None: BASE = _base()
    im = BASE.copy(); k = min(1.0, t / max(0.1, dur))
    level = WEIR
    if state == "dry": level = WEIR + (DRY - WEIR) * ease_in_out(min(1.0, t / (dur * 0.55)))
    if state == "refill": level = DRY + (WEIR - DRY) * ease_in_out(min(1.0, max(0.0, t - 0.5) / (dur * 0.45)))
    tap = state in ("fill", "refill") and t > 0.3
    # water in the bend: inner stroke of the pipe, kept only below the surface
    w = Image.new("L", (PW, PH), 0); _stroke(ImageDraw.Draw(w), PATH[:-1], INNER, 255)
    ImageDraw.Draw(w).rectangle([0, 0, PW, int(level)], fill=0)
    if tap:                                                    # flowing: stream, full tailpiece and arm
        dw = ImageDraw.Draw(w); wob = 4 * math.sin(t * 18)
        dw.line([(TX + 40, 78), (TX + 40, TOPY - 60), (TX, TOPY)], fill=255, width=int(18 + wob), joint="curve")
        _stroke(dw, PATH[:2], int(INNER * 0.5), 255)
        if level <= WEIR + 2: dw.line([(RX, AY + INNER // 4), (PW - 60, AY + INNER // 4)], fill=255, width=INNER // 2)
    im.paste(Image.new("RGB", (PW, PH), WATER), (0, 0), w)
    d = ImageDraw.Draw(im)
    if not tap and level < DRY - 4:                            # surface shimmer
        for x in (TX, RX):
            if level < CROWN or True: d.line([(x - INNER // 2 + 4, level + 2 * math.sin(t * 5 + x)), (x + INNER // 2 - 4, level + 2 * math.cos(t * 5 + x))], fill=(190, 225, 255), width=4)
    # sewer gas puffs
    if state in ("seal", "dry", "refill"):
        open_ = level > CROWN + 6
        if open_: path = GASPATH_OPEN
        else: path = [(PW - 60, AY), (RX, AY), (RX, max(AY + 20, level - 22))]
        L = _len(path); n = 9 if open_ else 6
        g = Image.new("RGBA", (PW, PH), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
        for i in range(n):
            s = ((t * 150 + i * L / n) % L)
            x, y = _along(path, s); r = 13 + 4 * math.sin(t * 6 + i)
            fade = 1.0 if open_ else min(1.0, (L - s) / 60)
            gd.ellipse([x - r + 10 * math.sin(t * 4 + i * 2), y - r, x + r + 10 * math.sin(t * 4 + i * 2), y + r], fill=GAS + (int(215 * fade),))
        im.paste(g.filter(ImageFilter.GaussianBlur(3)), (0, 0), g.filter(ImageFilter.GaussianBlur(3)))
    # callouts
    pulse = 0.5 + 0.5 * math.sin(t * 5)
    if state == "intro":
        r = R + PIPE // 2 + 24 + 8 * pulse
        d.arc([TX + R - r, BY - r, TX + R + r, BY + r], 0, 180, fill=YEL, width=7)
        _label(im, "P-TRAP", (90, 760), (TX + R - 60, BY + R + 30), YEL, 44)
    if state in ("fill", "seal") or (state == "refill" and level <= WEIR + 4):
        _label(im, "WATER SEAL", (70, 560), (TX - 10, BY + 30), WATER, 34)
    if state in ("seal", "dry", "refill"):
        _label(im, "SEWER GAS", (600, 330), (720, AY - 6), GAS, 34)
    if state == "dry" and level > CROWN + 6:
        _label(im, "NO WATER = NO SEAL", (70, 760), (TX + R, BY + R - 10), YEL, 34)
    if state == "seal" or (state == "refill" and level <= WEIR + 4):
        x, y = RX, AY + 62
        d.line([(x - 26, y - 26), (x + 26, y + 26)], fill=YEL, width=9); d.line([(x - 26, y + 26), (x + 26, y - 26)], fill=YEL, width=9)
    t2 = text_layer("TO SEWER", FONT, 24, (120, 150, 190), tracking=0.14); im.paste(t2, (PW - 60 - t2.width - 14, AY + 52), t2)
    return im
DIAGRAMS = {"ptrap": ptrap}
