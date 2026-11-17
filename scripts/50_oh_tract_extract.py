#!/usr/bin/env python3
"""Copy the Ohio tracts out of TractEconHealth for the ohio-income-health post.

Source: ~/PycharmProjects/TractEconHealth/data/processed/tracts.parquet, built
by that project's 10_build.py. Income is ACS 2020-2024 5-year median household
income (B19013, 2024 dollars, top-coded at $250,001). The seven health measures
are CDC PLACES 2025 tract estimates, percent of adults, model-based.

That project's filters already apply: tracts under 500 people or with group
quarters at 50% or more of the population are dropped.

Run with the TractEconHealth venv, which has pandas and pyarrow:
  ~/PycharmProjects/TractEconHealth/.venv/bin/python scripts/50_oh_tract_extract.py
Writes data/health/oh_tracts_2024.csv, and data/health/oh_counties_2024.csv with
the ACS 2020-2024 population of all 88 counties (B01003, no filters), which
the map divides by for dollars per person.
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
SRC = Path.home() / "PycharmProjects/TractEconHealth/data/processed/tracts.parquet"
MEASURES = ["fair_poor_health", "diabetes", "obesity", "smoking", "inactivity",
            "short_sleep", "food_insecurity", "loneliness"]

t = pd.read_parquet(SRC)
oh = t[t.stateabbr == "OH"].copy()
oh.index.name = "GEOID"
out = oh[["pop", "countyname", "med_hh_income"] + MEASURES].reset_index()
out["GEOID"] = out["GEOID"].astype(str)
dest = ROOT / "data" / "health" / "oh_tracts_2024.csv"
out.to_csv(dest, index=False)
print(f"{len(out)} Ohio tracts, {out.med_hh_income.notna().sum()} with income")
for m in MEASURES:
    n = (out.med_hh_income.notna() & out[m].notna()).sum()
    print(f"  {m:16s} {n} tracts with income and the measure")
print(f"  top-coded at $250,001: {(out.med_hh_income >= 250001).sum()}")
print(f"wrote {dest.relative_to(ROOT)}")

c = pd.read_parquet(SRC.parent / "counties.parquet")
c = c[c.index.astype(str).str.startswith("39")].copy()
c["county"] = c["name"].str.replace(" County, Ohio", "", regex=False)
cdest = ROOT / "data" / "health" / "oh_counties_2024.csv"
c.reset_index()[["geoid", "county", "pop"]].astype({"pop": int}).to_csv(cdest, index=False)
print(f"{len(c)} Ohio counties, population {int(c['pop'].sum()):,}; wrote {cdest.relative_to(ROOT)}")
