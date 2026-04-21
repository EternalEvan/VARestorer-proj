"""Render the 16x16 / 32x32 / 48x48 frames from favicon.ico upscaled so we can
eyeball how the tab icon will actually read in a browser.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image

ICO = "/Users/bytedance/Desktop/工作文件/iclr-VAR/VARestorer-proj/static/images/favicon.ico"
OUT = os.path.join(os.path.dirname(__file__), "favicon_check.png")

img = Image.open(ICO)
frames = {}
# .ico is a multi-image file: iterate size metadata.
for sz in img.ico.sizes():
    img.size = sz
    frames[sz] = img.copy()
print("sizes in ico:", sorted(frames))

targets = [(16, 16), (32, 32), (48, 48)]
# Upscale each small frame by 8x with nearest-neighbor so we see actual pixel grid.
upscaled = []
for sz in targets:
    f = frames[sz].resize((sz[0] * 8, sz[1] * 8), Image.NEAREST)
    upscaled.append(f)

pad = 20
w = sum(f.width for f in upscaled) + pad * (len(upscaled) + 1)
h = max(f.height for f in upscaled) + pad * 2
canvas = Image.new("RGBA", (w, h), (245, 245, 245, 255))
x = pad
for f in upscaled:
    canvas.paste(f, (x, pad), f if f.mode == "RGBA" else None)
    x += f.width + pad
canvas.save(OUT)
print("wrote", OUT)
