# 06 Regression Baseline

Baseline date: 2026-10-14 (all date-relative expectations assume this date; regenerate with `python3 -I qa/tools/expected_values.py YYYY-MM-DD` for any other day).

## How to run a check

- **API probe:** query the data source with a formula-result filter equal to the expected value and confirm the returned rows are exactly the expected rows.
- **UI check:** open the view in Notion and read the value. Use this when the connector quota is exhausted.

## Baseline checks

| ID | Area | Check | Expected | Baseline result |
|---|---|---|---|---|
| R-F1 | Tasks | Status Label for all 12 tasks | Today 2, Upcoming 5, ✓ Done 3, ⚠ Overdue 1 (Cancel unused streaming trial), Inbox 1 (Book dentist) | PASS |
| R-F2 | Goals | Progress Bar | 10K and Emergency "▰▰▰▰▰▱▱▱▱▱  50%"; Read, Bedroom, Pottery "▱▱▱▱▱▱▱▱▱▱  0%" | PASS |
| R-F3 | Projects | Progress Bar | 10K plan, Automate savings 50%; Bedroom refresh 0% | PASS (50% rows), 0% row BLOCKED |
| R-F4 | Daily Log | Habits Done / Habit Bar | 8 Oct 3, 9 Oct 2, 10 Oct 5, 11 Oct 4, 12 Oct 3, 13 Oct 1, 14 Oct 3 | BLOCKED |
| R-F5 | Home Care | Due | Clean bathroom "⚠ 3d overdue"; bedsheets and plants "In 2d"; fridge "In 6d"; vacuum "In 4d"; smoke alarm "In 93d"; kettle "In 15d"; tyres "In 11d" | BLOCKED |
| R-F6 | Contacts | Days to birthday / Birthday soon | Grandma 8 (soon), Sam 19, Maya 151, Priya 259; Dr. Lee blank | BLOCKED |
| R-F7 | Documents | Expiry | Passport "Renew soon" (48 days); others "OK" | BLOCKED |
| R-F8 | Subscriptions | Monthly / Yearly | Newspaper 21.67 / 260.00; Cloud 2.50 / 29.99; Gym 35 / 420 | BLOCKED |
| R-F9 | Budget | Spent this month | Rent 1200, Groceries 202.55, Transport 113.50, Eating out 73.80, Fun 93.00, Savings 300.00 | BLOCKED |
| R-F10 | Budget | Remaining / Used | Groceries 197.45 / 51%; Transport 36.50 / 76%; Eating out 76.20 / 49%; Fun 7.00 / 93% | BLOCKED |
| R-F11 | Money Goals | Progress / Per month | Emergency 36% / 770; Credit card 50% / 300; Japan 17% / 290 | BLOCKED |
| R-F12 | Life Areas | Balance | Relationships 8 dots … Fun 4 dots | BLOCKED |
| R-V1 | Views | All 33 linked views resolve to dev collections | Yes | PASS |
| R-V2 | Today | Birthdays soon filtered to ≤14 days | Only Grandma Rose | FAIL (no filter) |
| R-V3 | Today | Today & overdue filter | Done = false AND Do date ≤ today | PASS (config read) |
| R-N1 | Hub | 9 child links resolve | Yes | PASS |
| R-N2 | Hub | No seller-only pages | None | FAIL (D-01) |
| R-C1 | Copy | No em dashes in customer copy | 0 | FAIL (D-20) |
| R-REL-1 | Relations | Tick a task → goal and project progress change | 10K goal 50% → 75% when "Tempo run" ticked | BLOCKED |
| R-REL-2 | Relations | Unlink a task → denominator drops | | BLOCKED |
| R-REL-3 | Relations | Move a transaction category | Both budget rows change | BLOCKED |
| R-REL-4 | Relations | Delete a task → leaves rollup | | BLOCKED |
| R-B1 | Buttons | Quick-add buttons exist and work | 4 buttons | FAIL (none exist; D-02) |
| R-T1 | Templates | Templates exist for 8 databases | 8+ templates | FAIL (none; D-03) |
| R-D1 | Duplication | Clean-account duplicate works | | NOT TESTED (no second account) |
| R-M1 | Mobile | Today and hub usable on phone | | NOT TESTED (no device) |

Summary at baseline: 5 PASS, 1 partial, 5 FAIL, 13 BLOCKED, 2 NOT TESTED.
