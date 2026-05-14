# -*- coding: utf-8 -*-
"""Restore closing divs removed with empty Mod98 megamenu leaderboard column."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# After col-9 + latest grid, we had 3 wrapper closes then </li>; one </div> was for removed full-width col — restore 2 more.
FIX = re.compile(
    r"(</div>\s*</div>\s*</div>\s*\n\s*</div>\s*</div>\s*\n)</div>\s*\n</li>\s*\n"
    r'(<li itemprop=["\']name["\'] class="dropdown mega mega-align-justify cat-(?:orange|blue|cyan|green|yellow))',
    re.MULTILINE,
)


def main() -> None:
    for p in sorted(ROOT.glob("*.html")):
        t = p.read_text(encoding="utf-8", errors="replace")
        n = len(FIX.findall(t))
        if not n:
            continue
        t2 = FIX.sub(r"\1</div></div></div>\n</li>\n\2", t)
        p.write_text(t2, encoding="utf-8", newline="\n")
        print(p.name, "fixed", n)


if __name__ == "__main__":
    main()
