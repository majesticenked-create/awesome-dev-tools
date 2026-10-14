# Customer Duplication QA (Phase 9D)

## Status: NOT PERFORMED

Checked 2026-10-14. This session has access to one Notion workspace only (the seller's). There is no second Notion account, free or otherwise, and no browser to sign in to one. A duplication test needs an independent account, so it was not run. Neither edition has been duplicated into another account. Free-plan chart behavior has not been tested in any workspace.

Nothing below is marked passed.

## Evidence available from the seller's workspace (not a substitute)

| Check | Result | How |
|---|---|---|
| Dev copy made by native Duplicate has all 10 pages and 21 databases | Yes (Phase 2) | Fetch |
| Relations, rollups and all linked views point at the copy's own databases | Yes (Phase 2, re-checked for views changed in Phase 9) | Fetch |
| Seller-only pages (SELLER NOTES, Finishing checklist, QA harness, QA TEMP records) are outside the product tree | Yes | They sit under "LifeOS SELLER NOTES", which is a separate top-level page; the hub fetch shows no link to it |
| One chart left in the product | Yes | All 21 source databases (22 views, all tables) and all 35 linked-view blocks (38 views) on the 8 dashboard pages fetched on 2026-10-14. The only chart is Money → Spending by category |

## Test script for each edition (Example, then Blank), in a separate free account

Record date, account plan, device and browser for each run.

1. In the release candidate: Share → Publish → turn on "Allow duplicate as template". Copy the link. **Requires your approval; do not share it publicly.**
2. In a private window, sign in to the free test account and open the link. Click Duplicate.
3. Check, ticking only what you actually saw:
   - [ ] Pages: Hub, Start Here, Today, Plan, Mind, Body & Home, Money, Life Admin, Databases
   - [ ] No SELLER NOTES, checklist, QA harness or QA TEMP pages anywhere
   - [ ] Hub title reads "LifeOS - All-in-One Life Planner" with no DEV marker
   - [ ] Each linked view opens the buyer's own copy (edit a sample row in Today; the change shows in Databases)
   - [ ] Tick "Tempo run, 20 min" Done: Run a 10K goal goes from 50% to 75%; 10K training plan project goes from 50% to 75% (Example edition)
   - [ ] Add an Expense of 10 to Groceries: Budget shows "On track: 187.45 left" (Example edition)
   - [ ] Buttons B1 to B4 create rows in the buyer's databases
   - [ ] Templates appear under New ▾ and the defaults apply
   - [ ] Start Here links open the buyer's pages
   - [ ] **Chart, workspace with no other chart:** Money → Spending by category displays, with no upgrade prompt
   - [ ] **Chart, workspace that already has one chart:** record exactly what Notion shows (upgrade prompt, locked chart, or nothing). Then delete the LifeOS chart and confirm the Budget table still shows all values
   - [ ] No other upgrade prompt anywhere
4. Phone (iOS or Android app): open Today and the Hub; note any view that needs sideways scrolling.

## Results

| Run | Edition | Account plan | Workspace had a chart already? | Device | Result |
|---|---|---|---|---|---|
| none yet | | | | | NOT PERFORMED |
