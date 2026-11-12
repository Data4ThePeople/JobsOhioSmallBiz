#!/usr/bin/env python3
"""Pull the SBA's small-business size standards from the regulation itself.

13 CFR 121.201 is the legal definition: a table of every six-digit NAICS code
with the threshold below which a firm in that industry counts as small. It is
fetched from the eCFR renderer rather than from SBA's own PDF, because the eCFR
is the authoritative current text and is machine readable.

The headline fact the post needs: **there is no single SBA employee number.**
Roughly half the industries define small by annual receipts, not headcount at
all, and among those that do use employees the threshold runs from 100 to
1,500. "500 employees" is a widely repeated shorthand that is the standard for
only about a tenth of the industries that use an employee test.

Writes data/sba_size_standards.csv (naics, description, basis, threshold) and
prints the distribution.
"""
import csv, re, subprocess, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "sba_size_standards.csv"
SRC = ("https://www.ecfr.gov/api/renderer/v1/content/enhanced/current/"
       "title-13?part=121&section=121.201")
UA = "Data 4 The People research"


def main():
    p = subprocess.run(["curl", "-sL", "--max-time", "90", "-A", UA, SRC],
                       capture_output=True, text=True)
    h = p.stdout
    if len(h) < 50_000:
        sys.exit(f"eCFR returned {len(h)} bytes; expected the full section")

    rows = []
    for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", h, re.S):
        cells = [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", c)).strip()
                 for c in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", tr, re.S)]
        if len(cells) < 2 or not re.match(r"^\d{6}$", cells[0]):
            continue
        naics, desc, rest = cells[0], cells[1], " ".join(cells[2:])
        money = re.search(r"\$\s*([\d.]+)", " | ".join(cells))
        if money:
            rows.append({"naics": naics, "description": desc, "basis": "receipts",
                         "threshold": money.group(1),
                         "units": "millions of dollars of average annual receipts"})
            continue
        head = re.search(r"([\d,]{3,})", rest)
        if head:
            rows.append({"naics": naics, "description": desc, "basis": "employees",
                         "threshold": head.group(1).replace(",", ""), "units": "employees"})

    if len(rows) < 800:
        sys.exit(f"parsed only {len(rows)} NAICS rows; the table layout may have changed")
    with OUT.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["naics", "description", "basis", "threshold", "units"])
        w.writeheader(); w.writerows(rows)

    basis = Counter(r["basis"] for r in rows)
    print(f"{len(rows)} NAICS industries: {basis['employees']} define small by employees, "
          f"{basis['receipts']} by annual receipts")
    emp = Counter(int(r["threshold"]) for r in rows if r["basis"] == "employees")
    print("\nemployee thresholds, most used first:")
    for v, n in emp.most_common(10):
        print(f"  {v:>6,} employees  {n:4d} industries  {n/basis['employees']:5.1%}")
    print(f"\n  range {min(emp):,} to {max(emp):,}")
    print(f"  industries using exactly 500: {emp.get(500,0)} "
          f"({emp.get(500,0)/basis['employees']:.1%} of those that count employees, "
          f"{emp.get(500,0)/len(rows):.1%} of all industries)")

    # manufacturing is what JobsOhio mostly funds, so report it separately
    man = Counter(int(r["threshold"]) for r in rows
                  if r["basis"] == "employees" and r["naics"][:2] in ("31", "32", "33"))
    if man:
        tot = sum(man.values())
        print(f"\nmanufacturing (NAICS 31-33), {tot} industries, all employee-based:")
        for v, n in man.most_common(6):
            print(f"  {v:>6,} employees  {n:4d}  {n/tot:5.1%}")
        med = sorted(v for v, n in man.items() for _ in range(n))[tot // 2]
        print(f"  median manufacturing threshold: {med:,} employees")
    print(f"\nwrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
