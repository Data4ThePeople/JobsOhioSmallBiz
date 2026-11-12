#!/usr/bin/env python3
"""Fold FY2025 into the analysis: the grant rows, then the new recipients.

FY2025 (year ending June 30, 2025) has no e-file XML anywhere, so its Schedule I
comes from JobsOhio's own PDF via 23_parse_sched_i_pdf.py. This script merges
that year into data/grants_raw.csv and adds the recipients that had never been
seen before to data/parents.csv, from the research batches in
data/research2025/.

Both halves are idempotent: the FY2025 grant rows are replaced rather than
appended, and a recipient already in parents.csv keeps its existing research
unless --overwrite is passed. Run it after 02_parse_sched_i.py and
23_parse_sched_i_pdf.py, and before 09_analyze.py.

Usage: 26_add_fy2025.py [--fy 2025] [--overwrite] [--dry-run]
"""
import csv, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from names import normalize_name

GRANTS = ROOT / "data" / "grants_raw.csv"
PARENTS = ROOT / "data" / "parents.csv"
BUCKETS = {"<100", "100-499", "500-4999", "5000+"}
CLASSES = {"business", "site_development", "government", "university", "hospital", "nonprofit"}
GRADES = {"A", "B", "C", "D"}


def recipient_id(name, ein):
    e = re.sub(r"\D", "", ein or "")
    return f"EIN:{e}" if len(e) == 9 and e.strip("0") else f"NAME:{normalize_name(name)}"


def main(argv):
    fy = int(argv[argv.index("--fy") + 1]) if "--fy" in argv else 2025
    overwrite, dry = "--overwrite" in argv, "--dry-run" in argv
    new_grants = ROOT / "data" / f"grants_fy{fy}.csv"
    research = ROOT / "data" / f"research{fy}"
    if not new_grants.exists():
        sys.exit(f"no {new_grants.relative_to(ROOT)}; run 23_parse_sched_i_pdf.py first")

    # --- grant rows -------------------------------------------------------
    rows = list(csv.DictReader(GRANTS.open()))
    fields = list(rows[0])
    add = list(csv.DictReader(new_grants.open()))
    kept = [r for r in rows if int(r["fiscal_year"]) != fy]
    for r in add:
        for k in fields:
            r.setdefault(k, "")
    merged = kept + [{k: r.get(k, "") for k in fields} for r in add]
    merged.sort(key=lambda r: (int(r["fiscal_year"]), int(r["row_in_filing"] or 0)))
    print(f"grant rows: {len(rows)} -> {len(merged)} "
          f"(FY{fy}: {len(rows) - len(kept)} replaced by {len(add)})")
    print(f"  FY{fy} cash ${sum(int(r['cash_amt']) for r in add):,}")

    # --- recipients -------------------------------------------------------
    parents = list(csv.DictReader(PARENTS.open()))
    pfields = list(parents[0])
    by_id = {r["recipient_id"]: r for r in parents}

    found = {}
    for f in sorted(research.glob("*.json")) if research.exists() else []:
        if f.stem.endswith("_input"):
            continue
        for x in json.load(f.open()):
            rid = x.get("recipient_id")
            if rid:
                found[rid] = x
    print(f"research rows available: {len(found)}")

    # roll the FY2025 grant rows up per recipient, the same way 04/05 do
    agg = {}
    for r in add:
        rid = recipient_id(r["recipient_name"], r["recipient_ein"])
        a = agg.setdefault(rid, {"name": r["recipient_name"], "ein": r["recipient_ein"],
                                 "city": r["city"], "state": r["state"],
                                 "irc_section": r["irc_section"], "cash": 0, "n": 0})
        a["cash"] += int(r["cash_amt"]); a["n"] += 1

    added, updated, unresearched = 0, 0, []
    for rid, a in agg.items():
        rec = found.get(rid)
        existing = by_id.get(rid)
        if existing:
            # A returning recipient keeps its research and gains the year. The
            # totals are RECOMPUTED from the merged grant rows rather than
            # incremented: incrementing is not idempotent, and re-running this
            # script after fixing the parser would have doubled the money.
            years = sorted(set(existing["years"].split()) | {str(fy)})
            existing["years"] = " ".join(years)
            own = [g for g in merged if recipient_id(g["recipient_name"], g["recipient_ein"]) == rid]
            existing["total_cash"] = str(sum(int(g["cash_amt"]) for g in own))
            existing["n_rows"] = str(len(own))
            updated += 1
            continue
        if not rec:
            unresearched.append((a["name"], a["cash"]))
            continue
        row = {k: "" for k in pfields}
        row.update(recipient_id=rid, name=a["name"], ein=a["ein"], city=a["city"],
                   state=a["state"], irc_section=a["irc_section"],
                   total_cash=str(a["cash"]), n_rows=str(a["n"]), years=str(fy))
        for k in ("recipient_class", "parent", "parent_hq_state", "hq_source",
                  "emp_bucket", "emp_source", "emp_asof", "confidence",
                  "founded_in_ohio", "notes"):
            row[k] = str(rec.get(k, "") or "")
        row["recipient_class_auto"] = row["recipient_class"]
        parents.append(row); by_id[rid] = row; added += 1

    # the analysis trusts these columns, so refuse values it cannot read
    bad = []
    for rid, a in agg.items():
        r = by_id.get(rid)
        if not r:
            continue
        if r["recipient_class"] and r["recipient_class"] not in CLASSES:
            bad.append(f"{r['name']}: recipient_class {r['recipient_class']!r}")
        if r["emp_bucket"] and r["emp_bucket"] not in BUCKETS:
            bad.append(f"{r['name']}: emp_bucket {r['emp_bucket']!r}")
        if r["confidence"] and r["confidence"] not in GRADES:
            bad.append(f"{r['name']}: confidence {r['confidence']!r}")
    if bad:
        print(f"\n{len(bad)} rows carry a value the analysis cannot read:")
        for b in bad[:12]:
            print("  " + b)
        sys.exit("fix the research output before merging")

    print(f"recipients: {added} added, {updated} returning recipients gained FY{fy}")
    if unresearched:
        tot = sum(c for _, c in unresearched)
        print(f"\n{len(unresearched)} FY{fy} recipients have no research yet (${tot:,}); "
              f"they would be unclassified in the headline:")
        for n, c in sorted(unresearched, key=lambda x: -x[1])[:10]:
            print(f"  ${c:>10,}  {n[:52]}")
        if len(unresearched) > 10:
            print(f"  ... and {len(unresearched) - 10} more")

    if dry:
        print("\n--dry-run: nothing written")
        return
    if unresearched and not overwrite:
        sys.exit("\nrefusing to write while recipients are unresearched; "
                 "finish the batches, or pass --overwrite to merge anyway")
    with GRANTS.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields); w.writeheader(); w.writerows(merged)
    with PARENTS.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=pfields); w.writeheader(); w.writerows(parents)
    print(f"\nwrote {GRANTS.relative_to(ROOT)} and {PARENTS.relative_to(ROOT)}")


if __name__ == "__main__":
    main(sys.argv[1:])
