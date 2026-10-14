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


def page_img(n, pdf=PDF, dpi=170):
    key = (n, pdf, dpi)
    if key not in _cache:
        base = os.path.join(TMP, f"{os.path.basename(pdf)}-{dpi}-{n}")
        subprocess.run(["pdftoppm", "-r", str(dpi), "-png", "-singlefile", "-f", str(n), "-l", str(n), pdf, base],
                       check=True)
        _cache[key] = Image.open(base + ".png").convert("RGB")
    return _cache[key]


def page_key(pdf=PDF):
    """Map bookmark titles -> 1-based page numbers so mockups survive page reordering."""
    r = PdfReader(pdf)
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
    img = soft_background((250, 246, 240), (245, 236, 226), [
        (2350, 380, 700, (214, 230, 220, 255)),
        (2050, 2050, 620, (247, 221, 207, 255)),
        (420, 2050, 480, (246, 234, 206, 200)),
    ])
    d = ImageDraw.Draw(img)
    # ---- copy (left, inside the square-crop safe zone x 375..2625)
    x = 400
    caps(d, x + 4, 330, "Printable + fillable", SANS_SB(46), SAGE, 9)
    d.text((x - 6, 390), "Moving", font=SERIF(270), fill=INK)
    d.text((x - 6, 650), "Planner", font=SERIF(270), fill=INK)
    d.text((x + 4, 965), "The Calm Move", font=SERIF_I(96), fill=CLAY)
    y = 1150
    for s, col in [("51 pages", CLAY), ("Fillable + printable", SAGE), ("US Letter + A4", (184, 149, 74)),
                   ("Color-coded box labels", (111, 136, 160))]:
        f = SANS_SB(46)
        w = d.textlength(s, font=f) + 2 * 40 + 40
        d.rounded_rectangle([x, y, x + w, y + 100], radius=50, fill=WHITE)
        d.ellipse([x + 34, y + 37, x + 60, y + 63], fill=col)
        d.text((x + 80, y + 24), s, font=f, fill=INK)
        y += 124
    # ---- composition (right)
    paste_page(img, page_img(pk["Room door signs 1"]), 1300, 330, 800, angle=9)
    paste_page(img, page_img(pk["Special labels"]), 1980, 250, 800, angle=-8)
    paste_page(img, page_img(1, dpi=200), 1560, 330, 900)
    # loose cut-out labels as props
    paste_page(img, sticker(470, 270, (233, 180, 158), "FRAGILE", "Handle with care", SANS_B(72), SANS(34)),
               1280, 1420, 470, angle=11)
    paste_page(img, sticker(470, 270, (169, 197, 178), "OPEN FIRST", "Essentials inside", SANS_B(64), SANS(34)),
               2150, 1430, 470, angle=-9)
    paste_page(img, box_label_sticker(560, 380, (233, 180, 158), "K", "KITCHEN", "Pots & pans"),
               1660, 1600, 560, angle=-3)
    # badge on the cover corner
    d = ImageDraw.Draw(img)
    cx, cy, r = 2420, 380, 150
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=CLAY)
    text_c(d, cx, cy - 112, "51", SERIF_B(140), WHITE)
    caps(d, cx, cy + 50, "pages", SANS_SB(34), WHITE, 7, center=True)
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
    steps = [("1", "Purchase", "Your files are ready right away\nin Etsy > Purchases."),
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
            text_c(d, cx, 1180 + j * 76, line, SANS(48), MUTED)
    text_c(d, W / 2, 1810, "No physical item will be shipped. For personal use only.", SANS_M(46), MUTED)
    save(img, "10-how-it-works.jpg")


if __name__ == "__main__":
    pk = page_key()
    for fn in [img1_hero, img2_inside, img3_system, img4_timeline, img5_fillable,
               img6_admin, img7_settle, img8_sizes, img9_contents, img10_how]:
        fn(pk)
