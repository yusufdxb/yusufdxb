"""Build the hero assets: assets/readme/hero.gif and assets/readme/hero.png.

The loop is deliberately front-loaded: it opens on the fully acquired frame and
holds there for about two seconds, so a viewer who sees only the first frame
(reduced motion, a social card, a static mirror) sees the finished image. The
hold is a handful of long-delay frames, which keeps the file small.
"""

import argparse
import os
import subprocess
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_hero as rh

OUT_W = 1600          # 2x the 800px display width used in the README

# (phase, milliseconds) - phases match the timeline in render_hero.py
SCHEDULE = []
for i in range(6):                                   # hold, acquired
    SCHEDULE.append((i * 0.065, 300))
for i in range(4):                                   # decay to raw return
    SCHEDULE.append((0.42 + i * 0.02, 70))
for i in range(26):                                  # scan sweep
    SCHEDULE.append((0.50 + i * (0.40 / 26), 65))
for i in range(9):                                   # telemetry settles back in
    SCHEDULE.append((0.90 + i * 0.011, 90))


def build(out_gif, out_png, colors=128):
    frames = []
    for n, (phase, _) in enumerate(SCHEDULE):
        im = rh.render(phase, tick=n)
        if im.width != OUT_W:
            im = im.resize((OUT_W, round(im.height * OUT_W / im.width)), Image.LANCZOS)
        frames.append(im)

    frames[0].quantize(colors=256, method=Image.MEDIANCUT).save(
        out_png, optimize=True)

    pal = frames[0].quantize(colors=colors, method=Image.MEDIANCUT)
    pframes = [f.quantize(palette=pal, dither=Image.Dither.NONE) for f in frames]
    pframes[0].save(out_gif, save_all=True, append_images=pframes[1:],
                    duration=[d for _, d in SCHEDULE], loop=0,
                    optimize=True, disposal=1)

    total = sum(d for _, d in SCHEDULE) / 1000
    size = os.path.getsize(out_gif) / 1e6
    print(f"{out_gif}: {len(frames)} frames, {total:.2f}s loop, "
          f"{frames[0].width}x{frames[0].height}, {size:.2f} MB")
    print(f"{out_png}: {os.path.getsize(out_png) / 1e6:.2f} MB")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "readme"))
    ap.add_argument("--colors", type=int, default=128)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    build(os.path.join(a.out, "hero.gif"), os.path.join(a.out, "hero.png"), a.colors)
