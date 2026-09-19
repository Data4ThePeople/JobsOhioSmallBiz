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
group and the worst-case bounds reassign them against the thesis."""
import csv, json, sys
from collections import defaultdict, Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GRANTS = ROOT / "data" / "grants_raw.csv"
PARENTS = ROOT / "data" / "parents.csv"
OUT = ROOT / "dist" / "data.json"
TIEOUT = ROOT / "TIEOUT.md"

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
    return grants, parents


def parent_key(p):
    return p["parent"].strip() if p["parent"].strip() else p["name"].strip()


def build_parents(grants, parents):
    """One record per parent with class, bucket, home state, confidence, dollars."""
    agg = {}
    for g in grants:
        p = parents[g["recipient_id"]]
        k = parent_key(p)
        a = agg.setdefault(k, {"parent": k, "class": "", "bucket": "", "hq": "", "conf": "", "founded_oh": "",
                               "recipients": set(), "rows": 0, "cash": 0, "years": set(), "by_fy": Counter(),
                               "sources": set(), "programs": set(), "resolved": False})
        a["recipients"].add(g["recipient_id"]); a["rows"] += 1; a["cash"] += g["cash"]
        a["years"].add(g["fy"]); a["by_fy"][g["fy"]] += g["cash"]
        cls = p["recipient_class"] or p["recipient_class_auto"]
        # a parent's attributes come from its researched recipients; the first
        # researched one wins, and any disagreement is reported
        if p["parent"]:
            a["resolved"] = True
            for field, col in (("class", cls), ("bucket", p["emp_bucket"]), ("hq", p["parent_hq_state"]),
                               ("conf", p["confidence"]), ("founded_oh", p["founded_in_ohio"])):
                if col and not a[field]:
                    a[field] = col
                elif col and a[field] and a[field] != col and field in ("bucket", "hq"):
                    a.setdefault("conflicts", set()).add(f"{field}: {a[field]} vs {col} ({p['name']})")
            for s in (p["hq_source"], p["emp_source"]):
                if s:
                    a["sources"].add(s)
        elif not a["class"]:
            a["class"] = cls
        for prog in p["metrics_programs"].split(";"):
            if prog.strip():
                a["programs"].add(prog.strip())
    return agg


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
            if g == "unknown" or a["conf"] in ("C", "D"):
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
    out["parents_table"] = sorted([{
        "parent": a["parent"], "class": a["class"], "bucket": a["bucket"], "hq": a["hq"], "conf": a["conf"],
        "founded_oh": a["founded_oh"], "cash": a["cash"], "rows": a["rows"], "recipients": len(a["recipients"]),
        "years": sorted(a["years"]), "programs": sorted(a["programs"]), "sources": sorted(a["sources"])[:3],
        "by_fy": {str(k): v for k, v in sorted(a["by_fy"].items())},
        "payees": " | ".join(sorted({parents[r]["name"] for r in a["recipients"]}))[:400],
    } for a in allp], key=lambda d: -d["cash"])
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
        lines += ["", "## Conflicts between recipients of one parent", ""] + [f"- {c}" for c in out["conflicts"]]
    TIEOUT.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(f"\nwrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size:,} bytes) and {TIEOUT.name}")


if __name__ == "__main__":
    main()
