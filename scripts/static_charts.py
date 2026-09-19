#!/usr/bin/env python3
"""Static dark-palette PNGs for the post, rendered from dist/data.json, the
same file the page reads, so they can never disagree with it.

  01-recipients-vs-dollars.png   two 100% bars: share of business recipients
                                 and share of paid dollars, small vs. large
  02-by-year.png                 dollars paid each fiscal year, stacked by size
  03-home-state.png              same two bars for Ohio-headquartered vs. not

House palette: background #181A1B, text #BBBDC0, legends as colored words.
Chart hues are the page's dark-mode series colors (validated for the dark
surface): small #3987e5, large #d95926, unresolved #6b6e70, Ohio #2fa32f,
elsewhere #9085e9."""
import json, sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "dist" / "data.json"
OUT = ROOT / "posts" / "images"

BG, INK, MUTED, GRID = "#181A1B", "#BBBDC0", "#8C9094", "#2A2E31"
SMALL, LARGE, UNK, OHIO, OTHER = "#3987e5", "#d95926", "#6b6e70", "#2fa32f", "#9085e9"
SOURCE = "JobsOhio Form 990 Schedule I, FY2014 to FY2024 (IRS e-file data); Data 4 The People analysis."
CREDIT = "Built by Data 4 The People"


def figure(width=8.4, height=4.6):
    fig, ax = plt.subplots(figsize=(width, height), dpi=200)
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(colors=MUTED, labelsize=9, length=0)
    ax.set_axisbelow(True)
    return fig, ax


def frame(fig, title, subtitle, top=0.78, left=0.075):
    fig.text(0.055, 0.955, title, color=INK, fontsize=14, fontweight="bold", va="top")
    fig.text(0.055, 0.893, subtitle, color=MUTED, fontsize=10, va="top")
    fig.text(0.055, 0.035, SOURCE, color=MUTED, fontsize=8.5)
    fig.text(0.945, 0.035, CREDIT, color=MUTED, fontsize=8.5, ha="right")
    fig.subplots_adjust(left=left, right=0.975, top=top, bottom=0.115)


def word_legend(fig, items, y=0.836, x=0.055):
    for label, colour in items:
        t = fig.text(x, y, label, color=colour, fontsize=9.5, fontweight="bold", va="top")
        fig.canvas.draw()
        x += t.get_window_extent().width / fig.get_size_inches()[0] / fig.dpi + 0.022


def pct(x):
    return f"{100 * x:.0f}%" if x >= 0.095 else f"{100 * x:.1f}%"


def two_bars(block, groups, colors, labels, title, subtitle, fname, key="500"):
    src = block[key] if key in block else block
    rows = [("Recipients", src["parents"]), ("Dollars", src["cash"])]
    fig, ax = figure(height=3.6)
    frame(fig, title, subtitle, top=0.80, left=0.15)
    present = [g for g in groups if any(o.get(g, {"share": 0})["share"] > 0 for _, o in rows)]
    word_legend(fig, [(labels[g], colors[g]) for g in present])
    for i, (name, o) in enumerate(rows):
        x = 0
        for g in groups:
            s = o.get(g, {"share": 0})["share"]
            if s <= 0:
                continue
            ax.barh(1 - i, s, left=x, height=0.62, color=colors[g], edgecolor=BG, linewidth=1.5)
            if s > 0.07:
                ax.text(x + s / 2, 1 - i, pct(s), ha="center", va="center", color="white" if g != "unknown" else INK, fontsize=10, fontweight="bold")
            x += s
    ax.set_yticks([1, 0]); ax.set_yticklabels([r[0] for r in rows], color=INK, fontsize=10.5)
    ax.set_xlim(0, 1); ax.set_xticks([]); ax.spines["bottom"].set_visible(False)
    fig.savefig(OUT / fname, facecolor=BG); plt.close(fig)
    print("wrote", fname)


def by_year(block, fname):
    by_fy = block["by_fy"]
    fys = sorted(by_fy)
    fig, ax = figure()
    frame(fig, "Dollars JobsOhio paid each fiscal year, by company size",
          "Grants over $5,000 paid to businesses, per Schedule I. Fiscal years end June 30.", top=0.78)
    word_legend(fig, [("Small (under 500 employees)", SMALL), ("Large (500 or more)", LARGE), ("Unresolved", UNK)])
    xs = range(len(fys))
    bottoms = [0] * len(fys)
    for g, c in (("small", SMALL), ("large", LARGE), ("unknown", UNK)):
        vals = [by_fy[f].get(g, 0) / 1e6 for f in fys]
        ax.bar(xs, vals, bottom=bottoms, color=c, width=0.7, edgecolor=BG, linewidth=1.2)
        bottoms = [b + v for b, v in zip(bottoms, vals)]
    ax.set_xticks(list(xs)); ax.set_xticklabels([f"FY{f[2:]}" for f in fys])
    ax.yaxis.grid(True, color=GRID, linewidth=0.8)
    ax.set_yticks(ax.get_yticks()); ax.set_yticklabels([f"${int(v)}M" if v else "0" for v in ax.get_yticks()])
    fig.savefig(OUT / fname, facecolor=BG); plt.close(fig)
    print("wrote", fname)


def main():
    d = json.loads(DATA.read_text())
    OUT.mkdir(parents=True, exist_ok=True)
    biz = d["business"]
    two_bars(biz, ["small", "large", "unknown"], {"small": SMALL, "large": LARGE, "unknown": UNK},
             {"small": "Small (under 500 employees)", "large": "Large (500 or more)", "unknown": "Unresolved"},
             "JobsOhio business grants: recipients vs. dollars, by company size",
             "Parent company size at the time of the grant. Recipients counted once each.", "01-recipients-vs-dollars.png")
    two_bars(biz["home"], ["ohio", "other", "unknown"], {"ohio": OHIO, "other": OTHER, "unknown": UNK},
             {"ohio": "Headquartered in Ohio", "other": "Headquartered elsewhere", "unknown": "Unresolved"},
             "JobsOhio business grants: recipients vs. dollars, by home state",
             "Where the ultimate parent was headquartered at the time of the grant.", "03-home-state.png", key=None)
    by_year(biz, "02-by-year.png")


if __name__ == "__main__":
    sys.exit(main())
