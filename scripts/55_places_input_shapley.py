#!/usr/bin/env python3
"""Which of CDC's PLACES inputs drives each tract estimate most?

Uses the same Ohio tract inputs as 53_places_input_check.py, in five groups:

  age_sex     share male; adult age bands
  race_eth    Hispanic; non-Hispanic Black, Asian, other
  education   adults 25+: no diploma, high school, some college
  poverty     tract share below 150% of poverty (with a curve), county share
  county      one adjustment per county

The groups overlap (education and poverty move together, for example), so
"how much does each explain" has no single answer. This uses the Shapley
split: fit the model on every one of the 32 combinations of groups, and give
each group its average gain in R2 when it is added, across all orders. The
five shares add up to the full model's R2. Also reported: each group alone,
and what is lost when that group alone is dropped (its unique part).

Run with the TractEconHealth venv. Writes data/health/checks/places_input_shapley.csv.
"""
from itertools import combinations
from math import factorial
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
MEASURES = ["diabetes", "obesity", "smoking", "inactivity",
            "short_sleep", "food_insecurity", "loneliness"]

inp = pd.read_csv(ROOT / "data/health/checks/acs_inputs_oh_2024.csv",
                  dtype={"GEOID": str, "county": str})
h = pd.read_csv(ROOT / "data/health/oh_tracts_2024.csv", dtype={"GEOID": str})
d = h.merge(inp, on="GEOID").dropna()

G = {
    "age_sex": d[["male", "a18_24", "a25_34", "a35_44", "a45_54", "a55_64", "a65_74"]].values,
    "race_eth": d[["hisp", "nh_black", "nh_asian", "nh_other"]].values,
    "education": d[["ed_lt_hs", "ed_hs", "ed_some"]].values,
    "poverty": np.column_stack([d.pov150, d.pov150 ** 2, np.sqrt(d.pov150), d.cpov150]),
    "county": pd.get_dummies(d.county, drop_first=True).values.astype(float),
}
names = list(G)
n = len(names)


def r2(groups, y):
    if not groups:
        return 0.0
    X = np.column_stack([np.ones(len(y))] + [G[g] for g in groups])
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    return 1 - (y - X @ b).var() / y.var()


rows = []
for m in MEASURES:
    y = d[m].values
    cache = {frozenset(s): r2(list(s), y)
             for k in range(n + 1) for s in combinations(names, k)}
    full = cache[frozenset(names)]
    for g in names:
        others = [x for x in names if x != g]
        sh = 0.0
        for k in range(n):
            w = factorial(k) * factorial(n - k - 1) / factorial(n)
            for s in combinations(others, k):
                sh += w * (cache[frozenset(s) | {g}] - cache[frozenset(s)])
        rows.append({"measure": m, "group": g, "full_r2": round(full, 3),
                     "shapley": round(sh, 3),
                     "share_of_explained": round(sh / full, 3),
                     "alone": round(cache[frozenset([g])], 3),
                     "unique": round(full - cache[frozenset(others)], 3)})

res = pd.DataFrame(rows)
res.to_csv(ROOT / "data/health/checks/places_input_shapley.csv", index=False)
wide = res.pivot(index="measure", columns="group", values="share_of_explained")[names]
print(f"{len(d)} tracts. Share of the explained variation credited to each group (Shapley):\n")
print((wide * 100).round(0).astype(int).astype(str).add("%").to_string())
print("\nEach group alone (R2):\n")
print(res.pivot(index="measure", columns="group", values="alone")[names].round(2).to_string())
print("\nLost if only that group is dropped (unique R2):\n")
print(res.pivot(index="measure", columns="group", values="unique")[names].round(3).to_string())
