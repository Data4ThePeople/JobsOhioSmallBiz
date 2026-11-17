#!/usr/bin/env python3
"""Build the 1680x1080 hero: a simplified view of the tool's own cards.

It carries the two headline tiles and the size-by-home-state grid, and
nothing else. Two things drove that. Type has to be readable when the image
is a thumbnail, which means fewer elements and much larger type than the page
uses. And the hero cannot use a word the post has not defined yet: the outcome
figures were on it until the word "failed" turned out to be meaningless to
someone meeting the project at the hero. (Eric Pachman, November 17, 2026.)

Not a screenshot of the page. A screenshot at hero size is unreadable, and
cropping one to 1680x1080 cuts the cards in half. This lays out a selection
of the cards at hero scale, so every figure on it is legible at the size the
image is actually used.

Every number is read from dist/data.json at the page's default settings
(businesses only, "small" means under 500), so the hero cannot drift from the
tool. Run build.py first.

Writes posts/<slug>/images/<slug>-hero-source.html, screenshots it with
headless Chrome, and saves <slug>-hero-1680x1080.png beside it.

Usage: 48_hero.py [slug]
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
SMALL_BUCKETS = {"<100", "100-499"}
W, H = 1680, 1080


def figures():
    d = json.loads((ROOT / "dist" / "data.json").read_text())
    biz = [p for p in d["parents_table"] if p["class"] == "business"]

    def size(p):
        b = p.get("bucket") or ""
        return "small" if b in SMALL_BUCKETS else ("large" if b else "unknown")

    def home(p):
        return "ohio" if p.get("hq") == "OH" else ("other" if p.get("hq") else "unknown")

    items = [p for p in biz if size(p) != "unknown" and home(p) != "unknown"]
    tc, tn = sum(p["cash"] for p in items), len(items)
    cell = {}
    for s in ("small", "large"):
        for h in ("ohio", "other"):
            g = [p for p in items if size(p) == s and home(p) == h]
            cell[(s, h)] = (100 * sum(p["cash"] for p in g) / tc, 100 * len(g) / tn)
    return {
        "meta": d["meta"], "cell": cell,
        "small_n": 100 * sum(1 for p in biz if size(p) == "small") / len(biz),
        "large_cash": 100 * sum(p["cash"] for p in biz if size(p) == "large")
                      / sum(p["cash"] for p in biz),
    }


PAGE = """<!doctype html><html><head><meta charset="utf-8"><style>
  @import url('');
  *{{box-sizing:border-box;margin:0;padding:0}}
  html,body{{width:{W}px;height:{H}px}}
  body{{background:#fcfcfb;color:#111;
    font:16px/1.45 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;
    padding:58px 72px;display:flex;flex-direction:column}}
  h1{{font-size:68px;line-height:1.06;letter-spacing:-.026em;font-weight:680}}
  .sub{{font-size:29px;color:#52514e;margin-top:18px;max-width:46ch;line-height:1.35}}
  .cards{{display:grid;grid-template-columns:1fr 1.5fr;gap:28px;margin-top:46px;
    flex:1;align-content:stretch}}
  .col{{display:flex;flex-direction:column;gap:28px}}
  .card{{border:1px solid #dcdbd6;border-radius:16px;padding:34px 38px;background:#fff;
    display:flex;flex-direction:column;justify-content:center;flex:1}}
  .lab{{font-size:25px;color:#52514e;line-height:1.3}}
  .val{{font-size:142px;font-weight:680;letter-spacing:-.03em;line-height:1;margin-top:10px;
    font-variant-numeric:tabular-nums}}
  .hint{{font-size:22px;color:#6b6a66;margin-top:14px;line-height:1.35}}
  h2{{font-size:32px;font-weight:650;letter-spacing:-.012em}}
  .note{{font-size:21px;color:#6b6a66;margin-top:7px;line-height:1.35}}
  .two{{display:grid;grid-template-columns:auto 1fr 1fr;gap:16px;margin-top:26px}}
  .hd{{font-size:22px;color:#52514e;text-align:center;align-self:end;padding-bottom:4px}}
  .rh{{font-size:22px;color:#52514e;align-self:center;padding-right:12px}}
  .cell{{border:1px solid #dcdbd6;border-left-width:10px;border-radius:12px;padding:22px 24px}}
  .cell .v{{font-size:62px;font-weight:660;letter-spacing:-.025em;line-height:1.05;
    font-variant-numeric:tabular-nums}}
  .cell .s{{font-size:22px;color:#6b6a66;margin-top:6px}}
  .foot{{display:flex;justify-content:space-between;align-items:flex-end;margin-top:40px;
    font-size:21px;color:#6b6a66}}
  .foot b{{color:#111;font-weight:650}}
</style></head><body>
  <h1>Where JobsOhio's grant money went</h1>
  <p class="sub">{rows} grants, {cash}, {parents} companies and organizations,
     fiscal years {fy0} to {fy1}.</p>
  <div class="cards">
    <div class="col">
      <div class="card">
        <div class="lab">Share of the businesses JobsOhio paid that are small</div>
        <div class="val">{small_n:.0f}%</div>
        <div class="hint">Under 500 employees at the parent company</div>
      </div>
      <div class="card">
        <div class="lab">Share of the dollars that went to large businesses</div>
        <div class="val">{large_cash:.0f}%</div>
        <div class="hint">Most of the companies are small. Most of the money is not.</div>
      </div>
    </div>
    <div class="col">
      <div class="card">
        <h2>Size and home state together</h2>
        <p class="note">Share of dollars in each cell, with the share of companies underneath</p>
        <div class="two">
          <div></div><div class="hd">Headquartered in Ohio</div><div class="hd">Headquartered elsewhere</div>
          <div class="rh">Small</div>
          <div class="cell" style="border-left-color:#2a6fdb"><div class="v">{so_c:.0f}%</div><div class="s">{so_n:.0f}% of companies</div></div>
          <div class="cell" style="border-left-color:#2a6fdb"><div class="v">{sx_c:.1f}%</div><div class="s">{sx_n:.1f}% of companies</div></div>
          <div class="rh">Large</div>
          <div class="cell" style="border-left-color:#d4661e"><div class="v">{lo_c:.0f}%</div><div class="s">{lo_n:.1f}% of companies</div></div>
          <div class="cell" style="border-left-color:#d4661e"><div class="v">{lx_c:.0f}%</div><div class="s">{lx_n:.0f}% of companies</div></div>
        </div>
      </div>
    </div>
  </div>
  <div class="foot">
    <div>Source: JobsOhio Form 990, Schedule I, fiscal years {fy0} to {fy1}. Free to use.</div>
    <div><b>Data 4 The People</b></div>
  </div>
</body></html>"""


def money(v):
    return f"${v/1e9:.2f} billion" if v >= 1e9 else f"${v/1e6:.0f} million"


def main(argv):
    slug = argv[0] if argv and not argv[0].startswith("-") else "jobsohio-grants"
    f = figures()
    m, c = f["meta"], f["cell"]
    html = PAGE.format(
        W=W, H=H, rows=f"{m['rows']:,}", cash=money(m["cash_total"]),
        parents=f"{m['parents']:,}", fy0=m["fy_min"], fy1=m["fy_max"],
        small_n=f["small_n"], large_cash=f["large_cash"],
        so_c=c[("small", "ohio")][0], so_n=c[("small", "ohio")][1],
        sx_c=c[("small", "other")][0], sx_n=c[("small", "other")][1],
        lo_c=c[("large", "ohio")][0], lo_n=c[("large", "ohio")][1],
        lx_c=c[("large", "other")][0], lx_n=c[("large", "other")][1])

    out = ROOT / "posts" / slug / "images"
    out.mkdir(parents=True, exist_ok=True)
    src = out / f"{slug}-hero-source.html"
    png = out / f"{slug}-hero-1680x1080.png"
    src.write_text(html)
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
                    f"--screenshot={png}", f"--window-size={W},{H}",
                    "--default-background-color=FFFFFFFF", src.as_uri()],
                   check=True, capture_output=True)
    from PIL import Image
    im = Image.open(png)
    if im.size != (W, H):
        raise SystemExit(f"hero is {im.size}, expected ({W}, {H})")
    print(f"wrote {png.relative_to(ROOT)}  {im.size[0]}x{im.size[1]}  "
          f"{png.stat().st_size/1024:.0f} KB")


if __name__ == "__main__":
    main(sys.argv[1:])
