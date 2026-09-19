#!/usr/bin/env python3
"""Write data/review_simple.csv: the simplified review sheet.

Three calls per company, each a plain choice:
  size        Large / Small (500 employees at the ultimate parent, worldwide,
              at the time of the grant)
  ohio_hq     Yes / No (parent headquartered in Ohio at the time of the grant)
  confidence  High (filing, JobsOhio or partner release, or news naming size
              and owner) / Best guess (website, directory, Wikipedia, or
              inference)
Rows: every business parent paid $1,000,000 or more, then every best-guess
business parent paid $250,000 or more, largest first within each. Answers
already typed into data/review_for_eric.csv are carried over."""
import csv, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
d = json.loads((ROOT / "dist" / "data.json").read_text())
# answers are never lost on a rebuild: take them from the earlier sheet and from
# the current simple sheet, the current one winning
old = {r["parent"]: r["eric_ok"] for r in csv.DictReader((ROOT / "data" / "review_for_eric.csv").open()) if r.get("eric_ok")}
cur = ROOT / "data" / "review_simple.csv"
if cur.exists():
    old.update({r["company"]: r["your_answer"] for r in csv.DictReader(cur.open()) if r.get("your_answer")})
notes = {}
for r in csv.DictReader((ROOT / "data" / "parents.csv").open()):
    notes.setdefault(r["parent"].strip() or r["name"].strip(), r)
rows = []
for p in d["parents_table"]:
    if p["class"] != "business":
        continue
    high = p["conf"] in ("A", "B")
    if p["cash"] >= 1_000_000:
        why = "Paid $1M or more"
    elif p["cash"] >= 250_000 and not high:
        why = "Best guess, paid $250K or more"
    else:
        continue
    n = notes.get(p["parent"], {})
    rows.append({
        "why_listed": why, "company": p["parent"], "paid": p["cash"],
        "size": "Small" if p["bucket"] in ("<100", "100-499") else "Large",
        "ohio_hq": "Yes" if (p["hq"] or "").upper() == "OH" else "No",
        "hq_where": p["hq"], "confidence": "High" if high else "Best guess",
        "basis": (n.get("notes", "") or "").split(" Random re-check")[0][:300],
        "source": (p["sources"] or [""])[0],
        "your_answer": old.get(p["parent"], ""),
    })
rows.sort(key=lambda r: (r["why_listed"] != "Paid $1M or more", -r["paid"]))
out = ROOT / "data" / "review_simple.csv"
with out.open("w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
a = [r for r in rows if r["why_listed"] == "Paid $1M or more"]
print(f"wrote {out.relative_to(ROOT)}: {len(a)} companies paid $1M+, {len(rows) - len(a)} best guesses paid $250K+; {sum(1 for r in rows if r['your_answer'])} answers carried over")
