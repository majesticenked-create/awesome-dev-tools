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
