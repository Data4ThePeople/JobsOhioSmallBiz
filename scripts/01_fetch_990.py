#!/usr/bin/env python3
"""Download JobsOhio's Form 990 e-file XMLs (EIN 45-2798687) into data/raw/990/.

Source: GivingTuesday 990 Data Lake, anonymous HTTPS. One file per fiscal year,
named by IRS object id. Object ids and years are in DATASETS.md. A file already
on disk is not re-downloaded. The FY2025 filing is not in the lake yet; drop it
in data/raw/990/ by hand from ProPublica (see DATASETS.md) and this script
reports it as present or missing."""
import sys, urllib.request
from pathlib import Path

RAW = Path(__file__).resolve().parent.parent / "data" / "raw" / "990"
LAKE = "https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{}_public.xml"
UA = "Data 4 The People research (eric@asaltollc.com)"

# fiscal year end -> IRS object id
FILINGS = {
    2014: "201413189349308116",
    2015: "201630469349301988",
    2016: "201700099349300615",
    2017: "201811169349300106",
    2018: "201900849349300615",
    2019: "202020599349300902",
    2020: "202140579349301709",
    2021: "202231369349300238",
    2022: "202321359349316252",
    2023: "202421369349306592",
    2024: "202531359349316618",
    2025: "202641359349309474",
}


def fetch(fy, oid):
    out = RAW / f"jobsohio_fy{fy}_{oid}.xml"
    if out.exists() and out.stat().st_size > 1000:
        return out, "on disk"
    req = urllib.request.Request(LAKE.format(oid), headers={"User-Agent": UA})
    try:
        body = urllib.request.urlopen(req, timeout=120).read()
    except urllib.error.HTTPError as e:
        return out, f"HTTP {e.code}"
    if not body.lstrip().startswith(b"<?xml") and b"<Return" not in body[:2000]:
        return out, "not XML"
    out.write_bytes(body)
    return out, f"downloaded {len(body):,} bytes"


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    missing = []
    for fy, oid in FILINGS.items():
        out, status = fetch(fy, oid)
        print(f"FY{fy}  {oid}  {status}")
        if not out.exists():
            missing.append(fy)
    if missing:
        print(f"missing: {missing}. FY2025 must be downloaded in a browser from "
              f"https://projects.propublica.org/nonprofits/download-xml?object_id={FILINGS[2025]} "
              f"and saved as {RAW / f'jobsohio_fy2025_{FILINGS[2025]}.xml'}")
        sys.exit(1)


if __name__ == "__main__":
    main()
