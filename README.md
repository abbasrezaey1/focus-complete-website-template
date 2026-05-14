# JA Focus — Complete static website template

A **self-contained, offline-friendly** export of the **JA Focus** news & magazine Joomla demo, rebuilt as plain **HTML + CSS + JavaScript** with local assets. Open `index.html` in a browser or serve the folder with any static host—no build step required.

![License](https://img.shields.io/badge/license-Demo%20template-blue)
![Stack](https://img.shields.io/badge/stack-HTML%20%7C%20CSS%20%7C%20JS-lightgrey)

## What you get

- **Full page set**: Home, About, Blog, Gallery, Tech, Videos, Single article, Contact, Login, Registration, Search, Offline, and 404.
- **Shared design system**: Bootstrap-based layout, megamenu, off-canvas, Swiper carousels, image galleries, and the original JA Focus look.
- **Local assets**: Styles in `./css/`, scripts in `./js/`, media in `./images/`. Paths are relative so the site works from disk or any subdirectory-aware server.
- **Performance polish**: Google Fonts with `preconnect`, critical **WOFF2 preloads**, `display=swap`, **LCP header image preloads** (leaderboard + magazine strip), stable vertical scrollbar (`scrollbar-gutter`), and reduced font synthesis flicker—so navigation between pages stays visually steady.

## Quick start

1. Clone the repository.
2. Open **`index.html`** in your browser, **or** run a local static server from the project root (recommended for correct loading of some features):

   ```bash
   npx serve .
   ```

   Or with Python:

   ```bash
   python -m http.server 8080
   ```

3. Visit `http://localhost:8080` (or the port shown by your tool).

## Project layout

| Path | Purpose |
|------|--------|
| `index.html`, `about.html`, … | Page entry points |
| `css/` | Stylesheets (`template.css`, Bootstrap, Font Awesome, modules) |
| `js/` | jQuery, Joomla front-end scripts, Swiper, gallery, etc. |
| `images/` | Logos, banners, article thumbs, icons |
| `tools/` | Helper scripts (e.g. migrating utility pages to local paths) |
| `*_files/` | Legacy export folders kept for reference or extra assets |

## Customization tips

- **Global fonts & base styles**: `css/template.css` (search for the “Local JA Focus” comment near the end for the `html` / `body` stack and scrollbar behavior).
- **Favicon & header images**: under `images/`; preload links live in each page `<head>` next to the Google Fonts stylesheet.
- **Internal links**: Many anchors already point to sibling `.html` files for offline navigation.

## Browser support

Modern evergreen browsers (Chrome, Firefox, Safari, Edge). Some legacy IE-oriented classes remain from the original template but are not a target for active support.

## Credits & license

- **Design & original template**: [JoomlArt — JA Focus](https://www.joomlart.com/joomla-templates/ja-focus) (Joomla demo export).
- This repository is a **static, educational/portfolio packaging** of that demo with local paths and small performance and consistency tweaks. **Respect JoomlArt’s license** if you use this commercially; purchase or license the official template from the vendor when appropriate.

## Author

Maintained by **[abbasrezaey1](https://github.com/abbasrezaey1)** — [`focus-complete-website-template`](https://github.com/abbasrezaey1/focus-complete-website-template).

---

If this template saved you time, consider starring the repo and crediting JoomlArt for the original design.
