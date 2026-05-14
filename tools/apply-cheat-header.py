# -*- coding: utf-8 -*-
"""Align root *.html header + top banner with cheat sheet.html (JA Focus)."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

OLD_TOP = """<!-- TOP BANNER -->
<div class="site-top-leader">
		<a class="site-top-leader__link" href="./registration.html">
			<img class="site-top-leader__img" src="./images/top-leaderboard.jpg" width="728" height="90" alt="Site sponsor">
		</a>
</div>
<!-- TOP BANNER -->"""

NEW_TOP = """	<!-- TOP BANNER -->
	<div class="ja-banner banner-top text-center ">
		<div class="container">
			<div class="bannergroup">
	<div class="banneritem">
			<a href="./registration.html" title="Site sponsor">
				<img src="./images/top-leaderboard.jpg" width="728" height="90" alt="Site sponsor">
			</a>
			<div class="clr"></div>
	</div>
</div>
		</div>
	</div>
	<!-- TOP BANNER -->"""

HDR = re.compile(
    r'<header id="t3-header" class="container t3-header">\s*<div class="row t3-header__row">\s*'
    r'<div class="col-xs-12 col-sm-6 col-md-4 col-lg-4 logo">(.*?)</div>\s*'
    r'<section class="col-xs-12 col-sm-6 col-md-4 col-lg-4 t3-header-magazine"[^>]*>(.*?)</section>\s*'
    r'<div class="col-xs-12 col-sm-12 col-md-4 col-lg-4 t3-header-breaking-col">\s*'
    r'<div class="t3-sl t3-sl-1">\s*'
    r'(<div class="t3-module module[^>]*id="Mod109">.*?</div>\s*</div>\s*</div>)\s*'
    r'</div>\s*</div>\s*</div>\s*</header>',
    re.DOTALL,
)


def repl_header(m: re.Match) -> str:
    logo, mag, mod = m.group(1), m.group(2).strip(), m.group(3).strip()
    return f"""<header id="t3-header" class="container t3-header">
	<div class="row">

		<div class="col-xs-12 col-sm-6 col-lg-4 logo">{logo}</div>

		<div class="col-xs-12 col-sm-6 col-lg-8">
							<div class="t3-sl t3-sl-1">
						<div class="t3-spotlight t3-spotlight-1 row">
					<div class="col col-lg-6 col-md-6 col-sm-6 hidden-sm col-xs-6 hidden-xs t3-header-magazine">
								<div class="t3-module module " id="Mod108"><div class="module-inner"><div class="module-ct no-title">
{mag}
</div></div></div>
							</div>
					<div class="col col-lg-6 col-md-6 col-sm-12 col-xs-12 hidden-xs t3-header-breaking-col">
								{mod}
							</div>
			</div>
				</div>
					</div>

	</div>
</header>"""


def main() -> None:
    for f in sorted(ROOT.glob("*.html")):
        t = f.read_text(encoding="utf-8", errors="replace")
        if "site-top-leader" in t:
            t2 = t.replace(OLD_TOP, NEW_TOP)
            if t2 == t:
                t2 = t.replace(OLD_TOP.replace("\n", "\r\n"), NEW_TOP.replace("\n", "\r\n"))
            t = t2
        m = HDR.search(t)
        if not m:
            print("SKIP (no header match)", f.name)
            continue
        t = HDR.sub(repl_header, t, count=1)
        f.write_text(t, encoding="utf-8", newline="\n")
        print("OK", f.name)


if __name__ == "__main__":
    main()
