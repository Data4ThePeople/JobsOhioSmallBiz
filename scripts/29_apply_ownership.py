#!/usr/bin/env python3
"""Fold the ownership re-check into data/parents.csv.

211 parents were classified by the automatic rules R1 to R4, which read a
signal about the payee itself and never asked whether the company is owned by
somebody else. Two errors surfaced by accident (OMNOVA was Synthomer's,
Continental Structural Plastics was Teijin's, both acquired years before their
grants), so all 211 were checked.

Only `owned` rows are applied. `acquired after the grant` means the record was
already right and must be left alone, which is the point of recording the
acquisition date rather than today's owner.

Each change writes its reason, the acquisition date and the source into the
parent's notes, so a reader who disputes one call can see what it rested on.

Usage: 29_apply_ownership.py [--dry-run]
"""
import csv, json, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PARENTS = ROOT / "data" / "parents.csv"
RES = ROOT / "data" / "research_owner"
BUCKETS = {"<100", "100-499", "500-4999", "5000+"}


def main(argv):
    dry = "--dry-run" in argv
    rows = list(csv.DictReader(PARENTS.open()))
    by_id = {r["recipient_id"]: r for r in rows}

    found, verdicts = {}, Counter()
    for f in sorted(RES.glob("own_*.json")):
        if f.stem.endswith("_input"):
            continue
        for x in json.load(f.open()):
            found[x["recipient_id"]] = x
            verdicts[x.get("verdict", "?")] += 1
    print(f"{len(found)} parents checked: " +
          ", ".join(f"{k} {v}" for k, v in verdicts.most_common()))

    changed, oh_out, oh_in, skipped = [], 0, 0, []
    for rid, x in found.items():
        if x.get("verdict") != "owned":
            continue
        r = by_id.get(rid)
        if not r:
            skipped.append(rid); continue
        was_oh = r["parent_hq_state"].strip().upper() == "OH"
        now_oh = (x.get("parent_hq_state") or "").strip().upper() == "OH"
        cash = int(r["total_cash"] or 0)
        if was_oh and not now_oh:
            oh_out += cash
        elif now_oh and not was_oh:
            oh_in += cash

        before = f"{r['parent']} / {r['parent_hq_state']} / {r['emp_bucket']}"
        r["parent"] = x.get("parent") or r["parent"]
        if x.get("parent_hq_state"):
            r["parent_hq_state"] = x["parent_hq_state"]
        if x.get("emp_bucket") in BUCKETS:
            r["emp_bucket"] = x["emp_bucket"]
        if x.get("confidence") in ("A", "B", "C", "D"):
            r["confidence"] = x["confidence"]
        if x.get("hq_source"):
            r["hq_source"] = x["hq_source"]
        if x.get("emp_source"):
            r["emp_source"] = x["emp_source"]
        note = (f"Ownership re-check: {before} -> {r['parent']} / {r['parent_hq_state']} / "
                f"{r['emp_bucket']}."
                + (f" Acquired {x['acquired_date']}, before the grant years {r['years']}."
                   if x.get("acquired_date") else "")
                + f" {(x.get('notes') or '')[:260]}")
        # idempotent: replace the previous re-check note rather than stacking
        old = r.get("notes", "").split("Ownership re-check:")[0].strip()
        r["notes"] = (old + " " + note).strip()[:1200]
        changed.append((cash, r["name"], before, f"{r['parent']} / {r['parent_hq_state']} / {r['emp_bucket']}"))

    changed.sort(reverse=True)
    print(f"\n{len(changed)} parents reclassified by ownership:")
    for cash, name, before, after in changed:
        print(f"  ${cash:>9,}  {name[:30]:30s} {before[:38]:38s} -> {after[:40]}")
    print(f"\ndollars moving OUT of the Ohio column: ${oh_out:,}")
    print(f"dollars moving INTO the Ohio column:  ${oh_in:,}")
    if skipped:
        print(f"\n{len(skipped)} checked ids are not in parents.csv: {skipped[:5]}")

    if dry:
        print("\n--dry-run: nothing written")
        return
    with PARENTS.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    print(f"\nwrote {PARENTS.relative_to(ROOT)}")


if __name__ == "__main__":
    main(sys.argv[1:])
