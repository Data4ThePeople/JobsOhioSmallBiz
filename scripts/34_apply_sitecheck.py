#!/usr/bin/env python3
"""Apply the funded-site check to data/failures.csv.

Every one of the 31 confirmed failures was re-checked on a single question: is
the operation that failed the operation the grant paid for? It is the question a
press office asks first, and three answers came back no.

  Dana Limited, $3,700,000.  Funded: a Lucas County project and a Henry County
    project, both paid to Maumee. Failed: the Lima plant in Allen County. The
    $3,700,000 paid is exactly JobsOhio's two commitments, $3,000,000 and
    $700,000, so no paid dollar can belong to Lima, and the closing entity is a
    different company, Dana Driveshaft Manufacturing LLC.
  New Horizons Baking, $100,000.  Funded: the Norwalk plant in Huron County,
    the only payment on Schedule I, matching a 2017 Huron County workforce
    grant of the same amount. Failed: the north Toledo plant. JobsOhio did
    commit $75,000 to Toledo in 2023, but Schedule I shows nothing paid on it.
  FedEx Supply Chain, $50,000.  Funded: Columbus, Franklin County, matching
    JobsOhio's 2016 grant of the same $50,000 to GENCO I, the company FedEx
    bought and renamed. Failed: the Lima distribution center in Allen County.

Those three are not dropped and not hidden. They keep a row and a verdict of
their own, because "the company failed somewhere else in Ohio" is true, is
interesting, and is not the same claim as "the site Ohio paid for failed". What
they stop doing is counting toward the closure and layoff dollars, which takes
the headline from 31 companies and $90,737,093 to 28 and $86,887,093.

Four more came back `partly`: a distinguishable piece of the funded operation
survived, which weakens the dollar attribution without undoing the finding.
Those keep their place in the count and gain a caveat saying what survived.

Idempotent: each row's caveat is rewritten rather than appended to, so running
this twice leaves the file identical.

Usage: 34_apply_sitecheck.py [--dry-run]
"""
import csv, json, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FAILURES = ROOT / "data" / "failures.csv"
SITECHECK = ROOT / "data" / "research3" / "sitecheck.json"
ELSEWHERE = "Failed away from the funded site"

# One caveat per row, written by hand rather than sliced out of the research
# notes, because this is the sentence a reader sees next to the money.
CAVEAT = {
    "DANA LIMITED":
        "The $3,700,000 paid for two projects in Lucas and Henry counties, both to "
        "Maumee. The plant that closed is in Lima, Allen County, and belongs to a "
        "different Dana company. The funded sites are still running.",
    "NEW HORIZONS BAKING COMPANY INC":
        "The $100,000 paid for the Norwalk plant in Huron County, which is still "
        "running. The plant that closed is in Toledo. JobsOhio committed $75,000 to "
        "Toledo in 2023, but no payment on it appears on Schedule I.",
    "FedEx Supply Chain Inc":
        "The $50,000 paid for a Columbus operation in Franklin County. The center that "
        "closed is in Lima, Allen County. No Columbus closure for this payee appears in "
        "Ohio's notices for 2020 through 2026.",
    "NESTLE USA INC":
        "The Solon factory is closing; the Solon research centre and Nestle's corporate "
        "operations there stay. JobsOhio's own project credits 1,251 jobs retained on "
        "$3,300,000 of investment at the campus address, which reads like the part that "
        "is staying, so it is possible little of the $3,200,000 paid for the factory.",
    "MULTI-COLOR CORPORATION":
        "No Ohio site failed. This was a prepackaged balance-sheet Chapter 11 of the "
        "payee itself, completed in May 2026, and the funded Batavia operation came "
        "through it. The company did close Norwood and Mason in 2023, neither of them "
        "the funded site.",
    "FirstMerit Corporation":
        "A sale, not an insolvency: the Akron bank ceased to exist when it merged into "
        "Huntington, which kept the Akron headquarters operation and said in 2018 it "
        "would add jobs there. FirstMerit appears in no JobsOhio project report, so what "
        "the $500,000 funded is unknown.",
    "AK STEEL CORPORATION":
        "A sale, not an insolvency: Cleveland-Cliffs still runs AK Steel's Ohio plants, "
        "and the job losses in the coverage were in Kentucky and Michigan. The funded "
        "site is unresolved, since JobsOhio puts the project in Warren County while the "
        "payment went to West Chester in Butler County.",
    # Republic Steel stays a confirmed, same-site failure: the funded Lorain mill
    # really is shuttered. But the dated event on the row came from the Canton
    # mill's notice, which is a different and unfunded site, so the row has to say
    # which number belongs to which mill.
    "REPUBLIC STEEL INC":
        "The funded site is the Lorain mill, and it is shuttered and empty. The 209 "
        "figure and the August 2023 date on this row are the Canton mill, a different "
        "site Ohio did not fund. Lorain's idling has no state notice and no date we "
        "could establish. JobsOhio's own 2023 suit pleads that 55 of 125 promised jobs "
        "were created at the Lorain project site.",
}


def main(argv):
    dry = "--dry-run" in argv
    rows = list(csv.DictReader(FAILURES.open()))
    by_id = {r["recipient_id"]: r for r in rows}
    checks = {x["recipient_id"]: x for x in json.loads(SITECHECK.read_text())}

    print(f"{len(checks)} site checks: "
          + ", ".join(f"{k} {v}" for k, v in
                      Counter(x["verdict"] for x in checks.values()).most_common()))

    missing = [r["name"] for r in rows
               if r["verdict"] == "Confirmed failure" and r["recipient_id"] not in checks]
    if missing:
        sys.exit(f"not site-checked, so this cannot be applied safely: {missing}")

    moved, caveated, before_n, before_c = [], [], 0, 0
    for r in rows:
        if r["verdict"] not in ("Confirmed failure", ELSEWHERE):
            continue
        before_n += r["verdict"] == "Confirmed failure"
        before_c += int(r["paid"] or 0) if r["verdict"] == "Confirmed failure" else 0
        x = checks.get(r["recipient_id"])
        if not x:
            continue
        want = CAVEAT.get(r["name"], "")
        if x["verdict"] == "different site":
            r["verdict"] = ELSEWHERE
            r["category"] = ELSEWHERE
            if not want:
                sys.exit(f"{r['name']}: moved off the count with no caveat written")
            moved.append(r)
        if want:
            r["caveat"] = want
            caveated.append(r["name"])

    now = [r for r in rows if r["verdict"] == "Confirmed failure"]
    print(f"\nmoved off the failure count: {len(moved)}")
    for r in moved:
        print(f"  ${int(r['paid'] or 0):>10,}  {r['name']}")
    print(f"\ncaveats written: {len(caveated)}")
    for n in caveated:
        print(f"  {n}")
    print(f"\nconfirmed failures: {before_n} -> {len(now)}")
    print(f"confirmed dollars : ${before_c:,} -> ${sum(int(r['paid'] or 0) for r in now):,}")

    if dry:
        print("\n--dry-run: nothing written")
        return
    with FAILURES.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    print(f"\nwrote {FAILURES.relative_to(ROOT)}")


if __name__ == "__main__":
    main(sys.argv[1:])
