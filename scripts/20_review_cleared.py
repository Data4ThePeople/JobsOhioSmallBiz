#!/usr/bin/env python3
"""Write data/review_cleared.csv: the review list with every row answered,
showing who answered it, the size and home-state call, the employee figure
behind it and how sure we are.

Columns: company, paid, size, employees, employees_asof, ohio_hq, hq_where,
answered_by (Eric / agent / unanswered), confidence, source, basis.
Sorted by dollars, largest first.
"""
import csv, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
rev = list(csv.DictReader((ROOT / "data" / "review_simple.csv").open()))
parents = {}
for r in csv.DictReader((ROOT / "data" / "parents.csv").open()):
    parents.setdefault(r["parent"].strip() or r["name"].strip(), r)

rows = []
for x in rev:
    p = parents.get(x["company"], {})
    by = p.get("review_by") or ""
    rows.append({
        "company": x["company"], "paid": int(x["paid"]),
        "size": p.get("review_size") or x["size"],
        "employees": p.get("review_employees", ""), "employees_asof": p.get("review_asof", ""),
        "ohio_hq": p.get("review_hq") or x["ohio_hq"], "hq_where": p.get("parent_hq_state") or x["hq_where"],
        "answered_by": {"eric": "Eric", "agent": "agent"}.get(by, "unanswered"),
        "confidence": p.get("review_confidence") or x["confidence"],
        "source": p.get("review_source", ""),
        "basis": (p.get("review_notes") or x["basis"])[:300],
    })
rows.sort(key=lambda r: -r["paid"])
out = ROOT / "data" / "review_cleared.csv"
with out.open("w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

from collections import Counter
by = Counter(r["answered_by"] for r in rows)
conf = Counter(r["confidence"] for r in rows if r["answered_by"] == "agent")
print(f"wrote {out.relative_to(ROOT)}: {len(rows)} companies, ${sum(r['paid'] for r in rows):,}")
print("  answered by:", dict(by))
print("  agent confidence:", dict(conf))
low = [r for r in rows if r["answered_by"] == "agent" and r["confidence"] == "Low"]
if low:
    print(f"  low confidence, worth your eye ({len(low)}):")
    for r in low:
        print(f"    ${r['paid']:>9,} {r['company'][:44]:44s} {r['size']:5s} {r['hq_where']:8s} {r['employees'][:40]}")
