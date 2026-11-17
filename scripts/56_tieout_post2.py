#!/usr/bin/env python3
"""Claude's tie-out for the ohio-income-health post. Writes TIEOUT-ohio-income-health.md.

Every figure on the two GIFs, recomputed from the raw source files rather than
from the built tables the GIF scripts read:

  - tract filter and income: raw ACS 2020-2024 B01003, B26001, B19013 parquet
    files in TractEconHealth/data/raw/acs/2024/
  - the seven measures: raw PLACES 2025 pages in TractEconHealth/data/raw/places/
  - county population: raw ACS county B01003
  - money: data/geo/investment_by_county.csv (tied out in the first post)

Then compares with data/health/oh_tracts_2024.csv, oh_counties_2024.csv and
dist/map_data.json, and checks the three analysis scripts reproduce.

Run with the TractEconHealth venv.
"""
import csv
import glob
import hashlib
import json
import math
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW = Path.home() / "PycharmProjects/TractEconHealth/data/raw"
PY = str(Path.home() / "PycharmProjects/TractEconHealth/.venv/bin/python")
IDS = {"DIABETES": "diabetes", "OBESITY": "obesity", "CSMOKING": "smoking",
       "LPA": "inactivity", "SLEEP": "short_sleep", "FOODINSECU": "food_insecurity",
       "LONELINESS": "loneliness"}
lines, fails = [], 0


def check(label, mine, built, tol=0):
    global fails
    ok = (mine == built) if tol == 0 else abs(float(mine) - float(built)) <= tol
    fails += 0 if ok else 1
    lines.append(f"| {label} | {mine} | {built} | {'match' if ok else '**DIFFERS**'} |")


def acs(table, col, county=False):
    sub = "acs_county" if county else "acs"
    a = pd.read_parquet(RAW / sub / "2024" / f"{table}.parquet")
    a = a[a.geoid.str.startswith("39")].set_index("geoid")
    return pd.to_numeric(a[col], errors="coerce")


# tracts, filters and income from raw ACS
pop = acs("B01003", "B01003_001E")
gq = acs("B26001", "B26001_001E").reindex(pop.index).fillna(0)
inc = acs("B19013", "B19013_001E").reindex(pop.index)
inc = inc.where(inc > 0)
keep = pop[(pop >= 500) & (gq / pop < 0.5)].index

# PLACES raw
parts = []
for f in sorted(glob.glob(str(RAW / "places" / "page_*.csv"))):
    p = pd.read_csv(f, dtype=str)
    parts.append(p[(p.stateabbr == "OH") & p.measureid.isin(IDS)
                   & (p.data_value_type == "Crude prevalence")])
pl = pd.concat(parts)
pl["v"] = pd.to_numeric(pl.data_value)
wide = pl.pivot(index="locationname", columns="measureid", values="v").rename(columns=IDS)
keep = [g for g in keep if g in wide.index]
raw = wide.loc[keep].assign(med_hh_income=inc.reindex(keep))

ext = pd.read_csv(ROOT / "data/health/oh_tracts_2024.csv", dtype={"GEOID": str}).set_index("GEOID")
lines += ["## GIF 1: income and health", "", "| Figure | Recomputed from raw | Built | |", "|---|---|---|---|"]
check("Ohio tracts after filters", len(raw), len(ext))
check("Tracts with income (dots per frame)", int(raw.med_hh_income.notna().sum()),
      int(ext.med_hh_income.notna().sum()))
check("Tracts top-coded at $250,001", int((raw.med_hh_income >= 250001).sum()),
      int((ext.med_hh_income >= 250001).sum()))
both = raw.join(ext, rsuffix="_b", how="inner")
check("Tracts where income differs from extract", int((both.med_hh_income.fillna(-1) != both.med_hh_income_b.fillna(-1)).sum()), 0)
for m in IDS.values():
    check(f"{m}: tracts where value differs", int((both[m].round(1) != both[m + "_b"].round(1)).sum()), 0)
    hi = raw.loc[raw.med_hh_income.notna(), m].max()
    check(f"{m}: highest tract / y-axis top", f"{hi} / {10 * math.ceil(hi / 10)}%",
          f"{ext.loc[ext.med_hh_income.notna(), m].max()} / "
          f"{10 * math.ceil(ext.loc[ext.med_hh_income.notna(), m].max() / 10)}%")
    rr = raw[["med_hh_income", m]].dropna()
    ee = ext[["med_hh_income", m]].dropna()
    check(f"{m}: R2, log income", f"{np.corrcoef(np.log(rr.med_hh_income), rr[m])[0, 1] ** 2:.2f}",
          f"{np.corrcoef(np.log(ee.med_hh_income), ee[m])[0, 1] ** 2:.2f}")
lo, hi = raw.med_hh_income.min(), raw.med_hh_income.max()

# map
lines += ["", "## GIF 2: the map", "", "| Figure | Recomputed | Built | |", "|---|---|---|---|"]
cp = acs("B01003", "B01003_001E", county=True)
names = pd.read_parquet(RAW / "acs_county" / "2024" / "B01003.parquet")
names = names[names.geoid.str.startswith("39")].set_index("geoid").NAME.str.replace(" County, Ohio", "", regex=False)
cpop = {names[g]: int(cp[g]) for g in cp.index}
inv = {r["county"]: int(r["cash"]) for r in csv.DictReader((ROOT / "data/geo/investment_by_county.csv").open())}
md = json.loads((ROOT / "dist/map_data.json").read_text())
built = {f["properties"]["NAME"]: f["properties"] for f in md["counties"]}
check("Counties", len(cpop), len(built))
check("Ohio population, all counties", sum(cpop.values()), sum(p["pop"] for p in built.values()))
check("Dollars placed in a county", sum(inv.get(n, 0) for n in cpop), md["meta"]["placed"])
tot = sorted(((inv.get(n, 0), n) for n in cpop), reverse=True)[:3]
per = sorted(((inv.get(n, 0) / cpop[n], n) for n in cpop), reverse=True)[:3]
for (v, n) in tot:
    check(f"Total, {n}", f"${v/1e6:.1f} million", f"${built[n]['cash']/1e6:.1f} million")
for (v, n) in per:
    check(f"Per person, {n}", f"${v:,.0f}", f"${built[n]['cash']/built[n]['pop']:,.0f}")
tinc = sorted(p["properties"]["inc"] for p in md["tracts"] if p["properties"].get("inc", 0) > 0)
check("Legend low end (lowest tract income)", f"${lo/1000:.0f}k", f"${tinc[0]/1000:.0f}k")
check("Legend high end", f"${hi/1000:.0f}k", f"${tinc[-1]/1000:.0f}k")
check("Tracts coloured on the map", int(raw.med_hh_income.notna().sum()), len(tinc))

# analyses reproduce
lines += ["", "## Analysis scripts reproduce", "", "| Script | Output unchanged on re-run | | |", "|---|---|---|---|"]
for script, out in [("53_places_input_check.py", "places_input_check.csv"),
                    ("54_county_counted_check.py", "county_counted_check.csv"),
                    ("55_places_input_shapley.py", "places_input_shapley.csv")]:
    f = ROOT / "data/health/checks" / out
    before = hashlib.sha256(f.read_bytes()).hexdigest()
    subprocess.run([PY, str(ROOT / "scripts" / script)], check=True, capture_output=True)
    check(script, before[:12], hashlib.sha256(f.read_bytes()).hexdigest()[:12])

head = ["# Tie-out: ohio-income-health", "",
        "Written by `scripts/56_tieout_post2.py`. Recomputed from the raw ACS and PLACES files in "
        "TractEconHealth, not from the tables the GIF scripts read. The first post's tie-out is `TIEOUT.md`.", "",
        f"**{fails} differences.**", ""]
INDEPENDENT = """
## Independent tie-out, 2026-11-17

A fresh agent that had not seen the work pulled ACS 2020-2024 from the Census API, PLACES 2025 tract
(cwsq-ngmh) and county (swc5-untb) data from data.cdc.gov, and the CHR 2025 analytic file and March 2026
supplement, and recomputed everything with its own code. It used only `data/geo/investment_by_county.csv`
from the project.

- **Every number on the nine frames matched**: 3,125 tracts after filters, 3,115 with income, 3 at the top
  code, all seven y-axis tops, $1,257,313,860 placed, the top three counties by total and per person, and the
  legend endpoints.
- **Its R-squared results matched the method**: income alone 50% to 69%; CDC-style inputs with county effects
  89% to 96%; income adds at most 0.2 points.
- **County Spearman results matched** to two decimals for the files the method names.
- **Fixed from its review:** the food insecurity subtitle said "ran short of food or worried about it";
  CDC's measure has nothing about worry and now reads "food ran out in the past year before they had money to
  buy more". Diabetes now says "doctor or other health professional". The footer now says incomes of $250k
  or more are shown at $250k.
- **Not checked by it:** circle sizes and tract shading (by eye only), the investment-by-county file (given),
  the Shapley split, frame timing.
"""
(ROOT / "TIEOUT-ohio-income-health.md").write_text("\n".join(head + lines) + "\n" + INDEPENDENT)
print("\n".join(head + lines))
