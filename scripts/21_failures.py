#!/usr/bin/env python3
"""Consolidate the verified failure checks into data/failures.csv.

Input: the verification files in data/research3/ (fail_*.json for the
bankruptcy-type flags, soft_*.json for closures and layoffs). Each row has
already been checked for whether it is the same company, what happened, and
whether it happened after the grant.

Output keeps every verdict, including the rejects, so the published count can
be audited: a reader should be able to see what was thrown out and why.
"""
import csv, json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "data" / "research3"
OUT = ROOT / "data" / "failures.csv"

parents = {}
for r in csv.DictReader((ROOT / "data" / "parents.csv").open()):
    parents[r["recipient_id"]] = r

rows = []
for f in sorted(RES.glob("*.json")):
    if f.stem.endswith("_input"):
        continue
    for x in json.load(f.open()):
        p = parents.get(x.get("recipient_id"), {})
        rows.append({
            "name": x.get("name") or p.get("name", ""),
            "parent": p.get("parent", ""),
            "class": p.get("recipient_class") or p.get("recipient_class_auto", ""),
            "paid": int(p.get("total_cash", 0) or 0),
            "grant_years": p.get("years", ""),
            "verdict": x.get("verdict", ""), "event": x.get("event", ""),
            "event_date": x.get("event_date", ""), "entity_filed": x.get("entity_filed", ""),
            "court": x.get("court", ""), "docket": x.get("docket", ""),
            "ohio_outcome": (x.get("ohio_outcome") or "")[:300],
            "confidence": x.get("confidence", ""), "source": x.get("source", ""),
            "flagged_by": "failure headline" if f.stem.startswith("fail") else "closure or layoff headline",
            "notes": (x.get("notes") or "")[:300],
        })
rows.sort(key=lambda r: (r["verdict"] != "Confirmed failure", -r["paid"]))
with OUT.open("w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

conf = [r for r in rows if r["verdict"] == "Confirmed failure"]
print(f"{len(rows)} candidates checked; verdicts: {dict(Counter(r['verdict'] for r in rows))}")
print(f"confirmed: {len(conf)} recipients, ${sum(r['paid'] for r in conf):,} paid\n")
print(f"{'company':34s} {'paid':>11s} {'grant yrs':12s} {'event':12s} {'when':11s} outcome")
for r in conf:
    print(f"{r['name'][:34]:34s} {r['paid']:11,} {r['grant_years'][:12]:12s} {r['event'][:12]:12s} "
          f"{r['event_date'][:11]:11s} {r['ohio_outcome'][:70]}")
print(f"\nwrote {OUT.relative_to(ROOT)}")
