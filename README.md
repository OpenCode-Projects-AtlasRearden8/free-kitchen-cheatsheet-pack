# Kitchen Cheatsheets Pack

Free printables for confident home cooking — seven warm, one-page cheatsheets
plus a getting-started sheet, ready to print at 100% scale on US Letter.
No accounts, no signups, no tracking: the build runs entirely on your machine.

## What's in the pack

| PDF (in `printables/`) | What it covers |
|---|---|
| `01-kitchen-conversions.pdf` | Spoons, cups, grams, oven temperatures |
| `02-ingredient-substitutions.pdf` | What to use when you're out of something |
| `03-grain-bean-ratios.pdf` | Water ratios, cook times, stovetop + pressure cooker |
| `04-safe-thawing-storage.pdf` | Safe thawing, the 2-hour rule, fridge & freezer times |
| `05-freezer-label-log.pdf` | A fill-in log so nothing in the freezer stays a mystery |
| `06-weekly-meal-skeleton.pdf` | Flexible dinner themes, not rigid recipes |
| `07-knife-basics.pdf` | Grip, cuts, sharpening, and safety basics |
| `08-getting-started.pdf` | A warm "start here" page with printing tips |

All final PDFs are unbranded — print and share freely.

## Building it yourself

Requirements: Python 3.10+ with `weasyprint` and `pypdf` (for tests).

```bash
pip install weasyprint pypdf pytest
python3 build.py          # renders every sheet to printables/
python3 -m pytest tests/  # verifies every PDF is valid and printable
```

`build.py` renders each `src/*.html` (sharing one stylesheet, `src/print.css`)
into `printables/*.pdf`, cleaning out stale outputs it doesn't recognize.

## Project layout

```
src/          HTML/CSS sources for every sheet (edit here)
printables/   Built, unbranded PDFs — the deliverable
build.py      One build script: src/*.html -> printables/*.pdf
tests/        Pytest suite verifying every sheet builds a valid PDF
```

## Editing notes

- Sheets are plain HTML/CSS — load any `src/*.html` in a browser to preview.
- `src/print.css` controls page size, fonts, and spacing; it is tuned so every
  sheet renders as exactly one US-Letter page (a test enforces this).
- Food-safety content follows standard FDA-based guidance for home cooks.
  These sheets are educational, not medical, dietary, or regulatory advice.

## Credits & license

Made by [Asdale Dynamics, LLC](https://dylanasdale.github.io) — the publishing
imprint behind *The Massive AI Manual* by Dylan Asdale. Plain-English guides
and practical tools, built local-first. Released under the MIT License (see
`LICENSE`; copyright (c) 2026 Asdale Dynamics, LLC).
