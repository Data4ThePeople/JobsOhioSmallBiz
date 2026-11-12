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
# only the failure-verification files. data/research3/ also holds the lawsuit
# readings and olive_ai_suit.json, which have a different shape; globbing
# "*.json" swept those in and iterating a dict yields its keys as strings.
for f in sorted(list(RES.glob("fail_*.json")) + list(RES.glob("soft_*.json"))):
    if f.stem.endswith("_input"):
        continue
    for x in json.load(f.open()):
        p = parents.get(x.get("recipient_id"), {})
        rows.append({
            # join key: two recipients can share a name under different EINs
            # (there are two Speedway LLCs), so a name-based join is unsafe
            "recipient_id": x.get("recipient_id", ""),
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
            "notes": (x.get("notes") or "")[:300], "category": "",
        })
# "Confirmed failure" covers several different outcomes, and the post should
# not call a sale a failure. The set is small enough to categorise by name,
# which is clearer than keyword rules that misread "sold" in a closure notice.
CATEGORY = {
    "Bankruptcy or receivership": ["PETMIN", "80 ACRES", "NOSTRUM", "Express Inc",
                                   "COLUMBUS STEEL", "MULTI-COLOR", "Zulily"],
    "Funded site closed": ["NESTLE", "DANA", "ST BERNARD", "P GRAHAM DUNN", "REPUBLIC STEEL", "iMFLUX",
                           "Mohawk", "NEW HORIZONS", "FedEx Supply Chain", "OLIVE AI"],
    "Mass layoff at the funded site": ["ULTIUM", "COVERMYMEDS", "HYLAND", "SAREPTA", "SPEEDWAY",
                                       "Sauder", "Klarna", "AIR WISCONSIN"],
    "Sold or absorbed": ["FirstMerit", "AK STEEL", "PPG INDUSTRIES"],
    # Air Wisconsin's $50,000 was a 2018 economic development grant for a
    # Dayton operation, not an air service grant, and the Ohio evidence is a
    # 201-person Dayton WARN notice. Only Avelo belongs in the air-service row.
    "Subsidized service ended": ["AVELO"],
}
for r in rows:
    r["category"] = ""
    if r["verdict"] != "Confirmed failure":
        continue
    for cat, names in CATEGORY.items():
        if any(n.lower() in r["name"].lower() for n in names):
            r["category"] = cat
            break
    if not r["category"]:
        r["category"] = {"Chapter 7": "Bankruptcy or receivership", "Chapter 11": "Bankruptcy or receivership",
                         "Receivership": "Bankruptcy or receivership", "Closure": "Funded site closed",
                         "Layoffs": "Mass layoff at the funded site"}.get(r["event"], "Other")

rows.sort(key=lambda r: (r["verdict"] != "Confirmed failure", r.get("category", ""), -r["paid"]))
with OUT.open("w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

conf = [r for r in rows if r["verdict"] == "Confirmed failure"]
print(f"{len(rows)} candidates checked; verdicts: {dict(Counter(r['verdict'] for r in rows))}")
print(f"confirmed: {len(conf)} recipients, ${sum(r['paid'] for r in conf):,} paid\n")
for cat in ("Bankruptcy or receivership", "Funded site closed", "Mass layoff at the funded site",
            "Sold or absorbed", "Subsidized service ended"):
    group = [r for r in conf if r["category"] == cat]
    if not group:
        continue
    print(f"\n{cat} ({len(group)}, ${sum(r['paid'] for r in group):,})")
    for r in group:
        print(f"  {r['name'][:32]:32s} {r['paid']:11,} {r['grant_years'][:12]:12s} {r['event_date'][:10]:10s} {r['ohio_outcome'][:62]}")
print(f"\nwrote {OUT.relative_to(ROOT)}")
