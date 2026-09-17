"""Turn the verified GO2 surface samples into particle artwork.

The geometry is never modified. Only which surface samples are drawn, how big
they are and how opaque they are changes between candidates and animation
frames.
"""

import numpy as np

import gorender as gr

RNG = np.random.default_rng(23)

# Two palettes, one per GitHub canvas. Both are drawn on full transparency so
# the robot sits directly on the page instead of inside a panel.
THEMES = {
    "light": dict(ink=np.array([0.07, 0.09, 0.11]),
                  mid=np.array([0.42, 0.46, 0.51]),
                  acc=np.array([0.11, 0.42, 0.52]),
                  gain=1.12, shadow=0.10),
    # on #0d1117 a mid grey vanishes, so the dark ramp sits much higher
    "dark": dict(ink=np.array([0.95, 0.97, 0.99]),
                 mid=np.array([0.54, 0.59, 0.65]),
                 acc=np.array([0.45, 0.80, 0.90]),
                 gain=1.30, shadow=0.0),
}


class Field:
    """A camera-resolved particle field over the posed GO2."""

    def __init__(self, pts, nrm, tag, cam, W, H, ss=3):
        self.W, self.H, self.ss = W, H, ss
        w, h = W * ss, H * ss
        xy, z = cam.project(pts, w, h)
        vd = cam.dirs(pts)
        n = gr.orient(nrm, vd)

        facing = np.einsum("ij,ij->i", n, vd)
        self.rim = np.clip(1.0 - facing, 0, 1) ** 1.9

        # occlusion: splat the full sample set densely, then keep the samples
        # that sit on the visible front surface
        _, zbuf, _ = gr.splat(xy, z, np.zeros((len(pts), 3), np.float32),
                              w, h, (0, 0, 0), radius=2)
        px = np.clip(np.round(xy[:, 0]).astype(int), 0, w - 1)
        py = np.clip(np.round(xy[:, 1]).astype(int), 0, h - 1)
        self.front = z - zbuf[py, px] < 0.010

        self.cam = cam
        self.xy, self.z, self.tag = xy, z, tag
        self.pts = pts
        zlo, zhi = np.percentile(z, 1), np.percentile(z, 99)
        self.near = np.clip(1.0 - (z - zlo) / max(zhi - zlo, 1e-6), 0, 1)
        # along-body coordinate, 0 at the tail, 1 at the nose
        x = pts[:, 0]
        self.along = np.clip((x - x.min()) / (x.max() - x.min()), 0, 1)
        self.head = (tag == 0) & (pts[:, 0] > 0.318) & (pts[:, 2] > 0.222) \
            & (pts[:, 2] < 0.252) & (np.abs(pts[:, 1]) < 0.055)

        # luminance of an ordinary studio render of the real surface. Stipple
        # density and dot weight follow it, so the dots describe the form the
        # way an engraving does rather than coating it evenly.
        alb = np.full((len(pts), 3), 0.90, np.float32)
        alb[tag == 4] = 0.12
        lit = gr.shade(n, vd, alb)
        self.lum = np.clip(lit @ np.array([0.2126, 0.7152, 0.0722]), 0, 1)
        self.dark = np.clip(1.0 - self.lum, 0, 1)


def choose(field, n, rim_gain=1.5, tone_gain=2.4, interior=0.10, seed=0,
           weight=None, floor=0.16):
    """Importance-resample the field. Density follows the shaded tone of the
    real surface, with an extra push on the silhouette."""
    rng = np.random.default_rng(1000 + seed)
    w = floor + tone_gain * field.dark ** 1.6 + rim_gain * field.rim ** 1.5
    # samples on the far side of the shell are kept only where they sit on the
    # back contour. Keeping them evenly would paint a flat haze across the body
    # instead of reading as volume.
    back = interior * (0.10 + 0.90 * field.rim ** 2.2)
    w = w * np.where(field.front, 1.0, back)
    if weight is not None:
        w = w * weight
    w = np.maximum(w, 1e-6)
    w /= w.sum()
    idx = rng.choice(len(w), size=min(n, (w > 0).sum()), replace=False, p=w)
    return idx


def colours(field, idx, theme="light", accent=True, base=0.86, rng_seed=7):
    t = THEMES[theme]
    ink, mid, acc = t["ink"], t["mid"], t["acc"]
    rng = np.random.default_rng(rng_seed)
    rim = field.rim[idx]
    near = field.near[idx]
    front = field.front[idx]
    dark = field.dark[idx]

    # tone 0 = flat lit surface, tone 1 = silhouette or shadowed form
    tone = np.clip(0.30 + 0.78 * dark + 0.52 * rim, 0, 1)
    col = mid[None, :] + (ink - mid)[None, :] * tone[:, None]
    col = np.where(front[:, None], col, mid[None, :] + (ink - mid)[None, :] * 0.15)

    alpha = base * t["gain"] * (0.34 + 0.90 * tone) * (0.74 + 0.26 * near)
    alpha = np.where(front, alpha, alpha * 0.30)
    alpha = np.clip(alpha * (0.84 + 0.32 * rng.random(len(idx))), 0.05, 0.97)

    size = (0.80 + 0.52 * tone + 0.28 * near) * np.where(front, 1.0, 0.72)
    if accent:
        h = field.head[idx]
        col[h] = mid + (acc - mid) * 0.85
        alpha[h] = np.clip(alpha[h] * 1.12, 0, 0.92)
    return col, alpha, size


def ground_shadow(field, theme, strength=1.0):
    """A soft contact shadow, built by flattening the robot onto z = 0 and
    blurring hard. It grounds the robot without drawing a floor."""
    from PIL import Image, ImageFilter
    amt = THEMES[theme]["shadow"] * strength
    ss, W, H = field.ss, field.W, field.H
    if amt <= 0:
        return Image.new("RGBA", (W, H), (0, 0, 0, 0))
    p = field.pts.copy()
    p[:, 2] = 0.0
    p[:, 0] -= 0.035
    p[:, 1] -= 0.020
    xy, _ = field.cam.project(p, W * ss, H * ss)
    acc = np.zeros((H, W), np.float32)
    x = np.round(xy[:, 0] / ss).astype(int)
    y = np.round(xy[:, 1] / ss).astype(int)
    ok = (x >= 0) & (x < W) & (y >= 0) & (y < H)
    np.add.at(acc, (y[ok], x[ok]), 1.0)
    a = np.clip(acc / max(np.percentile(acc[acc > 0], 80), 1.0), 0, 1) if acc.any() else acc
    im = Image.fromarray((a * 255).astype(np.uint8), "L")
    im = im.filter(ImageFilter.GaussianBlur(radius=max(W, H) * 0.018))
    a = np.asarray(im).astype(np.float32) / 255.0
    a = np.clip(a * amt, 0, 1)
    rgba = np.zeros((H, W, 4), np.uint8)
    rgba[..., :3] = (np.array([0.18, 0.21, 0.25]) * 255).astype(np.uint8)
    rgba[..., 3] = (a * 255).astype(np.uint8)
    return Image.fromarray(rgba, "RGBA")


KERNEL = None


def _kernel(ss):
    global KERNEL
    if KERNEL is None or KERNEL[0] != ss:
        r = ss
        ax = np.arange(-r, r + 1)
        gx, gy = np.meshgrid(ax, ax)
        d = np.sqrt(gx ** 2 + gy ** 2)
        KERNEL = (ss, gx.ravel(), gy.ravel(), d.ravel())
    return KERNEL[1:]


def draw(field, idx, col, alpha, size, bg=None, out_alpha=False):
    """Accumulate soft round dots, then composite over bg (or return RGBA)."""
    ss, W, H = field.ss, field.W, field.H
    w, h = W * ss, H * ss
    acc_a = np.zeros(w * h, np.float32)
    acc_c = np.zeros((w * h, 3), np.float32)

    gx, gy, gd = _kernel(ss)
    xy = field.xy[idx]
    order = np.argsort(-field.z[idx])
    xy, col, alpha, size = xy[order], col[order], alpha[order], size[order]

    rad = np.maximum(size * ss * 0.62, 0.8)
    for dx, dy, dd in zip(gx, gy, gd):
        fall = np.clip(1.0 - (dd - 0.0) / np.maximum(rad, 1e-6), 0, 1) ** 1.3
        m = fall > 0.02
        if not m.any():
            continue
        x = np.round(xy[m, 0] + dx).astype(np.int64)
        y = np.round(xy[m, 1] + dy).astype(np.int64)
        ok = (x >= 0) & (x < w) & (y >= 0) & (y < h)
        flat = y[ok] * w + x[ok]
        a = (alpha[m][ok] * fall[m][ok]).astype(np.float32)
        np.add.at(acc_a, flat, a)
        np.add.at(acc_c, flat, col[m][ok] * a[:, None])

    a = np.clip(acc_a, 0, 1.0)
    c = np.where(acc_a[:, None] > 1e-6, acc_c / np.maximum(acc_a[:, None], 1e-6), 0.0)

    from PIL import Image
    if out_alpha:
        rgba = np.concatenate([np.clip(c, 0, 1), a[:, None]], axis=1)
        im = Image.fromarray((rgba.reshape(h, w, 4) * 255).astype(np.uint8), "RGBA")
        return im.resize((W, H), Image.LANCZOS)
    bg = np.asarray(bg, np.float32)
    out = bg[None, :] * (1 - a[:, None]) + c * a[:, None]
    im = Image.fromarray((np.clip(out, 0, 1).reshape(h, w, 3) * 255).astype(np.uint8))
    return im.resize((W, H), Image.LANCZOS)
