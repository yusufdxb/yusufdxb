"""Surface sampling and point-splat rendering for the posed GO2 mesh."""

import numpy as np

RNG = np.random.default_rng(11)


# ------------------------------------------------------------------ sampling
def sample_surface(V, F, FT, n, rng=RNG):
    """Area-weighted barycentric sampling. Never samples vertices, so mesh
    topology never shows through as banding or clumps."""
    tri = V[F]
    e1 = tri[:, 1] - tri[:, 0]
    e2 = tri[:, 2] - tri[:, 0]
    cross = np.cross(e1, e2)
    area = 0.5 * np.linalg.norm(cross, axis=1)
    nrm = cross / np.maximum(np.linalg.norm(cross, axis=1, keepdims=True), 1e-12)

    p = area / area.sum()
    idx = rng.choice(len(F), size=n, p=p)
    u = rng.random(n)
    v = rng.random(n)
    over = u + v > 1.0
    u[over] = 1.0 - u[over]
    v[over] = 1.0 - v[over]
    pts = tri[idx, 0] + u[:, None] * e1[idx] + v[:, None] * e2[idx]
    return pts.astype(np.float32), nrm[idx].astype(np.float32), FT[idx]


# -------------------------------------------------------------------- camera
class Camera:
    """Perspective camera specified the way a product shot is: a lens length
    and a distance, not a field of view."""

    def __init__(self, azim, elev, dist, target, focal_mm=85.0, sensor_mm=36.0,
                 roll=0.0):
        a, e = np.radians(azim), np.radians(elev)
        self.target = np.asarray(target, float)
        self.eye = self.target + dist * np.array(
            [np.cos(e) * np.cos(a), np.cos(e) * np.sin(a), np.sin(e)])
        fwd = self.target - self.eye
        fwd /= np.linalg.norm(fwd)
        right = np.cross(fwd, (0, 0, 1.0))
        right /= np.linalg.norm(right)
        up = np.cross(right, fwd)
        if roll:
            c, s = np.cos(roll), np.sin(roll)
            right, up = c * right + s * up, -s * right + c * up
        self.R = np.stack([right, up, fwd])
        self.focal_mm = focal_mm
        self.sensor_mm = sensor_mm

    def view(self, p):
        return (np.atleast_2d(p) - self.eye) @ self.R.T

    def project(self, p, W, H):
        cam = self.view(p)
        z = np.clip(cam[:, 2], 1e-5, None)
        f = self.focal_mm / self.sensor_mm * W
        return np.stack([W / 2 + f * cam[:, 0] / z,
                         H / 2 - f * cam[:, 1] / z], axis=1), cam[:, 2]

    def dirs(self, p):
        d = self.eye - np.atleast_2d(p)
        return d / np.linalg.norm(d, axis=1, keepdims=True)


# ------------------------------------------------------------------ splatting
def splat(xy, depth, rgb, W, H, bg, radius=1, alpha=None):
    """Painter's algorithm: paint far to near so nearer samples win.
    Returns (image float32 HxWx3, depth buffer, coverage mask)."""
    img = np.repeat(np.asarray(bg, np.float32)[None, :], W * H, axis=0)
    zbuf = np.full(W * H, np.inf, np.float32)
    cov = np.zeros(W * H, bool)

    order = np.argsort(-depth)
    xy = xy[order]
    depth = depth[order]
    rgb = np.asarray(rgb, np.float32)
    rgb = rgb[order] if rgb.ndim == 2 else np.repeat(rgb[None, :], len(xy), 0)
    a = None if alpha is None else np.clip(alpha, 0, 1)[order][:, None]

    offs = [(dx, dy) for dx in range(-radius + 1, radius)
            for dy in range(-radius + 1, radius)] or [(0, 0)]
    for dx, dy in offs:
        x = np.round(xy[:, 0] + dx).astype(np.int64)
        y = np.round(xy[:, 1] + dy).astype(np.int64)
        ok = (x >= 0) & (x < W) & (y >= 0) & (y < H)
        flat = y[ok] * W + x[ok]
        src = rgb[ok]
        if a is None:
            img[flat] = src
        else:
            img[flat] = img[flat] * (1 - a[ok]) + src * a[ok]
        zbuf[flat] = np.minimum(zbuf[flat], depth[ok])
        cov[flat] = True
    return (img.reshape(H, W, 3), zbuf.reshape(H, W), cov.reshape(H, W))


# -------------------------------------------------------------------- shading
KEY = np.array([0.55, 0.62, 0.56])
KEY /= np.linalg.norm(KEY)
FILL = np.array([-0.62, 0.35, 0.18])
FILL /= np.linalg.norm(FILL)


def orient(nrm, view_dirs):
    """Collada winding is inconsistent across these meshes, so flip every
    normal toward the camera before shading. Without this the shell speckles."""
    s = np.sign(np.einsum("ij,ij->i", nrm, view_dirs))
    s[s == 0] = 1.0
    return nrm * s[:, None]


def shade(nrm, view_dirs, albedo):
    """Three-light studio setup: key, cool fill, and a rim that separates the
    robot from a light background."""
    lam = np.clip(nrm @ KEY, 0, 1)
    fil = np.clip(nrm @ FILL, 0, 1)
    facing = np.abs(np.einsum("ij,ij->i", nrm, view_dirs))
    rim = (1.0 - facing) ** 2.4
    half = KEY + view_dirs
    half /= np.maximum(np.linalg.norm(half, axis=1, keepdims=True), 1e-9)
    spec = np.clip(np.einsum("ij,ij->i", nrm, half), 0, 1) ** 42

    lit = (0.30 + 0.72 * lam + 0.20 * fil)[:, None] * albedo
    lit = lit + rim[:, None] * np.array([0.16, 0.17, 0.19]) + spec[:, None] * 0.55
    return np.clip(lit, 0, 1)
