"""Extract the blue magnifying-glass badge from logo.png and write a multi-size
favicon.ico.  We auto-detect the badge by locating the "dark blue" cluster on
the right half of the logo, tighten the bbox into a square, and downsample.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image

SRC = "/Users/bytedance/Desktop/工作文件/iclr-VAR/VARestorer-proj/static/images/logo.png"
OUT = "/Users/bytedance/Desktop/工作文件/iclr-VAR/VARestorer-proj/static/images/favicon.ico"
DEBUG_PNG = os.path.join(os.path.dirname(__file__), "favicon_preview.png")

img = Image.open(SRC).convert("RGBA")
W, H = img.size
arr = np.array(img)
r, g, b, a = arr[..., 0], arr[..., 1], arr[..., 2], arr[..., 3]

# "Dark blue" mask: saturated blue region that forms the badge. We also require
# the pixel to be opaque so we ignore the transparent background.
is_blue = (b > 110) & (r < 100) & (g < 130) & (a > 200)

# Limit search to the top-right quadrant of the logo.  The badge sits inside
# the upper illustration (top ~62% of the image) on the right side; restricting
# the search avoids catching the blue "VARestorer" wordmark at the bottom.
mask = np.zeros_like(is_blue)
y_cut = int(H * 0.62)
mask[:y_cut, W // 2:] = is_blue[:y_cut, W // 2:]

# Find the largest connected dark-blue blob on the right half via bbox of all
# qualifying pixels.  This is fine because the rightmost blue cluster is the
# magnifying-glass body.
ys, xs = np.where(mask)
if len(xs) == 0:
    raise RuntimeError("could not locate the magnifying-glass badge")
x0, x1 = int(xs.min()), int(xs.max())
y0, y1 = int(ys.min()), int(ys.max())
print(f"detected blue bbox: ({x0},{y0})-({x1},{y1})  size={x1-x0}x{y1-y0}")

# Expand by ~10% margin so the glossy highlight and white star + handle have
# breathing room at the edges of the tile.
pad = int(max(x1 - x0, y1 - y0) * 0.10)
x0 = max(0, x0 - pad)
y0 = max(0, y0 - pad)
x1 = min(W, x1 + pad)
y1 = min(H, y1 + pad)

# Make it perfectly square by expanding the shorter side around the center.
side = max(x1 - x0, y1 - y0)
cx = (x0 + x1) // 2
cy = (y0 + y1) // 2
x0 = max(0, cx - side // 2)
y0 = max(0, cy - side // 2)
x1 = x0 + side
y1 = y0 + side
# Shift back if we went past the right/bottom edge.
if x1 > W:
    x0 -= (x1 - W); x1 = W
if y1 > H:
    y0 -= (y1 - H); y1 = H
x0 = max(0, x0); y0 = max(0, y0)
print(f"square crop: ({x0},{y0})-({x1},{y1})  size={x1-x0}x{y1-y0}")

tile = img.crop((x0, y0, x1, y1))

# High-quality down-sampled preview so we can eyeball the result.
preview = tile.resize((256, 256), Image.LANCZOS)
preview.save(DEBUG_PNG)
print(f"preview -> {DEBUG_PNG}")

# Write a multi-resolution ICO.  Pillow picks the right downscale for each size.
sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
tile.save(OUT, format="ICO", sizes=sizes)
print(f"wrote {OUT}  sizes={sizes}")
