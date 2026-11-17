# Tie-out: ohio-income-health

Written by `scripts/56_tieout_post2.py`. Recomputed from the raw ACS and PLACES files in TractEconHealth, not from the tables the GIF scripts read. The first post's tie-out is `TIEOUT.md`.

**0 differences.**

## GIF 1: income and health

| Figure | Recomputed from raw | Built | |
|---|---|---|---|
| Ohio tracts after filters | 3125 | 3125 | match |
| Tracts with income (dots per frame) | 3115 | 3115 | match |
| Tracts top-coded at $250,001 | 3 | 3 | match |
| Tracts where income differs from extract | 0 | 0 | match |
| diabetes: tracts where value differs | 0 | 0 | match |
| diabetes: highest tract / y-axis top | 39.0 / 40% | 39.0 / 40% | match |
| obesity: tracts where value differs | 0 | 0 | match |
| obesity: highest tract / y-axis top | 57.7 / 60% | 57.7 / 60% | match |
| smoking: tracts where value differs | 0 | 0 | match |
| smoking: highest tract / y-axis top | 41.9 / 50% | 41.9 / 50% | match |
| inactivity: tracts where value differs | 0 | 0 | match |
| inactivity: highest tract / y-axis top | 57.5 / 60% | 57.5 / 60% | match |
| short_sleep: tracts where value differs | 0 | 0 | match |
| short_sleep: highest tract / y-axis top | 57.0 / 60% | 57.0 / 60% | match |
| food_insecurity: tracts where value differs | 0 | 0 | match |
| food_insecurity: highest tract / y-axis top | 75.3 / 80% | 75.3 / 80% | match |
| loneliness: tracts where value differs | 0 | 0 | match |
| loneliness: highest tract / y-axis top | 50.7 / 60% | 50.7 / 60% | match |

## GIF 2: the map

| Figure | Recomputed | Built | |
|---|---|---|---|
| Counties | 88 | 88 | match |
| Ohio population, all counties | 11810293 | 11810293 | match |
| Dollars placed in a county | 1257313860 | 1257313860 | match |
| Total, Cuyahoga | $227.7 million | $227.7 million | match |
| Total, Franklin | $150.3 million | $150.3 million | match |
| Total, Licking | $145.9 million | $145.9 million | match |
| Per person, Licking | $802 | $802 | match |
| Per person, Belmont | $566 | $566 | match |
| Per person, Logan | $456 | $456 | match |
| Legend low end (lowest tract income) | $7k | $7k | match |
| Legend high end | $250k | $250k | match |
| Tracts coloured on the map | 3115 | 3115 | match |

## Analysis scripts reproduce

| Script | Output unchanged on re-run | | |
|---|---|---|---|
| 53_places_input_check.py | 917a865d4024 | 917a865d4024 | match |
| 54_county_counted_check.py | b67a840f8eb8 | b67a840f8eb8 | match |
| 55_places_input_shapley.py | e62d16194c2e | e62d16194c2e | match |

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
