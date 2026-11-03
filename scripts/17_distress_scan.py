#!/usr/bin/env python3
"""Scan every grant recipient for public signs of failure after its first
grant: bankruptcy, receivership, liquidation, closure, layoffs, foreclosure.

Google News RSS is the index (no key, no blocking at a polite rate). A hit is
a candidate headline, not a finding: the same company name turns up in other
states, and "closing" can mean a single store. Candidates go to
data/distress_candidates.csv and are confirmed one by one, by the court
docket where there is one.

Why not court records directly: CourtListener's API now needs an account and
its public pages throttle after a couple of dozen queries, so the full list
cannot be swept that way. Court dockets are used to confirm the candidates
this scan turns up, not to find them.

Usage: 17_distress_scan.py [--start N] [--limit N] [--sleep 1.5] [--min-cash N]
"""
import csv, html, email.utils, re, subprocess, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from names import name_tokens, normalize_name

PARENTS = ROOT / "data" / "parents.csv"
OUT = ROOT / "data" / "distress_candidates.csv"
UA = "Data 4 The People research"
TERMS = ("bankruptcy OR \"chapter 11\" OR \"chapter 7\" OR receivership OR liquidation "
         "OR \"closes plant\" OR \"shutting down\" OR layoffs OR foreclosure")
HARD = re.compile(r"\b(bankrupt\w*|chapter 11|chapter 7|receivership|receiver|liquidat\w+|"
                  r"insolven\w+|wound down|winding down|assignment for the benefit)\b", re.I)
SOFT = re.compile(r"\b(clos\w+|shut\w+|layoff\w*|laying off|cut \d+ jobs|foreclos\w+|auction)\b", re.I)


def rss(query):
    url = ("https://news.google.com/rss/search?q=" + query.replace(" ", "+").replace('"', "%22")
           + "&hl=en-US&gl=US&ceid=US:en")
    for attempt in range(3):
        p = subprocess.run(["curl", "-sL", "--max-time", "40", "-A", UA, url], capture_output=True, text=True)
        if p.returncode == 0 and "<item>" in p.stdout:
            return p.stdout
        if p.returncode == 0:
            return ""      # a valid empty feed
        time.sleep(4 * (attempt + 1))
    return ""


def items(feed):
    out = []
    for it in re.findall(r"<item>(.*?)</item>", feed, re.S):
        t = re.search(r"<title>(.*?)</title>", it, re.S)
        d = re.search(r"<pubDate>(.*?)</pubDate>", it)
        s = re.search(r"<source[^>]*>(.*?)</source>", it, re.S)
        if not t:
            continue
        try:
            dt = email.utils.parsedate_to_datetime(d.group(1)) if d else None
        except Exception:
            dt = None
        out.append({"title": html.unescape(re.sub(r"<[^>]+>", "", t.group(1))).strip(),
                    "date": dt.strftime("%Y-%m-%d") if dt else "",
                    "source": html.unescape(re.sub(r"<[^>]+>", "", s.group(1))).strip() if s else ""})
    return out


def main(args):
    def opt(flag, cast, default):
        return cast(args[args.index(flag) + 1]) if flag in args else default
    start, limit = opt("--start", int, 0), opt("--limit", int, 10**9)
    sleep, min_cash = opt("--sleep", float, 1.5), opt("--min-cash", int, 1)

    rows = [r for r in csv.DictReader(PARENTS.open()) if int(r["total_cash"]) >= min_cash]
    seen, queue = set(), []
    for r in rows:
        key = normalize_name(r["name"])
        if not key or key in seen:
            continue
        seen.add(key)
        queue.append(r)
    queue.sort(key=lambda r: -int(r["total_cash"]))
    queue = queue[start:start + limit]

    done = {r["recipient_id"]: r for r in csv.DictReader(OUT.open())} if OUT.exists() else {}
    out_rows = list(done.values())

    def save():
        if not out_rows:
            return
        with OUT.open("w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(out_rows[0])); w.writeheader(); w.writerows(out_rows)

    for i, r in enumerate(queue, 1):
        if r["recipient_id"] in done:
            continue
        first_year = int(min(r["years"].split()))
        toks = name_tokens(r["name"])
        # headline test: the first two words of the name without its legal suffix
        # ("petmin usa", "nostrum laboratories"). For a one-word name the suffix
        # or the city must appear too, so "Intel Corporation" does not match a
        # story about "Intel Markets".
        words = re.sub(r"[^a-z0-9 ]", " ", r["name"].lower()).split()
        SUFFIX = {"inc", "incorporated", "llc", "lc", "ltd", "limited", "lp", "llp", "plc",
                  "co", "corp", "corporation", "company", "holdings", "group"}
        core = [w for w in words if w not in SUFFIX]
        suffixes = [w for w in words if w in SUFFIX]
        # query the real name minus its legal suffix: normalize_name() drops
        # meaningful words like "International" that the company actually uses
        phrase = " ".join(core[:4]) or r["name"]
        feed = rss(f'"{phrase}" ({TERMS})')
        hard, soft, weak = [], [], []
        for it in items(feed):
            if it["date"] and int(it["date"][:4]) < first_year:
                continue
            title_norm = " ".join(re.sub(r"[^a-z0-9 ]", " ", it["title"].lower()).split())
            if len(core) >= 2:
                named = " ".join(core[:2]) in title_norm
            elif core:
                extra = suffixes + ([r["city"].lower()] if r.get("city") else [])
                named = core[0] in title_norm and any(x and x in title_norm for x in extra)
            else:
                named = False
            if not named:
                # Google matched the article body, not the headline: keep as weak,
                # since real cases turn up this way (a story about the owner, say)
                if HARD.search(it["title"]):
                    weak.append(it)
                continue
            if HARD.search(it["title"]):
                hard.append(it)
            elif SOFT.search(it["title"]):
                soft.append(it)
        out_rows.append({
            "recipient_id": r["recipient_id"], "name": r["name"], "parent": r["parent"],
            "class": r["recipient_class"] or r["recipient_class_auto"],
            "total_cash": r["total_cash"], "grant_years": r["years"], "first_year": first_year,
            "n_hard": len(hard), "n_soft": len(soft), "n_weak": len(weak),
            "hard_headlines": " | ".join(f"{h['date']} {h['title'][:95]} [{h['source'][:24]}]" for h in hard[:3]),
            "soft_headlines": " | ".join(f"{h['date']} {h['title'][:95]} [{h['source'][:24]}]" for h in soft[:2]),
            "weak_headlines": " | ".join(f"{h['date']} {h['title'][:95]} [{h['source'][:24]}]" for h in weak[:2]),
        })
        if hard:
            print(f"  FAILURE? {r['name'][:38]:38s} ${int(r['total_cash']):>10,} :: {out_rows[-1]['hard_headlines'][:150]}", flush=True)
        if i % 50 == 0:
            save()
            print(f"  ... {i}/{len(queue)} scanned, {sum(1 for x in out_rows if int(x['n_hard']))} with failure headlines", flush=True)
        time.sleep(sleep)
    save()
    print(f"wrote {OUT.name}: {len(out_rows)} recipients scanned, "
          f"{sum(1 for x in out_rows if int(x['n_hard']))} with failure headlines, "
          f"{sum(1 for x in out_rows if int(x['n_soft']) and not int(x['n_hard']))} with softer distress headlines")


if __name__ == "__main__":
    main(sys.argv[1:])
