# Migrate Login, Registration, Smart Search, 404 exports to shared ./css ./js ./images
$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path

function Rewrite-AssetPaths([string]$text, [string]$folderName) {
  $esc = [regex]::Escape("./$folderName/")
  $text = [regex]::Replace($text, $esc + '([^"'']+\.css)(?=")', './css/$1', [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
  $text = [regex]::Replace($text, $esc + '(icon|css)(?=")', './css/$1')
  $text = [regex]::Replace($text, $esc + '([^"'']+\.Download)(?=")', './js/$1', [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
  $text = [regex]::Replace($text, $esc + '([^"'']+\.(jpg|jpeg|png|gif))(?=")', './images/$1', [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
  return $text
}

function Ensure-HeadFonts([string]$text) {
  if ($text -match 'fonts\.googleapis\.com') { return $text }
  $inject = @"
	<link rel="preconnect" href="https://fonts.googleapis.com">
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
	<link rel="preload" as="font" type="font/woff2" crossorigin href="https://fonts.gstatic.com/s/heebo/v28/NGS6v5_NC0k9P9H2TbE.woff2">
	<link rel="preload" as="font" type="font/woff2" crossorigin href="https://fonts.gstatic.com/s/noticiatext/v16/VuJ2dNDF2Yv9qppOePKYRP12ZjtY.woff2">
	<link rel="preload" as="font" type="font/woff2" crossorigin href="https://fonts.gstatic.com/s/noticiatext/v16/VuJpdNDF2Yv9qppOePKYRP1-3R5NuGvQ.woff2">
	<link rel="preload" as="font" type="font/woff2" crossorigin href="https://fonts.gstatic.com/s/noticiatext/v16/VuJodNDF2Yv9qppOePKYRP12Ywtan04.woff2">
	<link href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;500;700;900&amp;family=Noticia+Text:ital,wght@0,400;0,700;1,400&amp;display=swap" rel="stylesheet" type="text/css">
	<link rel="preload" as="image" href="./images/top-leaderboard.jpg" />
	<link rel="preload" as="image" href="./images/header-mag-cover.jpg" />
"@
  if ($text -notmatch '(?i)<head[^>]*>') { return $text }
  return [regex]::Replace($text, '(?i)(<head[^>]*>)', "`$1`n$inject", 1)
}

function Fix-TopBanner([string]$text) {
  $needle = '<img src="./images/top-leaderboard.jpg" alt="Top 1">'
  if ($text.IndexOf($needle, [StringComparison]::Ordinal) -lt 0) { return $text }
  $once = $true
  $sb = New-Object System.Text.StringBuilder
  $idx = 0
  while ($true) {
    $i = $text.IndexOf($needle, $idx, [StringComparison]::Ordinal)
    if ($i -lt 0) { break }
    [void]$sb.Append($text.Substring($idx, $i - $idx))
    if ($once) {
      [void]$sb.Append('<img fetchpriority="high" src="./images/top-leaderboard.jpg" width="728" height="90" alt="Top 1" />')
      $once = $false
    }
    else {
      [void]$sb.Append('<img src="./images/top-leaderboard.jpg" width="728" height="90" alt="Top 1" />')
    }
    $idx = $i + $needle.Length
  }
  [void]$sb.Append($text.Substring($idx))
  return $sb.ToString()
}

function Fix-Logo([string]$text) {
  return $text.Replace('href="https://ja-focus.demo.joomlart.com/" title="focus"', 'href="./index.html" title="focus"')
}

function Fix-BannerFallback([string]$text) {
  return $text
}

function Strip-RssAtomOpensearch([string]$text) {
  $text = [regex]::Replace($text, '\s*<link href="https://ja-focus\.demo\.joomlart\.com/index\.php/[^"]+\?format=feed[^>]+>\s*', "`n")
  $text = [regex]::Replace($text, '\s*<link href="https://ja-focus\.demo\.joomlart\.com/index\.php/component/search/\?[^>]+>\s*', "`n")
  return $text
}

# --- copy extra assets for Smart Search + 404 image ---
$ss = Join-Path $root "Smart Search_files"
$css = Join-Path $root "css"
$js = Join-Path $root "js"
$img = Join-Path $root "images"
@(
  @((Join-Path $ss "chosen.css"), (Join-Path $css "chosen.css")),
  @((Join-Path $ss "finder.css"), (Join-Path $css "finder.css")),
  @((Join-Path $ss "chosen.jquery.min.js.Download"), (Join-Path $js "chosen.jquery.min.js.Download")),
  @((Join-Path $ss "jquery.autocomplete.min.js.Download"), (Join-Path $js "jquery.autocomplete.min.js.Download")),
  @((Join-Path $root "404 Page_files\404-page.jpg"), (Join-Path $img "404-page.jpg"))
) | ForEach-Object { if (Test-Path $_[0]) { Copy-Item $_[0] $_[1] -Force } }

$migrations = @(
  @{ Src = "Login.html"; Folder = "Login_files"; Dest = "login.html"; StripFeeds = $false; Slug = "login" },
  @{ Src = "Registration.html"; Folder = "Registration_files"; Dest = "registration.html"; StripFeeds = $false; Slug = "registration" },
  @{ Src = "Smart Search.html"; Folder = "Smart Search_files"; Dest = "search.html"; StripFeeds = $true; Slug = "smart-search" },
  @{ Src = "404 Page.html"; Folder = "404 Page_files"; Dest = "404.html"; StripFeeds = $true; Slug = "404-page" }
)

foreach ($m in $migrations) {
  $srcPath = Join-Path $root $m.Src
  if (-not (Test-Path $srcPath)) { Write-Warning "Missing $($m.Src)"; continue }
  $c = [IO.File]::ReadAllText($srcPath)
  $c = Rewrite-AssetPaths $c $m.Folder
  if ($m.StripFeeds) { $c = Strip-RssAtomOpensearch $c }
  $c = Ensure-HeadFonts $c
  $c = Fix-TopBanner $c
  $c = Fix-Logo $c
  $c = Fix-BannerFallback $c
  $slug = $m.Slug
  $c = $c.Replace("https://ja-focus.demo.joomlart.com/index.php/$slug#", "#")
  [IO.File]::WriteAllText((Join-Path $root $m.Dest), $c)
  Write-Host "Wrote $($m.Dest)"
}

# --- search.html ---
$searchPath = Join-Path $root "search.html"
if (Test-Path $searchPath) {
  $s = [IO.File]::ReadAllText($searchPath)
  $s = $s.Replace('<title>Smart Search</title>', '<title>Search</title>')
  $s = [regex]::Replace($s, 'action="https://ja-focus\.demo\.joomlart\.com/index\.php/smart-search[^"]*"', 'action="./search.html"')
  $s = $s.Replace("serviceUrl: '/index.php/smart-search?task=suggestions.suggest&amp;format=json&amp;tmpl=component',", "serviceUrl: './search-suggestions.json',")
  $s = $s.Replace('minChars: 1,', 'minChars: 99,')
  [IO.File]::WriteAllText($searchPath, $s)
}

# --- login.html ---
$loginPath = Join-Path $root "login.html"
if (Test-Path $loginPath) {
  $L = [IO.File]::ReadAllText($loginPath)
  $L = $L.Replace('href="https://ja-focus.demo.joomlart.com/index.php/login#"', 'href="#"')
  $L = $L.Replace('action="https://ja-focus.demo.joomlart.com/index.php/login"', 'action="./login.html"')
  $L = $L.Replace('action="https://ja-focus.demo.joomlart.com/index.php/login?task=user.login"', 'action="./login.html"')
  [IO.File]::WriteAllText($loginPath, $L)
}

# --- registration.html ---
$regPath = Join-Path $root "registration.html"
if (Test-Path $regPath) {
  $R = [IO.File]::ReadAllText($regPath)
  $R = $R.Replace('href="https://ja-focus.demo.joomlart.com/index.php/registration#"', 'href="#"')
  $R = $R.Replace('action="https://ja-focus.demo.joomlart.com/index.php/registration"', 'action="./registration.html"')
  $R = $R.Replace('action="https://ja-focus.demo.joomlart.com/index.php/registration?task=registration.register"', 'action="./registration.html"')
  $R = $R.Replace('href="https://ja-focus.demo.joomlart.com/index.php/registration?view=reset"', 'href="./registration.html"')
  $R = $R.Replace('href="https://ja-focus.demo.joomlart.com/index.php/registration?view=remind"', 'href="./registration.html"')
  $R = $R.Replace('href="https://ja-focus.demo.joomlart.com/index.php/registration">', 'href="./registration.html">')
  [IO.File]::WriteAllText($regPath, $R)
}

# --- 404.html ---
$fourPath = Join-Path $root "404.html"
if (Test-Path $fourPath) {
  $F = [IO.File]::ReadAllText($fourPath)
  $F = $F.Replace('href="https://ja-focus.demo.joomlart.com/index.php/404-page#"', 'href="#"')
  $F = $F.Replace('action="https://ja-focus.demo.joomlart.com/index.php/404-page"', 'action="./404.html"')
  $F = $F.Replace('<title>404 Page</title>', '<title>Page not found</title>')
  $F = $F.Replace('href="https://ja-focus.demo.joomlart.com/index.php/404-page"', 'href="./404.html"')
  [IO.File]::WriteAllText($fourPath, $F)
}

# --- offline.html (from 404) — only article + header search; keep ./404.html in menus ---
if (Test-Path $fourPath) {
  $O = [IO.File]::ReadAllText($fourPath)
  $O = $O.Replace('<title>Page not found</title>', '<title>Offline</title>')
  $O = $O.Replace('<form action="./404.html" method="post" class="form-inline form-search">', '<form action="./offline.html" method="post" class="form-inline form-search">')
  $O = $O.Replace('<a href="./404.html" itemprop="url" title="404 Page">', '<a href="./offline.html" itemprop="url" title="Offline">')
  $O = $O.Replace('>404 Page</a>', '>Offline</a>')
  $O = $O.Replace('<div class="well"><center>Each <strong>JA Joomla Template</strong> has its own matching 404 page. Below is the screenshot of <strong>404 page style</strong>.</center></div>', '<div class="well"><center>This page represents the template <strong>offline</strong> screen (maintenance mode).</center></div>')
  $O = $O.Replace('<p align="center"><img class="img-responsive" src="./images/404-page.jpg" alt="Sample Image" border="0"></p>', '<p align="center"><span class="fa fa-power-off fa-5x text-muted" aria-hidden="true"></span></p>')
  $O = $O.Replace('<li class="item-131"><a href="./offline.html" class="">Offline Page</a></li><li class="item-132 current active"><a href="./404.html" class="">404 Page</a></li></ul>', '<li class="item-131 current active"><a href="./offline.html" class="">Offline Page</a></li><li class="item-132"><a href="./404.html" class="">404 Page</a></li></ul>')
  [IO.File]::WriteAllText((Join-Path $root "offline.html"), $O)
}

[IO.File]::WriteAllText((Join-Path $root "search-suggestions.json"), "[]`n")

@("Login.html", "Registration.html", "Smart Search.html", "404 Page.html") | ForEach-Object {
  $p = Join-Path $root $_
  if (Test-Path $p) { Remove-Item $p -Force; Write-Host "Removed $_" }
}

$pairs = @(
  @('href="https://ja-focus.demo.joomlart.com/index.php/login"', 'href="./login.html"'),
  @('href="https://ja-focus.demo.joomlart.com/index.php/registration"', 'href="./registration.html"'),
  @('href="https://ja-focus.demo.joomlart.com/index.php/search"', 'href="./search.html"'),
  @('href="https://ja-focus.demo.joomlart.com/index.php/smart-search"', 'href="./search.html"'),
  @('href="https://ja-focus.demo.joomlart.com/index.php/404-page"', 'href="./404.html"'),
  @('href="https://ja-focus.demo.joomlart.com/index.php/offline-page"', 'href="./offline.html"')
)
Get-ChildItem -Path $root -Filter "*.html" | ForEach-Object {
  $c = [IO.File]::ReadAllText($_.FullName)
  $orig = $c
  foreach ($p in $pairs) { $c = $c.Replace($p[0], $p[1]) }
  if ($c -ne $orig) { [IO.File]::WriteAllText($_.FullName, $c); Write-Host "Updated links in $($_.Name)" }
}

Write-Host "Done."
