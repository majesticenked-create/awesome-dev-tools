# 01 System Inventory

Audit date: 2026-10-14. Auditor: Claude (via the Notion connector).
Source of truth: the live workspace. No export ZIP was available in this session, so nothing here is derived from an export.

## Workspaces

| Role | Title | Page ID |
|---|---|---|
| Production (original, untouched during audit) | Notion Life Hub | `3f9570f2a4298179a432e8850ede84e4` |
| Development copy (all changes go here) | Life Hub DEV (working copy, do not sell) | `3f9570f2a42981e5a009c25cc8874f3b` |

The dev copy was made with Notion's native "Duplicate" (connector `duplicate-page`). Every database, relation, rollup and linked view in the copy was checked and points at the copy's own databases, not at production (see 03 and 04).

## Access verified

| Capability | Status | Notes |
|---|---|---|
| Read pages, schemas, view configs | Available | `fetch` |
| Edit page content, schemas, views | Available | `update-page`, `update-data-source`, `update-view`, `create-view` |
| Read formula **source code** back | Not available | API returns `formulaCode://` handles only. Formulas are documented from the build record. |
| Read formula **results** | Not available directly | Results come back as `formulaResult://` handles. Workaround used: server-side filters on the formula result (see 02). |
| Server-side filtered queries | Limited | Free-plan connector quota. Quota was exhausted mid-audit (Notion: "usage limit reached, try again later"). Remaining probes are marked BLOCKED. |
| Create or click buttons | Not available | No button block or button property support in the connector. |
| Create database templates | Not available | Connector can apply templates but not define them. |
| Second Notion account for duplication test | Not available | No independent account in this session. |
| Mobile app / device testing | Not available | Cloud session, no device. |

## Top-level structure (production; dev copy is identical)

```
Notion Life Hub (hub page)
├── Columns: Daily | Life | Setup
│   ├── Today
│   ├── Plan
│   ├── Mind
│   ├── Body & Home
│   ├── Money
│   ├── Life Admin
│   ├── Start Here
│   ├── Databases (holds all 21 source databases)
│   └── Finishing checklist (seller only)   <- defect D-01
└── Hub linked views: This week (Tasks), Goals in motion (Goals), Life balance (Life Areas)
```

## Pages (10)

| Page | Purpose | Linked views |
|---|---|---|
| Hub | Navigation + 3 summary views | 3 |
| Start Here | Onboarding, FAQ | 0 |
| Today | Daily page | 6 |
| Plan | Areas, goals, projects, tasks, reviews | 5 |
| Mind | Journal, habits, library, ideas, habit chart | 5 (1 chart) |
| Body & Home | Workouts, meals, recipes, home care, groceries | 5 |
| Money | Budget, transactions, subscriptions, money goals, spending chart | 5 (1 chart) |
| Life Admin | Contacts, documents, trips, lists | 4 |
| Databases | Container for 21 source databases | 0 (21 child databases) |
| Finishing checklist | Seller-only manual steps | 0 |

Total linked views on dashboards: 33, including 2 chart views.

## Databases (21) and properties

Legend: T title, Tx text, N number, D date, CB checkbox, S select, MS multi-select, ST status, R relation, RU rollup, F formula, U url, FL files, E email, P phone.

| # | Database | Properties |
|---|---|---|
| 1 | Life Areas | Name T, Vision Tx, Satisfaction N, Balance F, Goals R(Goals), Projects R(Projects), Journal R(Journal), Ideas R(Ideas), Goal Count RU |
| 2 | Goals | Name T, Area R, Status ST, Horizon S, Target date D, Why it matters Tx, Projects R, Tasks R, Progress RU(percent checked), Progress Bar F |
| 3 | Projects | Name T, Goal R, Area R, Status ST, Dates D, Notes Tx, Tasks R, Progress RU, Progress Bar F |
| 4 | Tasks | Name T, Done CB, Do date D, Priority S, Energy S, Project R, Goal R, Status Label F |
| 5 | Reviews | Name T, Type S, Period D, Wins Tx, Lessons Tx, Focus next Tx, Score N |
| 6 | Journal | Title T, Date D, Type S, Mood S, Area R, Tags MS |
| 7 | Daily Log | Day T, Date D, Water/Move/Read/Meditate/No-phone morning CB, Sleep N, Energy N, Mood S, Habits Done F, Habit Bar F |
| 8 | Library | Title T, Type S, Creator Tx, Status ST, Rating S, Started D, Finished D, Cover FL, Notes Tx |
| 9 | Ideas & Inspo | Name T, Kind S, Link U, Area R, Tags MS, Image FL |
| 10 | Workouts | Session T, Date D, Type S, Minutes N, Intensity S, Notes Tx |
| 11 | Recipes | Name T, Meal MS, Prep time N, Tags MS, Source U |
| 12 | Meal Plan | Day T, Date D, Breakfast/Lunch/Dinner R(Recipes, one-way), Notes Tx |
| 13 | Home Care | Task T, Room S, Kind S, Every N, Last done D, Next due F, Due F |
| 14 | Budget Categories | Category T, Group S, Monthly budget N, Transactions R, Spent this month RU(sum), Remaining F, Used F |
| 15 | Transactions | Description T, Amount N, Type S(Expense, Income), Date D, Category R, Method S, Month F, Spent this month F |
| 16 | Subscriptions | Name T, Cost N, Cycle S, Next renewal D, Status S, Category S, Monthly cost F, Yearly cost F, Renews in (days) F |
| 17 | Money Goals | Name T, Kind S, Target N, Current N, Target date D, Progress F, Progress Bar F, Per month needed F |
| 18 | Contacts | Name T, Circle S, Birthday D, Phone P, Email E, Last contacted D, Notes Tx, Next birthday F, Days to birthday F, Birthday soon F |
| 19 | Documents | Name T, Category S, Expires D, Where it lives Tx, File FL, Expiry F |
| 20 | Trips | Trip T, Destination Tx, Dates D, Status S, Budget N |
| 21 | Lists | Item T, List S, Got it CB, Price N, Link U, For R(Contacts, one-way) |

Counts: 21 databases, 22 formula properties, 4 rollups, 20 relation properties (8 two-way pairs = 16 properties, plus 4 one-way: Meal Plan Breakfast/Lunch/Dinner and Lists For).

## Sample records (production and dev)

| Database | Rows | Database | Rows |
|---|---:|---|---:|
| Life Areas | 8 | Meal Plan | 5 |
| Goals | 5 | Home Care | 8 |
| Projects | 3 | Budget Categories | 7 |
| Tasks | 12 | Transactions | 12 |
| Reviews | 1 | Subscriptions | 5 |
| Journal | 3 | Money Goals | 3 |
| Daily Log | 7 | Contacts | 5 |
| Library | 5 | Documents | 4 |
| Ideas & Inspo | 4 | Trips | 2 |
| Workouts | 4 | Lists | 12 |
| Recipes | 5 | **Total** | **120** (corrected 2026-10-14; earlier "131" was an addition error) |

All sample dates cluster around 2026-10-14. Every sample person and brand is fictional or generic.

## Buttons and database templates

| Item | Present | Notes |
|---|---|---|
| Button blocks (Today, Money) | No | Listed as a manual step on the Finishing checklist |
| Database templates (any database) | No | None exist. Review prompts live in a callout and in the sample "Week 41" review |

## Hidden or seller-only content

- "Finishing checklist (seller only, delete before publishing)" is a child of the customer hub. Defect D-01.
- The dev copy itself (marked do not sell).

## Orphans, duplicates, unused fields

- No orphaned pages found under the hub.
- No duplicate databases.
- Unused or low-value fields: Life Areas `Goal Count` counts achieved goals too (cosmetic). Library `Cover` and Ideas `Image` are empty in sample data (expected, user uploads).
- Redundant formulas: none. `Habits Done` feeds `Habit Bar` and the chart; `Progress` feeds `Progress Bar`.
