#!/usr/bin/env python3
"""Parse Schedule I Part II out of a Form 990 PDF, for a year with no e-file XML.

FY2025 (year ending June 30, 2025) is not in the GivingTuesday data lake, not in
the IRS S3 bucket and not on ProPublica. JobsOhio posts its own return as a PDF
at jobsohio.com/files/tax-returns/, so that is the only source for the year.

This is a fallback, not the main path. 02_parse_sched_i.py reads the XML and is
exact. Here the return is read by position rather than by text order, because
the first Schedule I page lays its columns out in a different reading order from
the continuation pages: `extract_text()` returns six names, then six EINs, then
six amounts, and pairing those by order is a guess. The geometry is the same on
every page and is not a guess.

Each recipient is one horizontal band holding, left to right:

    x<200   CITY, ST ZIP          x~213  EIN
    x~370   cash amount           x~468  non-cash amount
    x~637   purpose of grant

with the name and street on the bands immediately above, also at x<200. An
optional IRC section sits between the EIN and the cash column.

Every parse is checked against the filer's own recipient count on Schedule I
Part I lines 2 and 3, and the script fails rather than write a file that does
not foot.

Usage: 23_parse_sched_i_pdf.py <pdf> <fiscal_year> [--out <csv>]
"""
import csv, re, sys
from pathlib import Path

import pdfplumber

ROOT = Path(__file__).resolve().parent.parent
FILER_EIN = "45-2798687"

EIN = re.compile(r"^\d{2}-\d{7}$")
MONEY = re.compile(r"^-?[\d,]+\.?$")
CITY = re.compile(r"^(.+?),\s*([A-Z]{2})\s+(\d{5}(?:-\d{4})?)$")

# column edges, in PDF points, read off the rendered return
X_LEFT, X_EIN, X_IRC, X_CASH, X_NONCASH, X_PURPOSE = 200, (205, 245), (245, 350), (350, 445), (445, 520), 600
BAND = 4          # y-tolerance for "same row", in points
NAME_BANDS = 4    # how far above an anchor to look for the name and street


def bands(page):
    """{rounded y: [words left to right]} for one page."""
    out = {}
    for w in page.extract_words():
        out.setdefault(round(w["top"] / BAND), []).append(w)
    for k in out:
        out[k].sort(key=lambda w: w["x0"])
    return out


def text_at(words, lo, hi=None):
    sel = [w["text"] for w in words if (lo <= w["x0"] < hi if hi else w["x0"] < lo)]
    return " ".join(sel).strip()


def parse_page(page):
    rows = bands(page)
    keys = sorted(rows)
    anchors = []
    for i, k in enumerate(keys):
        ein = next((w["text"] for w in rows[k]
                    if X_EIN[0] <= w["x0"] < X_EIN[1] and EIN.match(w["text"])), None)
        if ein and ein != FILER_EIN:
            anchors.append((i, k, ein))

    out = []
    for n, (i, k, ein) in enumerate(anchors):
        band = rows[k]
        city_line = text_at(band, X_LEFT)
        cash = text_at(band, *(X_CASH[0], X_CASH[1]))
        noncash = text_at(band, *(X_NONCASH[0], X_NONCASH[1]))
        irc = text_at(band, *(X_IRC[0], X_IRC[1]))
        purpose = text_at(band, X_PURPOSE, 10_000)
        if not MONEY.match(cash.replace(" ", "")):
            continue
        # Collect the whole left column for this recipient: the bands above,
        # then the anchor band itself. The address wraps, so the city can sit
        # on the band above while only its ZIP lands beside the EIN (Miami
        # University reads "... - OXFORD, OH" then "45056"). Reading the anchor
        # band alone loses the city and swallows the street into the name.
        stop = anchors[n - 1][0] if n else -1
        above = []
        for j in range(i - 1, max(stop, i - 1 - NAME_BANDS), -1):
            line = text_at(rows[keys[j]], X_LEFT)
            if not line or CITY.match(line):
                break
            above.append(line)
        above.reverse()
        if city_line:
            above.append(city_line)

        # the form separates name, street and city with " - " when a block
        # wraps, so split on it and treat the pieces as one ordered list
        parts = []
        for line in above:
            parts += [x.strip() for x in line.split(" - ") if x.strip()]

        city = state = zipc = ""
        for take in (1, 2):                      # the city may span two pieces
            if len(parts) < take:
                break
            cand = " ".join(parts[-take:])
            m = CITY.match(cand)
            if m:
                # "PO BOX 631547 - CINCINNATI, OH 45263" leaves the box number
                # inside the city capture; the city is the last " - " piece
                city = m.group(1).split(" - ")[-1].strip()
                lead = m.group(1)[:len(m.group(1)) - len(city)].strip(" -")
                state, zipc = m.group(2), m.group(3)
                parts = parts[:-take] + ([lead] if lead else [])
                break
        # "PO BOX" and its number can land on separate bands; rejoin them so
        # the box number does not become the whole street
        if len(parts) > 2 and parts[-2].upper().rstrip(".").endswith(("PO BOX", "P O BOX", "P.O. BOX")):
            parts[-2:] = [" ".join(parts[-2:])]
        street = parts.pop().strip(" -") if len(parts) > 1 else ""
        name = " ".join(parts).strip(" -")
        city = city.strip(" -")
        out.append({"name": name, "street": street, "city": city, "state": state,
                    "zip": zipc, "ein": ein, "irc": irc,
                    "cash": int(float(cash.rstrip(".").replace(",", "") or 0)),
                    "noncash": int(float((noncash or "0").rstrip(".").replace(",", "") or 0)),
                    "purpose": purpose})
    return out


def filer_counts(pdf):
    """Schedule I Part I lines 2 and 3: the filer's own recipient counts.

    Each count sits in the far-right answer column on, or just above, the band
    carrying its question. Reading "the last two numbers on the page" instead
    picks up "990" out of "Form 990".
    """
    for page in pdf.pages:
        if "Enter total number of section 501(c)(3)" not in (page.extract_text() or ""):
            continue
        rows = bands(page)
        got = {}
        for k, line in rows.items():
            txt = " ".join(w["text"] for w in line)
            which = ("c3gov" if "Enter total number of section 501(c)(3)" in txt
                     else "other" if "Enter total number of other organizations" in txt else None)
            if not which:
                continue
            # the answer is in the right-hand column, same band or the one above
            for kk in (k, k - 1, k + 1):
                for w in rows.get(kk, []):
                    if w["x0"] > 700 and re.fullmatch(r"\d{1,4}\.", w["text"]):
                        got.setdefault(which, int(w["text"].rstrip(".")))
        if len(got) == 2:
            return got["c3gov"], got["other"]
    return None


def main(argv):
    if len(argv) < 2:
        sys.exit(__doc__)
    pdf_path, fy = Path(argv[0]), int(argv[1])
    out = (Path(argv[argv.index("--out") + 1]) if "--out" in argv
           else ROOT / "data" / f"grants_fy{fy}.csv")

    rows = []
    with pdfplumber.open(str(pdf_path)) as pdf:
        pages = [p for p in pdf.pages
                 if "Name and address of" in (p.extract_text() or "")
                 and "Purpose of grant" in (p.extract_text() or "")]
        if not pages:
            sys.exit(f"{pdf_path.name}: no Schedule I Part II pages")
        for p in pages:
            for r in parse_page(p):
                rows.append({
                    "fiscal_year": fy, "object_id": "", "row_in_filing": len(rows) + 1,
                    "recipient_name": r["name"], "recipient_name_2": "",
                    "recipient_ein": r["ein"], "street": r["street"], "city": r["city"],
                    "state": r["state"], "zip": r["zip"], "country": "",
                    "irc_section": r["irc"], "cash_amt": r["cash"],
                    "noncash_amt": r["noncash"], "purpose": r["purpose"],
                    "source": f"PDF: {pdf_path.name}",
                })
        counts = filer_counts(pdf)

    print(f"{len(pages)} Schedule I pages, {len(rows)} rows, "
          f"${sum(r['cash_amt'] for r in rows):,} cash")

    blank = [r for r in rows if not r["recipient_name"]]
    if blank:
        sys.exit(f"{len(blank)} rows parsed with no recipient name, first EIN "
                 f"{blank[0]['recipient_ein']}")
    dups = [k for k, n in __import__("collections").Counter(
        (r["recipient_ein"], r["cash_amt"]) for r in rows).items() if n > 1]
    if dups:
        print(f"note: {len(dups)} (EIN, amount) pairs appear twice; "
              f"a recipient can take two grants in a year, so this is not fatal: {dups[:3]}")
    if counts:
        want = sum(counts)
        print(f"filer's own count on Part I: {counts[0]} + {counts[1]} = {want}")
        if len(rows) != want:
            sys.exit(f"parsed {len(rows)} rows against the filer's {want}; "
                     f"do not use this file until that is explained")
    else:
        print("could not read the filer's own count; the row count is unchecked")

    with out.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    print(f"wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main(sys.argv[1:])
