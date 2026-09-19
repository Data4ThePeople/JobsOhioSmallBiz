#!/usr/bin/env python3
"""Apply subsidiary-check results (data/research/sub_*.json) to data/parents.csv.

Only rows first classified by rule R1 or R2 are touched. A 'yes' with a parent,
a bucket and a source replaces the parent, home state and bucket, grade B
(ownership shown on a company or news page), and notes the change. 'no' and
'unknown' leave the row as it was and append the check result to the notes, so
the methodology can count how many rule rows were checked and how many moved."""
import csv, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PARENTS = ROOT / "data" / "parents.csv"
BUCKETS = {"500-4999", "5000+", "<100", "100-499"}


def main(files):
    rows = list(csv.DictReader(PARENTS.open()))
    by_id = {r["recipient_id"]: r for r in rows}
    moved = checked = 0
    for f in files:
        for x in json.load(open(f)):
            r = by_id.get(x.get("recipient_id"))
            if r is None:
                sys.exit(f"{f}: unknown recipient_id {x.get('recipient_id')!r}")
            if not r["notes"].startswith(("Rule R1", "Rule R2")) or "Subsidiary check" in r["notes"]:
                continue
            checked += 1
            ans = (x.get("owned_by_larger") or "").strip().lower()
            if ans == "yes" and x.get("parent") and x.get("emp_bucket") in BUCKETS and x.get("source"):
                # grade B only when the source is an actual page stating the ownership; a
                # search-results link, or ownership or size the checker had to infer, is C
                weak = "news.google.com" in x["source"] or any(
                    w in (x.get("notes") or "").lower() for w in ("inferred", "estimate", "unconfirmed", "no source", "not confirmed", "likely"))
                r.update(parent=x["parent"].strip(), parent_hq_state=(x.get("parent_hq_state") or "").strip(),
                         emp_bucket=x["emp_bucket"], confidence="C" if weak else "B", hq_source=x["source"], emp_source=x["source"])
                r["notes"] += f" Subsidiary check: owned by {x['parent'].strip()}; rule result replaced. {x.get('notes', '')}".rstrip()
                moved += 1
            else:
                r["notes"] += f" Subsidiary check: {ans or 'unknown'}. {x.get('notes', '')}".rstrip()
    with PARENTS.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    total = sum(1 for r in rows if r["notes"].startswith(("Rule R1", "Rule R2")))
    done = sum(1 for r in rows if r["notes"].startswith(("Rule R1", "Rule R2")) and "Subsidiary check" in r["notes"])
    print(f"applied {len(files)} files: {checked} rule rows checked, {moved} moved to a larger parent; {done}/{total} rule rows now checked")


if __name__ == "__main__":
    main(sys.argv[1:])
