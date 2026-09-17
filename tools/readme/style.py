"""Shared palette, typography and drawing helpers for the README assets.

Every asset is drawn through this module so the hero, the system map and the
activity plot share one type scale and one colour set. Drawing happens on a
supersampled canvas and is downsampled at the end, which is where the
antialiasing comes from.
"""

import os

from PIL import Image, ImageDraw, ImageFont

SS = 3            # supersample factor
OUT_SCALE = 2     # final pixel scale relative to the logical design units

BG        = (7, 9, 11)
GRID      = (18, 23, 27)
RULE      = (34, 43, 50)
RULE_HI   = (52, 65, 74)
INK       = (233, 239, 242)
DIM       = (132, 147, 157)
MUTE      = (88, 101, 110)
FAINTTXT  = (62, 73, 81)
CYAN      = (110, 231, 250)
CYAN_MID  = (52, 150, 172)
CYAN_DEEP = (26, 74, 88)
AMBER     = (226, 163, 76)
AMBER_DIM = (120, 88, 44)

_HERE = os.path.dirname(os.path.abspath(__file__))


def _resolve(*candidates):
    for c in candidates:
        if os.path.exists(c):
            return c
    return candidates[0]


# The mono faces are vendored in tools/readme/fonts so the activity panel
# renders identically on a GitHub Actions runner, which has no font of ours.
MONO = _resolve(os.path.join(_HERE, "fonts", "DejaVuSansMono.ttf"),
                "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf")
MONOB = _resolve(os.path.join(_HERE, "fonts", "DejaVuSansMono-Bold.ttf"),
                 "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf")
# Inter is used only for the hero wordmark, which is built locally, never in CI.
SANS = _resolve(os.path.expanduser("~/.local/share/fonts/demo/Inter.ttf"),
                "/usr/share/fonts/truetype/inter/Inter.ttf")

_fc = {}


def font(path, size, variation=None):
    key = (path, size, variation)
    if key not in _fc:
        f = ImageFont.truetype(path, int(round(size * SS)))
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
    t = max(0.0, min(1.0, float(t)))
    return tuple(int(round(x + (y - x) * t)) for x, y in zip(a, b))


def canvas(w, h, bg=BG):
    im = Image.new("RGB", (w * SS, h * SS), bg)
    return im, ImageDraw.Draw(im)


def finish(im, w, h):
    return im.resize((w * OUT_SCALE, h * OUT_SCALE), Image.LANCZOS)


def text_w(d, s, fnt, spacing=0.0):
    return (sum(d.textlength(c, font=fnt) for c in s)
            + spacing * SS * max(0, len(s) - 1)) / SS


def track(d, xy, s, fnt, fill, spacing=0.0, right=False, center=False):
    """Draw text with manual letter tracking. Coordinates are logical units."""
    sp = spacing * SS
    ws = [d.textlength(c, font=fnt) for c in s]
    total = sum(ws) + sp * max(0, len(s) - 1)
    x, y = px(xy[0]), px(xy[1])
    if right:
        x -= total
    elif center:
        x -= total / 2
    for c, w in zip(s, ws):
        d.text((x, y), c, font=fnt, fill=fill)
        x += w + sp
    return total / SS


def hline(d, x0, x1, y, fill=RULE, width=1):
    d.line([px(x0), px(y), px(x1), px(y)], fill=fill, width=px(width))


def vline(d, x, y0, y1, fill=RULE, width=1):
    d.line([px(x), px(y0), px(x), px(y1)], fill=fill, width=px(width))


def rect(d, x0, y0, x1, y1, outline=RULE, fill=None, width=1):
    d.rectangle([px(x0), px(y0), px(x1), px(y1)], outline=outline, fill=fill,
                width=px(width))


def corners(d, x0, y0, x1, y1, size=13, fill=RULE, width=1):
    for cx, cy, sx, sy in ((x0, y0, 1, 1), (x1, y0, -1, 1),
                           (x0, y1, 1, -1), (x1, y1, -1, -1)):
        d.line([px(cx), px(cy), px(cx + size * sx), px(cy)], fill=fill, width=px(width))
        d.line([px(cx), px(cy), px(cx), px(cy + size * sy)], fill=fill, width=px(width))


def section_head(d, x, y, number, title, right_note=None, w=None):
    """`01 // HERO` style section header with a rule under it."""
    track(d, (x, y), number, font(MONO, 12), CYAN_MID, 2.0)
    track(d, (x + 34, y), title, font(MONOB, 12), DIM, 2.6)
    if right_note and w:
        track(d, (w - x, y), right_note, font(MONO, 11), MUTE, 1.6, right=True)
    hline(d, x, (w - x) if w else x + 200, y + 21)
