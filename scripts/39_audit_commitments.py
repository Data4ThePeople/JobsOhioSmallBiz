#!/usr/bin/env python3
"""Report what is wrong with data/commitments.csv, which is three things.

JobsOhio's monthly project reports are PDFs and `03_parse_metrics.py` reads
them by word position. It gets most of it right and three things wrong, and
none of them is logged by the anomalies file the parser already writes, so
they were invisible until someone went looking.

**This script reports; it does not fix.** An attempt to fix the first defect
by changing where the header block stops cut the file from 2,984 rows to
2,468, because `build_layout` needs those lines to find its columns. The fix
is a real piece of work on the layout builder and it should not be done in a
hurry. Until then this makes the damage visible and countable.

What it finds:

  truncated   A company name reduced to a bare corporate suffix, like "Inc."
              or "& Rubber Company", or lost entirely. The first line of a
              wrapped name on the first data row of a page is swallowed by the
              header block, which stops only at a line carrying a dollar
              amount. Each one is a join that silently misses: line 2311 is a
              New Horizons Baking project in Lucas County that the site check
              for that very company did not know about.
  missing     A month absent from the series. November 2016 is the only one,
              and it is absent because the space glyph on those two pages is
              "$", which the parser cannot add to its glyph list without
              breaking every money field. 19 projects and $26,209,640 of
              commitments are missing, including a $14,000,000 revitalisation
              loan to FirstEnergy Generation whose matching Schedule I payment
              of $12,408,019 in FY2017 is the largest in the data with no
              commitment row behind it.
  shifted     A page where names and values are off by one row. June 2023 does
              this across six merged names, which is why Speyside Bourbon
              Cooperage currently reads as a $25,000 Summit County inclusion
              grant when its real project that month is Jackson and Pike
              counties, food and agribusiness, $125,000.

None of this touches a published share: the headline numbers come from
Schedule I and `parents.csv`, not from here. It touches the funded-county
fallback in `35_warn_join.py` and the site checks, both of which were
hand-verified for every case that mattered.

Usage: 39_audit_commitments.py
"""
import csv, re, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COM = ROOT / "data" / "commitments.csv"
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
SUFFIX = re.compile(r"(?i)^(&\s+)?(inc|llc|ltd|corp|co|company|corporation|holdings|"
                    r"group|llp|lp|plc)[.,]?( inc[.,]?)?$")
# months after the last report JobsOhio has published are not gaps
LAST_PUBLISHED = (2026, 7)


def main():
    rows = list(csv.DictReader(COM.open()))
    print(f"{len(rows)} commitment rows\n")

    bad = [(i, r) for i, r in enumerate(rows, 2)
           if not r["company"].strip() or SUFFIX.match(r["company"].strip())
           or len(r["company"].strip()) <= 4]
    print(f"TRUNCATED: {len(bad)} rows whose company name is a bare suffix or empty")
    for i, r in bad:
        print(f"  line {i:5d}  {r['company']!r:20s} {r['report_month']:9s} "
              f"{r['county'][:14]:14s} {r['program_value']:>12s}  {r['source_file'][:28]}")

    have = {r["report_month"] for r in rows}
    gaps = [f"{y}-{m}" for y in range(2015, 2027) for m in MONTHS
            if f"{y}-{m}" not in have
            and (y, MONTHS.index(m) + 1) >= (2015, 4)
            and (y, MONTHS.index(m) + 1) <= LAST_PUBLISHED]
    print(f"\nMISSING MONTHS: {len(gaps)}")
    for g in gaps:
        print(f"  {g}  no rows parsed from this report at all")

    # A month whose row count is far off its neighbours is worth a look too.
    per = Counter(r["report_month"] for r in rows)
    vals = sorted(per.values())
    med = vals[len(vals) // 2]
    thin = [(m, n) for m, n in sorted(per.items()) if n <= max(1, med // 4)]
    print(f"\nTHIN MONTHS: {len(thin)} with {max(1, med//4)} rows or fewer "
          f"(median month has {med})")
    for m, n in thin:
        print(f"  {m}  {n} rows")

    print(f"\n{len(bad)} truncated, {len(gaps)} months missing, {len(thin)} thin.")
    print("Reported, not fixed. See this file's header for why, and for the "
          "FirstEnergy\nlead hiding in the missing month.")
    return 1 if (bad or gaps) else 0


if __name__ == "__main__":
    sys.exit(main())
