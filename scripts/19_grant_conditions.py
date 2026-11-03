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
        rows.append({
            "fiscal_year": g["fiscal_year"], "recipient": g["recipient_name"],
            "parent": p.get("parent", ""), "class": p.get("recipient_class") or p.get("recipient_class_auto", ""),
            "cash": g["cash_amt"], "programs": prog, "conditions": call,
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
    cl = [r for r in rows if r["clawback_seen"]]
    print(f"\nrecipients with money recorded as returned: {len({r['recipient'] for r in cl})}")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
