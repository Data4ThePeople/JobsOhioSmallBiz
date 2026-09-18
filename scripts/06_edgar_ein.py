#!/usr/bin/env python3
"""Match Schedule I recipient EINs to SEC registrants using the EDGAR bulk
submissions archive (data/raw/edgar/submissions.zip, ~1M JSON files).

Writes data/edgar_ein_matches.csv: ein, cik, name, state_inc, hq_state,
sic, former_names, tickers. A hit means the recipient entity itself is an
SEC registrant (a public company or a filing subsidiary). The archive is
scanned once with a byte-level regex before any JSON parsing, so it runs in
minutes rather than an hour."""
import csv, json, re, sys, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ZIP = ROOT / "data" / "raw" / "edgar" / "submissions.zip"
RECIP = ROOT / "data" / "recipients.csv"
OUT = ROOT / "data" / "edgar_ein_matches.csv"
EIN_RE = re.compile(rb'"ein":"(\d{9})"')


def main():
    eins = {r["ein"] for r in csv.DictReader(RECIP.open()) if r["ein"]}
    print(f"{len(eins)} recipient EINs; scanning {ZIP.name}")
    hits = []
    with zipfile.ZipFile(ZIP) as z:
        names = [n for n in z.namelist() if n.endswith(".json") and "-submissions-" not in n]
        for i, n in enumerate(names):
            if i % 100000 == 0:
                print(f"  {i:,}/{len(names):,} scanned, {len(hits)} hits", flush=True)
            head = z.open(n).read(4000)
            m = EIN_RE.search(head)
            if not m or m.group(1).decode() not in eins:
                continue
            d = json.loads(z.open(n).read())
            biz = (d.get("addresses") or {}).get("business") or {}
            hits.append({
                "ein": d.get("ein", ""), "cik": str(d.get("cik", "")).zfill(10), "name": d.get("name", ""),
                "state_inc": d.get("stateOfIncorporation", ""), "hq_state": biz.get("stateOrCountry", ""),
                "hq_city": biz.get("city", ""), "sic": d.get("sic", ""), "sic_desc": d.get("sicDescription", ""),
                "tickers": " ".join(d.get("tickers") or []),
                "former_names": " | ".join(f.get("name", "") for f in (d.get("formerNames") or [])),
                "last_filing": (d.get("filings", {}).get("recent", {}).get("filingDate") or [""])[0],
            })
    hits.sort(key=lambda h: h["name"])
    with OUT.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(hits[0]) if hits else ["ein"]); w.writeheader(); w.writerows(hits)
    print(f"wrote {OUT.name}: {len(hits)} EIN matches")
    for h in hits:
        print(f"  {h['ein']} {h['name'][:40]:40s} inc={h['state_inc']} hq={h['hq_state']} tickers={h['tickers']} last={h['last_filing']}")


if __name__ == "__main__":
    main()
