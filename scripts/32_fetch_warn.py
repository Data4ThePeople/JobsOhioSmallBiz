#!/usr/bin/env python3
"""Download Ohio's own WARN notices, so a layoff claim can be checked against the state.

18 of the 31 confirmed failures are a closure or a mass layoff, and the state has
an official record of both: the WARN notice an employer must file before closing
a plant or cutting 50 or more jobs. Up to now those notices were fetched by hand
one company at a time, which means nothing re-checks them. This pulls every year
into data/warn/ so 31_audit_failures.py can tie each Ohio claim to the state's
own filing.

Two traps, both found the hard way:

  * jfs.ohio.gov returns 404 to a descriptive User-Agent and 200 to a browser
    one. The fetch below sends a browser string for that reason, and only to
    this host.
  * the WARN pages moved. They were under
    /job-services-and-unemployment/job-seekers/..., and are now under
    /job-workforce-services/job-programs-and-services/submit-a-warn-notice/...
    Every old URL is a 404, so the year pages are discovered from the site's
    own sitemap rather than hardcoded, and the script says so when the shape
    changes again.

There is no table in the HTML to scrape. The year pages are a Next.js app that
renders a CSV published on Ohio's asset host, and the CSV's address sits in the
page's own data payload as `csvUrl`. That CSV is the state's machine-readable
record, so it is what gets pulled, and the notices come back as fields rather
than as scraped cells.

Writes data/warn/notices.csv (one row per notice, every year), saves each year's
page under data/warn/pages/ and each year's CSV under data/warn/csv/ so the
parse can be re-checked.

Usage: 32_fetch_warn.py [--no-cache]
"""
import csv, html, re, subprocess, sys
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "warn"
PAGES = OUT / "pages"
CSVS = OUT / "csv"
SITEMAP = "https://jfs.ohio.gov/sitemap.xml"
# this host serves 404 to anything that announces itself as a research script
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")
YEAR_PAGE = re.compile(r"(\d{4}|current)-public-notices-of-layoffs-and-closures")


def get(url, timeout=60):
    p = subprocess.run(["curl", "-sL", "--max-time", str(timeout), "-A", UA, url],
                       capture_output=True, text=True, errors="ignore")
    return p.stdout or ""


def strip_tags(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def clean_url(u):
    """Ohio's CSV holds paths with raw spaces in them, as in
    "WARN 2023/Republic Steel.pdf". Left alone those fail to fetch at all, so
    the path is percent-encoded while the rest of the URL is left untouched."""
    u = (u or "").strip()
    if not u:
        return ""
    return quote(u, safe=":/?#[]@!$&'()*+,;=%~")


def year_pages():
    sm = get(SITEMAP)
    if "<loc>" not in sm:
        sys.exit("the sitemap did not come back as XML; check the host by hand")
    urls = sorted({u for u in re.findall(r"<loc>([^<]+)</loc>", sm) if YEAR_PAGE.search(u)})
    if not urls:
        sys.exit("no year pages in the sitemap: the WARN section has moved again, "
                 "so find its new path before trusting anything here")
    return urls


def csv_url(page_html):
    """The year's CSV, out of the page's own Next.js payload. The payload is
    JSON embedded in a script as escaped text, so the address is matched
    directly rather than by walking a parsed tree."""
    m = re.search(r'csvUrl\\?"\s*:\s*\\?"(https?://[^"\\\s]+\.csv)', page_html)
    return m.group(1) if m else ""


# Ohio's column names and their order drift between years, so each field is
# matched by what its header says rather than by position. The one that must be
# matched before anything else is the PDF link, because two columns are headed
# "Company" (one holds the text, one the hyperlink) and the employer field would
# otherwise swallow the wrong one.
FIELD = {
    "pdf": ("url", "link"),
    "employer": ("company", "employer", "business"),
    "received": ("received",),
    "place": ("city", "county", "location"),
    "affected": ("affected", "employees", "workers", "impacted"),
    "when": ("layoff date", "closure date", "effective"),
    "kind": ("layoff/closure", "type", "reason"),
    "notice_id": ("notice id",),
}
# the real header sits below a row of column-type codes and a blank row
HEADER_HINT = "company"


def pick(header):
    """our field name -> column index. A column is claimed once, so the second
    "Company" column cannot be read as the employer when the first already was."""
    out, taken = {}, set()
    for field, words in FIELD.items():
        for i, h in enumerate(header):
            low = (h or "").strip().lower()
            if i in taken or not low:
                continue
            if any(w in low for w in words):
                out[field], _ = i, taken.add(i)
                break
    return out


def header_row(rows):
    """Index of the real header. Ohio's export puts a row of column-type codes
    and a blank row above it, so the first row is not it."""
    for i, r in enumerate(rows[:8]):
        if any(HEADER_HINT in (c or "").lower() for c in r):
            return i
    return 0


def main(argv):
    PAGES.mkdir(parents=True, exist_ok=True)
    CSVS.mkdir(parents=True, exist_ok=True)
    urls = year_pages()
    print(f"{len(urls)} year pages in the sitemap")

    out, no_csv = [], []
    for u in urls:
        label = YEAR_PAGE.search(u).group(1)
        page = PAGES / f"{label}.html"
        if page.exists() and "--no-cache" not in argv:
            h = page.read_text(errors="ignore")
        else:
            h = get(u)
            page.write_text(h)
        cu = csv_url(h)
        if not cu:
            no_csv.append(label)
            print(f"  {label:8s} no csvUrl in the page payload")
            continue
        f = CSVS / f"{label}.csv"
        if not f.exists() or "--no-cache" in argv:
            f.write_text(get(cu))
        rows = list(csv.reader(f.open(errors="ignore")))
        rows = [r for r in rows if any((c or "").strip() for c in r)]
        if not rows:
            no_csv.append(label)
            print(f"  {label:8s} csv came back empty ({cu[:60]})")
            continue
        hr = header_row(rows)
        ix = pick(rows[hr])
        if "employer" not in ix:
            no_csv.append(label)
            print(f"  {label:8s} no employer column in {rows[hr][:6]}")
            continue
        n = 0
        for r in rows[hr + 1:]:
            def cell(k):
                i = ix.get(k)
                return (r[i].strip() if i is not None and i < len(r) else "")
            if not cell("employer"):
                continue
            n += 1
            out.append({"year": label, "employer": cell("employer"), "place": cell("place"),
                        "affected": cell("affected"), "received": cell("received"),
                        "when": cell("when"), "kind": cell("kind"),
                        "notice_id": cell("notice_id"), "pdf": clean_url(cell("pdf")),
                        "row": " | ".join(c.strip() for c in r), "csv_url": cu, "source": u})
        print(f"  {label:8s} {n:4d} notices   fields: " + ", ".join(sorted(ix)))

    if not out:
        sys.exit("no notices parsed from any year; the page layout has changed")
    f = OUT / "notices.csv"
    with f.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["year", "employer", "place", "affected", "received",
                                           "when", "kind", "notice_id", "pdf", "row",
                                           "csv_url", "source"])
        w.writeheader(); w.writerows(out)
    print(f"\nwrote {f.relative_to(ROOT)}: {len(out)} notices across "
          f"{len({r['year'] for r in out})} years")
    if no_csv:
        print(f"no CSV for: {', '.join(no_csv)}")


if __name__ == "__main__":
    main(sys.argv[1:])
