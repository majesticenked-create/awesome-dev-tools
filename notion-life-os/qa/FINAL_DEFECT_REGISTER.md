# Final Defect Register

All fixes were applied to the **dev copy** ("Life Hub DEV (working copy, do not sell)"). Production ("Notion Life Hub") is unchanged except for the incident in D-29, which was reverted.

"Fixed (config verified)" means Notion accepted and saved the change (schema or view read back after the write). "Output verified" means a live probe showed the expected values. Most output checks are BLOCKED by the connector quota (see FORMULA_TEST_RESULTS.md).

| ID | Sev | Title | Status | Evidence |
|---|---|---|---|---|
| D-01 | High | Seller checklist inside customer hub | **Fixed** | Moved to "Life Hub SELLER NOTES" (private, outside the hub). Hub fetch shows no checklist link. |
| D-02 | High | No quick-add buttons | **Open (UI only)** | Connector cannot create buttons. Exact button specs in the seller checklist. Interim: Hub "Quick actions" callout with honest text links and the "New" button on filtered views. |
| D-03 | High | No database templates | **Open (UI only)** | Connector cannot create templates. Paste-ready text for 11 templates in `TEMPLATES_TO_CREATE.md`. |
| D-04 | High | Birthdays soon view unfiltered | **Fixed (config verified)**, output BLOCKED | "Birthday soon" is now a text formula ("Soon"/blank). View filter `Birthday soon = Soon` saved and read back. |
| D-05 | Low | Birthday CSV missing from export | **Not a product defect** | Export artifact of linked views; buyers get a duplicate link. ZIP not available to confirm. |
| D-06 | Medium | Formatting unfinished | **Open (UI only)** | Footers, hidden view titles, serif font, full width, locking listed in seller checklist. |
| D-07 | Medium | Sample data removal manual | **Mitigated** | Start Here now has a "Remove the sample data" section. Edition decision pending (CUSTOMER_PACKAGE_INVENTORY.md). |
| D-08 | Critical | Savings counted as spending; no transfer/refund/debt types | **Fixed (config verified)**, output BLOCKED | Type now has Expense, Income, Refund, Savings, Debt payment, Transfer. Spending = Expense minus Refund. New "Saved or repaid" column. Sample savings transfer re-typed. Spending chart excludes the Savings group. |
| D-09 | Medium | Budget only shows current month; sample data goes stale | **Mitigated** | Behavior documented in Money callout and Start Here. Seller checklist: refresh sample dates before listing. History via Transactions Month filter. |
| D-10 | Medium | Overspend only shown by colour/percentage | **Fixed (config verified)** | New "Budget status": "⚠ Over by X", "✓ Fully used", "On track: X left", "No budget set". Shown first in the Budget view. |
| D-11 | Medium | 0% shown when nothing is linked | **Fixed (config verified)** | Goals and Projects show "No tasks linked yet"; number goals show "Set start and target values". |
| D-12 | Medium | No numeric goals | **Fixed (config verified)** | Measure (Tasks/Number), Start, Target, Current values. Handles decreasing targets and >100%. Sample "Read 24 books" converted (14 of 24). |
| D-13 | Medium | Tasks linked only via project ignored by goal | **Fixed (config verified)** | Goal falls back to the average progress of its projects when no tasks are linked directly. |
| D-14 | Medium | Static renewal date | **Fixed (config verified)** | "Next charge" rolls forward by cycle; "Renews in" and new "Due this week" use it; Today view filters on Due this week. |
| D-15 | Low | No Paused status; cancelled cost counted | **Fixed (config verified)** | Paused added; Monthly cost is 0 for Paused and Cancelled. |
| D-16 | Low | Negative per-month amount; no remaining | **Fixed (config verified)** | Per month needed floored at 0; Remaining and Goal status added; debt "Current" defined as paid off. |
| D-17 | Low | Empty interval reads overdue | **Fixed (config verified)** | Due shows "Set how often (Every)". |
| D-18 | Low | Balance bar breaks outside 0 to 10 | **Fixed (config verified)** | Clamped and rounded; empty shows "Not scored yet". |
| D-19 | Medium | Feb 29 birthdays undefined | **Fixed (config verified)**, output BLOCKED | Policy: shown on Feb 28 in non-leap years. Formula handles either Notion date behavior. |
| D-20 | High | Em dashes in customer copy | **Fixed (verified by page fetch)** | Hub, Today, Plan, Money, Life Admin, Databases, Start Here, 2 task titles, 2 journal entries, Documents Expiry output. |
| D-21 | Medium | Sample dates fixed to Oct 2026 | **Open (process)** | Seller checklist item. |
| D-22 | Low | Duplicate Daily Log rows | **Mitigated** | "All days, newest first (spot duplicates)" view tab on Daily Log; guidance in Start Here. |
| D-23 | Medium | No canceled tasks | **Fixed (config verified)** | Canceled checkbox; Status Label "Canceled"; progress = done ÷ (total − canceled); all task views exclude canceled. |
| D-24 | High | Two charts vs free plan limit of one | **Open, needs owner approval** | Free plan allows 1 chart per workspace (third-party sources). Removing a chart deletes existing functionality, so approval requested. FAQ updated to be accurate meanwhile. |
| D-25 | Low | Goal Count includes achieved | Open (accepted) | Cosmetic. |
| D-26 | Medium | Product name "Notion Life Hub" | **Open, owner decision** | Trademark and name-clash risk. |
| D-27 | High | Clean-account duplication untested | **Open, BLOCKED** | No second account in session. |
| D-28 | Medium | Formula outputs unverified | **Open, BLOCKED** | Connector quota. Expected values ready. |
| D-29 | Process | Accidental write to production | **Resolved** | During Phase 2 an unused checkbox column "noop_check" was added to production Transactions by an ID mix-up and removed within the same minute. Production schema re-read and matches the original. No records touched. Guard added (`DEV_ID_MAP.md`). |
| D-30 | Low | Hub cannot show today's date as text | Open (accepted) | Static pages cannot show a live date; Today's views are date-filtered instead. |
