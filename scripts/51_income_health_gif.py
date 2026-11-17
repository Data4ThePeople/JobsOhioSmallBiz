#!/usr/bin/env python3
"""GIF: Ohio census tracts, median household income against seven health measures.

A sneak peek of the TractEconHealth project, Ohio only. One frame per measure,
each a scatter of every Ohio tract that has both an income and the measure.
No health index, so there is nothing to explain, and no trend line or
annotation, so the chart claims nothing beyond the dots.

Every frame is real data. Nothing is interpolated between frames.

  x  median household income, ACS 2020-2024 5-year (B19013), 2024 dollars.
     Top-coded by the Census Bureau at $250,001; those tracts sit at the cap.
  y  percent of adults, CDC PLACES 2025 tract estimates. Model-based, not
     counted: CDC predicts each tract from survey answers and the tract's
     population makeup, with tract poverty as one input.

Reads data/health/oh_tracts_2024.csv (scripts/50_oh_tract_extract.py).
Writes posts/<slug>/social/income-health-ohio.gif.

Usage: 51_income_health_gif.py [slug]
"""
import csv
import io
import math
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
W, H, DPI = 1200, 675, 100
HOLD_MS = 2500
BG, INK, MUTED, DOT, GRID = "#fcfcfb", "#111111", "#6b6a66", "#1F6F6B", "#e6e5e0"

# column, title, plain-words definition (CDC PLACES measure definitions)
MEASURES = [
    ("diabetes", "Diabetes",
     "Share of adults ever told by a doctor or other health professional they have diabetes"),
    ("obesity", "Obesity",
     "Share of adults with a body mass index of 30 or more"),
    ("smoking", "Smoking",
     "Share of adults who currently smoke cigarettes"),
    ("inactivity", "No leisure-time physical activity",
     "Share of adults who did no physical activity outside of work in the past month"),
    ("short_sleep", "Short sleep",
     "Share of adults who usually sleep less than 7 hours a night"),
    ("food_insecurity", "Food insecurity",
     "Share of adults whose food ran out in the past year before they had money to buy more"),
    ("loneliness", "Loneliness",
     "Share of adults who feel lonely always, usually or sometimes"),
]

plt.rcParams.update({
    "font.family": ["Helvetica Neue", "Helvetica", "Arial"],
    "text.color": INK, "axes.labelcolor": MUTED,
    "xtick.color": MUTED, "ytick.color": MUTED,
})


def load():
    rows = list(csv.DictReader((ROOT / "data/health/oh_tracts_2024.csv").open()))
    return rows


def frame(rows, col, title, definition):
    pts = [(float(r["med_hh_income"]), float(r[col])) for r in rows
           if r["med_hh_income"] and r[col]]
    xs, ys = zip(*pts)
    top = max(ys)
    ymax = 10 * math.ceil(top / 10)

    fig = plt.figure(figsize=(W / DPI, H / DPI), dpi=DPI, facecolor=BG)
    fig.text(0.04, 0.925, f"Income and {title.lower()}, Ohio census tracts",
             fontsize=25, fontweight="bold")
    fig.text(0.04, 0.868, definition + ". Each dot is one census tract.",
             fontsize=14.5, color=MUTED)
    ax = fig.add_axes([0.085, 0.16, 0.875, 0.65], facecolor=BG)
    ax.scatter(xs, ys, s=9, color=DOT, alpha=0.35, linewidths=0)
    ax.set_xlim(0, 255000)
    ax.set_ylim(0, ymax)
    ax.xaxis.set_major_formatter(FuncFormatter(
        lambda v, _: "$0" if v == 0 else f"${v/1000:.0f}k"))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.0f}%"))
    ax.set_xticks(range(0, 250001, 50000))
    ax.set_xlabel("Median household income", fontsize=13.5, labelpad=8)
    ax.set_ylabel(f"{title}, % of adults", fontsize=13.5, labelpad=8)
    ax.grid(True, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color("#c9c8c2")
    ax.tick_params(labelsize=12.5, length=0)
    fig.text(0.04, 0.035,
             f"{len(pts):,} tracts. Income: ACS 2020-2024; \\$250k or more shown at \\$250k. "
             "Health: CDC PLACES 2025, model-based estimates.",
             fontsize=11.5, color=MUTED)
    fig.text(0.96, 0.035, "Data 4 The People", fontsize=12.5, fontweight="bold",
             ha="right")
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=DPI, facecolor=BG)
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf).convert("RGB"), len(pts), top


def main(argv):
    slug = argv[0] if argv else "ohio-income-health"
    out = ROOT / "posts" / slug / "social"
    out.mkdir(parents=True, exist_ok=True)
    rows = load()
    frames = []
    for col, title, d in MEASURES:
        im, n, top = frame(rows, col, title, d)
        im.save(out / f"income-health-{col}.png")
        frames.append(im.convert("P", palette=Image.ADAPTIVE, colors=64))
        print(f"  {col:16s} {n} dots, max {top}")
    gif = out / "income-health-ohio.gif"
    frames[0].save(gif, save_all=True, append_images=frames[1:],
                   duration=HOLD_MS, loop=0, optimize=True, disposal=2)
    print(f"wrote {gif.relative_to(ROOT)}  {W}x{H}  {len(frames)} frames  "
          f"{len(frames)*HOLD_MS/1000:.1f}s  {gif.stat().st_size/1024:.0f} KB")


if __name__ == "__main__":
    main(sys.argv[1:])
