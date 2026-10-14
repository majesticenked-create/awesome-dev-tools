# Final Defect Register

All fixes were applied to the **dev copy**, now titled "LifeOS - All-in-One Life Planner [DEV, do not sell]". Production ("Notion Life Hub") is unchanged except for the incident in D-29, which was reverted (re-checked in Phase 9C, see `PRODUCTION_INTEGRITY_CHECK.md`).

Status key:
- **Fixed, output verified**: the live values were checked against an independent calculation (Phase 9B, `FORMULA_TEST_RESULTS.md`).
- **Fixed (config verified)**: the change was saved and read back, but the output needs the Notion app to check.
- **Open**, **INCOMPLETE**, **BLOCKED**: not done, with the reason given.

Last updated 2026-10-14 (Phase 9).

| ID | Sev | Title | Status | Evidence |
|---|---|---|---|---|
| D-01 | High | Seller checklist inside customer hub | **Fixed** | Moved to "LifeOS SELLER NOTES" (private, outside the hub). Hub fetch shows no link to it. |
| D-02 | High | No quick-add buttons | **Open, INCOMPLETE (UI only)** | No UI tool in this environment. Step-by-step build and verification spec: `BUTTON_AND_TEMPLATE_QA.md` Part 1 (B1 to B4). |
| D-03 | High | No database templates | **Open, INCOMPLETE (UI only)** | Spec for 11 templates: `BUTTON_AND_TEMPLATE_QA.md` Part 2 (T1 to T11). Text in `TEMPLATES_TO_CREATE.md`. All referenced options exist. |
| D-04 | High | Birthdays soon view unfiltered | **Fixed, output verified** | Birthday soon = "Soon" for Grandma Rose only. Edge cases: today, 14 days (Soon), 15 days (blank). |
| D-05 | Low | Birthday CSV missing from export | Not a product defect | Export artifact of linked views. |
| D-06 | Medium | Formatting unfinished | **Open (UI only)** | Footers, hidden view titles, serif font, full width and locking are listed in the seller checklist. |
| D-07 | Medium | Sample data removal manual | **Mitigated** | Approved plan: Example master plus a Blank edition made for each release (`CUSTOMER_PACKAGE_INVENTORY.md`). |
| D-08 | Critical | Savings counted as spending; no transfer/refund/debt types | **Fixed, output verified** | Sample: Savings row Spent 0, Saved 300; consumption total 1,682.85. Edge E-B1: Refund lowers spending, Debt payment goes to Saved, Transfer, Income and last month's expense are ignored. |
| D-09 | Medium | Budget counts current month only; sample goes stale | **Mitigated** | Documented. The month reset is on the manual matrix (M1). |
| D-10 | Medium | Overspend shown only by colour | **Fixed, output verified** | E-B2: "⚠ Over by 12.35"; sample rows "✓ Fully used" / "On track: X left" / "No budget set". |
| D-11 | Medium | 0% shown when nothing linked | **Fixed, output verified** | Pottery and E-G6 "No tasks linked yet"; E-G3 "Set start and target values". |
| D-12 | Medium | No numeric goals | **Fixed, output verified** | Read 24 books 58%; E-G2 (82 → 70, current 76) 50%; E-G7 (over target) 120%. |
| D-13 | Medium | Tasks linked only via project ignored by goal | **Fixed, output verified** | E-G1: goal with only a project shows the project's 100%. |
| D-14 | Medium | Static renewal date | **Fixed, output verified** | E-S1, S2, S4, S5, S6, S8: Next charge rolls forward for monthly, quarterly, yearly, weekly and month-end dates. |
| D-15 | Low | No Paused status; cancelled cost counted | **Fixed, output verified** | E-S3 (Paused) and E-S7 (Cancelled): Monthly and Yearly 0, not due. |
| D-16 | Low | Negative per-month amount; no remaining | **Fixed, output verified** | E-M1: overpaid shows Remaining 0, Per month 0, "✓ Reached". E-M2: past target date asks for the full remaining. |
| D-17 | Low | Empty interval reads overdue | **Fixed, output verified** | E-H1 "Set how often (Every)"; E-H2 "Set last done". |
| D-18 | Low | Balance bar breaks outside 0 to 10 | **Fixed, output verified** | E-L1 to L4 (empty, 12, −3, 6.6). |
| D-19 | Medium | Feb 29 birthdays undefined | **Fixed, output verified (non-leap year)** | E-C1: 2000-02-29 shows 2027-02-28. The leap-year case (2028-02-29) is on the manual matrix (M2). |
| D-20 | High | Em dashes in customer copy | **Fixed (verified by page fetch)** | New copy added in Phase 9 (LifeOS line, About LifeOS, chart FAQ) contains none. |
| D-21 | Medium | Sample dates fixed to Oct 2026 | **Open (process)** | Refresh sample dates before each release. |
| D-22 | Low | Duplicate Daily Log rows | **Mitigated** | "All days, newest first" view; Start Here guidance. |
| D-23 | Medium | No canceled tasks | **Fixed, output verified** | E-P1: 3 done + 1 canceled of 4 = 100%. E-T1: Done and Canceled shows "Canceled". |
| D-24 | High | Two charts vs free-plan limit | **Fixed in dev (approved)**; free-plan validation **NOT PERFORMED** | Habit trend chart removed from Mind (2026-10-14). The Habit tracker and its Habit Bar progress column are unchanged. One chart remains (Money → Spending by category). Source databases checked: no chart tabs in Budget Categories or Daily Log. FAQ explains what to do if a workspace already has a chart. Not tested in a free workspace, with or without an existing chart. |
| D-25 | Low | Goal Count includes achieved | Open (accepted) | Cosmetic. |
| D-26 | Medium | Product name | **Fixed in dev** | Renamed "LifeOS - All-in-One Life Planner". "A Notion template" appears only as a secondary line. Start Here has an "About LifeOS" non-affiliation notice. Hub, Start Here, Databases and seller notes updated; links and relations untouched (no database or page was moved or renamed apart from titles). |
| D-27 | High | Clean-account duplication untested | **Open, NOT PERFORMED** | No second (free) Notion account available to this session. |
| D-28 | Medium | Formula outputs unverified | **Closed, verified** | Phase 9B: 79/79 sample rows and 46/46 edge cases match. |
| D-29 | Process | Accidental write to production | **Resolved** | "noop_check" added and dropped in Phase 2. Re-checked in Phase 9C. |
| D-30 | Low | Hub cannot show today's date as text | Open (accepted) | Views are date-filtered instead. |
| D-31 | Low | A document expiring today shows "Renew soon" | Open (accepted) | It shows "⚠ Expired" from the next day. Found in E-D5; behavior is reasonable, wording unchanged. |
| D-32 | Process | QA artifacts in seller notes | **Open (owner action)** | "QA harness" page and "QA TEMP records" (53 moved test rows) sit under LifeOS SELLER NOTES, outside the product. They are not duplicated with the template. Delete them when you no longer need them. |
