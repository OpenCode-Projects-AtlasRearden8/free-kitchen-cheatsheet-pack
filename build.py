#!/usr/bin/env python3
"""Build the Kitchen Cheatsheets pack: HTML/CSS sources -> print-ready PDFs.

Local build only. No accounts, no signups, no network. Output lands in
printables/ as unbranded US-Letter PDFs ready to print at 100% scale.
"""

import sys
from pathlib import Path

from weasyprint import HTML

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
OUT = ROOT / "printables"

# (source file, output file) pairs, in pack order.
SHEETS = [
    ("measuring-conversions.html", "01-kitchen-conversions.pdf"),
    ("ingredient-substitutions.html", "02-ingredient-substitutions.pdf"),
    ("grain-bean-ratios.html", "03-grain-bean-ratios.pdf"),
    ("thawing-storage.html", "04-safe-thawing-storage.pdf"),
    ("freezer-label-log.html", "05-freezer-label-log.pdf"),
    ("weekly-meal-skeleton.html", "06-weekly-meal-skeleton.pdf"),
    ("knife-basics.html", "07-knife-basics.pdf"),
    ("getting-started.html", "08-getting-started.pdf"),
]


def build(verbose: bool = True) -> list[Path]:
    """Render every sheet to PDF. Returns the list of output paths."""
    OUT.mkdir(exist_ok=True)
    clean(verbose=verbose)
    built: list[Path] = []
    for src_name, out_name in SHEETS:
        src_path = SRC / src_name
        out_path = OUT / out_name
        if not src_path.is_file():
            raise FileNotFoundError(f"missing source sheet: {src_path}")
        html = HTML(filename=str(src_path), base_url=str(SRC))
        html.write_pdf(target=str(out_path))
        built.append(out_path)
        if verbose:
            print(f"  built {out_path.relative_to(ROOT)}")
    return built


def clean(verbose: bool = True) -> None:
    """Remove any PDFs that no longer have a matching source sheet."""
    wanted = {out_name for _, out_name in SHEETS}
    if OUT.is_dir():
        for pdf in OUT.glob("*.pdf"):
            if pdf.name not in wanted:
                pdf.unlink()
                if verbose:
                    print(f"  removed stale {pdf.relative_to(ROOT)}")


def main() -> int:
    print("Warm up the oven... welcome to the Kitchen Cheatsheets build.")
    print("Building your print-ready pack (local only, nothing is sent anywhere).")
    built = build()
    print(f"\nDone! {len(built)} sheets in {OUT.relative_to(ROOT)}:")
    for path in built:
        size_kb = path.stat().st_size / 1024
        print(f"  {path.name}  ({size_kb:.0f} KB)")
    print("\nPrint tip: US Letter, 100% scale (Actual Size), portrait.")
    print("Cook warmly, friend.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
