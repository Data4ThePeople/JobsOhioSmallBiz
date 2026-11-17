#!/usr/bin/env python3
"""Build the social GIF: the two-by-two as the "small" line moves.

The tool's whole argument is that "small business" has no single legal
meaning, so it hands the reader the line and lets them move it. A still
cannot show that. This steps the matrix through the three settings the page
offers, 100, 500 and 5,000 employees at the parent, and comes to rest on 500,
which is the page default and the figure the post and hero publish.

Every frame is a real setting with real values. Nothing is interpolated, so
no frame shows a number that is not in the data.

Frames, in order: 100, 500, 5,000, then back to 500 held five seconds, so the
loop ends on the published figures rather than on whichever setting happened
to be last.

Writes posts/<slug>/social/size-home-state-cutoffs.gif.

Usage: 49_social_gif.py [slug]
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
W, H = 1200, 675
CUTOFFS = {"100": {"<100"},
           "500": {"<100", "100-499"},
           "5000": {"<100", "100-499", "500-4999"}}
# the three steps, then a long hold on the page default
SEQUENCE = [("100", 2000), ("500", 2000), ("5000", 2000), ("500", 5000)]
LABEL = {"100": "100", "500": "500", "5000": "5,000"}


def cells(cutoff):
    d = json.loads((ROOT / "dist" / "data.json").read_text())
    small = CUTOFFS[cutoff]
    items = [p for p in d["parents_table"]
             if p["class"] == "business" and (p.get("bucket") or "") and p.get("hq")]
    tc, tn = sum(p["cash"] for p in items), len(items)
    out = {}
    for s in (True, False):
        for h in (True, False):
            g = [p for p in items
                 if ((p["bucket"] in small) == s) and ((p["hq"] == "OH") == h)]
            out[(s, h)] = (100 * sum(x["cash"] for x in g) / tc, 100 * len(g) / tn)
    return out, d["meta"]


PAGE = """<!doctype html><html><head><meta charset="utf-8"><style>
  *{{box-sizing:border-box;margin:0;padding:0}}
  html,body{{width:{W}px;height:{H}px}}
  body{{background:#fcfcfb;color:#111;
    font:16px/1.45 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;
    padding:40px 48px;display:flex;flex-direction:column}}
  h2{{font-size:31px;font-weight:660;letter-spacing:-.016em}}
  .note{{font-size:17px;color:#6b6a66;margin-top:6px}}
  .seg{{display:flex;gap:7px;margin-top:16px;align-items:center}}
  .seg .cap{{font-size:16px;color:#52514e;margin-right:5px}}
  .seg b{{font-size:17px;font-weight:600;padding:7px 15px;border-radius:7px;
    border:1px solid #dcdbd6;background:#fff;color:#6b6a66}}
  .seg b.on{{background:#1F6F6B;border-color:#1F6F6B;color:#fff}}
  .two{{display:grid;grid-template-columns:auto 1fr 1fr;gap:12px;margin-top:18px;flex:1}}
  .hd{{font-size:17px;color:#52514e;text-align:center;align-self:end;padding-bottom:4px}}
  .rh{{font-size:19px;color:#52514e;align-self:center;padding-right:13px;
    text-align:right;line-height:1.2}}
  .rh span{{display:block;font-size:14px;color:#8a8781;margin-top:3px}}
  .cell{{border:1px solid #dcdbd6;border-left-width:8px;border-radius:10px;
    padding:16px 20px;background:#fff;display:flex;flex-direction:column;justify-content:center}}
  .cell .v{{font-size:50px;font-weight:660;letter-spacing:-.026em;line-height:1;
    font-variant-numeric:tabular-nums}}
  .cell .s{{font-size:17px;color:#6b6a66;margin-top:7px}}
  .foot{{display:flex;justify-content:space-between;align-items:flex-end;margin-top:20px;
    font-size:15px;color:#6b6a66}}
  .foot b{{color:#111;font-weight:650}}
</style></head><body>
  <h2>Where JobsOhio's grant dollars went</h2>
  <p class="note">Share of the dollars in each cell, with the share of companies underneath.</p>
  <div class="seg"><span class="cap">"Small" means under</span>
    <b class="{on100}">100</b><b class="{on500}">500</b><b class="{on5000}">5,000</b>
    <span class="cap" style="margin-left:7px">employees at the parent company</span></div>
  <div class="two">
    <div></div><div class="hd">Headquartered in Ohio</div><div class="hd">Headquartered elsewhere</div>
    <div class="rh">Small<span>under {lab}</span></div>
    <div class="cell" style="border-left-color:#2a6fdb"><div class="v">{so_c}</div><div class="s">{so_n} of companies</div></div>
    <div class="cell" style="border-left-color:#2a6fdb"><div class="v">{sx_c}</div><div class="s">{sx_n} of companies</div></div>
    <div class="rh">Large<span>{lab} or more</span></div>
    <div class="cell" style="border-left-color:#d4661e"><div class="v">{lo_c}</div><div class="s">{lo_n} of companies</div></div>
    <div class="cell" style="border-left-color:#d4661e"><div class="v">{lx_c}</div><div class="s">{lx_n} of companies</div></div>
  </div>
  <div class="foot">
    <div>JobsOhio Form 990, Schedule I, FY{fy0} to FY{fy1}. Business recipients only.</div>
    <div><b>Data 4 The People</b></div>
  </div>
</body></html>"""


def pct(x):
    """One decimal below 10, none above, so a cell never reads '0%'."""
    return f"{x:.1f}%" if x < 9.95 else f"{x:.0f}%"


def frame(cutoff, out_dir):
    c, m = cells(cutoff)
    html = PAGE.format(
        W=W, H=H, lab=LABEL[cutoff], fy0=m["fy_min"], fy1=m["fy_max"],
        on100="on" if cutoff == "100" else "",
        on500="on" if cutoff == "500" else "",
        on5000="on" if cutoff == "5000" else "",
        so_c=pct(c[(True, True)][0]), so_n=pct(c[(True, True)][1]),
        sx_c=pct(c[(True, False)][0]), sx_n=pct(c[(True, False)][1]),
        lo_c=pct(c[(False, True)][0]), lo_n=pct(c[(False, True)][1]),
        lx_c=pct(c[(False, False)][0]), lx_n=pct(c[(False, False)][1]))
    src = out_dir / f"frame-{cutoff}.html"
    png = out_dir / f"frame-{cutoff}.png"
    src.write_text(html)
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
                    f"--screenshot={png}", f"--window-size={W},{H}",
                    "--default-background-color=FFFFFFFF", src.as_uri()],
                   check=True, capture_output=True)
    return png


def main(argv):
    from PIL import Image
    slug = argv[0] if argv and not argv[0].startswith("-") else "jobsohio-grants"
    out_dir = ROOT / "posts" / slug / "social"
    out_dir.mkdir(parents=True, exist_ok=True)

    shot = {c: frame(c, out_dir) for c in CUTOFFS}
    frames = [Image.open(shot[c]).convert("P", palette=Image.ADAPTIVE, colors=64)
              for c, _ in SEQUENCE]
    gif = out_dir / "size-home-state-cutoffs.gif"
    frames[0].save(gif, save_all=True, append_images=frames[1:],
                   duration=[ms for _, ms in SEQUENCE], loop=0, optimize=True,
                   disposal=2)
    for p in out_dir.glob("frame-*.html"):
        p.unlink()
    kb = gif.stat().st_size / 1024
    print(f"wrote {gif.relative_to(ROOT)}  {W}x{H}  {len(SEQUENCE)} frames  "
          f"{sum(ms for _, ms in SEQUENCE)/1000:.0f}s  {kb:.0f} KB")
    if kb > 5000:
        print("  WARNING: over 5 MB, LinkedIn will not animate it")


if __name__ == "__main__":
    main(sys.argv[1:])
