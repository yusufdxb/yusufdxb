"""Render assets/readme/system-map.png: the layer stack this work spans.

Signal runs top to bottom, perception into the robot. The return path on the
right is the reliability loop, which is where most of these repos actually live.
"""

import argparse
import os

from PIL import Image, ImageDraw

from style import (BG, CYAN, CYAN_DEEP, CYAN_MID, DIM, FAINTTXT, INK, MONO,
                   MONOB, MUTE, RULE, RULE_HI, SS, canvas, corners, finish,
                   font, hline, mix, px, rect, track, vline)

W, H = 900, 528

X_RAIL = 46
X_BOX0, X_BOX1 = 78, 500
X_RET = 538
X_LABEL = 552
X_REPO = 600
ROW_H = 60
BOX_H = 46
Y0 = 104

LAYERS = [
    ("L6", "PERCEPTION", "RGB-D · MIC ARRAY · LIDAR",
     ["go2-semantic-nav", "openvocab-tsdf"]),
    ("L5", "REASONING", "SCENE GRAPH · LANGUAGE GROUNDING",
     ["GO2-seeing-eye-dog", "come-here"]),
    ("L4", "PLANNING", "NAV2 · COSTMAP · ROUTE-RISK MEMORY",
     ["riskgraph-go2", "ros2-go2-nav2-yolo"]),
    ("L3", "SAFETY", "OOD GATE · FAIL-CLOSED ENVELOPE",
     ["policy-health-monitor", "helix"]),
    ("L2", "CONTROL", "LEARNED LOCOMOTION · ONNX · SLEW CAP",
     ["go2-phoenix", "ashfall"]),
    ("L1", "PLATFORM", "GO2 EDU · JETSON ORIN NX · ROS 2",
     ["BlackBoxRS", "go2-jetson-setup-guide"]),
]

RETURN_FROM, RETURN_TO = 5, 3


def arrow_down(d, x, y0, y1, col):
    vline(d, x, y0, y1 - 5, col)
    d.polygon([(px(x), px(y1)), (px(x - 3.4), px(y1 - 6)), (px(x + 3.4), px(y1 - 6))],
              fill=col)


def rotated_label(im, x, y, text, size, colour, spacing=1.8):
    """Bottom-to-top text, pasted through a mask so it cannot erase the art."""
    fnt = font(MONO, size)
    probe = ImageDraw.Draw(Image.new("L", (1, 1)))
    w = int(sum(probe.textlength(c, font=fnt) for c in text)
            + spacing * SS * (len(text) - 1)) + 4
    h = int(size * SS * 1.5)
    mask = Image.new("L", (w, h), 0)
    md = ImageDraw.Draw(mask)
    cx = 2
    for c in text:
        md.text((cx, 0), c, font=fnt, fill=255)
        cx += md.textlength(c, font=fnt) + spacing * SS
    mask = mask.rotate(90, expand=True)
    tint = Image.new("RGB", mask.size, colour)
    im.paste(tint, (px(x), px(y) - mask.size[1]), mask)


def render():
    im, d = canvas(W, H)
    corners(d, 22, 22, W - 22, H - 22, 14, RULE)

    track(d, (X_RAIL, 44), "04", font(MONO, 12), CYAN_MID, 2.0)
    track(d, (X_RAIL + 32, 44), "SYSTEM MAP", font(MONOB, 12), DIM, 2.8)
    track(d, (W - X_RAIL, 44), "SIGNAL FLOWS DOWN  /  FAULTS FLOW BACK UP",
          font(MONO, 11), MUTE, 1.6, right=True)
    hline(d, X_RAIL, W - X_RAIL, 65)

    track(d, (X_BOX0, 82), "LAYER", font(MONO, 10.5), FAINTTXT, 2.4)
    track(d, (X_REPO, 82), "WHERE THE WORK LIVES", font(MONO, 10.5), FAINTTXT, 2.4)

    for i, (tag, name, detail, repos) in enumerate(LAYERS):
        y = Y0 + i * ROW_H
        yc = y + BOX_H / 2
        accent = i in (RETURN_TO, RETURN_FROM)

        track(d, (X_RAIL, yc - 7), tag, font(MONO, 12), FAINTTXT, 1.4)
        rect(d, X_BOX0, y, X_BOX1, y + BOX_H, outline=RULE_HI if accent else RULE)
        vline(d, X_BOX0 + 1.5, y + 1.5, y + BOX_H - 1.5,
              CYAN if accent else mix(BG, CYAN_DEEP, 0.85), width=2)

        track(d, (X_BOX0 + 20, yc - 10), name, font(MONOB, 19), INK, 1.6)
        track(d, (X_BOX1 - 18, yc - 6), detail, font(MONO, 11.5), DIM, 0.8, right=True)

        for k, r in enumerate(repos):
            track(d, (X_REPO, yc - 15 + k * 17), r, font(MONO, 13),
                  DIM if k == 0 else MUTE, 0.6)

        if i < len(LAYERS) - 1:
            arrow_down(d, X_BOX0 + 52, y + BOX_H + 2, y + ROW_H - 2, RULE_HI)

    y_from = Y0 + RETURN_FROM * ROW_H + BOX_H / 2
    y_to = Y0 + RETURN_TO * ROW_H + BOX_H / 2
    d.line([px(X_BOX1), px(y_from), px(X_RET), px(y_from)], fill=CYAN_MID, width=px(1))
    d.line([px(X_RET), px(y_from), px(X_RET), px(y_to)], fill=CYAN_MID, width=px(1))
    d.line([px(X_RET), px(y_to), px(X_BOX1 + 6), px(y_to)], fill=CYAN_MID, width=px(1))
    d.polygon([(px(X_BOX1), px(y_to)), (px(X_BOX1 + 7), px(y_to - 3.6)),
               (px(X_BOX1 + 7), px(y_to + 3.6))], fill=CYAN_MID)
    rotated_label(im, X_LABEL, y_from - 6, "OBSERVE / RECOVER", 11, CYAN)

    hline(d, X_RAIL, W - X_RAIL, H - 56)
    track(d, (X_RAIL, H - 44),
          "REPOS SIT AT THE LAYER THEY OWN. SEVERAL SPAN MORE THAN ONE.",
          font(MONO, 11), MUTE, 1.4)
    track(d, (X_RAIL, H - 28),
          "ivf AND physx-newton-bench SIT OFF THIS STACK. THEY GATE WHAT IS "
          "ALLOWED ONTO IT.", font(MONO, 11), FAINTTXT, 1.4)
    return finish(im, W, H)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "..",
        "assets", "readme", "system-map.png"))
    a = ap.parse_args()
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    render().save(a.out)
    print(a.out, os.path.getsize(a.out) // 1024, "KB")
