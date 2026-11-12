#!/usr/bin/env python3
"""Fold the site-developer re-check into data/parents.csv.

Why this pass exists: `site_development` excludes a recipient from the headline
denominator, so every one of those calls is load-bearing. An independent tie-out
found that reversing the whole batch would move the small-business share of
dollars from 18.1% to 26.2%, and the editor then caught a real error in it
(Tractor Supply, a retailer, classed as a developer because one of its payees
was a project LLC).

The test applied to all 122, recorded per row in `data/site_dev_review.csv`:
whose business is building? A developer who builds and leases to others stays
`site_development`. An operating company that received money to build, expand
or clean up its own facility is that operating company, whatever the payee
vehicle is called.

Only rows whose `verdict` differs from `site_development` are applied, and each
one writes its reason and source into the parent's research columns so the call
can be defended line by line. An employee figure, where the review found one,
sets the size bucket the same way 18_apply_review.py does.
"""
import csv, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from names import normalize_name

PARENTS = ROOT / "data" / "parents.csv"
REVIEW = ROOT / "data" / "site_dev_review.csv"
CLASSES = {"business", "site_development", "government", "university", "hospital", "nonprofit"}


def bucket_for(text):
    """A size bucket from "330", "10-59", "about 6,800", or None."""
    if not text:
        return None
    nums = [float(x) for x in re.findall(r"\d[\d,]*", text.replace(",", ""))]
    if not nums:
        return None
    n = sum(nums) / len(nums) if len(nums) > 1 else nums[0]
    return "<100" if n < 100 else "100-499" if n < 500 else "500-4999" if n < 5000 else "5000+"


def main():
    if not REVIEW.exists():
        sys.exit(f"no {REVIEW.relative_to(ROOT)}; run the review first")
    review = {normalize_name(r["parent"]): r for r in csv.DictReader(REVIEW.open())}
    rows = list(csv.DictReader(PARENTS.open()))
    fields = list(rows[0])

    applied, rebucketed, skipped = 0, 0, []
    for r in rows:
        key = normalize_name(r["parent"].strip() or r["name"].strip())
        rev = review.get(key)
        if not rev:
            continue
        verdict = (rev["verdict"] or "").strip()
        if verdict == "site_development" or not verdict:
            continue
        if verdict not in CLASSES:
            skipped.append((r["parent"], verdict))
            continue
        r["recipient_class"] = verdict
        note = f"Class set to {verdict} by the site-developer re-check: {rev['reason']}"
        r["notes"] = (r.get("notes", "") + " " + note).strip()[:900]
        if rev.get("source"):
            r["hq_source"] = r["hq_source"] or rev["source"]
        applied += 1
        b = bucket_for(rev.get("employees", ""))
        if b and b != r["emp_bucket"]:
            r["notes"] = (r["notes"] + f" Size bucket set to {b} from the re-check "
                          f"({rev['employees']}, {rev.get('employees_asof') or 'date not stated'}).")[:900]
            r["emp_bucket"] = b
            rebucketed += 1

    with PARENTS.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields); w.writeheader(); w.writerows(rows)
    print(f"site-developer re-check applied: {applied} recipients reclassified, "
          f"{rebucketed} size buckets set from it")
    if skipped:
        print("verdicts the script would not guess at:")
        for p, v in skipped:
            print(f"  {p}: {v!r}")
    open_rows = [r for r in review.values() if "OPEN" in (r.get("notes") or "")]
    flag_rows = [r for r in review.values() if "FLAG" in (r.get("notes") or "")]
    print(f"left as site_development but unsettled (OPEN): {len(open_rows)}")
    print(f"kept, but a reader could dispute (FLAG):       {len(flag_rows)}")


if __name__ == "__main__":
    main()
