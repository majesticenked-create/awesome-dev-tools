"""Build "The Calm Move" moving planner as fillable, hyperlinked PDFs (US Letter + A4).

Usage:  python3 build_planner.py            -> dist/*.pdf
"""
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")
DIST = os.path.join(HERE, "dist")

for name, file in [
    ("Serif", "Caladea-Regular.ttf"), ("Serif-Bold", "Caladea-Bold.ttf"),
    ("Serif-Italic", "Caladea-Italic.ttf"),
    ("Sans", "Inter-Regular.ttf"), ("Sans-Medium", "Inter-Medium.ttf"),
    ("Sans-SemiBold", "Inter-SemiBold.ttf"), ("Sans-Bold", "Inter-Bold.ttf"),
    ("Sans-Italic", "Inter-Italic.ttf"),
]:
    pdfmetrics.registerFont(TTFont(name, os.path.join(FONTS, file)))

# ---------------------------------------------------------------- palette
INK = HexColor("#2F3A3A")
MUTED = HexColor("#6B7774")
LINE = HexColor("#C9CFCC")
FAINT = HexColor("#E4E8E6")
SAND = HexColor("#F4EFE7")
SAGE = HexColor("#6F8F7F")
CLAY = HexColor("#C47F62")
SLATE = HexColor("#6F88A0")
MUSTARD = HexColor("#B8954A")
OLIVE = HexColor("#7F8E5E")
PLUM = HexColor("#94809F")

SECTIONS = {
    "Plan": SAGE, "Timeline": CLAY, "Admin": SLATE,
    "Declutter & Pack": MUSTARD, "Clean & Settle": OLIVE, "Labels & Signs": PLUM,
}

# Room code system: code, default room name, label color
ROOMS = [
    ("K", "Kitchen", "#E9B49E"), ("L", "Living Room", "#A9C5B2"),
    ("D", "Dining Room", "#EBD394"), ("B1", "Bedroom 1", "#A9C0D8"),
    ("B2", "Bedroom 2", "#CBB8D8"), ("BA", "Bathroom", "#9ED2CD"),
    ("O", "Office", "#D9C4A7"), ("G", "Garage / Storage", "#C2C3BA"),
]

BRAND = "THE CALM MOVE"


def wrap(text, font, size, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if pdfmetrics.stringWidth(t, font, size) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


class Planner:
    def __init__(self, path, pagesize):
        self.c = canvas.Canvas(path, pagesize=pagesize)
        self.c.setTitle("The Calm Move: Moving Planner")
        self.c.setAuthor("The Calm Move")
        self.c.setSubject("Printable & fillable moving planner")
        self.W, self.H = pagesize
        self.M = 40
        self.CW = self.W - 2 * self.M
        self.n = 0
        self.page_no = 0
        self.bottom = self.M + 26  # lowest y content may reach (footer above)
        self.overflows = []

    # ------------------------------------------------------------ form fields
    def _name(self):
        self.n += 1
        return f"f{self.n}"

    def tfield(self, x, y, w, h=13, size=9, multiline=False, value=""):
        """Invisible text field whose bottom edge sits at y."""
        self.c.acroForm.textfield(
            name=self._name(), x=x, y=y, width=w, height=h, value=value,
            borderWidth=0, fillColor=None, borderColor=None, textColor=INK,
            fontName="Helvetica", fontSize=0 if multiline else size,
            fieldFlags="multiline" if multiline else "", maxlen=0 if multiline else 200,
        )

    def checkbox(self, x, y, s=8.5, color=None):
        c = self.c
        c.setStrokeColor(color or MUTED)
        c.setLineWidth(0.7)
        c.roundRect(x, y, s, s, 1.6, stroke=1, fill=0)
        c.acroForm.checkbox(
            name=self._name(), x=x, y=y, size=s, borderWidth=0, fillColor=None,
            borderColor=None, textColor=INK, buttonStyle="check", fieldFlags="",
        )

    # ------------------------------------------------------------ text helpers
    def text(self, x, y, s, font="Sans", size=9, color=INK, align="left", spacing=0):
        c = self.c
        c.setFillColor(color)
        c.setFont(font, size)
        if spacing:
            t = c.beginText()
            t.setFont(font, size)
            t.setCharSpace(spacing)
            w = pdfmetrics.stringWidth(s, font, size) + spacing * (len(s) - 1)
            if align == "right":
                x -= w
            elif align == "center":
                x -= w / 2
            t.setTextOrigin(x, y)
            t.textOut(s)
            t.setCharSpace(0)  # Tc persists in the graphics state; reset it
            c.drawText(t)
            return
        if align == "right":
            c.drawRightString(x, y, s)
        elif align == "center":
            c.drawCentredString(x, y, s)
        else:
            c.drawString(x, y, s)

    def caps(self, x, y, s, color=MUTED, size=6.8, align="left"):
        self.text(x, y, s.upper(), "Sans-SemiBold", size, color, align, spacing=0.9)

    def para(self, x, y, s, width, size=9, font="Sans", color=INK, lead=1.45):
        for line in wrap(s, font, size, width):
            self.text(x, y, line, font, size, color)
            y -= size * lead
        return y

    def hline(self, x1, x2, y, color=LINE, w=0.6):
        self.c.setStrokeColor(color)
        self.c.setLineWidth(w)
        self.c.line(x1, y, x2, y)

    def check_room(self, y, need):
        if y - need < self.bottom - 0.5:
            self.overflows.append(f"page {self.page_no}: short by {self.bottom - (y - need):.0f}pt")

    # ------------------------------------------------------------ page chrome
    def page(self, key, title, section, subtitle=None, date_field=False):
        if self.page_no:
            self.c.showPage()
        self.page_no += 1
        self.section = section
        self.accent = SECTIONS.get(section, SAGE)
        c, M, W, H = self.c, self.M, self.W, self.H
        c.bookmarkPage(key)
        # thin accent bar
        c.setFillColor(self.accent)
        c.rect(M, H - M + 6, 34, 3, stroke=0, fill=1)
        self.caps(M, H - M - 8, section, self.accent, 7)
        self.text(M, H - M - 36, title, "Serif", 27, INK)
        y = H - M - 50
        if subtitle:
            self.text(M, y, subtitle, "Sans-Italic", 8.6, MUTED)
            y -= 6
        if date_field:
            self.caps(W - M - 120, H - M - 34, "Date", MUTED)
            self.hline(W - M - 96, W - M, H - M - 36)
            self.tfield(W - M - 96, H - M - 35, 96)
        self.hline(M, W - M, y - 6, INK, 0.8)
        self.footer(key)
        return y - 26

    def footer(self, key):
        c, M, W = self.c, self.M, self.W
        y = M - 6
        self.hline(M, W - M, y + 14, FAINT, 0.6)
        self.caps(M, y, BRAND, MUTED, 6.2)
        self.text(W / 2, y, str(self.page_no), "Sans", 7, MUTED, "center")
        if key != "contents":
            self.caps(W - M, y, "Contents  ↗", self.accent, 6.2, "right")
            c.linkAbsolute("Contents", "contents", (W - M - 70, y - 4, W - M, y + 9))

    def section_title(self, x, y, s, color=None, width=None):
        self.text(x, y, s, "Serif-Bold", 12.5, color or INK)
        if width:
            self.hline(x, x + width, y - 6, FAINT)
        return y - 20

    # ------------------------------------------------------------ building blocks
    def field_line(self, x, y, w, label, label_w=None):
        """CAPS LABEL ________ with a fillable field."""
        label_w = label_w if label_w is not None else pdfmetrics.stringWidth(label.upper(), "Sans-SemiBold", 6.8) + len(label) * 0.9 + 6
        self.caps(x, y + 1, label)
        self.hline(x + label_w, x + w, y - 1)
        self.tfield(x + label_w, y, w - label_w)

    def lines(self, x, y, w, n, row=19):
        for _ in range(n):
            y -= row
            self.hline(x, x + w, y)
            self.tfield(x, y + 1, w)
        return y - 6

    def checklist(self, x, y, w, items, row=17.5, blanks=0, date_col=False):
        self.check_room(y, (len(items) + blanks) * row)
        for i, it in enumerate(list(items) + [None] * blanks):
            yy = y - i * row
            self.checkbox(x, yy - 1.5)
            tx = x + 15
            right = x + w - (58 if date_col else 0)
            if it is None:
                self.hline(tx, right, yy - 2)
                self.tfield(tx, yy - 1, right - tx)
            else:
                fs = 8.8
                while pdfmetrics.stringWidth(it, "Sans", fs) > right - tx - 2 and fs > 7:
                    fs -= 0.2
                self.text(tx, yy, it, "Sans", fs)
            if date_col:
                self.hline(x + w - 50, x + w, yy - 2)
                self.tfield(x + w - 50, yy - 1, 50, size=8)
        return y - (len(items) + blanks) * row - 4

    def table(self, x, y, cols, rows, row=18, prefill=None, header=True, number_from=None):
        """cols: list of (header, width, kind) where kind in text|check|static|multi."""
        prefill = prefill or []
        self.check_room(y, (rows + 1) * row)
        if header:
            cx = x
            for h, w, kind in cols:
                if kind == "check":
                    self.caps(cx + w / 2, y, h, MUTED, 6.2, "center")
                else:
                    self.caps(cx + 2, y, h, MUTED, 6.5)
                cx += w
            y -= 6
            self.hline(x, x + sum(w for _, w, _ in cols), y, INK, 0.7)
        for r in range(rows):
            top = y
            y -= row
            cx = x
            for ci, (h, w, kind) in enumerate(cols):
                pre = prefill[r][ci] if r < len(prefill) and ci < len(prefill[r]) else None
                if number_from is not None and ci == 0:
                    pre = str(number_from + r)
                if kind == "check":
                    self.checkbox(cx + w / 2 - 4.25, y + (row - 8.5) / 2)
                elif pre:
                    fs = 8.6
                    while pdfmetrics.stringWidth(pre, "Sans", fs) > w - 6 and fs > 6.5:
                        fs -= 0.2
                    self.text(cx + 2, y + (row - 8) / 2 + 1, pre, "Sans-Medium" if ci == 0 else "Sans", fs)
                elif kind == "multi":
                    self.tfield(cx + 1, y + 1, w - 3, row - 2, multiline=True)
                elif kind != "static":
                    self.tfield(cx + 1, y + 1, w - 3, min(row - 3, 14), size=8.5)
                cx += w
            self.hline(x, x + sum(w for _, w, _ in cols), y)
            # light column separators
            cx = x
            for h, w, kind in cols[:-1]:
                cx += w
                self.c.setStrokeColor(FAINT)
                self.c.setLineWidth(0.5)
                self.c.line(cx, y + 2, cx, top - 2)
        return y - 14

    def fill_notes(self, y, title="Notes", x=None, w=None, row=20):
        x = self.M if x is None else x
        w = self.CW if w is None else w
        if y - self.bottom < 70:
            return y
        y = self.section_title(x, y, title, width=w)
        n = int((y + 10 - self.bottom) // row)
        return self.lines(x, y + 10, w, n, row)

    def box(self, x, y, w, h, fill=SAND, stroke=None, r=6):
        c = self.c
        if fill:
            c.setFillColor(fill)
        if stroke:
            c.setStrokeColor(stroke)
            c.setLineWidth(0.7)
        c.roundRect(x, y - h, w, h, r, stroke=1 if stroke else 0, fill=1 if fill else 0)

    def tip(self, x, y, w, s, title="Tip"):
        lines = wrap(s, "Sans", 8.2, w - 24 - 34)
        h = max(30, 12 + len(lines) * 11.5)
        self.check_room(y, h)
        self.box(x, y, w, h)
        self.caps(x + 12, y - 17, title, self.accent, 6.8)
        yy = y - 17
        for ln in lines:
            self.text(x + 12 + 34, yy, ln, "Sans", 8.2, INK)
            yy -= 11.5
        return y - h - 14

    def save(self):
        self.c.showPage()
        self.c.save()


# =================================================================== content
TIMELINE = {
    "8 weeks": [
        "Set your moving date; confirm lease end or closing date",
        "Start a moving folder for contracts, quotes and receipts",
        "Set your moving budget (Budget page)",
        "Request at least 3 mover or truck-rental quotes",
        "Start decluttering, one room at a time",
        "Photograph valuables and note serial numbers",
        "Give notice to your landlord (if renting)",
        "Research schools and request record transfers",
        "Start using up frozen food and pantry items",
        "Ask your employer about relocation support",
    ],
    "6 weeks": [
        "Book movers or truck; get confirmation in writing",
        "Order packing supplies (Supplies page)",
        "Assign a code and color to every room (Room Key)",
        "Sell, donate or recycle what you won't move",
        "Pack rarely used items: seasonal, books, decor",
        "Measure rooms, doorways and stairs at the new home",
        "Sketch furniture placement (Layout page)",
        "Request medical, dental and vet records",
        "Arrange childcare / pet care for moving day",
        "Book time off work for moving day",
    ],
    "4 weeks": [
        "Submit your change of address / mail forwarding",
        "Schedule utility shut-off at the old home",
        "Schedule utility set-up at the new home",
        "Update address: bank, cards, insurance, employer",
        "Transfer or start home / renters insurance",
        "Reserve elevator or parking at both homes",
        "Keep packing room by room; log every box",
        "Refill prescriptions to cover the move",
        "Book storage if you need it",
        "Plan how you'll carry valuables & documents yourself",
    ],
    "2 weeks": [
        "Reconfirm mover date, time, addresses and payment",
        "Pack most rooms; keep only daily essentials out",
        "Take apart furniture; bag and label all hardware",
        "Return borrowed items; collect things you lent",
        "Cancel or transfer local memberships",
        "Service your car if driving a long distance",
        "Plan easy meals for moving week",
        "Back up computers and phones",
        "Plan your route and overnight stops",
        "Use up cleaning products & liquids you can't move",
    ],
    "1 week": [
        "Pack an Open-First box for every person",
        "Pack a suitcase with 3 to 4 days of clothes",
        "Defrost and dry the freezer (24 to 48 hrs before)",
        "Drain hoses; dispose of paint, fuel and chemicals",
        "Confirm utility off / on dates",
        "Get cash for tips, plus water & snacks for helpers",
        "Label every box on two sides + top",
        "Print room signs for the new home",
        "Start move-out cleaning in finished rooms",
    ],
}

DAY_BEFORE = [
    "Finish packing except bed and bathroom",
    "Set aside anything the movers must NOT take",
    "Charge phones; essentials bag ready by the door",
    "Prepare tip envelopes and drinks for the crew",
]

MOVING_DAY = [
    "Photograph meter readings at the old home",
    "Walk through with the crew lead; point out fragile items",
    "Keep valuables, documents & essentials with you",
    "Check every room, cupboard and closet is empty",
    "Read the inventory / bill of lading before signing",
    "Lock windows & doors; hand over keys",
    "Photograph meter readings at the new home",
    "Tape room signs on doors before boxes arrive",
    "Tick off boxes on the Box Inventory as they arrive",
    "Note any damage before the movers leave",
]

AFTER = {
    "First 24 hours": [
        "Unpack Open-First boxes", "Make up the beds", "Check power, water, heat & internet",
        "Find the breaker & water shut-off", "Test smoke & CO alarms", "Order (or cook!) a celebration meal",
    ],
    "First week": [
        "Change or rekey the locks", "Unpack kitchen and bathrooms", "File moving damage claims",
        "Register kids at school", "Meet the neighbors", "Recycle or pass on boxes",
    ],
    "First month": [
        "Update driver's license & car registration", "Register to vote at your new address",
        "Find a doctor, dentist and vet", "Update pet microchip details",
        "Check mail is forwarding properly", "Compare budget estimate vs actual",
    ],
}

BUDGET = [
    "Movers / truck rental", "Fuel, tolls & parking", "Packing supplies", "Storage",
    "Cleaning service", "Travel & lodging", "Meals during the move", "Utility deposits & connection fees",
    "Child / pet care", "Tips for movers & helpers", "Repairs at the old home",
    "Security deposit / closing costs", "New home essentials", "Furniture & decor",
]

QUOTE_ROWS = [
    "Company", "Contact name", "Phone / email", "Date available", "Arrival window",
    "Quote type (binding?)", "Total estimate", "Deposit required", "Hourly or flat rate",
    "Crew size / truck", "Packing included?", "Insurance / valuation", "Extra fees (stairs, etc.)",
    "Reviews / rating", "Notes",
]

ADDRESS = [
    ("Government", ["Postal mail forwarding", "Driver's license / ID", "Vehicle registration",
                    "Voter registration", "Tax office", "Benefits agencies"]),
    ("Money", ["Bank accounts", "Credit cards", "Loans / mortgage", "Investments / pension",
               "Payment apps", "Car insurance", "Home / renters insurance"]),
    ("Health", ["Doctor", "Dentist", "Pharmacy", "Health insurance", "Vet & pet microchip"]),
    ("Work & school", ["Employer / payroll", "Schools / daycare", "Professional bodies"]),
    ("Home & life", ["Online shopping accounts", "Subscriptions & magazines", "Phone provider",
                     "Gym / clubs", "Charities", "Family & friends"]),
]

UTILITIES = ["Electricity", "Gas", "Water & sewer", "Trash & recycling", "Internet", "TV / streaming",
             "Mobile / phone", "Home security", "Lawn / pest control", "HOA / building"]

CONTACTS = ["Moving company", "Truck rental", "Current landlord / agent", "New landlord / agent",
            "Realtor", "Lender / mortgage", "Storage unit", "Old building manager",
            "New building manager", "Childcare", "Pet sitter", "Helper", "Helper", "", "", ""]

SUPPLIES = ["Small boxes (books, heavy items)", "Medium boxes", "Large boxes (light items)",
            "Wardrobe boxes", "Dish-pack boxes", "Packing tape + tape gun", "Markers",
            "Packing paper", "Bubble wrap", "Stretch wrap", "Mattress bags", "Furniture pads / blankets",
            "Zip bags for screws & hardware", "Box cutter / scissors", "Trash bags", "Dolly / hand truck",
            "Tool kit", "Cleaning supplies"]

ROOM_TASKS = [
    "Declutter: keep / sell / donate / toss", "Pack books, decor & things you rarely use",
    "Empty drawers, closets & shelves", "Wrap fragile items in paper or bubble wrap",
    "Photograph electronics wiring before unplugging", "Take down art and mirrors; patch holes",
    "Take apart furniture; bag + label the hardware", "Label each box: code, number, contents",
    "Log boxes on the Box Inventory", "Final check: under beds, behind doors, high shelves",
    "Clean the empty room",
]

ESSENTIALS = {
    "Kitchen": ["Paper plates & cups", "Cutlery", "Kettle / coffee maker", "Snacks & water",
                "Dish soap & sponge", "Trash bags", "Can opener"],
    "Bathroom": ["Toilet paper!", "Towels", "Soap & shampoo", "Toothbrush & paste",
                 "Shower curtain & hooks", "Hand towel"],
    "Bedroom": ["Sheets & pillows", "Blankets", "Pajamas", "Change of clothes", "Phone chargers"],
    "Tools": ["Box cutter", "Screwdrivers", "Allen keys", "Tape measure", "Light bulbs",
              "Flashlight", "Extension cord"],
    "Documents": ["IDs & passports", "Lease / closing papers", "Mover contract", "New keys",
                  "This planner"],
    "Health & cleaning": ["Medications", "First-aid kit", "Hand sanitizer", "All-purpose spray",
                          "Paper towels", "Broom / dustpan"],
}

KIDS = ["Talk about the move early and often", "Visit or show photos of the new neighborhood",
        "Request school records & register at new school", "Let kids pack their own Open-First box",
        "Arrange childcare for moving day", "Set up kids' rooms first",
        "Keep meals and bedtime routines steady", "Find new clubs, sports & activities"]
PETS = ["Update microchip and ID tag", "Get vet records & refill medications",
        "Find a new vet near the new home", "Pet sitter or quiet room on moving day",
        "Pack a pet bag: food, bowls, leash, litter, meds", "Check lease / HOA pet rules",
        "Pet-proof the new home before arrival", "Plan travel crate & rest stops"]

CLEAN_OUT = {
    "Kitchen": ["Inside oven & stovetop", "Fridge & freezer (unplug, dry)", "Microwave",
                "Cabinets & drawers inside", "Dishwasher filter", "Sink & faucet", "Floor & behind appliances"],
    "Bathrooms": ["Toilet inside & out", "Tub / shower & grout", "Sink, mirror & fixtures",
                  "Cabinets & drawers", "Exhaust fan cover", "Floor"],
    "Every room": ["Ceiling fans & light fixtures", "Baseboards & door frames", "Switches & outlets",
                   "Windows, sills & tracks", "Inside closets", "Patch nail holes",
                   "Spot-clean walls", "Vacuum & mop floors"],
    "Final": ["Remove all trash & recycling", "Replace dead light bulbs", "Photo / video of clean home",
              "Return keys, remotes & fobs", "Leave forwarding address"],
}

CLEAN_IN = {
    "Kitchen": ["Wipe cabinets & drawers inside", "Clean fridge before stocking", "Run dishwasher empty",
                "Clean oven & microwave", "Sanitize counters & sink"],
    "Bathrooms": ["Disinfect toilet, sink & tub", "New shower liner", "Wipe cabinets", "Clean mirrors & floor"],
    "Every room": ["Dust high surfaces & fans", "Wipe switches & door handles", "Clean vents & returns",
                   "Wash windows & sills", "Vacuum & mop floors"],
    "Safety": ["Change or rekey locks", "Test smoke & CO alarms", "Find breaker panel",
               "Find water & gas shut-off", "Check fire extinguisher", "Replace HVAC filter"],
}

WALK_ROOMS = ["Entry / hall", "Living room", "Kitchen", "Dining", "Bedroom 1", "Bedroom 2",
              "Bedroom 3", "Bathroom 1", "Bathroom 2", "Laundry", "Garage", "Outdoor / balcony", "", ""]

NEIGHBORHOOD = [
    ("Home", ["Trash day", "Recycling day", "Wi-Fi name", "Wi-Fi password", "Garage / gate code",
              "Breaker panel location", "Water shut-off location", "Gas shut-off location",
              "HOA / building contact"]),
    ("Nearby", ["Grocery store", "Pharmacy", "Hardware store", "Post office", "Gym",
                "Park / playground", "Library", "Favorite takeout", "Coffee shop"]),
    ("Health & school", ["Urgent care / hospital", "Doctor", "Dentist", "Vet", "School(s)",
                         "Childcare"]),
    ("People", ["Neighbor", "Neighbor", "Neighbor", "Emergency contact"]),
]


# =================================================================== pages
def p_cover(p):
    c, W, H, M = p.c, p.W, p.H, p.M
    p.page_no += 1
    c.bookmarkPage("cover")
    # soft panel
    c.setFillColor(SAND)
    c.rect(0, H * 0.38, W, H * 0.62, stroke=0, fill=1)
    # line-art house
    cx, base = W / 2, H * 0.56
    c.setStrokeColor(INK)
    c.setLineWidth(1.4)
    c.setLineJoin(1)
    c.setLineCap(1)
    w, h = 120, 82
    c.rect(cx - w / 2, base, w, h, stroke=1, fill=0)
    path = c.beginPath()
    path.moveTo(cx - w / 2 - 16, base + h - 4)
    path.lineTo(cx, base + h + 58)
    path.lineTo(cx + w / 2 + 16, base + h - 4)
    c.drawPath(path, stroke=1, fill=0)
    c.setFillColor(CLAY)
    c.roundRect(cx - 14, base, 28, 46, 2, stroke=0, fill=1)
    c.setFillColor(SAGE)
    c.rect(cx - w / 2 + 14, base + 44, 22, 22, stroke=0, fill=1)
    c.rect(cx + w / 2 - 36, base + 44, 22, 22, stroke=0, fill=1)
    # little boxes beside the house
    for bx, by, bw, col in [(cx + w / 2 + 30, base, 42, "#E9B49E"), (cx + w / 2 + 38, base + 34, 30, "#EBD394"),
                            (cx - w / 2 - 70, base, 38, "#A9C0D8")]:
        c.setFillColor(HexColor(col))
        c.setStrokeColor(INK)
        c.setLineWidth(1.1)
        c.rect(bx, by, bw, bw * 0.8, stroke=1, fill=1)
        c.line(bx + bw * 0.38, by + bw * 0.8, bx + bw * 0.38, by + bw * 0.8 - 10)
        c.line(bx + bw * 0.62, by + bw * 0.8, bx + bw * 0.62, by + bw * 0.8 - 10)
    c.setStrokeColor(INK)
    c.line(cx - w / 2 - 100, base, cx + w / 2 + 100, base)

    p.caps(W / 2, H - 92, "Complete moving planner", SAGE, 9, "center")
    p.text(W / 2, H - 160, "The Calm Move", "Serif", 58, INK, "center")
    p.text(W / 2, H - 190, "From eight weeks out to your first month at home", "Serif-Italic", 15, MUTED, "center")

    y = H * 0.38 - 60
    fw = 330
    x = W / 2 - fw / 2
    for lbl in ["Moving from", "Moving to", "Moving day"]:
        p.field_line(x, y, fw, lbl, 82)
        y -= 34
    p.caps(W / 2, M + 4, "Fillable  ·  Printable  ·  Color-coded box system", MUTED, 7, "center")


def p_contents(p, toc):
    y = p.page("contents", "Contents", "Plan", "Tap any line to jump to that page. Every page links back here.")
    colw = (p.CW - 24) / 2
    groups = []
    for title, key, num, section in toc:
        if not groups or groups[-1][0] != section:
            groups.append((section, []))
        groups[-1][1].append((title, key, num))
    # split into two columns
    left, right, count = [], [], 0
    total = sum(len(g[1]) + 2 for g in groups)
    for g in groups:
        (left if count < total / 2 - 2 else right).append(g)
        count += len(g[1]) + 2
    for col, gs in enumerate([left, right]):
        x = p.M + col * (colw + 24)
        yy = y
        for section, items in gs:
            p.caps(x, yy, section, SECTIONS[section], 7.2)
            yy -= 16
            for title, key, num in items:
                p.text(x, yy, title, "Sans", 9.6)
                p.text(x + colw, yy, str(num), "Sans-Medium", 9.6, MUTED, "right")
                tw = pdfmetrics.stringWidth(title, "Sans", 9.6)
                p.c.setStrokeColor(FAINT)
                p.c.setDash(1, 2.5)
                p.c.line(x + tw + 6, yy + 1, x + colw - 18, yy + 1)
                p.c.setDash()
                p.c.linkAbsolute(title, key, (x, yy - 4, x + colw, yy + 11))
                yy -= 16.4
            yy -= 10
        p.check_room(yy, 0)


def p_howto(p):
    y = p.page("howto", "How to Use This Planner", "Plan")
    steps = [
        ("Fill in Move at a Glance", "Write down your dates, both addresses and your mover's details. It's the page you'll check most."),
        ("Follow the timeline", "Work through one week's checklist at a time. If you have less than 8 weeks, start at the matching page and catch up on anything earlier that still matters."),
        ("Give every room a code", "On the Room Key, each room gets a letter code and a color (K = Kitchen, B1 = Bedroom 1 and so on). Print the matching box labels and room signs."),
        ("Number and log every box", "Write the room code and a box number on each label (K-07) and note what's inside on the Box Inventory. On moving day, tick boxes off as they arrive."),
        ("Tape room signs to doors", "Put a sign on each door at the new home before the truck arrives. Movers match the label color to the door, so boxes end up in the right room."),
        ("Keep the admin in one place", "Budget, quotes, address changes, utilities and contacts all live in the Admin section, so you won't have to search for a phone number on moving day."),
    ]
    colw = p.CW
    for i, (h, body) in enumerate(steps, 1):
        p.c.setFillColor(SAND)
        p.c.circle(p.M + 12, y - 3, 12, stroke=0, fill=1)
        p.text(p.M + 12, y - 7.5, str(i), "Serif-Bold", 13, CLAY, "center")
        p.text(p.M + 36, y, h, "Sans-SemiBold", 10.5)
        y = p.para(p.M + 36, y - 15, body, colw - 36, 9, color=MUTED) - 12
    y -= 2
    y = p.section_title(p.M, y, "Two ways to use it", width=p.CW)
    half = (p.CW - 20) / 2
    for i, (h, body) in enumerate([
        ("Type on a screen", "Open the PDF in Adobe Acrobat Reader (free), Preview, Xodo or a browser. Click any line to type and any box to tick it. Save often. In GoodNotes or Notability, import the PDF and write with your stylus."),
        ("Print and write", "Print at 'Actual size' / 100% on US Letter or A4 (use the matching file). Print only the pages you need, and print extra box labels and inventory pages as you go."),
    ]):
        x = p.M + i * (half + 20)
        p.box(x, y + 6, half, 116)
        p.text(x + 14, y - 12, h, "Sans-SemiBold", 10)
        p.para(x + 14, y - 28, body, half - 28, 8.6, color=MUTED)
    y -= 132
    p.tip(p.M, y, p.CW, "Keep this planner, your keys and your documents with you on moving day, not on the truck.", "Tip")


def p_glance(p):
    y = p.page("glance", "Move at a Glance", "Plan", "Everything important on one page.")
    half = (p.CW - 24) / 2
    xs = [p.M, p.M + half + 24]
    for x, t in zip(xs, ["Moving from", "Moving to"]):
        yy = p.section_title(x, y, t, width=half)
        for lbl in ["Address", "", "City / zip", "Key handover"]:
            if lbl:
                p.field_line(x, yy, half, lbl, 66)
            else:
                p.hline(x + 66, x + half, yy - 1)
                p.tfield(x + 66, yy, half - 66)
            yy -= 22
    y = yy - 8
    y = p.section_title(p.M, y, "Key dates", width=p.CW)
    dates = ["Moving day", "Lease end / closing", "Movers arrive", "Keys to new home",
             "Utilities off (old)", "Utilities on (new)", "Last day work / school", "First day work / school"]
    for i, d in enumerate(dates):
        x = xs[i % 2]
        p.field_line(x, y - (i // 2) * 22, half, d, 112)
    y -= 4 * 22 + 12
    y = p.section_title(p.M, y, "Moving company", width=p.CW)
    for i, d in enumerate(["Company", "Phone", "Booking #", "Arrival window", "Crew lead", "Total cost"]):
        p.field_line(xs[i % 2], y - (i // 2) * 22, half, d, 80)
    y -= 3 * 22 + 12
    y = p.section_title(p.M, y, "Budget", width=p.CW)
    bw = (p.CW - 2 * 16) / 3
    for i, d in enumerate(["Total budget", "Estimated", "Actual"]):
        x = p.M + i * (bw + 16)
        p.box(x, y + 8, bw, 44)
        p.caps(x + 10, y - 6, d, MUTED)
        p.text(x + 10, y - 28, "$", "Serif", 14, MUTED)
        p.tfield(x + 22, y - 31, bw - 32, 16, size=12)
    y -= 58
    y = p.section_title(p.M, y, "My top 3 priorities for this move", width=p.CW)
    for i in range(3):
        p.text(p.M, y - i * 22, f"{i + 1}.", "Serif-Bold", 11, CLAY)
        p.hline(p.M + 18, p.M + p.CW, y - i * 22 - 2)
        p.tfield(p.M + 18, y - i * 22 - 1, p.CW - 18)
    p.check_room(y - 2 * 22, 0)


def p_countdown(p):
    y = p.page("countdown", "8-Week Countdown", "Plan", "Write the dates in the corners and plan the key appointments.")
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    lw = 54
    cw = (p.CW - lw) / 7
    avail = y - p.bottom - 14
    rh = avail / 8
    for i, d in enumerate(days):
        p.caps(p.M + lw + i * cw + cw / 2, y, d, MUTED, 6.8, "center")
    y -= 8
    labels = ["8 weeks", "7 weeks", "6 weeks", "5 weeks", "4 weeks", "3 weeks", "2 weeks", "Move week"]
    c = p.c
    for r, lab in enumerate(labels):
        top = y - r * rh
        if r == 7:
            c.setFillColor(SAND)
            c.rect(p.M, top - rh, p.CW, rh, stroke=0, fill=1)
        p.text(p.M, top - 16, lab.split()[0], "Serif-Bold", 15, CLAY if r == 7 else INK)
        p.caps(p.M, top - 27, lab.split()[1] if " " in lab else "", MUTED, 6.2)
        for i in range(7):
            x = p.M + lw + i * cw
            c.setStrokeColor(LINE)
            c.setLineWidth(0.6)
            c.rect(x, top - rh, cw, rh, stroke=1, fill=0)
            p.tfield(x + 2, top - 13, 18, 11, size=7)
            p.tfield(x + 2, top - rh + 2, cw - 4, rh - 16, multiline=True)


def p_week(p, key, label, items, extra=None):
    big, small = label.split()
    y = p.page(key, f"{big} {small.capitalize()} Before", "Timeline", date_field=True)
    y = p.section_title(p.M, y, "To do", width=p.CW)
    y = p.checklist(p.M, y, p.CW, items, row=19.5, blanks=3)
    if extra:
        y -= 6
        y = p.section_title(p.M, y, extra[0], width=p.CW)
        y = p.checklist(p.M, y, p.CW, extra[1], row=19.5, blanks=1)
        y -= 4
    y -= 4
    y = p.section_title(p.M, y, "Notes & reminders", width=p.CW)
    n = int((y - p.bottom) // 19)
    p.lines(p.M, y + 10, p.CW, n)


def p_movingday(p):
    y = p.page("movingday", "Moving Day", "Timeline", "Breathe. Check things off one at a time.", date_field=True)
    lw = 196
    rx = p.M + lw + 22
    rw = p.CW - lw - 22
    p.section_title(p.M, y, "Schedule", width=lw)
    yy = y - 22
    hours = ["6 am", "7", "8", "9", "10", "11", "12 pm", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    row = 23
    for i, h in enumerate(hours):
        p.text(p.M, yy - i * row, h, "Sans-Medium", 8.4, MUTED)
        p.hline(p.M + 36, p.M + lw, yy - i * row - 3)
        p.tfield(p.M + 36, yy - i * row - 2, lw - 36)
    yr = p.section_title(rx, y, "Checklist", width=rw)
    yr = p.checklist(rx, yr, rw, MOVING_DAY, row=19.5)
    yr -= 4
    yr = p.section_title(rx, yr, "Crew & contacts", width=rw)
    for lbl in ["Crew lead", "Phone", "Truck #", "New home contact"]:
        p.field_line(rx, yr, rw, lbl, 92)
        yr -= 22
    ybot = min(yy - len(hours) * row, yr) - 6
    p.section_title(p.M, ybot, "Meter readings", width=p.CW)
    ybot -= 22
    cols = [("", 76, "static"), ("Electric", (p.CW - 76) / 3, "text"), ("Gas", (p.CW - 76) / 3, "text"),
            ("Water", (p.CW - 76) / 3, "text")]
    y = p.table(p.M, ybot, cols, 2, row=20, prefill=[["Old home"], ["New home"]])
    p.fill_notes(y, "Notes")


def p_after(p):
    y = p.page("after", "After the Move", "Timeline", "Settle in. Get these done to finish the move properly.")
    colw = (p.CW - 2 * 18) / 3
    ybot = y
    for i, (h, items) in enumerate(AFTER.items()):
        x = p.M + i * (colw + 18)
        p.box(x, y + 8, colw, 34)
        p.text(x + 12, y - 12, h, "Serif-Bold", 12.5)
        yy = y - 44
        for it in items + [None, None]:
            p.checkbox(x + 4, yy - 1.5)
            if it:
                ln = wrap(it, "Sans", 8.4, colw - 24)
                for j, l in enumerate(ln):
                    p.text(x + 18, yy - j * 11, l, "Sans", 8.4)
                yy -= 11 * len(ln) + 12
            else:
                p.hline(x + 18, x + colw, yy - 2)
                p.tfield(x + 18, yy - 1, colw - 18)
                yy -= 22
        ybot = min(ybot, yy)
    y = ybot - 8
    y = p.section_title(p.M, y, "Things I want to do in our new home", width=p.CW)
    n = int((y - p.bottom - 90) // 20)
    y = p.lines(p.M, y + 10, p.CW, n, 20)
    p.tip(p.M, y - 4, p.CW, "Most movers set a deadline for damage claims (often 9 months in the US, sometimes much shorter). Photograph damage straight away and keep this page handy.", "Note")


def p_budget(p):
    y = p.page("budget", "Moving Budget", "Admin", "Estimate first, then track what you actually spend.")
    w = p.CW
    cols = [("Expense", w - 3 * 84 - 40, "text"), ("Estimated", 84, "text"), ("Actual", 84, "text"),
            ("Difference", 84, "text"), ("Paid", 40, "check")]
    rows = int((y - p.bottom - 60) // 20.5)
    y = p.table(p.M, y, cols, rows, row=20.5, prefill=[[b] for b in BUDGET])
    p.c.setFillColor(SAND)
    p.c.roundRect(p.M, y - 18, w, 30, 5, stroke=0, fill=1)
    p.text(p.M + 10, y - 6, "Total", "Serif-Bold", 13)
    cx = p.M + cols[0][1]
    for _ in range(3):
        p.tfield(cx + 2, y - 10, 80, 14, size=10)
        cx += 84


def p_quotes(p):
    y = p.page("quotes", "Mover Quotes", "Admin", "Compare up to three movers or truck rentals side by side.")
    lw = 128
    cw = (p.CW - lw) / 3
    cols = [("", lw, "static")] + [(f"Option {c}", cw, "text") for c in "ABC"]
    y = p.table(p.M, y, cols, len(QUOTE_ROWS), row=23, prefill=[[r] for r in QUOTE_ROWS])
    p.caps(p.M, y, "We chose", MUTED)
    for i, c in enumerate("ABC"):
        x = p.M + lw + i * cw + 2
        p.checkbox(x, y - 1)
        p.text(x + 14, y, f"Option {c}", "Sans", 8.8)
    y -= 26
    y = p.section_title(p.M, y, "Ask every mover", width=p.CW)
    half = (p.CW - 24) / 2
    qs = ["Are you licensed and insured? (US: USDOT number)", "Is this quote binding or an estimate?",
          "What's not included? Stairs, long carry, fuel?", "How do you handle damage claims?",
          "Can I see the contract before I pay a deposit?", "Do you subcontract to another company?"]
    p.checklist(p.M, y, half, qs[:3], row=19)
    y = p.checklist(p.M + half + 24, y, half, qs[3:], row=19)
    y = p.tip(p.M, y - 4, p.CW, "Get quotes in writing. Be wary of a quote far below the others, or of anyone asking for a large cash deposit.", "Tip")
    p.fill_notes(y, "Notes")


def p_address(p):
    y = p.page("address", "Change of Address", "Admin", "Tick each one off when it's updated and write the date.")
    colw = (p.CW - 24) / 2
    x0, x1 = p.M, p.M + colw + 24
    cols = [ADDRESS[:2], ADDRESS[2:]]
    ys = []
    for ci, groups in enumerate(cols):
        x = [x0, x1][ci]
        yy = y
        for g, items in groups:
            p.caps(x, yy, g, SLATE, 7)
            p.caps(x + colw, yy, "date", MUTED, 6, "right")
            yy -= 18
            yy = p.checklist(x, yy, colw, items, row=17.5, blanks=1, date_col=True) - 8
        if ci == 1:
            ys.append(yy)
        if ci == 0:
            yy -= 4
            p.caps(x, yy, "Other", SLATE, 7)
            yy = p.checklist(x, yy - 18, colw, [], row=17.5, blanks=5, date_col=True)
        ys.append(yy)
    p.fill_notes(min(ys) - 4, "Login reminders & notes")


def p_utilities(p):
    y = p.page("utilities", "Utilities", "Admin", "Shut off at the old home and set up at the new one, with no gap in between.")
    w = p.CW
    cols = [("Service", 96, "text"), ("Provider & phone", w - 96 - 70 - 30 - 70 - 30, "text"),
            ("Old: stop", 70, "text"), ("Done", 30, "check"), ("New: start", 70, "text"), ("Done", 30, "check")]
    y = p.table(p.M, y, cols, len(UTILITIES) + 4, row=26, prefill=[[u] for u in UTILITIES])
    y = p.section_title(p.M, y, "Account numbers & notes", width=p.CW)
    n = int((y - p.bottom - 64) // 20)
    y = p.lines(p.M, y + 10, p.CW, n, 20)
    p.tip(p.M, y - 4, p.CW, "Book internet set-up early. Installers can be booked up for 2 to 3 weeks in busy months, and you'll want Wi-Fi on day one.", "Tip")


def p_contacts(p):
    y = p.page("contacts", "Important Contacts", "Admin")
    w = p.CW
    cols = [("Who", 118, "text"), ("Name", 112, "text"), ("Phone", 100, "text"), ("Email / notes", w - 330, "text")]
    p.table(p.M, y, cols, 22, row=25.5, prefill=[[c] for c in CONTACTS])


def p_declutter(p):
    y = p.page("declutter", "Declutter Tracker", "Declutter & Pack", "If you won't use it at the new home, don't pay to move it.")
    w = p.CW
    cols = [("Item", w - 70 - 4 * 44, "text"), ("Room", 70, "text"), ("Keep", 44, "check"), ("Sell", 44, "check"),
            ("Donate", 44, "check"), ("Toss", 44, "check")]
    y = p.table(p.M, y, cols, int((y - p.bottom - 60) // 21.5), row=21.5)
    p.tip(p.M, y, p.CW, "Can't decide? Ask: Have I used it in the last year? Would I buy it again? Does it fit the new space?", "Ask")


def p_sell_log(p):
    y = p.page("sell", "Sell, Gift & Donate Log", "Declutter & Pack", "Track what's listed, sold, given away and dropped off. Keep donation receipts for taxes.")
    w = p.CW
    cols = [("Item", w - 84 - 92 - 66 - 2 * 40, "text"), ("Sell/gift/donate", 84, "text"), ("Where", 92, "text"),
            ("Price", 66, "text"), ("Done", 40, "check"), ("Paid", 40, "check")]
    y = p.table(p.M, y, cols, int((y - p.bottom - 46) // 21.5), row=21.5)
    p.c.setFillColor(SAND)
    p.c.roundRect(p.M, y - 18, w, 30, 5, stroke=0, fill=1)
    p.text(p.M + 10, y - 6, "Total earned", "Serif-Bold", 13)
    p.tfield(p.M + 110, y - 10, 120, 14, size=10)


def p_supplies(p):
    y = p.page("supplies", "Packing Supplies", "Declutter & Pack")
    lw = p.CW - 170
    cols = [("Item", lw, "text"), ("Need", 50, "text"), ("Have", 50, "text"), ("Bought", 70, "check")]
    y = p.table(p.M, y, cols, len(SUPPLIES) + 3, row=19.5, prefill=[[s] for s in SUPPLIES])
    y = p.section_title(p.M, y, "How many boxes? A rough guide", width=p.CW)
    guide = [("Studio", "15-25"), ("1 bed", "25-40"), ("2 bed", "40-60"), ("3 bed", "60-80"), ("4+ bed", "80-120")]
    gw = p.CW / 6
    for i, (h, n) in enumerate(guide):
        x = p.M + i * gw
        p.box(x + 2, y + 6, gw - 6, 42)
        p.caps(x + gw / 2 - 2, y - 8, h, MUTED, 6.5, "center")
        p.text(x + gw / 2 - 2, y - 26, n, "Serif-Bold", 13, INK, "center")
    x = p.M + 5 * gw
    p.box(x + 2, y + 6, gw - 2, 42, fill=None, stroke=CLAY)
    p.caps(x + gw / 2, y - 8, "My estimate", CLAY, 6.5, "center")
    p.tfield(x + 8, y - 30, gw - 14, 16, size=12)
    p.fill_notes(y - 56, "Where to get free boxes / notes")


def p_roomkey(p):
    y = p.page("roomkey", "Room Key", "Declutter & Pack",
               "One code + one color per room. Use them on labels, signs and the box inventory.")
    w = p.CW
    cols = [("Color", 52, "static"), ("Code", 52, "text"), ("Room", 150, "text"),
            ("Where in new home (floor / door)", w - 52 - 52 - 150 - 64, "text"), ("# Boxes", 64, "text")]
    rows = len(ROOMS) + 4
    row = 30
    top = y
    # draw table manually so we can prefill editable values
    p.check_room(y, (rows + 1) * row)
    cx = p.M
    for h, cw, _ in cols:
        p.caps(cx + 2, y, h)
        cx += cw
    y -= 6
    p.hline(p.M, p.M + w, y, INK, 0.7)
    for r in range(rows):
        y -= row
        cx = p.M
        if r < len(ROOMS):
            code, name, col = ROOMS[r]
            p.c.setFillColor(HexColor(col))
            p.c.roundRect(cx + 4, y + 6, 40, row - 12, 4, stroke=0, fill=1)
        else:
            code, name = "", ""
            p.c.setStrokeColor(LINE)
            p.c.setDash(2, 2)
            p.c.roundRect(cx + 4, y + 6, 40, row - 12, 4, stroke=1, fill=0)
            p.c.setDash()
        cx += cols[0][1]
        p.tfield(cx + 2, y + 7, cols[1][1] - 6, 16, size=12, value=code)
        cx += cols[1][1]
        p.tfield(cx + 2, y + 7, cols[2][1] - 6, 16, size=10, value=name)
        cx += cols[2][1]
        p.tfield(cx + 2, y + 7, cols[3][1] - 6, 16, size=9)
        cx += cols[3][1]
        p.tfield(cx + 2, y + 7, cols[4][1] - 6, 16, size=10)
        p.hline(p.M, p.M + w, y)
    y -= 22
    y = p.tip(p.M, y, p.CW, "Number boxes per room (K-01, K-02 ...) or straight through the whole house (1, 2, 3 ...). Just stick to one system. Write the number on the top and two sides of every box.", "How")
    p.fill_notes(y, "Rooms that need special care")


def p_roompack(p):
    y = p.page("roompack", "Room Packing Checklist", "Declutter & Pack", "Print one for each room.")
    third = (p.CW - 32) / 3
    p.field_line(p.M, y, third * 2 + 16, "Room", 40)
    p.field_line(p.M + third * 2 + 32, y, third, "Code", 40)
    y -= 30
    y = p.section_title(p.M, y, "Steps", width=p.CW)
    y = p.checklist(p.M, y, p.CW, ROOM_TASKS, row=19, blanks=2)
    half = (p.CW - 24) / 2
    p.section_title(p.M, y, "Special items / fragile", width=half)
    p.section_title(p.M + half + 24, y, "Box numbers for this room", width=half)
    y -= 4
    n = int((y - p.bottom) // 19)
    p.lines(p.M, y, half, n)
    # box number grid
    gx = p.M + half + 24
    cols, cw = 6, half / 6
    rows = n
    for r in range(rows):
        for ci in range(cols):
            x = gx + ci * cw
            yy = y - (r + 1) * 19
            p.c.setStrokeColor(LINE)
            p.c.setLineWidth(0.6)
            p.c.rect(x, yy, cw, 19, stroke=1, fill=0)
            p.tfield(x + 2, yy + 3, cw - 4, 13, size=8)


def p_inventory(p, key, start):
    y = p.page(key, "Box Inventory", "Declutter & Pack",
               f"Boxes {start} to {start + 25}. Tick boxes off on moving day, then again when unpacked.")
    w = p.CW
    cols = [("#", 32, "static"), ("Room", 52, "text"), ("Contents", w - 32 - 52 - 3 * 50, "text"),
            ("Fragile", 50, "check"), ("Arrived", 50, "check"), ("Unpacked", 50, "check")]
    p.table(p.M, y, cols, 26, row=22, number_from=start)


def p_essentials(p):
    y = p.page("essentials", "Open-First Box", "Declutter & Pack",
               "Everything you need for the first night and morning. This box travels with you.")
    colw = (p.CW - 2 * 16) / 3
    groups = list(ESSENTIALS.items())
    for row in range(2):
        ybot = y
        for ci in range(3):
            h, items = groups[row * 3 + ci]
            x = p.M + ci * (colw + 16)
            p.box(x, y + 8, colw, 30)
            p.text(x + 10, y - 9, h, "Serif-Bold", 12)
            yy = p.checklist(x + 4, y - 36, colw - 4, items, row=18.5, blanks=2)
            ybot = min(ybot, yy)
        y = ybot - 12
    y = p.tip(p.M, y, p.CW, "Label this box OPEN FIRST on every side, and load it last so it comes off the truck first. Better still, take it in your car.", "Tip")
    p.fill_notes(y, "Also pack for")


def p_kidspets(p):
    y = p.page("kidspets", "Kids & Pets", "Declutter & Pack", "A calm move for the smallest (and furriest) movers.")
    half = (p.CW - 24) / 2
    for i, (h, items, fields) in enumerate([
        ("Kids", KIDS, ["New school", "School contact", "Sitter (moving day)", "Phone"]),
        ("Pets", PETS, ["New vet", "Vet phone", "Pet sitter", "Phone"]),
    ]):
        x = p.M + i * (half + 24)
        p.box(x, y + 8, half, 30)
        p.text(x + 10, y - 9, h, "Serif-Bold", 12.5)
        yy = p.checklist(x + 4, y - 38, half - 4, items, row=21, blanks=2)
        yy -= 6
        for f in fields:
            p.field_line(x, yy, half, f, 96)
            yy -= 22
        yy -= 6
        p.caps(x, yy, "Notes", MUTED)
        n = int((yy - p.bottom) // 19)
        p.lines(x, yy + 6, half, n)


def two_col_groups(p, y, groups, row=17.5):
    colw = (p.CW - 24) / 2
    keys = list(groups.keys())
    # balance columns by item count
    best, split = None, 1
    for s in range(1, len(keys)):
        a = sum(len(groups[k]) + 3 for k in keys[:s])
        b = sum(len(groups[k]) + 3 for k in keys[s:])
        if best is None or max(a, b) < best:
            best, split = max(a, b), s
    ys = []
    for ci, ks in enumerate([keys[:split], keys[split:]]):
        x = p.M + ci * (colw + 24)
        yy = y
        for k in ks:
            yy = p.section_title(x, yy, k, width=colw)
            yy = p.checklist(x, yy, colw, groups[k], row=row, blanks=1) - 6
        ys.append(yy)
    return min(ys)


def p_clean_out(p):
    y = p.page("cleanout", "Move-Out Cleaning", "Clean & Settle", "Get the deposit back: clean top to bottom, room by room.")
    y = two_col_groups(p, y, CLEAN_OUT, row=18.5)
    y = p.tip(p.M, y - 4, p.CW, "Before you hand back the keys, take a dated photo or video of every room. It's your best evidence if the deposit is disputed.", "Tip")
    p.fill_notes(y, "Repairs to do before leaving")


def p_clean_in(p):
    y = p.page("cleanin", "Move-In Cleaning", "Clean & Settle", "Clean and check before the furniture goes in. It's much easier with empty rooms.")
    y = two_col_groups(p, y, CLEAN_IN, row=18.5)
    y = p.tip(p.M, y - 4, p.CW, "Clean top to bottom (ceiling fans, then counters, then floors) and from the back of the room toward the door.", "Tip")
    p.fill_notes(y, "Things to fix or replace")


def p_walkthrough(p):
    y = p.page("walkthrough", "Walk-Through Report", "Clean & Settle",
               "Record condition on move-in and move-out. G = good, F = fair, D = damaged. Take photos!")
    half = (p.CW - 24) / 2
    p.field_line(p.M, y, half, "Address", 56)
    p.field_line(p.M + half + 24, y, half / 2 - 6, "Date", 30)
    p.field_line(p.M + half + 24 + half / 2 + 6, y, half / 2 - 6, "With", 30)
    y -= 22
    p.caps(p.M, y, "Report type", MUTED)
    for i, t in enumerate(["Move-in", "Move-out"]):
        x = p.M + 72 + i * 80
        p.checkbox(x, y - 1)
        p.text(x + 13, y, t, "Sans", 8.8)
    y -= 24
    w = p.CW
    cols = [("Room", 100, "text"), ("Walls", 44, "text"), ("Floor", 44, "text"), ("Windows", 48, "text"),
            ("Fixtures", 48, "text"), ("Notes / damage", w - 100 - 44 - 44 - 48 - 48 - 44, "text"), ("Photo", 44, "check")]
    y = p.table(p.M, y, cols, len(WALK_ROOMS), row=24.5, prefill=[[r] for r in WALK_ROOMS])
    p.field_line(p.M, y - 8, half, "Tenant signature", 92)
    p.field_line(p.M + half + 24, y - 8, half, "Landlord / agent", 92)
    p.fill_notes(y - 34, "Damage details")


def p_layout(p):
    y = p.page("layout", "Furniture Layout", "Clean & Settle",
               "Plan where things go. Each dot spacing = 1 ft (or 0.5 m). Measure first!")
    third = (p.CW - 32) / 3
    p.field_line(p.M, y, third, "Room", 36)
    p.field_line(p.M + third + 16, y, third, "Size", 30)
    p.field_line(p.M + 2 * third + 32, y, third, "Ceiling", 46)
    y -= 18
    step = 18
    cols = int(p.CW // step)
    rows = int((y - p.bottom - 8) // step)
    gx = p.M + (p.CW - cols * step) / 2
    p.c.setFillColor(LINE)
    for r in range(rows + 1):
        for ci in range(cols + 1):
            p.c.circle(gx + ci * step, y - r * step, 0.9, stroke=0, fill=1)


def p_neighborhood(p):
    y = p.page("neighborhood", "New Home & Neighborhood", "Clean & Settle", "The details you'll need, all in one place.")
    colw = (p.CW - 24) / 2
    groups = NEIGHBORHOOD
    for ci, gs in enumerate([groups[:2], groups[2:]]):
        x = p.M + ci * (colw + 24)
        yy = y
        for g, items in gs:
            yy = p.section_title(x, yy, g, width=colw)
            for it in items:
                p.field_line(x, yy, colw, it, 116)
                yy -= 21
            yy -= 8
        p.fill_notes(yy, "Notes" if ci else "Also nearby", x, colw, 21)


def p_notes(p):
    y = p.page("notes", "Notes", "Clean & Settle")
    n = int((y - p.bottom + 10) // 21)
    p.lines(p.M, y + 12, p.CW, n, 21)


def p_homesearch(p):
    y = p.page("homesearch", "Home Search", "Plan", "Compare the places you view. Score each one 1 to 5.")
    lw = 118
    cw = (p.CW - lw) / 3
    rows = ["Address", "Rent / price", "Beds / baths", "Size (sq ft / m\u00b2)", "Move-in date",
            "Commute", "Schools", "Parking", "Outdoor space", "Storage", "Pets allowed?",
            "Bills included?", "Neighborhood feel", "Pros", "Cons", "Score (1-5)"]
    cols = [("", lw, "static")] + [(f"Home {c}", cw, "text") for c in "ABC"]
    y = p.table(p.M, y, cols, len(rows), row=24, prefill=[[r] for r in rows])
    p.fill_notes(y, "Questions to ask at viewings")


def p_receipts(p):
    y = p.page("receipts", "Receipt Tracker", "Admin",
               "Log every moving expense. Some moving costs may be tax-deductible or reimbursable by your employer.")
    w = p.CW
    cols = [("Date", 56, "text"), ("Store / company", 120, "text"), ("What for", w - 56 - 120 - 80 - 64 - 2 * 44, "text"),
            ("Category", 80, "text"), ("Amount", 64, "text"), ("Kept", 44, "check"), ("Claim", 44, "check")]
    rows = int((y - p.bottom - 46) // 21.5)
    y = p.table(p.M, y, cols, rows, row=21.5)
    p.c.setFillColor(SAND)
    p.c.roundRect(p.M, y - 18, w, 30, 5, stroke=0, fill=1)
    p.text(p.M + 10, y - 6, "Page total", "Serif-Bold", 13)
    p.tfield(p.M + w - 64 - 88, y - 10, 70, 14, size=10)


def p_goodbye(p):
    y = p.page("goodbye", "Saying Goodbye", "Timeline",
               "Leave well. The people, places and last moments you don't want to miss.")
    half = (p.CW - 24) / 2
    p.section_title(p.M, y, "People to see", width=half)
    p.section_title(p.M + half + 24, y, "Places to visit one last time", width=half)
    y -= 20
    p.checklist(p.M, y, half, [], row=20, blanks=9)
    y = p.checklist(p.M + half + 24, y, half, [], row=20, blanks=9)
    y = p.section_title(p.M, y - 4, "Photos to take before we go", width=p.CW)
    shots = ["Each room, furnished", "The front door & street", "Height marks / kids' doorframe",
             "The view from the window", "Favorite corner of the garden", "Neighbors & friends"]
    p.checklist(p.M, y, half, shots[:3], row=20, blanks=1)
    y = p.checklist(p.M + half + 24, y, half, shots[3:], row=20, blanks=1)
    y = p.section_title(p.M, y - 4, "Gifts & thank-yous", width=p.CW)
    cols = [("For", 150, "text"), ("Gift / note", p.CW - 150 - 50, "text"), ("Done", 50, "check")]
    y = p.table(p.M, y, cols, 4, row=21)
    p.fill_notes(y, "Favorite memories of this home")


def p_measure(p):
    y = p.page("measure", "Measurements & Paint", "Clean & Settle",
               "Measure once and you won't buy a sofa that doesn't fit through the door.")
    w = p.CW
    cols = [("Room", 96, "text"), ("Item (wall, window, door...)", w - 96 - 3 * 64, "text"), ("Width", 64, "text"),
            ("Height", 64, "text"), ("Depth", 64, "text")]
    y = p.table(p.M, y, cols, 12, row=21)
    y = p.section_title(p.M, y, "Paint index", width=w)
    cols = [("Room / wall", 110, "text"), ("Brand", 90, "text"), ("Color name & code", w - 110 - 90 - 70 - 60, "text"),
            ("Finish", 70, "text"), ("Qty", 60, "text")]
    rows = int((y - p.bottom) // 21) - 1
    p.table(p.M, y, cols, rows, row=21)


def p_shopping(p):
    y = p.page("shopping", "New Home Shopping List", "Clean & Settle", "What to buy for the new place, room by room, within budget.")
    w = p.CW
    cols = [("Item", w - 90 - 70 - 70 - 44, "text"), ("Room", 90, "text"), ("Budget", 70, "text"),
            ("Paid", 70, "text"), ("Bought", 44, "check")]
    rows = int((y - p.bottom - 46) // 21.5)
    y = p.table(p.M, y, cols, rows, row=21.5)
    p.c.setFillColor(SAND)
    p.c.roundRect(p.M, y - 18, w, 30, 5, stroke=0, fill=1)
    p.text(p.M + 10, y - 6, "Total", "Serif-Bold", 13)
    p.tfield(p.M + w - 44 - 140, y - 10, 66, 14, size=10)
    p.tfield(p.M + w - 44 - 70, y - 10, 66, 14, size=10)


# ---------------------------------------------------------------- labels
def draw_label(p, x, y, w, h, code, room, color):
    c = p.c
    c.setStrokeColor(LINE)
    c.setLineWidth(0.6)
    c.setDash(3, 3)
    c.roundRect(x, y - h, w, h, 8, stroke=1, fill=0)
    c.setDash()
    band = 46
    if color:
        c.setFillColor(HexColor(color))
        c.roundRect(x + 6, y - band - 6, w - 12, band, 5, stroke=0, fill=1)
    else:
        c.setStrokeColor(LINE)
        c.roundRect(x + 6, y - band - 6, w - 12, band, 5, stroke=1, fill=0)
    if code:
        p.text(x + 18, y - 42, code, "Serif-Bold", 30, INK)
        p.text(x + w - 16, y - 34, room.upper(), "Sans-Bold", 10, INK, "right")
    else:
        p.tfield(x + 14, y - 44, 70, 30, size=24)
        p.tfield(x + 90, y - 40, w - 108, 18, size=11)
    yy = y - band - 24
    p.caps(x + 12, yy, "Box #", MUTED)
    p.hline(x + 46, x + w / 2 - 6, yy - 2)
    p.tfield(x + 46, yy - 1, w / 2 - 54, size=11)
    p.caps(x + w / 2 + 4, yy, "Of", MUTED)
    p.hline(x + w / 2 + 22, x + w - 12, yy - 2)
    p.tfield(x + w / 2 + 22, yy - 1, w / 2 - 34, size=11)
    yy -= 18
    p.caps(x + 12, yy, "Contents", MUTED)
    for i in range(3):
        yy -= 15
        p.hline(x + 12, x + w - 12, yy - 2)
        p.tfield(x + 12, yy - 1, w - 24, 12, size=8)
    yy -= 18
    for i, t in enumerate(["Fragile", "Open first", "Heavy"]):
        bx = x + 12 + i * (w - 24) / 3
        p.checkbox(bx, yy - 1, 8)
        p.text(bx + 12, yy, t, "Sans", 8)


def p_labels(p, idx):
    if idx < len(ROOMS):
        code, room, col = ROOMS[idx]
        title = f"Box Labels: {room}"
    else:
        code, room, col = "", "", None
        title = "Box Labels: Blank"
    y = p.page(f"labels{idx}", title, "Labels & Signs", "Cut along the dashed lines. Tape one on the top and one on the side of each box.")
    cols, rows, gap = 2, 4, 12
    w = (p.CW - gap) / cols
    h = (y - p.bottom + 2 - gap * (rows - 1)) / rows
    for r in range(rows):
        for ci in range(cols):
            draw_label(p, p.M + ci * (w + gap), y + 10 - r * (h + gap), w, h, code, room, col)


def p_signs(p, key, rooms, title):
    y = p.page(key, title, "Labels & Signs", "Tape these to the doors of your new home so the movers know where each box goes.")
    cols, rows, gap = 2, 2, 14
    w = (p.CW - gap) / cols
    h = (y - p.bottom + 2 - gap) / rows
    c = p.c
    for i, (code, room, col) in enumerate(rooms):
        r, ci = divmod(i, cols)
        x = p.M + ci * (w + gap)
        top = y + 10 - r * (h + gap)
        c.setStrokeColor(LINE)
        c.setDash(3, 3)
        c.roundRect(x, top - h, w, h, 10, stroke=1, fill=0)
        c.setDash()
        if col:
            c.setFillColor(HexColor(col))
            c.roundRect(x + 10, top - h + 10, w - 20, h - 20, 8, stroke=0, fill=1)
            c.setFillColor(white)
            c.roundRect(x + 26, top - h + 26, w - 52, h - 52, 6, stroke=0, fill=1)
            p.text(x + w / 2, top - h / 2 + 4, code, "Serif-Bold", 72, INK, "center")
            p.text(x + w / 2, top - h / 2 - 34, room.upper(), "Sans-Bold", 13, INK, "center", spacing=1.6)
        else:
            c.setStrokeColor(LINE)
            c.roundRect(x + 10, top - h + 10, w - 20, h - 20, 8, stroke=1, fill=0)
            p.tfield(x + 30, top - h / 2 - 16, w - 60, 70, size=60)
            p.tfield(x + 30, top - h / 2 - 46, w - 60, 20, size=13)


SPECIAL = [("FRAGILE", "Handle with care", "#E9B49E"), ("OPEN FIRST", "Essentials inside", "#A9C5B2"),
           ("THIS SIDE UP", "↑  ↑  ↑", "#EBD394"), ("HEAVY", "Lift with two people", "#C2C3BA"),
           ("DO NOT MOVE", "Stays in the house", "#CBB8D8"), ("LOAD LAST", "Unload first", "#A9C0D8"),
           ("KEEP WITH ME", "Do not load on truck", "#9ED2CD"), ("DONATE", "Not moving with us", "#D9C4A7"),
           ("FRAGILE", "Handle with care", "#E9B49E"), ("OPEN FIRST", "Essentials inside", "#A9C5B2"),
           ("THIS SIDE UP", "↑  ↑  ↑", "#EBD394"), ("FRAGILE", "Handle with care", "#E9B49E")]


def p_special(p):
    y = p.page("special", "Special Labels", "Labels & Signs", "Cut out and tape on boxes that need extra care.")
    cols, rows, gap = 3, 4, 10
    w = (p.CW - gap * (cols - 1)) / cols
    h = (y - p.bottom + 2 - gap * (rows - 1)) / rows
    c = p.c
    for i, (t, s, col) in enumerate(SPECIAL):
        r, ci = divmod(i, cols)
        x = p.M + ci * (w + gap)
        top = y + 10 - r * (h + gap)
        c.setStrokeColor(LINE)
        c.setDash(3, 3)
        c.roundRect(x, top - h, w, h, 8, stroke=1, fill=0)
        c.setDash()
        c.setFillColor(HexColor(col))
        c.roundRect(x + 7, top - h + 7, w - 14, h - 14, 6, stroke=0, fill=1)
        fs = 20
        while pdfmetrics.stringWidth(t, "Sans-Bold", fs) > w - 30:
            fs -= 1
        p.text(x + w / 2, top - h / 2 + 2, t, "Sans-Bold", fs, INK, "center")
        p.text(x + w / 2, top - h / 2 - 18, s, "Sans", 8.6, INK, "center")


# =================================================================== assemble
def build(path, pagesize):
    p = Planner(path, pagesize)
    plan = [
        ("cover", None, None, p_cover),
        ("contents", "Contents", "Plan", None),
        ("howto", "How to use this planner", "Plan", p_howto),
        ("glance", "Move at a glance", "Plan", p_glance),
        ("homesearch", "Home search", "Plan", p_homesearch),
        ("countdown", "8-week countdown", "Plan", p_countdown),
        ("w8", "8 weeks before", "Timeline", lambda p: p_week(p, "w8", "8 weeks", TIMELINE["8 weeks"])),
        ("w6", "6 weeks before", "Timeline", lambda p: p_week(p, "w6", "6 weeks", TIMELINE["6 weeks"])),
        ("w4", "4 weeks before", "Timeline", lambda p: p_week(p, "w4", "4 weeks", TIMELINE["4 weeks"])),
        ("w2", "2 weeks before", "Timeline", lambda p: p_week(p, "w2", "2 weeks", TIMELINE["2 weeks"])),
        ("w1", "1 week + day before", "Timeline",
         lambda p: p_week(p, "w1", "1 week", TIMELINE["1 week"], ("The day before", DAY_BEFORE))),
        ("goodbye", "Saying goodbye", "Timeline", p_goodbye),
        ("movingday", "Moving day", "Timeline", p_movingday),
        ("after", "After the move", "Timeline", p_after),
        ("budget", "Moving budget", "Admin", p_budget),
        ("receipts", "Receipt tracker", "Admin", p_receipts),
        ("quotes", "Mover quotes", "Admin", p_quotes),
        ("address", "Change of address", "Admin", p_address),
        ("utilities", "Utilities", "Admin", p_utilities),
        ("contacts", "Important contacts", "Admin", p_contacts),
        ("declutter", "Declutter tracker", "Declutter & Pack", p_declutter),
        ("sell", "Sell, gift & donate log", "Declutter & Pack", p_sell_log),
        ("supplies", "Packing supplies", "Declutter & Pack", p_supplies),
        ("roomkey", "Room key (codes & colors)", "Declutter & Pack", p_roomkey),
        ("roompack", "Room packing checklist", "Declutter & Pack", p_roompack),
        ("inv1", "Box inventory 1 to 26", "Declutter & Pack", lambda p: p_inventory(p, "inv1", 1)),
        ("inv2", "Box inventory 27 to 52", "Declutter & Pack", lambda p: p_inventory(p, "inv2", 27)),
        ("inv3", "Box inventory 53 to 78", "Declutter & Pack", lambda p: p_inventory(p, "inv3", 53)),
        ("essentials", "Open-first box", "Declutter & Pack", p_essentials),
        ("kidspets", "Kids & pets", "Declutter & Pack", p_kidspets),
        ("cleanout", "Move-out cleaning", "Clean & Settle", p_clean_out),
        ("cleanin", "Move-in cleaning", "Clean & Settle", p_clean_in),
        ("walkthrough", "Walk-through report", "Clean & Settle", p_walkthrough),
        ("measure", "Measurements & paint", "Clean & Settle", p_measure),
        ("layout", "Furniture layout", "Clean & Settle", p_layout),
        ("shopping", "New home shopping list", "Clean & Settle", p_shopping),
        ("neighborhood", "New home & neighborhood", "Clean & Settle", p_neighborhood),
        ("notes", "Notes", "Clean & Settle", p_notes),
    ]
    for i in range(len(ROOMS) + 1):
        name = ROOMS[i][1] if i < len(ROOMS) else "Blank (your colors)"
        plan.append((f"labels{i}", f"Box labels: {name}", "Labels & Signs", lambda p, i=i: p_labels(p, i)))
    plan += [
        ("signs1", "Room door signs 1", "Labels & Signs", lambda p: p_signs(p, "signs1", ROOMS[:4], "Room Door Signs")),
        ("signs2", "Room door signs 2", "Labels & Signs", lambda p: p_signs(p, "signs2", ROOMS[4:], "Room Door Signs")),
        ("signs3", "Blank door signs", "Labels & Signs",
         lambda p: p_signs(p, "signs3", [("", "", None)] * 4, "Blank Door Signs")),
        ("special", "Special labels", "Labels & Signs", p_special),
    ]
    toc = [(t, k, i + 1, s) for i, (k, t, s, _) in enumerate(plan) if t and k != "contents"]
    for i, (k, t, s, fn) in enumerate(plan):
        if k == "contents":
            p_contents(p, toc)
        else:
            fn(p)
        if t:
            p.c.addOutlineEntry(t, k, level=0)
    p.save()
    for o in p.overflows:
        print("  OVERFLOW", o)
    return len(plan)


def build_readme(path):
    p = Planner(path, letter)
    p.c.setTitle("The Calm Move: Quick Start")
    y = p.page("contents", "Quick Start", "Plan", "Thank you for your purchase! Here's how to get the most from your planner.")
    blocks = [
        ("Your files", "The-Calm-Move-Moving-Planner-US-Letter.pdf for US / Canada paper, and "
                       "The-Calm-Move-Moving-Planner-A4.pdf for A4 paper (UK, EU, Australia and most other countries). "
                       "Both have the same 51 pages."),
        ("To type into it", "Open the PDF in Adobe Acrobat Reader (free), Apple Preview, Xodo or Microsoft Edge. "
                            "Click a line to type and click a box to tick it. Save often. Some phone and browser "
                            "previewers can't fill forms, so if typing doesn't work, open the file in Acrobat Reader."),
        ("To write by hand on a tablet", "Import the PDF into GoodNotes, Notability or Noteshelf. The contents "
                                         "page and the 'Contents' link on every page are clickable, so you can jump around."),
        ("To print", "Choose 'Actual size' or 100% scale (not 'Fit'). Print only the pages you need, and print "
                     "extra copies of the room packing checklist, box inventory and box labels as you go. Labels "
                     "and signs look best in color; everything else prints well in black and white."),
        ("Box labels tip", "Print labels on sticker paper (full-sheet label paper), or on plain paper and attach "
                           "them with clear packing tape. Put one on top and one on the side of each box."),
        ("Terms of use", "For personal use only. Please don't share, resell or redistribute the files. "
                         "No physical item will be shipped."),
    ]
    for h, body in blocks:
        p.text(p.M, y, h, "Serif-Bold", 13)
        y = p.para(p.M, y - 17, body, p.CW, 9.6, color=MUTED) - 14
    p.tip(p.M, y, p.CW, "Questions or a problem with your files? Message me through Etsy and I'll help. "
                        "If the planner made your move calmer, a review means the world to a small shop.", "Help")
    p.save()


if __name__ == "__main__":
    os.makedirs(DIST, exist_ok=True)
    for label, size in [("US-Letter", letter), ("A4", A4)]:
        out = os.path.join(DIST, f"The-Calm-Move-Moving-Planner-{label}.pdf")
        n = build(out, size)
        print(f"{out}  ({n} pages, {os.path.getsize(out) // 1024} KB)")
    build_readme(os.path.join(DIST, "READ-ME-Quick-Start.pdf"))
