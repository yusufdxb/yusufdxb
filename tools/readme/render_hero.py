"""Render the GO2 acquisition hero: static poster + animation frames.

The robot is a projected 3D model (see go2_model.py), drawn as a LiDAR-style
point reconstruction over a dimmed wireframe. A scan front sweeps the model;
everything behind the front is "acquired" and lit, everything ahead of it is
raw noisy return. Frame 0 of the loop is the fully acquired state, so a viewer
who only ever sees a still frame sees the finished image.

Usage:
  python3 render_hero.py --poster out.png [--phase 0.0]
  python3 render_hero.py --frames DIR --count 48
"""

import argparse
import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont

import go2_model as g2

# ------------------------------------------------------------------- canvas
W, H = 900, 580
SS = 3
OUT_SCALE = 2

BG        = (7, 9, 11)
GRID      = (18, 23, 27)
RULE      = (34, 43, 50)
INK       = (233, 239, 242)
DIM       = (132, 147, 157)
MUTE      = (88, 101, 110)
FAINTTXT  = (62, 73, 81)
CYAN      = (110, 231, 250)
CYAN_MID  = (52, 150, 172)
CYAN_DEEP = (26, 74, 88)
AMBER     = (226, 163, 76)

RAW_PT    = (36, 46, 53)
RAW_EDGE  = (24, 31, 36)
STEEL_COOL = (46, 62, 72)
STEEL_LIT  = (226, 238, 245)
EDGE_FAR  = (32, 41, 47)
EDGE_NR   = (104, 124, 136)

from style import MONO, MONOB, SANS  # noqa: E402

_fc = {}


def font(path, size, variation=None):
    key = (path, size, variation)
    if key not in _fc:
        f = ImageFont.truetype(path, size * SS)
        if variation:
            try:
                f.set_variation_by_name(variation)
            except Exception:
                pass
        _fc[key] = f
    return _fc[key]


def px(v):
    return int(round(v * SS))


def mix(a, b, t):
    t = float(np.clip(t, 0, 1))
    return tuple(int(round(x + (y - x) * t)) for x, y in zip(a, b))


def mixv(a, b, t):
    """Vectorised colour mix. a,b are RGB triples, t is (N,)."""
    a = np.array(a, float)
    b = np.array(b, float)
    return a[None, :] + (b - a)[None, :] * t[:, None]


def track(d, xy, text, fnt, fill, spacing=0.0, right=False):
    sp = spacing * SS
    ws = [d.textlength(c, font=fnt) for c in text]
    total = sum(ws) + sp * max(0, len(text) - 1)
    x, y = px(xy[0]), px(xy[1])
    if right:
        x -= total
    for c, w in zip(text, ws):
        d.text((x, y), c, font=fnt, fill=fill)
        x += w + sp
    return total / SS


# ----------------------------------------------------------------- projection
VERTS, EDGES, EPARTS, CLOUD, CNORM, CPARTS = g2.build_model()
GROUND_Z = -g2.stand_height()

CAM = g2.Camera(azim_deg=42, elev_deg=12, dist=5.4,
                target=(0.0, 0.0, -0.075), focal=3050, centre=(0, 0))

STAGE = (50, 84, 612, 400)

_v2, VD = CAM.project(VERTS)
_c2, CD = CAM.project(CLOUD)
_all = np.vstack([_v2, _c2])
_x0, _x1 = _all[:, 0].min(), _all[:, 0].max()
_y0, _y1 = _all[:, 1].min(), _all[:, 1].max()
_fit = min((STAGE[2] - STAGE[0]) / (_x1 - _x0), (STAGE[3] - STAGE[1]) / (_y1 - _y0))
_ox = STAGE[0] + ((STAGE[2] - STAGE[0]) - (_x1 - _x0) * _fit) / 2 - _x0 * _fit
_oy = STAGE[1] + ((STAGE[3] - STAGE[1]) - (_y1 - _y0) * _fit) / 2 - _y0 * _fit


def to_img(p2):
    return np.stack([p2[:, 0] * _fit + _ox, p2[:, 1] * _fit + _oy], axis=1)


def world_to_img(p3):
    p2, _ = CAM.project(np.atleast_2d(p3))
    return to_img(p2)[0]


V2 = to_img(_v2)
C2 = to_img(_c2)

_dlo = min(CD.min(), VD.min())
_dhi = max(CD.max(), VD.max())
C_NEAR = np.clip(1.0 - (CD - _dlo) / (_dhi - _dlo), 0, 1) ** 1.25
V_NEAR = np.clip(1.0 - (VD - _dlo) / (_dhi - _dlo), 0, 1) ** 1.25

ACCENT = np.isin(CPARTS, ("lidar", "lens"))
SOFT_ACCENT = CPARTS == "foot"

# surface shading: rim light picks out the silhouette, a key light gives form,
# and returns off the far side of the shell drop back so the robot reads solid.
# a little normal scatter keeps flat faces from flashing as one uniform sliver
# when they are seen edge on, and reads as real sensor return noise
_n = CNORM + g2.RNG.normal(scale=0.13, size=CNORM.shape)
_n /= np.linalg.norm(_n, axis=1, keepdims=True)
_vd = CAM.view_dirs(CLOUD)
_facing = np.einsum("ij,ij->i", _n, _vd)
_front = _facing > 0.0
_rim = np.clip(1.0 - np.abs(_facing), 0, 1) ** 1.6
_key = np.array([0.42, 0.72, 0.55])
_key /= np.linalg.norm(_key)
_lam = np.clip(_n @ _key, 0, 1)
SHADE = 0.30 + 0.78 * _rim + 0.58 * _lam
SHADE = np.where(_front, SHADE, SHADE * 0.17)
SHADE *= 0.62 + 0.38 * C_NEAR
# per-return intensity scatter: stops any flat face read edge on from turning
# into one solid white sliver, and is what real range returns look like
SHADE *= 0.70 + 0.45 * g2.RNG.random(len(SHADE))
SHADE = np.clip(SHADE, 0, 1.22)

PT_R = (0.78 + 0.62 * C_NEAR) * (0.74 + 0.50 * np.clip(SHADE, 0, 1))
DEPTH_SORT = np.lexsort((-CD, _front))

_jit = g2.RNG.normal(scale=1.0, size=C2.shape)
_jit_m = (g2.RNG.random(len(C2)) < 0.5)[:, None]

RX0, RX1 = C2[:, 0].min(), C2[:, 0].max()
RSPAN = RX1 - RX0
EDGE_ORDER = sorted(range(len(EDGES)), key=lambda k: -(VD[EDGES[k][0]] + VD[EDGES[k][1]]))
EDGE_W = {"body": 0.20, "deck": 0.22, "head": 0.62, "lidar": 0.95,
          "lens": 1.0, "leg": 1.0, "foot": 0.9}
EDGE_GAIN = np.array([EDGE_W.get(p, 0.6) for p in EPARTS])

# foot contact points, for the ground plane marks
FEET = [world_to_img(g2.leg_points(sx, sy)[3]) for sx in (1, -1) for sy in (1, -1)]

# callout anchors, in world coordinates
CALLOUTS = [
    ((0.150, 0.0, g2.TRUNK_H / 2 + 0.078), "L1 LIDAR", "up-left", 56),
    ((-0.082, 0.0, g2.TRUNK_H / 2 + 0.066), "JETSON ORIN NX", "up-right", 42),
    (tuple(g2.leg_points(1, 1)[2]), "12 x ACTUATOR", "down-left", 128),
]


# -------------------------------------------------------------------- timeline
HOLD_END, DECAY_END, SWEEP_END = 0.42, 0.50, 0.90


def sweep_u(phase):
    u = (phase - DECAY_END) / (SWEEP_END - DECAY_END)
    return u * u * (3 - 2 * u)


def scan_front(phase):
    if not (DECAY_END <= phase < SWEEP_END):
        return None
    return RX0 - 0.12 * RSPAN + sweep_u(phase) * 1.26 * RSPAN


def lit_profile(x, phase):
    n = len(x)
    if phase < HOLD_END:
        return np.ones(n), np.zeros(n)
    if phase < DECAY_END:
        g = 1.0 - (phase - HOLD_END) / (DECAY_END - HOLD_END)
        return np.full(n, g * g), np.zeros(n)
    if phase < SWEEP_END:
        f = scan_front(phase)
        a = np.clip((f - x) / (0.085 * RSPAN), 0.0, 1.0)
        hot = np.exp(-((x - f) / (0.028 * RSPAN)) ** 2)
        return a, hot
    return np.ones(n), np.zeros(n)


# -------------------------------------------------------------------- drawing
TELEM = [
    ("UNIT",       "GO2 EDU",         "n"),
    ("COMPUTE",    "JETSON ORIN NX",  "n"),
    ("MIDDLEWARE", "ROS 2 HUMBLE",    "n"),
    ("SIM",        "ISAAC LAB",       "n"),
    ("NAV",        "NAV2 / RTAB-MAP", "n"),
    ("PERCEPTION", "ONLINE",          "c"),
    ("SAFETY",     "FAIL-CLOSED",     "c"),
    ("STATE",      "ACTIVE",          "c"),
]

M = 46


def draw_chrome(d):
    b = 15
    for cx, cy, sx, sy in ((M, 32, 1, 1), (W - M, 32, -1, 1),
                           (M, H - 26, 1, -1), (W - M, H - 26, -1, -1)):
        d.line([px(cx), px(cy), px(cx + b * sx), px(cy)], fill=RULE, width=px(1))
        d.line([px(cx), px(cy), px(cx), px(cy + b * sy)], fill=RULE, width=px(1))

    d.line([px(M), px(60), px(W - M), px(60)], fill=RULE, width=px(1))
    f = font(MONO, 11.5)
    track(d, (M, 39), "UNITREE GO2 EDU  //  QUADRUPED FIELD UNIT", f, DIM, 1.7)
    track(d, (W - M, 39), "LIDAR RECONSTRUCTION", f, MUTE, 1.7, right=True)

    gx0, gx1 = M, 612
    for gx in range(gx0, gx1 + 1, 38):
        d.line([px(gx), px(78), px(gx), px(404)], fill=GRID, width=px(1))
    for gy in range(78, 405, 34):
        d.line([px(gx0), px(gy), px(gx1), px(gy)], fill=GRID, width=px(1))

    d.line([px(M), px(412), px(W - M), px(412)], fill=RULE, width=px(1))
    for i in range(15):
        x = M + i * (W - 2 * M) / 14
        d.line([px(x), px(412), px(x), px(412 + (7 if i % 2 == 0 else 4))],
               fill=RULE, width=px(1))
    fs = font(MONO, 10)
    track(d, (M, 424), "0.0 m", fs, FAINTTXT, 1.0)
    track(d, (612, 424), "1.0 m", fs, FAINTTXT, 1.0)


def draw_ground(d, phase):
    a = float(lit_profile(np.array([(RX0 + RX1) / 2]), phase)[0][0])
    col = mix(BG, CYAN_DEEP, 0.25 + 0.75 * a)
    for fx, fy in FEET:
        for r in (7.0, 12.0):
            d.ellipse([px(fx - r), px(fy - r * 0.34), px(fx + r), px(fy + r * 0.34)],
                      outline=col, width=px(1))
        d.line([px(fx), px(fy), px(fx), px(412)], fill=mix(BG, RULE, 0.55 + 0.45 * a),
               width=px(1))


def draw_robot(d, phase):
    a_c, hot_c = lit_profile(C2[:, 0], phase)
    a_v, _ = lit_profile(V2[:, 0], phase)

    pts = C2 + (1.0 - a_c)[:, None] * _jit_m * _jit * 2.6

    for k in EDGE_ORDER:
        i, j = EDGES[k]
        a = (a_v[i] + a_v[j]) / 2
        if a < 0.03:
            col = RAW_EDGE
        else:
            near = (V_NEAR[i] + V_NEAR[j]) / 2
            col = mix(RAW_EDGE, mix(EDGE_FAR, EDGE_NR, near), a * EDGE_GAIN[k])
        d.line([px(V2[i, 0]), px(V2[i, 1]), px(V2[j, 0]), px(V2[j, 1])],
               fill=col, width=px(1))

    base = mixv(STEEL_COOL, STEEL_LIT, np.clip(SHADE, 0, 1))
    accent = mixv(CYAN_MID, CYAN, np.clip(SHADE, 0, 1))
    base = np.where(ACCENT[:, None], accent, base)
    base = np.where(SOFT_ACCENT[:, None], (base + accent * 0.8) / 1.8, base)
    base = base * np.clip(SHADE, 0.10, 1.25)[:, None]
    raw = mixv(BG, RAW_PT, 0.40 + 0.60 * C_NEAR)
    col = raw + (base - raw) * a_c[:, None]
    hotc = np.clip(hot_c, 0, 1)[:, None]
    col = col + (np.array([240., 253., 255.]) - col) * hotc * 0.9
    col = np.clip(col, 0, 255).astype(int)

    r = PT_R * (0.72 + 0.28 * a_c)
    for idx in DEPTH_SORT:
        x, y = pts[idx]
        rr = r[idx]
        c = tuple(col[idx])
        d.ellipse([px(x - rr), px(y - rr), px(x + rr), px(y + rr)], fill=c)


def draw_callouts(d, phase):
    vis = 1.0 if phase < HOLD_END else (0.0 if phase < 0.93 else (phase - 0.93) / 0.07)
    if vis <= 0.02:
        return
    f = font(MONO, 10.5)
    col = mix(BG, MUTE, vis)
    lcol = mix(BG, CYAN_MID, vis * 0.75)
    for world, label, side, off in CALLOUTS:
        ax, ay = world_to_img(np.array(world))
        up = side.startswith("up")
        left = side.endswith("left")
        dy = -30 if up else 34
        dx = -off if left else off
        ex, ey = ax + dx, ay + dy
        tail = -26 if left else 26
        d.ellipse([px(ax - 2), px(ay - 2), px(ax + 2), px(ay + 2)], outline=lcol,
                  width=px(1))
        d.line([px(ax), px(ay), px(ex), px(ey)], fill=lcol, width=px(1))
        d.line([px(ex), px(ey), px(ex + tail), px(ey)], fill=lcol, width=px(1))
        track(d, (ex + tail + (-5 if left else 5), ey - 6), label, f, col, 1.1,
              right=left)


def draw_scan_readout(d, phase):
    f = scan_front(phase)
    if f is None:
        return
    fm = font(MONO, 10.5)
    u = np.clip((f - RX0) / RSPAN, 0, 1)
    d.line([px(f), px(66), px(f), px(78)], fill=CYAN, width=px(1))
    track(d, (f + 7, 64), f"ACQ {u * 100:4.0f}%", fm, CYAN, 1.2)


def draw_telemetry(d, phase, tick):
    x, y = 640, 112
    fl = font(MONO, 11.5)
    fv = font(MONOB, 12.5)
    track(d, (x, y - 28), "TELEMETRY", font(MONO, 10.5), MUTE, 2.8)
    d.line([px(x), px(y - 10), px(W - M), px(y - 10)], fill=RULE, width=px(1))

    if phase < HOLD_END:
        n = len(TELEM)
    elif phase < 0.90:
        n = 0
    else:
        n = int(len(TELEM) * min(1.0, (phase - 0.90) / 0.075))

    for i, (k, v, kind) in enumerate(TELEM[:n]):
        yy = y + i * 25
        track(d, (x, yy), k, fl, MUTE, 1.2)
        track(d, (x + 100, yy - 1), v, fv, CYAN if kind == "c" else DIM, 0.4)

    if n >= len(TELEM):
        yy = y + len(TELEM) * 25 + 16
        d.line([px(x), px(yy - 10), px(W - M), px(yy - 10)], fill=RULE, width=px(1))
        track(d, (x, yy), "CMD_VEL", fl, MUTE, 1.2)
        lvl = 4 + int(2.4 + 2.4 * math.sin(tick * 0.42))
        for i in range(10):
            bx = x + 100 + i * 11
            on = i < lvl
            d.rectangle([px(bx), px(yy + 1), px(bx + 7), px(yy + 10)],
                        fill=mix(CYAN_DEEP, CYAN, 0.85) if on else None,
                        outline=None if on else RULE, width=px(1))

    track(d, (x, 368), "INTERFACE GRAPHIC, NOT A LIVE", font(MONO, 9.5), FAINTTXT, 1.4)
    track(d, (x, 381), "ROBOT FEED. SPEC IS FACTUAL.", font(MONO, 9.5), FAINTTXT, 1.4)


def draw_identity(d):
    d.line([px(M), px(462), px(W - M), px(462)], fill=RULE, width=px(1))
    d.line([px(M), px(492), px(M), px(538)], fill=CYAN, width=px(2))

    fn = font(SANS, 43, "SemiBold")
    d.text((px(M + 17), px(486)), "YUSUF GUENENA", font=fn, fill=INK)
    track(d, (M + 19, 536), "ROBOTICS   ·   EMBODIED AI   ·   AUTONOMY",
          font(MONO, 12.5), mix(CYAN_MID, CYAN, 0.45), 2.4)

    f3 = font(MONO, 11.5)
    track(d, (W - M, 492), "DETROIT  /  WAYNE STATE UNIVERSITY", f3, DIM, 1.4, right=True)
    track(d, (W - M, 512), "M.S. ROBOTICS ENGINEERING  /  CARES LAB", f3, MUTE, 1.4, right=True)
    track(d, (W - M, 536), "RESEARCH SYSTEMS BUILT ON REAL HARDWARE", f3, MUTE, 1.4, right=True)


def scanline(arr, phase):
    f = scan_front(phase)
    if f is None:
        return
    h, w, _ = arr.shape
    xs = np.arange(w) / SS
    band = np.exp(-((xs - f) / 1.5) ** 2) * 0.80 + np.exp(-((xs - f) / 22.0) ** 2) * 0.11
    y0, y1 = px(78), px(404)
    arr[y0:y1] = np.clip(
        arr[y0:y1] + band[None, :, None] * np.array(CYAN, np.float32)[None, None, :],
        0, 255)


def render(phase, tick=0):
    im = Image.new("RGB", (W * SS, H * SS), BG)
    d = ImageDraw.Draw(im)
    draw_chrome(d)
    draw_ground(d, phase)
    draw_robot(d, phase)
    draw_callouts(d, phase)
    draw_scan_readout(d, phase)
    draw_telemetry(d, phase, tick)
    draw_identity(d)
    arr = np.asarray(im).astype(np.float32)
    scanline(arr, phase)
    im = Image.fromarray(arr.astype(np.uint8))
    return im.resize((W * OUT_SCALE, H * OUT_SCALE), Image.LANCZOS)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--poster")
    ap.add_argument("--frames")
    ap.add_argument("--count", type=int, default=48)
    ap.add_argument("--phase", type=float, default=0.0)
    a = ap.parse_args()
    if a.poster:
        render(a.phase).save(a.poster)
        print("poster ->", a.poster)
    if a.frames:
        os.makedirs(a.frames, exist_ok=True)
        for i in range(a.count):
            render(i / a.count, tick=i).save(f"{a.frames}/f{i:03d}.png")
        print(a.count, "frames ->", a.frames)


if __name__ == "__main__":
    main()
