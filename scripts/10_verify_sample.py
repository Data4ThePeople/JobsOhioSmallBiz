#!/usr/bin/env python3
"""Independent re-check of a random sample of researched recipients.

  10_verify_sample.py draw [--n 150] [--max 1000000] [--seed 20260918]
      Draw a seeded random sample of researched recipients with total_cash
      under --max (the tiers Eric does not review by hand) and write
      data/research/verify_input.json with the same signal fields the first
      pass saw, but none of its answers.

  10_verify_sample.py compare data/research/verify_*.json
      Compare the second pass's emp_bucket, parent_hq_state and
      recipient_class with the first pass in data/parents.csv. Prints the
      disagreement rate for each field and for the small/large call at the
      500 cutoff, and writes data/verify_report.csv with every disagreement
      for hand adjudication."""
import csv, json, random, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PARENTS = ROOT / "data" / "parents.csv"
OUT = ROOT / "data" / "research" / "verify_input.json"
REPORT = ROOT / "data" / "verify_report.csv"
SIGNALS = ["recipient_id", "name", "ein", "city", "state", "irc_section", "total_cash", "years",
           "recipient_class_auto", "edgar_name", "edgar_state_inc", "edgar_hq_state",
           "f5500_participants_2015", "f5500_participants_2019", "f5500_participants_2023", "f5500_sponsor",
           "metrics_company", "metrics_programs", "metrics_jobs_retained_max", "metrics_industry", "metrics_commit_total"]
SMALL = {"<100", "100-499"}


def draw(args):
    n = int(args[args.index("--n") + 1]) if "--n" in args else 150
    hi = int(args[args.index("--max") + 1]) if "--max" in args else 1_000_000
    seed = int(args[args.index("--seed") + 1]) if "--seed" in args else 20260918
    rows = [r for r in csv.DictReader(PARENTS.open()) if r["parent"] and int(r["total_cash"]) < hi]
    random.Random(seed).shuffle(rows)
    sample = rows[:n]
    OUT.write_text(json.dumps([{k: r[k] for k in SIGNALS} for r in sample], indent=1))
    print(f"wrote {OUT.relative_to(ROOT)}: {len(sample)} of {len(rows)} researched recipients under ${hi:,} (seed {seed})")


def compare(files):
    first = {r["recipient_id"]: r for r in csv.DictReader(PARENTS.open())}
    second = [x for f in files for x in json.load(open(f))]
    fields = ["emp_bucket", "parent_hq_state", "recipient_class"]
    dis = {f: 0 for f in fields}; dis["size_call"] = 0; n = 0
    report = []
    for s in second:
        a = first.get(s["recipient_id"])
        if not a or not a["parent"]:
            continue
        n += 1
        row = {"recipient_id": s["recipient_id"], "name": a["name"], "total_cash": a["total_cash"],
               "first_rule": a["notes"][:7] if a["notes"].startswith("Rule") else "research"}
        for f in fields:
            row[f"first_{f}"], row[f"second_{f}"] = a[f], s.get(f, "")
            # a government or nonprofit row with no size recorded is not a size disagreement
            if f == "emp_bucket" and not a[f] and (a["recipient_class"] or a["recipient_class_auto"]) != "business":
                row[f"second_{f}"] = a[f]
                continue
            if (a[f] or "").strip().lower() != (s.get(f, "") or "").strip().lower():
                dis[f] += 1
        c1 = "small" if a["emp_bucket"] in SMALL else ("large" if a["emp_bucket"] else "unknown")
        c2 = "small" if row["second_emp_bucket"] in SMALL else ("large" if row["second_emp_bucket"] else "unknown")
        row["first_size"], row["second_size"] = c1, c2
        if c1 != c2:
            dis["size_call"] += 1
        row["second_parent"], row["second_notes"] = s.get("parent", ""), s.get("notes", "")
        if any(row[f"first_{f}"].strip().lower() != row[f"second_{f}"].strip().lower() for f in fields):
            report.append(row)
    with REPORT.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(report[0]) if report else ["recipient_id"]); w.writeheader(); w.writerows(report)
    print(f"compared {n} recipients")
    from collections import Counter
    print("  size-call disagreements by first-pass method:", dict(Counter(r["first_rule"] for r in report if r["first_size"] != r["second_size"])))
    print("  sample by first-pass method:", dict(Counter((first[x["recipient_id"]]["notes"][:7] if first[x["recipient_id"]]["notes"].startswith("Rule") else "research") for x in second if x["recipient_id"] in first)))
    for k, v in dis.items():
        print(f"  {k:18s} disagree {v:3d}  ({v / n:.1%})")
    print(f"wrote {REPORT.relative_to(ROOT)}: {len(report)} rows with any disagreement, for adjudication")


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in ("draw", "compare"):
        sys.exit(__doc__)
    (draw if sys.argv[1] == "draw" else compare)(sys.argv[2:])
