# -*- coding: utf-8 -*-
"""One-off: category nav -> single-category.html, one top leaderboard, header order."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Off-canvas + footer strip (six section labels)
OFF_CANVAS_NAV = re.compile(
    r'<li class="item-101(?:\s+current\s+active)?"><a href="\./[^"]+" class="">Politics</a></li>'
    r'<li class="item-109(?:\s+current\s+active)?"><a href="\./[^"]+" class="">Business</a></li>'
    r'<li class="item-110(?:\s+current\s+active)?"><a href="\./[^"]+" class="">World</a></li>'
    r'<li class="item-111(?:\s+current\s+active)?"><a href="\./[^"]+" class="">Tech</a></li>'
    r'<li class="item-112(?:\s+current\s+active)?"><a href="\./[^"]+" class="">Sport</a></li>'
    r'<li class="item-113(?:\s+current\s+active)?"><a href="\./[^"]+" class="">Entertainment</a></li>'
)

def repl_off_canvas(m: re.Match) -> str:
    return (
        '<li class="item-101"><a href="./single-category.html" class="">Politics</a></li>'
        '<li class="item-109"><a href="./single-category.html" class="">Business</a></li>'
        '<li class="item-110"><a href="./single-category.html" class="">World</a></li>'
        '<li class="item-111"><a href="./single-category.html" class="">Tech</a></li>'
        '<li class="item-112"><a href="./single-category.html" class="">Sport</a></li>'
        '<li class="item-113"><a href="./single-category.html" class="">Entertainment</a></li>'
    )

# Megamenu top row (itemprop="url" or itemprop='url')
MEGA_SIMPLE = [
    (re.compile(r'<a\s+itemprop=["\']url["\']\s+href="\./index\.html">Politics\s*</a>'),
     '<a itemprop="url" href="./single-category.html">Politics </a>'),
    (re.compile(r'<a\s+itemprop=["\']url["\']\s+href="\./blog\.html">Business\s*</a>'),
     '<a itemprop="url" href="./single-category.html">Business </a>'),
    (re.compile(r'<a\s+itemprop=["\']url["\']\s+href="\./gallery\.html">World\s*</a>'),
     '<a itemprop="url" href="./single-category.html">World </a>'),
    (re.compile(
        r'<a\s+itemprop=["\']url["\']\s+href="\./(?:index|blog|gallery|videos|single-article)\.html">Tech\s*</a>'),
     '<a itemprop="url" href="./single-category.html">Tech </a>'),
    (re.compile(
        r'<a\s+itemprop=["\']url["\']\s+href="\./(?:index|blog|gallery|videos|single-article)\.html">Sport\s*</a>'),
     '<a itemprop="url" href="./single-category.html">Sport </a>'),
    (re.compile(
        r'<a\s+itemprop=["\']url["\']\s+href="\./(?:index|blog|gallery|videos|single-article|single-category)\.html">Entertainment\s*</a>'),
     '<a itemprop="url" href="./single-category.html">Entertainment </a>'),
]

MEGA_TOGGLE = [
    (re.compile(
        r'(<a\s+itemprop=["\']url["\']\s+class="\s*dropdown-toggle"\s+href="\./)index\.html(".*?>\s*Politics\s*<em)'),
     r'\1single-category.html\2'),
    (re.compile(
        r'(<a\s+itemprop=["\']url["\']\s+class="\s*dropdown-toggle"\s+href="\./)blog\.html(".*?>\s*Business\s*<em)'),
     r'\1single-category.html\2'),
    (re.compile(
        r'(<a\s+itemprop=["\']url["\']\s+class="\s*dropdown-toggle"\s+href="\./)gallery\.html(".*?>\s*World\s*<em)'),
     r'\1single-category.html\2'),
    (re.compile(
        r'(<a\s+itemprop=["\']url["\']\s+class="\s*dropdown-toggle"\s+href="\./)(?:single-category|index|blog|gallery|videos|single-article)\.html(".*?>\s*Tech\s*<em)'),
     r'\1single-category.html\2'),
    (re.compile(
        r'(<a\s+itemprop=["\']url["\']\s+class="\s*dropdown-toggle"\s+href="\./)(?:index|blog|gallery|videos|single-article|single-category)\.html(".*?>\s*Sport\s*<em)'),
     r'\1single-category.html\2'),
    (re.compile(
        r'(<a\s+itemprop=["\']url["\']\s+class="\s*dropdown-toggle"\s+href="\./)(?:index|blog|gallery|videos|single-article|single-category)\.html(".*?>\s*Entertainment\s*<em)'),
     r'\1single-category.html\2'),
]

# "All Sections" megamenu (Mod121) — top-level h4 only
MOD121_H4 = [
    (re.compile(r'<a href="\./index\.html">\s*\n\s*Politics\s*</a>'), '<a href="./single-category.html">\n\t\t\t\n\t\t\tPolitics\t\t</a>'),
    (re.compile(r'<a href="\./blog\.html">Business\s*</a>'), '<a href="./single-category.html">Business\t\t</a>'),
    (re.compile(r'<a href="\./gallery\.html">World\s*</a>'), '<a href="./single-category.html">World\t\t</a>'),
    (re.compile(r'<a href="\./videos\.html">Sport\s*</a>'), '<a href="./single-category.html">Sport\t\t</a>'),
    (re.compile(r'<a href="\./index\.html">\s*\n\s*Entertaiment\s*</a>'),
     '<a href="./single-category.html">\n\t\t\t\n\t\t\tEntertainment\t\t</a>'),
]

# Brick category strip (index + any copy)
CATEGORY_MENU = re.compile(
    r'(<div class="category-menu"><ul><li>\s*)'
    r'(<a href="\./[^"]+">Politics</a>\s*</li><li>\s*)'
    r'(<a href="\./[^"]+">Business\s*</a>\s*</li><li>\s*)'
    r'(<a href="\./[^"]+">World\s*</a>\s*</li><li>\s*)'
    r'(<a href="\./[^"]+">Tech</a>\s*</li><li>\s*)'
    r'(<a href="\./[^"]+">Sport\s*</a>\s*</li><li>\s*)'
    r'(<a href="\./[^"]+">Entertaiment</a>)',
    re.DOTALL,
)

def repl_category_menu(m: re.Match) -> str:
    return (
        m.group(1)
        + '<a href="./single-category.html">Politics</a>\n\t\t\t\t\t</li><li>\n'
        + '\t\t\t\t\t\t<a href="./single-category.html">Business\t\t</a>\n\t\t\t\t\t</li><li>\n'
        + '\t\t\t\t\t\t<a href="./single-category.html">World\t\t</a>\n\t\t\t\t\t</li><li>\n'
        + '\t\t\t\t\t\t<a href="./single-category.html">Tech</a>\n\t\t\t\t\t</li><li>\n'
        + '\t\t\t\t\t\t<a href="./single-category.html">Sport\t\t</a>\n\t\t\t\t\t</li><li>\n'
        + '\t\t\t\t\t\t<a href="./single-category.html">Entertainment</a>'
    )

# Remove embedded duplicate leaderboard ads (title Top 1), keep empty banneritem shell
DUP_LEADER = re.compile(
    r'(<div class="banneritem">)\s*<a[^>]*title="Top 1"[^>]*>\s*'
    r'<img[^>]*top-leaderboard\.jpg[^>]*>\s*'
    r'</a>\s*(<div class="clr"></div>\s*</div>)',
    re.IGNORECASE | re.DOTALL,
)

# Multiline <img ... src= on next lines
DUP_LEADER2 = re.compile(
    r'(<div class="banneritem">)\s*<a[\s\S]*?title="Top 1"[\s\S]*?>[\s\S]*?'
    r'top-leaderboard\.jpg[\s\S]*?/>[\s\S]*?</a>\s*(<div class="clr"></div>\s*</div>)',
    re.IGNORECASE | re.DOTALL,
)

# Top leaderboard sponsor link (all pages use same anchor text + image pair)
TOP_BANNER_SPONSOR = '<a href="./registration.html" title="Site sponsor">'
TOP_BANNER_SPONSOR_NEW = '<a href="./single-category.html" title="Browse category">'

# Megamenu: remove empty leaderboard placeholder column (was duplicate ad)
EMPTY_LEADER_MEGA = re.compile(
    r'<div class="col-xs-12 mega-col-module" data-width="12" data-position="98"><div class="mega-inner">\s*'
    r'<div class="t3-module module mod-noborder " id="Mod98"><div class="module-inner"><div class="module-ct no-title"><div class="bannergroup mod-noborder">\s*'
    r'<div class="banneritem"><div class="clr"></div>\s*</div>\s*'
    r"</div>\s*</div>\s*</div>\s*</div>\s*</div>\s*</div>\s*</div>\s*</div>",
    re.DOTALL,
)

# index.html mastbot: strip empty leaderboard modules under separator
MASTBOT_EMPTY = re.compile(
    r"\s*<div class=\"t3-module module mod-noborder \" id=\"Mod98\">[\s\S]*?<div class=\"banneritem\"><div class=\"clr\"></div>[\s\S]*?</div>\s*</div>\s*</div>\s*</div>\s*</div>",
    re.DOTALL,
)
MASTBOT_EMPTY107 = re.compile(
    r'\s*<div class="t3-module module " id="Mod107">[\s\S]*?<div class="banneritem"><div class="clr"></div>[\s\S]*?</div>\s*</div>\s*</div>\s*</div>\s*</div>',
    re.DOTALL,
)

LOGO_COL_MARKER = '<div class="col-xs-12 col-sm-6 col-lg-4 logo">'
SPOT_COL_MARKER = '<div class="col-xs-12 col-sm-6 col-lg-8">'


def _consume_outer_div(s: str, start: int) -> tuple[str, int] | None:
    """Given start at '<div', return (substring including outer div, index after it) or None."""
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

MAG_BREAK_SNIPPET = """<div class="col-xs-12 col-sm-6 col-lg-8">
							<div class="t3-sl t3-sl-1">
						<div class="t3-spotlight t3-spotlight-1 row">
					<div class="col col-lg-6 col-md-6 col-sm-6 hidden-sm col-xs-6 hidden-xs t3-header-magazine">
								<div class="t3-module module " id="Mod108"><div class="module-inner"><div class="module-ct no-title">
<a class="t3-header-magazine__imgwrap" href="./registration.html" title="Newsletters — Subscribe now and save">
				<img class="t3-header-magazine__img" src="./images/header-mag-cover.jpg" alt="Newsletters — Subscribe now and save" width="333" height="120">
			</a>
</div></div></div>
							</div>
					<div class="col col-lg-6 col-md-6 col-sm-12 col-xs-12 hidden-xs t3-header-breaking-col">
								<div class="t3-module module " id="Mod109"><div class="module-inner"><h3 class="module-title "><span>Breaking News</span></h3><div class="module-ct "><ul class="latest-news-header ">
	<li class="clearfix">
		<a class="item-title" href="./single-article.html" itemprop="url">
			<span itemprop="name">
				Donald Trump Threatens to Sue The Times Over Article on Unwa...			</span>
		</a>

		
<div class="pull-left item-image" itemprop="image">

  <a href="./single-article.html" itemprop="url">
   <img src="./images/news-1.jpg" alt="Donald Trump Threatens to Sue The Times Over Article on Unwanted  Advances" itemprop="thumbnailUrl">
  </a>
</div>
	</li>
</ul>
</div></div></div>
							</div>
			</div>
				</div>
					</div>"""

LOGO_SNIPPET = """<div class="col-xs-12 col-sm-6 col-lg-4 logo">
			<div class="logo-text">
				<a href="./index.html" title="focus">
															<span>focus</span>
				</a>
							</div>
		</div>"""


def swap_header_newsletter_before_logo(content: str) -> str:
    """Put spotlight (magazine + breaking) column before logo column inside #t3-header."""
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
        if spot_i < logo_i:
            out.append(content[h : hend + len("</header>")])
            pos = hend + len("</header>")
            continue
        logo_block = _consume_outer_div(content, logo_i)
        spot_block = _consume_outer_div(content, spot_i)
        if not logo_block or not spot_block:
            out.append(content[h : hend + len("</header>")])
            pos = hend + len("</header>")
            continue
        logo_s, _logo_end = logo_block
        spot_s, spot_end = spot_block
        before = content[h : row + len('<div class="row">')]
        tail = content[spot_end : hend + len("</header>")]
        rebuilt = before + "\n\n" + spot_s + "\n\n" + logo_s + tail
        out.append(rebuilt)
        pos = hend + len("</header>")
    return "".join(out)


SINGLE_CATEGORY_HEADER_BLOCK = (
    "<!-- HEADER -->\n"
    '<header id="t3-header" class="container t3-header">\n'
    "\t<div class=\"row\">\n\n"
    + LOGO_SNIPPET
    + "\n\n"
    + MAG_BREAK_SNIPPET
    + "\n\n"
    "\t</div>\n"
    "</header>\n"
    "<!-- //HEADER -->"
)


def fix_single_category_header(content: str) -> str:
    """Rebuild single-category header: logo first, then magazine + breaking (default JA layout)."""
    start = content.find("<!-- HEADER -->")
    end = content.find("<!-- //HEADER -->")
    if start == -1 or end == -1:
        return content
    end += len("<!-- //HEADER -->")
    return content[:start] + SINGLE_CATEGORY_HEADER_BLOCK + content[end:]


def fix_top_banner_block(content: str) -> str:
    """single-category: broken top banner -> standard leaderboard."""
    old = re.compile(
        r'<!-- TOP BANNER -->[\s\S]*?<!-- TOP BANNER -->',
        re.DOTALL,
    )

    def repl_banner(mm: re.Match) -> str:
        return (
            "\t<!-- TOP BANNER -->\n"
            "\t<div class=\"ja-banner banner-top text-center \">\n"
            "\t\t<div class=\"container\">\n"
            "\t\t\t<div class=\"bannergroup\">\n"
            "\t<div class=\"banneritem\">\n"
            "\t\t\t<a href=\"./single-category.html\" title=\"Browse category\">\n"
            "\t\t\t\t<img src=\"./images/top-leaderboard.jpg\" width=\"728\" height=\"90\" alt=\"Site sponsor\">\n"
            "\t\t\t</a>\n"
            "\t\t\t<div class=\"clr\"></div>\n"
            "\t</div>\n"
            "</div>\n"
            "\t\t</div>\n"
            "\t</div>\n"
            "\t<!-- TOP BANNER -->"
        )

    return old.sub(repl_banner, content, count=1)


def process_file(path: Path) -> bool:
    raw = path.read_text(encoding="utf-8", errors="replace")
    orig = raw

    raw = OFF_CANVAS_NAV.sub(repl_off_canvas, raw)
    for pat, rep in MEGA_SIMPLE:
        raw = pat.sub(rep, raw)
    for pat, rep in MEGA_TOGGLE:
        raw = pat.sub(rep, raw)
    for pat, rep in MOD121_H4:
        raw = pat.sub(rep, raw)
    raw = CATEGORY_MENU.sub(repl_category_menu, raw)

    raw = DUP_LEADER.sub(r"\1\2", raw)
    raw = DUP_LEADER2.sub(r"\1\2", raw)
    raw = EMPTY_LEADER_MEGA.sub("", raw)
    raw = raw.replace(TOP_BANNER_SPONSOR, TOP_BANNER_SPONSOR_NEW)
    raw = re.sub(
        r'<a href="\./registration\.html\d+"([^>]*>\s*<img[^>]*top-leaderboard\.jpg)',
        r'<a href="./single-category.html"\1',
        raw,
        flags=re.IGNORECASE | re.DOTALL,
    )

    if path.name == "index.html":
        raw = MASTBOT_EMPTY.sub("", raw)
        raw = MASTBOT_EMPTY107.sub("", raw)

    if path.name == "single-category.html":
        raw = fix_top_banner_block(raw)
        raw = fix_single_category_header(raw)

    # Fix megamenu wrong active on single-category (World vs Tech)
    if path.name == "single-category.html":
        raw = raw.replace(
            '<li itemprop="name" class="current active mega-align-justify cat-blue">\n'
            '<a itemprop="url" href="./single-category.html">World </a>',
            '<li itemprop="name" class="mega-align-justify cat-blue">\n'
            '<a itemprop="url" href="./single-category.html">World </a>',
        )
        raw = raw.replace(
            '<li itemprop="name" class="mega-align-justify cat-cyan">\n'
            '<a itemprop="url" href="./single-category.html">Tech </a>',
            '<li itemprop="name" class="current active mega-align-justify cat-cyan">\n'
            '<a itemprop="url" href="./single-category.html">Tech </a>',
        )

    if raw != orig:
        path.write_text(raw, encoding="utf-8", newline="\n")
        return True
    return False


def main() -> None:
    changed = []
    for p in sorted(ROOT.glob("*.html")):
        if process_file(p):
            changed.append(p.name)
    print("updated:", ", ".join(changed) if changed else "(none)")


if __name__ == "__main__":
    main()
