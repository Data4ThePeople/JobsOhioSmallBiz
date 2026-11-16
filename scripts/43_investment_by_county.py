#!/usr/bin/env python3
"""Place every JobsOhio dollar in an Ohio county, or say it cannot be placed.

The map asks whether investment goes where it is needed most, which requires
knowing where it went. That is harder than it sounds and the difficulty is the
reason this map is at county level rather than census tract.

**The payee address is not the project.** Every one of the 2,415 payments has a
street and a zip, but that is where the cheque was posted. $390 million, 28.5%
of the dollars, went to an address outside Ohio: Intel's $125,415,416 to Santa
Clara, Bechtel's $20,000,000 to Houston. And among Ohio addresses, one in ten
is the wrong county, because the cheque went to a head office: FirstEnergy's
$12,408,019 went to Akron for a project in Belmont.

So the order of preference here is:

  1. **JobsOhio's own project county**, from its monthly project reports
     (`commitments_norm.csv`). This is the only source that says where the
     project was meant to be. It covers about three quarters of the dollars.
  2. **The payee address county**, but only where that address is in Ohio and
     no project county is known. Better than nothing and wrong one time in ten.
  3. **Unplaceable.** Out-of-state payee, no project record. Reported, never
     dropped silently, and never spread around.

A project recorded across several counties ("Lorain and Cuyahoga") has its
money split evenly between them rather than counted in both, so the state
total still adds up.

Writes data/geo/investment_by_county.csv.

Usage: 43_investment_by_county.py
"""
import csv, re, sys, warnings
from collections import defaultdict
from pathlib import Path
warnings.filterwarnings("ignore")
import geopandas as gpd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from names import normalize_name

OUT = ROOT / "data" / "geo" / "investment_by_county.csv"
COUNTIES = ROOT / "data" / "geo" / "cb_2023_us_county_20m.zip"
NOT_A_COUNTY = {"", "various", "statewide", "multiple", "various cities", "n/a"}


def real_counties():
    """The 88. Everything placed has to land on one of them."""
    g = gpd.read_file(COUNTIES)
    return set(g[g.STATEFP == "39"].NAME)


def split_counties(cell, real):
    """County names out of one cell of JobsOhio's project reports.

    Two things make this more than a split. The reports join counties with an
    ampersand and not the word "and", so splitting on "and" alone invented
    counties called "Scioto &" and "Clermont &". And the PDF parse truncates:
    "Montgomer", "Tuscaraw". Both silently created places that are not in Ohio
    and quietly took $9,772,327 off the map with them, so every piece is
    checked against the real 88 and anything that still does not match is
    returned as unresolved rather than mapped.
    """
    out, bad = set(), []
    for piece in re.split(r"\band\b|&|[,/]", cell or ""):
        k = piece.strip().title()
        if not k or k.lower() in NOT_A_COUNTY:
            continue
        if k in real:
            out.add(k); continue
        # two counties with the separator lost: "Cuyahoga Summit"
        parts = k.split()
        if len(parts) > 1 and all(x in real for x in parts):
            out.update(parts); continue
        # a truncated name, if exactly one real county starts with it
        hits = [c for c in real if c.lower().startswith(k.lower())]
        if len(hits) == 1:
            out.add(hits[0]); continue
        # a transposition: Hamliton. Only accept a single candidate at
        # edit distance one, so this cannot quietly invent a county.
        near = [c for c in real if len(c) == len(k) and
                sum(a != b for a, b in zip(c.lower(), k.lower())) == 2]
        if len(near) == 1:
            out.add(near[0])
        else:
            bad.append(k)
    return out, bad


def county_from_places():
    """city -> county for Ohio, 1,243 places.

    Built by `44_place_county.py` from the Census places gazetteer, by taking
    each place's published centre point and asking which county polygon it
    falls inside. The first version of this used the WARN register, which
    doubles as a city-county table but only covers the 250 towns that have had
    a mass layoff since 2020, and that left 61 Ohio towns and $20,180,560
    unplaceable.
    """
    f = ROOT / "data" / "geo" / "place_county_oh.csv"
    if not f.exists():
        return {}
    return {r["place"]: r["county"] for r in csv.DictReader(f.open())}


def county_from_warn():
    """The register's own city-county pairs, as a second pass for anywhere the
    gazetteer spells differently."""
    out = {}
    f = ROOT / "data" / "warn" / "notices.csv"
    if not f.exists():
        return out
    for w in csv.DictReader(f.open()):
        if "/" in (w["place"] or ""):
            city, county = w["place"].rsplit("/", 1)
            city = re.sub(r"[^a-z ]", "", city.strip().lower()).strip()
            county = county.strip().title()
            if city and county and "unknown" not in county.lower():
                out.setdefault(city, county)
    return out


def main():
    par = list(csv.DictReader((ROOT / "data" / "parents.csv").open()))
    fails = {r["recipient_id"]: r for r in
             csv.DictReader((ROOT / "data" / "failures.csv").open())
             if r["verdict"] == "Confirmed failure"}

    real = real_counties()
    proj, unresolved = defaultdict(set), defaultdict(int)
    for c in csv.DictReader((ROOT / "data" / "commitments_norm.csv").open()):
        if c["company"].strip() and c["county"].strip():
            got, bad = split_counties(c["county"], real)
            proj[normalize_name(c["company"])] |= got
            for b in bad:
                unresolved[b] += 1
    if unresolved:
        print("county names that match no Ohio county and were not mapped: "
              + ", ".join(f"{k} ({n})" for k, n in
                          sorted(unresolved.items(), key=lambda kv: -kv[1])[:8]))

    cmap = {**county_from_warn(), **county_from_places()}
    agg = defaultdict(lambda: {"cash": 0.0, "n": 0, "failed_cash": 0.0, "failed_n": 0,
                               "basis": set(), "names": []})
    unplaced = []
    for p in par:
        cash = int(p["total_cash"] or 0)
        if cash <= 0:
            continue
        counties = (proj.get(normalize_name(p["name"]))
                    or proj.get(normalize_name(p.get("parent") or "")))
        basis = "JobsOhio project record"
        if not counties and p["state"].strip().upper() == "OH":
            city = re.sub(r"[^a-z ]", "", p["city"].strip().lower()).strip()
            c = cmap.get(city)
            if c and c not in real:
                c = None
            if c:
                counties, basis = {c}, "payee address"
        if not counties:
            unplaced.append((cash, p["name"], p["city"], p["state"]))
            continue
        failed = p["recipient_id"] in fails
        share = cash / len(counties)
        for c in counties:
            a = agg[c]
            a["cash"] += share; a["n"] += 1; a["basis"].add(basis)
            a["names"].append(p["name"])
            if failed:
                a["failed_cash"] += share; a["failed_n"] += 1

    placed = sum(a["cash"] for a in agg.values())
    lost = sum(c for c, *_ in unplaced)
    print(f"{len(agg)} Ohio counties carry money")
    print(f"  placed    ${placed:>14,.0f}")
    print(f"  unplaced  ${lost:>14,.0f}  ({len(unplaced)} recipients, "
          f"{lost/(placed+lost):.1%} of the total)")
    print("\n  biggest unplaced, all of them out-of-state payees with no project record:")
    for cash, n, city, st in sorted(unplaced, reverse=True)[:8]:
        print(f"    ${cash:>12,}  {n[:32]:32s} {city}, {st}")

    rows = []
    for c, a in sorted(agg.items(), key=lambda kv: -kv[1]["cash"]):
        rows.append({"county": c, "cash": round(a["cash"]), "recipients": a["n"],
                     "failed_cash": round(a["failed_cash"]), "failed_recipients": a["failed_n"],
                     "basis": "; ".join(sorted(a["basis"])),
                     "top": "; ".join(sorted(set(a["names"]))[:4])})
    with OUT.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    print(f"\n  top ten counties by dollars placed:")
    for r in rows[:10]:
        print(f"    {r['county']:<14s} ${r['cash']:>12,}  {r['recipients']:>4} recipients"
              + (f"   {r['failed_recipients']} failed, ${r['failed_cash']:,}"
                 if r["failed_recipients"] else ""))
    print(f"\nwrote {OUT.relative_to(ROOT)}")
    print(f"counties with at least one confirmed failure: "
          f"{sum(1 for r in rows if r['failed_recipients'])}")


if __name__ == "__main__":
    main()
