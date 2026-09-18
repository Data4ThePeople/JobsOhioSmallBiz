#!/usr/bin/env python3
"""Build dist/index.html (full page) and dist/embed.html (Prismic frame variant,
780px, light theme pinned) from scripts/template.html and dist/data.json.
One template; the two files differ only in the __FORCE_FRAMED__ flag, so they
cannot drift. Run 09_analyze.py first."""
import base64, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "scripts" / "template.html"
DATA = ROOT / "dist" / "data.json"
DIST = ROOT / "dist"
LOGOS = {"__LOGO_ON_LIGHT__": "d4tp-text-dark.svg", "__LOGO_ON_DARK__": "d4tp-text-light.svg"}


def main():
    data = json.loads(DATA.read_text())
    tpl = TEMPLATE.read_text()
    assert "__DATA__" in tpl and "__FORCE_FRAMED__" in tpl
    for k, name in LOGOS.items():
        raw = (ROOT / "assets" / name).read_bytes()
        tpl = tpl.replace(k, "data:image/svg+xml;base64," + base64.b64encode(raw).decode())
    payload = json.dumps(data, separators=(",", ":"))
    for fname, framed in (("index.html", "false"), ("embed.html", "true")):
        html = tpl.replace("__DATA__", payload).replace("__FORCE_FRAMED__", framed)
        (DIST / fname).write_text(html)
        print(f"wrote dist/{fname}  {len(html)/1024:.0f} KB")


if __name__ == "__main__":
    main()
