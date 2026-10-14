# Button and Template QA (Phase 9A)

## Status: INCOMPLETE (manual build required)

Re-checked 2026-10-14 in Phase 10: this session still has no browser or computer-use tool, the Notion connector's block format has no button block, and no connector tool creates database templates or sets page font or locking.

**Build kit in Notion:** "Template and button build kit (seller only)" under LifeOS SELLER NOTES holds all 11 template bodies as ready-made Notion blocks inside toggles (open, select all, copy, paste into the new template), a button table and a test checklist. It is outside the product and is not copied to buyers.

Order of work: build everything in the **dev master** first, test it, then regenerate both editions from the master (see `CUSTOMER_PACKAGE_INVENTORY.md`). The RC1 editions made in Phase 10 do not have buttons or templates and must be replaced. Nothing below has been built or tested. Every item stays **INCOMPLETE** until the owner builds it in the Notion app and records the result in the "Result" columns.

Build everything in the **dev copy** ("LifeOS - All-in-One Life Planner [DEV, do not sell]"), never in the original "Notion Life Hub". Buttons and templates are on Notion's free plan, but confirm that during the free-account duplication test (`CUSTOMER_DUPLICATION_QA.md`).

All option names below were read from the dev databases on 2026-10-14 (Journal Type, Reviews Type, Trips Status, Projects Status, Goals Status, Goals Measure, Transactions Type).

---

## Part 1: Buttons (4)

### How to make any button

1. On the page, type `/button` and press Enter.
2. Name the button and pick an icon.
3. Click **Add action** → **Add page to** → choose the database.
4. Click **Edit property** for each default below. For dates choose **Today** (the relative value), never a fixed calendar date.
5. Click **Add action** → **Open page** → choose the page from step 3, so the new row opens straight away.
6. Click **Done**.

### B1. Add task

| Field | Value |
|---|---|
| Placement | Hub → Quick actions callout (replace the "Add a task" text line) and top of Today |
| Database | Tasks |
| Action 1 | Add page to Tasks |
| Defaults | Do date = Today. Leave Done, Canceled, Project and Goal empty |
| Action 2 | Open page (the new task) |
| Expected result | A new untitled task opens with today's Do date and appears in Today → "Today & overdue" and Hub → "Due today and overdue" |
| Verification | 1) Click once. 2) In Databases → Tasks, confirm one new row, Do date = today, Status Label = "Today". 3) Click again: a second row appears (Notion buttons do not prevent duplicates). 4) Delete both test rows. |
| Result | INCOMPLETE |

### B2. New journal entry

| Field | Value |
|---|---|
| Placement | Hub → Quick actions and top of Today, next to Add task |
| Database | Journal |
| Action 1 | Add page to Journal |
| Defaults | Date = Today, Type = Evening reflection |
| Action 2 | Open page |
| Expected result | A new journal page opens. If template T5 exists and is the default, its prompts appear in the body |
| Verification | Click once; confirm the row in Databases → Journal has today's date and Type = Evening reflection, and that it shows under Mind → Journal. Delete the test row. |
| Result | INCOMPLETE |

### B3. Open today's log

| Field | Value |
|---|---|
| Placement | Hub → Quick actions and Today → Daily check-in |
| Database | Daily Log |
| Action 1 | Add page to Daily Log |
| Defaults | Date = Today. Leave Day blank and all habits unticked |
| Action 2 | Open page |
| Expected result | A new log row for today opens. Hub → "Today's habits" shows it with Habit Bar "◇◇◇◇◇" until habits are ticked |
| Known limit | Each click adds a new row. A button cannot check whether today's row already exists. Start Here says "Keep one row per date". Keep the label "Open today's log" and use it once a day |
| Verification | Click once; tick two habits; confirm Habit Bar shows "◆◆◇◇◇" and Hub → Today's habits lists the row. Delete the test row. |
| Result | INCOMPLETE |

### B4. Log expense

| Field | Value |
|---|---|
| Placement | Top of the Money page, under the intro callout |
| Database | Transactions |
| Action 1 | Add page to Transactions |
| Defaults | Type = Expense, Date = Today. Leave Category empty (the buyer picks it) |
| Action 2 | Open page |
| Expected result | A new expense opens. After Amount and Category are filled in, that category's Spent this month, Remaining and Budget status update |
| Verification | Click once; set Amount 10 and Category Groceries; confirm Money → Budget shows Groceries "On track: 187.45 left" (197.45 before). Delete the test row and confirm it returns to 197.45. |
| Result | INCOMPLETE |

After all four buttons work, update the Hub "Quick actions" callout so it no longer says "click New under …" for the actions that now have buttons. Re-fetch the Hub and check no em dashes were introduced.

---

## Part 2: Database templates (11)

### How to make any template

1. Open the database in **Databases** (full page).
2. Click the arrow next to **New** → **New template**.
3. Type the template name in the title field and set the properties listed.
4. Paste the body from `TEMPLATES_TO_CREATE.md`.
5. For date properties choose **Today** in the date picker so the date fills in when a page is created from the template.
6. To make it the default: arrow next to **New** → **•••** next to the template → **Set as default**.

| # | Database | Template name | Properties to set | Default? | Body source | Expected result | Verification | Result |
|---|---|---|---|---|---|---|---|---|
| T1 | Daily Log | Daily log | Date = Today | Yes | TEMPLATES_TO_CREATE.md → Daily Log | New log rows get today's date and the "One word for today" prompt | New → check date is today and body present; delete | INCOMPLETE |
| T2 | Reviews | Weekly review | Type = Weekly | Yes | → Reviews: Weekly | Five headings (Wins … Top 3 for next week) | New → Weekly review; check Type and headings; delete | INCOMPLETE |
| T3 | Reviews | Monthly review | Type = Monthly | No | → Reviews: Monthly | Five headings incl. Money check | Same as T2 | INCOMPLETE |
| T4 | Reviews | Quarterly review | Type = Quarterly | No | → Reviews: Quarterly | Four headings incl. Re-score your life areas | Same as T2 | INCOMPLETE |
| T5 | Journal | Evening reflection | Type = Evening reflection, Date = Today | Yes | → Journal: Evening reflection | Four H3 prompts | New → check Type, today's date, prompts; delete | INCOMPLETE |
| T6 | Journal | Morning pages | Type = Morning pages, Date = Today | No | → Journal: Morning pages | Free-writing prompt | Same as T5 | INCOMPLETE |
| T7 | Trips | Trip | Status = Planning | Yes | → Trips | Itinerary, Bookings and Packing sections | New → check Status = Planning; delete | INCOMPLETE |
| T8 | Recipes | Recipe | none | Yes | → Recipes | Ingredients, Method, Notes | New → check headings; delete | INCOMPLETE |
| T9 | Projects | Project | Status = Planning | Yes | → Projects | Outcome, Tasks, Notes | New → check Status; Progress Bar shows "No tasks linked yet"; delete | INCOMPLETE |
| T10 | Goals | Task goal | Measure = Tasks, Status = Not started | Yes | → Goals: Task goal | Why it matters, First three steps | New → Progress Bar "No tasks linked yet", Goal health "Not enough information"; delete | INCOMPLETE |
| T11 | Goals | Number goal | Measure = Number, Start value = 0, Status = Not started | No | → Goals: Number goal | Why it matters, How I'll measure it | New → Progress Bar "Set start and target values"; set Target 10, Current 5 → "▰▰▰▰▰▱▱▱▱▱  50%"; delete | INCOMPLETE |

The expected empty states in T9 to T11 were verified on 2026-10-14 with temporary records (see `FORMULA_TEST_RESULTS.md`, Phase 9B edge cases E-G3, E-G6). The templates themselves were not.

---

## Part 3: After building

1. Run every Verification above in the dev copy and fill in the Result column (PASS or FAIL, date, plan).
2. Regenerate the Blank edition from the master (see `CUSTOMER_PACKAGE_INVENTORY.md`). Templates and buttons copy with a duplicate, but confirm it in the Blank edition too.
3. Repeat B1 to B4 and T1, T5, T10 in the free-account duplication test.
