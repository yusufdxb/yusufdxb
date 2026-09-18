"""Particle reconstruction loop, written as APNG with a real alpha channel.

The geometry never changes. Each particle gets a reveal rank from a smooth
spatial field, and the loop only moves a threshold across those ranks, so the
GO2 dissolves and rebuilds without ever deforming.

Frame 0 is the fully resolved robot, so any context that shows a single frame
shows the finished image.
"""

import os
import sys

import numpy as np
from PIL import Image

import gorender as gr
import particles as pa

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "assets", "readme")

SCALE = 1.45
W, H = int(1040 * SCALE), int(600 * SCALE)
N_DOTS = 26_000

# Two thirds of the loop is spent on a fully resolved robot. The transition is
# short on purpose: nobody should have to wait to see what this is.
SCHEDULE = (
    [(1.00, 950)] * 3 +                                            # hold, resolved
    [(1.00 - 0.80 * (i + 1) / 6, 85) for i in range(6)] +          # dissolve
    [(0.20 + 0.80 * ((i + 1) / 12) ** 0.85, 115) for i in range(12)] +  # rebuild
    [(1.00, 450)] * 2                                              # settle
)


def build_field():
    npz = os.path.join(HERE, "go2_posed.npz")
    if not os.path.exists(npz):
        raise SystemExit("run go2_asset.py first to build go2_posed.npz")
    d = np.load(npz)
    V, F, FT = d["V"].astype(np.float64), d["F"], d["FT"]
    pts, nrm, tag = gr.sample_surface(V, F, FT, 2_200_000)
    cam = gr.Camera(50, 3, 2.70, (0.02, 0.0, 0.215), focal_mm=100)
    fld = pa.Field(pts, nrm, tag, cam, W, H, ss=2)
    # silhouette first, then head and hip housings, then legs. Interior stays
    # low so the robot reads as a particle sculpture rather than a shaded model.
    idx = pa.choose(fld, N_DOTS, rim_gain=4.4, tone_gain=1.5, interior=0.12,
                    seed=2, floor=0.12)
    return fld, idx


def reveal_rank(fld, idx):
    """Smooth spatial field: the robot resolves front to back with enough
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
    col, alpha, size = pa.colours(fld, idx, theme=theme, base=0.94,
                                  accent=False)
    size = size * 1.30 * SCALE
    nrm_screen = fld.rim[idx]
    rng = np.random.default_rng(31)
    drift = rng.normal(size=(len(idx), 2)) * ((2.4 + 3.0 * nrm_screen) * SCALE)[:, None]
    xy0 = fld.xy[idx].copy()

    shadow = pa.ground_shadow(fld, theme)

    out, durations = [], []
    for progress, ms in SCHEDULE:
        vis = np.clip((progress - rank) / 0.22 + 0.5, 0, 1)
        vis = vis * vis * (3 - 2 * vis)
        if progress >= 0.999:
            vis[:] = 1.0
        keep = vis > 0.012
        fld.xy[idx] = xy0 + drift * ((1.0 - vis) ** 1.6)[:, None] * fld.ss
        im = pa.draw(fld, idx[keep], col[keep],
                     alpha[keep] * vis[keep],
                     size[keep] * (0.72 + 0.28 * vis[keep]), out_alpha=True)
        # the shadow is identical in every frame: the robot is there the whole
        # time, only its particle representation resolves. Holding it constant
        # also lets the encoder diff it away instead of re-coding a large soft
        # gradient 25 times.
        sh = shadow.copy()
        sh.alpha_composite(im)
        out.append(sh)
        durations.append(ms)
    fld.xy[idx] = xy0
    return out, durations


MARGIN = 190   # asset px of empty space on every side of the robot


def pad_uniform(ims, margin=MARGIN):
    """Put the robot on a canvas with the same empty margin on all four sides.
    Cropping alone cannot do this: the render canvas has no room to grow into,
    so the top and bottom margins come out clamped."""
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


def content_box(ims, margin=MARGIN):
    """Union alpha bounding box over every frame, so the transparent margin
    (which is most of the file) is not shipped."""
    box = None
    for im in ims:
        b = im.getchannel("A").point(lambda v: 255 if v > 3 else 0).getbbox()
        if b is None:
            continue
        box = b if box is None else (min(box[0], b[0]), min(box[1], b[1]),
                                     max(box[2], b[2]), max(box[3], b[3]))
    x0, y0, x1, y1 = box
    return (max(0, x0 - margin), max(0, y0 - margin),
            min(ims[0].width, x1 + margin), min(ims[0].height, y1 + margin))


def posterize(im, rgb_bits=5, a_bits=6):
    """Fewer distinct values compress far better and are invisible on dots."""
    a = np.asarray(im).astype(np.uint16)
    rq, aq = 1 << (8 - rgb_bits), 1 << (8 - a_bits)
    a[..., :3] = (a[..., :3] // rq) * rq + rq // 2
    a[..., 3] = (a[..., 3] // aq) * aq
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGBA")


if __name__ == "__main__":
    import pickle
    os.makedirs(OUT, exist_ok=True)
    for theme in ("light", "dark"):
        cache = os.path.join(HERE, f".frames_{theme}.pkl")
        if os.path.exists(cache) and "--recache" not in sys.argv:
            with open(cache, "rb") as fh:
                ims, dur = pickle.load(fh)
        else:
            ims, dur = frames(theme)
            box = content_box(ims)
            ims = [posterize(im.crop(box)) for im in ims]
            with open(cache, "wb") as fh:
                pickle.dump((ims, dur), fh)
        ims = pad_uniform(ims)
        q = int(os.environ.get("WEBP_Q", "72"))
        path = os.path.join(OUT, f"hero-{theme}.webp")
        ims[0].save(path, save_all=True, append_images=ims[1:], duration=dur,
                    loop=0, lossless=False, quality=q, method=6,
                    minimize_size=True)
        print(f"[{theme}] {ims[0].size[0]}x{ims[0].size[1]}  {len(ims)} frames  "
              f"{sum(dur)/1000:.2f}s  webp {os.path.getsize(path)/1e6:.2f} MB")
