#!/usr/bin/env python3
"""Merge the verified WARN-join candidates into data/failures.csv.

The original failure set came from scanning news headlines, which can only find
a closure somebody wrote about. Joining Ohio's whole WARN register against every
recipient found candidates nobody had checked, and
data/research3/warncheck_{a,b}.json are the verifications. This merges the
confirmed ones.

Judgment calls encoded here, because they are not in the research files and a
reader deserves to see them made in one place:

  Pier 1 is a company-level failure, not a site one. It liquidated in 2020.
    The Schedule I address, Grove City, does not match the Groveport
    distribution centre in the notice, and JobsOhio has no project record for
    it at all, so the row is filed as a bankruptcy and carries a caveat saying
    what the money cannot be tied to.
  Curation Foods and Mitec Powertrain carry $0. Both closed the funded Ohio
    plant and in both cases JobsOhio got every dollar back: Curation was paid
    $350,000 in FY2021 and reversed $350,000 in FY2022, Mitec $200,000 in
    FY2019 and reversed $200,000 in FY2020. They are failures of the project
    and successes of the recovery clause, and the piece is stronger for
    carrying both facts. They count as companies and add nothing to the money.
  FCA is a mass layoff, not a closure. The Toledo Assembly Complex is open.
    1,094 of the 1,225 in the 2023 notice are supplemental, meaning temporary,
    workers, so the caveat carries the 2024 notice's 1,134 as the firmer
    figure.
  ATW Ohio is partial. Some staff could transfer to a sister plant in
    Clermont County and JobsOhio's project record spans Clermont and Brown.

Idempotent: a recipient already in failures.csv is updated in place rather than
added again, so running twice changes nothing.

Usage: 37_merge_warncheck.py [--write]
"""
import csv, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FAILURES = ROOT / "data" / "failures.csv"
SOURCES = ROOT / "data" / "failure_sources.csv"
PARENTS = ROOT / "data" / "parents.csv"
WARNJOIN = ROOT / "data" / "warn_join.csv"
CHECKS = [ROOT / "data" / "research3" / "warncheck_a.json",
          ROOT / "data" / "research3" / "warncheck_b.json"]
SITECHECK = ROOT / "data" / "research3" / "sitecheck.json"
# The site verdict for the two rows whose research file records the site in
# prose rather than in a verdict field. Pier 1 is "unresolved" and not "same
# site": the company genuinely liquidated, which is a company-level fact that
# needs no site, but the Grove City address on Schedule I cannot be tied to the
# Groveport centre in the notice and JobsOhio has no project record for it.
SITE_VERDICT = {"MITEC POWERTRAIN INC": "same site",
                "Pier 1 Imports (US) Inc": "unresolved"}

# event -> category, the same map 31_audit_failures.py enforces
CATEGORY = {
    "Closure": "Funded site closed", "Layoffs": "Mass layoff at the funded site",
    "Chapter 7": "Bankruptcy or receivership", "Chapter 11": "Bankruptcy or receivership",
    "Acquisition": "Sold or absorbed", "Divestiture": "Sold or absorbed",
}
# per-company overrides, each one a decision rather than a lookup
OVERRIDE = {
    "Pier 1 Imports (US) Inc": dict(
        event="Chapter 11", category="Bankruptcy or receivership",
        caveat="A company-level failure, not a site one. Pier 1 filed Chapter 11 in "
               "February 2020 and liquidated. The Groveport distribution centre in the "
               "state's notice is not the Grove City address on Schedule I, and JobsOhio "
               "has no project record for Pier 1 at all, so what the $30,000 paid for "
               "cannot be established."),
    "CURATION FOODS INC": dict(
        caveat="The funded Bowling Green plant closed, and JobsOhio got all of the money "
               "back: $350,000 paid in FY2021 and $350,000 reversed in FY2022, the same "
               "year as the closure. The row counts as a company and carries $0, because "
               "net nothing was paid. JobsOhio's project record is under the company's "
               "earlier name, Apio, Inc."),
    "MITEC POWERTRAIN INC": dict(
        caveat="The funded Findlay plant closed permanently, and JobsOhio got all of the "
               "money back: $200,000 paid in FY2019 and $200,000 reversed in FY2020. The "
               "row counts as a company and carries $0. The closure was not the pandemic: "
               "the letter gives the cause as the largest customer moving production to "
               "Mexico and Canada, and it is signed by a chief restructuring officer."),
    "FCA US LLC": dict(
        event="Layoffs", category="Mass layoff at the funded site",
        caveat="The Toledo Assembly Complex is still open. Two notices: 1,225 in December "
               "2023, of which 1,094 are supplemental, meaning temporary, workers, and "
               "1,134 in November 2024. The 2024 figure is the firmer one. The same shift "
               "cut took 68 jobs at syncreon, a supplier JobsOhio also paid."),
    "ATW OHIO LLC": dict(
        caveat="Partial. The Mount Orab plant closed, and the notice says some staff could "
               "transfer to the sister Big Tex plant in Clermont County, which JobsOhio's "
               "project record covers alongside Brown. A related recipient, American "
               "Trailer World Corp, was paid a further $300,000 in FY2022 on the same "
               "project record."),
    "XELLIA PHARMACEUTICALS USA LLC": dict(
        event="Layoffs", category="Mass layoff at the funded site",
        caveat="Two things at once at the funded Bedford plant: the site was sold to "
               "Hikma and 297 jobs went across three notices. Filed as the layoff, "
               "because that is the Ohio impact, but the sale is the reason."),
    "DOREL HOME FURNISHINGS INC": dict(
        event="Closure", category="Funded site closed",
        caveat="Manufacturing at the funded Tiffin plant ended; about 40 warehouse jobs "
               "stayed. The letter says about 130 hourly, the attached worker list is "
               "headed 154, and the state's table says 130."),
    "JO-ANN STORES": dict(
        caveat="The 662-job notice widely reported is the Hudson head office, which is not "
               "the funded site. JobsOhio's project is a Madison County distribution "
               "centre, and the notice for it closes the whole West Jefferson fulfilment "
               "centre, 116 jobs. The 116 is the figure that belongs beside this grant."),
}


def main(argv):
    rows = list(csv.DictReader(FAILURES.open()))
    cols = list(rows[0])
    by_id = {r["recipient_id"]: r for r in rows}
    parents = {r["recipient_id"]: r for r in csv.DictReader(PARENTS.open())}
    warn = {}
    for w in csv.DictReader(WARNJOIN.open()):
        k = w["recipient_id"]
        if k not in warn or int(w["affected_n"]) > int(warn[k]["affected_n"]):
            warn[k] = w

    found = []
    for f in CHECKS:
        if f.exists():
            found += [x for x in json.loads(f.read_text())
                      if x.get("verdict") == "Confirmed failure"]

    before_n = sum(1 for r in rows if r["verdict"] == "Confirmed failure")
    before_c = sum(int(r["paid"] or 0) for r in rows if r["verdict"] == "Confirmed failure")

    added, updated, skipped = [], [], []
    for x in found:
        rid = x["recipient_id"]
        p = parents.get(rid)
        if not p:
            skipped.append((x["name"], "not in parents.csv"))
            continue
        ov = OVERRIDE.get(x["name"], {})
        event = ov.get("event") or x.get("event") or "Closure"
        cat = ov.get("category") or CATEGORY.get(event)
        if not cat:
            skipped.append((x["name"], f"no category for event {event!r}"))
            continue
        w = warn.get(rid, {})
        row = by_id.get(rid) or {c: "" for c in cols}
        row.update({
            "recipient_id": rid, "name": p["name"],
            "parent": p.get("parent", ""), "class": p.get("recipient_class", ""),
            "paid": p.get("total_cash", "0"), "grant_years": p.get("years", ""),
            "verdict": "Confirmed failure", "event": event,
            "event_date": x.get("event_date", ""),
            "entity_filed": x.get("entity_filed", ""), "court": x.get("court", ""),
            "docket": x.get("docket", ""), "ohio_outcome": x.get("ohio_outcome", ""),
            "confidence": x.get("confidence", ""), "source": x.get("source", ""),
            "flagged_by": "Ohio WARN register, joined against every recipient "
                          "(scripts/35_warn_join.py)",
            "notes": x.get("notes", ""), "category": cat,
            "caveat": ov.get("caveat", "") or (
                f"Site check: {x['site_verdict']}. {x.get('failed_site','')}"
                if x.get("site_verdict") == "partly" else ""),
        })
        (updated if rid in by_id else added).append(row)
        if rid not in by_id:
            rows.append(row); by_id[rid] = row

    after = [r for r in rows if r["verdict"] == "Confirmed failure"]
    print(f"{len(found)} confirmed in the research files: {len(added)} new, "
          f"{len(updated)} already present, {len(skipped)} skipped")
    for n, why in skipped:
        print(f"  skipped {n}: {why}")
    print(f"\nadded:")
    for r in sorted(added, key=lambda x: -int(x["paid"] or 0)):
        print(f"  ${int(r['paid'] or 0):>10,}  {r['name'][:32]:32s} {r['category'][:30]:30s} "
              f"{r['confidence']}")
    print(f"\nconfirmed failures: {before_n} -> {len(after)}")
    print(f"confirmed dollars : ${before_c:,} -> "
          f"${sum(int(r['paid'] or 0) for r in after):,}")

    # The audit reads one file for the funded-site question, so the verdicts the
    # research files carry have to land there too rather than in a second place
    # nothing checks.
    site = json.loads(SITECHECK.read_text()) if SITECHECK.exists() else []
    seen_site = {x["recipient_id"] for x in site}
    new_site = 0
    for x in found:
        rid = x["recipient_id"]
        if rid in seen_site or rid not in parents:
            continue
        v = x.get("site_verdict") or SITE_VERDICT.get(x["name"], "")
        if not v:
            print(f"  NO SITE VERDICT for {x['name']}")
            continue
        site.append({"recipient_id": rid, "name": x["name"], "verdict": v,
                     "funded_site": x.get("funded_site", ""),
                     "failed_site": x.get("failed_site", ""),
                     "same_site": v == "same site", "partial": v == "partly",
                     "what_survives": "", "confidence": x.get("confidence", ""),
                     "source": x.get("source", ""),
                     "notes": "From the WARN-join verification, "
                              "data/research3/warncheck_*.json. "
                              + (x.get("recommend") or "")})
        new_site += 1
    print(f"\n{new_site} site verdicts folded into sitecheck.json")

    # Each new row needs a source the audit can fetch, and for these the best
    # one is the thing that found them: the employer's own notice to the state.
    srcs = list(csv.DictReader(SOURCES.open()))
    scols = list(srcs[0])
    by_name = {r["name"]: r for r in srcs}
    new_src = 0
    for r in added:
        if r["name"] in by_name:
            continue
        w = warn.get(r["recipient_id"], {})
        if not w.get("warn_pdf"):
            print(f"  NO SOURCE for {r['name']}: no WARN pdf in the join")
            continue
        srcs.append({**{c: "" for c in scols},
                     "name": r["name"], "url": w["warn_pdf"],
                     "url_kind": "state WARN notice",
                     "title": f"WARN notice, {w['warn_employer']}, {w['warn_place']}",
                     "publisher": "Ohio Department of Job and Family Services",
                     "published": w["warn_received"], "paywalled": "no", "verified": "yes",
                     "notes": f"The employer's own filing with the state, {w['warn_affected']} "
                              f"affected, received {w['warn_received']}. This notice is what "
                              f"identified the company: scripts/35_warn_join.py joined the "
                              f"whole register against every recipient. Verified in "
                              f"data/research3/warncheck_*.json."})
        new_src += 1
    print(f"\n{new_src} source rows added, each the employer's own notice to Ohio")

    if "--write" not in argv:
        print("\n--dry-run by default; pass --write")
        return
    with FAILURES.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(rows)
    with SOURCES.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=scols); w.writeheader(); w.writerows(srcs)
    SITECHECK.write_text(json.dumps(site, indent=1))
    print(f"\nwrote {FAILURES.relative_to(ROOT)} and {SOURCES.relative_to(ROOT)}")


if __name__ == "__main__":
    main(sys.argv[1:])
