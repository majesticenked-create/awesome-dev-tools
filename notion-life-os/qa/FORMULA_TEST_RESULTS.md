# Formula Test Results

Status values: PASS, FAIL, BLOCKED, NOT TESTED, N/A. A formula being accepted by Notion at save time is **not** counted as a pass. Only a live value that equals an independently computed value is a PASS.

## Phase 9B summary (2026-10-14, dev copy)

| Set | Rows checked | Matched | Mismatched |
|---|---:|---:|---:|
| Sample data, all changed formulas (12 databases) | 79 | 79 | 0 |
| Edge cases with temporary records (12 databases) | 46 | 46 | 0 |
| Negative control (deliberately wrong expectation) | 1 | returned 0 rows, as it should | n/a |

No mismatches were found, so nothing needed investigating or re-running.

## When and where

- Run between 15:50 and 16:00 UTC on Wednesday 2026-10-14 (11:50 to 12:00 EDT). Every time zone from UTC−12 to UTC+7 was on 14 October for the whole run, so `today()` and `now()` gave the same date whichever zone Notion used.
- Target: the dev copy only. Production was not touched (see `PRODUCTION_INTEGRITY_CHECK.md`).

## Method

1. **Inputs**: raw properties (amounts, dates, checkboxes, statuses, relations) were read from the dev databases with view-mode queries. That mode has no plan quota. The inputs matched the documented sample data exactly.
2. **Expected values**: `tools/verify_dev_formulas.py` computes every expected value from those inputs with its own logic. It does not read any Notion formula. Its sample results also agree with the older `tools/expected_values.py`.
3. **Number and date formulas**: Notion's view filters cannot match number or date formula results (the API dropped such filters). So a temporary text formula **"zz QA probe"** was added to 9 dev databases. It writes the numbers and dates out as text, rounded to 2 or 4 places, for example `202.55|0|202.55|197.45`. Text formulas (Budget status, Used, Progress Bar, Goal health, Due, Expiry, Balance, Status Label, Habit Bar, Birthday soon, Due this week, Goal status) were filtered on directly.
4. **Check**: one linked view per database, on the seller-only "QA harness" page (outside the product). Each view's filter is an OR of one group per row: `(title = row AND formula = expected AND ...)`. Every filter was read back after saving to confirm none had been dropped. If the view returns every expected row, every value matches. A missing row would be a mismatch.
5. **Negative control**: a filter expecting Passport Expiry = "OK" (the true value is "Renew soon") returned 0 rows. This shows the filters really test the values.
6. **Clean-up**: the 53 temporary records (Life Areas 4, Contacts 5, Subscriptions 8, Money Goals 3, Home Care 3, Documents 5, Daily Log 1, Projects 1, Tasks 7, Goals 7, Budget Categories 2, Transactions 7) were moved out of the databases to the seller-only page "QA TEMP records (moved out of dev databases after testing)". All edge views then returned 0 rows. The sample values were re-checked and unchanged. The "zz QA probe" column was dropped from all 9 databases, and each schema was read back without it. Nothing was deleted: the delete tool may only be used when you ask for it, so the archived page is left for you to delete.

## Results on sample data (dev copy)

| ID | Formula(s) | Rows | Expected (summary) | Result |
|---|---|---:|---|---|
| F1 | Tasks.Status Label | 12 | Today 2, Upcoming 5, ✓ Done 3, ⚠ Overdue 1, Inbox 1 | PASS 12/12 |
| F2/F3 | Goals.Progress, Progress Bar, Goal health, rollups Tasks total/done/canceled, Projects count, Project progress | 5 | 10K and Emergency 50%; Read 24 books 58% (number goal 0→24, current 14); Bedroom 0%; Pottery "No tasks linked yet" / "Not enough information"; others "On track" | PASS 5/5 |
| F4 | Projects.Progress, Progress Bar, rollups | 3 | 50%, 50%, 0% (2/4/2 tasks) | PASS 3/3 |
| F5/F6 | Daily Log.Habits Done, Habit Bar | 7 | 3, 2, 5, 4, 3, 1, 3 and matching ◆ bars | PASS 7/7 |
| F7 | Life Areas.Balance | 8 | Dots equal to Satisfaction | PASS 8/8 |
| F8/F9 | Home Care.Next due, Due | 8 | e.g. Clean bathroom 2026-10-11 "⚠ 3d overdue"; smoke alarm 2027-01-15 "In 93d" | PASS 8/8 |
| F13 | Transactions.Spent this month, Saved or repaid this month | 12 | Expenses = amount; Savings auto-transfer 0 / 300; Salary 0 / 0 | PASS 12/12 |
| F10/F11/New | Budget.Spent this month, Saved or repaid (rollups), Actual this month, Remaining, Used, Budget status | 7 | Rent and Savings "✓ Fully used"; Groceries "On track: 197.45 left" 51%; Transport 36.5 left 76%; Eating out 76.2 left 49%; Fun 7 left 93%; Salary "No budget set" | PASS 7/7 |
| F14 to F16/New | Subscriptions.Monthly cost, Yearly cost, Next charge, Renews in, Due this week | 5 | Newspaper 21.67 / 260, in 3d, Yes; Cloud 2.5 / 29.99, in 112d; Music 10.99 / 131.88, in 14d; Streaming in 5d Yes; Gym in 2d Yes | PASS 5/5 |
| F17 to F19/New | Money Goals.Progress, Remaining, Per month needed, Progress Bar, Goal status | 3 | Emergency 0.3583 / 3850 / 770 / 36%; Japan 0.1714 / 2900 / 290 / 17%; Credit card 0.5 / 900 / 300 / 50% | PASS 3/3 |
| F20 to F22 | Contacts.Next birthday, Days to birthday, Birthday soon | 5 | Grandma 2026-10-22, 8, Soon; Sam 19; Maya 151; Priya 259; Dr. Lee (no birthday) blank | PASS 5/5 |
| F23 | Documents.Expiry | 4 | Passport "Renew soon"; 3 × "OK" | PASS 4/4 |

Note on F2/F3 and Salary: a rollup average over no projects, and Remaining with no budget, were checked by prefix and suffix only, because the empty value can print as either "" or "0". The visible fields (Progress Bar, Goal health, Budget status, Used) were checked exactly.

## Edge cases (temporary records, dev copy)

| ID | Case | Expected | Result |
|---|---|---|---|
| E-C1 | Birthday 2000-02-29, today 2026-10-14 | Next 2027-02-28 (non-leap policy), 137 days, not soon | PASS |
| E-C2 | Birthday today | 2026-10-14, 0 days, Soon | PASS |
| E-C3 | Birthday yesterday | 2027-10-13, 364 days | PASS |
| E-C4/C5 | 14 days vs 15 days away | 14 → Soon; 15 → blank | PASS |
| E-S1 | Monthly, Next renewal 2026-08-10 | Next charge 2026-11-10, 27 days, not due | PASS |
| E-S2 | Monthly, Next renewal 2026-08-14 | Next charge today, 0 days, Due Yes | PASS |
| E-S3 | Weekly $5, Paused | Monthly 0, Yearly 0, not due | PASS |
| E-S4 | Quarterly $30, Next renewal 2026-07-20 | Monthly 10, Next charge 2026-10-20, Due Yes | PASS |
| E-S5 | Yearly $120, Next renewal 2025-11-01 | Next charge 2026-11-01, 18 days | PASS |
| E-S6 | Weekly $7, Next renewal 2026-09-30 | Monthly 30.33, Yearly 364, Next charge today | PASS |
| E-S7 | Cancelled, renews in 2 days | Monthly 0, not due | PASS |
| E-S8 | Monthly from Aug 31 (month-end) | Next charge 2026-10-31, 17 days | PASS |
| E-M1 | Money goal target 1000, current 1200 | Progress 1 (capped), Remaining 0, Per month 0, "✓ Reached", bar 100% | PASS |
| E-M2 | Target date already passed | Per month needed = full remaining (400) | PASS |
| E-M3 | No target | Goal status "Set a target" | PASS |
| E-H1 | Home care, Every empty | "Set how often (Every)" | PASS |
| E-H2 | Home care, Last done empty | "Set last done" | PASS |
| E-H3 | Due today | Next due 2026-10-14, "Due today" | PASS |
| E-D1 to D5 | Expired; no expiry; 59 days; 60 days; expires today | "⚠ Expired"; "No expiry date"; "Renew soon"; "OK"; "Renew soon" | PASS |
| E-L1 to L4 | Satisfaction empty, 12, −3, 6.6 | "Not scored yet"; 10 dots; 0 dots; 7 dots | PASS |
| E-DL1 | Daily log, no habits | 0, "◇◇◇◇◇" | PASS |
| E-T1 | Done and Canceled both ticked | Status Label "Canceled" | PASS |
| E-P1 | Project with 4 tasks: 3 done, 1 canceled | 4/3/1, progress 1, "100%" | PASS |
| E-G1 | Goal with a project only (no direct tasks) | Uses project progress: 100%, "✓ Completed" | PASS |
| E-G2 | Number goal going down: 82 → 70, current 76 | 50%, On track | PASS |
| E-G3 | Number goal without target | "Set start and target values", "Not enough information" | PASS |
| E-G4 | Target date passed, 0% | "⚠ Needs attention: past target date" | PASS |
| E-G5 | Target in 6 days, 0% | "⚠ Needs attention: due soon" | PASS |
| E-G6 | Status Achieved, nothing linked | "No tasks linked yet", "✓ Completed" | PASS |
| E-G7 | Number goal over target: 0 → 10, current 12 | Progress 1.2, full bar "120%", "✓ Completed" | PASS |
| E-B1 | Budget 100: Expense 80, Refund 10, Debt payment 20, Transfer 50, Income 40, last month's Expense 30 | Spent 70, Saved 20, Actual 90, Remaining 10, "On track: 10 left", 90% | PASS |
| E-B2 | Budget 50, Expense 62.35 | Remaining −12.35, "⚠ Over by 12.35", full bar "125%" | PASS |
| E-X1 to X7 | Transaction rows behind E-B1/E-B2 | Refund −10; Debt payment 0 / 20; Transfer, Income, last month 0 / 0 | PASS |

Observation (not a defect): a document that expires **today** shows "Renew soon", not "⚠ Expired". It counts as expired from the next day. This is documented, not changed.

## Not tested, with a manual verification matrix

These need a different date, a clock near midnight, or the Notion app. Check them by hand with the exact expected values below.

| ID | Check | How | Expected |
|---|---|---|---|
| M1 | Budget resets on the 1st | On the 1st of any month, open Money → Budget | Every Spent this month and Saved or repaid = 0; statuses "On track: <budget> left" (Salary "No budget set") |
| M2 | Feb 29 birthday in a leap year | In 2028, or by temporarily setting a contact's birthday to 2000-02-29 and checking after 2028-01-01 | Next birthday 2028-02-29 |
| M3 | Time-zone edge | Between 00:00 and 01:00 local time on the 1st of a month, add an Expense dated today and look at Budget | It counts in the new month. If not, note your time zone and Notion's (Settings → Language & region) |
| M4 | Display matches filter | Open Money → Budget in the app | Values equal the F10/F11 row above (e.g. Groceries 202.55 spent, "On track: 197.45 left") |
| M5 | Chart | Open Money → Spending by category | Bars per category for Spent this month (Savings group excluded); total 1,682.85 on 2026-10-14 data |

## Earlier phases (kept for the record)

| When | Target | Probes | Outcome |
|---|---|---|---|
| Phase 1 | Production (1), dev (10) | 11 | 11 PASS |
| Phase 1, probe 12 and Phase 7 | Dev | 0 | SQL/rows quota reached. Not retried automatically. Superseded by Phase 9B (view mode has no quota) |

## Re-running the harness

1. Re-add the probe columns (formulas listed below) to the dev databases.
2. Run `python3 -I tools/verify_dev_formulas.py <YYYY-MM-DD>` and paste each printed `FILTER` line into the matching "QA <database>" view on the QA harness page.
3. Query each view in view mode and compare the row count with the expected count.
4. Drop the probe columns again.

Probe formulas: Transactions `format(round(prop("Spent this month")*100)/100)+"|"+format(round(prop("Saved or repaid this month")*100)/100)`; Budget Categories adds Actual and Remaining the same way; Subscriptions `Monthly cost|Yearly cost|formatDate(Next charge,"YYYY-MM-DD")|Renews in (days)`; Money Goals `round(Progress,4)|Remaining|Per month needed`; Contacts `formatDate(Next birthday,"YYYY-MM-DD")|Days to birthday`; Home Care `formatDate(Next due,"YYYY-MM-DD")`; Projects `Tasks total|Tasks done|Tasks canceled|round(Progress,4)`; Goals `Tasks total|Tasks done|Tasks canceled|Projects count|round(Project progress,4)|round(Progress,4)`; Daily Log `format(Habits Done)`.
