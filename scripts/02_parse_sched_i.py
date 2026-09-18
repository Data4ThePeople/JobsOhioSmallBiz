#!/usr/bin/env python3
"""Parse Schedule I Part II from every 990 XML in data/raw/990/ into
data/grants_raw.csv, one row per Schedule I line, and write the per-year
reconciliation against Part IX line 1 to data/reconcile_990.csv.

Fields kept exactly as filed (name case, punctuation). Normalization happens in
04_normalize.py so the raw file stays a faithful copy of the return.
A duplicate (fiscal_year, recipient_ein, name, amount) tuple is a hard failure:
it would mean a row was parsed twice."""
import csv, sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw" / "990"
OUT = ROOT / "data" / "grants_raw.csv"
RECON = ROOT / "data" / "reconcile_990.csv"
NS = {"i": "http://www.irs.gov/efile"}

COLS = ["fiscal_year", "object_id", "row_in_filing", "recipient_name", "recipient_name_2",
        "recipient_ein", "street", "city", "state", "zip", "irc_section",
        "cash_amt", "noncash_amt", "purpose"]


def tx(el, path):
    x = el.find(path, NS)
    return (x.text or "").strip() if x is not None and x.text else ""


def parse(path):
    root = ET.parse(path).getroot()
    end = tx(root, ".//i:TaxPeriodEndDt")
    fy = int(end[:4])
    oid = path.stem.split("_")[-1]
    si = root.find(".//i:IRS990ScheduleI", NS)
    if si is None:
        sys.exit(f"{path.name}: no Schedule I")
    rows = []
    for n, r in enumerate(si.findall("i:RecipientTable", NS), 1):
        rows.append({
            "fiscal_year": fy, "object_id": oid, "row_in_filing": n,
            "recipient_name": tx(r, "i:RecipientBusinessName/i:BusinessNameLine1Txt"),
            "recipient_name_2": tx(r, "i:RecipientBusinessName/i:BusinessNameLine2Txt"),
            "recipient_ein": tx(r, "i:RecipientEIN"),
            "street": tx(r, "i:USAddress/i:AddressLine1Txt"),
            "city": tx(r, "i:USAddress/i:CityNm"),
            "state": tx(r, "i:USAddress/i:StateAbbreviationCd"),
            "zip": tx(r, "i:USAddress/i:ZIPCd"),
            "irc_section": tx(r, "i:IRCSectionDesc"),
            "cash_amt": int(float(tx(r, "i:CashGrantAmt") or 0)),
            "noncash_amt": int(float(tx(r, "i:NonCashAssistanceAmt") or 0)),
            "purpose": tx(r, "i:PurposeOfGrantTxt"),
        })
    recon = {
        "fiscal_year": fy, "object_id": oid, "period_end": end,
        "return_version": root.get("returnVersion", ""),
        "amended": "yes" if root.find(".//i:AmendedReturnInd", NS) is not None else "no",
        "sched_i_rows": len(rows),
        "sched_i_cash": sum(r["cash_amt"] for r in rows),
        "sched_i_noncash": sum(r["noncash_amt"] for r in rows),
        "filer_count_501c3_gov": tx(si, "i:Total501c3OrgCnt"),
        "filer_count_other": tx(si, "i:TotalOtherOrgCnt"),
        "part_ix_line1_grants_domestic_orgs": tx(root, ".//i:GrantsToDomesticOrgsGrp/i:TotalAmt"),
        "part_ix_line2_grants_individuals": tx(root, ".//i:GrantsToDomesticIndividualsGrp/i:TotalAmt"),
        "total_expenses": tx(root, ".//i:TotalExpensesGrp/i:TotalAmt") or tx(root, ".//i:CYTotalExpensesAmt"),
    }
    return rows, recon


def main():
    files = sorted(RAW.glob("jobsohio_fy*.xml"))
    if not files:
        sys.exit("no XML files; run 01_fetch_990.py")
    all_rows, recons = [], []
    for f in files:
        rows, recon = parse(f)
        all_rows += rows
        recons.append(recon)
        print(f"FY{recon['fiscal_year']}: {len(rows):4d} rows  ${recon['sched_i_cash']:>13,}  "
              f"Part IX L1 ${int(recon['part_ix_line1_grants_domestic_orgs'] or 0):>13,}  "
              f"filer counts {recon['filer_count_501c3_gov']}+{recon['filer_count_other']}")
    keys = [(r["fiscal_year"], r["recipient_ein"], r["recipient_name"], r["cash_amt"]) for r in all_rows]
    dups = {k for k in keys if keys.count(k) > 1}
    if dups:
        sys.exit(f"duplicate rows parsed: {sorted(dups)[:5]}")
    fys = [r["fiscal_year"] for r in recons]
    if len(fys) != len(set(fys)):
        sys.exit("two files for one fiscal year")
    OUT.parent.mkdir(exist_ok=True)
    with OUT.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS); w.writeheader(); w.writerows(all_rows)
    with RECON.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(recons[0])); w.writeheader(); w.writerows(recons)
    print(f"wrote {OUT.name}: {len(all_rows)} rows, ${sum(r['cash_amt'] for r in all_rows):,} cash, "
          f"FY{min(fys)} to FY{max(fys)}; {RECON.name}: {len(recons)} years")


if __name__ == "__main__":
    main()
