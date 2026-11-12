#!/usr/bin/env python3
"""Audit every number shown in the summary panel, from the raw files.

These five tiles are the figures a reader will quote and a press office will
attack, so each one is recomputed here from the file it should come from,
independently of `09_analyze.py`, and compared to what `dist/data.json`
actually carries. Any mismatch is a hard failure.

The specific trap this guards against: a failure is verified against the
**payee** named on Schedule I, while the table groups by **parent**. Rolling
the payees up loses companies that share a parent and sweeps in that parent's
other payees. At the time of writing that turns 29 companies and $86,537,093
into 26 and $96,452,820. The panel must use the payee figures.

Usage: 30_audit_summary.py
"""
import csv, json, re, statistics, sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from names import normalize_name

DATA = ROOT / "dist" / "data.json"
FAILURES = ROOT / "data" / "failures.csv"
LAWSUITS = ROOT / "data" / "jobsohio_lawsuits.csv"
GRANTS = ROOT / "data" / "grants_raw.csv"
PARENTS = ROOT / "data" / "parents.csv"

checks, bad = [], []


def check(name, got, want, note=""):
    ok = got == want
    checks.append((ok, name, got, want, note))
    if not ok:
        bad.append((name, got, want, note))


def main():
    S = json.loads(DATA.read_text())["summary"]
    fails = [r for r in csv.DictReader(FAILURES.open()) if r["verdict"] == "Confirmed failure"]
    suits = [r for r in csv.DictReader(LAWSUITS.open()) if r["kind"] == "suit"]
    grants = list(csv.DictReader(GRANTS.open()))
    parents = {r["recipient_id"]: r for r in csv.DictReader(PARENTS.open())}
    by_name = {normalize_name(r["name"]): r for r in parents.values()}

    # --- the suits tile -----------------------------------------------------
    sought = []
    for r in suits:
        h = re.search(r"\$\s*([\d,]+(?:\.\d{2})?)", r["amount_sought"] or "")
        if h:
            sought.append(float(h.group(1).replace(",", "")))
    check("suits filed", S["sued"]["suits"], len(suits))
    check("total sought", S["sued"]["sought"], round(sum(sought)))
    check("median sought", S["sued"]["median_sought"], round(statistics.median(sought)))
    check("every suit has a pleaded sum", len(sought), len(suits),
          "a suit with no amount would silently drop out of the median")

    sued_recs = [by_name[normalize_name(r["recipient"])] for r in suits
                 if r.get("recipient") and normalize_name(r["recipient"]) in by_name]
    check("suits tied to a recipient", S["sued"]["recipients_matched"], len(sued_recs))
    sc = [int(r["total_cash"] or 0) for r in sued_recs]
    check("paid to the sued", S["sued"]["paid_to_them"], sum(sc))
    check("mean paid to the sued", S["sued"]["mean_paid"], round(statistics.mean(sc)))

    # --- the failure tiles --------------------------------------------------
    cat = defaultdict(lambda: [0, 0])
    for r in fails:
        cat[r["category"]][0] += 1
        cat[r["category"]][1] += int(r["paid"] or 0)
    check("failure companies", S["failures"]["companies"], len(fails))
    check("failure dollars", S["failures"]["paid"], sum(int(r["paid"] or 0) for r in fails))
    for k, (n, c) in cat.items():
        shown = S["failures"]["by_category"].get(k, {})
        check(f"{k}: companies", shown.get("companies"), n)
        check(f"{k}: dollars", shown.get("paid"), c)
    check("categories sum to the total",
          sum(v["paid"] for v in S["failures"]["by_category"].values()), S["failures"]["paid"],
          "a company in two categories would break this")
    check("no company counted twice", len({r["name"] for r in fails}), len(fails))
    check("every failure carries a join key",
          sum(1 for r in fails if r.get("recipient_id")), len(fails),
          "without recipient_id the join falls back to the name, and two "
          "Speedway LLCs with different EINs collapse onto one another")

    # the payee figure must tie to parents.csv, not to the parent rollup
    mismatch = [r["name"] for r in fails
                if r.get("recipient_id") in parents
                and int(r["paid"] or 0) != int(parents[r["recipient_id"]]["total_cash"] or 0)]
    check("each failure's paid ties to parents.csv", len(mismatch), 0,
          f"first few: {mismatch[:3]}" if mismatch else "")

    # --- the returned tile --------------------------------------------------
    neg = sum(int(g["cash_amt"]) for g in grants if int(g["cash_amt"]) < 0)
    pos = sum(int(g["cash_amt"]) for g in grants if int(g["cash_amt"]) > 0)
    check("dollars returned", S["returned"]["dollars"], abs(neg))
    check("returned as a share of what went out",
          round(S["returned"]["share_of_paid"], 6), round(abs(neg) / pos, 6),
          "the denominator is positive payments, not the net total")

    # --- the size-contrast sentence ----------------------------------------
    fail_recs = [parents[r["recipient_id"]] for r in fails if r.get("recipient_id") in parents]
    for label, rows, shown in (("sued", sued_recs, S["sued"]["bands"]),
                               ("failed", fail_recs, S["failures"]["bands"])):
        c = Counter(r["emp_bucket"] or "unresolved" for r in rows)
        check(f"{label}: band mix", dict(shown), {k: v for k, v in c.items() if v})
    check("no failure is in the under-100 band",
          S["failures"]["bands"].get("<100", 0), 0,
          "the sentence on the page says none employs fewer than 100")

    # --- report -------------------------------------------------------------
    for ok, name, got, want, note in checks:
        mark = "ok  " if ok else "FAIL"
        line = f"  {mark} {name:44s} {got!r:>18}"
        if not ok:
            line += f"  expected {want!r}"
        if note and not ok:
            line += f"\n       {note}"
        print(line)
    print(f"\n{sum(1 for c in checks if c[0])} of {len(checks)} checks pass")
    if bad:
        sys.exit(f"{len(bad)} summary figures do not tie to their source files")
    print("every figure in the summary panel ties to the file it was verified against")


if __name__ == "__main__":
    main()
