#!/usr/bin/env python3
"""Rule-based classification for recipients the automated signals settle,
applied only to rows with no researched parent yet. Every row it fills
records the rule in emp_source / notes so a reader can see why.

Rules, in order:
  R1 Inclusion Grant only. JobsOhio's Inclusion (Small Business) Grant is
     restricted to small businesses and capped at $50,000. Class business,
     parent = the recipient, home state OH (the program funds Ohio
     businesses), bucket <100 or 100-499 by the larger of jobs retained and
     Form 5500 participants. Skipped if either signal reaches 500. Grade B.
  R2 Form 5500 under 250 participants, no subsidiary marker in the name, not
     an SEC registrant. Parent = the recipient, home state = the plan
     sponsor's state, bucket <100 or 100-499 by participants. Skipped if jobs
     retained reaches 500. Grade B.
  R3 Form 5500 at 1,500 or more participants, no subsidiary marker. Bucket
     500-4999, or 5000+ at 10,000 participants (retirees inflate counts).
     Home state = sponsor's state. Grade B.
  R4 Non-business classes (government, university, hospital, nonprofit,
     site_development by the seed heuristic) with an Ohio address: parent =
     the recipient, home state OH, bucket from Form 5500 if any. Grade B.
Everything else is left for research."""
import csv, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PARENTS = ROOT / "data" / "parents.csv"
SUB = re.compile(r"\b(usa|america|americas|north america|of ohio|ohio inc|holdings|international|group|us inc|na inc|na llc|dedc|division|subsidiary|midwest|east|west)\b", re.I)


def p5500(r):
    v = [(int(r[f"f5500_participants_{y}"]), y) for y in ("2015", "2019", "2023") if r[f"f5500_participants_{y}"]]
    return max(v) if v else (None, None)


def bucket_small(n):
    return "<100" if n < 100 else "100-499"


def main():
    rows = list(csv.DictReader(PARENTS.open()))
    counts = {}
    for r in rows:
        if r["parent"]:
            continue
        progs = {p.strip() for p in r["metrics_programs"].split(";") if p.strip()}
        jr = int(r["metrics_jobs_retained_max"]) if r["metrics_jobs_retained_max"] else 0
        p, py = p5500(r)
        sponsor_state = ""
        # sponsor state comes from f5500_participants.csv via 05; not carried, so infer from address only when Ohio
        cls = r["recipient_class_auto"]
        rule = None
        if cls == "business" and progs == {"Inclusion Grant"} and jr < 500 and (p is None or p < 500):
            rule = "R1"
            r.update(recipient_class="business", parent=r["name"], parent_hq_state="OH",
                     hq_source="JobsOhio Inclusion Grant program rule (Ohio small business); JobsOhio monthly metrics report",
                     emp_bucket=bucket_small(max(jr, p or 0)), emp_source="JobsOhio Inclusion Grant eligibility (small business, cap $50,000); metrics jobs retained " + str(jr) + (f"; Form 5500 {py}: {p} participants" if p else ""),
                     emp_asof=(r["years"].split()[-1] if r["years"] else ""), confidence="B",
                     notes="Rule R1: Inclusion Grant recipient with no contrary size signal.")
        elif cls == "business" and p is not None and p < 250 and jr < 500 and not SUB.search(r["name"]) and not r["edgar_cik"]:
            rule = "R2"
            r.update(recipient_class="business", parent=r["name"], parent_hq_state=r["f5500_sponsor_state"] or r["state"],
                     hq_source=f"Form 5500 plan sponsor address ({py})", emp_bucket=bucket_small(max(p, jr)),
                     emp_source=f"Form 5500 {py}: {p} participants, largest plan, sponsor {r['f5500_sponsor']}" + (f"; metrics jobs retained {jr}" if jr else ""),
                     emp_asof=py, confidence="B", notes="Rule R2: own plan under 250 participants, no subsidiary marker in the name, not an SEC registrant.")
        elif cls == "business" and p is not None and p >= 1500 and not SUB.search(r["name"]):
            rule = "R3"
            r.update(recipient_class="business", parent=r["name"], parent_hq_state=r["f5500_sponsor_state"] or r["state"],
                     hq_source=f"Form 5500 plan sponsor address ({py})", emp_bucket="5000+" if (p >= 10000 or jr >= 5000) else "500-4999",
                     emp_source=f"Form 5500 {py}: {p} participants, largest plan, sponsor {r['f5500_sponsor']}" + (f"; metrics jobs retained {jr}" if jr else ""),
                     emp_asof=py, confidence="B", notes="Rule R3: own plan at 1,500 or more participants; counts include retirees, so the bucket is conservative.")
        elif cls != "business" and r["state"] == "OH":
            rule = "R4"
            r.update(recipient_class=cls, parent=r["name"], parent_hq_state="OH", hq_source="Schedule I address; Ohio public or nonprofit entity",
                     emp_bucket=("5000+" if p and p >= 10000 else "500-4999" if p and p >= 1500 else bucket_small(p) if p is not None and p < 250 else ""),
                     emp_source=(f"Form 5500 {py}: {p} participants" if p else ""), emp_asof=py or "", confidence="B",
                     notes=f"Rule R4: {cls} by name and IRC section; not in the business headline.")
        if rule:
            counts[rule] = counts.get(rule, 0) + 1
    with PARENTS.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    done = sum(1 for r in rows if r["parent"])
    print("auto-classified:", counts, f"-> {done}/{len(rows)} rows have a parent; {len(rows) - done} left for research")


if __name__ == "__main__":
    main()
