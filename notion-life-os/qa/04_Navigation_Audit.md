# 04 Navigation Audit

Method: fetched every page in the dev copy and every linked-view block. "Click" here means resolving the link target through the API, not a mouse click in the app.

## Hub links

| Link | Target resolves | Inside the hub tree (ships with duplicate) | Points to dev, not production |
|---|---|---|---|
| Today | Yes | Yes | Yes |
| Plan | Yes | Yes | Yes |
| Mind | Yes | Yes | Yes |
| Body & Home | Yes | Yes | Yes |
| Money | Yes | Yes | Yes |
| Life Admin | Yes | Yes | Yes |
| Start Here | Yes | Yes | Yes |
| Databases | Yes | Yes | Yes |
| Finishing checklist | Yes | Yes, which is the problem | Yes. Seller-only page ships to buyers (D-01) |

All hub links are child-page blocks, not mentions of outside pages, so a duplicate carries them along.

## Linked views

| Page | Views | Source collections |
|---|---|---|
| Hub | This week, Goals in motion, Life balance | Tasks, Goals, Life Areas (dev) |
| Today | Today & overdue, Today's check-in, Today's entries, Today's meals, Renewing this week, Birthdays soon | Tasks, Daily Log, Journal, Meal Plan, Subscriptions, Contacts (dev) |
| Plan | Life areas, Goals by status, Projects by status, Open tasks, Reviews | dev |
| Mind | Journal calendar, Habit tracker, Bookshelf, Ideas & vision board, Habit trend (chart) | dev |
| Body & Home | Workout log, This week's meals, Recipe box, Home care, Grocery list | dev |
| Money | Budget, Transactions, Subscriptions, Money goals, Spending by category (chart) | dev |
| Life Admin | Contacts, Documents, Trips, Lists | dev |

All 33 linked views reference the dev copy's own collections. Duplication within the same workspace remapped them correctly.

## View-level findings

| View | Finding | Defect |
|---|---|---|
| Today / Birthdays soon | Filter list is empty. The view shows every contact, including people with no birthday. Text above it says "Birthdays in the next two weeks". | D-04 |
| Today / Renewing this week | Uses the static Next renewal date. Once a renewal date passes it never shows again until the buyer edits the date. | D-14 |
| Money / Spending by category | Includes the Savings category, so a savings transfer is drawn as spending. | D-08 |
| Mind / Habit trend and Money / Spending by category | Two chart views. Notion's free plan allows a limited number of charts per workspace (believed to be 1). Needs confirming on a free account. | D-24 |
| Plan / Open tasks | Inbox tasks (no date) sort to the bottom as described. | OK |

## Export note (birthday CSV)

The earlier export review reported that the Today page references a birthday CSV that was not in the export. In the live workspace the "Birthdays soon" block is a linked view of the Contacts database, whose source lives under Databases. Notion exports a linked view as a link to the source database's CSV, so a partial export (for example, exporting only Today, or exporting without subpages) produces a link to a file that is not in the ZIP. This is an export artifact, not a missing database. Buyers receive a duplicate link, not an export, so they are not affected. The ZIP itself was not provided in this session, so this is reasoned from Notion's export behavior and the live structure, not confirmed against the file.

## Mobile

NOT TESTED. No mobile device or mobile app is available in this session. Structural notes only: the hub uses a 3-column block, which Notion's mobile app stacks vertically; Today is single-column by design.
