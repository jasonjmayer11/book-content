"""Stitch 4 browser screenshot tiles (canvas rows 0,600,1200,1302) into a 1080x1920 image. usage: out.png t0 t1 t2 t3"""
import sys
from PIL import Image
out = Image.new("RGB", (1080, 1920))
for f, y in zip(sys.argv[2:6], (0, 600, 1200, 1302)): out.paste(Image.open(f).convert("RGB").crop((0, 0, 1080, 618)), (0, y))
out.save(sys.argv[1])
