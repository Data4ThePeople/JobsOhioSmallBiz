#!/usr/bin/env python3
"""Map every Ohio place to its county, by point in polygon.

`43_investment_by_county.py` falls back to the payee's city when JobsOhio's own
project records do not say where a project was. That needs a city-to-county
table for Ohio, and the obvious one to hand was the WARN register, which writes
each notice as "Canton/Stark". It covers only the 250 towns that have had a
mass layoff since 2020, which left 61 Ohio towns and $20,180,560 unplaceable.

This builds the full table instead: the Census places gazetteer publishes a
centre point for all 1,265 Ohio places, and the county that point falls inside
is the county. 1,243 resolve; the rest are places whose centre lands outside
the generalised county boundaries, and they fall through to the WARN table.

Writes data/geo/place_county_oh.csv.

Usage: 44_place_county.py
"""
import csv, re, sys, warnings
from pathlib import Path
warnings.filterwarnings("ignore")
import geopandas as gpd
from shapely.geometry import Point

ROOT = Path(__file__).resolve().parent.parent
GAZ = ROOT / "data" / "geo" / "gaz_place_oh_2023.txt"
CTY = ROOT / "data" / "geo" / "cb_2023_us_county_20m.zip"
OUT = ROOT / "data" / "geo" / "place_county_oh.csv"


def main():
    if not GAZ.exists():
        sys.exit(f"missing {GAZ}; fetch 2023_gaz_place_39.txt from the Census gazetteer")
    cty = gpd.read_file(CTY)
    cty = cty[cty.STATEFP == "39"][["NAME", "geometry"]].to_crs(4326)
    pts, names = [], []
    for r in csv.DictReader(GAZ.open(encoding="latin-1"), delimiter="\t"):
        r = {k.strip(): (v.strip() if isinstance(v, str) else v) for k, v in r.items()}
        try:
            pts.append(Point(float(r["INTPTLONG"]), float(r["INTPTLAT"])))
        except (ValueError, TypeError, KeyError):
            continue
        names.append(re.sub(r"\s+(village|city|town|CDP)$", "", r["NAME"], flags=re.I).lower())
    g = gpd.GeoDataFrame({"place": names}, geometry=pts, crs=4326)
    j = gpd.sjoin(g, cty, how="left", predicate="within")
    out = {}
    for place, county in zip(j["place"], j["NAME"]):
        if isinstance(county, str):
            out.setdefault(place, county)
    with OUT.open("w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["place", "county"])
        for k in sorted(out):
            w.writerow([k, out[k]])
    print(f"{len(pts)} places, {len(out)} resolved to a county")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
