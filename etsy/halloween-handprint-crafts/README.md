# Halloween Handprint Art — printable Etsy product

A 30-design Halloween handprint / footprint / fingerprint keepsake bundle,
built as an improved, fully original alternative to a 12-design competitor.

**Ready-to-upload files are in [`dist/`](dist/)** and the listing copy (title,
tags, description, price) is in [`LISTING.md`](LISTING.md).

## Plan & how this beats the competitor

| | Competitor | This bundle |
|---|---|---|
| Designs | 12 | **30** (15 hand · 8 foot · 7 fingerprint) |
| Paper sizes | US Letter only | **US Letter + A4** |
| Ink-saver / coloring version | — | **Yes, every design** |
| Placement guides | — | **Faint corner guides (hidden by paint)** |
| Name / age / year | — | **Type-in PDF fields + write-in lines** |
| Extras | — | **How-to guide, visual index with paint colors, cut & glue face pieces (color + coloring), 4 mini cards** |
| Artwork & wording | — | 100% original drawings and puns (no copied art, layouts or text) |

## What's in `dist/`

| File | Pages |
|---|---|
| `0_START-HERE_Guide-and-Bonus-Pages.pdf` | 9 — cover, how-to, visual index ×2, cut & glue pieces (color + coloring), mini cards ×2, terms |
| `1_…_COLOR_US-Letter.pdf` | 30 |
| `2_…_COLOR_A4.pdf` | 30 |
| `3_…_INK-SAVER-COLORING_US-Letter.pdf` | 30 |
| `4_…_INK-SAVER-COLORING_A4.pdf` | 30 |
| `listing-images/01…10.jpg` | 10 Etsy listing images, 2400×2400 |

## Rebuilding

Everything is generated from code, so designs are easy to tweak or extend.

```bash
pip install pymupdf pillow           # PDF fields + image conversion
node src/preview.mjs [design-id ...] # PNG previews -> build/preview/
node src/build.mjs                   # render every page -> build/pages/
python3 src/assemble.py              # merge + fillable fields -> dist/*.pdf
node src/mockups.mjs                 # listing images -> build/listing/ (convert to JPG: see below)
```

JPG conversion for the listing images:

```bash
python3 -c "from PIL import Image; import glob,os; [Image.open(f).convert('RGB').save('dist/listing-images/'+os.path.basename(f)[:-4]+'.jpg',quality=90,optimize=True) for f in glob.glob('build/listing/*.png')]"
```

Uses the Playwright/Chromium install at `/opt/node-tools` (adjust the import
path in the `src/*.mjs` files if yours lives elsewhere).

### Source layout

- `src/lib.mjs` — palette (color / ink-saver modes), outlined components, hand & foot models, placement guides, paint-texture sample prints
- `src/designs*.mjs` — the 30 designs (hand A/B, foot, finger)
- `src/helpers.mjs` — shared design helpers (fingertip positions, bat wings, haunted house…)
- `src/page.mjs` — turns a design into a full page SVG
- `src/bonus.mjs` — START HERE guide + bonus pages
- `src/build.mjs`, `src/assemble.py` — PDF pipeline
- `src/mockups.mjs` — Etsy listing images

## Licenses

Fonts in `fonts/` are from Google Fonts under the SIL Open Font License 1.1
(Grandstander, Patrick Hand, Creepster, Fredoka), which allows embedding in
commercial products. All illustrations are original vector artwork drawn in
`src/`.
