"""Render planner pages and compose Etsy listing images (3000x2250, 4:3).

Usage:  python3 make_mockups.py      (run build_planner.py first)
"""
import os
import subprocess
import tempfile
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from pypdf import PdfReader, PdfWriter

HERE = os.path.dirname(os.path.abspath(__file__))
PDF = os.path.join(HERE, "dist", "The-Calm-Move-Moving-Planner-US-Letter.pdf")
PDF_A4 = os.path.join(HERE, "dist", "The-Calm-Move-Moving-Planner-A4.pdf")
OUT = os.path.join(HERE, "mockups")
MARKET = "etsy"  # or "creative-market": changes the marketplace wording on image 10
F = os.path.join(HERE, "fonts")
W, H = 3000, 2250

SAND = (244, 239, 231)
CREAM = (250, 247, 242)
INK = (47, 58, 58)
MUTED = (107, 119, 116)
SAGE = (111, 143, 127)
CLAY = (196, 127, 98)
WHITE = (255, 255, 255)


def font(name, size):
    return ImageFont.truetype(os.path.join(F, name), size)


SERIF = lambda s: font("Caladea-Regular.ttf", s)
SERIF_B = lambda s: font("Caladea-Bold.ttf", s)
SERIF_I = lambda s: font("Caladea-Italic.ttf", s)
SANS = lambda s: font("Inter-Regular.ttf", s)
SANS_M = lambda s: font("Inter-Medium.ttf", s)
SANS_SB = lambda s: font("Inter-SemiBold.ttf", s)
SANS_B = lambda s: font("Inter-Bold.ttf", s)

TMP = tempfile.mkdtemp()
_cache = {}


def page_img(n, pdf=None, dpi=170):
    pdf = pdf or PDF
    key = (n, pdf, dpi)
    if key not in _cache:
        base = os.path.join(TMP, f"{len(_cache)}-{os.path.basename(pdf)}-{dpi}-{n}")
        subprocess.run(["pdftoppm", "-r", str(dpi), "-png", "-singlefile", "-f", str(n), "-l", str(n), pdf, base],
                       check=True)
        _cache[key] = Image.open(base + ".png").convert("RGB")
    return _cache[key]


def page_key(pdf=None):
    """Map bookmark titles -> 1-based page numbers so mockups survive page reordering."""
    r = PdfReader(pdf or PDF)
    return {o.title: r.get_destination_page_number(o) + 1 for o in r.outline}


def canvas(bg=SAND):
    return Image.new("RGB", (W, H), bg)


def paste_page(img, page, x, y, w, angle=0, shadow=True, border=False):
    p = page.resize((w, int(page.height * w / page.width)), Image.LANCZOS)
    if border:
        d = ImageDraw.Draw(p)
        d.rectangle([0, 0, p.width - 1, p.height - 1], outline=(225, 228, 226), width=2)
    if angle:
        p = p.convert("RGBA").rotate(angle, expand=True, resample=Image.BICUBIC)
    if shadow:
        mask = p.split()[-1] if p.mode == "RGBA" else Image.new("L", p.size, 255)
        sh = Image.new("RGBA", (p.width + 120, p.height + 120), (0, 0, 0, 0))
        sm = Image.new("L", sh.size, 0)
        sm.paste(mask, (60, 60))
        sm = sm.filter(ImageFilter.GaussianBlur(28)).point(lambda v: int(v * 0.28))
        sh.putalpha(sm)
        img.paste((40, 40, 30), (x - 60 + 10, y - 60 + 22), sh)
    if p.mode == "RGBA":
        img.paste(p, (x, y), p)
    else:
        img.paste(p, (x, y))
    return p.size


def text_c(d, cx, y, s, f, fill=INK):
    w = d.textlength(s, font=f)
    d.text((cx - w / 2, y), s, font=f, fill=fill)


def caps(d, x, y, s, f, fill=MUTED, spacing=6, center=False):
    s = s.upper()
    total = sum(d.textlength(ch, font=f) + spacing for ch in s) - spacing
    if center:
        x -= total / 2
    for ch in s:
        d.text((x, y), ch, font=f, fill=fill)
        x += d.textlength(ch, font=f) + spacing


def pill(d, x, y, s, f, bg=WHITE, fg=INK, padx=34, h=84):
    w = d.textlength(s, font=f) + 2 * padx
    d.rounded_rectangle([x, y, x + w, y + h], radius=h // 2, fill=bg)
    bb = d.textbbox((0, 0), s, font=f)
    d.text((x + padx, y + (h - (bb[3] - bb[1])) / 2 - bb[1]), s, font=f, fill=fg)
    return w


def header(img, kicker, title, sub=None, y=120):
    d = ImageDraw.Draw(img)
    caps(d, W / 2, y, kicker, SANS_SB(40), SAGE, 8, center=True)
    text_c(d, W / 2, y + 70, title, SERIF(150))
    if sub:
        text_c(d, W / 2, y + 250, sub, SERIF_I(64), MUTED)
    return d


SHOP = "CropUp Creative"


def save(img, name):
    d = ImageDraw.Draw(img)
    caps(d, W / 2, H - 110, SHOP, SANS_SB(38), MUTED, 10, center=True)
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, name)
    img.save(path, "JPEG", quality=90, optimize=True)
    print(path)


def filled_sample():
    """Copy of the planner with a few fields filled, for the 'fillable' mockup."""
    r = PdfReader(PDF)
    w = PdfWriter(clone_from=r)
    pk = page_key()
    glance = w.pages[pk["Move at a glance"] - 1]
    tx = [a.get_object()["/T"] for a in glance["/Annots"] if a.get_object().get("/FT") == "/Tx"]
    vals = ["12 Oak Street", "Apartment 4B", "Portland, OR 97201", "June 28, 10 am",
            "48 Maple Avenue", "", "Denver, CO 80203", "June 30, 2 pm",
            "Sat, June 29", "June 30", "8:00 am", "June 30",
            "June 29", "June 28", "June 27", "July 8",
            "Blue Bird Movers", "(555) 014-2290", "BB-20931", "8 to 9 am", "Marcus", "2,450",
            "6,000", "5,200", "",
            "Keep the kids' routine steady", "Sell the old sofa before we go", "Wi-Fi working on day one"]
    w.update_page_form_field_values(glance, {n: v for n, v in zip(tx, vals) if v}, auto_regenerate=False)
    w.set_need_appearances_writer(True)
    out = os.path.join(TMP, "filled.pdf")
    w.write(out)
    return out


# ---------------------------------------------------------------- images
def soft_background(top, bottom, blobs):
    """Vertical gradient with large blurred color blobs."""
    grad = Image.new("RGB", (1, H))
    for yy in range(H):
        t = yy / (H - 1)
        grad.putpixel((0, yy), tuple(int(a + (b - a) * t) for a, b in zip(top, bottom)))
    img = grad.resize((W, H))
    for cx, cy, r, col in blobs:
        # blur a mask rather than an RGBA layer, so no dark fringes bleed in
        mask = Image.new("L", (W, H), 0)
        ImageDraw.Draw(mask).ellipse([cx - r, cy - r, cx + r, cy + r], fill=col[3])
        mask = mask.filter(ImageFilter.GaussianBlur(160))
        img.paste(Image.new("RGB", (W, H), col[:3]), (0, 0), mask)
    return img


def sticker(w, h, color, title, sub, title_font, sub_font):
    """A cut-out label with a white margin, like the ones in the planner."""
    t = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(t)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=34, fill=WHITE)
    d.rounded_rectangle([18, 18, w - 19, h - 19], radius=24, fill=color)
    tw = d.textlength(title, font=title_font)
    tb = d.textbbox((0, 0), title, font=title_font)
    th = tb[3] - tb[1]
    gap = 18 if sub else 0
    sb = d.textbbox((0, 0), sub, font=sub_font) if sub else (0, 0, 0, 0)
    total = th + gap + (sb[3] - sb[1])
    y0 = (h - total) / 2 - tb[1]
    d.text(((w - tw) / 2, y0), title, font=title_font, fill=INK)
    if sub:
        sw = d.textlength(sub, font=sub_font)
        d.text(((w - sw) / 2, y0 + tb[1] + th + gap - sb[1]), sub, font=sub_font, fill=INK)
    return t


def box_label_sticker(w, h, color, code, room, note):
    t = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(t)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=30, fill=WHITE)
    d.rounded_rectangle([20, 20, w - 21, 150], radius=20, fill=color)
    d.text((48, 26), code, font=SERIF_B(110), fill=INK)
    rw = d.textlength(room, font=SANS_B(40))
    d.text((w - 48 - rw, 66), room, font=SANS_B(40), fill=INK)
    d.text((48, 190), "BOX #", font=SANS_SB(30), fill=MUTED)
    d.text((170, 172), "07", font=SERIF_I(64), fill=INK)
    d.line([160, 246, w - 48, 246], fill=(201, 207, 204), width=3)
    d.text((48, 270), note, font=SERIF_I(56), fill=INK)
    d.line([48, 342, w - 48, 342], fill=(201, 207, 204), width=3)
    return t


def img1_hero(pk):
    """Square hero (3000x3000) so Etsy's square thumbnail crop shows everything."""
    global W, H
    saved = (W, H)
    W, H = 3000, 3000
    try:
        _hero(pk)
    finally:
        W, H = saved


def _hero(pk):
    oy = 250
    img = soft_background((250, 246, 240), (245, 236, 226), [
        (2450, 420, 820, (214, 230, 220, 255)),
        (2100, 2750, 760, (247, 221, 207, 255)),
        (420, 2700, 560, (246, 234, 206, 200)),
    ])
    d = ImageDraw.Draw(img)
    # ---- copy (left)
    x = 260
    caps(d, x + 4, 330 + oy, "Printable + fillable", SANS_SB(52), SAGE, 10)
    d.text((x - 8, 400 + oy), "Moving", font=SERIF(300), fill=INK)
    d.text((x - 8, 690 + oy), "Planner", font=SERIF(300), fill=INK)
    d.text((x + 4, 1035 + oy), "The Calm Move", font=SERIF_I(108), fill=CLAY)
    y = 1250 + oy
    for s, col in [("51 pages", CLAY), ("Fillable + printable", SAGE), ("US Letter + A4", (184, 149, 74)),
                   ("Color-coded box labels", (111, 136, 160))]:
        f = SANS_SB(52)
        w = d.textlength(s, font=f) + 130
        d.rounded_rectangle([x, y, x + w, y + 112], radius=56, fill=WHITE)
        d.ellipse([x + 38, y + 41, x + 68, y + 71], fill=col)
        d.text((x + 90, y + 26), s, font=f, fill=INK)
        y += 140
    # room color swatches: the box system at a glance
    y += 60
    caps(d, x + 4, y, "8 color-coded rooms", SANS_SB(40), MUTED, 8)
    y += 70
    sw = 112
    for i, (code, col) in enumerate([("K", "#E9B49E"), ("L", "#A9C5B2"), ("D", "#EBD394"), ("B1", "#A9C0D8"),
                                     ("B2", "#CBB8D8"), ("BA", "#9ED2CD"), ("O", "#D9C4A7"), ("G", "#C2C3BA")]):
        sx = x + i * (sw + 14)
        d.rounded_rectangle([sx, y, sx + sw, y + sw], radius=22, fill=col)
        f = SERIF_B(54 if len(code) == 1 else 44)
        tw = d.textlength(code, font=f)
        bb = d.textbbox((0, 0), code, font=f)
        d.text((sx + (sw - tw) / 2, y + (sw - (bb[3] - bb[1])) / 2 - bb[1]), code, font=f, fill=INK)
    # ---- composition (right)
    paste_page(img, page_img(pk["Room door signs 1"]), 1300, 380 + oy, 840, angle=9)
    paste_page(img, page_img(pk["Special labels"]), 1990, 300 + oy, 770, angle=-8)
    paste_page(img, page_img(1, dpi=220), 1450, 340 + oy, 1060)
    paste_page(img, sticker(560, 320, (233, 180, 158), "FRAGILE", "Handle with care", SANS_B(86), SANS(40)),
               1260, 1720 + oy, 560, angle=10)
    paste_page(img, sticker(560, 320, (169, 197, 178), "OPEN FIRST", "Essentials inside", SANS_B(76), SANS(40)),
               2290, 1680 + oy, 560, angle=-9)
    paste_page(img, box_label_sticker(680, 460, (233, 180, 158), "K", "KITCHEN", "Pots & pans"),
               1700, 1930 + oy, 680, angle=-3)
    d = ImageDraw.Draw(img)
    cx, cy, r = 2500, 400 + oy, 170
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=CLAY)
    text_c(d, cx, cy - 128, "51", SERIF_B(160), WHITE)
    caps(d, cx, cy + 56, "pages", SANS_SB(38), WHITE, 8, center=True)
    save(img, "01-hero.jpg")


def img2_inside(pk):
    img = canvas(CREAM)
    header(img, "What's inside", "Everything for your move, in one place")
    pages = [pk[t] for t in ["Move at a glance", "Home search", "8-week countdown", "8 weeks before",
                             "Moving day", "After the move", "Moving budget", "Receipt tracker",
                             "Mover quotes", "Change of address", "Utilities", "Room key (codes & colors)",
                             "Box inventory 1 to 26", "Open-first box", "Kids & pets", "Move-out cleaning",
                             "Walk-through report", "Measurements & paint", "Box labels: Bedroom 1",
                             "Room door signs 1", "Special labels"]]
    cols, tw = 7, 340
    gap = (W - 2 * 150 - cols * tw) / (cols - 1)
    for i, n in enumerate(pages):
        r, c = divmod(i, cols)
        paste_page(img, page_img(n, dpi=80), int(150 + c * (tw + gap)), 520 + r * 560, tw, border=True)
    save(img, "02-whats-inside.jpg")


def img3_system(pk):
    img = canvas()
    d = header(img, "The color-coded box system", "Know what's in every box")
    items = [("Room key", "1  Give each room a code & color", pk["Room key (codes & colors)"]),
             ("Labels", "2  Label & number every box", pk["Box labels: Kitchen"]),
             ("Inventory", "3  Log what's inside", pk["Box inventory 1 to 26"]),
             ("Signs", "4  Tape signs on the new doors", pk["Room door signs 1"])]
    tw = 620
    gap = (W - 2 * 130 - 4 * tw) / 3
    for i, (_, cap, n) in enumerate(items):
        x = int(130 + i * (tw + gap))
        paste_page(img, page_img(n, dpi=120), x, 560, tw)
        d = ImageDraw.Draw(img)
        text_c(d, x + tw / 2, 1440, cap.split("  ")[0], SERIF_B(90), CLAY)
        text_c(d, x + tw / 2, 1560, cap.split("  ")[1], SANS_M(44), INK)
    text_c(d, W / 2, 1820, "Movers match the label color to the door. Boxes go straight to the right room.",
           SERIF_I(60), MUTED)
    save(img, "03-box-system.jpg")


def img4_timeline(pk):
    img = canvas(CREAM)
    header(img, "Week-by-week timeline", "Always know what to do next",
           "8 weeks out, moving day, and your first month after")
    ns = [pk[t] for t in ["8 weeks before", "4 weeks before", "1 week + day before", "Moving day", "After the move"]]
    tw = 820
    step = (W - 2 * 90 - tw) / 4
    for i, n in enumerate(ns):
        paste_page(img, page_img(n, dpi=140), int(90 + i * step), 640 + (i % 2) * 70, tw)
    save(img, "04-timeline.jpg")


def img5_fillable(pk):
    img = canvas()
    d = ImageDraw.Draw(img)
    filled = filled_sample()
    # tablet frame
    tx, ty, tw = 1450, 200, 1300
    pg = page_img(pk["Move at a glance"], pdf=filled, dpi=200)
    ph = int(pg.height * tw / pg.width)
    d.rounded_rectangle([tx - 70, ty - 70, tx + tw + 70, ty + ph + 70], radius=90, fill=(38, 42, 44))
    d.rounded_rectangle([tx - 4, ty - 4, tx + tw + 4, ty + ph + 4], radius=8, fill=(20, 20, 20))
    paste_page(img, pg, tx, ty, tw, shadow=False)
    d = ImageDraw.Draw(img)
    x = 180
    caps(d, x, 420, "Fillable PDF", SANS_SB(46), SAGE, 9)
    d.text((x, 500), "Type it.", font=SERIF(170), fill=INK)
    d.text((x, 690), "Or print it.", font=SERIF(170), fill=INK)
    y = 1000
    for s in ["Click any line to type, any box to tick", "Works in Adobe Reader, Preview, Xodo",
              "Import into GoodNotes or Notability", "Prints clean: no form boxes on paper"]:
        d.ellipse([x, y + 14, x + 26, y + 40], fill=CLAY)
        d.text((x + 52, y), s, font=SANS_M(50), fill=INK)
        y += 100
    save(img, "05-fillable.jpg")


def img6_admin(pk):
    img = canvas(CREAM)
    header(img, "Admin, sorted", "Budget, quotes & addresses", "Every number and phone call in one place")
    ns = [pk[t] for t in ["Moving budget", "Mover quotes", "Change of address", "Utilities"]]
    tw = 860
    step = (W - 2 * 110 - tw) / 3
    for i, n in enumerate(ns):
        paste_page(img, page_img(n, dpi=150), int(110 + i * step), 660 + (i % 2) * 60, tw)
    save(img, "06-admin.jpg")


def img7_settle(pk):
    img = canvas()
    header(img, "Clean & settle", "Get your deposit back", "Move-out / move-in cleaning, walk-through report, layout")
    ns = [pk[t] for t in ["Move-out cleaning", "Walk-through report", "Furniture layout", "New home & neighborhood"]]
    tw = 860
    step = (W - 2 * 110 - tw) / 3
    for i, n in enumerate(ns):
        paste_page(img, page_img(n, dpi=150), int(110 + i * step), 660 + (i % 2) * 60, tw)
    save(img, "07-clean-settle.jpg")


def img8_sizes(pk):
    img = canvas(CREAM)
    d = header(img, "Two sizes included", "US Letter  +  A4", "Print at home or at any copy shop, anywhere in the world")
    a = page_img(1, dpi=120)
    b = page_img(1, pdf=PDF_A4, dpi=120)
    paste_page(img, a, 640, 760, 760)
    paste_page(img, b, 1600, 735, 738)
    d = ImageDraw.Draw(img)
    text_c(d, 1020, 1830 + 30, "US Letter  8.5 x 11 in", SANS_M(50))
    text_c(d, 1969, 1830 + 30, "A4  210 x 297 mm", SANS_M(50))
    save(img, "08-sizes.jpg")


def img9_contents(pk):
    img = canvas()
    d = header(img, "51 pages", "What's included")
    left = ["How to use + clickable contents", "Move at a glance", "Home search comparison", "8-week countdown calendar",
            "8 / 6 / 4 / 2 / 1-week checklists", "Saying goodbye list", "Moving day schedule", "After the move",
            "Moving budget", "Receipt tracker", "Mover quote comparison", "Change of address", "Utilities"]
    right = ["Important contacts", "Declutter tracker", "Sell, gift & donate log", "Packing supplies + box estimate",
             "Room key (codes & colors)", "Room packing checklist", "Box inventory (78 boxes)", "Open-first box",
             "Kids & pets", "Move-out & move-in cleaning", "Walk-through report", "Measurements & paint index",
             "Furniture layout grid"]
    extra = ["New home shopping list", "New neighborhood info", "72 color box labels (9 sets)",
             "12 room door signs", "12 special labels (Fragile, Open first...)"]
    cols = [left, right, extra]
    xs = [200, 1130, 2060]
    for x, items in zip(xs, cols):
        y = 520
        for s in items:
            d.ellipse([x, y + 16, x + 20, y + 36], fill=SAGE)
            d.text((x + 44, y), s, font=SANS(46), fill=INK)
            y += 104
    save(img, "09-whats-included.jpg")


def img10_how(pk):
    img = canvas(CREAM)
    d = header(img, "Instant digital download", "How it works")
    where = "in Etsy > Purchases." if MARKET == "etsy" else "on Creative Market."
    steps = [("1", "Purchase", "Your files are ready right away\n" + where),
             ("2", "Download", "Two PDFs: US Letter and A4,\nplus a quick-start guide."),
             ("3", "Fill or print", "Type on any device, or print\nonly the pages you need.")]
    bw = 760
    gap = (W - 3 * bw) / 4
    for i, (n, h, body) in enumerate(steps):
        x = gap + i * (bw + gap)
        d.rounded_rectangle([x, 620, x + bw, 1640], radius=40, fill=WHITE)
        cx = x + bw / 2
        d.ellipse([cx - 110, 720, cx + 110, 940], fill=SAND)
        text_c(d, cx, 735, n, SERIF_B(150), CLAY)
        text_c(d, cx, 1010, h, SERIF(96))
        for j, line in enumerate(body.split("\n")):
            size = 48
            while d.textlength(line, font=SANS(size)) > bw - 80:  # never spill past the card
                size -= 1
            text_c(d, cx, 1180 + j * 76, line, SANS(size), MUTED)
    note = "No physical item will be shipped." + (" For personal use only." if MARKET == "etsy" else "")
    text_c(d, W / 2, 1810, note, SANS_M(46), MUTED)
    save(img, "10-how-it-works.jpg")


def hero_wide(pk):
    """3:2 hero (3000x2000) for marketplaces with landscape thumbnails, e.g. Creative Market."""
    global W, H
    saved = (W, H)
    W, H = 3000, 2000
    try:
        img = soft_background((250, 246, 240), (245, 236, 226), [
            (2450, 260, 700, (214, 230, 220, 255)),
            (2050, 1900, 620, (247, 221, 207, 255)),
            (380, 1850, 480, (246, 234, 206, 200)),
        ])
        d = ImageDraw.Draw(img)
        x = 230
        caps(d, x + 4, 250, "Printable + fillable", SANS_SB(46), SAGE, 9)
        d.text((x - 6, 305), "Moving", font=SERIF(250), fill=INK)
        d.text((x - 6, 545), "Planner", font=SERIF(250), fill=INK)
        d.text((x + 4, 830), "The Calm Move", font=SERIF_I(92), fill=CLAY)
        y = 1010
        for s_, col in [("51 pages", CLAY), ("Fillable + printable", SAGE), ("US Letter + A4", (184, 149, 74)),
                        ("Color-coded box labels", (111, 136, 160))]:
            f = SANS_SB(46)
            w = d.textlength(s_, font=f) + 120
            d.rounded_rectangle([x, y, x + w, y + 100], radius=50, fill=WHITE)
            d.ellipse([x + 34, y + 37, x + 60, y + 63], fill=col)
            d.text((x + 80, y + 24), s_, font=f, fill=INK)
            y += 122
        y += 40
        sw = 100
        for i, (code, col) in enumerate([("K", "#E9B49E"), ("L", "#A9C5B2"), ("D", "#EBD394"), ("B1", "#A9C0D8"),
                                         ("B2", "#CBB8D8"), ("BA", "#9ED2CD"), ("O", "#D9C4A7"), ("G", "#C2C3BA")]):
            sx = x + i * (sw + 12)
            d.rounded_rectangle([sx, y, sx + sw, y + sw], radius=20, fill=col)
            f = SERIF_B(48 if len(code) == 1 else 40)
            tw = d.textlength(code, font=f)
            bb = d.textbbox((0, 0), code, font=f)
            d.text((sx + (sw - tw) / 2, y + (sw - (bb[3] - bb[1])) / 2 - bb[1]), code, font=f, fill=INK)
        paste_page(img, page_img(pk["Room door signs 1"]), 1420, 200, 740, angle=9)
        paste_page(img, page_img(pk["Special labels"]), 2060, 140, 720, angle=-8)
        paste_page(img, page_img(1, dpi=200), 1580, 170, 860)
        paste_page(img, sticker(500, 290, (233, 180, 158), "FRAGILE", "Handle with care", SANS_B(78), SANS(36)),
                   1390, 1250, 500, angle=10)
        paste_page(img, sticker(500, 290, (169, 197, 178), "OPEN FIRST", "Essentials inside", SANS_B(68), SANS(36)),
                   2290, 1230, 500, angle=-9)
        paste_page(img, box_label_sticker(600, 400, (233, 180, 158), "K", "KITCHEN", "Pots & pans"),
                   1800, 1380, 600, angle=-3)
        d = ImageDraw.Draw(img)
        cx, cy, r = 2440, 230, 150
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=CLAY)
        text_c(d, cx, cy - 112, "51", SERIF_B(140), WHITE)
        caps(d, cx, cy + 50, "pages", SANS_SB(34), WHITE, 7, center=True)
        save(img, "01-hero.jpg")
    finally:
        W, H = saved


def to_3x2(src, dst, size=(3640, 2428)):
    """Pad a 4:3 image to 3:2 with its own (flat) background color, then resize."""
    im = Image.open(src).convert("RGB")
    w, h = im.size
    if w / h < 1.5:
        nw = round(h * 1.5)
        c = Image.new("RGB", (nw, h), im.getpixel((4, 4)))
        c.paste(im, ((nw - w) // 2, 0))
        im = c
    im.resize(size, Image.LANCZOS).save(dst, "JPEG", quality=90, optimize=True)
    print(dst)


def build_creative_market():
    global PDF, PDF_A4, OUT, MARKET
    saved = (PDF, PDF_A4, OUT, MARKET)
    cm = os.path.join(HERE, "dist-creative-market")
    PDF = os.path.join(cm, "The-Calm-Move-Moving-Planner-US-Letter.pdf")
    PDF_A4 = os.path.join(cm, "The-Calm-Move-Moving-Planner-A4.pdf")
    OUT = tempfile.mkdtemp()
    MARKET = "creative-market"
    try:
        pk = page_key()
        hero_wide(pk)
        for fn in [img2_inside, img3_system, img4_timeline, img5_fillable,
                   img6_admin, img7_settle, img8_sizes, img9_contents, img10_how]:
            fn(pk)
        final = os.path.join(HERE, "mockups-creative-market")
        os.makedirs(final, exist_ok=True)
        for name in sorted(os.listdir(OUT)):
            to_3x2(os.path.join(OUT, name), os.path.join(final, name))
    finally:
        PDF, PDF_A4, OUT, MARKET = saved


if __name__ == "__main__":
    pk = page_key()
    for fn in [img1_hero, img2_inside, img3_system, img4_timeline, img5_fillable,
               img6_admin, img7_settle, img8_sizes, img9_contents, img10_how]:
        fn(pk)
    build_creative_market()
