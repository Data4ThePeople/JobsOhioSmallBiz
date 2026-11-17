#!/usr/bin/env python3
"""Check 1: how much of each PLACES tract estimate do the model's own inputs explain?

CDC does not survey each tract. It fits a model to individual survey answers
using age, sex, race and ethnicity, education, and county poverty (below 150%
of the poverty line), with tract poverty used in the prediction step, then
applies it to each tract's population. So a tract value is what the model
expects for a tract with that makeup.

This rebuilds those inputs for every Ohio tract from the ACS 2020-2024 5-year
release and asks, for each of the seven measures:

  A  how much of the tract-to-tract variation income alone explains (R2)
  B  how much the model's inputs explain, without income (with county
     effects, as CDC's model has, and a curve in tract poverty)
  C  how much income adds on top of the inputs (R2 of B plus income, minus B)
  D  the inputs without tract or county poverty, so B minus D is what the
     poverty input adds

If B is close to 1, nearly all of the variation between tracts comes from the
inputs, and the tightness of the scatter is mostly the model. C says how much
of the income pattern is left once the inputs are known.

This is an approximation of CDC's model, not a copy: CDC uses 2020 census
block counts, a multilevel logistic model with interactions, and does not say
which tract poverty table it uses. A plain linear fit on tract shares will
explain somewhat less than the real model does, so B is a floor.

Inputs, as shares of the relevant tract population:
  B01001  sex; adults 18-24, 25-34, 35-44, 45-54, 55-64, 65-74, 75+ (of 18+)
  B03002  Hispanic; non-Hispanic Black, Asian, other (white is the base)
  B15003  25+: below high school, high school, some college (BA+ is the base)
  C17002  below 150% of poverty, tract and county

Run with the TractEconHealth venv:
  ~/PycharmProjects/TractEconHealth/.venv/bin/python scripts/53_places_input_check.py
Writes data/health/checks/places_input_check.csv and caches the ACS pulls
in data/health/checks/acs_inputs_oh_2024.csv.
"""
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import requests

warnings.filterwarnings("ignore")
sys.path.insert(0, str(Path.home() / ".claude/d4tp-process"))
from d4tp_env import get_key, load_env  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data/health/checks"
CACHE = OUT / "acs_inputs_oh_2024.csv"
API = "https://api.census.gov/data/2024/acs/acs5"
MEASURES = ["diabetes", "obesity", "smoking", "inactivity",
            "short_sleep", "food_insecurity", "loneliness"]


def pull(table, geo):
    load_env(ROOT)
    r = requests.get(API, params={"get": f"group({table})", "for": geo,
                                  "in": "state:39", "key": get_key("CENSUS_API_KEY")},
                     timeout=120)
    r.raise_for_status()
    rows = r.json()
    df = pd.DataFrame(rows[1:], columns=rows[0])
    keep = [c for c in df.columns if c.endswith("E") and c.startswith(table)]
    for c in keep:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    return df


def v(df, table, *nums):
    return sum(df[f"{table}_{n:03d}E"] for n in nums)


def build():
    """One pull per table, each joined on GEOID. The API does not promise the
    same row order across tables, so nothing is aligned by position."""
    geo = "tract:*"
    a = pull("B01001", geo)
    a["GEOID"] = a.state + a.county + a.tract
    out = pd.DataFrame({"GEOID": a.GEOID, "county": a.state + a.county})
    out["male"] = (v(a, "B01001", 2) / v(a, "B01001", 1)).values
    # adults by band, men (7-25) and women (31-49)
    bands = {"a18_24": (7, 8, 9, 10), "a25_34": (11, 12), "a35_44": (13, 14),
             "a45_54": (15, 16), "a55_64": (17, 18, 19), "a65_74": (20, 21, 22),
             "a75p": (23, 24, 25)}
    cols = {k: v(a, "B01001", *ns) + v(a, "B01001", *[n + 24 for n in ns])
            for k, ns in bands.items()}
    adults = sum(cols.values())
    for k in bands:
        out[k] = (cols[k] / adults).values

    def add(table, fn):
        t = pull(table, geo)
        t["GEOID"] = t.state + t.county + t.tract
        part = fn(t)
        part["GEOID"] = t["GEOID"].values
        return part

    race = add("B03002", lambda r: pd.DataFrame({
        "hisp": (v(r, "B03002", 12) / v(r, "B03002", 1)).values,
        "nh_black": (v(r, "B03002", 4) / v(r, "B03002", 1)).values,
        "nh_asian": (v(r, "B03002", 6) / v(r, "B03002", 1)).values,
        "nh_other": (v(r, "B03002", 5, 7, 8, 9) / v(r, "B03002", 1)).values}))
    educ = add("B15003", lambda e: pd.DataFrame({
        "ed_lt_hs": (v(e, "B15003", *range(2, 17)) / v(e, "B15003", 1)).values,
        "ed_hs": (v(e, "B15003", 17, 18) / v(e, "B15003", 1)).values,
        "ed_some": (v(e, "B15003", 19, 20, 21) / v(e, "B15003", 1)).values}))
    pov = add("C17002", lambda p: pd.DataFrame({
        "pov150": (v(p, "C17002", 2, 3, 4, 5) / v(p, "C17002", 1)).values}))
    for part in (race, educ, pov):
        out = out.merge(part, on="GEOID", how="left")

    pc = pull("C17002", "county:*")
    pc["county"] = pc.state + pc.county
    pc["cpov150"] = v(pc, "C17002", 2, 3, 4, 5) / v(pc, "C17002", 1)
    out = out.merge(pc[["county", "cpov150"]], on="county", how="left")
    out.to_csv(CACHE, index=False)
    return out


def r2(X, y):
    X = np.column_stack([np.ones(len(y)), X])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    return 1 - resid.var() / y.var()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    inp = pd.read_csv(CACHE, dtype={"GEOID": str, "county": str}) if CACHE.exists() else build()
    h = pd.read_csv(ROOT / "data/health/oh_tracts_2024.csv", dtype={"GEOID": str})
    d = h.merge(inp, on="GEOID", how="inner").dropna()
    X_cols = ["male", "a18_24", "a25_34", "a35_44", "a45_54", "a55_64", "a65_74",
              "hisp", "nh_black", "nh_asian", "nh_other",
              "ed_lt_hs", "ed_hs", "ed_some", "pov150", "cpov150"]
    inc = np.log(d.med_hh_income.values)
    # county effects, as in CDC's model (88 counties, one left out as the base)
    fe = pd.get_dummies(d.county, drop_first=True).values.astype(float)
    print("check: corr(log income, tract share below 150% of poverty) = "
          f"{np.corrcoef(inc, d.pov150)[0, 1]:.2f}")
    rows = []
    for m in MEASURES:
        y = d[m].values
        a_ = r2(inc[:, None], y)
        Xb = np.column_stack([d[X_cols].values, d.pov150 ** 2, np.sqrt(d.pov150), fe])
        b_ = r2(Xb, y)
        c_ = r2(np.column_stack([Xb, inc]), y) - b_
        nopov = [c for c in X_cols if c not in ("pov150", "cpov150")]
        d_ = r2(np.column_stack([d[nopov].values, fe]), y)
        rows.append({"measure": m, "tracts": len(d),
                     "A_income_only": round(a_, 3),
                     "B_model_inputs": round(b_, 3),
                     "C_income_added": round(c_, 3),
                     "D_inputs_without_poverty": round(d_, 3)})
    res = pd.DataFrame(rows)
    res.to_csv(OUT / "places_input_check.csv", index=False)
    print(f"{len(d)} Ohio tracts with income, all seven measures and every input\n")
    print(res.to_string(index=False))


if __name__ == "__main__":
    main()
