#!/usr/bin/env python3
"""Scan every JobsOhio grant recipient for a federal bankruptcy filing after
its first grant, using CourtListener's public search over PACER dockets
(RECAP). Writes data/bankruptcy_candidates.csv for hand or agent verification.

Method: query the payee name as an exact phrase, keep results from bankruptcy
courts ("Bankr.") filed in or after the first grant year, and require the case
name to carry the recipient's distinctive words so unrelated cases drop out.
A hit is a candidate, not a finding: company names repeat across states, so
each one is checked before it is used.

Limits worth stating in the post: RECAP holds the dockets someone has paid to
fetch, so coverage of small cases is uneven; state-court receiverships and
assignments for benefit of creditors (how several Ohio companies wind down)
never appear; and a parent's filing may not name the subsidiary that got the
grant.

Usage: 16_bankruptcy_scan.py [--start N] [--limit N] [--sleep 2.0]
"""
import csv, html, re, subprocess, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from names import name_tokens, normalize_name

PARENTS = ROOT / "data" / "parents.csv"
OUT = ROOT / "data" / "bankruptcy_candidates.csv"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/128.0 Safari/537.36"
MONTHS = {m: i for i, m in enumerate(
    "January February March April May June July August September October November December".split(), 1)}


def fetch(query):
    url = f"https://www.courtlistener.com/?q=%22{query.replace(' ', '+')}%22&type=r&order_by=dateFiled+desc"
    for attempt in range(3):
        p = subprocess.run(["curl", "-s", "--max-time", "45", "-A", UA, url], capture_output=True, text=True)
        if p.returncode == 0 and "Results" in p.stdout:
            return p.stdout
        time.sleep(5 * (attempt + 1))
    return ""


def parse(page):
    out = []
    for block in re.findall(r"<article[^>]*>(.*?)</article>", page, re.S):
        text = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", block)))
        court = re.search(r"\(([^)]*?)\s+(\d{4})\)", text)
        filed = re.search(r"Date Filed: (\w+) (\d+)\w\w, (\d{4})", text)
        docket = re.search(r"Docket Number: ([\w:\-]+)", text)
        case = text.split(" (")[0].strip()
        if not (court and filed):
            continue
        out.append({"case": case[:90], "court": court.group(1).strip(),
                    "filed": f"{filed.group(3)}-{MONTHS[filed.group(1)]:02d}-{int(filed.group(2)):02d}",
                    "docket": docket.group(1) if docket else "", "snippet": text[:200]})
    return out


def main(args):
    start = int(args[args.index("--start") + 1]) if "--start" in args else 0
    limit = int(args[args.index("--limit") + 1]) if "--limit" in args else 10**9
    sleep = float(args[args.index("--sleep") + 1]) if "--sleep" in args else 2.0

    rows = [r for r in csv.DictReader(PARENTS.open()) if int(r["total_cash"]) > 0]
    # one query per distinct payee name; the payee is the entity that took the money
    seen, queries = set(), []
    for r in rows:
        key = normalize_name(r["name"])
        if not key or key in seen:
            continue
        seen.add(key)
        queries.append(r)
    queries.sort(key=lambda r: -int(r["total_cash"]))
    queries = queries[start:start + limit]

    done = {}
    if OUT.exists():
        done = {r["recipient_id"]: r for r in csv.DictReader(OUT.open())}
    out_rows = list(done.values())
    for i, r in enumerate(queries, 1):
        if r["recipient_id"] in done:
            continue
        first_year = int(min(r["years"].split()))
        toks = name_tokens(r["name"])
        # query the distinctive words, not the full legal name: an exact-phrase
        # search for "PETMIN USA INC" misses the docket "Petmin USA, Inc."
        query = " ".join(normalize_name(r["name"]).split()[:3])
        if not query:
            continue
        page = fetch(query)
        hits = []
        for h in parse(page):
            if "Bankr" not in h["court"]:
                continue
            if int(h["filed"][:4]) < first_year:
                continue
            ct = name_tokens(h["case"])
            if not toks or not (toks & ct) or len(toks & ct) < min(2, len(toks)):
                continue
            hits.append(h)
        out_rows.append({
            "recipient_id": r["recipient_id"], "name": r["name"], "parent": r["parent"],
            "total_cash": r["total_cash"], "grant_years": r["years"], "first_year": first_year,
            "n_hits": len(hits),
            "cases": " | ".join(f"{h['case']} ({h['court']}, {h['filed']}, {h['docket']})" for h in hits[:3]),
        })
        if hits:
            print(f"  HIT {r['name'][:40]:40s} ${int(r['total_cash']):>10,} -> {out_rows[-1]['cases'][:140]}", flush=True)
        if i % 25 == 0:
            with OUT.open("w", newline="") as fh:
                w = csv.DictWriter(fh, fieldnames=list(out_rows[0])); w.writeheader(); w.writerows(out_rows)
            print(f"  ... {i}/{len(queries)} scanned, {sum(1 for x in out_rows if int(x['n_hits']))} with hits", flush=True)
        time.sleep(sleep)
    with OUT.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out_rows[0])); w.writeheader(); w.writerows(out_rows)
    print(f"wrote {OUT.name}: {len(out_rows)} recipients scanned, {sum(1 for x in out_rows if int(x['n_hits']))} with candidate filings")


if __name__ == "__main__":
    main(sys.argv[1:])
