#!/usr/bin/env python3
"""Apply the third independent tie-out (docs/TIEOUT_INDEPENDENT_3.md).

Its arithmetic check found nothing: 43 companies, $97,009,323, every category,
every band, every `paid` figure against Schedule I, zero differences. What it
found instead was that several rows are **labelled** more confidently than
their own evidence supports, and that the hedges which do exist are written in
`notes`, which the page does not render, while `caveat`, which it does render
on hover, is empty.

That matters more now than it would have last week. The piece is no longer a
story about these companies; it is the tool, handed to reporters. A hedge a
reader never meets is not a hedge.

What this changes:

  Ultium Cells, $50,000,000 and 51.5% of all the failure dollars, had an empty
    caveat. Its own notes say the cut is a layoff and not a closure, that the
    state notice breaks 1,300 into 484 permanent and 850 temporary, and that
    most of it has been reversed. The plant is open. All of that now shows.
  CoverMyMeds, $6,613,235, and Hyland, $2,500,001, carry "Mass layoff at the
    funded site" on company-wide job cuts whose Ohio share was never disclosed
    and for which Ohio holds no notice. They stay in the count, because the
    Ohio sites did contract and both notes say how we know, but the row now
    says the Ohio number does not exist.
  Speedway is recategorised. It read "Mass layoff at the funded site" while
    the explanation for its missing notice says the Enon cut was fewer than
    35 people, which is not a mass layoff and does not clear Ohio's own
    threshold. What is documented is the sale to 7-Eleven, so the row becomes
    Sold or absorbed and the Enon cuts move into the caveat.
  Republic Steel's caveat said the August 2023 date belongs to Canton. Grupo
    Simec's FY2025 annual report says the August 2023 cessation covered Lorain
    as well, and its FY2022 report shows $27,100,000 of construction in
    progress at Lorain to prepare a restart. The core finding stands, that the
    mill produced nothing from 2016 and the money was paid in FY2022, but the
    caveat cannot assert what the filing contradicts.

Usage: 40_apply_tieout3.py [--write]
"""
import csv, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FAILURES = ROOT / "data" / "failures.csv"

CAVEAT = {
    "ULTIUM CELLS":
        "Read this row with its size in mind: $50,000,000 is 51.5% of all the money in "
        "this panel. It is also a layoff and not a closure, and the plant is open. Ohio's "
        "notice breaks the cut into 484 permanent and 850 temporary, the company said "
        "temporary workers would be recalled, and most of the cut has since been "
        "reversed. The 484 is the firm figure. Without Ultium the panel is $47.0 million "
        "and the median failure is $462,500.",
    "COVERMYMEDS LLC":
        "The Ohio number does not exist. The 815-job cut was company-wide and the Ohio "
        "share was never broken out, and Ohio holds no layoff notice for CoverMyMeds or "
        "McKesson in any published year. What is documented in Ohio is that the company "
        "put part of its Franklinton headquarters up for sublease and closed its Arizona "
        "office. The row is kept on that basis and the site-level figure is unknown.",
    "HYLAND SOFTWARE INC":
        "The Ohio number does not exist. The 1,000-job cut was 20% of a global workforce "
        "and the Ohio share was never disclosed, and Ohio holds no layoff notice for "
        "Hyland in any published year. What is documented in Ohio is that it listed two "
        "of its Westlake buildings for sale in August 2023. The row is kept on that "
        "basis and the site-level figure is unknown.",
    "SPEEDWAY LLC":
        "Recategorised from a mass layoff, because no mass layoff is documented in Ohio. "
        "Marathon Petroleum sold Speedway to 7-Eleven for $21 billion in May 2021, the "
        "year of the last grant. 7-Eleven then cut fewer than 35 jobs at the Enon "
        "headquarters in October 2021 and cut more in July 2022 as part of about 880 "
        "corporate cuts, but the Enon figure for 2022 was never published and fewer than "
        "35 is below the 50 that would require a notice. The sale is the documented "
        "event; the Ohio job loss is real but unquantified.",
    "REPUBLIC STEEL INC":
        "The funded site is the Lorain mill and it produced no steel from 2016, six years "
        "before the money was paid in FY2022. Grupo Simec, Republic's parent, has "
        "reported Lorain at zero tons in every annual report since, and JobsOhio's own "
        "2023 suit pleads that 55 of the 125 promised jobs were created. Two things cut "
        "against a simple reading and both come from Simec's own filings: its FY2022 "
        "report shows $27,100,000 of construction in progress at Lorain to prepare a "
        "restart, so the company was presenting the mill as idle rather than finished; "
        "and its FY2025 report says the August 2023 cessation covered Lorain as well as "
        "Canton. Ohio's register holds no Lorain notice because the Lorain layoff was "
        "January 2016, four years before the register begins.",
    # Two more above $1m that the tie-out graded Medium on the site, where the
    # gap is small but a reporter should know it is there before ringing anyone.
    "SAREPTA THERAPEUTICS":
        "The site tie is close but not exact. The money was paid to 3435 Stelzer Road and "
        "the state notice names 4201 Easton Commons, about a mile apart in the same "
        "Columbus ZIP and the same gene therapy operation, and the affected job titles "
        "are research and vivarium roles consistent with the funded project. The 80 is "
        "firm: the position list attached to the notice runs to exactly 80 lines. The 80 "
        "was part of about 500 cuts company-wide after a safety setback.",
    "MORGAN TRUCK BODY LLC":
        "The weakest site tie among the confirmed failures. The notice is unambiguous, a "
        "permanent reduction of 110 at 600 E. Chestnut Street, Orrville, and the plant "
        "stayed open. What no document we could reach establishes is that the $1,000,000 "
        "paid for that street: it ties to a Wayne County project of the right vintage, "
        "and Orrville is Morgan's only Wayne County site, but the payment address is in "
        "New York. Worth confirming before relying on it.",
}
RECATEGORISE = {
    "SPEEDWAY LLC": ("Acquisition", "Sold or absorbed"),
}


def main(argv):
    rows = list(csv.DictReader(FAILURES.open()))
    changed = []
    for r in rows:
        n = r["name"]
        if n in RECATEGORISE and r["verdict"] == "Confirmed failure":
            ev, cat = RECATEGORISE[n]
            if (r["event"], r["category"]) != (ev, cat):
                changed.append((n, f"{r['event']}/{r['category']} -> {ev}/{cat}"))
                r["event"], r["category"] = ev, cat
        if n in CAVEAT and r["verdict"] == "Confirmed failure" and r["caveat"] != CAVEAT[n]:
            changed.append((n, "caveat written" if not r["caveat"] else "caveat rewritten"))
            r["caveat"] = CAVEAT[n]

    for n, what in changed:
        print(f"  {n[:26]:26s} {what}")
    missing = [r["name"] for r in rows
               if r["verdict"] == "Confirmed failure" and not r["caveat"]
               and int(r["paid"] or 0) >= 1_000_000]
    print(f"\n{len(changed)} changes")
    if missing:
        print(f"still uncaveated above $1m: {missing}")
    if "--write" not in argv:
        print("\n--dry-run by default; pass --write")
        return
    with FAILURES.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    print(f"\nwrote {FAILURES.relative_to(ROOT)}")


if __name__ == "__main__":
    main(sys.argv[1:])
