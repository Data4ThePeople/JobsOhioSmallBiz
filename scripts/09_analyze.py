#!/usr/bin/env python3
"""Compute every published number from data/grants_raw.csv and
data/parents.csv, and write dist/data.json for the page and the static
charts, plus TIEOUT.md.

Units of analysis:
  row       one Schedule I line (recipient, fiscal year, cash)
  recipient one distinct payee entity (EIN or normalized name)
  parent    the ultimate parent the recipient resolves to; the headline
            "share of recipients" counts parents, not rows

Size: emp_bucket of the parent at the time of the grant, one of
<100, 100-499, 500-4999, 5000+. "Small" at the default cutoff means under
500. Home: parent_hq_state == OH. Class: business, site_development,
government, university, hospital, nonprofit. The headline denominator is
class == business; the page can toggle to all classes.

Uncertain rows (confidence C or D, or no bucket) are shown as their own
group and the worst-case bounds reassign them against the thesis.

Two later findings ride along on the parent record so the page can show them
beside the size and home-state calls: `conditions`, the weakest conditions
published for any program that paid this parent (19_grant_conditions.py), and
`failure`, the verified post-grant outcome where there is one
(21_failures.py). Both are optional inputs: the analysis runs without them."""
import csv, json, sys
from collections import defaultdict, Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from names import normalize_name

ROOT = Path(__file__).resolve().parent.parent
GRANTS = ROOT / "data" / "grants_raw.csv"
PARENTS = ROOT / "data" / "parents.csv"
CONDITIONS = ROOT / "data" / "grant_conditions.csv"
FAILURES = ROOT / "data" / "failures.csv"
LAWSUITS = ROOT / "data" / "jobsohio_lawsuits.csv"
FAILURE_SOURCES = ROOT / "data" / "failure_sources.csv"
OUT = ROOT / "dist" / "data.json"
TIEOUT = ROOT / "TIEOUT.md"

# weakest published terms win when a parent was paid by several programs,
# because the payment cannot be tied to one of them
# strongest evidence of recourse first; a parent paid under several programs
# takes the weakest, because the payment cannot be tied to one of them
RECOURSE_ORDER = {"agreement seen": 6, "standard form": 5, "published clawback": 4,
                  "loan": 3, "service not cash": 2, "none found": 1, "program unknown": 0}

BUCKETS = ["<100", "100-499", "500-4999", "5000+"]
CUTOFFS = {"100": ["<100"], "500": ["<100", "100-499"], "5000": ["<100", "100-499", "500-4999"]}


def load():
    grants = list(csv.DictReader(GRANTS.open()))
    parents = {r["recipient_id"]: r for r in csv.DictReader(PARENTS.open())}
    # recipient_id for each grant row, same rule as 04_normalize
    import re
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from names import normalize_name
    for g in grants:
        ein = re.sub(r"\D", "", g["recipient_ein"])
        g["recipient_id"] = f"EIN:{ein}" if len(ein) == 9 and ein.strip("0") else f"NAME:{normalize_name(g['recipient_name'])}"
        g["cash"] = int(g["cash_amt"])
        g["fy"] = int(g["fiscal_year"])
        if g["recipient_id"] not in parents:
            sys.exit(f"grant row without a parents.csv entry: {g['recipient_id']} (run 04 and 05)")

    # The review columns are the record of who decided what, but the analysis
    # reads emp_bucket and parent_hq_state. 18_apply_review.py merges one into
    # the other. If that merge is ever skipped, a changed review answer would be
    # silently ignored and the headline would not move, so check it here.
    SMALL, LARGE = ("<100", "100-499"), ("500-4999", "5000+")
    bad = []
    for p in parents.values():
        rs, rh, bucket = p.get("review_size", ""), p.get("review_hq", ""), p["emp_bucket"]
        if rs == "Large" and bucket in SMALL or rs == "Small" and bucket in LARGE:
            bad.append(f"{p['name']}: review says {rs}, emp_bucket is {bucket}")
        if rh and bucket:  # home state only; a blank review means not reviewed
            want = "OH" if rh.strip().lower() in ("yes", "y", "oh") else ""
            if want and p["parent_hq_state"] and p["parent_hq_state"] != want:
                bad.append(f"{p['name']}: review says Ohio, parent_hq_state is {p['parent_hq_state']}")
    if bad:
        sys.exit("review answers not merged into the analysis columns; rerun "
                 "scripts/18_apply_review.py:\n  " + "\n  ".join(bad[:10]))
    return grants, parents


# a research pass that could not find an owner wrote the word rather than
# leaving the cell empty, and keying on it merged 12 unrelated project LLCs
# into two companies called "unknown" and "unresolved". A recipient whose
# owner was not found is its own parent, which is also what the page should
# show the reader.
NO_PARENT = {"", "unknown", "unresolved", "none", "n/a", "not found"}


def parent_key(p):
    name = p["parent"].strip()
    return name if name.lower() not in NO_PARENT else p["name"].strip()


def load_side_findings(parents):
    """(recourse, failure, suits) by parent. Every input file is optional."""
    import re
    def key(parent, fallback):
        parent = parent.strip()
        return parent if parent.lower() not in NO_PARENT else fallback.strip()

    cond = {}
    if CONDITIONS.exists():
        for r in csv.DictReader(CONDITIONS.open()):
            k = key(r["parent"], r["recipient"])
            call = r["recourse"]
            # a parent paid under several programs takes the weakest grade, since
            # the payment cannot be tied to one of them
            if k and (k not in cond or RECOURSE_ORDER.get(call, 0) < RECOURSE_ORDER.get(cond[k]["grade"], 0)):
                cond[k] = {"grade": call, "note": r["recourse_note"]}
    # a resolved URL for each confirmed failure, where one was found
    fail_url = {}
    if FAILURE_SOURCES.exists():
        for r in csv.DictReader(FAILURE_SOURCES.open()):
            if r.get("url"):
                fail_url[normalize_name(r["name"])] = {
                    "url": r["url"], "kind": r.get("url_kind", ""),
                    "title": r.get("title", ""), "publisher": r.get("publisher", ""),
                    "published": r.get("published", ""),
                    "paywalled": r.get("paywalled", ""), "verified": r.get("verified", "")}
    fail = {}
    if FAILURES.exists():
        # parents.csv is keyed by recipient, failures.csv by payee name, so the
        # payee is mapped up to its parent the same way the table is keyed
        by_name = {p["name"].strip(): parent_key(p) for p in parents.values()}
        for r in csv.DictReader(FAILURES.open()):
            if r["verdict"] != "Confirmed failure":
                continue
            k = key(r["parent"], by_name.get(r["name"].strip()) or r["name"].strip())
            fail[k] = {"category": r["category"], "event": r["event"],
                       "date": r["event_date"], "confidence": r["confidence"],
                       "cite": (r.get("source") or "")[:400],
                       "court": r.get("court", ""), "docket": r.get("docket", ""),
                       "src": fail_url.get(normalize_name(r["name"]))}
    # JobsOhio's own suits against the recipient, keyed the same way. A company
    # can be sued more than once, so they are collected into a list.
    sued = defaultdict(list)
    if LAWSUITS.exists():
        by_name = {p["name"].strip(): parent_key(p) for p in parents.values()}
        for r in csv.DictReader(LAWSUITS.open()):
            if r["kind"] != "suit" or not r["recipient"]:
                continue
            k = key(r["parent"], by_name.get(r["recipient"].strip()) or r["recipient"].strip())
            # the clerk serves a case only behind its disclaimer, so the link
            # goes to the case search with the case already filled in; a reader
            # accepts the disclaimer once and lands on the docket
            m = re.match(r"(\d{2})([A-Z]{2})(\d+)", r["case"].replace(" ", ""))
            url = ("https://fcdcfcjs.co.franklin.oh.us/CaseInformationOnline/caseSearch"
                   f"?caseYear={m.group(1)}&caseType={m.group(2)}&caseSeq={m.group(3)}&reallySubmit=true"
                   ) if m else ""
            sued[k].append({"case": r["case"], "filed": r["filed"], "url": url,
                            "sought": r["amount_sought"][:120], "outcome": r["outcome"][:120]})
    return cond, fail, dict(sued)


def resolve_class(a, b):
    """The parent's class when two of its payees disagree.

    `site_development` describes a payee: a single-project LLC built to hold a
    building. It says nothing about who owns it, so it loses to any other class.
    Tractor Supply Company pays through NAVARRE FACILITY LLC, and Tractor Supply
    is a retailer, not a developer. Among the rest the more specific class wins
    over `business`, which both keeps Nationwide Children's Hospital a hospital
    rather than a business and is the conservative call for a headline whose
    denominator is operating businesses.
    """
    if a == b:
        return a
    pair = {a, b}
    if "site_development" in pair:
        return (pair - {"site_development"}).pop()
    return next((c for c in (a, b) if c != "business"), a)


def build_parents(grants, parents):
    """One record per parent with class, bucket, home state, confidence, dollars."""
    agg = {}
    for g in grants:
        p = parents[g["recipient_id"]]
        k = parent_key(p)
        a = agg.setdefault(k, {"parent": k, "class": "", "bucket": "", "hq": "", "conf": "", "founded_oh": "",
                               "recipients": set(), "rows": 0, "cash": 0, "years": set(), "by_fy": Counter(),
                               "sources": set(), "programs": set(), "resolved": False,
                               "grades": set(), "auto_class": ""})
        a["recipients"].add(g["recipient_id"]); a["rows"] += 1; a["cash"] += g["cash"]
        a["years"].add(g["fy"]); a["by_fy"][g["fy"]] += g["cash"]
        cls = p["recipient_class"] or p["recipient_class_auto"]
        # every payee's grade is kept, not just the first one read: the worst
        # case sweeps on the weakest grade under the parent, so a parent with
        # one A-graded payee and one C-graded payee is swept
        if p["confidence"]:
            a["grades"].add(p["confidence"])
        if not a["auto_class"]:
            a["auto_class"] = p["recipient_class_auto"] or cls
        # a parent's attributes come from its researched recipients; the first
        # researched one wins, and any disagreement is reported
        if p["parent"]:
            a["resolved"] = True
            for field, col in (("class", cls), ("bucket", p["emp_bucket"]), ("hq", p["parent_hq_state"]),
                               ("conf", p["confidence"]), ("founded_oh", p["founded_in_ohio"])):
                if col and not a[field]:
                    a[field] = col
                elif col and a[field] and a[field] != col and field in ("bucket", "hq", "class"):
                    # Two recipients of one parent were researched to different
                    # answers. Rather than let whichever was read first win, the
                    # conflict is resolved against the finding: the smaller size
                    # band, which moves the dollars into "small"; Ohio, which
                    # moves them into "homegrown"; and for class, out of
                    # "business", which is the headline denominator. The
                    # conflict is still reported.
                    a.setdefault("conflicts", set()).add(f"{field}: {a[field]} vs {col} ({p['name']})")
                    if field == "bucket":
                        a[field] = min(a[field], col, key=lambda b: BUCKETS.index(b) if b in BUCKETS else 99)
                    elif field == "hq" and "OH" in (a[field], col):
                        a[field] = "OH"
                    elif field == "class":
                        a[field] = resolve_class(a[field], col)
            for s in (p["hq_source"], p["emp_source"]):
                if s:
                    a["sources"].add(s)
        elif not a["class"]:
            a["class"] = cls
        for prog in p["metrics_programs"].split(";"):
            if prog.strip():
                a["programs"].add(prog.strip())
    return agg


def merge_duplicate_names(agg):
    """Collapse parents that are the same company written two ways.

    "Berkshire Hathaway Inc." appears four times with different parentheticals,
    "McKesson Corporation" twice in different case. Counting them separately
    overstated the recipient count by about 22. Two records merge only when the
    normalized name, size bucket, home state and class all agree, so a genuine
    disagreement is never papered over; those stay separate and are reported.
    """
    groups = defaultdict(list)
    for k, a in agg.items():
        groups[(normalize_name(k), a["bucket"], a["hq"], a["class"])].append(k)
    merged, notes = {}, []
    by_norm = defaultdict(set)
    for k in agg:
        by_norm[normalize_name(k)].add(k)
    for (norm, *_), keys in groups.items():
        if len(keys) == 1:
            merged[keys[0]] = agg[keys[0]]
            continue
        # keep the longest spelling, which carries the ownership detail
        keep = max(keys, key=len)
        a = agg[keep]
        for k in keys:
            if k == keep:
                continue
            b = agg[k]
            a["recipients"] |= b["recipients"]; a["rows"] += b["rows"]; a["cash"] += b["cash"]
            a["years"] |= b["years"]; a["by_fy"].update(b["by_fy"])
            a["sources"] |= b["sources"]; a["programs"] |= b["programs"]
            a["grades"] |= b["grades"]
            a["conflicts"] = a.get("conflicts", set()) | b.get("conflicts", set())
        notes.append(f"{keep}  <=  {', '.join(sorted(k for k in keys if k != keep))}")
        merged[keep] = a
    # same company name, different attributes, so not merged: report them
    unmerged = []
    for norm, keys in by_norm.items():
        live = sorted(k for k in keys if k in merged)
        if len(live) < 2:
            continue
        unmerged.append(" | ".join(
            f"{k} [{merged[k]['bucket'] or '?'}, {merged[k]['hq'] or '?'}, "
            f"{merged[k]['class'] or '?'}, ${merged[k]['cash']:,}]" for k in live))
    return merged, notes, unmerged


def size_group(a, cutoff="500"):
    """small / large / unknown at a cutoff, using the bucket and confidence."""
    if a["bucket"] not in BUCKETS:
        return "unknown"
    return "small" if a["bucket"] in CUTOFFS[cutoff] else "large"


def home_group(a):
    if not a["hq"]:
        return "unknown"
    return "ohio" if a["hq"].upper() == "OH" else "other"


def shares(items, key, weight):
    c = Counter()
    for a in items:
        c[key(a)] += weight(a)
    tot = sum(c.values())
    return {k: {"n": v, "share": (v / tot if tot else 0)} for k, v in sorted(c.items())}, tot


def main():
    grants, parents = load()
    agg = build_parents(grants, parents)
    agg, merge_notes, unmerged = merge_duplicate_names(agg)
    # A parent whose payments net to zero or less (JobsOhio reversed or clawed
    # back everything) is not counted as a recipient. Its negative dollars
    # stay in the net totals.
    clawed = [a for a in agg.values() if a["cash"] <= 0]
    allp = [a for a in agg.values() if a["cash"] > 0]
    biz = [a for a in allp if a["class"] == "business"]
    from datetime import date
    out = {"meta": {"built": date.today().strftime("%B %-d, %Y"), "rows": len(grants), "recipients": len({g['recipient_id'] for g in grants}), "parents": len(allp),
                    "fy_min": min(g["fy"] for g in grants), "fy_max": max(g["fy"] for g in grants),
                    "cash_total": sum(g["cash"] for g in grants),
                    "reversal_rows": sum(1 for g in grants if g["cash"] < 0),
                    "reversal_dollars": sum(g["cash"] for g in grants if g["cash"] < 0),
                    "parents_net_zero_or_less": len(clawed),
                    "net_negative_dollars": sum(a["cash"] for a in clawed),
                    "resolved_parents": sum(1 for a in allp if a["resolved"]),
                    "resolved_cash": sum(a["cash"] for a in allp if a["resolved"]),
                    "cash_positive": sum(a["cash"] for a in allp)}}
    out["by_class"] = {k: {"parents": v["n"], "cash": 0} for k, v in shares(allp, lambda a: a["class"], lambda a: 1)[0].items()}
    for a in allp:
        out["by_class"][a["class"]]["cash"] += a["cash"]

    def block(items):
        b = {}
        for cut in CUTOFFS:
            b[cut] = {
                "parents": shares(items, lambda a: size_group(a, cut), lambda a: 1)[0],
                "cash": shares(items, lambda a: size_group(a, cut), lambda a: a["cash"])[0],
            }
        b["home"] = {"parents": shares(items, home_group, lambda a: 1)[0], "cash": shares(items, home_group, lambda a: a["cash"])[0]}
        b["two_by_two"] = {"parents": shares(items, lambda a: f"{size_group(a)}|{home_group(a)}", lambda a: 1)[0],
                           "cash": shares(items, lambda a: f"{size_group(a)}|{home_group(a)}", lambda a: a["cash"])[0]}
        # worst case for the thesis "most dollars go to large": unknown and low-confidence -> small
        # worst case for "most recipients are small": unknown and low-confidence -> large
        def wc_size(a, against):
            g = size_group(a)
            # sweep on the WEAKEST grade among the parent's payees, not the one
            # inherited from whichever payee was read first. An independent
            # tie-out found 6 parents escaping the sweep although they had a
            # C-graded payee, $16.4m of it, which made the published floor less
            # unfavorable than its own wording promised.
            weakest = max(a["grades"] or {a["conf"] or "D"})
            if g == "unknown" or weakest in ("C", "D"):
                return against
            return g
        b["worst_case"] = {
            "cash_large_min": shares(items, lambda a: wc_size(a, "small"), lambda a: a["cash"])[0].get("large", {"share": 0})["share"],
            "parents_small_min": shares(items, lambda a: wc_size(a, "large"), lambda a: 1)[0].get("small", {"share": 0})["share"],
        }
        by_fy = defaultdict(Counter)
        for a in items:
            for fy, c in a["by_fy"].items():
                by_fy[fy][size_group(a)] += c
        b["by_fy"] = {str(fy): dict(v) for fy, v in sorted(by_fy.items())}
        return b

    out["business"] = block(biz)
    out["all"] = block(allp)
    out["confidence"] = {"parents": shares(allp, lambda a: a["conf"] or "none", lambda a: 1)[0],
                         "cash": shares(allp, lambda a: a["conf"] or "none", lambda a: a["cash"])[0]}
    out["conflicts"] = sorted(c for a in allp for c in a.get("conflicts", set()))
    cond, fail, sued = load_side_findings(parents)
    out["parents_table"] = sorted([{
        "parent": a["parent"], "class": a["class"], "bucket": a["bucket"], "hq": a["hq"], "conf": a["conf"],
        "founded_oh": a["founded_oh"], "cash": a["cash"], "rows": a["rows"], "recipients": len(a["recipients"]),
        "years": sorted(a["years"]), "programs": sorted(a["programs"]), "sources": sorted(a["sources"])[:3],
        "by_fy": {str(k): v for k, v in sorted(a["by_fy"].items())},
        "payees": " | ".join(sorted({parents[r]["name"] for r in a["recipients"]}))[:400],
        "recourse": cond.get(a["parent"], None), "failure": fail.get(a["parent"], None),
        "sued": sued.get(a["parent"], None),
    } for a in allp], key=lambda d: -d["cash"])
    # dollars by published conditions, and the verified post-grant failures,
    # on the same parent universe the headline uses
    cond_agg = defaultdict(lambda: {"parents": 0, "cash": 0})
    for a in allp:
        c = cond_agg[(cond.get(a["parent"]) or {}).get("grade", "program unknown")]
        c["parents"] += 1; c["cash"] += a["cash"]
    out["recourse"] = dict(cond_agg)
    # Two dollar figures, and the post must use the payee one. Rolling a failed
    # payee up to its parent sweeps in the parent's other payees, which did not
    # fail: Nestle USA's closed Solon plant took $3.2M, but Nestle S.A. as a
    # parent took $9.2M across Ohio. The payee figure is the amount paid to the
    # thing that failed; the parent figure is an upper bound on exposure.
    fail_agg = defaultdict(lambda: {"parents": 0, "parent_cash": 0, "payee_cash": 0})
    payee_cash = defaultdict(int)
    if FAILURES.exists():
        for r in csv.DictReader(FAILURES.open()):
            if r["verdict"] == "Confirmed failure":
                payee_cash[r["parent"].strip() or r["name"].strip()] += int(r["paid"] or 0)
    matched = 0
    for a in allp:
        f = fail.get(a["parent"])
        if not f:
            continue
        matched += 1
        g = fail_agg[f["category"] or "Uncategorised"]
        g["parents"] += 1; g["parent_cash"] += a["cash"]; g["payee_cash"] += payee_cash.get(a["parent"], 0)
    sued_parents = [a for a in allp if sued.get(a["parent"])]
    out["lawsuits"] = {
        "parents_sued": len(sued_parents),
        "suits": sum(len(sued[a["parent"]]) for a in sued_parents),
        "cash_to_parents_sued": sum(a["cash"] for a in sued_parents),
        "suits_total": sum(len(v) for v in sued.values()),
    }
    out["failures"] = {"by_category": dict(fail_agg), "confirmed": len(fail),
                       "matched_to_a_parent": matched,
                       "payee_cash_total": sum(payee_cash.values()),
                       "parent_cash_total": sum(g["parent_cash"] for g in fail_agg.values())}
    out["rows"] = [{"fy": g["fy"], "recipient": g["recipient_name"], "city": g["city"], "state": g["state"],
                    "cash": g["cash"], "parent": parent_key(parents[g["recipient_id"]])} for g in grants]
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(out, separators=(",", ":")))

    # console summary and TIEOUT.md
    def pct(x):
        return f"{100 * x:.1f}%"
    lines = ["# Tie-out", "", "Every number below is recomputed from `data/grants_raw.csv` and `data/parents.csv` by `scripts/09_analyze.py`.", ""]
    m = out["meta"]
    lines += [f"- Schedule I rows: {m['rows']:,}; distinct recipients: {m['recipients']:,}; parents: {m['parents']:,}; FY{m['fy_min']} to FY{m['fy_max']}; cash ${m['cash_total']:,}",
              f"- Reversed payments (negative Schedule I rows): {m['reversal_rows']} rows, ${m['reversal_dollars']:,}; parents netting to zero or less, not counted as recipients: {m['parents_net_zero_or_less']} (net ${m['net_negative_dollars']:,})",
              f"- Parents counted (net payment above zero): {m['parents']:,}; with a classification: {m['resolved_parents']:,}, carrying ${m['resolved_cash']:,} of the ${m['cash_positive']:,} they were paid on net ({pct(m['resolved_cash'] / m['cash_positive'])})", ""]
    lines += ["## By recipient class (all parents)", ""]
    for k, v in sorted(out["by_class"].items(), key=lambda kv: -kv[1]["cash"]):
        lines.append(f"- {k}: {v['parents']:,} parents, ${v['cash']:,} ({pct(v['cash'] / m['cash_total'])})")
    for label, key in (("Businesses only", "business"), ("All recipients", "all")):
        b = out[key]
        lines += ["", f"## {label}", ""]
        for cut in CUTOFFS:
            p, c = b[cut]["parents"], b[cut]["cash"]
            lines.append(f"- Cutoff {cut} employees: parents small {pct(p.get('small', {'share': 0})['share'])}, large {pct(p.get('large', {'share': 0})['share'])}, unknown {pct(p.get('unknown', {'share': 0})['share'])}; "
                         f"dollars small {pct(c.get('small', {'share': 0})['share'])}, large {pct(c.get('large', {'share': 0})['share'])}, unknown {pct(c.get('unknown', {'share': 0})['share'])}")
        h = b["home"]
        lines.append(f"- Home state: parents Ohio {pct(h['parents'].get('ohio', {'share': 0})['share'])}, other {pct(h['parents'].get('other', {'share': 0})['share'])}, unknown {pct(h['parents'].get('unknown', {'share': 0})['share'])}; "
                     f"dollars Ohio {pct(h['cash'].get('ohio', {'share': 0})['share'])}, other {pct(h['cash'].get('other', {'share': 0})['share'])}, unknown {pct(h['cash'].get('unknown', {'share': 0})['share'])}")
        lines.append(f"- Worst case: dollars to large at least {pct(b['worst_case']['cash_large_min'])}; parents small at least {pct(b['worst_case']['parents_small_min'])}")
        lines.append("- Two-by-two (dollars): " + ", ".join(f"{k} {pct(v['share'])}" for k, v in b["two_by_two"]["cash"].items()))
    if out["conflicts"]:
        lines += ["", "## Conflicts between recipients of one parent", "",
                  "Resolved against the finding, not by read order: the smaller size band, Ohio, "
                  "and out of the `business` denominator.", ""] + [f"- {c}" for c in out["conflicts"]]

    # Sensitivities. The worst case moves size inside the business set; it never
    # reconsiders which recipients are businesses, and it never asks what one
    # payment is carrying. Both of those move the headline more than size does,
    # so both are computed here and belong in the post.
    lines += ["", "## Sensitivities", "",
              "These are not errors. They are the places the headline is most exposed, "
              "computed so the post can state them before a reader finds them.", ""]

    auto = [a for a in allp if (a["auto_class"] or a["class"]) == "business"]
    a_small = sum(a["cash"] for a in auto if size_group(a) == "small")
    a_tot = sum(a["cash"] for a in auto)
    b_small = sum(a["cash"] for a in biz if size_group(a) == "small")
    b_tot = sum(a["cash"] for a in biz)
    moved = [a for a in allp if a["class"] != "business"
             and (a["auto_class"] or a["class"]) == "business"]
    moved_small = [a for a in moved if size_group(a) == "small"]
    lines += [
        f"**The class boundary, and it is the largest one.** {len(moved)} parents carrying "
        f"${sum(a['cash'] for a in moved):,} were classed out of `business` by hand after the "
        f"automatic classifier called them businesses, mostly into site_development: project "
        f"LLCs and industrial developers rather than operating companies. "
        f"{len(moved_small)} of them, carrying ${sum(a['cash'] for a in moved_small):,}, would "
        f"have scored small. Recompute the headline on the automatic class instead and the "
        f"business universe goes {len(biz):,} parents / ${b_tot:,} to {len(auto):,} / ${a_tot:,}, "
        f"and the small share of business dollars goes "
        f"**{pct(b_small / b_tot)} to {pct(a_small / a_tot)}**. The published worst case does not "
        f"cover this: it reassigns size inside the business set and never reconsiders the class "
        f"boundary. The post should state this figure itself rather than wait to be asked why a "
        f"company that builds and leases industrial buildings is not a small business.", ""]

    top = sorted(biz, key=lambda a: -a["cash"])[:3]
    one = top[0]
    rest = [a for a in biz if a is not one]
    r_oh = sum(a["cash"] for a in rest if home_group(a) == "ohio")
    r_lg = sum(a["cash"] for a in rest if size_group(a) == "large")
    r_tot = sum(a["cash"] for a in rest)
    # read these off the business block by name: `b` and `h` are loop variables
    # above and hold the "all recipients" block by the time we get here
    bb = out["business"]
    h_oh = bb["home"]["cash"].get("ohio", {"share": 0})["share"]
    b_large = bb["500"]["cash"].get("large", {"share": 0})["share"]
    lines += [
        f"**One payment carries the home-state finding.** {one['parent']} alone is "
        f"${one['cash']:,}, {pct(one['cash'] / b_tot)} of all business dollars. The top three "
        f"({', '.join(a['parent'][:28] for a in top)}) are {pct(sum(a['cash'] for a in top) / b_tot)}. "
        f"Leave {one['parent']} out and Ohio's share of business dollars goes "
        f"**{pct(h_oh)} to {pct(r_oh / r_tot)}**, and the large share goes "
        f"{pct(b_large)} to {pct(r_lg / r_tot)}. "
        f"Its classification is not in doubt, so this is leverage rather than error. Name it "
        f"beside the number.", ""]

    sm = sorted((a for a in biz if size_group(a) == "small"), key=lambda a: -a["cash"])[:1]
    if sm:
        lines.append(f"**The small side is not outlier-driven,** which is the reassuring half: the "
                     f"largest small parent is {sm[0]['parent']} at ${sm[0]['cash']:,}, "
                     f"{pct(sm[0]['cash'] / b_small)} of small dollars.")
    lines += ["",
              f"**Two denominators, on purpose.** The size and home-state shares run on dollars "
              f"net of the 33 reversed payments (${m['cash_total']:,}). The conditions shares in "
              f"`data/grant_conditions.csv` run on positive payments only "
              f"(${m['cash_total'] - m['reversal_dollars']:,}), because a reversal has no program "
              f"to label. The post must say which denominator each number uses.", ""]

    if merge_notes:
        lines += ["## Parents merged as the same company written two ways", "",
                  "Merged only where the normalized name, size bucket, home state and class all "
                  "agree, so a real disagreement is never papered over.", ""]
        lines += [f"- {n}" for n in sorted(merge_notes)]
    if unmerged:
        lines += ["", "### Same normalized name, left separate because an attribute disagrees", "",
                  "Each of these is worth one look before publishing: either they are genuinely "
                  "different entities, or one of the two records is wrong.", ""]
        lines += [f"- {n}" for n in sorted(unmerged)]
    TIEOUT.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(f"\nwrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size:,} bytes) and {TIEOUT.name}")


if __name__ == "__main__":
    main()
