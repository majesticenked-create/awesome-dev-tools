# Changelog

All changes are in the dev copy unless marked PRODUCTION.

## 2026-10-14

### Setup
- Created dev copy by native duplicate of the production hub. Renamed "Life Hub DEV (working copy, do not sell)".
- Created private "Life Hub SELLER NOTES (not part of the product)" page.

### Incident (PRODUCTION, reverted)
- Added an unused checkbox column "noop_check" to production Transactions by using a production ID instead of the dev ID. Removed it immediately with DROP COLUMN. Production schema re-read and matches the original (Amount, Category, Date, Description, Method, Month, Spent this month, Type). No rows were touched. Added `DEV_ID_MAP.md` with an ID-shape guard for all later writes.

### Tasks and projects
- Tasks: added Canceled; Status Label shows "Canceled" first.
- Projects: progress is now done ÷ (total − canceled) via three rollups and a formula; empty state "No tasks linked yet".
- Task views on Hub, Today and Plan exclude canceled tasks.
- Plan tasks block: added Focus: high priority, Inbox (no date) and Calendar tabs.

### Goals
- Added Measure (Tasks/Number), Start, Target and Current values.
- Progress: number goals use (Current − Start) ÷ (Target − Start); task goals use tasks, falling back to average project progress.
- Progress Bar empty states. New Goal health with documented rules.
- Sample: "Read 24 books" set to Number 0 → 24, current 14. Other goals set to Tasks.

### Money
- Transactions Type: added Refund, Savings, Debt payment, Transfer. Spending = Expense − Refund. New "Saved or repaid this month".
- Budget: added Saved or repaid, Actual this month, Budget status. Remaining and Used now use Actual.
- Sample "Savings auto-transfer" re-typed from Expense to Savings.
- Spending chart excludes the Savings group.
- Subscriptions: added Paused; Monthly cost 0 when Paused or Cancelled; added rolling Next charge and Due this week; Renews in uses Next charge.
- Money Goals: Per month needed floored at 0; added Remaining and Goal status; clarified debt "Current".

### Other formulas
- Contacts: Feb 29 policy (Feb 28 in non-leap years); Birthday soon now text, so the view filter works.
- Home Care: "Set how often (Every)" when the interval is empty.
- Life Areas: Balance clamped; "Not scored yet" when empty.
- Documents: Expiry shows "No expiry date" instead of an em dash.

### Views
- Today: Birthdays soon filtered on Birthday soon = Soon (was unfiltered). Renewing this week filtered on Due this week.
- Money: Budget, Subscriptions and Money goals views show the new fields.
- Daily Log: "All days, newest first (spot duplicates)" view tab.
- Hub: added Due today and overdue, Today's habits, Active projects.

### Pages and copy
- Hub rebuilt: Welcome, Today at a glance, Quick actions, Life overview, Explore. First attempt left blocks in the wrong order; fixed and re-checked.
- Start Here rewritten (structure, setup, customization, goals, money definitions, automatic vs manual, troubleshooting, FAQ).
- Removed all em dashes from customer pages, 2 sample task titles and 2 journal entries. Restored two intro-line colours that an edit had dropped.
- Money page callout explains every transaction type.
- Moved the Finishing checklist out of the hub into SELLER NOTES and rewrote it (button specs, template list, chart decision, polish, publishing).

### Repo
- `qa/` folder: Phase 1 audit (01 to 06), final reports, `TEMPLATES_TO_CREATE.md`, `DEV_ID_MAP.md`, `tools/expected_values.py`.

## 2026-10-14, Phase 9 (owner decisions approved)

### Charts (approved decision 1)
- Removed the "Habit trend" heading and its linked chart view from Mind. The Daily Log data, the Habit tracker view and its Habit Bar column are unchanged (read back after the change).
- The customer template now has one chart: Money → Spending by category.
- Start Here FAQ rewritten: lists the single chart, explains that Notion may ask to upgrade if the buyer's workspace already has a chart, and that LifeOS works without it. It does not claim universal free-plan compatibility.

### Name (approved decision 2)
- Dev hub renamed "LifeOS - All-in-One Life Planner [DEV, do not sell]". The DEV marker is dropped only in a release copy.
- Hub: secondary line "LifeOS - All-in-One Life Planner · A Notion template"; "Explore your Life Hub" → "Explore LifeOS".
- Start Here: intro now "Welcome to LifeOS, your all-in-one life planner"; new "About LifeOS" section with a non-affiliation notice.
- Databases page callout: "Life Hub" → "LifeOS".
- Seller notes renamed "LifeOS SELLER NOTES (not part of the product)"; checklist updated (chart decision done, edition plan, release title).
- Only titles and text changed. No page or database was moved, so links and relations are unaffected (hub fetch shows all 8 links and mentions resolving).

### Editions (approved decision 3)
- Plan recorded in `CUSTOMER_PACKAGE_INVENTORY.md`: Example edition is the master; a Blank edition is generated for each release. Not generated yet (see Phase 9D).

### Verification (Phase 9B)
- Built a seller-only "QA harness" page with linked filter views (view-mode queries, no quota).
- Temporarily added a text formula "zz QA probe" to 9 dev databases to expose number and date results. Removed afterwards; schemas read back without it.
- 79/79 sample rows and 46/46 edge cases matched the independent calculator (`tools/verify_dev_formulas.py`). Negative control returned 0 rows.
- 53 temporary "QA TEMP" records were created for edge cases, then moved out of the databases to a seller-only archive page. Nothing deleted. Dev databases back to the original sample data (edge views empty, sample values re-checked).

### Docs
- `BUTTON_AND_TEMPLATE_QA.md` rewritten as a step-by-step build and verification guide (all items INCOMPLETE).
- New: `TEST_MATRIX.md`, `PRODUCTION_INTEGRITY_CHECK.md`, `tools/verify_dev_formulas.py`.
- Updated: defect register, formula results, release readiness, package inventory, duplication QA, inventory, navigation.
