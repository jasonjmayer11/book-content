"""Paint a closed steel jacket over the water-heater cutaway (crop coords), saved as RGBA overlay."""
import math, random
from PIL import Image, ImageDraw, ImageFilter
src = Image.open("assets/book/wh-clean.png").convert("RGB"); W, H = src.size
X0, X1, Y0, Y1 = 340, 836, 212, 1502; cx, R = (X0 + X1) / 2, (X1 - X0) / 2
sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); px = sh.load(); random.seed(7)
streak = [random.uniform(-9, 9) for _ in range(W)]
for x in range(X0, X1):
    u = (x - cx) / R; n = math.sqrt(max(0.0, 1 - u * u))
    b = 70 + 95 * n ** 0.8 + 70 * math.exp(-((u + .55) / .10) ** 2) + 95 * math.exp(-((u - .62) / .07) ** 2) - 40 * (abs(u) > .93)
    b += streak[x]
    for y in range(Y0, Y1):
        v = b + random.uniform(-4, 4)
        px[x, y] = (int(min(255, v * 1.02)), int(min(255, v * .99)), int(min(255, v * .96)), 255)
d = ImageDraw.Draw(sh)
for y, a in ((268, 70), (1418, 70)):                                    # rolled seams
    d.line([(X0 + 4, y), (X1 - 4, y)], fill=(40, 40, 42, a + 120), width=4); d.line([(X0 + 4, y + 4), (X1 - 4, y + 4)], fill=(235, 235, 235, 90), width=2)
d.ellipse([X0, Y0 - 26, X1, Y0 + 30], outline=(225, 222, 218, 220), width=5)   # top rim
d.rectangle([X0, Y1 - 70, X1, Y1], fill=(46, 46, 50, 255))               # base skirt
d.rounded_rectangle([cx - 120, Y1 - 160, cx + 120, Y1 - 40], radius=14, fill=(34, 35, 40, 255), outline=(150, 150, 150, 255), width=4)  # burner access door
d.ellipse([cx - 22, Y1 - 120, cx + 22, Y1 - 76], fill=(255, 150, 50, 255), outline=(90, 90, 90, 255), width=4)  # sight glass
d.rounded_rectangle([460, 470, 640, 700], radius=8, fill=(232, 230, 222, 255), outline=(150, 148, 140, 255), width=3)  # rating plate
d.rectangle([460, 470, 640, 515], fill=(196, 60, 46, 255))
for i, y in enumerate(range(540, 690, 22)): d.line([(478, y), (478 + (140 if i % 3 else 95), y)], fill=(120, 120, 120, 255), width=6)
sh = sh.filter(ImageFilter.GaussianBlur(0.6))
m = Image.new("L", (W, H), 0); ImageDraw.Draw(m).rounded_rectangle([X0, Y0 - 4, X1, Y1], radius=34, fill=255)
sh.putalpha(Image.composite(sh.getchannel("A"), Image.new("L", (W, H), 0), m))
box = (322, 1110, 428, 1312); sh.paste(src.crop(box).convert("RGBA"), box[:2])     # keep the controller on the front
sh.save("assets/book/wh-shell.png")
prev = src.convert("RGBA"); prev.alpha_composite(sh); prev.crop((280, 120, 940, 1528)).resize((330, 704)).convert("RGB").save("/tmp/shell.jpg")
