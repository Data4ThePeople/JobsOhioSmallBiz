#!/usr/bin/env python3
"""Join Ohio's whole WARN register against every grant recipient.

The failure count in this project is a floor, not a count, because it was found
by scanning Google News headlines: a closure nobody wrote up is invisible to it.
Ohio's WARN register has no such gap. It is every qualifying closure and mass
layoff in the state, reported by the employer, under penalty of being the
employer's own filing. Joining all 810 notices against all 1,789 recipients is
the one pass that can turn the floor into something close to a count.

**This script produces candidates, not findings.** A name match is a reason to
go and check, and every match here still has to be verified the way the
existing 102 were. Nothing it outputs is published without that.

How a match is scored, and why each part is here:

  rarity   A shared word is weighed by how many distinct companies in the
           register use it. "ultium" is near proof; "logistics" is nothing. A
           first attempt at this kind of match, without weighting, paired
           Ultium Cells with American Energy Corporation on the word "energy"
           and FedEx with DHL on "supply chain". Counted over companies rather
           than over filings, because Olive AI filed three notices under three
           spellings and that made its own name look three times less
           distinctive than it is.
  places   Ohio place names are stripped out of the identity words entirely,
           using the 310 city and county words the register itself supplies.
           Without that the join reads a shared location as a shared identity
           and then scores the same signal twice: it matched CITY OF WAPAKONETA
           to an employer in Wapakoneta, GLOBAL CLEVELAND to United Airlines in
           Cleveland, and CITY OF FREMONT to a Fremont paper mill, and ranked
           all three top tier because the city also matched.
  overlap  The shared words have to cover most of at least one of the two
           names AND be distinctive. Coverage alone is not enough, because a
           name that reduces to a single ordinary word covers itself
           completely: on coverage alone the join read L Brands as Rise Brands
           on the word "brands", Carlisle as The Michaels Companies on
           "companies", and the City of Wapakoneta as Murotech Ohio on the
           word "ohio".
  place    The notice's county against the counties the grant actually funded.
           Those come from two places and need both. Schedule I gives the city
           each payment was sent to, but that is often an out-of-state head
           office: Pixelle's cheque went to Spring Grove, Pennsylvania, Morgan
           Truck Body's to New York and Dorel's to Missouri, so on payment
           address alone all three looked like failures somewhere unconnected.
           JobsOhio's own project records name the county, and they place
           Pixelle in Ross, which is exactly where its 780-job notice is. City
           names are also normalised, because Schedule I writes MT ORAB where
           the register writes Mount Orab.
  date     A notice before the grant is not a post-grant failure. Compared
           against the FIRST grant year, and anything earlier is reported
           separately rather than dropped, because "Ohio funded a company that
           had just filed a mass-layoff notice here" is its own story.
  covid    **46% of the whole register is 2020, and March to June 2020 alone is
           28% of it.** 225 notices in four months against a baseline of about
           6 a month. Those are the shutdown, and a large share were temporary
           layoffs that were recalled, so a 2020 notice is not evidence a
           company failed. Every candidate in that window is flagged and is
           held to a different standard: it needs evidence the layoff stuck.

Tiers, which are a triage order and not a verdict:

  A  rare name match AND the notice is in a city the money was paid into
  B  rare name match AND the notice is in a county the money was paid into
  C  rare name match, somewhere else in Ohio
  D  the whole name matches but every word in it is common

Writes data/warn_join.csv. Companies already in data/failures.csv are marked
rather than hidden, so the join can be checked against the hand-verified set:
if it misses one of those, the matching is too tight.

Usage: 35_warn_join.py [--write] [--min-tier C]
"""
import csv, re, sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WARN = ROOT / "data" / "warn" / "notices.csv"
PARENTS = ROOT / "data" / "parents.csv"
GRANTS = ROOT / "data" / "grants_raw.csv"
FAILURES = ROOT / "data" / "failures.csv"
OUT = ROOT / "data" / "warn_join.csv"

# Words carrying no identifying weight: legal suffixes, plus the industry nouns
# that a large share of Ohio employers share. Kept identical to 33_match_warn.py
# so the two passes cannot disagree about what counts as a name.
STOP = {"inc", "inc.", "corp", "corporation", "company", "co", "llc", "ltd", "the", "of",
        "and", "usa", "holdings", "group", "us", "incorporated", "lp", "plc", "llp",
        "north", "america", "american", "supply", "chain", "logistics", "services",
        "service", "health", "care", "system", "energy", "international", "industries",
        "products", "solutions", "technologies", "manufacturing", "enterprises",
        "partners", "global", "limited", "center", "centers",
        # singular forms of the above: "enterprises" was stopped but
        # "enterprise" was not, which read RL Cole Enterprise as Enterprise
        # Holdings, the car rental company
        "enterprise", "industry", "product", "solution", "technology", "partner",
        # "doing business as" joins two names for the same company, and counting
        # it as a third name diluted Technicote below the overlap threshold:
        # "Technicote Inc dba Beontag" scored 0.33 where it should score 0.50
        "dba", "fka", "aka", "formerly", "with"}
RARE = 2          # a word used by this many companies or fewer is distinctive
COVER = 0.6       # the shared words must cover this much of one name
UPDATE = re.compile(r"^\s*(update|revised)?\s*\d*\s*(update|revised)?\b[:\s-]*", re.I)


def words(s):
    return [w for w in re.split(r"[^a-z0-9]+", (s or "").lower())
            if w and w not in STOP and len(w) > 2]


PARENS = re.compile(r"\s*\([^)]*\)")


def toks(s, places=frozenset(), strip_parens=False):
    """The identity words in a name: no legal suffixes, no industry nouns, and
    no Ohio place names, since where a company is gets scored separately.

    `strip_parens` is for THIS PROJECT'S `parent` column only, which carries
    research prose in brackets. Those words count as part of the name unless
    they come out: "Bitwise Industries (joint venture with ProMedica Health
    System)" diluted the one word that identifies it, bitwise, from 1.00 to
    0.20 and dropped a $1,500,000 recipient out of the join altogether. The
    project already strips parentheses this way when it merges duplicate
    parent names, so this makes the two passes agree.

    It is deliberately NOT applied to the employer names in the register,
    where a bracket usually holds a real alternate name rather than prose
    ("Shutterfly Lifetouch LLC (Lifetouch Church Directories)"). Stripping
    those as well read Stride Tool as Stride, Inc., two unrelated companies.
    """
    if strip_parens:
        s = PARENS.sub(" ", s or "")
    return {w for w in words(s) if w not in places}


def year_of(s):
    m = re.search(r"(\d{4})", s or "")
    if m:
        return int(m.group(1))
    m = re.match(r"\d{1,2}/\d{1,2}/(\d{2})$", (s or "").strip())
    return 2000 + int(m.group(1)) if m else None


def place_words(warn):
    """Every city and county word the register uses, which is the best list of
    Ohio place names available here and costs no extra source."""
    out = set()
    for w in warn:
        if "/" in (w["place"] or ""):
            for part in re.split(r"[^A-Za-z]+", w["place"].replace("/", " ")):
                if len(part) > 2:
                    out.add(part.lower())
    return out


def covid_window(received):
    """March to June 2020, when Ohio took 225 notices against a normal six a
    month. A notice here says a plant shut for the pandemic, which is not the
    same claim as a company failing after taking public money."""
    m = re.match(r"(\d{1,2})/\d{1,2}/(\d{2,4})$", (received or "").strip())
    if not m:
        return False
    y = int(m.group(2))
    y = y + 2000 if y < 100 else y
    return y == 2020 and 3 <= int(m.group(1)) <= 6


def headcount(s):
    m = re.search(r"\d[\d,]*", s or "")
    return int(m.group(0).replace(",", "")) if m else 0


ABBREV = {"mt": "mount", "st": "saint", "ft": "fort", "hts": "heights",
          "twp": "township", "n": "north", "s": "south", "e": "east", "w": "west"}


def norm_city(c):
    """Schedule I and the register spell the same town differently: MT ORAB
    against Mount Orab, ST MARYS against Saint Marys."""
    out = []
    for w in re.split(r"[^a-z0-9]+", (c or "").lower()):
        if w:
            out.append(ABBREV.get(w, w))
    return " ".join(out)


def split_place(place):
    """("city", "county") from Ohio's "Canton/Stark". Whitespace is collapsed
    first because a few rows carry an embedded newline from the source CSV."""
    place = re.sub(r"\s+", " ", place or "").strip()
    if "/" not in place:
        return "", ""
    city, county = place.rsplit("/", 1)
    return norm_city(city), county.strip().lower()


def main(argv):
    warn = list(csv.DictReader(WARN.open()))
    parents = list(csv.DictReader(PARENTS.open()))
    checked = {r["recipient_id"]: r for r in csv.DictReader(FAILURES.open())}

    # every city Schedule I paid each recipient at, and the county it sits in
    cities = defaultdict(set)
    for g in csv.DictReader(GRANTS.open()):
        ein = re.sub(r"\D", "", g["recipient_ein"] or "")
        rid = f"EIN:{ein}" if len(ein) == 9 and ein.strip("0") else ""
        if rid and g["city"] and (g["state"] or "").upper() == "OH":
            cities[rid].add(norm_city(g["city"]))
    # the register doubles as a city -> county table for Ohio
    county_of = {}
    for w in warn:
        c, k = split_place(w["place"])
        if c and k and "unknown" not in k:
            county_of.setdefault(c, k)

    places = place_words(warn)

    # One company, not one filing. Olive AI appears as "Olive AI, Inc.",
    # "Olive AI, Inc" and "Olive", and counting those as three employers made
    # its own name look three times more common than it is.
    companies = {frozenset(toks(UPDATE.sub("", w["employer"]), places)) for w in warn}
    # The counties JobsOhio's own project records put each company in. This is
    # the only source that says where a grant was MEANT to land, as against
    # where the cheque was posted, and it is matched on the same identity words
    # the notices are so the two passes cannot disagree about what a name is.
    funded_counties = defaultdict(set)
    com_path = ROOT / "data" / "commitments_norm.csv"
    if com_path.exists():
        com = []
        for c in csv.DictReader(com_path.open()):
            t = toks(c["company"], places, strip_parens=True)
            if t and c["county"]:
                # "Lorain and Cuyahoga" is two counties in one cell
                cs = {x.strip().lower() for x in re.split(r"\band\b|[,/]", c["county"])
                      if x.strip()}
                com.append((t, cs))
        for p_ in parents:
            pt_all = (toks(p_["name"], places)
                      | toks(p_.get("parent", ""), places, strip_parens=True))
            if not pt_all:
                continue
            for t, cs in com:
                inter = t & pt_all
                if not inter:
                    continue
                lo = min(len(inter) / len(t), len(inter) / len(pt_all))
                if lo >= 0.6:
                    funded_counties[p_["recipient_id"]] |= cs

    weight = Counter()
    for c in companies:
        for t in c:
            weight[t] += 1

    indexed = [(toks(UPDATE.sub("", w["employer"]), places), w) for w in warn]

    rows = []
    for p in parents:
        rid = p["recipient_id"]
        # the payee and its parent are matched separately, so the row can say
        # which name actually matched rather than blurring the two
        cands = {("payee", p["name"]), ("parent", (p.get("parent") or "").strip())}
        sides = [(lab, toks(n, places, strip_parens=(lab == "parent")))
                 for lab, n in cands if n]
        sides = [(lab, t) for lab, t in sides if t]
        if not sides:
            continue
        paid_cities = cities.get(rid, set())
        # Where the money landed, preferring the payment address and falling
        # back to JobsOhio's project county only when every payment went out of
        # state. The fallback has to be a fallback: a commitment is a county
        # JobsOhio promised money to, not one it paid, and New Horizons Baking
        # has a Toledo commitment that Schedule I shows was never paid, so
        # using it unconditionally promoted a known different-site case.
        if paid_cities:
            paid_counties = {county_of[c] for c in paid_cities if c in county_of}
            place_basis = "payment address"
        else:
            paid_counties = funded_counties.get(rid, set())
            place_basis = "JobsOhio project county (paid out of state)"
        first_year = min((int(y) for y in (p.get("years") or "").split() if y.isdigit()),
                         default=None)
        for wt, w in indexed:
            if not wt:
                continue
            best = None
            for lab, pt in sides:
                inter = wt & pt
                if not inter:
                    continue
                rare = min(weight[t] for t in inter)
                # how much of each name the shared words account for
                c_emp, c_rec = len(inter) / len(wt), len(inter) / len(pt)
                hi, lo = max(c_emp, c_rec), min(c_emp, c_rec)
                # words shared that few companies in the register use at all
                distinctive = sum(1 for t in inter if weight[t] <= RARE)
                ok = (
                    # two distinctive words in common is close to proof
                    distinctive >= 2
                    # one distinctive word, and it accounts for most of both
                    or (distinctive == 1 and hi >= COVER and lo >= 0.5)
                    # or the two names are the same name, whatever the words
                    or (hi >= 0.99 and lo >= COVER)
                )
                if not ok:
                    continue
                score = (distinctive, hi, -rare, len(inter))
                if best is None or score > best[0]:
                    best = (score, lab, inter, rare, lo, hi, distinctive)
            if best is None:
                continue
            _, matched_on, inter, rare, lo, hi, distinctive = best
            city, county = split_place(w["place"])
            if city and city in paid_cities:
                tier = "A"
            elif county and county in paid_counties:
                tier = "B"
            elif rare <= RARE:
                tier = "C"
            else:
                tier = "D"
            ny = year_of(w["received"])
            rows.append({
                "tier": tier, "recipient_id": rid, "recipient": p["name"],
                "parent": p.get("parent", ""), "total_cash": p.get("total_cash", ""),
                "grant_years": p.get("years", ""),
                "warn_year": w["year"], "warn_employer": w["employer"],
                "warn_place": w["place"], "warn_affected": w["affected"],
                "warn_received": w["received"], "warn_pdf": w["pdf"],
                "shared_words": " ".join(sorted(inter)), "rarity": rare,
                "distinctive_words": distinctive, "matched_on": matched_on,
                "name_overlap": f"{lo:.2f}-{hi:.2f}",
                "place_basis": place_basis if tier in ("A", "B") else "",
                "covid_window": "yes" if covid_window(w["received"]) else "",
                "affected_n": headcount(w["affected"]),
                "notice_after_first_grant": ("" if not (ny and first_year)
                                             else "yes" if ny >= first_year else "no"),
                "already_checked": checked.get(rid, {}).get("verdict", ""),
            })

    order = {"A": 0, "B": 1, "C": 2, "D": 3}
    rows.sort(key=lambda r: (order[r["tier"]], -int(r["total_cash"] or 0)))

    # --- report -------------------------------------------------------------
    by_tier = Counter(r["tier"] for r in rows)
    print(f"{len(warn)} notices against {len(parents)} recipients: {len(rows)} name matches")
    print("  " + ", ".join(f"tier {t} {by_tier[t]}" for t in "ABCD" if by_tier[t]))

    # Does the join find the closures that were already verified by hand? If
    # it misses one, the matching is too tight and the new candidates cannot be
    # trusted. Tier is NOT the test: four of the verified set are known to have
    # failed away from the site the money reached, so tier C is the right
    # answer for them and a tier A would mean the place scoring was broken.
    want = {r["recipient_id"] for r in checked.values()
            if r["category"] in ("Funded site closed", "Mass layoff at the funded site",
                                 "Failed away from the funded site")
            and year_of(r["event_date"]) and year_of(r["event_date"]) >= 2020}
    no_notice = {r["recipient_id"] for r in
                 csv.DictReader((ROOT / "data" / "failure_warn.csv").open())
                 if r["state_notice"] == "none"} if (ROOT / "data" / "failure_warn.csv").exists() else set()
    should_find = want - no_notice
    found = {r["recipient_id"] for r in rows}
    print(f"\nrecall: {len(should_find & found)} of {len(should_find)} hand-verified "
          f"closures that have a state notice are found")
    missed = should_find - found
    if missed:
        print("  MISSED, so the matching is too tight: "
              + ", ".join(checked[m]["name"] for m in missed))
    if want & no_notice:
        print(f"  ({len(want & no_notice)} more are verified failures with no notice in the "
              f"register at all, so nothing here could find them)")
    at = Counter(min((r["tier"] for r in rows if r["recipient_id"] == k), default="-")
                 for k in should_find)
    print("  they land at: " + ", ".join(f"tier {t} {n}" for t, n in sorted(at.items())))

    new = [r for r in rows if not r["already_checked"]
           and r["notice_after_first_grant"] == "yes" and r["tier"] in ("A", "B")]

    def show(group, title):
        """One line per recipient, showing its BIGGEST notice.

        An earlier version showed whichever notice happened to sort first,
        which badly understated three companies: ProMedica appeared as a
        6-person notice when it also filed one for 189, INOAC as 1 when it also
        filed 174, and Sherwin-Williams as 2 when it also filed 51. A triage
        list that hides the large notice is worse than no triage list.
        """
        best = {}
        for r in group:
            k = r["recipient_id"]
            if k not in best or r["affected_n"] > best[k]["affected_n"]:
                best[k] = r
        print(f"\n{len(best)} {title}")
        n_each = Counter(r["recipient_id"] for r in group)
        for r in sorted(best.values(), key=lambda x: -x["affected_n"]):
            more = n_each[r["recipient_id"]] - 1
            print(f"  {r['tier']}  {r['affected_n']:>5} jobs  "
                  f"${int(r['total_cash'] or 0):>11,}  {r['recipient'][:29]:29s} "
                  f"grants {r['grant_years'][:14]:14s} <- {r['warn_employer'][:30]:30s} "
                  f"{r['warn_place'][:20]:20s} {r['warn_received'][:10]}"
                  + (f"  (+{more} more notices)" if more else ""))

    show([r for r in new if not r["covid_window"]],
         "recipients to check: a notice after the grant, outside the pandemic window")
    show([r for r in new if r["covid_window"]],
         "more in March-June 2020, which is the shutdown and needs a higher bar")

    before = [r for r in rows if r["tier"] in ("A", "B")
              and r["notice_after_first_grant"] == "no"]
    if before:
        show(before, "filed a mass-layoff notice BEFORE Ohio first paid them, which is "
                     "its own question (most are the 2020 shutdown; the later ones are not)")

    if "--write" not in argv:
        print("\n(not written; pass --write)")
        return
    with OUT.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    print(f"\nwrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main(sys.argv[1:])
