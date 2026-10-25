"""Tests for the Kitchen Cheatsheets pack.

Run: python -m pytest tests/ -v
(or: python tests/test_build.py)

Each test renders PDFs fresh via build.build() into a temp directory, so the
pack itself is always verified end-to-end, not just the last committed files.
Every sheet must produce a valid, loadable PDF with real, extractable text.
"""

import io
import sys
import unittest
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from build import SHEETS, ROOT, SRC, OUT, build  # noqa: E402


class PackSourcesTestCase(unittest.TestCase):
    """Every sheet declared in build.py has real HTML/CSS sources."""

    def test_documented_sheets_build_to_pdfs(self):
        paths = build(verbose=False)
        self.assertEqual(len(paths), len(SHEETS))
        for path in paths:
            self.assertTrue(path.is_file(), f"missing PDF: {path}")

    def test_all_sources_have_stylesheets(self):
        for src_name, _ in SHEETS:
            html = (SRC / src_name).read_text(encoding="utf-8")
            self.assertIn('href="print.css"', html, src_name)

    def test_shared_stylesheet_exists(self):
        css = (SRC / "print.css").read_text(encoding="utf-8")
        self.assertIn("@page", css)
        self.assertIn("size: Letter", css)


def _read_pdf(path: Path) -> PdfReader:
    data = path.read_bytes()
    self_bytes_check = PdfReader(io.BytesIO(data))
    self_bytes_check.metadata  # forces full parse
    return self_bytes_check


class PdfValidityTestCase(unittest.TestCase):
    """Every sheet builds a valid, openable PDF with extractable content."""

    def setUp(self):
        self.paths = build(verbose=False)

    def _by_src(self, src_name: str) -> Path:
        idx = [s for s, _ in SHEETS].index(src_name)
        return self.paths[idx]

    def test_every_pdf_is_valid_and_has_pages(self):
        for path in self.paths:
            reader = _read_pdf(path)
            self.assertGreaterEqual(len(reader.pages), 1, path.name)

    def test_every_sheet_is_a_one_pager(self):
        """These are fridge cheatsheets — each must fit one printed page."""
        for path in self.paths:
            reader = PdfReader(str(path))
            self.assertEqual(len(reader.pages), 1, f"{path.name} spilled over")

    def test_every_pdf_is_letter_portrait(self):
        for path in self.paths:
            reader = PdfReader(str(path))
            box = reader.pages[0].mediabox
            width, height = float(box.width), float(box.height)
            self.assertAlmostEqual(width, 612, delta=2, msg=path.name)  # 8.5in
            self.assertGreater(height, width, msg=path.name)

    def test_every_pdf_has_extractable_text(self):
        for path in self.paths:
            reader = PdfReader(str(path))
            text = " ".join(page.extract_text() or "" for page in reader.pages)
            self.assertGreater(len(text.strip()), 80, f"no text in {path.name}")

    def test_each_sheet_covers_its_topic(self):
        expectations = {
            "measuring-conversions.html": ["Tablespoons", "Oven Temperatures"],
            "ingredient-substitutions.html": ["Use instead", "Eggs"],
            "grain-bean-ratios.html": ["Water", "Simmer time", "Pressure"],
            "thawing-storage.html": ["Cold water", "2-hour rule", "165"],
            "freezer-label-log.html": ["Date frozen", "Use by", "Label"],
            "weekly-meal-skeleton.html": ["Theme", "Mon", "Sun"],
            "knife-basics.html": ["Grip", "Mince", "Sharp"],
            "getting-started.html": ["Welcome", "Printing tips"],
        }
        for src_name, phrases in expectations.items():
            path = self._by_src(src_name)
            reader = PdfReader(str(path))
            text = " ".join(page.extract_text() or "" for page in reader.pages)
            lowered = text.lower()
            for phrase in phrases:
                self.assertIn(phrase.lower(), lowered, f"{path.name}: expected '{phrase}'")

    def test_pdfs_are_unbranded(self):
        """Final PDFs must not carry brand names (warm, generic pages only)."""
        for path in self.paths:
            reader = PdfReader(str(path))
            text = " ".join(page.extract_text() or "" for page in reader.pages)
            lowered = text.lower()
            for brand in ("asdle", "dylan", "massive ai manual"):
                self.assertNotIn(brand, lowered, f"{path.name} mentions '{brand}'")

    def test_getting_started_sheet_exists_in_pack(self):
        path = self._by_src("getting-started.html")
        reader = PdfReader(str(path))
        text = reader.pages[0].extract_text() or ""
        self.assertIn("printing tips", text.lower())

    def test_clean_removes_stale_pdfs(self):
        stale = OUT / "00-stale-should-vanish.pdf"
        stale.write_bytes(b"not a real pdf")
        build(verbose=False)
        self.assertFalse(stale.exists(), "clean() should drop orphan PDFs")


if __name__ == "__main__":
    unittest.main()
