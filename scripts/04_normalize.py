#!/usr/bin/env python3
"""Build data/recipients.csv: one row per distinct Schedule I recipient entity,
keyed by EIN when the return gives one and by normalized name otherwise, with
totals across years. Then attach the monthly-metrics side: program family,
commitment total, jobs retained, industry, by conservative name matching.

Also writes data/commitments_norm.csv (program family and dollars parsed) and
prints coverage: how many recipients and how many dollars matched a metrics
record, and how many metrics grant companies have no Schedule I recipient."""
import csv, re, sys
from collections import defaultdict, Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from names import normalize_name, best_match, program_family, name_tokens

ROOT = Path(__file__).resolve().parent.parent
GRANTS = ROOT / "data" / "grants_raw.csv"
COMMIT = ROOT / "data" / "commitments.csv"
OUT = ROOT / "data" / "recipients.csv"
COMMIT_OUT = ROOT / "data" / "commitments_norm.csv"


def dollars(s):
    s = re.sub(r"[^\d.]", "", s or "")
    if not s:
        return 0
    return int(round(float(s)))


def intval(s):
    s = re.sub(r"[^\d]", "", s or "")
    return int(s) if s else None


def main():
    grants = list(csv.DictReader(GRANTS.open()))
    by_key = defaultdict(list)
    for g in grants:
        ein = re.sub(r"\D", "", g["recipient_ein"])
        key = f"EIN:{ein}" if len(ein) == 9 and ein.strip("0") else f"NAME:{normalize_name(g['recipient_name'])}"
        by_key[key].append(g)
    recipients = []
    for key, rows in by_key.items():
        rows.sort(key=lambda r: (int(r["fiscal_year"]), int(r["row_in_filing"])))
        latest = rows[-1]
        names = Counter(r["recipient_name"] for r in rows)
        recipients.append({
            "recipient_id": key,
            "name": latest["recipient_name"],
            "all_names": " | ".join(sorted(names)),
            "ein": key[4:] if key.startswith("EIN:") else "",
            "city": latest["city"], "state": latest["state"], "zip": latest["zip"][:5],
            "irc_section": latest["irc_section"],
            "first_fy": rows[0]["fiscal_year"], "last_fy": latest["fiscal_year"],
            "years": " ".join(sorted({r["fiscal_year"] for r in rows})),
            "n_rows": len(rows),
            "total_cash": sum(int(r["cash_amt"]) for r in rows),
        })
    # duplicate check: two keys must not share an EIN
    eins = [r["ein"] for r in recipients if r["ein"]]
    if len(eins) != len(set(eins)):
        sys.exit("duplicate EIN keys")

    commits = list(csv.DictReader(COMMIT.open()))
    for c in commits:
        c["value"] = dollars(c["program_value"])
        c["program_family"] = program_family(c["program"], c["value"])
        c["company_norm"] = normalize_name(c["company"])
        c["jobs_retained_n"] = intval(c["jobs_retained"])
        c["jobs_created_n"] = intval(c["jobs_created"])
        c["investment_n"] = dollars(c["investment"]) if c["investment"].startswith("$") else None
    with COMMIT_OUT.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(commits[0])); w.writeheader(); w.writerows(commits)
    fam = Counter(c["program_family"] for c in commits)
    print("program families:", fam.most_common())

    # per company (normalized name) on the metrics side
    by_co = defaultdict(list)
    for c in commits:
        if c["company_norm"]:
            by_co[c["company_norm"]].append(c)
    cands = [(k, k) for k in by_co]
    # index candidates by token to keep matching fast
    index = defaultdict(set)
    for k in by_co:
        for t in name_tokens(k):
            index[t].add(k)

    matched_n = matched_dollars = 0
    for r in recipients:
        toks = name_tokens(r["name"])
        pool = set()
        for t in toks:
            pool |= index.get(t, set())
        m = best_match(r["name"], [(k, k) for k in pool], threshold=0.6) if pool else None
        r["metrics_company"] = r["metrics_programs"] = r["metrics_industry"] = ""
        r["metrics_match_score"] = ""
        r["metrics_commit_total"] = r["metrics_jobs_retained_max"] = r["metrics_jobs_created_sum"] = ""
        r["metrics_months"] = ""
        if m:
            k, s = m
            rows = by_co[k]
            r["metrics_company"] = rows[0]["company"]
            r["metrics_match_score"] = f"{s:.2f}"
            r["metrics_programs"] = "; ".join(sorted({c["program_family"] for c in rows}))
            r["metrics_industry"] = Counter(c["industry"] for c in rows if c["industry"]).most_common(1)[0][0] if any(c["industry"] for c in rows) else ""
            r["metrics_commit_total"] = sum(c["value"] for c in rows)
            jr = [c["jobs_retained_n"] for c in rows if c["jobs_retained_n"] is not None]
            jc = [c["jobs_created_n"] for c in rows if c["jobs_created_n"] is not None]
            r["metrics_jobs_retained_max"] = max(jr) if jr else ""
            r["metrics_jobs_created_sum"] = sum(jc) if jc else ""
            r["metrics_months"] = " ".join(sorted({c["report_month"] for c in rows if c["report_month"]}))
            matched_n += 1; matched_dollars += r["total_cash"]

    recipients.sort(key=lambda r: -r["total_cash"])
    with OUT.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(recipients[0])); w.writeheader(); w.writerows(recipients)
    tot = sum(r["total_cash"] for r in recipients)
    print(f"wrote {OUT.name}: {len(recipients)} recipients, ${tot:,} from {len(grants)} rows")
    print(f"matched to metrics: {matched_n} recipients ({matched_n/len(recipients):.0%}), ${matched_dollars:,} ({matched_dollars/tot:.0%} of dollars)")
    # reverse coverage: metrics grant companies (not loans) with no Schedule I match
    grant_cos = {k for k, rows in by_co.items() if any("Loan" not in c["program_family"] for c in rows)}
    matched_cos = {normalize_name(r["metrics_company"]) for r in recipients if r["metrics_company"]}
    print(f"metrics grant companies: {len(grant_cos)}, of which unmatched to any 990 recipient: {len(grant_cos - matched_cos)}")


if __name__ == "__main__":
    main()
