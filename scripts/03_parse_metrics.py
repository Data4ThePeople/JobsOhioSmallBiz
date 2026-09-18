#!/usr/bin/env python3
"""Parse JobsOhio's Monthly Executed Grants and Loans Reports (PDF) into
data/commitments.csv, one row per executed agreement and program.

Two layouts exist. 2015 to 2021: a wide table with one dollar column per
program (Growth Fund Loan, Workforce Grant, Economic Dev. Grant, ...). 2022
onward: one line per agreement with "Program Type" and "Program Value"
columns. Both share one geometry: header words are left-aligned with the
start of their column, and the two or three lines of a header overlap
horizontally within a column.

Method: read words with positions; build columns from the header block by
horizontal overlap; place text words in the rightmost column starting at or
left of them; place dollar amounts by clustering where they actually sit
(right-aligned amounts can start a few points left of their header) and
mapping each cluster to a header column; split a header column that received
two clusters (tight layouts where 'Revitalization Grant' touches 'Inclusion
Grant'); group words into lines; attach wrapped name fragments to the nearest
data line. A wide-format row with two program amounts becomes two output rows.

Output columns: report_month, company, county, region, industry,
jobs_created, payroll, jobs_retained, investment, program, program_value,
source_file, page. Rows with no program value, pages with no header, and
pages with font-encoding damage go to data/commitments_anomalies.csv."""
import csv, re, sys
from collections import defaultdict
from pathlib import Path

import pdfplumber

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw" / "metrics"
OUT = ROOT / "data" / "commitments.csv"
ANOM = ROOT / "data" / "commitments_anomalies.csv"

MONTHS = "January|February|March|April|May|June|July|August|September|October|November|December"
MONTH_RE = re.compile(rf"during ({MONTHS}),? (\d{{4}})")
MONEY = re.compile(r"^\$[\d,.]+$")
NUM = re.compile(r"^[\d,]+$")
NA = {"N/A", "TBD", "-", "--", "n/a", "N/A*", "TBD*"}
BANNER = ("Information", "Commitments", "Below", "Monthly")
GLYPHS = "!&#%@^~|"      # characters a broken font may use for the space
ANOMALIES = []


def is_val(t):
    return bool(MONEY.match(t) or NUM.match(t)) or t in NA


def is_data_line(ln):
    """A data line carries a dollar amount or at least two numeric cells; a
    header line like 'Grant-Phase 2' carries at most one stray digit."""
    toks = [w["text"] for w in ln]
    return any(MONEY.match(t) for t in toks) or sum(1 for t in toks if is_val(t)) >= 2


def page_words(page, fname, pno):
    """Words with positions. Several 2016 pages were exported with a font
    whose space glyph reads as '!' or '&' (and hyphen as '0' or 'Y'). Split
    those on the glyph so column positions survive, and log the damage."""
    words = page.extract_words(x_tolerance=1.5, y_tolerance=2)
    joined = " ".join(w["text"] for w in words)
    glyphs = [g for g in GLYPHS if joined.count(g) > 0.015 * max(1, len(joined))]
    if glyphs:
        words = page.extract_words(x_tolerance=1.5, y_tolerance=2, split_at_punctuation="".join(glyphs))
        words = [dict(w, text=w["text"].strip("".join(glyphs))) for w in words]
        words = [w for w in words if w["text"]]
        ANOMALIES.append({"file": fname, "page": pno, "issue": f"font encoding: space read as {glyphs}; hyphens in names may read as 0 or Y", "text": ""})
    return words


def lines_of(words, ytol=3):
    rows = []
    for w in sorted(words, key=lambda w: (w["top"], w["x0"])):
        if rows and abs(rows[-1][0]["top"] - w["top"]) <= ytol:
            rows[-1].append(w)
        else:
            rows.append([w])
    return [sorted(r, key=lambda w: w["x0"]) for r in rows]


def text(ws):
    return " ".join(w["text"] for w in sorted(ws, key=lambda w: (round(w["top"]), w["x0"])))


def canonical(label):
    L = label.lower().replace(" ", "")   # 'Indu stry', 'Job s': a header word split in two
    if "company" in L: return "company"
    if "industry" in L: return "industry"
    if "region" in L: return "region"
    if "county" in L: return "county"
    if "payroll" in L: return "payroll"
    if "retained" in L: return "jobs_retained"
    if "created" in L or L == "jobs": return "jobs_created"
    if "investment" in L: return "investment"
    if "type" in L: return "program_type"     # 'Program Type' or, some 2022 months, 'Record Type'
    if "value" in L: return "program_value"
    return "prog:" + re.sub(r"\s+", " ", label).strip()


def header_block(lines):
    """Index of the first data line and the header lines before it."""
    hc = next((i for i, ln in enumerate(lines) if ln[0]["text"] == "Company" and ln[0]["x0"] < 120), None)
    if hc is None:
        return None, None
    block = []
    if hc > 0 and lines[hc][0]["top"] - lines[hc - 1][0]["top"] < 9 and not any(w["text"] in BANNER for w in lines[hc - 1]):
        block.append(lines[hc - 1])
    block.append(lines[hc])
    j = hc + 1
    while j < len(lines) and not is_data_line(lines[j]) and lines[j][0]["top"] - lines[hc][0]["top"] < 30:
        block.append(lines[j]); j += 1
    return j, block


def merge_columns(words):
    """Group header words into columns. Words on the same header line join
    when they nearly touch ('Economic Dev.', 'Program Type'); words on
    different lines join only when they overlap horizontally, because
    'Retained' and 'Investment' can sit a point apart on adjacent lines."""
    cols = []
    for w in sorted(words, key=lambda w: w["x0"]):
        for c in cols:
            same_line = any(abs(w["top"] - cw["top"]) < 2 for cw in c["words"])
            gap = w["x0"] - c["x1"]
            if (same_line and gap <= 2.5) or (not same_line and gap < 0 and w["x1"] > c["x0"]):
                c["x0"] = min(c["x0"], w["x0"]); c["x1"] = max(c["x1"], w["x1"]); c["words"].append(w)
                break
        else:
            cols.append({"x0": w["x0"], "x1": w["x1"], "words": [w]})
    return sorted(cols, key=lambda c: c["x0"])


def money_clusters(body, gap=16):
    """Clusters of dollar amounts by x-center. Amounts in one column vary in
    width by a few points; adjacent columns sit 25 points or more apart."""
    xs = sorted(((w["x0"] + w["x1"]) / 2, w["x0"]) for ln in body for w in ln if MONEY.match(w["text"]))
    clusters = []
    for xc, x0 in xs:
        if clusters and xc - clusters[-1]["centers"][-1] <= gap:
            clusters[-1]["centers"].append(xc); clusters[-1]["min_x0"] = min(clusters[-1]["min_x0"], x0)
        else:
            clusters.append({"centers": [xc], "min_x0": x0})
    for c in clusters:
        c["lo"], c["hi"] = c["centers"][0] - gap / 2, c["centers"][-1] + gap / 2
    return clusters


def build_layout(lines):
    """Return (first data line index, layout) or (None, None). layout has
    'text_cols': [(name, x0)] for text placement and 'money': [(lo, hi, name)]
    for dollar placement, plus 'long' (long format flag)."""
    j, block = header_block(lines)
    if j is None:
        return None, None
    cols = merge_columns([w for ln in block for w in ln])
    for c in cols:
        c["name"] = canonical(text(c["words"]))
    names = [c["name"] for c in cols]
    if "company" not in names or "payroll" not in names:
        return None, None
    long_fmt = "program_value" in names
    body = lines[j:]
    clusters = money_clusters(body)
    # map each dollar cluster to the header column with the largest x0 at or
    # left of the cluster's leftmost amount, allowing 4pt of right-aligned overhang
    for cl in clusters:
        owner = None
        for c in cols:
            if c["x0"] <= cl["min_x0"] + 4:
                owner = c
        cl["owner"] = owner
    money = []
    for c in cols:
        mine = [cl for cl in clusters if cl["owner"] is c]
        if len(mine) <= 1 or not c["name"].startswith("prog:"):
            for cl in mine:
                money.append((cl["lo"], cl["hi"], c["name"]))
            continue
        # a merged header: split its words between the clusters
        groups = [[] for _ in mine]
        for w in c["words"]:
            k = max(0, sum(1 for cl in mine if cl["min_x0"] - 4 <= w["x0"]) - 1)
            groups[k].append(w)
        for cl, g in zip(mine, groups):
            money.append((cl["lo"], cl["hi"], canonical(text(g)) if g else c["name"]))
    text_cols = [(c["name"], c["x0"]) for c in cols]
    # Some months center the header over a left-aligned text column, so the
    # header x0 is not where the text starts, and a broken header word ('C',
    # 'ou' for County) can merge into a neighbor. Text columns are therefore
    # anchored on the body: the positions where cells begin (a word with no
    # neighbor ending within 3pt to its left) left of the first numeric
    # column. When exactly four such starts are strong, they are named in the
    # layout's fixed order; otherwise the header positions stand.
    nums = sorted(w["x0"] for ln in body for w in ln if NUM.match(w["text"]))
    data_lines = [ln for ln in body if is_data_line(ln)]
    # the first numeric column: the leftmost x where a good share of the
    # numbers begin (a company name that starts with a digit does not count)
    num_min = next((x for x in nums if sum(1 for y in nums if x <= y <= x + 14) >= 0.4 * max(1, len(data_lines))), None)
    if num_min is not None:
        starts_x = []
        for ln in body:
            for k, w in enumerate(ln):
                if w["x0"] >= num_min - 2 or is_val(w["text"]):
                    continue
                if k > 0 and w["x0"] - ln[k - 1]["x1"] <= 3:
                    continue
                starts_x.append(w["x0"])
        starts = []
        for x in sorted(starts_x):
            if starts and x - starts[-1][-1] <= 3:
                starts[-1].append(x)
            else:
                starts.append([x])
        strong = [cl[0] for cl in starts if len(cl) >= 0.5 * max(1, len(data_lines))]
        order = ["company", "county", "region", "industry"] if long_fmt else ["company", "industry", "region", "county"]
        if len(strong) == 4:
            text_cols = [(n, x) for n, x in text_cols if n not in order]
            text_cols += list(zip(order, strong))
    if long_fmt:
        # the program-type text is centered under its header on some pages;
        # start that column where the type words actually begin
        inv = [cl for cl in clusters if cl["owner"] is not None and cl["owner"]["name"] == "investment"]
        pv = [cl for cl in clusters if cl["owner"] is not None and cl["owner"]["name"] == "program_value"]
        if inv and pv:
            right_of_inv = max(w["x1"] for ln in body for w in ln if MONEY.match(w["text"]) and inv[0]["lo"] <= (w["x0"] + w["x1"]) / 2 <= inv[0]["hi"])
            starts = [w["x0"] for ln in body for w in ln if right_of_inv < w["x0"] < pv[0]["lo"] and not is_val(w["text"])]
            if starts:
                text_cols = [(n, min(starts) if n == "program_type" else x) for n, x in text_cols]
    return j, {"text_cols": sorted(text_cols, key=lambda t: t[1]), "money": money, "long": long_fmt}


def place(word, layout):
    if MONEY.match(word["text"]):
        xc = (word["x0"] + word["x1"]) / 2
        for lo, hi, name in layout["money"]:
            if lo <= xc <= hi:
                return name
    best = layout["text_cols"][0][0]
    for name, x0 in layout["text_cols"]:
        if x0 <= word["x0"] + 2.5:
            best = name
        else:
            break
    return best


def parse_page(page, fname, pno, carry):
    words = page_words(page, fname, pno)
    lines = lines_of(words)
    month = None
    for ln in lines[:6]:
        m = MONTH_RE.search(text(ln))
        if m:
            month = f"{m.group(2)}-{m.group(1)[:3]}"
            break
    j, layout = build_layout(lines)
    if layout is None:
        if carry is None:
            ANOMALIES.append({"file": fname, "page": pno, "issue": "no header", "text": text(lines[0])[:120] if lines else ""})
            return None, [], None
        layout, j = carry, 0
    rows, orphans = [], []
    for ln in lines[j:]:
        t = text(ln)
        if t.startswith(("NOTE", "Note", "*", "For projects", "Below is", "Monthly Executed", "Project Information")):
            continue
        cells = defaultdict(list)
        for w in ln:
            cells[place(w, layout)].append(w["text"])
        cells = {k: " ".join(v) for k, v in cells.items()}
        has_val = any(is_val(tok) for k in ("payroll", "investment", "jobs_created", "jobs_retained", "program_value")
                      for tok in cells.get(k, "").split())
        if has_val:
            rows.append({"cells": cells, "top": ln[0]["top"]})
        else:
            orphans.append((ln[0]["top"], cells))
    for top, cells in orphans:
        if not rows:
            continue
        near = min(rows, key=lambda r: abs(r["top"] - top))
        if abs(near["top"] - top) > 14:
            continue
        for k, v in cells.items():
            if k in ("company", "industry", "county", "region", "program_type"):
                if top < near["top"]:
                    near["cells"][k] = (v + " " + near["cells"].get(k, "")).strip()
                else:
                    near["cells"][k] = (near["cells"].get(k, "") + " " + v).strip()
    out = []
    prog_names = sorted({n for _, _, n in layout["money"] if n.startswith("prog:")})
    for r in rows:
        c = r["cells"]
        base = {"report_month": month, "company": c.get("company", ""), "county": c.get("county", ""),
                "region": c.get("region", ""), "industry": c.get("industry", ""),
                "jobs_created": c.get("jobs_created", ""), "payroll": c.get("payroll", ""),
                "jobs_retained": c.get("jobs_retained", ""), "investment": c.get("investment", ""),
                "source_file": fname, "page": pno}
        progs = []
        if layout["long"] and c.get("program_value"):
            progs.append((c.get("program_type", ""), c["program_value"]))
        for name in prog_names:
            for v in c.get(name, "").split():
                progs.append((name[5:], v))
        if not progs or not base["company"]:
            ANOMALIES.append({"file": fname, "page": pno, "issue": "no program value" if not progs else "no company", "text": str(c)[:300]})
        for pt, pv in progs:
            out.append({**base, "program": pt, "program_value": pv})
    return month, out, layout


def main():
    files = sorted(RAW.glob("*.pdf"))
    if not files:
        sys.exit("no PDFs in data/raw/metrics")
    rows = []
    for f in files:
        n0, carry = len(rows), None
        with pdfplumber.open(f) as pdf:
            for i, page in enumerate(pdf.pages, 1):
                month, r, carry = parse_page(page, f.name, i, carry)
                rows += r
        months = sorted({r["report_month"] for r in rows[n0:] if r["report_month"]})
        progs = sorted({r["program"] for r in rows[n0:]})
        print(f"{f.name:38s} rows={len(rows)-n0:4d} months={len(months):2d} programs={len(progs)}")
    with OUT.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    with ANOM.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["file", "page", "issue", "text"]); w.writeheader(); w.writerows(ANOMALIES)
    print(f"wrote {OUT.name}: {len(rows)} rows; {ANOM.name}: {len(ANOMALIES)} anomalies")


if __name__ == "__main__":
    main()
