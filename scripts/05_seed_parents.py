#!/usr/bin/env python3
"""Create or refresh data/parents.csv, the hand-curated crosswalk from each
Schedule I recipient to its ultimate parent, size bucket and home state.

Automated columns are recomputed on every run:
  recipient_class_auto  business / university / hospital / government / nonprofit,
                        from the IRC section and name keywords
  edgar_*               EIN match against SEC EDGAR submissions (scripts/06_edgar_ein.py)
  f5500_*               Form 5500 participant counts on the recipient EIN (scripts/07_f5500.py)
  metrics_*             program family, jobs retained, industry from the monthly reports
Hand-filled columns are preserved across runs:
  recipient_class, parent, parent_hq_state, hq_source, emp_bucket, emp_source,
  emp_asof, confidence (A/B/C/D), founded_in_ohio, notes
emp_bucket values: <100, 100-499, 500-4999, 5000+."""
import csv, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

ROOT = Path(__file__).resolve().parent.parent
RECIP = ROOT / "data" / "recipients.csv"
PARENTS = ROOT / "data" / "parents.csv"
EDGAR = ROOT / "data" / "edgar_ein_matches.csv"
F5500 = ROOT / "data" / "f5500_participants.csv"

HAND = ["recipient_class", "parent", "parent_hq_state", "hq_source", "emp_bucket",
        "emp_source", "emp_asof", "confidence", "founded_in_ohio", "notes"]
AUTO = ["recipient_id", "name", "ein", "city", "state", "irc_section", "total_cash", "n_rows", "years",
        "recipient_class_auto", "edgar_cik", "edgar_name", "edgar_name_match", "edgar_state_inc", "edgar_hq_state",
        "f5500_participants_2015", "f5500_participants_2019", "f5500_participants_2023", "f5500_sponsor", "f5500_sponsor_state",
        "metrics_company", "metrics_programs", "metrics_jobs_retained_max", "metrics_industry", "metrics_commit_total"]

UNIVERSITY = re.compile(r"\b(university|college|universities)\b(?!.*\b(tees|inc)\b)", re.I)
HOSPITAL = re.compile(r"\b(hospital|hospitals|clinic|health system|medical center|children'?s hospital|metrohealth|health network|healthcare system)\b", re.I)
GOVERNMENT = re.compile(r"\b(city of|village of|county|port authority|township|state of ohio|board of|commission|community improvement corp|cic\b|development authority|regional transit|ohio department|school district|municipal)\b", re.I)
NONPROFIT = re.compile(r"\b(foundation|institute|chamber|committee|council|coalition|team neo|one columbus|redi cincinnati|dayton development|regional growth|host committee|innovation district|nonprofit|non-profit|society|center for|consortium|economic development corp|economic development partnership|development corporation|global cleveland)\b", re.I)
SITE = re.compile(r"\b(real estate|realty|properties|property|land|development llc|developers|holdings ii|partners llc|acquisitions|investors)\b", re.I)


def recipient_class(name, irc, programs=""):
    """Seed class from the return's IRC section, the name, and (for site
    developers) the program family. Hand review can overrule it."""
    irc = (irc or "").upper()
    if UNIVERSITY.search(name):
        return "university"
    if "GOVERNMENT" in irc or "STATE OF OHIO" in irc or GOVERNMENT.search(name):
        return "government"
    if HOSPITAL.search(name):
        return "hospital"
    if "501" in irc or NONPROFIT.search(name):
        return "nonprofit"
    site_programs = {"Spec Development (OSIP)", "Vibrant Community Grant"}
    progs = {p.strip() for p in programs.split(";") if p.strip()}
    if (progs and progs <= site_programs) or SITE.search(name):
        return "site_development"
    return "business"


def load(path, key):
    if not path.exists():
        return {}
    return {r[key]: r for r in csv.DictReader(path.open())}


def main():
    recips = list(csv.DictReader(RECIP.open()))
    old = load(PARENTS, "recipient_id")
    edgar = load(EDGAR, "ein")
    f5500 = load(F5500, "ein")
    out = []
    for r in recips:
        row = {k: r.get(k, "") for k in AUTO if k in r}
        row["recipient_class_auto"] = recipient_class(r["name"], r["irc_section"])
        e = edgar.get(r["ein"], {})
        from names import score as _score
        nm = max([_score(r["name"], e.get("name", ""))] + [_score(r["name"], f) for f in e.get("former_names", "").split(" | ") if f]) if e else 0
        row["edgar_name_match"] = ("" if not e else "same name" if nm >= 0.34 else "DIFFERENT NAME: EIN reused or a parent/former filer; confirm before using")
        row.update({"edgar_cik": e.get("cik", ""), "edgar_name": e.get("name", ""),
                    "edgar_state_inc": e.get("state_inc", ""), "edgar_hq_state": e.get("hq_state", "")})
        f = f5500.get(r["ein"], {})
        for y in ("2015", "2019", "2023"):
            row[f"f5500_participants_{y}"] = f.get(f"participants_{y}", "")
        row["f5500_sponsor"] = f.get("sponsor", "")
        row["f5500_sponsor_state"] = f.get("sponsor_state", "")
        prev = old.get(r["recipient_id"], {})
        for k in HAND:
            row[k] = prev.get(k, "")
        out.append(row)
    ids = [r["recipient_id"] for r in out]
    if len(ids) != len(set(ids)):
        sys.exit("duplicate recipient ids")
    with PARENTS.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=AUTO + HAND); w.writeheader(); w.writerows(out)
    from collections import Counter
    c = Counter(r["recipient_class_auto"] for r in out)
    d = Counter()
    for r in out:
        d[r["recipient_class_auto"]] += int(r["total_cash"])
    print(f"wrote {PARENTS.name}: {len(out)} rows; hand-filled parents kept: {sum(1 for r in out if r['parent'])}")
    for k, n in c.most_common():
        print(f"  {k:12s} {n:5d} recipients  ${d[k]:>14,}")
    print(f"  EDGAR EIN matches: {sum(1 for r in out if r['edgar_cik'])}; Form 5500 matches: {sum(1 for r in out if r['f5500_sponsor'])}")


if __name__ == "__main__":
    main()
