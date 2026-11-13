#!/usr/bin/env python3
"""Apply the gap-closing research to data/failures.csv and sitecheck.json.

Nine open questions went to a research pass (data/research3/gaps.json). Eight
came back resolved, and five of those contradict what this project currently
says. Those corrections are applied here, each one off a primary record.

The biggest is Republic Steel, and it changes the finding rather than
sharpening it. The project said the Lorain mill was shuttered at some date it
could not establish. Grupo Simec, Republic's parent, has told the SEC the
answer every year since 2016: the Lorain furnace was idled in June 2015, the
whole facility on 31 March 2016, and every 20-F from FY2018 to FY2024 repeats
that it "did not produce any steel billets or finished steel bars" and books
Lorain at zero tons. The EPA agrees twice, through greenhouse-gas reporting
that stops after 2015 and toxics-release forms showing a production ratio of
zero. **So JobsOhio signed a workforce-training agreement effective 4 September
2018, committed $500,000 in February 2019 to train 85 workers and create 125
jobs, and paid it in FY2022, at a mill its parent had told the SEC made no
steel after 2015.** The missing Lorain WARN notice is explained by the same
fact: the Lorain layoff was January 2016, before Ohio's register begins.

The others:
  AK Steel's county was never a mismatch. The funded project is the Research
    and Innovation Center at 6180 Research Way, Middletown, in Warren County,
    and AK Steel's own SEC-filed release thanks the Warren County Port
    Authority and counts the 75 researchers JobsOhio recorded as retained. The
    West Chester address is a remit-to. Confidence goes up.
  Battelle was not AmplifyBio's prepetition secured lender. Hercules Capital
    was, for $28,071,890.43, and assigned the loan to Battelle on 14 April
    2025, two weeks after the layoffs.
  Multi-Color was taken private by CD&R in 2021, not 2019. The 2019 deal was
    the W/S Packaging merger.
  Goodlevel Enterprises is The Maple City Rubber Company of Norwalk and is
    trading, with Form 5500 participants rising from 73 to 77. It stops being
    Unresolved and becomes Not a failure. The Canadian insolvency is a separate
    Ontario balloon subsidiary, and the Ohio company is its largest creditor.

Usage: 38_apply_gaps.py [--write]
"""
import csv, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FAILURES = ROOT / "data" / "failures.csv"
SITECHECK = ROOT / "data" / "research3" / "sitecheck.json"

OUTCOME = {
    "REPUBLIC STEEL INC":
        "The funded Lorain mill has made no steel since 2015. Grupo Simec, Republic's "
        "parent, told the SEC that the new electric arc furnace was idled in June 2015 "
        "and the whole Lorain facility on 31 March 2016, took a $130.7 million "
        "impairment on the melt shop, and has reported Lorain at zero tons in every "
        "annual report since. EPA greenhouse-gas reporting for the site stops after "
        "2015 and its toxics-release forms show a production ratio of zero. JobsOhio "
        "signed the grant agreement on 4 September 2018, committed $500,000 in "
        "February 2019 to train 85 workers and create 125 jobs there, and paid it in "
        "FY2022. Its own 2023 suit pleads that 55 of the 125 jobs were created. "
        "Separately, Republic idled its Canton mill on 10 August 2023; that is a "
        "different site and Ohio did not fund it.",
}
CAVEAT = {
    "REPUBLIC STEEL INC":
        "The funded site is the Lorain mill and it has been idle since 2016, before "
        "the money was paid. The 209 jobs and the August 2023 date that appeared on "
        "this row are the Canton mill, a different site Ohio did not fund, and Ohio's "
        "WARN register has no Lorain notice because the Lorain layoff was January "
        "2016, four years before the register begins. One unresolved wrinkle: Simec's "
        "most recent filings say Lorain 'ceased operations in August 2023', which "
        "contradicts nine earlier filings and its own zero-tonnage tables.",
    "AK STEEL CORPORATION":
        "A sale, not an insolvency: Cleveland-Cliffs still runs AK Steel's Ohio "
        "plants, and the job losses in the coverage were in Kentucky and Michigan. "
        "The funded site is the Research and Innovation Center at 6180 Research Way, "
        "Middletown, in Warren County; the West Chester address on Schedule I is the "
        "head office the cheque went to.",
}
EVENT = {"REPUBLIC STEEL INC": ("Closure", "Funded site closed", "2016-03-31")}
CONFIDENCE = {"AK STEEL CORPORATION": "Medium", "REPUBLIC STEEL INC": "High"}
VERDICT = {"Goodlevel Enterprises LLC": "Not a failure"}
GOODLEVEL = ("Not a failure. Goodlevel Enterprises LLC is The Maple City Rubber Company "
             "of Norwalk, confirmed through its own Form 5500 filings, and it is "
             "trading: its 2025 return, received 19 July 2026, is non-final with active "
             "participants rising from 73 to 77, which corroborates the 74 retained in "
             "JobsOhio's February 2026 report. The Canadian insolvency that flagged it "
             "is a separate Hamilton, Ontario latex-balloon subsidiary, and the Ohio "
             "company is that estate's largest creditor at about $3.3 million.")
# AK Steel's site verdict rested on a county mismatch that turns out not to
# exist, so the grade it was given for that reason goes up.
SITE_CONFIDENCE = {"EIN:311267098": "Medium"}
SITE_FIX = {
    "EIN:311267098": (  # AK Steel
        "The county mismatch is resolved and was never a mismatch. The funded project "
        "is the Research and Innovation Center, 6180 Research Way, Middletown, in "
        "WARREN County, which is where JobsOhio put it. AK Steel's own SEC-filed "
        "release of 23 February 2015 thanks the Warren County Port Authority and "
        "JobsOhio and says the building houses about 75 researchers, scientists and "
        "engineers, matching the 75 retained in JobsOhio's record exactly. Confirmed "
        "against Warren County Port Authority minutes and the county auditor's parcel "
        "layer. The West Chester address on Schedule I is the head office the cheque "
        "went to. Still unexplained: JobsOhio records $4.7 million of investment "
        "against a project reported at $36 million."),
    "EIN:862301671": (  # AmplifyBio
        "Battelle was NOT the prepetition secured lender. The chief restructuring "
        "officer's declaration names Hercules Capital, Inc., owed $28,071,890.43, and "
        "says Hercules assigned the loan to Battelle on 14 April 2025, two weeks after "
        "the layoffs and a month before the filing. The funded project spans Licking "
        "and Madison counties and BOTH were built: the Licking site is 9885 Innovation "
        "Campus Way, New Albany, in Jersey Township, 351,846 square feet, built 2022. "
        "The federal complaint in Freeman v. AmplifyBio says about 200 employees were "
        "terminated on or around 4 April 2025 in a total closure of both facilities. "
        "Ohio's WARN register books Madison at 212 and Licking at zero."),
    "EIN:311125853": (  # Multi-Color
        "CD&R acquired Multi-Color in 2021, not 2019; the 2019 take-private was the W/S "
        "Packaging merger. The funded Batavia plant is still running on documents "
        "rather than on the absence of a notice: EPA air source OH0000001413020513 is "
        "Operating with twelve consecutive quarters of compliance reporting through Q4 "
        "2026, the Clermont County parcel is still owned by MCC Manufacturing Inc, and "
        "the company's own site still lists Batavia while Norwood has been removed."),
}


def main(argv):
    rows = list(csv.DictReader(FAILURES.open()))
    changed = []
    for r in rows:
        n = r["name"]
        if n in OUTCOME:
            r["ohio_outcome"] = OUTCOME[n]; changed.append((n, "outcome rewritten"))
        if n in EVENT:
            r["event"], r["category"], r["event_date"] = EVENT[n]
            changed.append((n, f"event -> {EVENT[n][0]}, dated {EVENT[n][2]}"))
        if n in CAVEAT:
            r["caveat"] = CAVEAT[n]; changed.append((n, "caveat rewritten"))
        if n in CONFIDENCE and r["confidence"] != CONFIDENCE[n]:
            changed.append((n, f"confidence {r['confidence']} -> {CONFIDENCE[n]}"))
            r["confidence"] = CONFIDENCE[n]
        if n.upper().startswith("GOODLEVEL"):
            r["verdict"] = "Not a failure"
            r["ohio_outcome"] = GOODLEVEL
            changed.append((n, "Unresolved -> Not a failure"))

    site = json.loads(SITECHECK.read_text())
    for x in site:
        want = SITE_CONFIDENCE.get(x["recipient_id"])
        if want and x.get("confidence") != want:
            changed.append((x["name"], f"site confidence {x.get('confidence')} -> {want}"))
            x["confidence"] = want
        extra = SITE_FIX.get(x["recipient_id"])
        if extra and extra not in (x.get("notes") or ""):
            base = (x.get("notes") or "").split("CORRECTED 2026-11-13:")[0].strip()
            x["notes"] = f"{base} CORRECTED 2026-11-13: {extra}"
            changed.append((x["name"], "site note corrected"))

    for n, what in changed:
        print(f"  {n[:34]:34s} {what}")
    print(f"\n{len(changed)} corrections")
    if "--write" not in argv:
        print("\n--dry-run by default; pass --write")
        return
    with FAILURES.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    SITECHECK.write_text(json.dumps(site, indent=1))
    print(f"\nwrote {FAILURES.relative_to(ROOT)} and {SITECHECK.relative_to(ROOT)}")


if __name__ == "__main__":
    main(sys.argv[1:])
