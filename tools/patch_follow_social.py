# -*- coding: utf-8 -*-
"""Topbar + sidebar: Instagram, Twitter, YouTube (theme-matched)."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TOPBAR_SOCIAL = re.compile(
    r'<div class="custom"\s*>\s*<ul class="social-list">[\s\S]*?</ul>\s*</div>',
    re.DOTALL,
)

TOPBAR_REPLACE = """<div class="custom">
	<ul class="social-list">
  <li><a href="#" title="Instagram" class="btn instagram" rel="noopener noreferrer" target="_blank"><span class="fa fa-instagram" aria-hidden="true"></span><span class="empty">empty</span></a></li>
  <li><a href="#" title="Twitter" class="btn twitter" rel="noopener noreferrer" target="_blank"><span class="fa fa-twitter" aria-hidden="true"></span><span class="empty">empty</span></a></li>
  <li><a href="#" title="YouTube" class="btn youtube" rel="noopener noreferrer" target="_blank"><span class="fa fa-youtube-play" aria-hidden="true"></span><span class="empty">empty</span></a></li>
</ul></div>"""

FOLLOW_SIDEBAR = """<div class="custom">
<ul class="follow-us-social">
  <li><a href="#" title="Instagram" class="btn instagram" rel="noopener noreferrer" target="_blank"><span class="fa fa-instagram" aria-hidden="true"></span><span class="follow-us-social__label">Instagram</span><span class="empty">empty</span></a></li>
  <li><a href="#" title="Twitter" class="btn twitter" rel="noopener noreferrer" target="_blank"><span class="fa fa-twitter" aria-hidden="true"></span><span class="follow-us-social__label">Twitter</span><span class="empty">empty</span></a></li>
  <li><a href="#" title="YouTube" class="btn youtube" rel="noopener noreferrer" target="_blank"><span class="fa fa-youtube-play" aria-hidden="true"></span><span class="follow-us-social__label">YouTube</span><span class="empty">empty</span></a></li>
</ul>
</div>"""

INDEX_MOD111 = re.compile(
    r'(<div class="t3-module module " id="Mod111"><div class="module-inner"><h3 class="module-title "><span>Follow Us on Social</span></h3><div class="module-ct ">\s*)<div class="custom"></div>',
    re.DOTALL,
)

ADDTHIS_FOLLOW = re.compile(
    r'<div class="custom">\s*<div class="ja-addthis">\s*<div class="addthis_inline_follow_toolbox"></div>\s*</div></div>',
    re.DOTALL,
)

MOD143_EMPTY = re.compile(
    r'(<div class="t3-module module " id="Mod143"><div class="module-inner"><h3 class="module-title "><span>Follow Us</span></h3><div class="module-ct ">\s*)<div class="custom"></div>',
    re.DOTALL,
)


def main() -> None:
    for p in sorted(ROOT.glob("*.html")):
        t = p.read_text(encoding="utf-8", errors="replace")
        o = t
        t = TOPBAR_SOCIAL.sub(TOPBAR_REPLACE, t)
        t = INDEX_MOD111.sub(r"\1" + FOLLOW_SIDEBAR, t)
        t = ADDTHIS_FOLLOW.sub(FOLLOW_SIDEBAR, t)
        t = MOD143_EMPTY.sub(r"\1" + FOLLOW_SIDEBAR, t)
        if t != o:
            p.write_text(t, encoding="utf-8", newline="\n")
            print("updated", p.name)


if __name__ == "__main__":
    main()
