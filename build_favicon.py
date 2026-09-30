#!/usr/bin/env python3
"""Render favicon PNGs and a multi-size .ico that match favicon.svg design.
Design space is 64x64; all coordinates are scaled by size/64.
"""
from PIL import Image, ImageDraw

# Coordinates in 64x64 design space (must match favicon.svg)
BG_TOP = (59, 130, 246)      # #3b82f6
BG_BOTTOM = (37, 99, 235)    # #2563eb
BOOK = [(14, 24), (32, 28), (50, 24), (50, 41), (32, 45), (14, 41)]
SPINE = [(32, 28), (32, 45)]
LINE_L = [(18, 30), (28, 32)]
LINE_R = [(36, 32), (46, 30)]
LINE_COL = (191, 219, 254, 255)   # #bfdbfe
SPARKLE = [(48, 12), (50, 16), (54, 18), (50, 20), (48, 24), (46, 20), (42, 18), (46, 16)]
SPARK_COL = (253, 230, 138, 255)  # #fde68a
WHITE = (255, 255, 255, 255)


def rounded_gradient(size, radius, c_top, c_bottom):
    w = h = size
    # vertical gradient built as 1xh then stretched
    grad = Image.new("RGBA", (1, h))
    px = grad.load()
    for y in range(h):
        t = y / (h - 1)
        r = int(c_top[0] + (c_bottom[0] - c_top[0]) * t)
        g = int(c_top[1] + (c_bottom[1] - c_top[1]) * t)
        b = int(c_top[2] + (c_bottom[2] - c_top[2]) * t)
        px[0, y] = (r, g, b, 255)
    grad = grad.resize((w, h))
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, w - 1, h - 1], radius=radius, fill=255)
    base = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    base.paste(grad, (0, 0), mask)
    return base


def render(size):
    s = float(size)
    scale = s / 64.0
    radius = 14 * scale
    img = rounded_gradient(size, int(round(radius)), BG_TOP, BG_BOTTOM)
    d = ImageDraw.Draw(img)

    def p(pt):
        return (pt[0] * scale, pt[1] * scale)

    # book
    d.polygon([p(c) for c in BOOK], fill=WHITE)
    lw = max(1.0, 1.4 * scale)
    d.line([p(SPINE[0]), p(SPINE[1])], fill=LINE_COL, width=int(round(lw)))
    d.line([p(LINE_L[0]), p(LINE_L[1])], fill=LINE_COL, width=int(round(lw)))
    d.line([p(LINE_R[0]), p(LINE_R[1])], fill=LINE_COL, width=int(round(lw)))
    # sparkle
    d.polygon([p(c) for c in SPARKLE], fill=SPARK_COL)
    return img


# High-res master for ICO
master = render(256)
ico_sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
master.save("favicon.ico", format="ICO", sizes=ico_sizes)
print("wrote favicon.ico")

# Apple touch icon (180x180) and high-res PNGs for shortcuts / PWA
render(180).save("apple-touch-icon.png", format="PNG")
render(192).save("icon-192.png", format="PNG")
render(512).save("icon-512.png", format="PNG")
print("wrote apple-touch-icon.png, icon-192.png, icon-512.png")
