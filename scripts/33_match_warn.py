#!/usr/bin/env python3
"""Tie every closure and mass layoff to Ohio's own WARN notice, or say why there isn't one.

A claim that a company closed an Ohio plant or cut Ohio jobs should not rest on a
news story when the state holds the employer's own filing. This matches each
confirmed closure or mass layoff against data/warn/notices.csv and writes
data/failure_warn.csv, which carries, per company, the matched notice, the site,
the headcount the employer itself reported, and the link to the filed letter.

**The absences matter as much as the matches.** Where the state has no notice,
that is recorded as a row too, with the reason, because a reader who checks will
find the same hole and should find our account of it first.

On the matching rule. An earlier version of this match was far too loose: it
counted any shared word, which paired Ultium Cells with American Energy
Corporation on the word "energy" and FedEx Supply Chain with DHL Supply Chain on
"supply chain". Two things fixed it:

  * **word rarity.** A word is weighed by how many different employers in the
    state record use it. Sharing "ultium" with one other filer is near proof;
    sharing "logistics" with thirty is no evidence at all.
  * **date proximity.** The notice has to sit near the event. Air Wisconsin has
    notices in 2020 and 2025, and only the 2025 one is this finding.

A match still needs a human to accept it, so every row carries the gap in months
and the rarity score it was accepted on, and `09_analyze.py` surfaces both. Where
a company filed more than one notice, every other candidate is carried in the row
as well, because picking one and hiding the rest is how a reader gets surprised.

Choosing between a company's own notices is its own trap. Closest-in-time alone
picked Nestle's "Nestle USA Update" for 13 people over the substantive Solon
notice for 241, because an update filed late in a phased closure sits nearer its
end. Preferring the largest headcount instead was worse: it reached back past
Olive AI's actual closure notice to an earlier layoff round. So the rule stays
closest-in-time, with one narrow exception: when the winner is a revision of an
earlier notice and a full notice sits within six months of it, the full notice
wins. That recovers Nestle's 241 and leaves GXO's one-month update in place,
which really is the notice for its site.

A matched notice is not by itself proof the funded site failed, and conflating
the two is how Republic Steel went wrong: the only Republic Steel notice Ohio
holds is for the Canton mill, while the grant paid for Lorain. So every match
also carries `notice_at_funded_site`, set by comparing the notice's county with
the counties the money was actually paid into, both read off the files rather
than off anybody's prose. Four of the fifteen come back no. The three companies
that failed away from the funded site keep their rows here for that reason:
their notice is the evidence of where the failure actually was.

Coverage limit worth stating in the post: Ohio publishes these notices from 2020
forward, so a failure before 2020 cannot be checked this way at all.

Usage: 33_match_warn.py [--write]
"""
import csv, json, re, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WARN = ROOT / "data" / "warn" / "notices.csv"
FAILURES = ROOT / "data" / "failures.csv"
GRANTS = ROOT / "data" / "grants_raw.csv"
WARNJOIN = ROOT / "data" / "warn_join.csv"
OUT = ROOT / "data" / "failure_warn.csv"
ELSEWHERE = "Failed away from the funded site"
CATS = ("Funded site closed", "Mass layoff at the funded site", ELSEWHERE)
FIRST_YEAR = 2020  # Ohio publishes no notices before this

# Words that carry no identifying weight. Legal suffixes, plus the industry
# nouns that half the manufacturers in the state share.
STOP = {"inc", "inc.", "corp", "corporation", "company", "co", "llc", "ltd", "the", "of",
        "and", "usa", "holdings", "group", "us", "incorporated", "lp", "plc", "llp",
        "north", "america", "american", "supply", "chain", "logistics", "services",
        "service", "health", "care", "system", "energy", "international", "industries",
        "products", "solutions", "technologies", "manufacturing", "enterprises",
        "partners", "global", "limited", "center", "centers"}

# Where the state has no notice, the reason, checked one at a time. Each of these
# was searched for by name and by city and county in every published year.
WHY_NO_NOTICE = {
    "COVERMYMEDS LLC":
        "The 815-job cut was company-wide and the Ohio share was never broken out. "
        "Ohio requires a notice only for 50 or more at a single site inside 30 days, "
        "so a cut spread across a national workforce and a subleased headquarters can "
        "clear the bar without one. Nothing for CoverMyMeds or McKesson appears in any "
        "published year.",
    "HYLAND SOFTWARE INC":
        "The 1,000-job cut was 20 percent of a global workforce and the Ohio share was "
        "never disclosed, so the same 50-at-one-site threshold can be cleared without a "
        "notice. Nothing for Hyland appears in any published year, and the Westlake "
        "notices in the record are other employers.",
    "SPEEDWAY LLC":
        "The reported Enon cut was fewer than 35 people in October 2021, which is below "
        "the 50 that triggers a notice, and the July 2022 Enon figure was never published. "
        "Nothing for Speedway or 7-Eleven appears in any published year.",
    "Sauder Woodworking Co":
        "This one is a real gap rather than a threshold. A permanent cut of about 150 at "
        "one Archbold plant would normally require a notice, and none exists for Sauder "
        "in any published year, by name or by Fulton County. The state's record is dense "
        "in that window, including notices for 1 person and for 39 part-time workers, so "
        "it is unlikely to be an omission. The likeliest reading is that the layoff was "
        "expected to last under six months, which Ohio exempts, and which fits the plant "
        "staying open. The 150 figure therefore rests on press reporting alone.",
}


def toks(s):
    return {w for w in re.split(r"[^a-z0-9]+", (s or "").lower())
            if w and w not in STOP and len(w) > 2}


def ym(s):
    """(year, month) from the several date shapes these files use."""
    s = (s or "").strip()
    for pat, f in ((r"^(\d{1,2})/(\d{1,2})/(\d{4})$", lambda m: (int(m[3]), int(m[1]))),
                   (r"^(\d{1,2})/(\d{1,2})/(\d{2})$", lambda m: (2000 + int(m[3]), int(m[1]))),
                   (r"^(\d{4})-(\d{1,2})", lambda m: (int(m[1]), int(m[2])))):
        m = re.match(pat, s)
        if m:
            return f(m)
    return None


def gap(a, b):
    return abs((a[0] - b[0]) * 12 + (a[1] - b[1])) if a and b else 999


def headcount(s):
    """The employer's own number. Some read "484 Perm Layoffs/850 Temp Layoffs",
    so the first figure is the permanent one and that is what is compared."""
    m = re.search(r"\d[\d,]*", s or "")
    return int(m.group(0).replace(",", "")) if m else 0


def county_map(warn):
    """city -> county, built from the notices themselves.

    Ohio writes each notice's place as "Canton/Stark", so 810 notices are also
    810 statements about which county a city is in. That is a better source for
    this than anything derived from prose: a first attempt read the funded
    counties out of the site check's wording and labelled Dana's Lima notice as
    on-site, because the sentence said "neither in Allen County" and the match
    did not know a negation when it saw one.
    """
    out = {}
    for w in warn:
        if "/" in (w["place"] or ""):
            city, county = w["place"].rsplit("/", 1)
            city, county = city.strip().lower(), county.strip().lower()
            if city and county and "unknown" not in county:
                out.setdefault(city, county)
    return out


def site_agrees(paid_cities, place, cmap):
    """Is the notice in a county the money was actually paid into?

    Compared by county rather than by city, because iMFLUX was paid at West
    Chester and closed at Hamilton, which are six miles apart in one county and
    one operation.

    Against *every* city the payee was paid at, not the first one. Reading only
    the first put Sarepta's Columbus notice outside its own funded county,
    because an earlier payment went to the Cambridge head office, and left
    Nestle unresolved behind a Glendale address. A grant paid into four places
    was paid into all four.

    Blank rather than guessed when no paid city can be placed in a county, which
    is the honest answer for a payee paid only out of state.
    """
    if "/" not in (place or "") or not paid_cities:
        return ""
    notice_county = place.rsplit("/", 1)[1].strip().lower()
    counties = {cmap[c.strip().lower()] for c in paid_cities
                if c.strip().lower() in cmap}
    if not counties or not notice_county:
        return ""
    return "yes" if notice_county in counties else "no"


def is_revision(employer):
    """Ohio files amendments under the same employer with the word in the name."""
    return bool(re.search(r"\bupdate\b|\brevis", employer or "", re.I))


def main(argv):
    warn = list(csv.DictReader(WARN.open()))
    fails = [r for r in csv.DictReader(FAILURES.open())
             if r["verdict"] in ("Confirmed failure", ELSEWHERE) and r["category"] in CATS]
    # the join's answer, for companies whose notice is filed under another name
    joined = {}
    if WARNJOIN.exists():
        by_notice = {(w["employer"], w["place"], w["received"]): w for w in warn}
        for j in csv.DictReader(WARNJOIN.open()):
            if j["tier"] not in ("A", "B"):
                continue
            k = j["recipient_id"]
            w = by_notice.get((j["warn_employer"], j["warn_place"], j["warn_received"]))
            if w and (k not in joined
                      or headcount(w["affected"]) > headcount(joined[k]["affected"])):
                joined[k] = w

    cmap = county_map(warn)
    # every city each payee's money was sent to, off Schedule I itself
    paid_city = {}
    for g in csv.DictReader(GRANTS.open()):
        rid = f"EIN:{g['recipient_ein']}" if g["recipient_ein"] else ""
        if rid and g["city"]:
            paid_city.setdefault(rid, set()).add(g["city"])

    # how many distinct employers in the state record use each word
    weight = Counter()
    for name in {w["employer"] for w in warn}:
        for k in toks(name):
            weight[k] += 1
    indexed = [(toks(w["employer"]), w) for w in warn]

    rows, unmatched = [], []
    for f in sorted(fails, key=lambda r: -int(r["paid"] or 0)):
        ft, fd = toks(f["name"]), ym(f["event_date"])
        # A failure that predates the register cannot have a notice in it, and
        # matching one anyway is worse than matching none: Republic Steel's
        # funded Lorain mill went idle in March 2016 and the only Republic
        # notice Ohio holds is Canton in 2023, 89 months later and a different
        # site. Say there is no notice and why.
        if fd and fd[0] < FIRST_YEAR:
            rows.append({"recipient_id": f["recipient_id"], "name": f["name"],
                         "category": f["category"], "state_notice": "none",
                         "why_none": f"The failure dates to {f['event_date']}, and Ohio "
                                     f"publishes these notices only from {FIRST_YEAR}. "
                                     f"Any notice this company filed at the time is not "
                                     f"in the register at all.",
                         "warn_year": "", "warn_employer": "", "warn_place": "",
                         "warn_affected": "", "warn_received": "", "warn_pdf": "",
                         "months_from_event": "", "name_rarity": "",
                         "notice_at_funded_site": "", "other_notices": ""})
            continue
        cands = []
        for t, w in indexed:
            inter = t & ft
            if not inter:
                continue
            rare = min(weight[k] for k in inter)
            cover = len(inter) / min(len(t), len(ft))
            if not (rare <= 2 or cover >= 0.8):
                continue
            cands.append((gap(fd, ym(w["received"])), rare, w))
        # Some companies file under a name this pass cannot reach from the
        # payee: ATW Ohio's notice is filed by its PJ Trailer subsidiary and
        # William R Hague's by its parent A.O. Smith. 35_warn_join.py searches
        # the payee AND the parent and a human verified those matches, so where
        # this pass finds nothing its answer is used rather than recording a
        # missing notice that is not missing.
        if not cands and f["recipient_id"] in joined:
            w = joined[f["recipient_id"]]
            cands = [(gap(fd, ym(w["received"])), weight.get("", 9) or 9, w)]
        cands.sort(key=lambda x: (x[0], x[1]))
        # a revision loses to the full notice it revises, when one is nearby
        if cands and is_revision(cands[0][2]["employer"]):
            full = [c for c in cands[1:]
                    if not is_revision(c[2]["employer"]) and abs(c[0] - cands[0][0]) <= 6]
            if full:
                best = max(full, key=lambda c: headcount(c[2]["affected"]))
                cands.remove(best); cands.insert(0, best)
        if not cands:
            unmatched.append(f)
            rows.append({"recipient_id": f["recipient_id"], "name": f["name"],
                         "category": f["category"], "state_notice": "none",
                         "why_none": WHY_NO_NOTICE.get(f["name"], ""),
                         "warn_year": "", "warn_employer": "", "warn_place": "",
                         "warn_affected": "", "warn_received": "", "warn_pdf": "",
                         "months_from_event": "", "name_rarity": "",
                         "notice_at_funded_site": "", "other_notices": ""})
            continue
        months, rare, w = cands[0]
        at_funded = site_agrees(paid_city.get(f["recipient_id"], set()), w["place"], cmap)
        others = "; ".join(f"{c[2]['year']} {c[2]['employer']} {c[2]['place']} "
                           f"aff {c[2]['affected']} rec {c[2]['received']}"
                           for c in cands[1:4])
        rows.append({"recipient_id": f["recipient_id"], "name": f["name"],
                     "category": f["category"], "state_notice": "matched", "why_none": "",
                     "warn_year": w["year"], "warn_employer": w["employer"],
                     "warn_place": w["place"], "warn_affected": w["affected"],
                     "warn_received": w["received"], "warn_pdf": w["pdf"],
                     "months_from_event": months, "name_rarity": rare,
                     "notice_at_funded_site": at_funded,
                     "other_notices": others})

    for r in rows:
        if r["state_notice"] == "matched":
            print(f"  matched  {r['name'][:30]:30s} <- {r['warn_year']:>7s} "
                  f"{r['warn_employer'][:32]:32s} {r['warn_place'][:22]:22s} "
                  f"aff {r['warn_affected'][:22]:22s} {r['months_from_event']}mo "
                  f"rare={r['name_rarity']}"
                  + ("   <- check this one, the notice is years from the event"
                     if int(r["months_from_event"]) > 24 else ""))
    print()
    for r in rows:
        if r["state_notice"] == "none":
            print(f"  NO NOTICE {r['name'][:30]:30s} "
                  + ("reason recorded" if r["why_none"] else "*** NO REASON RECORDED ***"))

    pre = [f for f in fails if (ym(f["event_date"]) or (9999, 1))[0] < FIRST_YEAR]
    print(f"\n{sum(1 for r in rows if r['state_notice']=='matched')} of {len(fails)} "
          f"closures and mass layoffs tie to the employer's own notice to the state")
    if pre:
        print(f"{len(pre)} fall before {FIRST_YEAR}, which the state does not publish: "
              + ", ".join(f["name"] for f in pre))
    no_reason = [r["name"] for r in rows if r["state_notice"] == "none" and not r["why_none"]]
    if no_reason:
        sys.exit(f"\nno reason recorded for the missing notice: {no_reason}")

    if "--write" not in argv:
        print("\n(not written; pass --write)")
        return
    with OUT.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    print(f"\nwrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main(sys.argv[1:])
