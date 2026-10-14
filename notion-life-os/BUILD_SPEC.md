# Atelier Life OS — Notion Build Spec

Working title: **Atelier Life OS** (rename freely before launch).
Look: warm editorial — cream backgrounds, serif headings, muted brown/sage accents.
Goal: an original, fully linked "life OS" Notion template to sell on Etsy. Inspired by the
*category* of all-in-one life hubs, but with original naming, structure, layouts and copy.

> **For the Claude session that builds this:** use the Notion connector. Create one top-level
> page "Atelier Life OS", then build in this order: databases (section 2, in listed order so
> relations resolve), then pages (section 3), then sample data (section 4). Anything the
> connector cannot do (buttons, some view types, progress-bar display) goes into the
> "Finishing checklist" page (section 5) — do not skip silently.

---

## 1. Structure

```
Atelier Life OS (Hub)
├── ✦ Start Here (quick start, FAQ)
├── ☀ Today
├── ◎ Plan        → Life Areas, Goals, Projects, Tasks, Reviews
├── ✎ Mind        → Journal, Daily Log (habits/mood), Library, Ideas & Inspo
├── ❦ Body & Home → Workouts, Recipes, Meal Plan, Home Care
├── $ Money       → Transactions, Budget Categories, Subscriptions, Money Goals
├── ⌂ Life Admin  → Contacts, Documents, Trips, Lists
└── ▤ Databases   (all source databases live here; module pages use linked views)
```

All source databases live under **Databases** so module pages stay clean and buyers can't
accidentally delete a source DB from a dashboard.

---

## 2. Databases

Notation: `Name (type)`; formulas use Notion Formulas 2.0.

### Plan

**1. Life Areas**
- Name (title)
- Vision (text) — "What does a great life look like here?"
- Satisfaction (number, 1–10)
- Goals (relation → Goals, two-way "Area")
- Projects (relation → Projects, two-way "Area")
- Journal (relation → Journal, two-way "Area")
- Active Goals (formula): `prop("Goals").filter(current.prop("Status") == "In progress").length()`
- Balance (formula): `"●".repeat(prop("Satisfaction")) + "○".repeat(10 - prop("Satisfaction"))`

Seed rows: Health, Mind, Relationships, Career, Money, Home, Fun & Creativity, Growth.

**2. Goals**
- Name (title)
- Area (relation → Life Areas)
- Status (status): Not started / In progress / Paused / Achieved
- Horizon (select): This quarter, This year, 3 years, Someday
- Target date (date)
- Why it matters (text)
- Projects (relation → Projects, two-way "Goal")
- Tasks (relation → Tasks, two-way "Goal")
- Progress (formula):
  ```
  let(total, prop("Tasks").length(),
      done, prop("Tasks").filter(current.prop("Done")).length(),
      if(total == 0, 0, round(done / total * 100) / 100))
  ```
- Progress Bar (formula):
  ```
  let(p, round(prop("Progress") * 10),
      "▰".repeat(p) + "▱".repeat(10 - p) + "  " + format(round(prop("Progress") * 100)) + "%")
  ```

**3. Projects**
- Name (title)
- Goal (relation → Goals)
- Area (relation → Life Areas)
- Status (status): Planning / Active / On hold / Done
- Dates (date, range)
- Tasks (relation → Tasks, two-way "Project")
- Notes (text)
- Progress / Progress Bar (formulas — same as Goals)

**4. Tasks**
- Name (title)
- Done (checkbox)
- Do date (date)
- Priority (select): High, Medium, Low
- Energy (select): Deep focus, Light, Errand
- Project (relation → Projects)
- Goal (relation → Goals)
- Status Label (formula):
  ```
  ifs(prop("Done"), "✓ Done",
      empty(prop("Do date")), "Inbox",
      dateBetween(prop("Do date"), today(), "days") < 0, "⚠ Overdue",
      dateBetween(prop("Do date"), today(), "days") == 0, "Today",
      "Upcoming")
  ```

**5. Reviews**
- Name (title) — e.g. "Week 42 · 2026"
- Type (select): Weekly, Monthly, Quarterly
- Period (date, range)
- Wins (text)
- Lessons (text)
- Focus next (text)
- Score (number, 1–10)
- Page templates (one per Type) — see section 3.

### Mind

**6. Journal**
- Title (title)
- Date (date, default today)
- Type (select): Morning pages, Evening reflection, Gratitude, Free write, Dream
- Mood (select): ☀ Great, ⛅ Good, ☁ Okay, 🌧 Low, ⛈ Rough
- Area (relation → Life Areas)
- Tags (multi-select)
- Template "Evening reflection": prompts — *What went well? What drained me? One thing I'm grateful for. Tomorrow's one priority.*

**7. Daily Log** (habits + wellbeing, one row per day)
- Day (title) — e.g. "Tue 14 Oct"
- Date (date)
- Water (checkbox), Move (checkbox), Read (checkbox), Meditate (checkbox), No-phone morning (checkbox)
- Sleep (number, hours)
- Energy (number, 1–5)
- Mood (select: same options as Journal)
- Habit Score (formula):
  ```
  let(done, [prop("Water"), prop("Move"), prop("Read"), prop("Meditate"), prop("No-phone morning")]
            .filter(current).length(),
      round(done / 5 * 100) / 100)
  ```
- Habit Bar (formula): `"◆".repeat(round(prop("Habit Score") * 5)) + "◇".repeat(5 - round(prop("Habit Score") * 5))`

**8. Library** (books, films, podcasts, courses)
- Title (title)
- Type (select): Book, Audiobook, Film, Series, Podcast, Course
- Creator (text)
- Status (status): Want / In progress / Finished / Abandoned
- Rating (select): ★, ★★, ★★★, ★★★★, ★★★★★
- Started (date), Finished (date)
- Cover (files)
- Notes (text)

**9. Ideas & Inspo**
- Name (title)
- Kind (select): Idea, Quote, Image, Link, Vision board
- URL (url)
- Area (relation → Life Areas)
- Tags (multi-select)
- Image (files)

### Body & Home

**10. Workouts**
- Session (title)
- Date (date)
- Type (select): Strength, Cardio, Yoga, Walk, Sport, Mobility
- Minutes (number)
- Intensity (select): Easy, Moderate, Hard
- Notes (text)

**11. Recipes**
- Name (title)
- Meal (multi-select): Breakfast, Lunch, Dinner, Snack, Dessert
- Prep time (number, minutes)
- Tags (multi-select): Quick, Batch-cook, Vegetarian, High-protein, Favourite
- Source (url)
- Ingredients and Method go in the page body.

**12. Meal Plan**
- Day (title)
- Date (date)
- Breakfast (relation → Recipes, one-way)
- Lunch (relation → Recipes, one-way)
- Dinner (relation → Recipes, one-way)
- Notes (text)

**13. Home Care** (chores and maintenance)
- Task (title)
- Room (select): Kitchen, Bathroom, Bedroom, Living, Outdoor, Whole home, Car
- Kind (select): Chore, Maintenance, Deep clean
- Every (number, days)
- Last done (date)
- Next due (formula): `dateAdd(prop("Last done"), prop("Every"), "days")`
- Due Label (formula):
  ```
  let(d, dateBetween(prop("Next due"), today(), "days"),
      ifs(empty(prop("Last done")), "Set last done",
          d < 0, "⚠ " + format(abs(d)) + "d overdue",
          d == 0, "Due today",
          "In " + format(d) + "d"))
  ```

### Money

**14. Budget Categories**
- Category (title)
- Group (select): Essentials, Lifestyle, Savings, Income
- Monthly budget (number, currency)
- Transactions (relation → Transactions, two-way "Category")
- Spent this month (formula):
  ```
  prop("Transactions")
    .filter(formatDate(current.prop("Date"), "YYYY-MM") == formatDate(now(), "YYYY-MM"))
    .map(current.prop("Amount")).sum()
  ```
- Remaining (formula): `prop("Monthly budget") - prop("Spent this month")`
- Used (formula):
  ```
  let(p, if(prop("Monthly budget") == 0, 0, min(prop("Spent this month") / prop("Monthly budget"), 1)),
      "▰".repeat(round(p * 10)) + "▱".repeat(10 - round(p * 10)))
  ```

**15. Transactions**
- Description (title)
- Amount (number, currency; always positive)
- Type (select): Expense, Income
- Date (date)
- Category (relation → Budget Categories)
- Method (select): Card, Cash, Transfer
- Month (formula): `formatDate(prop("Date"), "MMMM YYYY")`

**16. Subscriptions**
- Name (title)
- Cost (number, currency)
- Cycle (select): Weekly, Monthly, Quarterly, Yearly
- Next renewal (date)
- Status (select): Active, Trial, Cancel soon, Cancelled
- Category (select): Streaming, Software, Fitness, News, Other
- Monthly cost (formula):
  ```
  ifs(prop("Cycle") == "Weekly", prop("Cost") * 52 / 12,
      prop("Cycle") == "Quarterly", prop("Cost") / 3,
      prop("Cycle") == "Yearly", prop("Cost") / 12,
      prop("Cost"))
  ```
- Yearly cost (formula): `prop("Monthly cost") * 12`
- Renews in (formula): `dateBetween(prop("Next renewal"), today(), "days")`

**17. Money Goals** (savings + debt payoff)
- Name (title)
- Kind (select): Savings, Debt payoff, Emergency fund, Investment
- Target (number, currency)
- Current (number, currency) — amount saved, or amount paid off for debt
- Target date (date)
- Progress (formula): `if(prop("Target") == 0, 0, min(prop("Current") / prop("Target"), 1))`
- Progress Bar (formula): `"▰".repeat(round(prop("Progress") * 10)) + "▱".repeat(10 - round(prop("Progress") * 10))`
- Per month needed (formula):
  ```
  let(m, dateBetween(prop("Target date"), today(), "months"),
      if(m <= 0, prop("Target") - prop("Current"), round((prop("Target") - prop("Current")) / m)))
  ```

### Life Admin

**18. Contacts**
- Name (title)
- Circle (select): Family, Friend, Work, Service provider
- Birthday (date)
- Phone (phone), Email (email)
- Last contacted (date)
- Notes (text) — gift ideas, kids' names, etc.
- Next birthday (formula):
  ```
  let(b, prop("Birthday"),
      nb, dateAdd(b, year(today()) - year(b), "years"),
      if(nb < today(), dateAdd(nb, 1, "years"), nb))
  ```
- Days to birthday (formula): `dateBetween(prop("Next birthday"), today(), "days")` (blank when no birthday)

**19. Documents**
- Name (title)
- Category (select): ID, Insurance, Health, Home, Car, Finance, Warranty, Education
- Expires (date)
- Where it lives (text) — "Drawer 2", "Google Drive/…"
- File (files)
- Expiry Label (formula):
  ```
  if(empty(prop("Expires")), "—",
     let(d, dateBetween(prop("Expires"), today(), "days"),
         ifs(d < 0, "⚠ Expired", d < 60, "Renew soon", "OK")))
  ```

**20. Trips**
- Trip (title)
- Destination (text)
- Dates (date, range)
- Status (select): Dreaming, Planning, Booked, Done
- Budget (number, currency)
- Page template: Itinerary (day-by-day), Bookings, Packing checklist.

**21. Lists** (shopping, wishlist, wardrobe, gifts)
- Item (title)
- List (select): Groceries, Household, Wishlist, Wardrobe, Gifts
- Got it (checkbox)
- Price (number, currency)
- Link (url)
- For (relation → Contacts, one-way) — for Gifts

---

## 3. Pages and views

Every module page: cover (cream/editorial), icon, one-line intro in italics, then a
two- or three-column layout of linked database views.

**Hub (top page)**
- Header quote callout: *"Small days, well kept, make a life."*
- Nav row (3 columns): links to Today, Plan, Mind / Body & Home, Money, Life Admin / Start Here, Reviews, Databases
- "This week" — Tasks, filter: not Done and Do date within this week; sort Do date
- "Goals in motion" — Goals gallery, filter Status = In progress, show Progress Bar
- "Life balance" — Life Areas table: Name, Satisfaction, Balance

**☀ Today** (phone-first: single column, short sections)
- Date + "One thing that would make today great:" (empty text block)
- Tasks — filter: not Done AND (Do date is today OR Status Label = Overdue); show Priority, Energy
- Daily Log — filter Date = today (card); note "Click + New to log today"
- Journal — "+ New entry" (button → checklist if unsupported); view filter Date = today
- Meals — Meal Plan, filter Date = today
- Subscriptions renewing in the next 7 days
- Birthdays in the next 14 days (Contacts, Days to birthday ≤ 14)

**◎ Plan**
- Life Areas — gallery
- Goals — board grouped by Status; second view: table grouped by Horizon
- Projects — board by Status
- Tasks — views: Inbox (no Do date), This week, Calendar, All
- Reviews — list, sorted by Period desc; templates:
  - **Weekly**: Wins · What didn't go to plan · Energy check (Daily Log for the week) · Inbox zero · Top 3 for next week
  - **Monthly**: Highlights · Money check (budget table) · Habit consistency · Goals on/off track · One thing to stop
  - **Quarterly**: Re-score every Life Area · Goal review (keep / change / drop) · Next quarter's 3 goals · Letter to future self

**✎ Mind**
- Journal — calendar view + list by Mood
- Habit tracker — Daily Log, table for this month with Habit Bar; and a chart view (if available) of Habit Score over time
- Library — gallery by Status ("Reading now", "Up next", "Finished this year")
- Ideas & Inspo — gallery titled "Vision board" (filter Kind = Vision board) + table for everything else

**❦ Body & Home**
- Workouts — calendar + table "This month" with Minutes sum
- Meal Plan — this week table; Recipes gallery (filter tags)
- Home Care — table sorted by Next due, grouped by Room; view "Due this week"
- Groceries — Lists, filter List = Groceries, not Got it

**$ Money**
- Callout: "Log every purchase in Transactions → it flows into your budget automatically."
- Budget — Budget Categories table: Category, Monthly budget, Spent this month, Remaining, Used (sum totals in footer)
- Transactions — table "This month" (Month = current month), grouped by Type
- Subscriptions — table sorted by Next renewal, footer sum Monthly cost / Yearly cost
- Money Goals — gallery with Progress Bar and Per month needed

**⌂ Life Admin**
- Contacts — table sorted by Days to birthday; view "Birthdays soon"
- Documents — table grouped by Category; view "Expiring soon"
- Trips — board by Status
- Lists — board grouped by List

**✦ Start Here**
1. Welcome (2 sentences on how the system thinks: *Areas → Goals → Projects → Tasks*).
2. 5-minute setup: (a) rename/score your Life Areas, (b) add one goal, (c) add today's tasks, (d) set your currency in Money, (e) delete sample data (checklist of which DBs hold samples).
3. Daily rhythm: open Today → log habits → tick tasks → 2-minute journal.
4. Weekly rhythm: Sunday weekly review template.
5. Using on your phone: add Today to Favourites.
6. FAQ: Do I need Notion Plus? (No — works on free.) How do I change habits? (Rename/add checkbox columns in Daily Log and update Habit Score formula.) How do I change currency? Can I share with a partner?
7. Support: "Questions? Message us through Etsy."

**▤ Databases** — plain page containing all 21 source databases (full-page DB children) with a note: *"Source data lives here. Dashboards show filtered views of these. Don't delete these."*

---

## 4. Sample data (enough to make screenshots look alive)

- Life Areas: 8 seeded rows with Satisfaction 4–8 and one-line visions.
- Goals: "Run a 10K" (Health, In progress), "Build a 3-month emergency fund" (Money, In progress), "Read 24 books" (Growth, In progress), "Redecorate the bedroom" (Home, Not started).
- Projects: "10K training plan" → Run a 10K; "Bedroom refresh" → Redecorate the bedroom.
- Tasks: 10 tasks spread over today/this week, half linked to projects, 3 done.
- Daily Log: last 7 days with varied checkboxes, sleep 6–8, energy 2–5.
- Journal: 3 entries (gratitude, evening reflection, free write).
- Library: 5 items across statuses (use generic/public-domain titles, e.g. *Pride and Prejudice*, *Meditations*).
- Recipes: 5 (Overnight oats, Chickpea traybake, Lemon pasta, Greek yoghurt bowl, Veggie curry). Meal Plan: this week.
- Workouts: 4 this month.
- Home Care: 8 chores with mixed Last done dates (one overdue).
- Budget Categories: Rent 1200, Groceries 400, Transport 150, Eating out 150, Fun 100, Savings 300, Salary (Income).
- Transactions: 12 this month across categories.
- Subscriptions: Streaming 12.99/mo, Music 10.99/mo, Cloud storage 29.99/yr, Gym 35/mo (Trial), News 5/wk.
- Money Goals: Emergency fund 6000 / 2150; Credit card payoff 1800 / 900; Japan trip 3500 / 600.
- Contacts: 5 fictional (birthday one within 10 days).
- Documents: Passport (expires within 60 days), Car insurance, Home insurance, Laptop warranty.
- Trips: "Lisbon weekend" (Planning), "Japan 2027" (Dreaming).
- Lists: groceries ×6, wishlist ×3, gift ×2 linked to a contact.

All sample people/brands are fictional or generic — no real brands, logos or people.

---

## 5. Finishing checklist (manual steps if the connector can't do them)

Create a page **"🛠 Finishing checklist (seller only — delete before publishing)"** listing every
item that could not be built via the connector, for example:

- [ ] Buttons: "+ Task", "+ Journal entry", "+ Log today", "+ Expense" on Today/Money
- [ ] Set number display to **bar** (or ring) for Progress formulas where wanted
- [ ] Chart views (Habit Score over time, spending by category) — Notion Charts
- [ ] Footer calculations (sums) on Money tables
- [ ] Database default templates (Reviews ×3, Journal evening reflection, Trips) set as default
- [ ] Covers + icons uploaded (light and dark sets)
- [ ] Hide source database titles on dashboard linked views; lock dashboard pages
- [ ] Share to web → Allow duplicate as template → copy link into the delivery PDF
- [ ] Test duplicate from a fresh free Notion account (desktop + phone)

---

## 6. Etsy package (after the Notion build)

- Delivery PDF: logo, duplicate link button, 5-minute setup, support note.
- 10 listing images (2000 px wide): hero, "what's inside" grid, Today on phone, Plan, Money,
  Habit tracker, Reviews, light vs dark, setup in 3 steps, tier comparison.
- Tiers: Lite (Today + Plan + Mind) · Complete · Bundle (Complete + both cover sets + Canva kit).
- Title, 13 tags and description from keyword research.
- Disclose AI-assisted creation in the description per Etsy's creativity standards.
