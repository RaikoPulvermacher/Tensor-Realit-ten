#!/usr/bin/env python3
"""
Generates a PDF document from all repository content:
text files (Fliestext, Methodik) and sketch images (*.png).

Usage:
    python3 generate_pdf.py
Output:
    Pulvermacher-Fundament-der-Natur.pdf
"""

import os
from fpdf import FPDF, XPos, YPos
from PIL import Image

REPO_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(REPO_DIR, "Pulvermacher-Fundament-der-Natur.pdf")

def _find_font(name: str) -> str:
    """Return the path of a Liberation Sans TTF variant, searching common locations."""
    candidates = [
        os.path.join("/usr/share/fonts/truetype/liberation", name),
        os.path.join("/usr/share/fonts/liberation", name),
        os.path.join(os.path.expanduser("~"), ".fonts", name),
        os.path.join(REPO_DIR, name),
    ]
    for path in candidates:
        if os.path.isfile(path):
            return path
    raise FileNotFoundError(
        f"Font file '{name}' not found. "
        "Please install the Liberation fonts package "
        "(e.g. 'sudo apt install fonts-liberation' on Debian/Ubuntu)."
    )


FONT_REGULAR    = _find_font("LiberationSans-Regular.ttf")
FONT_BOLD       = _find_font("LiberationSans-Bold.ttf")
FONT_ITALIC     = _find_font("LiberationSans-Italic.ttf")
FONT_BOLDITALIC = _find_font("LiberationSans-BoldItalic.ttf")

SKETCHES = [
    ("Superposition.png",         "Superposition"),
    ("Materie.png",               "Materie"),
    ("Gravitation.png",           "Gravitation"),
    ("Zeit.png",                  "Zeit"),
    ("Tensor der Realitäten.png", "Tensor der Realitäten"),
    ("Atome beschreibung.png",    "Atome \u2013 Beschreibung"),
    ("Energie flucht.png",        "Energie \u2013 Flucht"),
    ("Neutron entwicklung.png",   "Neutron \u2013 Entwicklung"),
]

LMARGIN = 15
RMARGIN = 15
TMARGIN = 15


class PDF(FPDF):
    def header(self):
        pass  # no automatic header

    def footer(self):
        self.set_y(-12)
        self.set_font("Sans", "I", 8)
        self.set_text_color(130, 130, 130)
        self.cell(
            0, 10,
            f"Raiko Pulvermacher \u2013 Seite {self.page_no()}",
            align="C",
        )
        self.set_text_color(0, 0, 0)


def _mcell(pdf: PDF, h: float, text: str, font: str = "Sans", style: str = "", size: int = 11) -> None:
    """Helper: reset x to left margin, set font, print multi_cell."""
    pdf.set_x(pdf.l_margin)
    pdf.set_font(font, style, size)
    effective_w = pdf.w - pdf.l_margin - pdf.r_margin
    pdf.multi_cell(effective_w, h, text)


def add_text_section(pdf: PDF, title: str, filepath: str) -> None:
    pdf.add_page()
    _mcell(pdf, 10, title, style="B", size=16)
    pdf.ln(4)
    with open(filepath, encoding="utf-8") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if line.startswith("# "):
                pdf.ln(2)
                _mcell(pdf, 8, line[2:], style="B", size=14)
            elif line.startswith("## "):
                pdf.ln(2)
                _mcell(pdf, 7, line[3:], style="B", size=12)
            elif line.startswith("### "):
                pdf.ln(2)
                _mcell(pdf, 7, line[4:], style="BI", size=11)
            elif line.strip() in ("---", ""):
                pdf.ln(3)
            else:
                _mcell(pdf, 6, line, style="", size=11)


def add_image_page(pdf: PDF, filename: str, caption: str) -> None:
    filepath = os.path.join(REPO_DIR, filename)
    if not os.path.exists(filepath):
        print(f"  Skipping missing file: {filename}")
        return

    pdf.add_page()
    effective_w = pdf.w - pdf.l_margin - pdf.r_margin
    pdf.set_x(pdf.l_margin)
    pdf.set_font("Sans", "B", 13)
    pdf.multi_cell(effective_w, 10, caption, align="C")
    pdf.ln(2)

    with Image.open(filepath) as img:
        img_w, img_h = img.size

    # Fit image within printable area
    max_w = pdf.w - pdf.l_margin - pdf.r_margin
    max_h = pdf.h - pdf.t_margin - 25  # leave room for caption + footer
    scale = min(max_w / img_w, max_h / img_h)
    draw_w = img_w * scale
    draw_h = img_h * scale
    x = (pdf.w - draw_w) / 2
    pdf.image(filepath, x=x, y=pdf.get_y(), w=draw_w, h=draw_h)


def build_pdf() -> None:
    pdf = PDF(orientation="P", unit="mm", format="A4")
    pdf.add_font("Sans", "",   FONT_REGULAR)
    pdf.add_font("Sans", "B",  FONT_BOLD)
    pdf.add_font("Sans", "I",  FONT_ITALIC)
    pdf.add_font("Sans", "BI", FONT_BOLDITALIC)
    pdf.set_margins(LMARGIN, TMARGIN, RMARGIN)
    pdf.set_auto_page_break(auto=True, margin=15)

    # ── Title page ───────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.ln(40)
    effective_w = pdf.w - LMARGIN - RMARGIN

    pdf.set_x(LMARGIN)
    pdf.set_font("Sans", "B", 24)
    pdf.multi_cell(effective_w, 12, "Pulvermacher", align="C")

    pdf.set_x(LMARGIN)
    pdf.set_font("Sans", "B", 18)
    pdf.multi_cell(effective_w, 10, "Fundament der Natur", align="C")

    pdf.ln(6)
    pdf.set_x(LMARGIN)
    pdf.set_font("Sans", "I", 13)
    pdf.multi_cell(effective_w, 8, "Eine Bottom-Up-Beschreibung der Realit\u00e4t", align="C")

    pdf.ln(16)
    pdf.set_x(LMARGIN)
    pdf.set_font("Sans", "", 11)
    pdf.multi_cell(effective_w, 7, "Raiko Pulvermacher", align="C")

    pdf.ln(4)
    pdf.set_text_color(100, 100, 100)
    pdf.set_font("Sans", "I", 9)
    pdf.set_x(LMARGIN)
    pdf.multi_cell(effective_w, 6, "https://orcid.org/0009-0003-9431-1001", align="C")
    pdf.set_x(LMARGIN)
    pdf.multi_cell(effective_w, 6, "https://osf.io/py42t/", align="C")
    pdf.set_text_color(0, 0, 0)

    # ── Text sections ────────────────────────────────────────────────────────
    add_text_section(pdf, "Flie\u00dftext", os.path.join(REPO_DIR, "Fliestext"))
    add_text_section(pdf, "Methodik",    os.path.join(REPO_DIR, "Methodik"))

    # ── Sketch images ────────────────────────────────────────────────────────
    for filename, caption in SKETCHES:
        print(f"  Adding image: {filename}")
        add_image_page(pdf, filename, caption)

    pdf.output(OUTPUT_FILE)
    print(f"\nPDF saved: {OUTPUT_FILE}")


if __name__ == "__main__":
    build_pdf()

