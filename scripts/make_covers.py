"""Paint the 'closed' exterior over each cutaway (1080x1920 crop coords) as an RGBA overlay for the reveal wipe."""
import random, math
from PIL import Image, ImageDraw, ImageFilter
random.seed(3)
A = "assets/book/"
def noise(im, amt=6):
    px = im.load(); w, h = im.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a: n = random.randint(-amt, amt); px[x, y] = (max(0, min(255, r + n)), max(0, min(255, g + n)), max(0, min(255, b + n)), a)
    return im
def vgrad(w, h, top, bot):
    g = Image.new("RGBA", (w, h)); d = ImageDraw.Draw(g)
    for y in range(h): t = y / max(1, h - 1); d.line([(0, y), (w, y)], fill=tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3)) + (255,))
    return g
def hgrad_shade(im, edge=0.18):          # darken left/right edges a little: reads as a solid object
    w, h = im.size; m = Image.new("L", (w, h), 0); d = ImageDraw.Draw(m)
    for x in range(w):
        u = abs(x / (w - 1) - .5) * 2; d.line([(x, 0), (x, h)], fill=int(255 * max(0, u - (1 - edge)) / edge * .5))
    dark = Image.new("RGBA", (w, h), (0, 0, 0, 255)); im.paste(Image.composite(dark, im, m), (0, 0)); return im
def save(ov, name, src):
    ov.save(A + name + "-cover.png")
    pv = Image.open(A + src + ".png").convert("RGBA"); pv.alpha_composite(ov); pv.resize((270, 480)).convert("RGB").save(f"/tmp/cov-{name}.jpg")

# furnace: closed front panel with louvers
ov = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0)); x0, y0, x1, y1 = 266, 404, 828, 1752
p = noise(vgrad(x1 - x0, y1 - y0, (70, 72, 78), (46, 48, 54)), 4); hgrad_shade(p); d = ImageDraw.Draw(p); w, h = p.size
d.line([(0, 640), (w, 640)], fill=(28, 29, 33, 255), width=6); d.line([(0, 646), (w, 646)], fill=(98, 100, 106, 255), width=2)   # two doors
for i in range(9):                                                                 # louvers on the lower door
    yy = 760 + i * 34; d.rounded_rectangle([90, yy, w - 90, yy + 14], radius=7, fill=(26, 27, 31, 255)); d.line([(92, yy + 15), (w - 92, yy + 15)], fill=(110, 112, 118, 255), width=2)
for cx in (40, w - 40):
    for cy in (40, 600, 690, h - 40): d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=(150, 152, 158, 255)); d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(60, 60, 64, 255))
d.rounded_rectangle([w // 2 - 46, 470, w // 2 + 46, 530], radius=10, fill=(16, 18, 26, 255), outline=(120, 122, 128, 255), width=3)  # sight window
d.ellipse([w // 2 - 22, 488, w // 2 + 22, 512], fill=(70, 120, 255, 255))
d.rounded_rectangle([120, 160, 300, 260], radius=6, fill=(214, 212, 204, 255)); d.rectangle([120, 160, 300, 186], fill=(40, 90, 160, 255))
for k in range(3): d.line([(136, 206 + k * 18), (270 - k * 30, 206 + k * 18)], fill=(130, 130, 130, 255), width=5)
ov.paste(p.filter(ImageFilter.GaussianBlur(.5)), (x0, y0)); save(ov, "furnace", "furnace")

# electrical panel: closed gray door (dead front)
ov = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0)); x0, y0, x1, y1 = 190, 50, 870, 1838
p = noise(vgrad(x1 - x0, y1 - y0, (150, 153, 156), (112, 115, 118)), 4); hgrad_shade(p, .12); d = ImageDraw.Draw(p); w, h = p.size
d.rectangle([0, 0, w - 1, h - 1], outline=(70, 72, 76, 255), width=8); d.rectangle([22, 22, w - 23, h - 23], outline=(170, 173, 176, 255), width=3)
d.rounded_rectangle([w - 90, h // 2 - 70, w - 50, h // 2 + 70], radius=10, fill=(60, 62, 66, 255)); d.rectangle([w - 76, h // 2 - 20, w - 64, h // 2 + 20], fill=(25, 25, 28, 255))   # latch
d.rounded_rectangle([90, 140, 420, 330], radius=6, fill=(236, 234, 226, 255)); d.rectangle([90, 140, 420, 176], fill=(200, 60, 46, 255))
for k in range(5): d.line([(108, 206 + k * 24), (380 - (k % 2) * 90, 206 + k * 24)], fill=(140, 140, 140, 255), width=6)
for cx, cy in ((60, 60), (w - 60, 60), (60, h - 60), (w - 60, h - 60)): d.ellipse([cx - 11, cy - 11, cx + 11, cy + 11], fill=(190, 192, 196, 255), outline=(80, 80, 84, 255), width=3)
ov.paste(p.filter(ImageFilter.GaussianBlur(.5)), (x0, y0)); save(ov, "panel", "panel")

# toilet: closed porcelain tank with its lid on, floating lid hidden
src = Image.open(A + "toilet.png").convert("RGBA")
ov = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
bg = src.crop((0, 40, 150, 260)); 
for xx in range(760, 1080, 150): ov.paste(bg, (xx, 40))                         # cover the floating lid with wall tile
x0, y0, x1, y1 = 150, 196, 922, 952
p = vgrad(x1 - x0, y1 - y0, (236, 238, 242), (200, 204, 212)); hgrad_shade(p, .2); w, h = p.size
m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).polygon([(0, 0), (w, 0), (w - 30, h), (40, h)], fill=255)
p.putalpha(m); d = ImageDraw.Draw(p)
hl = Image.new("RGBA", (w, h), (0, 0, 0, 0)); hd = ImageDraw.Draw(hl)
for x in range(60, w - 60, 3):                                                     # soft highlight band
    a = int(60 * math.exp(-((x - w * .3) / 70) ** 2)); hd.line([(x, 20), (x - 6, h - 20)], fill=(255, 255, 255, a))
p.alpha_composite(hl); p.putalpha(m)
ov.alpha_composite(p, (x0, y0)); d = ImageDraw.Draw(ov)
d.rounded_rectangle([x0 - 16, y0 - 34, x1 + 16, y0 + 18], radius=18, fill=(244, 246, 250, 255), outline=(170, 176, 186, 255), width=3)  # lid
src_handle = src.crop((55, 320, 240, 390)); ov.alpha_composite(src_handle, (55, 320))                                        # keep the handle in front
save(ov.filter(ImageFilter.GaussianBlur(.4)), "toilet", "toilet")

# attic: gable end closed with lap siding and a louvered vent
ov = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0)); tri = [(612, 236), (1080, 905), (1080, 1365), (0, 1365), (0, 880)]
p = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0)); d = ImageDraw.Draw(p)
for y in range(200, 1380, 46):
    d.rectangle([0, y, 1080, y + 46], fill=(214, 206, 190, 255)); d.line([(0, y + 44), (1080, y + 44)], fill=(150, 142, 128, 255), width=4); d.line([(0, y + 2), (1080, y + 2)], fill=(236, 230, 218, 255), width=2)
d.polygon([(470, 640), (612, 470), (754, 640)], fill=(60, 58, 54, 255))
for i in range(6): yy = 520 + i * 20; d.line([(612 - (yy - 470) * .83 + 8, yy), (612 + (yy - 470) * .83 - 8, yy)], fill=(160, 154, 142, 255), width=6)
m = Image.new("L", (1080, 1920), 0); ImageDraw.Draw(m).polygon(tri, fill=255); p.putalpha(m)
p = noise(p, 3); d = ImageDraw.Draw(p); d.line(tri[:2], fill=(240, 236, 228, 255), width=18); d.line([tri[0], tri[4]], fill=(240, 236, 228, 255), width=18)   # fascia trim
d.rectangle([0, 1330, 1080, 1366], fill=(240, 236, 228, 255))
ov.alpha_composite(p); save(ov, "attic", "attic")

# septic: plain soil over everything underground (lids stay visible at the surface)
src = Image.open(A + "septic.png").convert("RGBA"); W, H = 1080, 1920
soil = Image.new("RGB", (W, H)); sd = ImageDraw.Draw(soil)
for y in range(H):
    t = min(1, max(0, (y - 200) / 1500)); sd.line([(0, y), (W, y)], fill=(int(58 + 60 * t), int(40 + 22 * t), int(28 + 8 * t)))
for _ in range(9000):                                                              # clods and pebbles
    x, y = random.randint(0, W), random.randint(200, H); r = random.choice((2, 3, 4, 6, 9)); v = random.randint(-30, 30)
    base = soil.getpixel((min(W - 1, x), min(H - 1, y))); sd.ellipse([x - r, y - r, x + r, y + r], fill=tuple(max(0, min(255, c + v)) for c in base))
for _ in range(500):
    x, y = random.randint(0, W), random.randint(260, H); r = random.randint(3, 7); g = random.randint(120, 170); sd.ellipse([x - r, y - r * .8, x + r, y + r * .8], fill=(g, g - 8, g - 20))
soil = soil.filter(ImageFilter.GaussianBlur(1.1)).convert("RGBA")
ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ov.alpha_composite(soil.crop((0, 200, W, H)), (0, 200))
top = src.crop((0, 0, W, 300)); fm = Image.new("L", (W, 300), 255); ImageDraw.Draw(fm)
for i in range(60): ImageDraw.Draw(fm).line([(0, 240 + i), (W, 240 + i)], fill=int(255 * (1 - i / 60)))
ov.paste(top, (0, 0), fm)                                                          # house, grass and roots as they are
save(ov, "septic", "septic")
