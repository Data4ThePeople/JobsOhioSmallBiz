#!/usr/bin/env python3
"""Merge the third batch of WARN-join candidates, which is one company, not two.

Six recipients surfaced after the name-matching fix. Four were name
collisions, correctly sitting at tier C or D and only reviewed because a
tie-out asked about them. Two came back Confirmed. Only one of those is
merged, and the reason the other is not is the whole substance of this file.

**Technicote, $700,000, goes in.** It is the cleanest site match in the data:
the FY2025 payment address, 6206 Wolf Creek Pike, Trotwood, is character for
character the facility address on the WARN letterhead. The letter says in its
own words that the layoff is permanent and that "the facility will remain
open, with reduced operations". 53 jobs, mostly production. JobsOhio paid the
full $700,000 for 163 new jobs at a $58.9 million plant that opened in October
2024; the cut came about sixteen months later.

**Toledo Innovation Center Landlord, $1,500,000, does not**, and is recorded
as Unresolved with its reasoning instead. The research graded it a confirmed
failure and I disagree, because four things each point the other way and they
compound:

  * **18 Ohio jobs.** Bitwise terminated 625 people nationally across 14 sites
    in 7 states; 18 were Ohio residents and the WARN letter names them
    individually as head-office and support roles. That is not a mass layoff
    by Ohio's own threshold or by any ordinary use of the phrase.
  * **The funded thing worked.** The grant was a Revitalization Grant to
    revive a building. The building was finished, opened as Innovation Post in
    February 2025 with tenants, and was still letting space at the end of
    2025.
  * **The payee is not a debtor.** Bitwise and four affiliates filed Chapter 7
    in Delaware; Toledo Innovation Center Landlord LLC filed nothing. What
    collapsed is the anchor tenant.
  * **The property link is inferred.** No deed or auditor record was reached
    tying the payee to 1300 Jefferson Avenue. The chain is the entity name, a
    PNC "Toledo Innovation Center Master Tenant" entity appearing in the
    bankruptcy, the Toledo payee address, and the $1,500,000 matching
    JobsOhio's Lucas County Revitalization Grant to the dollar. Strong, and
    still inferred.

None of the five categories fits it: the payee did not go bankrupt, the site
did not close, 18 is not a mass layoff, nothing was sold, no service ended.
When no category fits, that is the data saying the row does not belong in the
count. It is a genuinely interesting finding and it is written up as a lead
instead, where the uncertainty can be stated at length rather than compressed
into a label a reporter will read as settled.

Usage: 41_merge_warncheck_c.py [--write]
"""
import csv, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FAILURES = ROOT / "data" / "failures.csv"
SOURCES = ROOT / "data" / "failure_sources.csv"
SITECHECK = ROOT / "data" / "research3" / "sitecheck.json"
PARENTS = ROOT / "data" / "parents.csv"
WARNJOIN = ROOT / "data" / "warn_join.csv"
CHECK = ROOT / "data" / "research3" / "warncheck_c.json"

MERGE = {"TECHNICOTE INC": ("Layoffs", "Mass layoff at the funded site")}
CAVEAT = {
    "TECHNICOTE INC":
        "The plant stayed open. The employer's own notice says the layoff is permanent "
        "and that the facility will continue with reduced operations, and the 53 jobs are "
        "mostly production roles. JobsOhio paid the full $700,000 it committed for 163 new "
        "jobs at a $58.9 million Trotwood plant; the plant opened in October 2024 and the "
        "cut came about sixteen months later. The site tie needs no inference: the payment "
        "address and the address on the notice are the same street.",
}
UNRESOLVED = {
    "TOLEDO INNOVATION CENTER LANDLORD LLC":
        "Not counted as a failure, and the reasons are worth reading. JobsOhio's "
        "$1,500,000 Revitalization Grant was to revive a building, and the building was "
        "finished: it opened as Innovation Post in February 2025 and was still letting "
        "space at the end of that year. What collapsed is the anchor tenant. Bitwise "
        "Industries and four affiliates filed Chapter 7 in Delaware on 2023-06-28 "
        "(23-10845-TMH), and its own notice to Ohio terminated 625 people nationally "
        "across 14 sites in 7 states, of whom 18 were Ohio residents named individually "
        "as head-office and support roles. The payee itself filed nothing and is not a "
        "debtor. And no deed was reached tying the payee to 1300 Jefferson Avenue; that "
        "link rests on the entity name, a PNC master-tenant entity appearing in the "
        "bankruptcy, the Toledo payee address and the amount matching to the dollar. "
        "None of the five failure categories fits, so the row is held here rather than "
        "counted. See lead 19.",
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
    found = {x["name"]: x for x in json.loads(CHECK.read_text())}

    before_n = sum(1 for r in rows if r["verdict"] == "Confirmed failure")
    before_c = sum(int(r["paid"] or 0) for r in rows if r["verdict"] == "Confirmed failure")
    site = json.loads(SITECHECK.read_text())
    seen_site = {x["recipient_id"] for x in site}
    srcs = list(csv.DictReader(SOURCES.open()))
    scols, by_name = list(srcs[0]), {r["name"] for r in srcs}
    added = []

    for name, x in found.items():
        rid = x["recipient_id"]
        p = parents.get(rid)
        if not p:
            print(f"  skipped {name}: not in parents.csv"); continue
        verdict = ("Confirmed failure" if name in MERGE
                   else "Unresolved" if name in UNRESOLVED else None)
        if verdict is None:
            continue
        ev, cat = MERGE.get(name, ("", ""))
        row = by_id.get(rid) or {c: "" for c in cols}
        row.update({
            "recipient_id": rid, "name": p["name"], "parent": p.get("parent", ""),
            "class": p.get("recipient_class", ""), "paid": p.get("total_cash", "0"),
            "grant_years": p.get("years", ""), "verdict": verdict,
            "event": ev, "event_date": x.get("event_date", "") if ev else "",
            "entity_filed": x.get("entity_filed", ""), "court": x.get("court", ""),
            "docket": x.get("docket", ""), "ohio_outcome": x.get("ohio_outcome", ""),
            "confidence": x.get("confidence", ""), "source": x.get("source", ""),
            "flagged_by": "Ohio WARN register, joined against every recipient "
                          "(scripts/35_warn_join.py), after the name-matching fix",
            "notes": x.get("notes", ""), "category": cat,
            "caveat": CAVEAT.get(name, "") or UNRESOLVED.get(name, ""),
        })
        if rid not in by_id:
            rows.append(row); by_id[rid] = row
        added.append((name, verdict))

        if verdict == "Confirmed failure":
            if rid not in seen_site:
                site.append({"recipient_id": rid, "name": name,
                             "verdict": x.get("site_verdict", ""),
                             "funded_site": x.get("funded_site", ""),
                             "failed_site": x.get("failed_site", ""),
                             "same_site": x.get("site_verdict") == "same site",
                             "partial": x.get("site_verdict") == "partly",
                             "what_survives": "", "confidence": x.get("confidence", ""),
                             "source": x.get("source", ""),
                             "notes": "From data/research3/warncheck_c.json. "
                                      + (x.get("recommend") or "")})
            w = warn.get(rid, {})
            if name not in by_name and w.get("warn_pdf"):
                srcs.append({**{c: "" for c in scols}, "name": name, "url": w["warn_pdf"],
                             "url_kind": "state WARN notice",
                             "title": f"WARN notice, {w['warn_employer']}, {w['warn_place']}",
                             "publisher": "Ohio Department of Job and Family Services",
                             "published": w["warn_received"], "paywalled": "no",
                             "verified": "yes",
                             "notes": f"The employer's own filing, {w['warn_affected']} "
                                      f"affected, received {w['warn_received']}. The "
                                      f"facility address on the letter is the address "
                                      f"JobsOhio's payment was remitted to."})

    now = [r for r in rows if r["verdict"] == "Confirmed failure"]
    for n, v in added:
        print(f"  {n[:40]:40s} -> {v}")
    print(f"\nconfirmed failures: {before_n} -> {len(now)}")
    print(f"confirmed dollars : ${before_c:,} -> ${sum(int(r['paid'] or 0) for r in now):,}")

    if "--write" not in argv:
        print("\n--dry-run by default; pass --write")
        return
    with FAILURES.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(rows)
    with SOURCES.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=scols); w.writeheader(); w.writerows(srcs)
    SITECHECK.write_text(json.dumps(site, indent=1))
    print(f"\nwrote {FAILURES.relative_to(ROOT)}, {SOURCES.relative_to(ROOT)} and sitecheck")


if __name__ == "__main__":
    main(sys.argv[1:])
