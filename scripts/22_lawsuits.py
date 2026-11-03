#!/usr/bin/env python3
"""Match JobsOhio's own lawsuits to the grants it paid.

A party-name search of the Franklin County Court of Common Pleas returns every
matter JobsOhio is named in. Most of them are JobsOhio suing a company it had
paid, which is the only public record of JobsOhio trying to get grant money
back: the program guidelines publish a clawback for two of twelve programs,
and the individual agreements are not public.

Input:  data/research3/jobsohio_franklin_cases.csv  (case, type, role, caption,
        filed, status), from the clerk's party-name search
        data/research3/lawsuit_*.json               (per-case docket readings)
Output: data/jobsohio_lawsuits.csv

The defendant name is matched to a Schedule I recipient by normalized name,
then by token overlap, and a match is only kept when it is unambiguous. A
judgment or certificate-of-judgment matter (type CJ or CERTIFICATE) is a
collection proceeding on an earlier suit, not a new suit, and is counted
separately so the suit count is not doubled.
"""
import csv, json, re, sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from names import normalize_name, name_tokens

CASES = ROOT / "data" / "research3" / "jobsohio_franklin_cases.csv"
RES = ROOT / "data" / "research3"
PARENTS = ROOT / "data" / "parents.csv"
OUT = ROOT / "data" / "jobsohio_lawsuits.csv"

# words that carry no identity, so a match cannot rest on them alone
NOISE = {"inc", "llc", "ltd", "corp", "corporation", "company", "co", "lp", "llp",
         "holdings", "group", "the", "usa", "us", "of", "and", "industries",
         "international", "technologies", "solutions", "products", "systems",
         "enterprises", "services", "manufacturing"}


def defendant(caption):
    """The defendant side of 'JOBSOHIO -VS- X ET AL', or the debtor name."""
    parts = re.split(r"\s+-VS-\s+", caption)
    name = parts[1] if len(parts) > 1 else caption
    name = re.sub(r"^\s*DEBTOR\s+", "", name, flags=re.I)
    return re.sub(r"\s+ET\s+AL\s*$", "", name, flags=re.I).strip()


def main():
    cases = list(csv.DictReader(CASES.open()))
    parents = list(csv.DictReader(PARENTS.open()))
    by_norm = defaultdict(list)
    for p in parents:
        by_norm[normalize_name(p["name"])].append(p)

    def match(name):
        """(parent row, how) for a defendant name, or (None, '')."""
        n = normalize_name(name)
        if n in by_norm and len(by_norm[n]) == 1:
            return by_norm[n][0], "exact name"
        toks = {t for t in name_tokens(name) if t not in NOISE}
        if len(toks) < 1:
            return None, ""
        hits = []
        for p in parents:
            pt = {t for t in name_tokens(p["name"]) if t not in NOISE}
            if pt and toks and (toks <= pt or pt <= toks):
                hits.append(p)
        uniq = {h["recipient_id"]: h for h in hits}
        # a match that could be two different companies is not a match
        return (list(uniq.values())[0], "distinctive words") if len(uniq) == 1 else (None, "")

    # the docket readings, keyed by case number
    read = {}
    for f in sorted(RES.glob("lawsuit_*.json")):
        if f.stem.endswith("_input"):
            continue
        for x in json.load(f.open()):
            if x.get("case"):
                read[x["case"].replace(" ", "").upper()] = x

    rows = []
    for c in cases:
        kind = ("collection" if "JUDGMENT" in c["case_type"] or c["case"][2:4] == "JG"
                else "suit" if c["party_role"] == "PL" else "against JobsOhio")
        name = defendant(c["caption"])
        p, how = match(name)
        d = read.get(c["case"].replace(" ", "").upper(), {})
        rows.append({
            "case": c["case"], "filed": c["filed"], "year": c["filed"][-4:],
            "kind": kind, "status": c["status"], "defendant": name,
            "recipient": p["name"] if p else "", "parent": (p or {}).get("parent", ""),
            "paid": (p or {}).get("total_cash", ""), "grant_years": (p or {}).get("years", ""),
            "matched_how": how,
            "agreement": d.get("agreement", ""), "agreement_date": d.get("agreement_date", ""),
            "program": d.get("program", ""),
            "amount_sought": d.get("amount_sought", ""),
            "job_commitments": str(d.get("job_commitments", ""))[:300],
            "shortfall": str(d.get("shortfall", ""))[:300],
            "repayment_quote": str(d.get("repayment_quote", ""))[:600],
            "remedy_named": d.get("remedy_named", ""),
            "agreement_is_exhibit": d.get("agreement_is_exhibit", ""),
            "outcome": str(d.get("outcome", ""))[:200], "outcome_date": d.get("outcome_date", ""),
            "amount_recovered": str(d.get("amount_recovered", ""))[:200],
            "confidence": d.get("confidence", ""),
            "docket_read": "yes" if d else "",
            "source": str(d.get("source", ""))[:300],
            "notes": str(d.get("notes", ""))[:600],
        })

    rows.sort(key=lambda r: (r["year"], r["filed"][:5]))
    with OUT.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

    suits = [r for r in rows if r["kind"] == "suit"]
    matched = [r for r in suits if r["recipient"]]
    print(f"{len(rows)} Franklin County matters: {len(suits)} suits by JobsOhio, "
          f"{sum(1 for r in rows if r['kind'] == 'collection')} collection proceedings, "
          f"{sum(1 for r in rows if r['kind'] == 'against JobsOhio')} against JobsOhio")
    print(f"{len(matched)} of {len(suits)} defendants tie to a Schedule I recipient, "
          f"carrying ${sum(int(r['paid'] or 0) for r in matched):,} paid")
    print(f"dockets read: {sum(1 for r in rows if r['docket_read'])}\n")
    print(f"{'year':6s} {'suits':>6s} {'tied to a grant':>16s} {'paid to them':>15s}")
    for y, n in sorted(Counter(r["year"] for r in suits).items()):
        m = [r for r in matched if r["year"] == y]
        print(f"{y:6s} {n:6d} {len(m):16d} {sum(int(r['paid'] or 0) for r in m):15,}")
    read_rows = [r for r in suits if r["docket_read"]]
    if read_rows:
        quoted = [r for r in read_rows if r["repayment_quote"]]
        attached = [r for r in read_rows if str(r["agreement_is_exhibit"]).lower().startswith(("y", "true"))]
        # the `program` field is prose, and almost every entry says some form of
        # "not named", so count only the ones that actually name a published
        # program rather than trusting the absence of a negative word
        PUBLISHED = ("economic development grant", "workforce grant", "revitalization",
                     "research & development", "research and development", "inclusion grant",
                     "small business grant", "site inventory", "osip", "air service",
                     "growth fund", "vibrant community", "aerospace and defense",
                     "talent acquisition", "talent attraction")
        named = [r for r in read_rows
                 if any(p in r["program"].lower() for p in PUBLISHED)
                 and not any(neg in r["program"].lower()[:60]
                             for neg in ("not named", "never names", "names no", "no jobsohio program"))]
        amts = []
        for r in read_rows:
            m = re.search(r"\$\s*([\d,]+(?:\.\d{2})?)", r["amount_sought"] or "")
            if m:
                amts.append(float(m.group(1).replace(",", "")))
        print(f"\nof the {len(read_rows)} dockets read:")
        print(f"  {len(quoted)} complaints quote the agreement's repayment clause")
        print(f"  {len(attached)} attach the agreement as an exhibit")
        print(f"  {len(named)} name one of JobsOhio's 12 published programs")
        if amts:
            print(f"  amounts sought: ${min(amts):,.0f} to ${max(amts):,.0f}, total ${sum(amts):,.0f}")
        outcomes = Counter()
        for r in read_rows:
            o = (r["outcome"] or "").lower()
            outcomes["default judgment" if "default" in o else
                     "dismissed" if "dismiss" in o else
                     "agreed judgment" if "agreed" in o else
                     "removed to federal court" if "remov" in o else
                     "still pending" if "pend" in o or "active" in o else
                     "other or not stated"] += 1
        for k, n in outcomes.most_common():
            print(f"  {n:3d} {k}")
    unmatched = sorted({r["defendant"] for r in suits if not r["recipient"]})
    print(f"\ndefendants with no Schedule I match ({len(unmatched)}), "
          f"either paid under another name or never over $5,000:")
    for n in unmatched:
        print(f"  {n}")
    print(f"\nwrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
