# Rewrite ja-focus.demo.joomlart.com links in all root *.html to internal static targets
$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path

function Map-JoomlaPath([string]$path) {
  $path = $path.TrimEnd('/')
  if ([string]::IsNullOrWhiteSpace($path)) { return "./index.html" }

  if ($path.StartsWith("component/")) { return "#" }
  if ($path.StartsWith("gallery")) { return "./gallery.html" }
  if ($path.StartsWith("videos")) { return "./videos.html" }
  if ($path.StartsWith("blog")) { return "./blog.html" }
  if ($path.StartsWith("contact")) { return "./contact.html" }
  if ($path.StartsWith("about")) { return "./about.html" }
  if ($path.StartsWith("login")) { return "./login.html" }
  if ($path.StartsWith("registration")) { return "./registration.html" }
  if ($path.StartsWith("smart-search") -or $path.StartsWith("search")) { return "./search.html" }
  if ($path.StartsWith("404-page")) { return "./404.html" }
  if ($path.StartsWith("offline-page")) { return "./offline.html" }
  if ($path.StartsWith("single-article")) { return "./single-article.html" }
  if ($path.StartsWith("featured-article") -or $path.StartsWith("typography")) { return "./single-article.html" }
  if ($path.StartsWith("tagged-items")) { return "./search.html" }

  # Tech: category landing slug used on demo
  if ($path -match '^tech/\d+-computer$' -or $path -eq 'tech') { return "./tech.html" }

  # Top-level section only (e.g. politics, business)
  if ($path -notmatch '/') { return "./index.html" }

  # Deep article / subcategory URLs
  return "./single-article.html"
}

function Rewrite-Html([string]$html) {
  # Remove Joomla feed link tags
  $html = [regex]::Replace($html, '\s*<link href="https://ja-focus\.demo\.joomlart\.com/index\.php\?format=[^"]+"[^>]*>\s*', "`n")

  # Favicon: avoid remote template host
  $html = $html.Replace('https://ja-focus.demo.joomlart.com/templates/ja_focus/favicon.ico', './images/logo.png')

  # Banner / tracking
  $html = [regex]::Replace($html, 'href="https://ja-focus\.demo\.joomlart\.com/index\.php/component/banners/[^"]*"', 'href="#"')

  # Joomla root hash
  $html = $html.Replace('href="https://ja-focus.demo.joomlart.com/#"', 'href="#"')

  # Form post to home index (header search etc.)
  $html = $html.Replace('action="https://ja-focus.demo.joomlart.com/index.php"', 'action="./search.html"')
  $html = $html.Replace("action='https://ja-focus.demo.joomlart.com/index.php'", "action='./search.html'")

  # Acymailing and other components — disable off-site submit
  $html = [regex]::Replace($html, 'action="https://ja-focus\.demo\.joomlart\.com/index\.php/component/[^"]*"', 'action="#"')

  # Meta / JSON absolute URLs on ja-focus host
  $html = [regex]::Replace($html, 'https://ja-focus\.demo\.joomlart\.com//templates/ja_focus/images/logo\.png', './images/logo.png')
  $html = [regex]::Replace($html, 'https://ja-focus\.demo\.joomlart\.com/templates/ja_focus/images/logo\.png', './images/logo.png')

  # href="https://ja-focus...index.php/..."
  $html = [regex]::Replace($html, 'href="https://ja-focus\.demo\.joomlart\.com/index\.php/([^"]*)"', {
      param($m)
      $rel = $m.Groups[1].Value
      $rel = $rel -replace '\?.*$', '' # strip query for mapping
      $target = Map-JoomlaPath $rel
      return 'href="' + $target + '"'
    })

  # Any remaining bare ja-focus URLs in href (e.g. index.php?option=...)
  $html = [regex]::Replace($html, 'href="https://ja-focus\.demo\.joomlart\.com/index\.php[^"]*"', 'href="./index.html"')

  # Meta logo URL only (avoid clobbering other microdata)
  $html = [regex]::Replace($html, 'content="https://ja-focus\.demo\.joomlart\.com//templates/ja_focus/images/logo\.png"', 'content="./images/logo.png"')
  $html = [regex]::Replace($html, 'content="https://ja-focus\.demo\.joomlart\.com/templates/ja_focus/images/logo\.png"', 'content="./images/logo.png"')

  # onclick window.open mailto links — point to # 
  $html = [regex]::Replace($html, 'https://ja-focus\.demo\.joomlart\.com/index\.php/component/mailto/[^''"]+', '#')

  # Form actions (header search, contact form, etc.)
  $html = [regex]::Replace($html, 'action="https://ja-focus\.demo\.joomlart\.com/index\.php/([^"]*)"', {
      param($m)
      $rel = $m.Groups[1].Value -replace '\?.*$', ''
      $target = Map-JoomlaPath $rel
      return 'action="' + $target + '"'
    })

  # JATabs ajax root (avoid remote fetches)
  $html = $html.Replace("siteroot:'https://ja-focus.demo.joomlart.com/'", "siteroot:'./'")

  # Remote images under /images/joomlart/...
  $html = [regex]::Replace($html, 'src="https://ja-focus\.demo\.joomlart\.com/images/joomlart/[^/]+/([^"]+)"', {
      param($m)
      return 'src="./images/' + $m.Groups[1].Value + '"'
    })

  # Saved-from / base comments (no external host in source comment)
  $html = [regex]::Replace($html, '<!-- saved from url=\([^)]+\)[^>]*-->', '<!-- local HTML export -->')
  $html = [regex]::Replace($html, '<!--<base href="https://ja-focus\.demo\.joomlart\.com[^"]*">-->', '<!--<base href=".">-->')

  return $html
}

Get-ChildItem -Path $root -Filter "*.html" | ForEach-Object {
  $p = $_.FullName
  $c = [IO.File]::ReadAllText($p)
  $n = Rewrite-Html $c
  if ($n -ne $c) {
    [IO.File]::WriteAllText($p, $n)
    Write-Host "Updated $($_.Name)"
  }
}

Write-Host "Pass 1 done."
