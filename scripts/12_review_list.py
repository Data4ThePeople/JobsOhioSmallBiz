#!/usr/bin/env python3
"""Write data/review_for_eric.csv: the parent companies Eric checks by hand.

Section 1: every parent paid $1,000,000 or more (about three quarters of all
dollars). Section 2: parents paid $250,000 to $999,999 whose classification
is low confidence (C or D) or unresolved. Sorted by dollars within each
section. Columns are the classification plus the evidence behind it, with an
empty 'eric_ok' column (y / n / note) for his answer."""
import csv, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "dist" / "data.json"
PARENTS = ROOT / "data" / "parents.csv"
OUT = ROOT / "data" / "review_for_eric.csv"


def main():
    d = json.loads(DATA.read_text())
    notes = {}
    for r in csv.DictReader(PARENTS.open()):
        k = r["parent"].strip() or r["name"].strip()
        notes.setdefault(k, []).append(r)
    tot = sum(p["cash"] for p in d["parents_table"])
    rows = []
    for p in d["parents_table"]:
        sec = "1: $1M+" if p["cash"] >= 1_000_000 else ("2: low-confidence $250k+" if p["cash"] >= 250_000 and (p["conf"] in ("C", "D") or not p["bucket"]) else None)
        if not sec:
            continue
        src = notes.get(p["parent"], [])
        rows.append({
            "section": sec, "parent": p["parent"], "paid": p["cash"], "share_of_all": f"{p['cash'] / tot:.2%}",
            "type": p["class"], "employees": p["bucket"] or "unresolved", "hq": p["hq"], "evidence": p["conf"],
            "payees_on_990": " | ".join(sorted({r["name"] for r in src}))[:200],
            "employee_source": " | ".join(sorted({r["emp_source"] for r in src if r["emp_source"]}))[:300],
            "notes": " | ".join(sorted({r["notes"] for r in src if r["notes"]}))[:500],
            "eric_ok": "",
        })
    rows.sort(key=lambda r: (r["section"], -r["paid"]))
    with OUT.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    s1 = [r for r in rows if r["section"].startswith("1")]
    s2 = [r for r in rows if r["section"].startswith("2")]
    print(f"wrote {OUT.relative_to(ROOT)}: section 1 {len(s1)} parents, ${sum(r['paid'] for r in s1):,} ({sum(r['paid'] for r in s1) / tot:.0%} of dollars); section 2 {len(s2)} parents")


if __name__ == "__main__":
    main()
