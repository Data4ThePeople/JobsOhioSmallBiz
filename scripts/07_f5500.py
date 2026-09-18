#!/usr/bin/env python3
"""Form 5500 participant counts for Schedule I recipient EINs, from the DOL
bulk files for plan years 2015, 2019 and 2023 (data/raw/f5500/*.zip).

Writes data/f5500_participants.csv: ein, sponsor, sponsor_state,
participants_2015, participants_2019, participants_2023, plans_<year>.
Participants = the largest plan's beginning-of-year total participants for
that sponsor EIN (max across plans, not sum, since one worker is usually in
both a retirement and a welfare plan). Includes former employees with
balances, so it is a size band, not a headcount."""
import csv, io, sys, zipfile
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw" / "f5500"
RECIP = ROOT / "data" / "recipients.csv"
OUT = ROOT / "data" / "f5500_participants.csv"
YEARS = ("2015", "2019", "2023")

# (zip name pattern, ein column, sponsor column, state column, participants column)
FORMS = [
    ("F_5500_{y}_Latest.zip", "SPONS_DFE_EIN", "SPONSOR_DFE_NAME", "SPONS_DFE_MAIL_US_STATE", "TOT_PARTCP_BOY_CNT"),
    ("F_5500_SF_{y}_Latest.zip", "SF_SPONS_EIN", "SF_SPONSOR_NAME", "SF_SPONS_US_STATE", "SF_TOT_PARTCP_BOY_CNT"),
]


def main():
    eins = {r["ein"] for r in csv.DictReader(RECIP.open()) if r["ein"]}
    best = defaultdict(dict)   # ein -> {year: (participants, sponsor, state, nplans)}
    for y in YEARS:
        for pat, ein_c, sp_c, st_c, p_c in FORMS:
            path = RAW / pat.format(y=y)
            if not path.exists():
                print(f"missing {path.name}"); continue
            n = hit = 0
            with zipfile.ZipFile(path) as z:
                csvname = next(m for m in z.namelist() if m.lower().endswith(".csv"))
                with z.open(csvname) as fh:
                    rd = csv.DictReader(io.TextIOWrapper(fh, encoding="utf-8", errors="replace"))
                    for row in rd:
                        n += 1
                        ein = (row.get(ein_c) or "").strip()
                        if ein not in eins:
                            continue
                        hit += 1
                        try:
                            p = int(float(row.get(p_c) or 0))
                        except ValueError:
                            p = 0
                        cur = best[ein].get(y)
                        if cur is None or p > cur[0]:
                            best[ein][y] = (p, (row.get(sp_c) or "").strip(), (row.get(st_c) or "").strip(), (cur[3] if cur else 0) + 1)
                        else:
                            best[ein][y] = (cur[0], cur[1], cur[2], cur[3] + 1)
            print(f"{path.name}: {n:,} filings, {hit} on recipient EINs")
    out = []
    for ein, years in best.items():
        latest = years[max(years)]
        row = {"ein": ein, "sponsor": latest[1], "sponsor_state": latest[2]}
        for y in YEARS:
            row[f"participants_{y}"] = years[y][0] if y in years else ""
            row[f"plans_{y}"] = years[y][3] if y in years else ""
        out.append(row)
    out.sort(key=lambda r: r["sponsor"])
    with OUT.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
    print(f"wrote {OUT.name}: {len(out)} recipient EINs with a Form 5500 filing")


if __name__ == "__main__":
    main()
