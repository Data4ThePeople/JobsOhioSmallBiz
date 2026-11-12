#!/usr/bin/env python3
"""Give every company on the page one link that actually works.

The page used to link a company name to the first entry in its research
`sources`, which was wrong twice over. Those fields were written to record *how*
a call was made, not *where* a reader can go, so most of them are prose ("Form
5500 2023: 86 participants, largest plan, sponsor ..."), and a sample of 60
found only 16 that resolved. Some of the rest were Google News search queries,
which are not citations, and the sec.gov ones failed only because they were
fetched without the contact User-Agent the SEC requires.

The order here is the reader's order, best evidence first:

  1. the company's own 10-K, when it has an SEC CIK on file
  2. a press release or news article already cited in the research
  3. the company's own website

Every candidate is fetched before it is kept. **A link that does not resolve is
not written**, because a dead link is worse than plain text: the page simply
shows the name unlinked and the reader is not sent anywhere.

Writes data/parent_links.csv. 09_analyze.py reads it if it is there.

Usage: 27_resolve_links.py [--limit N] [--only-missing] [--workers 8]
"""
import concurrent.futures as cf
import csv, json, re, subprocess, sys, time
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent
PARENTS = ROOT / "data" / "parents.csv"
OUT = ROOT / "data" / "parent_links.csv"

SEC_UA = "Data 4 The People research connect@data4thepeople.com"
UA = "Data 4 The People research"
URL = re.compile(r"https?://[^\s,;'\"|)\]<>]+")
# a search query is not a citation, and these hosts rate-limit or block anyway
JUNK_HOST = ("news.google.com", "google.com", "bing.com", "duckduckgo.com",
             "linkedin.com", "facebook.com", "twitter.com", "x.com")
JUNK_PATH = ("/search?", "/search/", "?q=", "&q=")
# A reference page is not the company's own site, and a shared report is not a
# record of this company. An audit found Visa's "company website" was
# cleveland.com, 89 were Wikipedia, and one JobsOhio PDF was the link for 66
# different companies. Labelling those honestly is the fix; dropping them is not,
# because a Wikipedia article is still useful to a reader who is told what it is.
REFERENCE_HOST = ("wikipedia.org", "propublica.org", "bizapedia.com", "crunchbase.com",
                  "bloomberg.com/profile", "dnb.com", "zoominfo.com", "opencorporates.com")
# targets that are about JobsOhio or the data, not about one company
SHARED_TARGET = ("/newsroom/transparency", "/newsroom/reports-publications",
                 "/files/reports/", "/files/tax-returns/", "askebsa.dol.gov", "efast.dol.gov",
                 "dam.assets.ohio.gov/raw/upload")
# an EDGAR browse or Atom feed is a search result, not a filing
SEC_SEARCH = ("cgi-bin/browse-edgar", "action=getcompany", "&output=atom", "/cgi-bin/srqsb")


def ua_for(url):
    return SEC_UA if "sec.gov" in urlsplit(url).netloc else UA


def fetch_status(url, timeout=14):
    """HTTP status after redirects, or '000'. HEAD first, GET if HEAD is refused."""
    for method in ("-I", ""):
        cmd = ["curl", "-sL", "-o", "/dev/null", "-w", "%{http_code}",
               "--max-time", str(timeout), "-A", ua_for(url)]
        if method:
            cmd.append(method)
        cmd.append(url)
        p = subprocess.run(cmd, capture_output=True, text=True)
        code = (p.stdout or "").strip()
        if code == "200":
            return code
        if code not in ("405", "403", "000", ""):
            return code
    return code or "000"


def tenk_for(cik, want_name=""):
    """The most recent 10-K for this CIK, but only if the registrant really is
    this company.

    EINs on Schedule I are self-reported and sometimes belong to another filer,
    so the CIK on file can point somewhere else entirely. An audit found
    Charoen Pokphand Foods linked to LUIGINO'S INC and Berkshire Hathaway to
    NOVEON INC. A link to the wrong company's annual report is worse than no
    link, so the registrant name has to share a distinctive word with the
    company before the filing is accepted.
    """
    cik = re.sub(r"\D", "", cik or "")
    if not cik:
        return None
    p = subprocess.run(["curl", "-s", "--max-time", "20", "-A", SEC_UA,
                        f"https://data.sec.gov/submissions/CIK{int(cik):010d}.json"],
                       capture_output=True, text=True)
    try:
        sub = json.loads(p.stdout)
        recent = sub["filings"]["recent"]
    except Exception:
        return None
    if want_name:
        STOP = {"inc", "inc.", "corp", "corp.", "corporation", "company", "co", "co.", "llc",
                "ltd", "ltd.", "limited", "plc", "group", "holdings", "the", "and", "&",
                "sa", "ag", "nv", "se", "international", "lp", "l.p.", "p.c."}
        def words(x):
            return {w.strip(".,").lower() for w in re.split(r"[\s/,()]+", x)
                    if w.strip(".,").lower() not in STOP and len(w.strip(".,")) > 2}
        reg = words(sub.get("name", "")) | {w for n in sub.get("formerNames", [])
                                            for w in words(n.get("name", ""))}
        if reg and not (reg & words(want_name)):
            return None
    for form, acc, doc, date in zip(recent.get("form", []), recent.get("accessionNumber", []),
                                    recent.get("primaryDocument", []), recent.get("filingDate", [])):
        if form == "10-K" and doc:
            a = acc.replace("-", "")
            return (f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{a}/{doc}", date)
    return None


def candidates(row):
    """(url, kind) in the order a reader should get them."""
    out = []
    blob = f"{row.get('hq_source','')} {row.get('emp_source','')} {row.get('notes','')}"
    for u in URL.findall(blob):
        u = u.rstrip(".,;)")
        host = urlsplit(u).netloc.lower()
        if any(j in host for j in JUNK_HOST) or any(j in u for j in JUNK_PATH):
            continue
        low = u.lower()
        if any(t in low for t in SHARED_TARGET):
            # a JobsOhio report or a DOL bulk file: true, but not about this
            # company in particular, so say so rather than calling it news
            kind = "JobsOhio report or bulk data"
        elif "sec.gov" in host and any(t in low for t in SEC_SEARCH):
            kind = "SEC search result"
        elif "sec.gov" in host and ("10-k" in low or "10k" in low):
            kind = "10-K"
        elif "sec.gov" in host:
            kind = "SEC filing"
        elif any(t in host or t in low for t in REFERENCE_HOST):
            kind = "reference page"
        elif any(k in low for k in ("press", "news", "newsroom", "/release", "prnewswire",
                                    "businesswire", "globenewswire")):
            kind = "press release"
        elif host.count(".") <= 2 and len(urlsplit(u).path.strip("/")) < 40:
            kind = "company website"
        else:
            kind = "news article"
        out.append((u, kind))
    # a record of THIS company beats a generic one, whatever its type
    rank = {"10-K": 0, "SEC filing": 1, "press release": 2, "news article": 3,
            "company website": 4, "reference page": 5, "SEC search result": 6,
            "JobsOhio report or bulk data": 7}
    out.sort(key=lambda x: rank.get(x[1], 9))
    # keep the order stable but drop duplicates
    seen, uniq = set(), []
    for u, k in out:
        if u not in seen:
            seen.add(u); uniq.append((u, k))
    return uniq


def resolve(row):
    name = row["parent"].strip() or row["name"].strip()
    # 1. the 10-K, which is the best thing a reader can be handed
    tk = tenk_for(row.get("edgar_cik", ""), name)
    if tk:
        url, date = tk
        if fetch_status(url) == "200":
            return {"recipient_id": row["recipient_id"], "parent": name, "url": url,
                    "kind": "10-K", "as_of": date, "status": "200",
                    "note": "most recent 10-K from the SEC submissions API"}
    # 2. then whatever real URL the research already cited
    for url, kind in candidates(row)[:6]:
        code = fetch_status(url)
        if code == "200":
            return {"recipient_id": row["recipient_id"], "parent": name, "url": url, "kind": kind,
                    "as_of": "", "status": code,
                    "note": "from the research sources, fetched and confirmed"}
    return {"recipient_id": row["recipient_id"], "parent": name, "url": "", "kind": "",
            "as_of": "", "status": "",
            "note": "no link that resolves; the page shows the name unlinked"}


def main(argv):
    def opt(flag, cast, default):
        return cast(argv[argv.index(flag) + 1]) if flag in argv else default
    limit, workers = opt("--limit", int, 10**9), opt("--workers", int, 8)

    rows = list(csv.DictReader(PARENTS.open()))
    by_parent = {}
    for r in rows:
        by_parent.setdefault(r["parent"].strip() or r["name"].strip(), r)
    todo = list(by_parent.values())

    done = {}
    if OUT.exists():
        done = {r.get("recipient_id") or r["parent"]: r for r in csv.DictReader(OUT.open())}
        if "--only-missing" in argv:
            todo = [r for r in todo
                    if not done.get(r["recipient_id"], {}).get("url")]
    todo = todo[:limit]
    print(f"{len(by_parent)} parents, resolving {len(todo)}")

    out, t0 = dict(done), time.time()
    with cf.ThreadPoolExecutor(workers) as ex:
        for i, res in enumerate(ex.map(resolve, todo), 1):
            out[res["recipient_id"]] = res
            if i % 100 == 0:
                hit = sum(1 for v in out.values() if v.get("url"))
                print(f"  {i}/{len(todo)}  {hit} with a working link  "
                      f"({time.time()-t0:.0f}s)", flush=True)
                with OUT.open("w", newline="") as fh:
                    w = csv.DictWriter(fh, fieldnames=["recipient_id", "parent", "url", "kind", "as_of", "status", "note"])
                    w.writeheader(); w.writerows(out.values())

    with OUT.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["recipient_id", "parent", "url", "kind", "as_of", "status", "note"])
        w.writeheader(); w.writerows(out.values())
    from collections import Counter
    kinds = Counter(v["kind"] or "none" for v in out.values())
    hit = sum(1 for v in out.values() if v.get("url"))
    print(f"\nwrote {OUT.relative_to(ROOT)}: {hit} of {len(out)} parents have a link that resolves")
    for k, n in kinds.most_common():
        print(f"  {k:18s} {n:5d}")


if __name__ == "__main__":
    main(sys.argv[1:])
