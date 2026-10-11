"""Build the small GO2 icon: the hero loop rendered at icon scale.

Same real-mesh geometry, reveal ranks and schedule as build_hero.py, with far
fewer, larger dots so the robot still reads at about 40 px tall.
"""

import os

import build_hero as bh

bh.W, bh.H = 240, 176
bh.N_DOTS = 5_000
bh.DOT_MULT = 2.2
bh.DRIFT = bh.DRIFT * (bh.W / 1520)

if __name__ == "__main__":
    os.makedirs(bh.OUT, exist_ok=True)
    for theme in ("light", "dark"):
        ims, dur = bh.frames(theme)
        ims = bh.pad_uniform([bh.posterize(im) for im in ims], margin=4)
        path = os.path.join(bh.OUT, f"icon-{theme}.webp")
        ims[0].save(path, save_all=True, append_images=ims[1:], duration=dur,
                    loop=0, quality=80, method=6, minimize_size=True)
        print(f"[{theme}] {ims[0].size}  {os.path.getsize(path)/1e3:.0f} KB")
