#!/usr/bin/env python3
"""Download BTS T-100 Domestic Segment (U.S. carriers) for Ohio, one file per
year, into data/raw/t100/. T-100 is the carriers' own monthly report to the
Department of Transportation of every nonstop segment flown: departures
scheduled and performed, seats and passengers, by carrier, origin,
destination and month.

Used to check what the JobsOhio Air Service Restoration grants paid for:
whether the routes started, how long they flew, and whether they kept flying
after the revenue guarantee ended.

The BTS download page is an ASP.NET form; this script posts it the way a
browser does (geography Ohio, all months, selected fields). The Ohio filter
keeps segments with an Ohio origin or destination."""
import io, re, sys, time, urllib.parse, urllib.request, http.cookiejar, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "raw" / "t100"
URL = "https://www.transtats.bts.gov/DL_SelectFields.aspx?gnoyr_VQ=FIM&QO_fu146_anzr=Nv4%20Pn44vr45"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/128.0 Safari/537.36"
FIELDS = ["DEPARTURES_SCHEDULED", "DEPARTURES_PERFORMED", "SEATS", "PASSENGERS", "UNIQUE_CARRIER",
          "UNIQUE_CARRIER_NAME", "ORIGIN", "ORIGIN_CITY_NAME", "ORIGIN_STATE_ABR", "DEST", "DEST_CITY_NAME",
          "DEST_STATE_ABR", "YEAR", "MONTH"]


def opener():
    cj = http.cookiejar.CookieJar()
    o = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    o.addheaders = [("User-Agent", UA)]
    return o


def hidden(html):
    return {n: v for n, v in re.findall(r'<input[^>]+type="hidden"[^>]+name="([^"]+)"[^>]+value="([^"]*)"', html)}


def fetch_year(year):
    o = opener()
    html = o.open(URL, timeout=90).read().decode("utf-8", "replace")
    form = hidden(html)
    form.update({"cboGeography": "Ohio", "cboYear": str(year), "cboPeriod": "All", "chkDownloadZip": "on",
                 "btnDownload": "Download"})
    for f in FIELDS:
        form[f] = "on"
    data = urllib.parse.urlencode(form).encode()
    resp = o.open(urllib.request.Request(URL, data=data, headers={"Referer": URL}), timeout=300)
    body = resp.read()
    if body[:2] != b"PK":
        raise RuntimeError(f"{year}: not a zip ({body[:120]!r})")
    with zipfile.ZipFile(io.BytesIO(body)) as z:
        # the zip also carries a small field-description CSV; take the data file
        name = max((n for n in z.namelist() if n.lower().endswith(".csv")), key=lambda n: z.getinfo(n).file_size)
        csv = z.read(name)
    out = OUT / f"t100d_segment_ohio_{year}.csv"
    out.write_bytes(csv)
    return out, csv.count(b"\n") - 1


def main(years):
    OUT.mkdir(parents=True, exist_ok=True)
    for y in years:
        out = OUT / f"t100d_segment_ohio_{y}.csv"
        if out.exists() and out.stat().st_size > 1000:
            print(f"{y}: on disk"); continue
        try:
            p, n = fetch_year(y)
            print(f"{y}: {n:,} rows -> {p.name}")
        except Exception as e:
            print(f"{y}: FAILED {e}")
        time.sleep(3)


if __name__ == "__main__":
    main([int(a) for a in sys.argv[1:]] or list(range(2019, 2027)))
