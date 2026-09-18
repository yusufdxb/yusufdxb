"""Scene assembly for the hero: real robot geometry, sampled as dust."""
import os
import numpy as np
import trimesh
import gorender as gr

HERE = os.path.dirname(os.path.abspath(__file__))
_cache = {}


def go2():
    if "go2" not in _cache:
        d = np.load(os.path.join(HERE, "go2_posed.npz"))
        _cache["go2"] = (d["V"].astype(np.float64), d["F"], d["FT"])
    return _cache["go2"]


def load_obj(path, scale=1.0, rot_z=0.0, translate=(0, 0, 0)):
    key = (path, scale, rot_z, translate)
    if key not in _cache:
        m = trimesh.load(path, process=False)
        if isinstance(m, trimesh.Scene):
            m = m.to_geometry()
        m.apply_scale(scale)
        if rot_z:
            c, s = np.cos(rot_z), np.sin(rot_z)
            R = np.eye(4); R[0, 0] = c; R[0, 1] = -s; R[1, 0] = s; R[1, 1] = c
            m.apply_transform(R)
        m.apply_translation(translate)
        _cache[key] = m
    return _cache[key]


def sample_mesh(V, F, n, seed=0):
    FT = np.zeros(len(F), np.int8)
    rng = np.random.default_rng(100 + seed)
    return gr.sample_surface(V, F, FT, n, rng=rng)[:2]


def build(parts):
    """parts: list of (V, F, count, object_id). Returns pts, nrm, obj."""
    P, N, O = [], [], []
    for i, (V, F, n, oid) in enumerate(parts):
        p, nr = sample_mesh(V, F, n, seed=i)
        P.append(p); N.append(nr); O.append(np.full(len(p), oid, np.int16))
    return np.vstack(P), np.vstack(N), np.concatenate(O)
