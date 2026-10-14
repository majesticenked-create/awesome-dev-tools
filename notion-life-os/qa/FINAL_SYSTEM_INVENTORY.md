# Final System Inventory (dev copy, release candidate)

Hub: "Life Hub DEV (working copy, do not sell)" `3f9570f2a42981e5a009c25cc8874f3b`. IDs in `DEV_ID_MAP.md`.

## Pages

| Page | Contents after changes |
|---|---|
| Hub | Welcome; Today at a glance (Due today and overdue, Today's habits); Quick actions (text links); Life overview (Goals in motion with Goal health, Active projects, Coming up this week, Life balance); Explore your Life Hub (navigation) |
| Start Here | Rewritten: what's included, structure, first five steps, personalization, tasks, goals, habits, money definitions, reviews, automatic vs manual table, phone, sample-data removal, troubleshooting, FAQ |
| Today | Unchanged layout; tasks view excludes canceled; renewals use Due this week; birthdays filtered |
| Plan | Goals board shows Goal health and Measure; Tasks block has 4 tabs: Open tasks, Focus: high priority, Inbox (no date), Calendar |
| Mind | Unchanged (Habit trend chart pending D-24 decision) |
| Body & Home | Unchanged |
| Money | New money-type callout; Budget view shows Budget status, Spent, Saved or repaid, Remaining; Subscriptions show Next charge; Money goals show Goal status and Remaining; Spending chart excludes Savings |
| Life Admin | Copy fix only |
| Databases | 21 databases (unchanged count); copy fix |
| Removed from hub | Finishing checklist (moved to SELLER NOTES) |

## Schema changes (dev copy)

| Database | Added | Changed | Removed |
|---|---|---|---|
| Tasks | Canceled (checkbox) | Status Label (Canceled branch) | |
| Projects | Tasks total, Tasks done, Tasks canceled (rollups) | Progress (rollup → formula, canceled-aware), Progress Bar (empty state) | Old Progress rollup |
| Goals | Measure, Start value, Target value, Current value, Tasks total, Tasks done, Tasks canceled, Projects count, Project progress, Goal health | Progress (rollup → formula), Progress Bar | Old Progress rollup |
| Transactions | Saved or repaid this month | Type options (+Refund, Savings, Debt payment, Transfer), Spent this month (refunds subtract) | |
| Budget Categories | Saved or repaid, Actual this month, Budget status | Remaining, Used (use Actual) | |
| Subscriptions | Next charge, Due this week | Status (+Paused), Monthly cost (0 when Paused/Cancelled), Renews in | |
| Money Goals | Remaining, Goal status | Current (description), Per month needed (floor 0) | |
| Home Care | | Due (empty interval) | |
| Life Areas | | Balance (clamp, empty state) | |
| Contacts | | Next birthday (Feb 29 policy), Birthday soon (checkbox → text) | |
| Documents | | Expiry (no em dash) | |

Counts now: 21 databases, 32 formulas, 11 rollups, 20 relation properties. All existing records kept. Migrated records: 1 transaction re-typed to Savings; 5 goals given a Measure (1 converted to Number: 0 → 24, current 14); 2 task titles and 2 journal texts edited for copy rules.

## New views

Hub: Due today and overdue, Today's habits, Active projects. Plan Tasks block: Focus: high priority, Inbox (no date), Calendar. Daily Log database: All days, newest first (spot duplicates).

## Buttons and templates

None. Both need the Notion app (D-02, D-03). Specs ready in the seller checklist and `TEMPLATES_TO_CREATE.md`.
