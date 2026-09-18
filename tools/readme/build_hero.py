"""Build the hero art: a GO2 that dissolves into dust and rebuilds out of it.

The geometry is the real Unitree visual mesh (see go2_asset.py) and it never
deforms. Each particle gets a reveal rank from a smooth spatial field, and the
loop only moves a threshold across those ranks, so the machine comes apart and
comes back without the shape ever changing.

Frame 0 is the fully resolved robot, so any context that shows a single frame
(reduced motion, a social card, a static mirror) shows the finished image.
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

DISPLAY_W = 760                  # width the README renders the art at
W, H = 1520, 1100                # 2x asset
SS = 2
# Density and dot size are held at the values tuned for this display width.
N_DOTS = 56_000
DOT_MULT = 1.40 * (860 / 470)

CAM = dict(azim=50, elev=3, dist=2.85, target=(0.02, 0.0, 0.215), focal_mm=100)

# Most of the loop is a fully resolved robot. The transition is short on
# purpose: nobody should have to wait to see what this is. GONE is far enough
# past zero that every particle clears, so the robot really does leave.
GONE = -0.18
SCHEDULE = (
    [(1.00, 950)] * 3 +                                                       # hold
    [(1.00 - (1.00 - GONE) * (i + 1) / 8, 80) for i in range(8)] +            # dissolve
    [(GONE + (1.00 - GONE) * ((i + 1) / 13) ** 0.85, 105) for i in range(13)] +  # rebuild
    [(1.00, 450)] * 2                                                         # settle
)
REVEAL_WIDTH = 0.22              # how soft the resolving front is
DRIFT = 1.45 * np.array([4.5, 6.0])   # render px: base, plus rim-weighted term


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


def reveal_rank(fld, idx):
    """Smooth spatial field: the robot resolves back to front with enough
    low-frequency noise that the front never reads as a hard line."""
    p = fld.pts[idx]
    rng = np.random.default_rng(5)
    along = fld.along[idx]
    k = rng.normal(size=(6, 3)) * 5.5
    ph = rng.random(6) * 2 * np.pi
    wob = sum(np.sin(p @ k[i] + ph[i]) for i in range(6)) / 6.0
    r = 0.70 * (1.0 - along) + 0.30 * (0.5 + 0.5 * wob)
    r += rng.normal(scale=0.045, size=len(r))
    return np.clip((r - r.min()) / (r.max() - r.min()), 0, 1)


def frames(theme):
    fld, idx = build_field()
    rank = reveal_rank(fld, idx)
    col, alpha, size = pa.colours(fld, idx, theme=theme, base=0.90,
                                  accent=False)
    size = size * DOT_MULT
    rng = np.random.default_rng(31)
    scatter = (DRIFT[0] + DRIFT[1] * fld.rim[idx])[:, None]
    drift = rng.normal(size=(len(idx), 2)) * scatter
    xy0 = fld.xy[idx].copy()

    out, durations = [], []
    for progress, ms in SCHEDULE:
        vis = np.clip((progress - rank) / REVEAL_WIDTH + 0.5, 0, 1)
        vis = vis * vis * (3 - 2 * vis)
        if progress >= 0.999:
            vis[:] = 1.0
        keep = vis > 0.012
        fld.xy[idx] = xy0 + drift * ((1.0 - vis) ** 1.6)[:, None] * fld.ss
        out.append(pa.draw(fld, idx[keep], col[keep],
                           alpha[keep] * vis[keep],
                           size[keep] * (0.72 + 0.28 * vis[keep]),
                           out_alpha=True))
        durations.append(ms)
    fld.xy[idx] = xy0
    return out, durations


def pad_uniform(ims, margin=50):
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
    import pickle
    os.makedirs(OUT, exist_ok=True)
    sizes = {}
    for theme in ("light", "dark"):
        cache = os.path.join(HERE, f".frames_{theme}.pkl")
        if os.path.exists(cache) and "--recache" not in sys.argv:
            with open(cache, "rb") as fh:
                ims, dur = pickle.load(fh)
        else:
            ims, dur = frames(theme)
            ims = pad_uniform([posterize(im) for im in ims])
            with open(cache, "wb") as fh:
                pickle.dump((ims, dur), fh)
        sizes[theme] = (ims, dur)
    w = max(v[0][0].width for v in sizes.values())
    h = max(v[0][0].height for v in sizes.values())
    for theme, (ims, dur) in sizes.items():
        norm = []
        for im in ims:
            c = Image.new("RGBA", (w, h), (0, 0, 0, 0))
            c.alpha_composite(im, ((w - im.width) // 2, (h - im.height) // 2))
            norm.append(c)
        path = os.path.join(OUT, f"hero-{theme}.webp")
        norm[0].save(path, save_all=True, append_images=norm[1:],
                     duration=dur, loop=0, lossless=False,
                     quality=int(os.environ.get("WEBP_Q", "72")), method=6,
                     minimize_size=True)
        print(f"[{theme}] {w}x{h}  {len(norm)} frames  "
              f"{sum(dur)/1000:.2f}s  {os.path.getsize(path)/1e6:.2f} MB")
