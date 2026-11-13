#!/usr/bin/env python3
"""Work out what JobsOhio actually got back through the courts, case by case.

`amount_recovered` in data/jobsohio_lawsuits.csv is prose, because that is what
the dockets give: mostly "no filing states any amount", sometimes "the judgment
of $X was recorded as satisfied". Pulling a dollar sign out of that text is
wrong, and wrong in a way that inflates the answer. Olive AI has two cases, and
the second one's field reads "Not stated in this case. The related $598,420.17
judgment in 23CV005498 was recorded as fully satisfied" — a naive sum counts
that $598,420 twice and reports $3,827,576 where the truth is $3,229,156.

So a sum is read only when the text is about THIS case: a dollar figure that
sits in the same sentence as another case number is a cross-reference and is
skipped. RM Biltrite genuinely has two satisfied judgments, $587,832.20 and
$125,000, and both are kept, which is the check that the rule is not too tight.

**What the number means, and the post has to say this.** A judgment "satisfied
and released" is discharged; it is not a receipt. Most of these notes add that
no filing states the sum actually paid, so this is the value of judgments
JobsOhio recorded as settled, not cash in the door. It is an upper bound.

Writes the `recovered_usd` and `recovered_basis` columns back to
data/jobsohio_lawsuits.csv and prints the reconciliation.

Usage: 36_recovered.py [--write]
"""
import csv, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LAWSUITS = ROOT / "data" / "jobsohio_lawsuits.csv"
CASE = re.compile(r"\b\d{2}CV\d{6}\b")
MONEY = re.compile(r"\$\s*([\d,]+(?:\.\d{2})?)")


def recovered(row):
    """(amount, why) for this case alone."""
    text = (row.get("amount_recovered") or "").strip()
    if not text:
        return 0.0, "nothing recorded"
    for sentence in re.split(r"(?<=[.;])\s+", text):
        m = MONEY.search(sentence)
        if not m:
            continue
        others = [c for c in CASE.findall(sentence) if c != row.get("case")]
        if others:
            # the sum belongs to a different case that this note points at
            continue
        return float(m.group(1).replace(",", "")), "a sum stated for this case"
    if MONEY.search(text):
        return 0.0, "the only sum stated belongs to another case"
    return 0.0, "no sum stated"


def main(argv):
    rows = list(csv.DictReader(LAWSUITS.open()))
    suits = [r for r in rows if r["kind"] == "suit"]

    naive = 0.0
    for r in suits:
        m = MONEY.search(r.get("amount_recovered") or "")
        if m:
            naive += float(m.group(1).replace(",", ""))

    total, got = 0.0, []
    for r in rows:
        amt, why = recovered(r) if r["kind"] == "suit" else (0.0, "")
        r["recovered_usd"] = f"{amt:.2f}" if amt else ""
        r["recovered_basis"] = why
        if amt:
            total += amt
            got.append((amt, r["case"], r["defendant"]))

    sought = 0.0
    for r in suits:
        m = MONEY.search(r.get("amount_sought") or "")
        if m:
            sought += float(m.group(1).replace(",", ""))

    got.sort(reverse=True)
    print(f"{len(got)} of {len(suits)} suits have a sum recorded for themselves\n")
    for amt, case, d in got:
        print(f"  ${amt:>12,.2f}  {case:<12s} {d[:40]}")
    print(f"\n  pleaded across all {len(suits)} suits : ${sought:>14,.2f}")
    print(f"  judgments recorded as satisfied : ${total:>14,.2f}  "
          f"({total/sought:.1%} of what was pleaded)")
    print(f"  a naive regex over the column   : ${naive:>14,.2f}  "
          f"(overstates by ${naive-total:,.2f}: Olive AI's judgment counted twice)")
    skipped = [r["case"] for r in suits
               if r["recovered_basis"] == "the only sum stated belongs to another case"]
    if skipped:
        print(f"  cross-references skipped        : {', '.join(skipped)}")
    print("\nThis is the value of judgments recorded as satisfied, NOT cash received.\n"
          "Most of these dockets say in terms that no filing states the sum actually\n"
          "paid, so treat it as an upper bound and say so wherever it is published.")

    if "--write" not in argv:
        print("\n(not written; pass --write)")
        return
    with LAWSUITS.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    print(f"\nwrote {LAWSUITS.relative_to(ROOT)}")


if __name__ == "__main__":
    main(sys.argv[1:])
