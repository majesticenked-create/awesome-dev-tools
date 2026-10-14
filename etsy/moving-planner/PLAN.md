# The Calm Move: Moving Planner Plan

A plan for a printable moving planner to sell on Etsy as an instant digital download.
It is meant to beat the reference listing (etsy.com/listing/1300369738).

**Status: built.** See `dist/` for the files, `mockups/` for the listing photos and
`LISTING.md` for the title, tags and description. To rebuild:
`python3 build_planner.py && python3 make_mockups.py`.

## 1. Competitor teardown (from the listing screenshots)

The reference listing is an Etsy **Bestseller**: "Moving Planner, Instant download
US Letter", 43 to 44 pages, 1 PDF.

| They have | Their weakness | Our answer |
|---|---|---|
| 43–44 pages, Letter only | No A4, so buyers outside the US get cropped margins | Letter **and** A4 |
| Flat Canva PDF | Can't type into it, no clickable links | Fillable fields + clickable contents + bookmarks |
| Black & white, small dense text | Cramped, hard to write in | Larger rows (0.27 to 0.3 in), clean grid, soft accents |
| Box labels = room name + "Box #" (B&W) | No link between boxes, rooms and inventory | Color-coded room **codes** across labels, door signs and inventory |
| Checklists grouped by "1 month / 2 weeks" | Loose timeline, no after-move section | 8 / 6 / 4 / 2 / 1-week + moving day + first 24 h / week / month |
| Receipts as 4 boxes per page | Clunky, no totals or categories | Receipt log with category, amount, kept / claim ticks |
| "Important Dates" as 12-month list | Not tied to the move | 8-week countdown calendar |
| Home search, paint index, measurements, sell/gift/buy/donate lists, say-goodbye list | (Good ideas, so we match them) | Home search, Measurements & paint, Sell/gift/donate log, Shopping list, Saying goodbye |
| Typos in the listing images ("Places" for plates, "US Portal Service", "Please feet free") | Looks careless | Proofread, consistent copy |
| Listing photos: yellow banners, script fonts, wood background | Dated and busy | Calm sand / sage palette, page fans, clear USP text |

Our planner: **51 pages**, and it beats theirs on page count, formats and features.

## 2. Positioning

**Product name:** The Calm Move: Complete Moving Planner
**Promise:** One planner that runs the whole move, from 8 weeks out to the first
month in the new home, with a color-coded box system so nothing gets lost.

**Five differentiators (these go in photo #1 and the title):**
1. **Fillable AND printable.** Invisible form fields: type on a laptop/iPad, or
   print it and write by hand. It looks the same either way.
2. **US Letter + A4** in the same purchase.
3. **Clickable table of contents** and a "home" link on every page (works in
   GoodNotes, Notability, Xodo, Adobe).
4. **Color-coded room system.** Each room has a color and a letter code (K =
   Kitchen, B1 = Bedroom 1…). Box labels, room door signs and the box inventory
   all use the same codes, so movers know where each box goes and you know what's
   inside it.
5. **Low-ink minimalist design.** White pages, thin lines, soft color accents.
   Prints well in black and white.

## 3. Page list (51 pages, as built)

**Plan:** 1 Cover · 2 Contents (clickable) · 3 How to use · 4 Move at a glance ·
5 Home search · 6 8-week countdown

**Timeline:** 7 8 weeks · 8 6 weeks · 9 4 weeks · 10 2 weeks · 11 1 week + day before ·
12 Saying goodbye · 13 Moving day · 14 After the move

**Admin:** 15 Budget · 16 Receipt tracker · 17 Mover quotes · 18 Change of address ·
19 Utilities · 20 Important contacts

**Declutter & pack:** 21 Declutter tracker · 22 Sell, gift & donate log · 23 Packing supplies ·
24 Room key · 25 Room packing checklist · 26–28 Box inventory (78 boxes) · 29 Open-first box ·
30 Kids & pets

**Clean & settle:** 31 Move-out cleaning · 32 Move-in cleaning · 33 Walk-through report ·
34 Measurements & paint · 35 Furniture layout · 36 New home shopping list ·
37 New home & neighborhood · 38 Notes

**Labels & signs:** 39–47 Box labels (8 rooms + blank, 8 per page) · 48–49 Room door signs ·
50 Blank door signs · 51 Special labels

## 4. Design system

- **Fonts:** Caladea (serif headings, OFL-1.1) + Inter (body, OFL-1.1, converted to
  TTF for embedding). Both are licensed for commercial embedding; see `fonts/`.
- **Palette:** ink `#2F3A3A`, sage `#7A9A8A`, clay `#C8866B`, sand `#EFE7DC`,
  plus 8 soft room colors for labels.
- **Layout:** 0.5" margins (safe for home printers), one section color tab per
  part, page footer with a section name and a "contents" link.
- **Grid:** checklists are 1 item per 0.3" row. Write-in lines 0.3" high, easy
  for handwriting.

## 5. How it's built (technical)

- `build_planner.py` (Python + ReportLab) generates every page from data. This
  keeps the content editable, and Letter/A4 come out of the same source.
- Form fields: one AcroForm text field over each write-in line and a checkbox over
  each tick box. Borders and backgrounds are transparent, so the printed page looks
  exactly like the plain version.
- Internal links: the table of contents and footer links use PDF bookmarks and
  link annotations.
- `make_mockups.py` renders pages to PNG (pdftoppm) and builds the Etsy listing
  images with Pillow.

## 6. What the buyer downloads (Etsy allows 5 files, 20 MB each)

1. `The-Calm-Move-Moving-Planner-US-Letter.pdf` (fillable + hyperlinked)
2. `The-Calm-Move-Moving-Planner-A4.pdf` (fillable + hyperlinked)
3. `READ-ME-Quick-Start.pdf`: printing tips, how to type into the file, GoodNotes
   import, a note asking for a review

## 7. Listing plan

- **Price:** $8.99, launched at a 30% sale ($6.29) for the first 2 weeks to
  get the first reviews. Later, a bundle with a home-inventory or new-home
  planner at $14.99.
- **Photos (10):** hero with the 5 USPs, everything included (page grid), the
  timeline, the box system (labels + inventory + signs), fillable on a tablet,
  Letter + A4, budget + quotes, address and utilities, cleaning, "what you get".
- **Title, 13 tags, description:** in `LISTING.md`.
- **Category:** Paper & Party Supplies › Paper › Calendars & Planners (digital).
- **Video:** a 10-second page flip (optional, but it helps search ranking).

## 8. Legal / originality

- All text, layout and graphics are original. Nothing is copied from the reference
  listing.
- The fonts are OFL-1.1, so commercial embedding in a PDF is allowed.
- The license terms in the listing say personal use only and no resale.

## 9. Later variations (cheap to add because everything is generated)

- Color themes (sage, blush, navy, mono) as separate listings.
- Niche versions: Military PCS move, Moving abroad, Downsizing/seniors, College
  dorm move, Moving with kids.
- Landscape digital-planner version with tabbed sidebar for GoodNotes.
