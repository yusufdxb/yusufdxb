"""Assemble the real Unitree GO2 visual meshes into one posed, world-space mesh.

Geometry source: go2_description/dae, the meshes the URDF <visual> blocks point
at, i.e. the surfaces RViz and Gazebo draw. Nothing here is modelled or
approximated: the only numbers used are the URDF joint origins and the joint
angles of the stance.
"""

import os

import numpy as np
import trimesh

# The visual meshes the GO2 URDF <visual> blocks point at. Not vendored here:
# they are Unitree's assets and ship with go2_description. Point GO2_DAE at a
# local checkout to rebuild the hero.
SRC = os.environ.get(
    "GO2_DAE",
    os.path.expanduser("~/workspace/ros2-go2-nav2-yolo/go2_description/dae"))
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "go2_posed.npz")

HIP_X, HIP_Y, THIGH_Y, LINK = 0.1934, 0.0465, 0.0955, 0.213

# sx (front/rear), sy (left/right), hip visual rpy, thigh mesh, calf mesh
LEGS = {
    "FL": (1, 1, (0.0, 0.0, 0.0), "thigh.dae", "calf.dae"),
    "FR": (1, -1, (np.pi, 0.0, 0.0), "thigh_mirror.dae", "calf_mirror.dae"),
    "RL": (-1, 1, (0.0, np.pi, 0.0), "thigh.dae", "calf.dae"),
    "RR": (-1, -1, (np.pi, np.pi, 0.0), "thigh_mirror.dae", "calf_mirror.dae"),
}

_cache = {}


def load(name):
    if name not in _cache:
        s = trimesh.load(os.path.join(SRC, name), process=False)
        _cache[name] = s.to_geometry() if isinstance(s, trimesh.Scene) else s
    return _cache[name].copy()


def T(x=0.0, y=0.0, z=0.0):
    m = np.eye(4)
    m[:3, 3] = (x, y, z)
    return m


def Rx(a):
    c, s = np.cos(a), np.sin(a)
    return np.array([[1, 0, 0, 0], [0, c, -s, 0], [0, s, c, 0], [0, 0, 0, 1.0]])


def Ry(a):
    c, s = np.cos(a), np.sin(a)
    return np.array([[c, 0, s, 0], [0, 1, 0, 0], [-s, 0, c, 0], [0, 0, 0, 1.0]])


def Rz(a):
    c, s = np.cos(a), np.sin(a)
    return np.array([[c, -s, 0, 0], [s, c, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1.0]])


def rpy(r, p, y):
    return Rz(y) @ Ry(p) @ Rx(r)


def build(stance=None, per_leg=None):
    """stance: (hip, thigh, calf) applied to every leg.
    per_leg: optional {tag: (hip, thigh, calf)} overrides, for a natural pose."""
    stance = stance or (0.0, 0.78, -1.56)
    per_leg = per_leg or {}
    parts, tags = [], []

    base = load("base.dae")
    parts.append(base)
    tags.append(np.full(len(base.faces), 0))       # 0 = body

    for i, (tag, (sx, sy, hip_rpy, thigh_mesh, calf_mesh)) in enumerate(LEGS.items()):
        q0, q1, q2 = per_leg.get(tag, stance)
        hip_T = T(sx * HIP_X, sy * HIP_Y, 0) @ Rx(q0)
        thigh_T = hip_T @ T(y=sy * THIGH_Y) @ Ry(q1)
        calf_T = thigh_T @ T(z=-LINK) @ Ry(q2)
        foot_T = calf_T @ T(z=-LINK)

        for mesh_name, xf, code in (
                ("hip.dae", hip_T @ rpy(*hip_rpy), 1),
                (thigh_mesh, thigh_T, 2),
                (calf_mesh, calf_T, 3),
                ("foot.dae", foot_T, 4)):
            m = load(mesh_name)
            m.apply_transform(xf)
            parts.append(m)
            tags.append(np.full(len(m.faces), code))

    robot = trimesh.util.concatenate(parts)
    face_tag = np.concatenate(tags)

    # drop the robot onto z = 0 so the feet sit on the floor plane
    robot.apply_translation((0, 0, -robot.bounds[0][2]))
    return robot, face_tag


NATURAL = {   # a settled standing stance, front legs a touch more upright
    "FL": (0.02, 0.74, -1.50),
    "FR": (-0.02, 0.74, -1.50),
    "RL": (0.03, 0.82, -1.60),
    "RR": (-0.03, 0.82, -1.60),
}


if __name__ == "__main__":
    for label, kw in (("default", {}), ("natural", {"per_leg": NATURAL})):
        r, t = build(**kw)
        print(f"{label:8s} tris={len(r.faces):7d} verts={len(r.vertices):7d} "
              f"extents={np.round(r.extents, 4).tolist()} "
              f"bounds_z={np.round(r.bounds[:, 2], 4).tolist()} "
              f"watertight={r.is_watertight}")
    r, t = build(per_leg=NATURAL)
    np.savez_compressed(OUT,
                        V=r.vertices.astype(np.float32),
                        F=r.faces.astype(np.int32),
                        FT=t.astype(np.int8))
    print("saved", OUT)
