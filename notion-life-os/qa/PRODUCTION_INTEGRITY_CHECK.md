# Production integrity check: Notion Life Hub

- **Check started:** Wed Oct 14 15:59:36 UTC 2026 (`date -u`)
- **Check finished:** about 16:01 UTC 2026-10-14 (`date -u` printed 16:01:03 just before the view-config re-fetch pass)
- **Mode:** strictly read-only. The only Notion tools called were `notion-fetch` and `notion-query-data-sources` with `mode: "view"`. No `sql` or `rows` queries were run, and no create, update, move, delete, duplicate or view-edit tool was called.
- **Baseline:** `qa/01_System_Inventory.md` (section "Databases (21) and properties") and the prod column of `qa/DEV_ID_MAP.md`.

## Target confirmation

- I fetched page `3f9570f2a4298179a432e8850ede84e4`. Its title is **"Notion Life Hub"** (icon 🕯️) and its ancestor path is empty, so it is a top-level page. It is not the dev copy (`3f9570f2a42981e5a009c25cc8874f3b`).
- I fetched the hub's "Databases" child page (`3f9570f2a429817f9176ec75f7af2343`). Its ancestor path ends at "Notion Life Hub", and it holds 21 child databases. Each one's `data-source-url` matches the production column of DEV_ID_MAP.md exactly.
- The hub's 3 inline linked views (This week, Goals in motion, Life balance) point at the prod collections `41fb423a…` (Tasks), `34f9e5f2…` (Goals) and `4e2804c3…` (Life Areas).
- Every one of the 21 database pages has the ancestor chain Databases → … → "Notion Life Hub" (prod).

## Per-database results

Schema match compares property names and types against the baseline list. Every relation target and rollup target was also checked against the dev-ID pattern `???570f2-a429-8???-…`. Counts come from `query-data-sources` in `mode: "view"`. Every query returned `has_more: false`, so no pagination was needed.

| # | Database | Prod collection ID | Schema match | Relations point to prod? | Rows found / expected | View used | View unfiltered? |
|---|---|---|---|---|---|---|---|
| 1 | Life Areas | 4e2804c3-09cb-465f-af74-3107c4009ae7 | Yes, 9/9 props (Name T, Vision Tx, Satisfaction N, Balance F, Goals/Projects/Journal/Ideas R, Goal Count RU count) | Yes (34f9e5f2, cc391287, da74b007, 0814757a) | **8 / 8** | view://91b78f8c-02f9-4d99-99d6-bccfd8fbcb4f "Default view" (table) | Yes, the fetched config has no filter or sort |
| 2 | Goals | 34f9e5f2-0a79-43d1-ae32-dc4a79a8f929 | Yes, 10/10 (Progress is a rollup with percent_checked on Tasks.Done). No dev-only props (Measure, Start/Target/Current value, Goal health, Tasks total/done/canceled, Projects count, Project progress all absent) | Yes (4e2804c3, cc391287, 41fb423a) | **5 / 5** | view://3b8c25e8-969d-4f9e-8ffd-6dbc120d5c0a "Default view" | Yes |
| 3 | Projects | cc391287-2da3-4f18-b466-4e95ed50b05f | Yes, 9/9. No Tasks total/done/canceled | Yes (34f9e5f2, 4e2804c3, 41fb423a) | **3 / 3** | view://1c73d8be-c1c8-4e47-a885-f18caa6699ba "Default view" | Yes |
| 4 | Tasks | 41fb423a-dcee-450a-a3ad-3264e902cd63 | Yes, 8/8. No "Canceled" property | Yes (cc391287, 34f9e5f2) | **12 / 12** | view://3f761ad9-989e-494b-ac9e-f1028b2368f9 "Default view" | Yes |
| 5 | Reviews | 23963e22-9521-4aa9-924b-f49deb87e1b2 | Yes, 7/7 | n/a (no relations) | **1 / 1** | view://466190c7-161b-4505-bf2c-a07d43086ace "Default view" | Yes |
| 6 | Journal | da74b007-ddaf-489c-9d1f-8e50ebd04ca2 | Yes, 6/6 | Yes (4e2804c3) | **3 / 3** | view://1afc010b-4d31-4c0c-973f-978a2f645094 "Default view" | Yes |
| 7 | Daily Log | 4648defe-2a34-4ecb-92ee-709ff9b9d93e | Yes, 12/12 (Day, Date, 5 habit CBs, Sleep, Energy, Mood, Habits Done F, Habit Bar F) | n/a | **7 / 7** | view://4a5b87a1-9de9-4196-bdf6-2fd1a01122ea "Default view" | Yes |
| 8 | Library | 36935501-6e7a-4a3c-abb2-a085a123fd4a | Yes, 9/9 (Status is a status type, Rating a select, Cover a file) | n/a | **5 / 5** | view://a1c48523-b412-4ccd-a8f9-b0496e106492 "Default view" | Yes |
| 9 | Ideas & Inspo | 0814757a-d7e7-41e0-ae6e-3a09f9724d7d | Yes, 6/6 | Yes (4e2804c3) | **4 / 4** | view://b2981de8-77aa-4259-a030-f2d9ae59da15 "Default view" | Yes |
| 10 | Workouts | fe32919e-953c-414c-a0b9-5100647f2f65 | Yes, 6/6 | n/a | **4 / 4** | view://f8378045-6d50-4455-b00a-3d8f909fe9eb "Default view" | Yes |
| 11 | Recipes | 21d8fd36-95a9-4e99-b5af-2b0c9fe8cba7 | Yes, 5/5 | n/a | **5 / 5** | view://174cec74-45cf-4e60-95c8-9fbb2622755e "Default view" | Yes |
| 12 | Meal Plan | 21793e82-2553-4b32-941e-c103bd73fc19 | Yes, 6/6 (Breakfast, Lunch and Dinner are one-way relations with no back-property) | Yes (21d8fd36) | **5 / 5** | view://305c383f-15fc-46f0-b98a-0264f0793900 "Default view" | Yes |
| 13 | Home Care | 42138be2-4a4c-432f-b082-1675feeee8b2 | Yes, 7/7 | n/a | **8 / 8** | view://5e3dd3c7-f3c6-4edf-a9b7-308d49c937e4 "Default view" | Yes |
| 14 | Budget Categories | 42475699-4054-4dcd-986e-830ab7ea950b | Yes, 7/7 (Spent this month is a sum rollup over Transactions."Spent this month"). No Saved or repaid, Actual this month or Budget status | Yes (2c6f5f8d; rollup target 2c6f5f8d/ZmJPSw) | **7 / 7** | view://3f2deae8-e4b6-4c24-a012-9bd41ffcac66 "Default view" | Yes |
| 15 | Transactions | 2c6f5f8d-df64-4b26-93d1-8bc42a8492b6 | Yes, 8/8. **No `noop_check`**, no "Saved or repaid this month". Type options are only Expense and Income | Yes (42475699) | **12 / 12** | view://7d490a68-a2d9-437d-afb7-d4845720b27e "Default view" | Yes |
| 16 | Subscriptions | fdc78963-3e88-49c4-a442-67818dcc8145 | Yes, 9/9. No Next charge or Due this week. Status options are Active, Trial, Cancel soon, Cancelled (no Paused) | n/a | **5 / 5** | view://34ba9969-ff6d-4dd3-91af-e73a7e05aa52 "Default view" | Yes |
| 17 | Money Goals | b61f6d8c-eb2d-4636-a4e0-5897760c4555 | Yes, 8/8. No Remaining or Goal status | n/a | **3 / 3** | view://e5cff91b-cfd2-4096-9c60-247f6f0b2d16 "Default view" | Yes |
| 18 | Contacts | 0507cb18-b84d-4093-9c2f-72885f82e555 | Yes, 10/10 (Phone is phone_number, Email is email) | n/a | **5 / 5** | view://3be2d874-63f8-4e12-87c6-6665697c7963 "Default view" | Yes |
| 19 | Documents | d5bad3d5-c72e-41bc-ab5a-a62567cb3f76 | Yes, 6/6 | n/a | **4 / 4** | view://c5b6ba11-393f-4ff6-b24b-a20f2c0edc75 "Default view" | Yes |
| 20 | Trips | c256eb3b-f181-447a-ba86-0c7324adf190 | Yes, 5/5 | n/a | **2 / 2** | view://e521c4dc-fa0a-43f3-a0f2-4ebf76d4403d "Default view" | Yes |
| 21 | Lists | 3e03598c-bc46-4e2c-b757-30cd8c237a47 | Yes, 6/6 (For is a one-way relation to Contacts) | Yes (0507cb18) | **12 / 12** | view://5b0d2f12-f1a5-4278-b39e-5c6ba6e959aa "Default view" | Yes |

**Totals:** 21 of 21 schemas match the baseline, with no missing, extra or retyped properties. 21 of 21 per-database counts match. **Rows found: 120.**

### Discrepancy in the expected total (the baseline document is wrong, not production)

The task and `01_System_Inventory.md` both give the total as **131**. The 21 per-database baseline numbers actually sum to **120** (8+5+3+12+1+3+7+5+4+4+5+5+8+7+12+5+3+5+4+2+12 = 120, checked with shell arithmetic). Production matches every per-database number, so production has 120 rows. The "131" in the inventory's Sample records table is an arithmetic error and should be corrected to 120.

### Dev-only property sweep

None of these appear in any production schema: Canceled (Tasks); Measure, Start value, Target value, Current value, Goal health, Tasks total, Tasks done, Tasks canceled, Projects count, Project progress (Goals); Tasks total/done/canceled (Projects); Saved or repaid this month (Transactions); Saved or repaid, Actual this month, Budget status (Budget Categories); Next charge, Due this week (Subscriptions); Remaining, Goal status (Money Goals); zz QA probe (any database). Budget Categories does have a baseline "Remaining" formula, which is expected. The dev-only "Remaining" is the one on Money Goals, and it is absent.

### Relation and rollup target sweep

Every `dataSourceUrl`, `propertyUrl`, `relationPropertyUrl` and `targetPropertyUrl` in the 21 schemas points to one of the 21 prod collection IDs. No dev-shaped ID (`???570f2-a429-8???-…`) appears in any schema.

## noop_check result

**Absent.** The full prod Transactions schema (`collection://2c6f5f8d-df64-4b26-93d1-8bc42a8492b6`) has exactly 8 properties: Amount, Category, Date, Description, Method, Month, Spent this month, Type. The SQLite table definition for the same collection also has no `noop_check` column.

## Spot checks (proof that production was not edited by the dev work)

| Check | Expected | Observed | Result |
|---|---|---|---|
| Transactions row "Savings auto-transfer", Type | Expense | `"Type":"Expense"` (Amount 300, Method Transfer, 2026-10-01, page 3f9570f2a42981bd9006fa0f2fcd5781) | PASS |
| Tasks title "Tempo run — 20 min" keeps its em dash | Em dash present | `"Name":"Tempo run — 20 min"` (page 3f9570f2a42981d0b8d4e91b56860142) | PASS |
| Tasks title "Long run — 7K" keeps its em dash | Em dash present | `"Name":"Long run — 7K"` (page 3f9570f2a42981548b7cdcb7d15af467) | PASS |
| Subscriptions Status options exclude "Paused" | No Paused | Options: Active, Trial, Cancel soon, Cancelled | PASS |
| Transactions Type options are original only | Expense and Income only | Options: Expense, Income (no Refund, Savings, Debt payment or Transfer). "Transfer" exists only as a **Method** option, which is in the baseline | PASS |
| Goals Status options (extra check) | Baseline status | Not started, In progress, Paused, Achieved. "Paused" here is a baseline Goals status, unrelated to the Subscriptions check | Informational |

## Could NOT verify, or verified only partly

1. **The 131 total.** It cannot be reconciled because the baseline's own per-database numbers sum to 120. Production matches all 21 per-database figures.
2. **Formula and rollup logic and results.** The connector returns only `formulaCode://` and `formulaResult://` handles, so formula source and computed values (Balance, Progress Bar, Remaining, Used, Month, Spent this month, Next due, and others) were not compared. Only each formula or rollup property's presence, type and (for rollups) aggregation and target were compared.
3. **Archived or trashed rows.** View queries ran with the default `is_archived` (false). Archived rows were not queried, so the counts are active rows only.
4. **Select option lists other than the ones named above.** The baseline lists option values only for Transactions Type. Other option lists were observed but had nothing to compare against.
5. **Full row-level content.** Apart from the spot checks, I did not compare individual cell values or page bodies with a baseline, because no row-level baseline exists in the repo.
6. **Dashboard pages** (Today, Plan, Mind, Body & Home, Money, Life Admin, Start Here, Finishing checklist) and their 33 linked views were not fetched. Only the hub page and the Databases page were inspected.
7. **Recent edit timestamps.** The hub page reports `page_last_edited_at` 2026-10-14T15:03:32Z and the Databases page 2026-10-14T14:54:10Z, both today. The fetch does not say what changed (possibly views or opens during today's audit, or the noop_check incident). Data source fetches expose no last-edited time. Nothing found in schemas or spot-checked values shows a change, but I cannot rule out edits to page content or view layouts.
8. **Row page IDs.** Row page IDs in both workspaces start with `3f9570f2-a429-81…`, so the dev-ID shape rule (which covers collection IDs) cannot tell prod rows from dev rows. I identified production by collection IDs and ancestor paths, not by row ID prefixes.

## Follow-up by the main session (2026-10-14, about 16:05 UTC, read-only)

- **Total corrected.** The 21 per-database baseline counts sum to 120. `01_System_Inventory.md` and `05_Defect_Register.md` now say 120. Production has 120 active rows, matching every database. Point 1 above is resolved.
- **Hub content.** The production hub page was fetched again. Its content is the original layout: the original "New here?" callout (with its em dash), the Daily / Life / Setup columns including the seller "Finishing checklist" child page, and the three original linked views "This week", "Goals in motion" and "Life balance", which point at the production Tasks, Goals and Life Areas collections. None of the dev-copy changes (LifeOS name, Quick actions, Today at a glance, moved checklist) appear. So the 15:03Z timestamp does not reflect any of the Phase 2 to 9 dev work. The dashboard sub-pages (point 6) were still not fetched.

## Verdict for Phase 9C

| Check | Result |
|---|---|
| Original template still exists and is separate from the dev copy | PASS |
| 21 of 21 schemas match the pre-dev baseline (properties and types) | PASS |
| Relations and rollups point only at production collections | PASS |
| `noop_check` absent from production Transactions | PASS |
| Record counts: 21 of 21 databases match, 120 rows in total | PASS |
| Spot-checked records unchanged by dev work | PASS (5 of 5) |
| Formula values in production | NOT TESTED (out of scope; production formulas were not changed) |
| Dashboard sub-pages and their linked views | NOT TESTED |
