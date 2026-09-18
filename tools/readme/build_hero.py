"""Build the hero art: a GO2 resolving out of drifting dust.

The geometry is the real Unitree visual mesh (see go2_asset.py). Only which
surface samples are drawn, and how far they have lifted off the surface,
changes over the loop.

Motion model: every particle gets a phase from a smooth spatial field and
lifts exactly once per loop, so at any instant a small, slowly migrating
fraction of the surface is dust. The machine is never less than about 85%
resolved, there is no scan front, and every frame stands on its own as a still.
"""

import os
import sys

import numpy as np
from PIL import Image

import gorender as gr
import particles as pa
import scene as sc

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "assets", "readme")

DISPLAY_W = 430                  # width the README renders the art at
W, H = DISPLAY_W * 2, 400 * 2    # 2x asset
SS = 2
N_DOTS = 24_000

CAM = dict(azim=50, elev=3, dist=2.85, target=(0.02, 0.0, 0.215), focal_mm=100)

FRAMES = 24
FRAME_MS = 330                   # ~7.9 s loop
LIFT_SHARE = 0.17                # fraction of the surface that is dust at once
DRIFT = 24.0 * (W / 430)
DIR_BIAS = np.array([0.92, -0.25])


def build_field():
    npz = os.path.join(HERE, "go2_posed.npz")
    if not os.path.exists(npz):
        raise SystemExit("run go2_asset.py first to build go2_posed.npz")
    d = np.load(npz)
    V, F, FT = d["V"].astype(np.float64), d["F"], d["FT"]
    pts, nrm, tag = gr.sample_surface(V, F, FT, 1_400_000)
    cam = gr.Camera(CAM["azim"], CAM["elev"], CAM["dist"], CAM["target"],
                    focal_mm=CAM["focal_mm"])
    fld = pa.Field(pts, nrm, tag, cam, W, H, ss=SS)
    idx = pa.choose(fld, N_DOTS, rim_gain=4.6, tone_gain=1.3, interior=0.10,
                    seed=2, floor=0.10)
    return fld, idx


def motion(fld, idx):
    """Per-particle phase and drift direction."""
    rng = np.random.default_rng(19)
    p = fld.pts[idx]
    k = rng.normal(size=(5, 3)) * 4.0
    ph = rng.random(5) * 2 * np.pi
    field = sum(np.sin(p @ k[i] + ph[i]) for i in range(5)) / 5.0
    phase = (0.5 + 0.5 * field + rng.normal(scale=0.06, size=len(idx))) % 1.0

    # dust comes mostly off the rear and the upper surfaces, the way it does in
    # the still, so the head and near legs stay crisp
    along = fld.along[idx]
    participates = rng.random(len(idx)) < np.clip(0.18 + 0.86 * (1 - along) ** 1.6, 0, 1)

    direction = DIR_BIAS[None, :] + rng.normal(scale=0.42, size=(len(idx), 2))
    reach = (rng.random(len(idx)) ** 1.8)[:, None] * DRIFT
    return phase, participates, direction * reach


def lift_amount(phase, u, width=LIFT_SHARE):
    """A single smooth bump per particle per loop, wrapped."""
    d = np.abs((u - phase + 0.5) % 1.0 - 0.5)
    t = np.clip(1.0 - d / width, 0.0, 1.0)
    return t * t * (3 - 2 * t)


def frames(theme):
    fld, idx = build_field()
    phase, participates, drift = motion(fld, idx)
    col, alpha0, size0 = pa.colours(fld, idx, theme=theme, base=0.90,
                                    accent=False)
    size0 = size0 * 1.40 * (W / 470)
    xy0 = fld.xy[idx].copy()

    out = []
    for i in range(FRAMES):
        u = i / FRAMES
        L = lift_amount(phase, u) * participates
        fld.xy[idx] = xy0 + drift * L[:, None]
        a = alpha0 * (1.0 - 0.52 * L)
        s = size0 * (1.0 - 0.18 * L)
        out.append(pa.draw(fld, idx, col, a, s, out_alpha=True))
    fld.xy[idx] = xy0
    return out


def pad_uniform(ims, margin=26):
    box = None
    for im in ims:
        b = im.getchannel("A").point(lambda v: 255 if v > 3 else 0).getbbox()
        if b is None:
            continue
        box = b if box is None else (min(box[0], b[0]), min(box[1], b[1]),
                                     max(box[2], b[2]), max(box[3], b[3]))
    x0, y0, x1, y1 = box
    w, h = (x1 - x0) + 2 * margin, (y1 - y0) + 2 * margin
    out = []
    for im in ims:
        c = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        c.alpha_composite(im, (margin - x0, margin - y0))
        out.append(c)
    return out


def posterize(im, rgb_bits=5, a_bits=6):
    a = np.asarray(im).astype(np.uint16)
    rq, aq = 1 << (8 - rgb_bits), 1 << (8 - a_bits)
    a[..., :3] = (a[..., :3] // rq) * rq + rq // 2
    a[..., 3] = (a[..., 3] // aq) * aq
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGBA")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    sizes = {}
    for theme in ("light", "dark"):
        ims = pad_uniform([posterize(im) for im in frames(theme)])
        sizes[theme] = ims
    w = max(v[0].width for v in sizes.values())
    h = max(v[0].height for v in sizes.values())
    for theme, ims in sizes.items():
        norm = []
        for im in ims:
            c = Image.new("RGBA", (w, h), (0, 0, 0, 0))
            c.alpha_composite(im, ((w - im.width) // 2, (h - im.height) // 2))
            norm.append(c)
        path = os.path.join(OUT, f"hero-{theme}.webp")
        norm[0].save(path, save_all=True, append_images=norm[1:],
                     duration=[FRAME_MS] * len(norm), loop=0, lossless=False,
                     quality=int(os.environ.get("WEBP_Q", "74")), method=4,
                     minimize_size=True)
        print(f"[{theme}] {w}x{h}  {len(norm)} frames  "
              f"{len(norm)*FRAME_MS/1000:.1f}s  "
              f"{os.path.getsize(path)/1e6:.2f} MB")
