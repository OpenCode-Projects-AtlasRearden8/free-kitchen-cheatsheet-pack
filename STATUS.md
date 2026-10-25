# STATUS — Kitchen Cheatsheets Pack

**Date:** 2026-10-25 · **Status:** Done and verified · **License:** MIT (Asdale Dynamics, LLC)

## What was built

A free, unbranded pack of printable kitchen cheatsheets for confident home
cooking, produced by a single local build script with a warm getting-started
page. No accounts, signups, network calls, secrets, or personal data anywhere.

Eight one-page US-Letter PDFs in `printables/` (in suggested print order):

1. `01-kitchen-conversions.pdf` — spoons/cups/grams, weight↔volume for common ingredients, °F→°C oven table
2. `02-ingredient-substitutions.pdf` — dairy & fats, egg swaps, pantry baking math, herbs/flavor, meat & grains
3. `03-grain-bean-ratios.pdf` — stovetop water ratios and cook times for grains, soaked/unsoaked beans, plus pressure-cooker times; includes kidney-bean boil-safety and fava/G6PD note
4. `04-safe-thawing-storage.pdf` — three safe thawing methods, danger zone / 2-hour rule, fridge and freezer storage times (FDA-based guidance)
5. `05-freezer-label-log.pdf` — the 4 W's of labeling plus a fill-in log table
6. `06-weekly-meal-skeleton.pdf` — theme-based weekly planner (ADHD-friendly "themes, not recipes") with a printable write-in table
7. `07-knife-basics.pdf` — pinch grip, claw hand, cuts, onion walk-through, sharpness/care/safety
8. `08-getting-started.pdf` — warm "start here" page with how-to-use and printing tips

Sources live in `src/` (HTML per sheet + one shared `src/print.css` tuned so
every sheet fits exactly one page). `build.py` is the one build script.

## How to run it

```bash
pip install weasyprint pypdf pytest
python3 build.py            # rebuild all PDFs into printables/ (local only)
python3 -m pytest tests/    # verify every sheet builds/covers its topic
```

Print at 100% scale ("Actual Size"), US Letter, portrait.

## Verification results

- `python3 build.py` — exits 0, builds all 8 PDFs (~16–25 KB each), removes stale outputs.
- `python3 -m pytest tests/` — **11/11 passed**. Tests verify:
  - every declared sheet builds to a real file (sources + shared CSS present)
  - every PDF parses with pypdf, is Letter-portrait (612×792 pt), and has extractable text
  - each PDF is exactly **one page** (one-pager guarantee)
  - topic keywords found in each sheet (e.g. "Simmer time", "2-hour rule", "Date frozen", "Grip")
  - PDFs are **unbranded** (no "Asdale", "Dylan", "Massive AI Manual" in output)
  - stale/orphan PDFs in `printables/` are removed by build

## Known gaps

- Grain/bean ratios use one default soak-and-simmer flow; high-altitude, rice-cooker, and no-knead bread ratios aren't covered.
- Storage times mirror FDA guidance but don't cover canned goods, produce, oils, or eggs-graded-by-country variations.
- Substitution table is a starter list; no gluten-free or dairy-free baking swaps yet.
- No duotone/grayscale preview assets; the warm cream palette prints fine on mono but a dedicated B&W theme could look crisper.
- PDFs are not screen-reader-optimized tagged PDFs (WeasyPrint output is untagged).

## Housekeeping

- Git initialized; single commit contains sources, build, tests, docs, `LICENSE`
  (exact line: `Copyright (c) 2026 Asdale Dynamics, LLC`), and built PDFs.
- Nothing was pushed or published anywhere; no remote configured.
