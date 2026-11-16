#!/usr/bin/env python3
"""Median household income against self-reported health, by Ohio census tract.

The second post's premise is that economic development is not only a jobs
question. This is the measurement behind it: for every census tract in Ohio,
what households earn, and what share of adults say their health is fair or
poor.

Two sources, both tract-level, both public:

  income  ACS 2023 five-year estimates, table B19013 (median household income)
          and B01003 (population), from the Census API. 3,168 Ohio tracts, of
          which 3,129 report an income.
  health  CDC PLACES, measure GHLTH, "fair or poor self-rated health status
          among adults". Model-based small-area estimates, which matters: they
          are modelled from BRFSS and not counted, so a single tract's value
          carries real uncertainty and the file ships confidence limits.

**Why one measure and not an index.** PLACES publishes about forty measures
and it is tempting to roll them into a health index. A composite invites the
question of how it was weighted, and there is no good answer. Fair-or-poor
self-rated health is a single number, widely used, and understood without
explanation. Other measures are available the same way and the relationship
looks similar in each; GHLTH is the one the post should lead on.

**What the relationship is NOT.** This is a correlation across tracts at one
point in time. Poorer places have worse health, which surprises nobody; it
does not establish that a grant to a poor tract would improve health there,
and the post must not imply that it does.

Writes data/health/tract_income_health_oh.csv and prints the correlation.

Usage: 42_health_income.py [--refetch]
"""
import csv, json, math, statistics, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "health"
UA = "Data 4 The People research"
ACS = OUT / "acs_income_tract_oh.json"
PLACES = OUT / "places_ghlth_tract_oh.json"


def key():
    sys.path.insert(0, str(Path.home() / ".claude" / "d4tp-process"))
    import d4tp_env
    return d4tp_env.read_env_file(d4tp_env.CENTRAL).get("CENSUS_API_KEY", "")


def fetch(url, dest):
    subprocess.run(["curl", "-s", "--max-time", "120", "-A", UA, url, "-o", str(dest)],
                   check=True)


def pearson(x, y):
    n = len(x)
    mx, my = sum(x) / n, sum(y) / n
    num = sum((a - mx) * (b - my) for a, b in zip(x, y))
    den = math.sqrt(sum((a - mx) ** 2 for a in x) * sum((b - my) ** 2 for b in y))
    return num / den if den else 0.0


def main(argv):
    OUT.mkdir(parents=True, exist_ok=True)
    if "--refetch" in argv or not ACS.exists():
        fetch("https://api.census.gov/data/2023/acs/acs5?get=NAME,B19013_001E,"
              f"B01003_001E&for=tract:*&in=state:39&key={key()}", ACS)
    if "--refetch" in argv or not PLACES.exists():
        fetch("https://data.cdc.gov/resource/cwsq-ngmh.json?stateabbr=OH"
              "&measureid=GHLTH&$limit=5000&$select=locationname,countyname,"
              "data_value,totalpopulation,low_confidence_limit,high_confidence_limit",
              PLACES)

    a = json.loads(ACS.read_text())
    hdr, rows = a[0], a[1:]
    ix = {c: hdr.index(c) for c in hdr}
    inc = {}
    for r in rows:
        geoid = r[ix["state"]] + r[ix["county"]] + r[ix["tract"]]
        try:
            v = int(r[ix["B19013_001E"]])
        except (TypeError, ValueError):
            continue
        # the API returns large negative sentinels for suppressed cells
        if v > 0:
            inc[geoid] = (v, int(r[ix["B01003_001E"]] or 0),
                          r[ix["NAME"]].split(";")[1].strip() if ";" in r[ix["NAME"]] else "")

    hl = {x["locationname"]: x for x in json.loads(PLACES.read_text())
          if x.get("data_value")}
    both = [(g, inc[g], hl[g]) for g in inc if g in hl]
    print(f"tracts: {len(inc)} with income, {len(hl)} with health, {len(both)} with both")

    f = OUT / "tract_income_health_oh.csv"
    with f.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["geoid", "county", "median_household_income", "population",
                    "pct_fair_or_poor_health", "ci_low", "ci_high"])
        for g, (income, pop, county), h in sorted(both):
            w.writerow([g, county, income, pop, h["data_value"],
                        h.get("low_confidence_limit", ""), h.get("high_confidence_limit", "")])

    x = [v[1][0] for v in both]
    lx = [math.log(v) for v in x]
    y = [float(v[2]["data_value"]) for v in both]
    print(f"\nmedian household income against fair or poor health, {len(both)} tracts")
    print(f"  Pearson r, income     : {pearson(x, y):+.3f}")
    print(f"  Pearson r, log income : {pearson(lx, y):+.3f}   r2 {pearson(lx, y)**2:.3f}")
    print("\n  income quintile    median income    mean fair/poor health")
    q = sorted(zip(x, y))
    n, step = len(q), len(q) // 5
    for i in range(5):
        c = q[i * step:(i + 1) * step if i < 4 else n]
        print(f"    Q{i+1}  {len(c):>4} tracts   ${statistics.median(v[0] for v in c):>8,.0f}"
              f"        {statistics.mean(v[1] for v in c):>5.1f}%")
    print(f"\nwrote {f.relative_to(ROOT)}")
    print("\nThis is a cross-sectional correlation. It says poorer tracts report worse\n"
          "health, not that money moved into one would improve health there.")


if __name__ == "__main__":
    main(sys.argv[1:])
