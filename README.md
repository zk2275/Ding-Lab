# Ding Lab — website

The website for the **Ding Lab** (Ying Ding), Department of Biostatistics,
University of Pittsburgh.

- **Live site:** https://zk2275.github.io/labing
- **Repo:** https://github.com/zk2275/labing

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

### Add a photo to the rolling gallery
See [Adding photos to the rolling gallery](#adding-photos-to-the-rolling-gallery)
— there's one rule that's easy to get wrong.

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
3. **The rolling gallery holds two identical photo sets.** Both must match exactly.
4. **Filenames are case-sensitive in production.** GitHub Pages serves from Linux;
   macOS doesn't care about case. So `Photo.JPG` referenced as `photo.jpg` works on your
   laptop and 404s on the live site. (This already happened once, with `teaching.JPG`.)

---

## Structure

```
labing/
├── index.html          Home (hero, intro, research interests, news, rolling gallery)
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
| `pittsburgh.jpg` | Home hero background, rolling gallery | Hero is set via `url()` in `style.css` (`.hero`). |
| `Ding_Ying.jpg` | Home intro portrait, People PI card | |
| `public_health.jpg` | Rolling gallery | |
| `teaching.jpg` | Teaching banner, rolling gallery | Banner is full-bleed 16:9 (`.page-banner`); natively 16:9, so no crop. |
| `School_of_Public_Health.png` | Home affiliation badge | Official Pitt School of Public Health logo (transparent PNG). Sits in the `.affiliation` block below the hero. |

Still placeholders, swap when you have real files:

- `figure-placeholder.svg` — three gallery tiles, and the four Research figures.
- `avatar-placeholder.svg` — student headshots on People (square photos, shown as circles).
- `banner-placeholder.svg`, `portrait-placeholder.svg` — unused; kept in case you want one back.

Update each image's `alt` text to describe the real photo. If you swap the hero for a
brighter photo, deepen the overlay alpha in `style.css` (`.hero::before`) so the cream
title stays readable.

### Adding photos to the rolling gallery

The strip is at the bottom of `index.html`, marked `<!-- ===== ROLLING GALLERY ===== -->`.
It has **two identical `.marquee-set` blocks** — the second is a copy that makes the loop
seamless, and is hidden from screen readers.

> **Add your `<figure>` to BOTH sets, in the same order.** If they differ, the loop visibly
> jumps. `tools/check.py` will catch it.

Tuning, in `style.css` under `.marquee-track`:

- **Speed** — the `40s`; larger is slower.
- **Direction** — `animation-direction: reverse` sends images left → right; `normal` reverses it.

It pauses on hover or keyboard focus, and stops entirely for visitors whose system asks for
reduced motion.

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
- The rolling gallery is the one deliberate piece of motion; everything else is static.
- "University of Pittsburgh" is wrapped in `<span class="pitt">` so it shows in the official
  Pitt blue (`--pitt-blue` in `style.css`). The department's formal name is
  **Biostatistics and Health Data Science**.
- Content still marked `<!-- TODO: -->` throughout — search the project for `TODO`.
