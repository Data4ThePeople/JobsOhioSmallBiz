#!/usr/bin/env python3
"""Two helpers for the parent-resolution research pass.

  08_research.py batch <N> [--min DOLLARS] [--max DOLLARS] [--size 25]
      Print batch N (0-based) of unresearched recipients as a JSON list with
      every automated signal, for a research agent to work from. Batches are
      ordered by total_cash descending within the dollar range.

  08_research.py merge data/research/*.json
      Merge researched rows into data/parents.csv. Each JSON file is a list of
      objects with recipient_id and the hand columns (recipient_class, parent,
      parent_hq_state, hq_source, emp_bucket, emp_source, emp_asof,
      confidence, founded_in_ohio, notes). Existing hand values are
      overwritten only when the incoming row has a non-empty value.
      A row whose recipient_id is unknown is a hard failure."""
import csv, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PARENTS = ROOT / "data" / "parents.csv"
HAND = ["recipient_class", "parent", "parent_hq_state", "hq_source", "emp_bucket",
        "emp_source", "emp_asof", "confidence", "founded_in_ohio", "notes"]
BUCKETS = {"<100", "100-499", "500-4999", "5000+", ""}
CLASSES = {"business", "site_development", "government", "nonprofit", "university", "hospital", ""}
SIGNALS = ["recipient_id", "name", "ein", "city", "state", "irc_section", "total_cash", "years",
           "recipient_class_auto", "edgar_name", "edgar_state_inc", "edgar_hq_state",
           "f5500_participants_2015", "f5500_participants_2019", "f5500_participants_2023", "f5500_sponsor",
           "metrics_company", "metrics_programs", "metrics_jobs_retained_max", "metrics_industry", "metrics_commit_total"]


def load():
    return list(csv.DictReader(PARENTS.open()))


def cmd_batch(args):
    n = int(args[0]); lo = 0; hi = 10**12; size = 25
    if "--min" in args: lo = int(args[args.index("--min") + 1])
    if "--max" in args: hi = int(args[args.index("--max") + 1])
    if "--size" in args: size = int(args[args.index("--size") + 1])
    rows = [r for r in load() if lo <= int(r["total_cash"]) < hi and not r["parent"]]
    rows.sort(key=lambda r: -int(r["total_cash"]))
    batch = rows[n * size:(n + 1) * size]
    print(json.dumps([{k: r[k] for k in SIGNALS} for r in batch], indent=1))
    print(f"# batch {n} of {(len(rows) + size - 1) // size} ({len(rows)} unresearched rows in range)", file=sys.stderr)


def cmd_merge(files):
    rows = load()
    by_id = {r["recipient_id"]: r for r in rows}
    n_new = 0
    for f in files:
        data = json.load(open(f))
        for item in data:
            rid = item.get("recipient_id")
            if rid not in by_id:
                sys.exit(f"{f}: unknown recipient_id {rid!r}")
            if item.get("emp_bucket", "") not in BUCKETS:
                sys.exit(f"{f}: bad emp_bucket {item.get('emp_bucket')!r} for {rid}")
            if item.get("recipient_class", "") not in CLASSES:
                sys.exit(f"{f}: bad recipient_class {item.get('recipient_class')!r} for {rid}")
            row = by_id[rid]
            was = bool(row["parent"])
            for k in HAND:
                v = item.get(k)
                if v not in (None, ""):
                    row[k] = str(v).strip()
            if not was and row["parent"]:
                n_new += 1
    with PARENTS.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    done = sum(1 for r in rows if r["parent"])
    print(f"merged {len(files)} files: {n_new} newly researched; {done}/{len(rows)} rows have a parent")


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in ("batch", "merge"):
        sys.exit(__doc__)
    (cmd_batch if sys.argv[1] == "batch" else cmd_merge)(sys.argv[2:])
