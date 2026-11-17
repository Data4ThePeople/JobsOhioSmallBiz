#!/usr/bin/env python3
"""Hero for ohio-income-health: the Ohio map, total JobsOhio dollars by county.

Re-rendered at 1680x1080 rather than padded from the 1200x675 GIF frame, so
the type is legible at hero size. Same data, bands, colors and circle rule as
scripts/52_map_gif.py (total-dollars frame), read from dist/map_data.json.

Writes posts/<slug>/images/<slug>-hero-1680x1080.png and
<slug>-hero-source.png (the same render, kept as the source per PROCESS.md).

Usage: 57_hero_map.py [slug]
"""
import json
import shutil
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as Poly, Rectangle
from matplotlib.collections import PatchCollection

ROOT = Path(__file__).resolve().parent.parent
W, H, DPI = 1680, 1080, 100
BG, INK, MUTED, BORDER = "#fcfcfb", "#111111", "#6b6a66", "#ffffff"
RAMP = ["#1F6F6B", "#569B91", "#93BFB7", "#C5DBD6", "#EDF2F0"]  # poorest first
NODATA, INV = "#e8e6e0", "#D98324"

plt.rcParams.update({"font.family": ["Helvetica Neue", "Helvetica", "Arial"],
                     "text.color": INK})


def rings(geom):
    polys = [geom["coordinates"]] if geom["type"] == "Polygon" else geom["coordinates"]
    for poly in polys:
        yield poly[0]


def money(v):
    if v >= 1e9:
        return f"${v/1e9:.2f} billion"
    if v >= 1e6:
        return f"${v/1e6:.1f} million"
    return f"${v:,.0f}"


def main(argv):
    slug = argv[0] if argv else "ohio-income-health"
    out = ROOT / "posts" / slug / "images"
    d = json.loads((ROOT / "dist" / "map_data.json").read_text())
    T, C, meta = d["tracts"], d["counties"], d["meta"]

    incs = sorted(f["properties"]["inc"] for f in T if f["properties"].get("inc", 0) > 0)
    cuts = [incs[int(q * len(incs))] for q in (0.2, 0.4, 0.6, 0.8)]

    def band(v):
        if not v or v <= 0:
            return -1
        for i, c in enumerate(cuts):
            if v < c:
                return i
        return 4

    tp, tc = [], []
    for f in T:
        b = band(f["properties"].get("inc"))
        for r in rings(f["geometry"]):
            tp.append(Poly(r, closed=True))
            tc.append(NODATA if b < 0 else RAMP[b])
    cp = [Poly(r, closed=True) for f in C for r in rings(f["geometry"])]

    fig = plt.figure(figsize=(W / DPI, H / DPI), dpi=DPI, facecolor=BG)
    ax = fig.add_axes([0.03, 0.04, 0.55, 0.92])
    ax.set_aspect(1 / 0.766)  # cos(40 degrees N)
    ax.add_collection(PatchCollection(tp, facecolor=tc, edgecolor="none", linewidth=0))
    ax.add_collection(PatchCollection(cp, facecolor="none", edgecolor=BORDER, linewidth=0.8))
    vals = [(f["properties"]["cash"], f["properties"]) for f in C]
    vmax = max(v for v, _ in vals)
    RMAX_PT = 58
    pts = sorted([(v, p) for v, p in vals if v > 0], key=lambda x: -x[0])
    ax.scatter([p["c"][0] for _, p in pts], [p["c"][1] for _, p in pts],
               s=[max(4.0, RMAX_PT * (v / vmax) ** 0.5) ** 2 for v, _ in pts],
               facecolor=INV, alpha=0.5, edgecolor=INV, linewidth=1.8, zorder=3)
    ax.set_xlim(-84.9, -80.45)
    ax.set_ylim(38.35, 42.0)
    ax.axis("off")

    x0 = 0.615
    fig.text(x0, 0.865, "Where JobsOhio's grant", fontsize=37, fontweight="bold")
    fig.text(x0, 0.808, "money landed in Ohio", fontsize=37, fontweight="bold")
    fig.text(x0, 0.745, "Circle area shows total grant dollars by county,",
             fontsize=19, color=MUTED)
    fig.text(x0, 0.712, "FY2014 to FY2025", fontsize=19, color=MUTED)

    top = sorted(vals, key=lambda x: -x[0])[:3]
    fig.text(x0, 0.635, "Most money", fontsize=19, color=MUTED)
    for i, (v, p) in enumerate(top):
        fig.text(x0, 0.585 - i * 0.048, f"{p['NAME']}: {money(v)}", fontsize=23)

    ly = 0.37
    fig.text(x0, ly + 0.04, "Median household income by census tract",
             fontsize=19, color=MUTED)
    sw = 0.06
    for i, c in enumerate(RAMP):
        fig.patches.append(Rectangle((x0 + i * (sw + 0.003), ly - 0.03), sw, 0.045,
                                     transform=fig.transFigure, facecolor=c,
                                     edgecolor="#dcdbd6", linewidth=0.6))
    fig.text(x0, ly - 0.072, f"${incs[0]/1000:.0f}k, poorest", fontsize=17, color=MUTED)
    fig.text(x0 + 5 * (sw + 0.003) - 0.003, ly - 0.072, f"${incs[-1]/1000:.0f}k",
             fontsize=17, color=MUTED, ha="right")
    fig.text(x0, ly - 0.112, "Five equal groups of tracts. Darker is poorer.",
             fontsize=17, color=MUTED)

    fig.text(x0, 0.155, f"{money(meta['placed'])} placed in an Ohio county.",
             fontsize=16, color=MUTED)
    fig.text(x0, 0.122, "Source: JobsOhio Form 990, Schedule I.", fontsize=16, color=MUTED)
    fig.text(x0, 0.089, "Income: Census ACS 2020-2024.", fontsize=16, color=MUTED)
    fig.text(0.97, 0.04, "Data 4 The People", fontsize=19, fontweight="bold", ha="right")

    hero = out / f"{slug}-hero-1680x1080.png"
    fig.savefig(hero, dpi=DPI, facecolor=BG)
    plt.close(fig)
    shutil.copyfile(hero, out / f"{slug}-hero-source.png")
    from PIL import Image
    print(f"wrote {hero.relative_to(ROOT)} {Image.open(hero).size}; top: " +
          "; ".join(f"{p['NAME']} {money(v)}" for v, p in top) +
          f"; income {incs[0]:,}-{incs[-1]:,}; placed {meta['placed']:,}")


if __name__ == "__main__":
    main(sys.argv[1:])
