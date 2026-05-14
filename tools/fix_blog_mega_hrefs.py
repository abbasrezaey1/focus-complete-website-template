from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAIRS = (
    (
        '<a itemprop=\'url\' class=" dropdown-toggle"  href="./index.html"   data-target="#" data-toggle="dropdown">Business <em class="caret"></em></a>',
        '<a itemprop=\'url\' class=" dropdown-toggle"  href="./single-category.html"   data-target="#" data-toggle="dropdown">Business <em class="caret"></em></a>',
    ),
    (
        '<a itemprop=\'url\' class=" dropdown-toggle"  href="./index.html"   data-target="#" data-toggle="dropdown">World <em class="caret"></em></a>',
        '<a itemprop=\'url\' class=" dropdown-toggle"  href="./single-category.html"   data-target="#" data-toggle="dropdown">World <em class="caret"></em></a>',
    ),
)

for p in sorted(ROOT.glob("*.html")):
    t = p.read_text(encoding="utf-8", errors="replace")
    o = t
    for a, b in PAIRS:
        t = t.replace(a, b)
    if t != o:
        p.write_text(t, encoding="utf-8", newline="\n")
        print("updated", p.name)
