"""Real GitHub contribution data, drawn as one quiet sparkline.

Writes assets/readme/activity-{light,dark}.png (transparent, no text) and
assets/readme/activity.json (the raw API response), and rewrites the single
sentence in README.md between the activity markers. Numbers live in the README
as ordinary text so they use GitHub's own typography and stay selectable.

Nothing is synthesised. If the fetch fails the script exits non-zero and leaves
every existing file alone.
"""

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import urllib.request

import numpy as np
from PIL import Image, ImageDraw

LOGIN = "yusufdxb"
W, H, SS = 460, 56, 4

THEMES = {                      # line, fill
    "light": ((0x6E, 0x77, 0x81), (0x6E, 0x77, 0x81, 34)),
    "dark": ((0x7D, 0x89, 0x95), (0x7D, 0x89, 0x95, 40)),
}

QUERY = """
query($l:String!){
  user(login:$l){
    contributionsCollection{
      restrictedContributionsCount
      contributionCalendar{
        totalContributions
        weeks{ contributionDays{ date contributionCount } }
      }
    }
    repositories(privacy:PUBLIC, ownerAffiliations:OWNER, isFork:false){ totalCount }
  }
}
"""


def token():
    for k in ("README_TOKEN", "GH_TOKEN", "GITHUB_TOKEN"):
        if os.environ.get(k):
            return os.environ[k]
    return subprocess.run(["gh", "auth", "token"], capture_output=True,
                          text=True, check=True).stdout.strip()


def fetch():
    body = json.dumps({"query": QUERY, "variables": {"l": LOGIN}}).encode()
    req = urllib.request.Request(
        "https://api.github.com/graphql", data=body,
        headers={"Authorization": f"bearer {token()}",
                 "Content-Type": "application/json",
                 "User-Agent": "yusufdxb-readme-activity"})
    with urllib.request.urlopen(req, timeout=30) as r:
        payload = json.load(r)
    if "errors" in payload:
        raise SystemExit(f"GraphQL error: {payload['errors']}")
    return payload["data"]["user"]


def summarise(user):
    cc = user["contributionsCollection"]
    cal = cc["contributionCalendar"]
    days = [d for w in cal["weeks"] for d in w["contributionDays"]]
    counts = [d["contributionCount"] for d in days]
    return {
        "fetched": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d"),
        "login": LOGIN,
        "total_contributions": cal["totalContributions"],
        "restricted_contributions": cc["restrictedContributionsCount"],
        "public_repos": user["repositories"]["totalCount"],
        "active_days": sum(1 for c in counts if c),
        "first_day": days[0]["date"],
        "last_day": days[-1]["date"],
        "days": [{"d": d["date"], "c": d["contributionCount"]} for d in days],
    }


def sparkline(weeks, theme):
    line, fill = THEMES[theme]
    w, h = W * SS, H * SS
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)

    peak = max(weeks) or 1
    pad = 5 * SS
    xs = np.linspace(pad, w - pad, len(weeks))
    ys = (h - pad) - (np.array(weeks) / peak) * (h - 2 * pad)
    pts = list(zip(xs.tolist(), ys.tolist()))

    d.polygon(pts + [(w - pad, h - pad), (pad, h - pad)], fill=fill)
    d.line(pts, fill=line + (200,), width=int(1.6 * SS), joint="curve")
    d.line([(pad, h - pad), (w - pad, h - pad)], fill=line + (55,), width=SS)
    return im.resize((W, H), Image.LANCZOS)


MARKER = re.compile(r"(<!--activity-->)(.*?)(<!--/activity-->)", re.S)


def update_readme(path, s):
    if not os.path.exists(path):
        return False
    src = open(path).read()
    # the sentence sits inside a raw HTML block, where GitHub does not parse
    # markdown, so emphasis has to be real tags
    sentence = (f"Last 12 months: <b>{s['total_contributions']:,}</b> contributions "
                f"on <b>{s['active_days']}</b> days, across "
                f"<b>{s['public_repos']}</b> public repositories.")
    new, n = MARKER.subn(lambda m: m.group(1) + sentence + m.group(3), src)
    if n and new != src:
        open(path, "w").write(new)
    return bool(n)


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(here, "..", "..", "assets", "readme"))
    ap.add_argument("--readme", default=os.path.join(here, "..", "..", "README.md"))
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)

    data = summarise(fetch())
    with open(os.path.join(a.out, "activity.json"), "w") as f:
        json.dump(data, f, indent=1)
        f.write("\n")

    days = data["days"]
    weeks = [sum(x["c"] for x in days[i:i + 7]) for i in range(0, len(days), 7)]
    for theme in THEMES:
        sparkline(weeks, theme).save(os.path.join(a.out, f"activity-{theme}.png"))

    touched = update_readme(a.readme, data)
    print(f"activity  total={data['total_contributions']} "
          f"days={data['active_days']} repos={data['public_repos']} "
          f"readme_updated={touched}")
