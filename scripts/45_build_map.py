#!/usr/bin/env python3
"""Build dist/map_data.json: Ohio tracts with income and health, counties with investment.

Two layers at two resolutions, and the mismatch is deliberate rather than
sloppy, so the page says so.

  tracts    3,162 census tracts, each with median household income (ACS 2020-2024
            five-year, B19013) and the share of adults reporting fair or poor
            health (CDC PLACES, GHLTH). This is the real resolution of both
            measures and it is where the correlation lives.
  counties  the 88, each with the JobsOhio money that can be placed in it and
            how much of that went to a company later confirmed to have failed.
            County is the finest resolution the investment can honestly claim:
            the payee address on Schedule I is where the cheque was posted,
            not where the project is, and 28.5% of the dollars went out of
            state. `43_investment_by_county.py` has the full reasoning.

A bubble sits at the county's centre of population rather than its geometric
centre, because the geometric centre of a county like Cuyahoga is a lake.

Geometry is simplified to about 50 metres and coordinates rounded to four
decimal places, which is roughly 11 metres. Both are far finer than anything
the data supports and keep the payload near 1.5 MB.

Usage: 45_build_map.py
"""
import csv, json, sys, warnings
from pathlib import Path
warnings.filterwarnings("ignore")
import geopandas as gpd

ROOT = Path(__file__).resolve().parent.parent
GEO = ROOT / "data" / "geo"
OUT = ROOT / "dist" / "map_data.json"
TOL, PLACES = 0.0005, 4


def rnd(c):
    if isinstance(c[0], (list, tuple)):
        return [rnd(x) for x in c]
    return [round(c[0], PLACES), round(c[1], PLACES)]


def shrink(gdf, keep):
    gdf = gdf.copy()
    gdf["geometry"] = gdf.geometry.simplify(TOL, preserve_topology=True)
    gj = json.loads(gdf[keep + ["geometry"]].to_json())
    for f in gj["features"]:
        f["geometry"]["coordinates"] = rnd(f["geometry"]["coordinates"])
        f.pop("id", None)
    return gj["features"]


def main():
    # Income: ACS 2020-2024 5-year, the same release as the TractEconHealth
    # scatter, so a tract shows one income across the post. Fair-or-poor
    # health (used only by this page's own scatter, not the GIFs) still comes
    # from the earlier file, joined on GEOID.
    hl_old = {r["geoid"]: r["pct_fair_or_poor_health"] for r in
              csv.DictReader((ROOT / "data" / "health" / "tract_income_health_oh.csv").open())}
    th = {}
    for r in csv.DictReader((ROOT / "data" / "health" / "oh_tracts_2024.csv").open()):
        if r["med_hh_income"]:
            th[r["GEOID"]] = {"median_household_income": float(r["med_hh_income"]),
                              "pct_fair_or_poor_health": hl_old.get(r["GEOID"]) or None,
                              "population": r["pop"],
                              "county": r["countyname"]}
    inv = {r["county"]: r for r in
           csv.DictReader((GEO / "investment_by_county.csv").open())}

    tr = gpd.read_file(GEO / "cb_2023_39_tract_500k.zip").to_crs(4326)
    feats = shrink(tr, ["GEOID"])
    kept = 0
    for f in feats:
        d = th.get(f["properties"]["GEOID"])
        if d:
            kept += 1
            f["properties"]["inc"] = int(float(d["median_household_income"]))
            if d["pct_fair_or_poor_health"]:
                f["properties"]["hl"] = float(d["pct_fair_or_poor_health"])
            f["properties"]["pop"] = int(float(d["population"] or 0))
    print(f"{len(feats)} tracts, {kept} with income, "
          f"{sum(1 for f in feats if 'hl' in f['properties'])} with health")

    # County population for dollars per person: ACS 2020-2024 county totals,
    # all residents, so tracts dropped by the tract filters still count.
    cpops = {r["county"]: int(r["pop"]) for r in
             csv.DictReader((ROOT / "data" / "health" / "oh_counties_2024.csv").open())}

    cty = gpd.read_file(GEO / "cb_2023_us_county_20m.zip").to_crs(4326)
    cty = cty[cty.STATEFP == "39"]
    cfeats = shrink(cty, ["NAME"])
    # centre of population, which the Census publishes, so a bubble for a
    # county like Cuyahoga does not land in Lake Erie
    cpop = {}
    f = GEO / "CenPop2020_Mean_CO.txt"
    if f.exists():
        # utf-8-sig: the Census ships this one with a byte order mark, which
        # turns the first column name into "\ufeffSTATEFP"
        for r in csv.DictReader(f.open(encoding="utf-8-sig")):
            if r["STATEFP"] == "39":
                cpop[r["COUNAME"].strip()] = (float(r["LONGITUDE"]), float(r["LATITUDE"]))
    missing = 0
    for f2 in cfeats:
        n = f2["properties"]["NAME"]
        d = inv.get(n)
        f2["properties"]["cash"] = int(d["cash"]) if d else 0
        f2["properties"]["n"] = int(d["recipients"]) if d else 0
        f2["properties"]["fcash"] = int(d["failed_cash"]) if d else 0
        f2["properties"]["fn"] = int(d["failed_recipients"]) if d else 0
        # population, so the page can divide. Summed from the county's own
        # tracts rather than taken from elsewhere, so it matches the income
        # and health layer exactly.
        f2["properties"]["pop"] = cpops.get(n, 0)
        # company names are deliberately not shipped. The map is about where
        # the money went, naming companies on a county bubble invites reading
        # the county's failure total as belonging to whichever name is first,
        # and the full tool is where a reader should meet a company.
        if n in cpop:
            f2["properties"]["c"] = [round(cpop[n][0], 4), round(cpop[n][1], 4)]
        else:
            missing += 1
            g = cty[cty.NAME == n].geometry.representative_point().iloc[0]
            f2["properties"]["c"] = [round(g.x, 4), round(g.y, 4)]
    print(f"{len(cfeats)} counties; {len(cfeats)-missing} placed on a centre of "
          f"population, {missing} on a representative point")

    # Does the money go where the need is? Counties ranked poorest to richest
    # by the median of their tracts, then dollars per head in each fifth. This
    # is the question the map exists to ask, so it ships as a figure rather
    # than left for the reader to eyeball from circle sizes.
    import statistics
    from collections import defaultdict as dd
    byc = dd(list)
    for r in th.values():
        byc[r["county"].replace(" County", "")].append(
            (int(float(r["median_household_income"])), int(float(r["population"] or 0)),
             float(r["pct_fair_or_poor_health"]) if r["pct_fair_or_poor_health"] else None))
    ranked = []
    for name, v in byc.items():
        pop = sum(x[1] for x in v)
        if not pop:
            continue
        d = inv.get(name)
        ranked.append({"county": name, "pop": pop,
                       "inc": statistics.median([x[0] for x in v]),
                       "hl": (sum(x[2] * x[1] for x in v if x[2] is not None)
                              / sum(x[1] for x in v if x[2] is not None)),
                       "cash": int(d["cash"]) if d else 0})
    ranked.sort(key=lambda r: r["inc"])
    n5, step = len(ranked), len(ranked) // 5
    quint = []
    for i in range(5):
        ch = ranked[i * step:(i + 1) * step if i < 4 else n5]
        pop = sum(r["pop"] for r in ch)
        cash = sum(r["cash"] for r in ch)
        quint.append({"counties": len(ch), "pop": pop, "cash": cash,
                      "per_capita": round(cash / pop, 2),
                      "health": round(sum(r["hl"] * r["pop"] for r in ch) / pop, 1),
                      "median_income": round(statistics.median([r["inc"] for r in ch]))})
    print("\n  dollars per head by county income quintile, poorest first:")
    for i, q in enumerate(quint):
        print(f"    Q{i+1}  ${q['per_capita']:>7.2f}   {q['health']:>4.1f}% fair or poor health")

    placed = sum(f["properties"]["cash"] for f in cfeats)
    out = {"tracts": feats, "counties": cfeats,
           "meta": {"placed": placed,
                    "counties_with_money": sum(1 for f in cfeats if f["properties"]["cash"]),
                    "counties_with_failure": sum(1 for f in cfeats if f["properties"]["fn"]),
                    "tracts_with_data": kept, "quintiles": quint}}
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(out, separators=(",", ":")))
    print(f"\nplaced ${placed:,} across {out['meta']['counties_with_money']} counties, "
          f"{out['meta']['counties_with_failure']} with a confirmed failure")
    print(f"wrote {OUT.relative_to(ROOT)}  {OUT.stat().st_size/1024/1024:.2f} MB")


if __name__ == "__main__":
    main()
