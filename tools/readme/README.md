# README asset generation

Every image on the profile is generated here. Nothing is fetched from a
third-party stats or badge service at render time.

```
style.py              palette, type scale, drawing helpers
go2_model.py          3D GO2 EDU geometry, surface sampling, camera
render_hero.py        one hero frame at a given point in the scan loop
build_hero.py         hero.gif + hero.png
render_system_map.py  system-map.png
render_activity.py    activity.png + activity.json, from the GitHub API
fonts/                DejaVu Sans Mono, vendored so CI renders identically
```

## Regenerate

```bash
python -m pip install "pillow>=10" "numpy>=1.26"

python tools/readme/build_hero.py          # hero.gif, hero.png
python tools/readme/render_system_map.py   # system-map.png
python tools/readme/render_activity.py     # activity.png, activity.json
```

The hero also uses Inter for the wordmark. If Inter is not installed the
script falls back to whatever the path resolves to, so build the hero on a
machine that has it. The hero is never rebuilt in CI.

`render_activity.py` needs a GitHub token in `README_TOKEN`, `GH_TOKEN` or
`GITHUB_TOKEN`, and otherwise falls back to `gh auth token`. It writes the raw
API response to `assets/readme/activity.json` next to the image, so any number
on the panel can be checked against its source. If the fetch fails it exits
non-zero rather than drawing a stale or invented figure.

`.github/workflows/readme-activity.yml` runs the activity script daily and
commits the result only when it changes.

## The hero loop

The loop opens on the fully acquired frame and holds there for about two
seconds, then dims to raw return, sweeps a scan front left to right, and
settles the telemetry back in. That ordering is deliberate: anything that shows
only the first frame of the GIF shows the finished image.
