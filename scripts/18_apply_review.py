#!/usr/bin/env python3
"""Fold the review answers into data/parents.csv.

Two sources, in this order of authority:

1. Eric's hand review in data/review_simple.csv (`your_answer`): "y" confirms
   the size and home-state shown on that sheet; "n, ..." corrects it.
2. The agent pass in data/research2/rev_*.json for the rows Eric did not
   reach: size, home state, an employee estimate or range, and a confidence.

The review is written into its own columns (`review_*`) rather than over the
research columns, so the provenance of every call stays readable, and
09_analyze.py prefers the review value when there is one.

Eric's free-text corrections are parsed conservatively: the words large,
small, Ohio and the name of a state decide, and anything the parser cannot
read is printed for hand entry rather than guessed at.
"""
import csv, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PARENTS = ROOT / "data" / "parents.csv"
REVIEW = ROOT / "data" / "review_simple.csv"
AGENTS = sorted((ROOT / "data" / "research2").glob("rev_*.json"))
COLS = ["review_size", "review_hq", "review_employees", "review_asof",
        "review_confidence", "review_source", "review_by", "review_notes"]
STATES = {"AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD",
          "MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC",
          "SD","TN","TX","UT","VT","VA","WA","WV","WI","WY","DC"}


def parse_eric(answer, row):
    """Return (size, hq, hq_where, note) from a free-text answer, or None for
    anything the parser should not guess at."""
    a = answer.strip()
    if a.lower() == "y":
        return row["size"], row["ohio_hq"], row["hq_where"], "confirmed by Eric Pachman"
    if not a.lower().startswith("n"):
        return None
    size = "Large" if re.search(r"\blarge\b", a, re.I) else ("Small" if re.search(r"\bsmall\b", a, re.I) else row["size"])
    hq, where = row["ohio_hq"], row["hq_where"]
    if re.search(r"\bnot ohio\b|\bnot in ohio\b", a, re.I):
        hq = "No"
    elif re.search(r"\bohio\b", a, re.I) and not re.search(r"\bnot ohio\b", a, re.I) and re.search(r"\bhq|headquart", a, re.I):
        hq, where = "Yes", "OH"
    m = re.search(r"\b(?:hq|headquarter\w*|based)\b[^A-Z]{0,12}\b([A-Z]{2})\b", a)
    if m and m.group(1) in STATES:
        where = m.group(1); hq = "Yes" if where == "OH" else "No"
    return size, hq, where, f"corrected by Eric Pachman: {a}"


def parse_employees(text):
    """A number from "about 120", "250-400", "over 10,000", "5,600+"."""
    if not text:
        return None
    t = text.lower().replace(",", "")
    nums = [float(x) for x in re.findall(r"\d+(?:\.\d+)?", t)]
    if not nums:
        return None
    if re.search(r"\bthousand\b", t) and max(nums) < 100:
        nums = [n * 1000 for n in nums]
    return sum(nums) / len(nums) if len(nums) >= 2 and "-" in t else nums[0]


def main():
    rows = list(csv.DictReader(PARENTS.open()))
    fields = list(rows[0]) + [c for c in COLS if c not in rows[0]]
    by_parent = {}
    for r in rows:
        by_parent.setdefault(r["parent"].strip() or r["name"].strip(), []).append(r)
        for c in COLS:
            r.setdefault(c, "")

    applied = {"eric": 0, "agent": 0}
    unparsed = []
    review = {r["company"]: r for r in csv.DictReader(REVIEW.open())}

    def put(company, size, hq, where, emp, asof, conf, source, who, note):
        targets = by_parent.get(company)
        if not targets:
            return False
        for r in targets:
            r.update(review_size=size, review_hq=hq, review_employees=emp or "", review_asof=asof or "",
                     review_confidence=conf, review_source=source or "", review_by=who, review_notes=note[:300])
            if where:
                r["parent_hq_state"] = where
        return True

    for company, r in review.items():
        ans = (r.get("your_answer") or "").strip()
        if not ans:
            continue
        parsed = parse_eric(ans, r)
        if parsed is None:
            unparsed.append((company, ans)); continue
        size, hq, where, note = parsed
        if put(company, size, hq, where, "", "", "Confirmed by Eric", "hand review", "eric", note):
            applied["eric"] += 1

    for f in AGENTS:
        for x in json.load(f.open()):
            company = x.get("company", "")
            if company in review and (review[company].get("your_answer") or "").strip():
                continue                      # Eric's answer wins
            where = (x.get("hq_where") or "").strip()
            if put(company, x.get("size", ""), x.get("ohio_hq", ""), where,
                   x.get("employees_estimate", ""), x.get("employees_asof", ""),
                   x.get("confidence", ""), x.get("source", ""), "agent", x.get("notes", "")):
                applied["agent"] += 1

    # the review decides the size bucket too, so the cutoff control and the
    # headline both move with it: an employee figure sets the bucket, and
    # where there is none the Large/Small call shifts a contradicting bucket
    # across the 500 line and leaves a consistent one alone
    SMALL, LARGE = ("<100", "100-499"), ("500-4999", "5000+")
    changed = 0
    for r in rows:
        if not r.get("review_size"):
            continue
        n = parse_employees(r.get("review_employees", ""))
        want = r["review_size"]
        if n is not None:
            bucket = "<100" if n < 100 else "100-499" if n < 500 else "500-4999" if n < 5000 else "5000+"
        elif want == "Large" and r["emp_bucket"] in SMALL:
            bucket = "500-4999"
        elif want == "Small" and r["emp_bucket"] in LARGE:
            bucket = "100-499"
        else:
            bucket = r["emp_bucket"]
        # a figure must not contradict the call it came with
        if want == "Large" and bucket in SMALL:
            bucket = "500-4999"
        if want == "Small" and bucket in LARGE:
            bucket = "100-499"
        if bucket and bucket != r["emp_bucket"]:
            r["notes"] += f" Size bucket set to {bucket} by the {r['review_by']} review ({r.get('review_employees') or want})."
            r["emp_bucket"] = bucket
            changed += 1
    print(f"size buckets changed by the review: {changed}")

    with PARENTS.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields); w.writeheader(); w.writerows(rows)
    print(f"review applied: {applied['eric']} companies from Eric, {applied['agent']} from the agent pass")
    if unparsed:
        print("answers the parser would not guess at (enter by hand):")
        for c, a in unparsed:
            print(f"  {c}: {a}")


if __name__ == "__main__":
    main()
