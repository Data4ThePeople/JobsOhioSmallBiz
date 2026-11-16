#!/usr/bin/env python3
"""An acquisition is only a failure if the funded operation stopped.

The count carried a category called "Sold or absorbed": four companies and
$2,500,000, every one of them bought or divested rather than closed. Eric
Pachman set the rule on November 16, 2026: if a company is acquired and keeps
operating, that is not a failure; if it is acquired and shut down, it is.

Checked against that rule, all four fall out, and the category goes with them.

  SPEEDWAY LLC            $1,700,000  7-Eleven bought Speedway in May 2021 and
                                      cut Enon headquarters staff in October
                                      2021 (fewer than 35) and again in July
                                      2022. No source records the Enon campus
                                      closing. Reduced is not closed.
  FirstMerit Corporation    $500,000  Merged into Huntington in August 2016.
                                      Huntington kept the Akron headquarters
                                      operation and said in 2018 it would add
                                      jobs there.
  AK STEEL CORPORATION      $250,000  Cleveland-Cliffs bought AK Steel in March
                                      2020 and still runs its Ohio plants. The
                                      job losses in the coverage were in
                                      Kentucky and Michigan.
  PPG INDUSTRIES INC         $50,000  Sold its silicas business to Qemetica in
                                      November 2024. The Barberton plant kept
                                      running under the new owner.

They are not deleted. Each becomes verdict "Not a failure" with the reason on
the row, which puts it in the tool's rejected-candidates view where a reader
can see what was taken out and why. That is the same treatment every other
rejected candidate gets.

Failures go from 44 companies and $97,709,323 to 40 and $95,209,323.

Idempotent: run it twice and the second run reports nothing to do.

Usage: 46_apply_acquired_rule.py
"""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FAILURES = ROOT / "data" / "failures.csv"

RULE = ("Acquired or divested, and the funded operation kept running. An "
        "acquisition counts as a failure here only when the funded site "
        "stopped. ")

WHY = {
    "SPEEDWAY LLC":
        "7-Eleven bought Speedway from Marathon Petroleum in May 2021 and cut "
        "fewer than 35 jobs at the Enon headquarters in October 2021, then cut "
        "more Enon staff in July 2022 as part of about 880 corporate cuts. No "
        "source records the Enon campus closing, and the 2022 Enon figure was "
        "never published. A headquarters that shrank is not a headquarters "
        "that shut.",
    "FirstMerit Corporation":
        "FirstMerit stopped existing as an Akron company when it merged into "
        "Huntington on August 16, 2016, but Huntington kept the Akron "
        "headquarters operation and said in 2018 it would add jobs there. "
        "FirstMerit appears in no JobsOhio project report, so what the "
        "$500,000 funded is unknown, and there is no funded site to call "
        "closed.",
    "AK STEEL CORPORATION":
        "Cleveland-Cliffs completed its purchase of AK Steel on March 13, "
        "2020. It still runs AK Steel's Ohio plants, and the job losses in "
        "the coverage were in Kentucky and Michigan. The funded site is the "
        "Research and Innovation Center on Research Way in Middletown; the "
        "West Chester address on Schedule I is the head office the cheque "
        "went to.",
    "PPG INDUSTRIES INC":
        "PPG sold its silicas products business to Qemetica in November 2024 "
        "and the Barberton plant kept running under the new owner. PPG's own "
        "10-K does not tie Barberton to the silicas sale; the Ohio link rests "
        "on Qemetica's site list.",
}


def main():
    rows = list(csv.DictReader(FAILURES.open()))
    before = [r for r in rows if r["verdict"] == "Confirmed failure"]
    changed = []
    for r in rows:
        if r["verdict"] != "Confirmed failure" or r["category"] != "Sold or absorbed":
            continue
        why = WHY.get(r["name"])
        if not why:
            raise SystemExit(f"no reason written for {r['name']}; refusing to "
                             "drop a row without saying why")
        r["verdict"] = "Not a failure"
        r["category"] = ""
        r["ohio_outcome"] = RULE + why
        r["caveat"] = ""
        changed.append(r)

    if not changed:
        print("nothing to do: no 'Sold or absorbed' rows are still counted as "
              "failures")
        return

    with FAILURES.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    after = [r for r in rows if r["verdict"] == "Confirmed failure"]
    print(f"moved {len(changed)} rows out of the failure count:")
    for r in changed:
        print(f"  {r['name'][:28]:28s} ${int(r['paid']):>10,}")
    print(f"\nfailures {len(before)} -> {len(after)} companies, "
          f"${sum(int(r['paid']) for r in before):,} -> "
          f"${sum(int(r['paid']) for r in after):,}")
    print(f"wrote {FAILURES.relative_to(ROOT)}")
    print("\nnow rerun 09_analyze.py and scripts/build.py")


if __name__ == "__main__":
    main()
