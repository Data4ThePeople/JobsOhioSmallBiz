#!/usr/bin/env python3
"""Build dist/index.html (full page) and dist/embed.html (Prismic frame variant,
780px, light theme pinned) from scripts/template.html and dist/data.json.
One template; the two files differ only in the __FORCE_FRAMED__ flag, so they
cannot drift. Run 09_analyze.py first."""
import base64, json, re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "scripts" / "template.html"
DATA = ROOT / "dist" / "data.json"
DIST = ROOT / "dist"
CHANGELOG = ROOT / "CHANGELOG.md"
LOGOS = {"__LOGO_ON_LIGHT__": "d4tp-text-dark.svg", "__LOGO_ON_DARK__": "d4tp-text-light.svg"}


def version():
    """The newest entry in CHANGELOG.md, as (number, date).

    Read from the changelog rather than kept in a constant here, so the tool
    cannot show a version number that nothing explains. Bumping the version
    means writing the entry first.
    """
    m = re.search(r"^## +(\d+\.\d+) +[-–—] +(\d{4}-\d{2}-\d{2}) *$",
                  CHANGELOG.read_text(), re.M)
    if not m:
        raise SystemExit("CHANGELOG.md has no '## <major>.<minor> - YYYY-MM-DD' "
                         "heading; add the entry for this version first")
    d = date.fromisoformat(m.group(2))
    return m.group(1), d.strftime("%B %-d, %Y")


def main():
    data = json.loads(DATA.read_text())
    tpl = TEMPLATE.read_text()
    assert "__DATA__" in tpl and "__FORCE_FRAMED__" in tpl
    ver, ver_date = version()
    tpl = tpl.replace("__VERSION__", ver).replace("__VERSION_DATE__", ver_date)
    for k, name in LOGOS.items():
        raw = (ROOT / "assets" / name).read_bytes()
        tpl = tpl.replace(k, "data:image/svg+xml;base64," + base64.b64encode(raw).decode())
    payload = json.dumps(data, separators=(",", ":"))
    for fname, framed in (("index.html", "false"), ("embed.html", "true")):
        html = tpl.replace("__DATA__", payload).replace("__FORCE_FRAMED__", framed)
        (DIST / fname).write_text(html)
        print(f"wrote dist/{fname}  {len(html)/1024:.0f} KB  v{ver}")


if __name__ == "__main__":
    main()
