# README asset generation

The hero is a particle rendering of the **real** Unitree GO2 surface geometry,
not a model of one. Nothing here approximates the robot from dimensions.

```
go2_asset.py        assembles the go2_description visual meshes with the URDF
                    joint transforms into one posed, world-space mesh
gorender.py         area-weighted surface sampling, camera, splatting, shading
particles.py        the particle treatment: which samples are drawn, how dark,
                    how large, per theme
build_hero.py       the reconstruction loop -> assets/readme/hero-{light,dark}.webp
```

## Where the geometry comes from

`go2_asset.py` loads the meshes the GO2 URDF `<visual>` blocks point at
(`base.dae`, `hip.dae`, `thigh.dae`, `thigh_mirror.dae`, `calf.dae`,
`calf_mirror.dae`, `foot.dae`), applies the URDF joint origins and a standing
stance, and concatenates them into a single world-space mesh of about 399k
triangles. The assembled robot measures 0.70 x 0.34 x 0.42 m against Unitree's
published GO2 standing dimensions of 70 x 31 x 40 cm.

Those meshes are Unitree's and are not vendored here. Point `GO2_DAE` at a
local `go2_description/dae` to rebuild:

```bash
python -m pip install "pillow>=10" "numpy>=1.26" trimesh pycollada
GO2_DAE=/path/to/go2_description/dae python tools/readme/go2_asset.py
python tools/readme/build_hero.py --recache
```

`go2_asset.py` writes `go2_posed.npz`, which is gitignored: it is a derived
artifact of someone else's mesh, and it is large.

## Sampling

Particles are drawn with area-weighted barycentric sampling across triangle
surfaces, never from vertices, so mesh topology never shows through as banding.
Density and weight follow the shaded tone of the real surface and the
silhouette, the way an engraving does, rather than coating the robot evenly.
Samples on the far side of the shell survive only where they land on a back
contour; kept evenly they paint a flat haze over the body instead of reading as
volume.

## The loop

The geometry never changes. Each particle gets a reveal rank from a smooth
spatial field, and the animation only slides a threshold across those ranks, so
the robot dissolves and rebuilds without deforming. Frame 0 is the fully
resolved robot, so any context that shows a single frame shows the finished
image. Both themes draw on full transparency, so the robot sits on the GitHub
page rather than inside a panel.
