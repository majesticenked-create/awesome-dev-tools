"""Merge the per-page PDFs from build.mjs into the files a buyer downloads,
adding fillable text fields over every name / age / year line.

    python3 src/assemble.py   ->  dist/*.pdf
"""
import json
import pathlib

import fitz  # PyMuPDF

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = ROOT / "build" / "pages"
DIST = ROOT / "dist"
DIST.mkdir(exist_ok=True)

NAME = "Halloween-Handprint-Art"
OUTPUTS = {
    "color-letter": (f"1_{NAME}_COLOR_US-Letter.pdf", "Color · US Letter"),
    "color-a4": (f"2_{NAME}_COLOR_A4.pdf", "Color · A4"),
    "bw-letter": (f"3_{NAME}_INK-SAVER-COLORING_US-Letter.pdf", "Ink-saver / coloring · US Letter"),
    "bw-a4": (f"4_{NAME}_INK-SAVER-COLORING_A4.pdf", "Ink-saver / coloring · A4"),
    "guide": (f"0_START-HERE_Guide-and-Bonus-Pages.pdf", "Start Here guide + bonus pages"),
}
INK = (0.17, 0.15, 0.19)


def add_fields(page, fields, pl, prefix):
    for i, f in enumerate(fields):
        s = pl["s"]
        rect = fitz.Rect(pl["ox"] + f["x"] * s, pl["oy"] + f["y"] * s,
                         pl["ox"] + (f["x"] + f["w"]) * s, pl["oy"] + (f["y"] + f["h"]) * s)
        w = fitz.Widget()
        w.field_type = fitz.PDF_WIDGET_TYPE_TEXT
        w.field_name = f"{prefix}_{i}_{f['name']}".replace(" ", "_")
        w.field_label = f["name"]
        w.rect = rect
        w.text_font = "Helv"
        w.text_fontsize = 0  # auto-size to the box
        w.text_color = INK
        w.border_width = 0
        w.fill_color = None
        page.add_widget(w)


def main():
    manifest = json.loads((PAGES / "manifest.json").read_text())
    for key, (fname, label) in OUTPUTS.items():
        doc = fitz.open()
        for n, entry in enumerate(manifest[key], 1):
            with fitz.open(entry["file"]) as src:
                doc.insert_pdf(src)
            add_fields(doc[-1], entry["fields"], entry["pl"], f"p{n}")
        doc.set_metadata({
            "title": f"Halloween Handprint Art — {label}",
            "subject": "Printable Halloween handprint, footprint and fingerprint keepsake crafts",
            "keywords": "halloween handprint, footprint art, fingerprint craft, keepsake, printable",
            "creator": "Halloween Handprint Art",
            "producer": "Halloween Handprint Art",
        })
        out = DIST / fname
        doc.save(out, garbage=4, deflate=True)
        print(f"{fname}: {len(doc)} pages, {out.stat().st_size / 1024:.0f} KB")
        doc.close()


if __name__ == "__main__":
    main()
