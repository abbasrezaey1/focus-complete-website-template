# -*- coding: utf-8 -*-
"""Remove duplicate .logo column inside #t3-header (bad revert tail)."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOGO = '<div class="col-xs-12 col-sm-6 col-lg-4 logo">'


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


def strip_second_logo(html: str) -> str:
    key = '<header id="t3-header" class="container t3-header">'
    h = html.find(key)
    if h == -1:
        return html
    hend = html.find("</header>", h)
    if hend == -1:
        return html
    inner = html[h:hend]
    p1 = inner.find(LOGO)
    if p1 == -1:
        return html
    p2 = inner.find(LOGO, p1 + 1)
    if p2 == -1:
        return html
    abs2 = h + p2
    blk = _consume_outer_div(html, abs2)
    if not blk:
        return html
    _, end_i = blk
    cut = abs2
    while cut > h and html[cut - 1] in "\n\r\t ":
        cut -= 1
    return html[:cut] + html[end_i:]


def main() -> None:
    for p in sorted(ROOT.glob("*.html")):
        raw = p.read_text(encoding="utf-8", errors="replace")
        n2 = raw.count(LOGO)
        if n2 < 2:
            continue
        # only fix when two logos live in same header
        h = raw.find('<header id="t3-header"')
        if h == -1:
            continue
        he = raw.find("</header>", h)
        if raw[h:he].count(LOGO) < 2:
            continue
        new = strip_second_logo(raw)
        if new != raw:
            p.write_text(new, encoding="utf-8", newline="\n")
            print("fixed", p.name)


if __name__ == "__main__":
    main()
