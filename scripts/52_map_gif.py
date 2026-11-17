#!/usr/bin/env python3
"""GIF: the Ohio map, JobsOhio money by county over income by tract.

Two frames, total dollars then dollars per person, each held four seconds.
Both are real values from dist/map_data.json (scripts/45_build_map.py), so
nothing here is interpolated and the GIF cannot drift from the map page.

  tracts    median household income, ACS 2020-2024 5-year, in five equal
            groups of tracts (quintiles), dark = poorest, the same bands and
            ramp as dist/map.html.
  circles   JobsOhio grant money that can be placed in the county, area
            proportional to the value. Total dollars, or dollars divided by
            the county's ACS 2020-2024 population.

One colour of circle only. The map page colours counties that include a
confirmed failure; that needs the post's definition of failure to read, so
the GIF leaves it out.

Usage: 52_map_gif.py [slug]
"""
import io
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as Poly, Rectangle
from matplotlib.collections import PatchCollection
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
W, H, DPI = 1200, 675, 100
HOLD_MS = 4000
BG, INK, MUTED, BORDER = "#fcfcfb", "#111111", "#6b6a66", "#ffffff"
RAMP = ["#1F6F6B", "#569B91", "#93BFB7", "#C5DBD6", "#EDF2F0"]  # poorest first
NODATA, INV = "#e8e6e0", "#D98324"
TOTAL_FRAMES = (("total", "Total dollars"), ("per", "Dollars per person"))

plt.rcParams.update({"font.family": ["Helvetica Neue", "Helvetica", "Arial"],
                     "text.color": INK})


def rings(geom):
    polys = [geom["coordinates"]] if geom["type"] == "Polygon" else geom["coordinates"]
    for poly in polys:
        yield poly[0]  # outer ring; Ohio tracts have no meaningful holes at this scale


def money(v):
    if v >= 1e9:
        return f"${v/1e9:.2f} billion"
    if v >= 1e6:
        return f"${v/1e6:.1f} million"
    return f"${v:,.0f}"


def main(argv):
    slug = argv[0] if argv else "ohio-income-health"
    out = ROOT / "posts" / slug / "social"
    out.mkdir(parents=True, exist_ok=True)
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

    tract_patches, tract_cols = [], []
    for f in T:
        b = band(f["properties"].get("inc"))
        for r in rings(f["geometry"]):
            tract_patches.append(Poly(r, closed=True))
            tract_cols.append(NODATA if b < 0 else RAMP[b])
    cty_patches = [Poly(r, closed=True) for f in C for r in rings(f["geometry"])]

    def val(p, mode):
        return p["cash"] if mode == "total" else (p["cash"] / p["pop"] if p["pop"] else 0)

    frames = []
    for mode, label in TOTAL_FRAMES:
        fig = plt.figure(figsize=(W / DPI, H / DPI), dpi=DPI, facecolor=BG)
        ax = fig.add_axes([0.015, 0.03, 0.56, 0.94])
        ax.set_aspect(1 / 0.766)  # cos(40 degrees N), so Ohio is not stretched
        ax.add_collection(PatchCollection(tract_patches, facecolor=tract_cols,
                                          edgecolor="none", linewidth=0))
        ax.add_collection(PatchCollection(cty_patches, facecolor="none",
                                          edgecolor=BORDER, linewidth=0.6))
        vals = [(val(f["properties"], mode), f["properties"]) for f in C]
        vmax = max(v for v, _ in vals)
        # Marker sizes are in points, so circles stay round whatever the map's
        # aspect. Area (s) is proportional to the value; the floor keeps the
        # smallest counties visible.
        RMAX_PT = 40
        pts = sorted([(v, p) for v, p in vals if v > 0], key=lambda x: -x[0])
        ax.scatter([p["c"][0] for _, p in pts], [p["c"][1] for _, p in pts],
                   s=[max(3.0, RMAX_PT * (v / vmax) ** 0.5) ** 2 for v, _ in pts],
                   facecolor=INV, alpha=0.5, edgecolor=INV, linewidth=1.4, zorder=3)
        ax.set_xlim(-84.9, -80.45)
        ax.set_ylim(38.35, 42.0)
        ax.axis("off")

        top = sorted(vals, key=lambda x: -x[0])[:3]
        x0 = 0.6
        fig.text(x0, 0.88, "Where JobsOhio's grant", fontsize=25, fontweight="bold")
        fig.text(x0, 0.825, "money went in Ohio", fontsize=25, fontweight="bold")
        fig.text(x0, 0.765, "Circle area shows", fontsize=14, color=MUTED)
        # the two-state switch, the active one filled
        bx = x0
        for m, lab in TOTAL_FRAMES:
            on = m == mode
            t = fig.text(bx + 0.008, 0.712, lab, fontsize=15, fontweight="bold",
                         color="#ffffff" if on else MUTED,
                         bbox=dict(boxstyle="round,pad=0.45", fc=INV if on else "#ffffff",
                                   ec=INV if on else "#dcdbd6"))
            bx += 0.145 if m == "total" else 0
        fig.text(x0, 0.625, "Most money" if mode == "total" else "Most per person",
                 fontsize=14, color=MUTED)
        for i, (v, p) in enumerate(top):
            shown = money(v) if mode == "total" else f"${v:,.0f} per person"
            fig.text(x0, 0.58 - i * 0.045, f"{p['NAME']}: {shown}", fontsize=15.5)

        # income legend, poorest (dark) to richest (light)
        ly = 0.36
        fig.text(x0, ly + 0.035, "Median household income by census tract",
                 fontsize=14, color=MUTED)
        for i, c in enumerate(RAMP):
            fig.patches.append(Rectangle((x0 + i * 0.062, ly - 0.03), 0.06, 0.04,
                                         transform=fig.transFigure, facecolor=c,
                                         edgecolor="#dcdbd6", linewidth=0.5))
        fig.text(x0, ly - 0.07, f"${incs[0]/1000:.0f}k, poorest", fontsize=12.5, color=MUTED)
        fig.text(x0 + 5 * 0.062, ly - 0.07, f"${incs[-1]/1000:.0f}k", fontsize=12.5,
                 color=MUTED, ha="right")
        fig.text(x0, ly - 0.115, "Five equal groups of tracts. Darker is poorer.",
                 fontsize=12.5, color=MUTED)

        fig.text(x0, 0.185,
                 f"{money(meta['placed'])} placed in an Ohio county, FY2014 to FY2025.",
                 fontsize=11.5, color=MUTED)
        fig.text(x0, 0.145,
                 "Source: JobsOhio Form 990, Schedule I.",
                 fontsize=11.5, color=MUTED)
        fig.text(x0, 0.105, "Income and population: Census ACS 2020-2024.",
                 fontsize=11.5, color=MUTED)
        fig.text(0.975, 0.03, "Data 4 The People", fontsize=12.5,
                 fontweight="bold", ha="right")
        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=DPI, facecolor=BG)
        plt.close(fig)
        buf.seek(0)
        im = Image.open(buf).convert("RGB")
        im.save(out / f"jobsohio-map-{mode}.png")
        frames.append(im.convert("P", palette=Image.ADAPTIVE, colors=64))
        print(f"  {mode:5s} top: " + "; ".join(
            f"{p['NAME']} {v:,.2f}" for v, p in top))

    gif = out / "jobsohio-map-total-vs-per-person.gif"
    frames[0].save(gif, save_all=True, append_images=frames[1:],
                   duration=HOLD_MS, loop=0, optimize=True, disposal=2)
    print(f"wrote {gif.relative_to(ROOT)}  {W}x{H}  {len(frames)} frames  "
          f"{len(frames)*HOLD_MS/1000:.0f}s  {gif.stat().st_size/1024:.0f} KB")
    print(f"  placed ${meta['placed']:,}; income cuts {cuts}")


if __name__ == "__main__":
    main(sys.argv[1:])
