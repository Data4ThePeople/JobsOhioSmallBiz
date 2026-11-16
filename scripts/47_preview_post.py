#!/usr/bin/env python3
"""Render posts/<slug>/POST.md to a shareable HTML page under preview/.

This is for handing a draft to a reporter before it is published. It is not
the publishing path: Prismic is, at step 2f. The point here is that the draft
reads the way it will read on the site, with the embed in place, so a reporter
is reacting to the real thing rather than to a markdown file.

It understands the slice notation in ~/.claude/d4tp-process/SLICES.md as far
as this post uses it: headings, paragraphs, bullets, bold, links, a raw
iframe, and the blurb, blurb-full, spacer, dropcap and divider fences.
Anything it does not recognise is passed through as a paragraph rather than
dropped, so a new fence shows up as visible odd text instead of vanishing.

An embargo banner goes at the top unless --no-embargo is passed, because the
only reason to run this is to send someone a link before publication.

Usage: 47_preview_post.py [slug] [--no-embargo]
"""
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "preview" / "index.html"


def front_matter(text):
    if not text.startswith("---"):
        return {}, text
    _, fm, body = text.split("---", 2)
    meta = {}
    for line in fm.strip().splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta, body.lstrip("\n")


def inline(s):
    """Escape, then put back the three inline forms the posts use."""
    s = html.escape(s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)",
               lambda m: '<a href="%s" target="_blank" rel="noopener">%s</a>'
                         % (m.group(2), m.group(1)), s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    return s


def render(body):
    out, i = [], 0
    lines = body.split("\n")
    dropcap_next = False
    bullets = []

    def flush_bullets():
        if bullets:
            out.append("<ul>" + "".join("<li>%s</li>" % inline(b) for b in bullets)
                       + "</ul>")
            bullets.clear()

    while i < len(lines):
        line = lines[i].rstrip()
        if not line.strip():
            flush_bullets()
            i += 1
            continue

        if line.startswith(":::"):
            flush_bullets()
            tag = line[3:].strip()
            if tag.startswith("spacer"):
                h = (tag.split() + ["20px"])[1]
                out.append('<div style="height:%s"></div>' % h)
            elif tag == "dropcap":
                dropcap_next = True
            elif tag == "divider":
                out.append('<p class="divider">· · ·</p>')
            elif tag.startswith("blurb"):
                full = tag.startswith("blurb-full")
                title = tag.split(None, 1)[1] if " " in tag else ""
                inner, i = [], i + 1
                while i < len(lines) and lines[i].strip() != ":::":
                    inner.append(lines[i])
                    i += 1
                out.append('<aside class="blurb%s">' % (" full" if full else ""))
                if title:
                    out.append("<h4>%s</h4>" % inline(title))
                out.append(render("\n".join(inner)))
                out.append("</aside>")
            i += 1
            continue

        if line.startswith("<iframe"):
            flush_bullets()
            out.append('<div class="frame">%s</div>' % line)
            i += 1
            continue

        if line.startswith("- "):
            bullets.append(line[2:])
            i += 1
            continue

        flush_bullets()
        m = re.match(r"(#{1,4})\s+(.*)", line)
        if m:
            # The H1 is the page title and comes from the front matter, so a
            # "##" is the first level in the body and becomes an h2. Offsetting
            # it to h3 left the document with no h2 at all, which is the kind
            # of thing a screen reader walks straight into.
            level = len(m.group(1))
            if level > 1:
                out.append("<h%d>%s</h%d>" % (level, inline(m.group(2)), level))
            i += 1
            continue

        cls = ' class="dropcap"' if dropcap_next else ""
        dropcap_next = False
        out.append("<p%s>%s</p>" % (cls, inline(line)))
        i += 1

    flush_bullets()
    return "\n".join(out)


PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<style>
  :root{{color-scheme:light dark;
    --page:#fcfcfb;--surface:#f4f4f1;--ink:#111;--ink2:#3d3c39;--muted:#6b6a66;
    --border:#dcdbd6;--focus:#1F6F6B;--warn:#8a3b12;--warnbg:#fdf0e6}}
  @media (prefers-color-scheme: dark){{:root{{
    --page:#181A1B;--surface:#212425;--ink:#E4E2DC;--ink2:#C8C6C0;--muted:#9A9892;
    --border:#34383A;--focus:#6FBFB7;--warn:#F0A878;--warnbg:#2A1D14}}}}
  *{{box-sizing:border-box}}
  body{{margin:0;background:var(--page);color:var(--ink);
    font:17px/1.65 Georgia,"Iowan Old Style","Times New Roman",serif;
    -webkit-text-size-adjust:100%}}
  .sans{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}}
  .embargo{{background:var(--warnbg);border-bottom:3px solid var(--warn);
    color:var(--warn);padding:16px;text-align:center;
    font:700 15px/1.45 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;
    letter-spacing:.06em;text-transform:uppercase;position:sticky;top:0;z-index:9}}
  .embargo span{{display:block;text-transform:none;letter-spacing:0;font-weight:400;
    font-size:13.5px;margin-top:5px;color:var(--ink2)}}
  main{{max-width:40rem;margin:0 auto;padding:40px 20px 90px}}
  h1{{font-size:34px;line-height:1.2;letter-spacing:-.015em;margin:0 0 10px}}
  .sub{{font-size:19px;line-height:1.5;color:var(--ink2);margin:0 0 6px}}
  .meta{{font-size:13px;color:var(--muted);margin:0 0 30px;
    font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}}
  h2{{font-size:25px;line-height:1.25;letter-spacing:-.01em;margin:36px 0 0}}
  h3{{font-size:19px;line-height:1.3;margin:28px 0 0}}
  h4{{font-size:16px;margin:0 0 8px;
    font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}}
  p{{margin:14px 0}}
  ul{{margin:14px 0;padding-left:22px}} li{{margin:7px 0}}
  a{{color:var(--focus)}}
  .dropcap::first-letter{{float:left;font-size:58px;line-height:.86;
    padding:4px 8px 0 0;font-weight:700}}
  .divider{{text-align:center;color:var(--muted);letter-spacing:.7em;margin:40px 0}}
  aside.blurb{{background:var(--surface);border:1px solid var(--border);
    border-left:4px solid var(--focus);border-radius:8px;padding:16px 18px;margin:26px 0;
    font-size:15.5px;line-height:1.55;
    font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}}
  aside.blurb p{{margin:10px 0}} aside.blurb p:first-child{{margin-top:0}}
  aside.blurb p:last-child{{margin-bottom:0}}
  aside.blurb.full{{border-left-color:var(--warn)}}
  @media (min-width: 900px){{
    aside.blurb.full{{width:calc(100% + 120px);margin-left:-60px}}
  }}
  .frame{{margin:24px 0}}
  .frame iframe{{width:100%;border:1px solid var(--border);border-radius:8px}}
  @media (min-width: 900px){{
    .frame{{width:calc(100% + 160px);margin-left:-80px}}
  }}
</style>
</head>
<body>
{embargo}
<main>
  <h1>{title}</h1>
  <p class="sub">{subtitle}</p>
  <p class="meta">{meta}</p>
  {body}
</main>
</body>
</html>
"""

EMBARGO = """<div class="embargo">Embargoed draft, not for publication
<span>Shared for review before release. Figures and wording may still change.
Please do not publish, quote or link this page.</span></div>"""


def main(argv):
    slug = next((a for a in argv if not a.startswith("-")), None)
    posts = sorted((ROOT / "posts").glob("*/POST.md"))
    src = (ROOT / "posts" / slug / "POST.md") if slug else (posts[0] if posts else None)
    if not src or not src.exists():
        raise SystemExit("no POST.md found; pass a slug")

    meta, body = front_matter(src.read_text())
    bits = [b for b in ("Data 4 The People",
                        meta.get("section", ""),
                        "planned for " + meta.get("date", "") if meta.get("date") else "")
            if b]
    page = PAGE.format(
        title=html.escape(meta.get("title", "Untitled")),
        subtitle=inline(meta.get("subtitle", "")),
        meta=html.escape(" · ".join(bits)),
        embargo="" if "--no-embargo" in argv else EMBARGO,
        body=render(body))
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(page)
    print(f"wrote {OUT.relative_to(ROOT)} from {src.relative_to(ROOT)} "
          f"({len(page)/1024:.0f} KB)")
    print("https://data4thepeople.github.io/JobsOhioSmallBiz/preview/")


if __name__ == "__main__":
    main(sys.argv[1:])
