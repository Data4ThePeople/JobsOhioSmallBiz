#!/usr/bin/env python3
"""Check 2: does the income pattern show up in Ohio data that no model touched?

The PLACES tract estimates are predictions (scripts/53_places_input_check.py),
so they cannot test whether poorer places really are less healthy. Deaths can:
they are counted from death certificates, not modelled. This ranks Ohio's 88
counties by median household income and asks whether counted death measures
move with income the same way the PLACES estimates do.

  counted   County Health Rankings 2025 (analytic file): premature death
            (years of life lost before 75, per 100,000), premature
            age-adjusted mortality (deaths before 75 per 100,000),
            life expectancy. Drug overdose and suicide rates come
            from the March 2026 supplement, via TractEconHealth's county table.
  modelled  CDC PLACES 2025 county estimates for the seven measures in the GIF,
            from the same table.
  income    ACS 2020-2024 5-year county median household income.

Spearman rank correlation, because 88 counties is a small set and a few big
ones should not drive the result. This tests direction and rough strength, not
the tightness of the tract scatter, and counties average over very different
tracts, so it is a coarse check by design.

Run with the TractEconHealth venv. Writes data/health/checks/county_counted_check.csv.
"""
from pathlib import Path

import pandas as pd
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parent.parent
TEH = Path.home() / "PycharmProjects/TractEconHealth"

c = pd.read_parquet(TEH / "data/processed/counties.parquet")
c = c[c.index.astype(str).str.startswith("39")].copy()

chr_ = pd.read_csv(TEH / "data/raw/chr/analytic_data2025_v3.csv", dtype=str,
                   low_memory=False).iloc[1:]  # row 1 holds the variable codes
chr_ = chr_[(chr_["State Abbreviation"] == "OH") & (chr_["County FIPS Code"] != "000")]
chr_ = chr_.set_index("5-digit FIPS Code")
for col, name in [("Premature Death raw value", "premature_death_ypll"),
                  ("Premature Age-Adjusted Mortality raw value", "premature_mortality"),
                  ("Life Expectancy raw value", "life_expectancy_2025")]:
    c[name] = pd.to_numeric(chr_[col], errors="coerce").reindex(c.index.astype(str))

ROWS = [("counted", "premature_death_ypll", "Premature death, years lost per 100,000"),
        ("counted", "premature_mortality", "Deaths before 75 per 100,000, age-adjusted"),
        ("counted", "life_expectancy_2025", "Life expectancy"),
        ("counted", "overdose_rate", "Drug overdose deaths per 100,000"),
        ("counted", "suicide_rate", "Suicides per 100,000"),
        ("modelled", "diabetes", "Diabetes (PLACES)"),
        ("modelled", "obesity", "Obesity (PLACES)"),
        ("modelled", "smoking", "Smoking (PLACES)"),
        ("modelled", "inactivity", "No leisure-time physical activity (PLACES)"),
        ("modelled", "short_sleep", "Short sleep (PLACES)"),
        ("modelled", "food_insecurity", "Food insecurity (PLACES)"),
        ("modelled", "loneliness", "Loneliness (PLACES)")]

out = []
for kind, col, label in ROWS:
    s = c[["med_hh_income", col]].dropna()
    rho, p = spearmanr(s.med_hh_income, s[col])
    out.append({"kind": kind, "measure": label, "counties": len(s),
                "spearman_with_income": round(rho, 2), "p_value": round(p, 4)})
res = pd.DataFrame(out)
dest = ROOT / "data/health/checks/county_counted_check.csv"
res.to_csv(dest, index=False)
print(res.to_string(index=False))
print(f"\nwrote {dest.relative_to(ROOT)}")
