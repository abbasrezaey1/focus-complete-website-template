# -*- coding: utf-8 -*-
"""Fix mega closings when template had only one </div> before </li> (e.g. blog.html)."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

BROKEN = re.compile(
    r"(</div></div></div>\s*</div></div>\s*)</div>\s*</li>\s*"
    r'(<li itemprop=["\']name["\'] class=["\']dropdown mega mega-align-justify[^"\']*["\'])',
    re.DOTALL,
)


def main() -> None:
    for p in sorted(ROOT.glob("*.html")):
        t = p.read_text(encoding="utf-8", errors="replace")
        n = len(BROKEN.findall(t))
        if not n:
            continue
        t2 = BROKEN.sub(r"\1</div></div></div>\n</li>\n\2", t)
        p.write_text(t2, encoding="utf-8", newline="\n")
        print(p.name, "fixed", n)


if __name__ == "__main__":
    main()
