"""Geometry for the Unitree GO2 hero artwork.

Builds a 3D model of a GO2 EDU quadruped from published link proportions
(go2_description URDF), as a wireframe plus a surface point sampling that
carries per-point normals. Normals let the renderer rim-light the cloud and
fade back-facing returns, which is what makes a point set read as a solid
machine instead of noise.

Frame: x forward, y left, z up. Origin at trunk centre.
"""

import numpy as np

# ---------------------------------------------------------------- dimensions
TRUNK_L, TRUNK_W, TRUNK_H = 0.372, 0.196, 0.118
HEAD_L = 0.098                      # forward sensor module
HIP_X, HIP_Y = 0.1934, 0.0465
THIGH_Y = 0.0955
THIGH_L = CALF_L = 0.213
FOOT_R = 0.023
STANCE = (0.0, 0.92, -1.80)         # hip roll, thigh, calf (rad), nominal stand

RNG = np.random.default_rng(7)


# ------------------------------------------------------------------ primitives
def _box_wire(c, l):
    sx, sy, sz = np.asarray(l, float) / 2
    c = np.asarray(c, float)
    v = np.array([c + [a * sx, b * sy, d * sz]
                  for a in (-1, 1) for b in (-1, 1) for d in (-1, 1)])
    e = [(0, 1), (0, 2), (0, 4), (1, 3), (1, 5), (2, 3),
         (2, 6), (3, 7), (4, 5), (4, 6), (5, 7), (6, 7)]
    return v, e


def _box_pts(c, l, n):
    c = np.asarray(c, float)
    lx, ly, lz = l
    faces = [(0, ly, lz), (1, lx, lz), (2, lx, ly)]
    areas = np.array([a * b for _, a, b in faces], float)
    areas /= areas.sum()
    P, N = [], []
    for (axis, a, b), w in zip(faces, areas):
        k = max(1, int(round(n * w)))
        other = [i for i in range(3) if i != axis]
        p = np.zeros((k, 3))
        p[:, other[0]] = (RNG.random(k) - 0.5) * a
        p[:, other[1]] = (RNG.random(k) - 0.5) * b
        s = RNG.choice((-1.0, 1.0), k)
        p[:, axis] = s * l[axis] / 2
        nrm = np.zeros((k, 3))
        nrm[:, axis] = s
        P.append(p + c)
        N.append(nrm)
    return np.vstack(P), np.vstack(N)


def _frame(p0, p1):
    d = np.asarray(p1, float) - np.asarray(p0, float)
    L = np.linalg.norm(d)
    d = d / L
    up = np.array([0.0, 1.0, 0.0])
    if abs(d @ up) > 0.9:
        up = np.array([0.0, 0.0, 1.0])
    u = np.cross(d, up)
    u /= np.linalg.norm(u)
    return d, L, u, np.cross(d, u)


def _cyl_wire(p0, p1, r, n_ring=10, rails=4):
    d, L, u, v = _frame(p0, p1)
    p0 = np.asarray(p0, float)
    ang = np.linspace(0, 2 * np.pi, n_ring, endpoint=False)
    ring = np.outer(np.cos(ang), u) + np.outer(np.sin(ang), v)
    verts, edges = [], []
    for t in (0.0, 1.0):
        base = len(verts)
        centre = p0 + d * (L * t)
        verts.extend(centre + ring * r)
        edges.extend([(base + i, base + (i + 1) % n_ring) for i in range(n_ring)])
    step = max(1, n_ring // rails)
    edges.extend([(i, n_ring + i) for i in range(0, n_ring, step)])
    return np.array(verts), edges


def _cyl_pts(p0, p1, r, n, taper=1.0):
    d, L, u, v = _frame(p0, p1)
    p0 = np.asarray(p0, float)
    t = RNG.random(n)
    a = RNG.random(n) * 2 * np.pi
    rad = r * (1.0 + (taper - 1.0) * t)
    nrm = np.outer(np.cos(a), u) + np.outer(np.sin(a), v)
    return p0 + np.outer(t * L, d) + nrm * rad[:, None], nrm


def _sphere_pts(c, r, n):
    p = RNG.normal(size=(n, 3))
    p /= np.linalg.norm(p, axis=1, keepdims=True)
    return np.asarray(c, float) + p * r, p


def _quad_pts(quad, n):
    q = np.asarray(quad, float)
    a, b = RNG.random(n)[:, None], RNG.random(n)[:, None]
    p = (q[0] * (1 - a) * (1 - b) + q[1] * a * (1 - b)
         + q[2] * a * b + q[3] * (1 - a) * b)
    nrm = np.cross(q[1] - q[0], q[3] - q[0])
    nrm = nrm / np.linalg.norm(nrm)
    return p, np.repeat(nrm[None, :], n, axis=0)


# ------------------------------------------------------------------- kinematics
def leg_points(sx, sy, stance=STANCE):
    q0, q1, q2 = stance
    hip = np.array([sx * HIP_X, sy * HIP_Y, 0.0])
    thigh = np.array([sx * HIP_X, sy * THIGH_Y, 0.0])
    knee = thigh + np.array([-THIGH_L * np.sin(q1), 0.0, -THIGH_L * np.cos(q1)])
    q12 = q1 + q2
    foot = knee + np.array([-CALF_L * np.sin(q12), 0.0, -CALF_L * np.cos(q12)])
    return hip, thigh, knee, foot


def stand_height():
    return -leg_points(1, 1)[3][2]


def build_model():
    """Return verts, edges, edge_parts, cloud_pts, cloud_normals, cloud_parts."""
    verts, edges, eparts = [], [], []
    cp, cn, cparts = [], [], []
    part = ["body"]

    def wire(v, e):
        base = len(verts)
        verts.extend(v)
        edges.extend([(a + base, b + base) for a, b in e])
        eparts.extend([part[0]] * len(e))

    def cloud(p, n):
        cp.append(p)
        cn.append(n)
        cparts.extend([part[0]] * len(p))

    HZ = TRUNK_H / 2

    # ---- trunk shell
    wire(*_box_wire((0, 0, 0), (TRUNK_L, TRUNK_W, TRUNK_H)))
    cloud(*_box_pts((0, 0, 0), (TRUNK_L, TRUNK_W, TRUNK_H), 1150))

    # side hip fairings, which give the GO2 its waisted profile
    for sy in (-1, 1):
        a = np.array([-0.150, sy * (TRUNK_W / 2 - 0.004), -0.012])
        b = np.array([0.150, sy * (TRUNK_W / 2 - 0.004), -0.012])
        wire(*_cyl_wire(a, b, 0.040, 10, 4))
        cloud(*_cyl_pts(a, b, 0.040, 340))

    # ---- upper deck
    part[0] = "deck"
    wire(*_box_wire((-0.03, 0, HZ + 0.018), (0.24, 0.132, 0.036)))
    cloud(*_box_pts((-0.03, 0, HZ + 0.018), (0.24, 0.132, 0.036), 260))
    hy = 0.050
    for sy in (-1, 1):
        a = np.array([-0.082, sy * hy, HZ + 0.036])
        b = np.array([-0.082, sy * hy, HZ + 0.066])
        wire(*_cyl_wire(a, b, 0.008, 6, 2))
        cloud(*_cyl_pts(a, b, 0.008, 26))
    a = np.array([-0.082, -hy, HZ + 0.066])
    b = np.array([-0.082, hy, HZ + 0.066])
    wire(*_cyl_wire(a, b, 0.008, 8, 4))
    cloud(*_cyl_pts(a, b, 0.008, 44))

    # ---- head: forward sensor module, tapering and dropping toward the face
    part[0] = "head"
    x0, x1 = TRUNK_L / 2, TRUNK_L / 2 + HEAD_L
    w0, w1 = TRUNK_W / 2, TRUNK_W / 2 - 0.036
    t0, t1 = HZ, HZ - 0.036
    b0, b1 = -HZ, -HZ + 0.030
    h = np.array([
        [x0, -w0, t0], [x0, w0, t0], [x0, w0, b0], [x0, -w0, b0],
        [x1, -w1, t1], [x1, w1, t1], [x1, w1, b1], [x1, -w1, b1],
    ])
    wire(h, [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4),
             (0, 4), (1, 5), (2, 6), (3, 7)])
    for quad, k in (((4, 5, 6, 7), 430),      # face
                    ((0, 1, 5, 4), 260),      # top
                    ((3, 2, 6, 7), 190),      # belly
                    ((0, 3, 7, 4), 300),      # left flank
                    ((1, 2, 6, 5), 300)):     # right flank
        cloud(*_quad_pts(h[list(quad)], k))

    # ---- front stereo lenses, recessed in the face
    part[0] = "lens"
    for sy in (-1, 1):
        c = np.array([x1 - 0.004, sy * 0.032, (t1 + b1) / 2 - 0.004])
        wire(*_cyl_wire(c, c + [0.010, 0, 0], 0.017, 14, 4))
        cloud(*_cyl_pts(c, c + np.array([0.010, 0, 0]), 0.017, 70))

    # ---- L1 LiDAR on the head crown
    part[0] = "lidar"
    lid = np.array([0.150, 0.0, HZ + 0.036])
    wire(*_cyl_wire(lid, lid + [0, 0, 0.042], 0.035, 16, 4))
    cloud(*_cyl_pts(lid, lid + np.array([0, 0, 0.042]), 0.035, 150))

    # ---- legs
    for sx in (1, -1):
        for sy in (1, -1):
            part[0] = "leg"
            hip, thigh, knee, foot = leg_points(sx, sy)
            m0 = hip + np.array([0, sy * 0.006, 0])
            m1 = np.array([hip[0], sy * (THIGH_Y + 0.022), 0.0])
            wire(*_cyl_wire(m0, m1, 0.046, 14, 4))
            cloud(*_cyl_pts(m0, m1, 0.046, 300))

            wire(*_cyl_wire(thigh, knee, 0.031, 10, 4))
            cloud(*_cyl_pts(thigh, knee, 0.031, 430))

            k0 = knee + np.array([0, -0.012 * sy, 0])
            k1 = knee + np.array([0, 0.018 * sy, 0])
            wire(*_cyl_wire(k0, k1, 0.027, 12, 4))
            cloud(*_cyl_pts(k0, k1, 0.027, 90))

            wire(*_cyl_wire(knee, foot, 0.017, 8, 4))
            cloud(*_cyl_pts(knee, foot, 0.018, 390, taper=0.55))

            part[0] = "foot"
            wire(*_cyl_wire(foot + [0, 0, 0.005], foot + [0, 0, -0.005],
                            FOOT_R, 12, 4))
            cloud(*_sphere_pts(foot, FOOT_R, 80))

    return (np.array(verts), edges, np.array(eparts),
            np.vstack(cp), np.vstack(cn), np.array(cparts))


# ------------------------------------------------------------------- projection
class Camera:
    def __init__(self, azim_deg, elev_deg, dist, target, focal, centre=(0, 0)):
        a, e = np.radians(azim_deg), np.radians(elev_deg)
        self.target = np.asarray(target, float)
        self.eye = self.target + dist * np.array(
            [np.cos(e) * np.cos(a), np.cos(e) * np.sin(a), np.sin(e)])
        fwd = self.target - self.eye
        fwd /= np.linalg.norm(fwd)
        right = np.cross(fwd, np.array([0.0, 0.0, 1.0]))
        right /= np.linalg.norm(right)
        self.R = np.stack([right, np.cross(right, fwd), fwd])
        self.fwd = fwd
        self.focal = focal
        self.centre = np.asarray(centre, float)

    def project(self, pts):
        p = np.atleast_2d(np.asarray(pts, float))
        cam = (p - self.eye) @ self.R.T
        z = np.clip(cam[:, 2], 1e-4, None)
        return np.stack([self.centre[0] + self.focal * cam[:, 0] / z,
                         self.centre[1] - self.focal * cam[:, 1] / z], axis=1), cam[:, 2]

    def view_dirs(self, pts):
        """Unit vectors from each point toward the camera."""
        v = self.eye - np.atleast_2d(np.asarray(pts, float))
        return v / np.linalg.norm(v, axis=1, keepdims=True)
