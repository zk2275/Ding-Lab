# Ding Lab — website

The website for the **Ding Lab** (Ying Ding), Department of Biostatistics,
University of Pittsburgh.

- **Live site:** https://zk2275.github.io/Ding-Lab
- **Repo:** https://github.com/zk2275/Ding-Lab

Plain HTML and CSS. **No build step, no dependencies, nothing to install.** Edit a
file, commit it, and the site updates. You do not need to understand the whole
project to make a change — find the task you want below and copy the pattern.

---

## Start here: common tasks

> After any change, run `python3 tools/check.py` (see [Checks](#checks)). It catches
> the mistakes that are easy to make and hard to notice.

### Add or remove a student
`people.html` → find `Current doctoral students`. Copy one whole
`<figure class="member-card">` block, change the name, role, years, and photo. To
move someone to alumni, delete their card and add a `<div class="person">` row in
the `Alumni` section.

### Add a publication
`publications.html` → find the right year heading (`<h2 class="pub-year">`) and copy
an existing `<li>`. Keep `<strong>Ding Y</strong>` bold. If the year doesn't exist
yet, copy a whole `<section>`.

### Add a news item
`index.html` → find `Recent news`. Copy an `<li>`, change the date and text. Newest
goes on top.

### Change a research interest or its listed papers
`index.html` → `Research interests`. Each is one `<article class="interest">`: a
title, a description, and a `Recent work` line of `(author) year Journal`.
The longer prose version lives in `research.html`.

### Change colours or fonts
`assets/css/style.css`, the `:root { ... }` block at the very top. Change a hex value
there and it updates everywhere.

### Add a whole new page
Copy an existing page (e.g. `contact.html`), then:
1. change the `<title>` and `<meta name="description">`;
2. move `aria-current="page"` onto your new page's nav link;
3. **add the new link to the nav on all seven other pages** — the nav is copied into
   every page (see [The fragile bits](#the-fragile-bits)).

Then run the checks — they will tell you if you missed a page.

---

## Checks

```bash
python3 tools/check.py
```

Needs nothing but Python 3. It verifies:

- the shared header/footer are identical on every page;
- exactly one nav link per page is marked as the current page, and it's the right one;
- every internal link points at a page that exists;
- every image referenced actually exists, **matching capitalisation**;
- every `<img>` has `alt` text;
- the two rolling-gallery photo sets are in sync.

It prints plain English and exits non-zero on failure. It also runs automatically on
every push via GitHub Actions (`.github/workflows/check.yml`), so a broken change gets
flagged on the repo even if you forget to run it.

## The fragile bits

The site is hand-written, which keeps it simple forever but leaves a few rules that
break *quietly* — the page still loads, it's just wrong. **You don't have to memorise
these; `tools/check.py` enforces all of them.** They're written down so the errors make
sense:

1. **The header and footer are copy-pasted onto all 7 pages.** Change one, change all
   seven. They're marked `<!-- ===== SHARED HEADER ... -->` / `<!-- ===== SHARED FOOTER ... -->`.
2. **`aria-current="page"`** must sit on the current page's own nav link — that's what
   underlines the active tab.
3. **Filenames are case-sensitive in production.** GitHub Pages serves from Linux;
   macOS doesn't care about case. So `Photo.JPG` referenced as `photo.jpg` works on your
   laptop and 404s on the live site. (This already happened once, with `teaching.JPG`.)

---

## Structure

```
Ding-Lab/
├── index.html          Home (hero + affiliation, intro, research interests, news)
├── about.html          Biography, education, appointments
├── research.html       Research areas (placeholder copy + figures)
├── publications.html   Selected publications by year
├── people.html         PI, current students (photo grid), alumni
├── teaching.html       16:9 banner + courses and mentoring
├── contact.html        Email, office, department
├── assets/
│   ├── css/style.css   Single shared stylesheet (palette + all styles)
│   └── img/            See "Images" below
├── tools/check.py      The checks described above
└── .nojekyll           Tells GitHub Pages to serve files as-is (no Jekyll)
```

## Images

In use:

| File | Where | Notes |
|------|-------|-------|
| `pittsburgh.jpg` | Home hero background | Set via `url()` in `style.css` (`.hero`). |
| `Ding_Ying.jpg` | People PI card | |
| `teaching.jpg` | Teaching banner | Full-bleed 16:9 (`.page-banner`); natively 16:9, so no crop. |
| `public_health.jpg` | (unused) | Was the rolling gallery, now removed; kept in case you want it. |
| `School_of_Public_Health.png` | Site header, left of the nav | Official Pitt School of Public Health logo (transparent PNG). Sits in `.site-header-inner`, to the left of the primary nav, on every page. (The header has no text title; the lab name appears in the home hero.) |
| `<First>_<Last>.jpg/.png` | People — student headshots | One per current student (e.g. `Haoran_Hu.jpg`, `Zhuodiao_Kuang.png`). Square works best; shown as circles cropped near the top. |

Still placeholders, swap when you have real files:

- `figure-placeholder.svg` — the four Research figures (see each figure's SUGGESTED-FIGURE comment in `research.html`).
- `avatar-placeholder.svg` — fallback student headshot (all current students now have real photos, so it's unused; keep it for the next new student until their photo arrives).
- `banner-placeholder.svg`, `portrait-placeholder.svg` — unused; kept in case you want one back.

To add a new student with a photo: drop `First_Last.jpg` in `assets/img/`, copy a
`<figure class="member-card">` block on `people.html`, and point its `src`/`alt` at the file.
If a face ends up cropped in the circle, tweak `object-position` on `.member-card .avatar`
in `style.css` (or add an inline `style="object-position: center 30%"` to that one image).

Update each image's `alt` text to describe the real photo. If you swap the hero for a
brighter photo, deepen the overlay alpha in `style.css` (`.hero::before`) so the cream
title stays readable.

---

## Preview locally

Open `index.html` in a browser — all links are relative, so it works straight from the
filesystem. For a closer match to production:

```bash
python3 -m http.server
# then visit http://localhost:8000
```

## Deploy

Push to `main`. GitHub Pages publishes from the repo root (Settings → Pages → Deploy from
a branch → `main` → `/ (root)`), usually within a minute or two.

## Notes

- Fonts (Cormorant Garamond + Source Serif 4) load from Google Fonts.
- Palette is a warm "walnut on beige" scheme — no drop shadows or gradients. Keep it that
  way for the classical-academic feel.
- **CV:** `assets/Ding_Ying_CV_2026.docx`, linked from the Contact page.
  To use a PDF instead, add `assets/Ding_Ying_CV_2026.pdf` and update the `href` and
  the "(Word)" label. `tools/check.py` fails if the linked file is missing.
- **Funding** is a section on `research.html` — current/active grants only, no dollar amounts.
  Update the list as awards start and end.
- **Open positions** (the postdoc ad) is a section on `people.html` with `id="openings"`,
  linked from the Home news list and the Contact page. Remove all three when the search closes.
- The department's formal name is **Biostatistics and Health Data Science**. "University of
  Pittsburgh" is wrapped in `<span class="pitt">`, but `.pitt` is currently uncoloured
  (`color: inherit`) — change that one rule if you ever want it styled again.
- The site is fully static — no animations.
- Content still marked `<!-- TODO: -->` throughout — search the project for `TODO`.
