#!/usr/bin/env python3
"""Label every Schedule I payment with the conditions published for the
program that paid it, and with whether JobsOhio ever took money back from
that recipient.

Two columns of evidence:

  conditions   from data/program_terms.json, the terms JobsOhio publishes for
               the program: Conditional (reimbursement, stated performance
               metrics and a written clawback), Partly conditional
               (reimbursement or metrics, no clawback published), Unknown
               (nothing published), or Program unknown when the payment
               cannot be tied to a program at all.
  clawback_seen  whether this recipient has a negative row on any Schedule I,
               which is JobsOhio recording money returned.

The program comes from JobsOhio's own monthly project reports, matched to the
recipient by name in 04_normalize.py. A quarter of recipients never appear in
those reports, and the air-service grants appear in none of them, so those are
labelled from the payee where it is an airline and left as Program unknown
otherwise. Writes data/grant_conditions.csv and prints the dollar split.
"""
import csv, json, re, sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from names import normalize_name

GRANTS = ROOT / "data" / "grants_raw.csv"
LAWSUITS = ROOT / "data" / "jobsohio_lawsuits.csv"
PARENTS = ROOT / "data" / "parents.csv"
TERMS = ROOT / "data" / "program_terms.json"
OUT = ROOT / "data" / "grant_conditions.csv"

AIRLINES = ("breeze", "aer lingus", "british airways", "united airlines", "avelo",
            "alaska airlines", "air wisconsin", "spirit airlines", "allegiant")
# program_terms.json names -> the family names used in the project reports
ALIAS = {
    "Economic Development Grant": ["Economic Development Grant"],
    "Workforce Grant": ["Workforce Grant"],
    "Revitalization Grant": ["Revitalization Grant", "Revitalization Grant Phase II"],
    "Revitalization Loan": ["Revitalization Loan"],
    "Research & Development Center Grant": ["Research & Development Grant"],
    "Inclusion Grant / Small Business Grant": ["Inclusion Grant"],
    "Ohio Site Inventory Program (OSIP / Spec Development)": ["Spec Development (OSIP)"],
    "Commercial Air Service Restoration": ["Air Service Restoration"],
    "Growth Fund Loan": ["Growth Fund Loan"],
    "Vibrant Community Grant": ["Vibrant Community Grant"],
    "Aerospace and Defense Opportunity Grant": ["Aerospace and Defense Opportunity Grant"],
    "Talent Acquisition": ["Talent Acquisition"],
}


# Can Ohio get the money back? This is the question a reader is asking, and it
# is NOT the same as what the guidelines publish. 56 signed JobsOhio grant
# agreements were obtained from Franklin County court files, spanning 2013 to
# 2023 and the Economic Development, Workforce, Revitalization, R&D and
# Inclusion programs. Every one carries the same Section 9(b)(ii), "Demand
# Repayment of Grant Funds." So recourse is established for those programs by
# the contracts themselves, whatever the published guidelines say.
#
# Grades, strongest evidence first:
#   agreement seen    this recipient's own signed agreement is in a court file
#   standard form     a program whose agreements were obtained, all identical
#   published terms   no agreement seen, but the guidelines publish a clawback
#   loan              repayable by its nature as debt
#   service not cash  JobsOhio paid subcontractors; it can bill the service value
#   none found        no clawback published and no agreement ever obtained
#   program unknown   the payment cannot be tied to a program at all
FORM_PROGRAMS = {"Economic Development Grant", "Workforce Grant", "Revitalization Grant",
                 "Revitalization Grant Phase II", "Research & Development Grant",
                 "Inclusion Grant"}
PUBLISHED_CLAWBACK = {"Spec Development (OSIP)"}
LOANS = {"Revitalization Loan", "Growth Fund Loan", "Other Loan"}
SERVICES = {"Talent Acquisition"}
# nothing published and no agreement obtained. Air service is the one where the
# guidelines affirmatively describe a disbursement process and still say nothing
# about getting the money back, and no airline appears among the 63 defendants.
NONE_FOUND = {"Air Service Restoration", "Aerospace and Defense Opportunity Grant",
              "Vibrant Community Grant", "Other Grant"}

RECOURSE_NOTE = {
    "agreement seen": "This company's own signed JobsOhio agreement is filed in a Franklin County court case and contains Section 9(b)(ii), 'Demand Repayment of Grant Funds': 'Grantor may demand repayment of all or a portion of Grant Funds disbursed.'",
    "standard form": "Paid under a program whose signed agreements were obtained from court files. All of them, 2013 to 2023, carry the same Section 9(b)(ii) repayment clause. This company's own agreement was not obtained, so this rests on the form being standard.",
    "published clawback": "No agreement obtained, but the program's published guidelines contain a repayment trigger.",
    "loan": "A loan. The principal is repayable by its nature, which is a different thing from a performance clawback.",
    "service not cash": "JobsOhio paid subcontractors to provide services rather than paying the company. The agreement makes the company liable for the value of those services as liquidated damages if it misses its metrics.",
    "none found": "No repayment language in the published guidelines, and no signed agreement for this program was ever obtained. For the air service grants the guidelines set out a disbursement process and still say nothing about what happens if the route ends, and no airline appears among the 63 companies JobsOhio has sued.",
    "program unknown": "The payment cannot be tied to a program in JobsOhio's own monthly project reports, so there is nothing to read either way.",
}


def recourse_for(fams, seen, tas):
    """The strongest grade the evidence supports for one payment."""
    if tas:
        # the court record says this company was on a services agreement, which
        # overrides the program families, since JobsOhio paid vendors not the
        # company and the remedy is liquidated damages rather than repayment
        return "service not cash"
    if seen:
        return "agreement seen"
    fams = set(fams)
    if fams & FORM_PROGRAMS:
        return "standard form"
    if fams & PUBLISHED_CLAWBACK:
        return "published clawback"
    if fams & LOANS:
        return "loan"
    if fams & SERVICES:
        return "service not cash"
    if fams & NONE_FOUND:
        return "none found"
    return "program unknown"


def main():
    terms = {t["program"]: t for t in json.loads(TERMS.read_text())}
    by_family = {}
    for prog, fams in ALIAS.items():
        t = terms.get(prog)
        if not t:
            continue
        for f in fams:
            by_family[f] = t

    parents = {r["recipient_id"]: r for r in csv.DictReader(PARENTS.open())}
    grants = list(csv.DictReader(GRANTS.open()))
    for g in grants:
        ein = re.sub(r"\D", "", g["recipient_ein"])
        g["recipient_id"] = (f"EIN:{ein}" if len(ein) == 9 and ein.strip("0")
                             else f"NAME:{normalize_name(g['recipient_name'])}")

    clawed = {g["recipient_id"] for g in grants if int(g["cash_amt"]) < 0}

    # recipients whose own signed agreement is filed in a court case
    seen_agreement, on_services = set(), set()
    if LAWSUITS.exists():
        for r in csv.DictReader(LAWSUITS.open()):
            if not r.get("recipient"):
                continue
            key = normalize_name(r["recipient"])
            if str(r.get("agreement_is_exhibit", "")).lower().startswith(("y", "true")):
                seen_agreement.add(key)
            a = (r.get("agreement") or "").lower()
            if "talent acquisition" in a or "tas agreement" in a:
                on_services.add(key)

    rows = []
    for g in grants:
        p = parents.get(g["recipient_id"], {})
        fams = [f.strip() for f in (p.get("metrics_programs") or "").split(";") if f.strip()]
        if not fams and any(a in g["recipient_name"].lower() for a in AIRLINES):
            fams = ["Air Service Restoration"]
        hits = [by_family[f] for f in fams if f in by_family]
        if not hits:
            call, prog, quote, src = "Program unknown", "; ".join(fams), "", ""
        else:
            # a recipient with several programs takes the weakest published terms,
            # since the payment cannot be tied to one of them
            order = {"Conditional": 3, "Partly conditional": 2, "Unknown": 1}
            weakest = min(hits, key=lambda t: order.get(t["conditional"], 0))
            call, prog = weakest["conditional"], "; ".join(fams)
            quote, src = weakest["evidence_quote"], weakest["source"]
        key = normalize_name(g["recipient_name"])
        grade = recourse_for(fams, key in seen_agreement, key in on_services)
        rows.append({
            # the join key: parent NAMES get rewritten by the ownership pass,
            # and a name join then silently drops the row
            "recipient_id": g["recipient_id"],
            "fiscal_year": g["fiscal_year"], "recipient": g["recipient_name"],
            "parent": p.get("parent", ""), "class": p.get("recipient_class") or p.get("recipient_class_auto", ""),
            "cash": g["cash_amt"], "programs": prog, "conditions": call,
            "recourse": grade, "recourse_note": RECOURSE_NOTE[grade],
            "clawback_seen": "yes" if g["recipient_id"] in clawed else "",
            "published_terms": quote[:200], "terms_source": src,
        })

    with OUT.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

    paid = [r for r in rows if int(r["cash"]) > 0]
    tot = sum(int(r["cash"]) for r in paid)
    print(f"{len(rows)} payments, ${tot:,} paid\n")
    print(f"{'conditions published':26s} {'payments':>9s} {'dollars':>15s} {'share':>7s}")
    agg = defaultdict(lambda: [0, 0])
    for r in paid:
        agg[r["conditions"]][0] += 1
        agg[r["conditions"]][1] += int(r["cash"])
    for k, (n, d) in sorted(agg.items(), key=lambda kv: -kv[1][1]):
        print(f"{k:26s} {n:9d} {d:15,} {d/tot:7.1%}")
    print(f"\n{'can Ohio get it back?':22s} {'payments':>9s} {'dollars':>15s} {'share':>7s}")
    agg2 = defaultdict(lambda: [0, 0])
    for r in paid:
        agg2[r["recourse"]][0] += 1
        agg2[r["recourse"]][1] += int(r["cash"])
    for k, (n, d) in sorted(agg2.items(), key=lambda kv: -kv[1][1]):
        print(f"{k:22s} {n:9d} {d:15,} {d/tot:7.1%}")
    yes = sum(d for k, (n, d) in agg2.items()
              if k in ("agreement seen", "standard form", "published clawback"))
    print(f"\nrecourse established for ${yes:,} of ${tot:,} ({yes/tot:.1%}) of paid dollars")
    cl = [r for r in rows if r["clawback_seen"]]
    print(f"\nrecipients with money recorded as returned: {len({r['recipient'] for r in cl})}")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
