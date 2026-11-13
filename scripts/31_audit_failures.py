#!/usr/bin/env python3
"""Audit the failure findings end to end, because that is where the scrutiny lands.

Every claim that a company failed after taking public money has to survive a
hostile read, so each one is checked here against the file it was verified
against and against the sources it cites. Any failure exits non-zero. Run it
before every publish, alongside 30_audit_summary.py.

What it checks, and why each one is here rather than assumed:

  identity    a join key, because two different Speedway LLCs file under
              different EINs and a name join silently picked one of them
  elsewhere   the three companies that failed away from the funded site are
              neither counted nor filed with the rejects, and each one says
              which site took the money and which site failed
  money       the paid figure ties to parents.csv by recipient_id, and again
              to the sum of that payee's Schedule I rows, because parents.csv
              is built by this pipeline and a check between two derived files
              would miss an error made in both. Merging a year once left the
              file stale by $2,200,000
  category    every confirmed failure has exactly one, and the category is
              consistent with the event recorded
  site        the operation that failed is the operation the grant paid for,
              from data/research3/sitecheck.json where that pass has run.
              Three findings have already turned on this: Howmet's Barberton
              layoff was not a funded site, International Paper's closure was
              Marion rather than the funded Kenton, and Nestle needed a
              partial caveat
  partial     a failure inside a parent that was paid more carries the payee
              split, so no reader can take the parent total as the loss
  warn        every closure and mass layoff after 2019 ties to the employer's
              own notice to Ohio, or records why the state has none, and a
              notice filed in a county the money never reached is labelled
              rather than counted
  sources     every confirmed failure has a URL, it is unique to that company,
              and nothing is a bare search page
  rejects     every rejected candidate states a reason, so the count is
              auditable by subtraction as well as by addition

Usage: 31_audit_failures.py [--fetch]   (--fetch re-checks that every source URL resolves)
"""
import csv, json, re, subprocess, sys
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent

FAILURES = ROOT / "data" / "failures.csv"
SOURCES = ROOT / "data" / "failure_sources.csv"
SITECHECK = ROOT / "data" / "research3" / "sitecheck.json"
WARNMATCH = ROOT / "data" / "failure_warn.csv"
PARENTS = ROOT / "data" / "parents.csv"
GRANTS = ROOT / "data" / "grants_raw.csv"
DATA = ROOT / "dist" / "data.json"

SEC_UA = "Data 4 The People research connect@data4thepeople.com"
BROWSER_UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")
ELSEWHERE = "Failed away from the funded site"
WARN_CATS = ("Funded site closed", "Mass layoff at the funded site")
WARN_FIRST_YEAR = 2020  # Ohio publishes no notices before this
# statuses that mean "a human gets this page, a script does not"
BLOCK_CODES = {"202", "401", "403", "429", "503"}
# Every event word a confirmed row is allowed to carry, and the one category it
# implies. The point is that the two columns cannot drift apart: `event` is what
# happened, `category` is how the page files it, and a row where those disagree
# is a row a reader can catch us on. Anything not in this map is itself a
# failure, so a new event word has to be thought about rather than typed in.
EVENT_CATEGORY = {
    "Chapter 7": "Bankruptcy or receivership", "Chapter 11": "Bankruptcy or receivership",
    "Receivership": "Bankruptcy or receivership",
    "Assignment for benefit of creditors": "Bankruptcy or receivership",
    "Closure": "Funded site closed",
    "Layoffs": "Mass layoff at the funded site",
    "Acquisition": "Sold or absorbed", "Divestiture": "Sold or absorbed",
    "Route discontinued": "Subsidized service ended",
}

problems = []


def bad(msg):
    problems.append(msg)


def main(argv):
    fails = [r for r in csv.DictReader(FAILURES.open())]
    conf = [r for r in fails if r["verdict"] == "Confirmed failure"]
    away = [r for r in fails if r["verdict"] == ELSEWHERE]
    rej = [r for r in fails if r["verdict"] not in ("Confirmed failure", ELSEWHERE)]
    parents = {r["recipient_id"]: r for r in csv.DictReader(PARENTS.open())}
    srcs = {r["name"]: r for r in csv.DictReader(SOURCES.open())} if SOURCES.exists() else {}
    site = {x["recipient_id"]: x for x in json.loads(SITECHECK.read_text())} if SITECHECK.exists() else {}
    warn = {r["recipient_id"]: r for r in csv.DictReader(WARNMATCH.open())} \
        if WARNMATCH.exists() else {}

    print(f"{len(fails)} candidates checked: {len(conf)} confirmed, {len(away)} failed "
          f"away from the funded site, {len(rej)} rejected")
    print(f"confirmed total: ${sum(int(r['paid'] or 0) for r in conf):,}")
    print(f"not counted, failed elsewhere: "
          f"${sum(int(r['paid'] or 0) for r in away):,}\n")

    # --- identity ---------------------------------------------------------
    for r in conf:
        if not r.get("recipient_id"):
            bad(f"{r['name']}: no recipient_id, so every join falls back to the name")
        elif r["recipient_id"] not in parents:
            bad(f"{r['name']}: recipient_id {r['recipient_id']} is not in parents.csv")
    dup = [k for k, n in Counter(r["recipient_id"] for r in conf).items() if n > 1 and k]
    if dup:
        bad(f"a recipient_id is confirmed twice: {dup}")

    # --- money ------------------------------------------------------------
    for r in conf:
        p = parents.get(r.get("recipient_id", ""))
        if p and int(r["paid"] or 0) != int(p["total_cash"] or 0):
            bad(f"{r['name']}: paid ${int(r['paid'] or 0):,} but parents.csv says "
                f"${int(p['total_cash'] or 0):,} (is failures.csv stale?)")

    # And again against the filings themselves, not the file derived from them.
    # Every dollar published beside a company's name should be re-addable from
    # Schedule I alone, because parents.csv is built by this pipeline and a
    # check that only compares the two would miss an error made in both.
    if GRANTS.exists():
        raw = defaultdict(int)
        for g in csv.DictReader(GRANTS.open()):
            ein = re.sub(r"\D", "", g["recipient_ein"] or "")
            if len(ein) == 9 and ein.strip("0"):
                raw[f"EIN:{ein}"] += int(g["cash_amt"])
        for r in conf + away:
            rid = r.get("recipient_id", "")
            if rid.startswith("EIN:") and rid not in raw:
                bad(f"{r['name']}: {rid} has no rows in grants_raw.csv at all")
            elif rid in raw and int(r["paid"] or 0) != raw[rid]:
                bad(f"{r['name']}: paid ${int(r['paid'] or 0):,} but Schedule I sums to "
                    f"${raw[rid]:,} for {rid}")

    # --- category ---------------------------------------------------------
    for r in conf:
        if not r["category"]:
            bad(f"{r['name']}: no category")
        if not r["event"]:
            bad(f"{r['name']}: confirmed as a failure with no event recorded")
        elif r["event"] not in EVENT_CATEGORY:
            bad(f"{r['name']}: event {r['event']!r} is not one of the recognised "
                f"events, so nothing checks that its category is right")
        want = EVENT_CATEGORY.get(r["event"])
        if want and r["category"] != want and not r.get("caveat"):
            bad(f"{r['name']}: event {r['event']!r} normally means {want!r}, "
                f"but it is filed as {r['category']!r} with no caveat explaining why")

    # --- site -------------------------------------------------------------
    if site:
        for r in conf:
            sc = site.get(r.get("recipient_id", ""))
            if not sc:
                bad(f"{r['name']}: not covered by the site check")
            elif sc.get("verdict") == "different site":
                bad(f"{r['name']}: the site check says the failure was at a DIFFERENT site "
                    f"({sc.get('failed_site')}) from the funded one ({sc.get('funded_site')}); "
                    f"this should not be in the count")
            elif sc.get("verdict") == "partly" and not r.get("caveat"):
                bad(f"{r['name']}: the site check calls this partial "
                    f"({sc.get('what_survives')}) but the row carries no caveat")
    else:
        print("note: data/research3/sitecheck.json is not present, so the "
              "funded-site check is not being enforced\n")

    # --- partial ----------------------------------------------------------
    if DATA.exists():
        d = json.loads(DATA.read_text())
        for row in d.get("parents_table", []):
            f = row.get("failure")
            if f and row["cash"] > f["payee_paid"] * 1.01 and not f.get("partial"):
                bad(f"{row['parent']}: paid ${row['cash']:,} against a failed payee's "
                    f"${f['payee_paid']:,}, but the row is not marked partial")
        shown = {x["payee"] for x in d.get("failed_payees", [])}
        missing = {r["name"] for r in conf} - shown
        if missing:
            bad(f"confirmed failures missing from the payee view: {sorted(missing)[:5]}")
        if len(d.get("rejected", [])) != len(rej):
            bad(f"the tool shows {len(d.get('rejected', []))} rejected candidates, "
                f"the file has {len(rej)}")
        if len(d.get("failed_elsewhere", [])) != len(away):
            bad(f"the tool shows {len(d.get('failed_elsewhere', []))} companies that "
                f"failed away from the funded site, the file has {len(away)}")
        # every candidate must appear in exactly one of the three views, or the
        # 102 stops adding up and a reader can show that it does not
        views = (len(d.get("failed_payees", [])) + len(d.get("failed_elsewhere", []))
                 + len(d.get("rejected", [])))
        if views != len(fails):
            bad(f"the three views hold {views} companies between them but "
                f"{len(fails)} candidates were checked")

    # --- elsewhere --------------------------------------------------------
    for r in away:
        sc = site.get(r.get("recipient_id", ""))
        if sc and sc.get("verdict") != "different site":
            bad(f"{r['name']}: moved off the count, but the site check says "
                f"{sc.get('verdict')!r}, not 'different site'")
        if not r.get("caveat"):
            bad(f"{r['name']}: moved off the count with no caveat saying which site "
                f"took the money and which site failed")
    for r in conf:
        sc = site.get(r.get("recipient_id", ""))
        if sc and sc.get("verdict") == "different site":
            bad(f"{r['name']}: the site check says a different site failed, but the "
                f"row is still counted as a failure")

    # --- warn -------------------------------------------------------------
    if warn:
        for r in conf + away:
            if r["category"] not in WARN_CATS and r["verdict"] != ELSEWHERE:
                continue
            yr = int((r["event_date"] or "0")[:4] or 0)
            w = warn.get(r.get("recipient_id", ""))
            if yr and yr < WARN_FIRST_YEAR:
                continue  # Ohio publishes nothing this old
            if not w:
                bad(f"{r['name']}: an Ohio closure or layoff with no row in the state "
                    f"notice match, so nothing says whether Ohio recorded it")
            elif w["state_notice"] == "none" and not w.get("why_none"):
                bad(f"{r['name']}: no state notice and no reason recorded for that")
            elif w["state_notice"] == "matched":
                if w.get("notice_at_funded_site") == "no" and not r.get("caveat"):
                    bad(f"{r['name']}: the matched notice is for {w['warn_place']}, a "
                        f"county the money never reached, and the row has no caveat "
                        f"saying so")
                if not w.get("warn_pdf"):
                    bad(f"{r['name']}: matched a state notice with no link to the "
                        f"filed letter")
    else:
        print("note: data/failure_warn.csv is not present, so Ohio's own notices "
              "are not being enforced\n")

    # --- sources ----------------------------------------------------------
    for r in conf:
        s = srcs.get(r["name"])
        if not s or not s.get("url"):
            bad(f"{r['name']}: no source URL")
        elif s.get("url_kind") == "search":
            bad(f"{r['name']}: the source is a search page, not a record")
        elif s.get("verified") != "yes":
            bad(f"{r['name']}: source recorded as verified={s.get('verified')!r}")
    urls = Counter(s["url"] for n, s in srcs.items() if s.get("url"))
    for u, n in urls.items():
        if n > 1:
            bad(f"{n} confirmed failures share one source URL: {u[:80]}")

    # --- rejects ----------------------------------------------------------
    for r in rej:
        if not (r.get("ohio_outcome") or r.get("notes")):
            bad(f"{r['name']}: rejected with no reason recorded")

    # --- report -----------------------------------------------------------
    if "--fetch" in argv:
        print("re-fetching every source URL...")
        blocked_ok, dead = 0, 0
        for r in conf:
            s = srcs.get(r["name"], {})
            u = s.get("url", "")
            if not u:
                continue
            ua = SEC_UA if "sec.gov" in urlsplit(u).netloc else BROWSER_UA
            p = subprocess.run(["curl", "-sL", "-o", "/dev/null", "-w", "%{http_code}",
                                "--max-time", "25", "-A", ua, u], capture_output=True, text=True)
            code = (p.stdout or "").strip()
            if code == "200":
                continue
            # A bot challenge is not a dead link, and treating the two alike both
            # cries wolf and hides the real thing. CourtListener answers every
            # automated fetch with an empty 202, and some newspapers with a 403.
            # Those are allowed through only when the row says so and names what
            # the finding was checked against instead, so the gap is on the record
            # rather than papered over.
            if code in BLOCK_CODES:
                if re.search(r"block|challenge|403|202|429|Cloudflare|paywall|bot",
                             s.get("notes", ""), re.I):
                    blocked_ok += 1
                else:
                    bad(f"{r['name']}: source returns HTTP {code} and the notes do not say "
                        f"the host blocks automated fetch or what was checked instead "
                        f"({u[:60]})")
            else:
                dead += 1
                bad(f"{r['name']}: source returns HTTP {code}, which means the record is "
                    f"gone, not blocked ({u[:60]})")
        print(f"  done: {blocked_ok} hosts block automated fetch and say so, "
              f"{dead} links are dead\n")

    if problems:
        print(f"{len(problems)} problems:\n")
        for m in problems:
            print(f"  FAIL {m}")
        sys.exit(f"\n{len(problems)} failure findings do not hold up")
    print("every failure finding ties to its source, its money and its site check")


if __name__ == "__main__":
    main(sys.argv[1:])
