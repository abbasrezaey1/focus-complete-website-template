# -*- coding: utf-8 -*-
"""Revert #t3-header to logo column first; megamenu h4/h5 subcategory links -> single-subcategory.html."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LOGO_COL_MARKER = '<div class="col-xs-12 col-sm-6 col-lg-4 logo">'
SPOT_COL_MARKER = '<div class="col-xs-12 col-sm-6 col-lg-8">'


def _consume_outer_div(s: str, start: int) -> tuple[str, int] | None:
    if start < 0 or start >= len(s) or not s.startswith("<div", start):
        return None
    depth = 0
    i = start
    while i < len(s):
        if s.startswith("<div", i) and (i + 4 >= len(s) or s[i + 4] in " \t\n\r>/"):
            depth += 1
            i += 4
            continue
        if s.startswith("</div>", i):
            depth -= 1
            i += 6
            if depth == 0:
                return s[start:i], i
            continue
        i += 1
    return None


def revert_header_logo_first(content: str) -> str:
    """If spotlight column appears before logo, swap back to logo first (original JA layout)."""
    key = '<header id="t3-header" class="container t3-header">'
    pos = 0
    out: list[str] = []
    while True:
        h = content.find(key, pos)
        if h == -1:
            out.append(content[pos:])
            break
        out.append(content[pos:h])
        row = content.find('<div class="row">', h)
        hend = content.find("</header>", h)
        if row == -1 or hend == -1:
            out.append(content[h:])
            break
        logo_i = content.find(LOGO_COL_MARKER, row, hend)
        spot_i = content.find(SPOT_COL_MARKER, row, hend)
        if logo_i == -1 or spot_i == -1:
            out.append(content[h : hend + len("</header>")])
            pos = hend + len("</header>")
            continue
        if spot_i > logo_i:
            out.append(content[h : hend + len("</header>")])
            pos = hend + len("</header>")
            continue
        logo_block = _consume_outer_div(content, logo_i)
        spot_block = _consume_outer_div(content, spot_i)
        if not logo_block or not spot_block:
            out.append(content[h : hend + len("</header>")])
            pos = hend + len("</header>")
            continue
        logo_s, logo_end = logo_block
        spot_s, _spot_end = spot_block
        before = content[h : row + len('<div class="row">')]
        # Original order was spotlight then logo; keep markup after the logo column only.
        tail = content[logo_end : hend + len("</header>")]
        rebuilt = before + "\n\n" + logo_s + "\n\n" + spot_s + tail
        out.append(rebuilt)
        pos = hend + len("</header>")
    return "".join(out)


# Megamenu subcategory rows: left column h4 (single-article only); nested h5; h4+gallery = section hub
def subcategory_hrefs(html: str) -> str:
    html = re.sub(
        r'(<h4[^>]*>\s*<a\s+href="\./)single-article\.html(")',
        r"\1single-subcategory.html\2",
        html,
        flags=re.IGNORECASE | re.DOTALL,
    )
    html = re.sub(
        r'(<h4[^>]*>\s*<a\s+href="\./)gallery\.html(")',
        r"\1single-category.html\2",
        html,
        flags=re.IGNORECASE | re.DOTALL,
    )
    html = re.sub(
        r'(<h5[^>]*>\s*<a\s+href="\./)(?:single-article|gallery)\.html(")',
        r"\1single-subcategory.html\2",
        html,
        flags=re.IGNORECASE | re.DOTALL,
    )
    return html


def main() -> None:
    for p in sorted(ROOT.glob("*.html")):
        raw = p.read_text(encoding="utf-8", errors="replace")
        orig = raw
        raw = revert_header_logo_first(raw)
        raw = subcategory_hrefs(raw)
        if raw != orig:
            p.write_text(raw, encoding="utf-8", newline="\n")
            print("updated", p.name)


if __name__ == "__main__":
    main()
