"""Fetch real GitHub contribution data and render assets/readme/activity.png.

Nothing here is synthesised. Every number drawn comes from the GitHub GraphQL
contributions API in the same run, and the raw response is written next to the
image as activity.json so the figure can be checked against its source. If the
fetch fails the script exits non-zero and leaves the existing asset alone.
"""

import argparse
import datetime as dt
import json
import os
import subprocess
import urllib.request

from style import (BG, CYAN, CYAN_DEEP, CYAN_MID, DIM, FAINTTXT, INK, MONO,
                   MONOB, MUTE, RULE, RULE_HI, canvas, corners, finish,
                   font, hline, mix, px, track, vline)

W, H = 900, 318
LOGIN = "yusufdxb"

QUERY = """
query($l:String!){
  user(login:$l){
    contributionsCollection{
      restrictedContributionsCount
      totalCommitContributions
      totalPullRequestContributions
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
    streak = best = 0
    for c in counts:
        streak = streak + 1 if c else 0
        best = max(best, streak)
    return {
        "fetched": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d"),
        "login": LOGIN,
        "total_contributions": cal["totalContributions"],
        "restricted_contributions": cc["restrictedContributionsCount"],
        "commits": cc["totalCommitContributions"],
        "pull_requests": cc["totalPullRequestContributions"],
        "public_repos": user["repositories"]["totalCount"],
        "active_days": sum(1 for c in counts if c),
        "busiest_day": max(counts) if counts else 0,
        "longest_streak": best,
        "first_day": days[0]["date"],
        "last_day": days[-1]["date"],
        "days": [{"d": d["date"], "c": d["contributionCount"]} for d in days],
    }


# ------------------------------------------------------------------ rendering
CX0, CX1 = 46, 854
CY0, CY1 = 158, 248


def stat(d, x, value, label):
    track(d, (x, 84), value, font(MONOB, 29), INK, 0.6)
    track(d, (x + 2, 124), label, font(MONO, 10.5), MUTE, 2.2)


def render(s):
    im, d = canvas(W, H)
    corners(d, 22, 22, W - 22, H - 22, 14, RULE)

    track(d, (46, 44), "07", font(MONO, 12), CYAN_MID, 2.0)
    track(d, (78, 44), "ACTIVITY", font(MONOB, 12), DIM, 2.8)
    track(d, (W - 46, 44), f"GITHUB  /  {s['first_day']}  TO  {s['last_day']}",
          font(MONO, 11), MUTE, 1.6, right=True)
    hline(d, 46, W - 46, 65)

    stat(d, 46, f"{s['total_contributions']:,}", "CONTRIBUTIONS")
    stat(d, 260, f"{s['active_days']}", "ACTIVE DAYS")
    stat(d, 448, f"{s['longest_streak']}", "LONGEST STREAK")
    stat(d, 668, f"{s['public_repos']}", "PUBLIC REPOS")
    for x in (240, 428, 648):
        vline(d, x, 86, 132, RULE)

    # weekly totals, aggregated from the daily calendar
    days = s["days"]
    weeks = [sum(x["c"] for x in days[i:i + 7]) for i in range(0, len(days), 7)]
    peak = max(weeks) or 1
    n = len(weeks)

    hline(d, CX0, CX1, CY1, RULE_HI)
    for frac in (0.5, 1.0):
        y = CY1 - (CY1 - CY0) * frac
        for x in range(CX0 + 44, CX1, 9):
            d.line([px(x), px(y), px(x + 3), px(y)], fill=RULE, width=px(1))
        track(d, (CX0, y - 5), f"{int(peak * frac)}/WK", font(MONO, 9.5),
              FAINTTXT, 1.0)

    pts = []
    for i, v in enumerate(weeks):
        x = CX0 + (CX1 - CX0) * (i / max(1, n - 1))
        y = CY1 - (CY1 - CY0) * (v / peak)
        pts.append((x, y))

    poly = [(px(x), px(y)) for x, y in pts]
    d.polygon(poly + [(px(CX1), px(CY1)), (px(CX0), px(CY1))],
              fill=mix(BG, CYAN_DEEP, 0.72))
    d.line(poly, fill=CYAN, width=px(1.4), joint="curve")
    for (x, y), v in zip(pts, weeks):
        if v == peak:
            d.ellipse([px(x - 2.6), px(y - 2.6), px(x + 2.6), px(y + 2.6)], fill=CYAN)
            lab = f"PEAK {v}"
            left = x > (CX0 + CX1) / 2
            track(d, (x + (-10 if left else 10), y - 6), lab, font(MONO, 10),
                  CYAN, 1.2, right=left)

    # month ticks
    seen = set()
    for i in range(0, len(days), 7):
        date = dt.date.fromisoformat(days[i]["d"])
        key = (date.year, date.month)
        if key in seen or date.day > 7:
            continue
        seen.add(key)
        x = CX0 + (CX1 - CX0) * ((i // 7) / max(1, n - 1))
        vline(d, x, CY1, CY1 + 5, RULE_HI)
        track(d, (x, CY1 + 10), date.strftime("%b").upper(), font(MONO, 9.5),
              FAINTTXT, 1.2, center=True)

    track(d, (46, H - 32), "SOURCE: GITHUB GRAPHQL CONTRIBUTIONS API",
          font(MONO, 10), FAINTTXT, 1.3)
    scope = (f"{s['restricted_contributions']:,} IN PRIVATE REPOS"
             if s["restricted_contributions"] else "PUBLIC CONTRIBUTIONS ONLY")
    track(d, (W - 46, H - 32), f"{scope}  ·  REGENERATED DAILY",
          font(MONO, 10), FAINTTXT, 1.3, right=True)
    return finish(im, W, H)


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(here, "..", "..", "assets", "readme"))
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    data = summarise(fetch())
    with open(os.path.join(a.out, "activity.json"), "w") as f:
        json.dump(data, f, indent=1)
        f.write("\n")
    render(data).save(os.path.join(a.out, "activity.png"))
    print(f"activity.png  total={data['total_contributions']} "
          f"active={data['active_days']} streak={data['longest_streak']} "
          f"repos={data['public_repos']}")
