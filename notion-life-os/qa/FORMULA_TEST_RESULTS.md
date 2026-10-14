# Formula Test Results

Method: expected values from `tools/expected_values.py` (independent of Notion). Actual values from server-side filters on formula results. Status: PASS, FAIL, BLOCKED, NOT TESTED, N/A.

## Execution log

| When | Target | Probes run | Outcome |
|---|---|---|---|
| Phase 1 | Production (1 probe), dev (10 probes) | 11 | 11 PASS |
| Phase 1, probe 12 | Dev Daily Log | 0 | Quota reached ("usage limit reached, try again later") |
| Phase 7 | Dev Budget status | 0 | Quota still reached. All post-fix probes BLOCKED |

No probe was ever retried automatically after the quota message.

## Results

| ID | Formula | Baseline (pre-fix) | Post-fix |
|---|---|---|---|
| F1 | Tasks.Status Label | PASS (12/12 rows) | BLOCKED (formula extended with "Canceled" branch; existing branches unchanged) |
| F2/F3 | Goals.Progress / Progress Bar | PASS (5/5 rows) | BLOCKED. Expected: 10K 50%, Emergency 50%, Read 58%, Bedroom 0%, Pottery "No tasks linked yet" |
| F4 | Projects.Progress Bar | PASS (2/3), 1 BLOCKED | BLOCKED. Expected 50%, 50%, 0% |
| F5/F6 | Daily Log.Habits Done / Habit Bar | BLOCKED | BLOCKED (unchanged formula) |
| F7 | Life Areas.Balance | BLOCKED | BLOCKED (clamped) |
| F8/F9 | Home Care.Next due / Due | BLOCKED | BLOCKED |
| F10/F11 | Budget.Remaining / Used | BLOCKED | BLOCKED (now based on Actual this month) |
| F13 | Transactions.Spent this month | BLOCKED | BLOCKED. Expected consumption total 1,682.85 |
| F14/F15 | Subscriptions.Monthly / Yearly | BLOCKED | BLOCKED. Expected Newspaper 21.67 / 260.00 |
| F16 | Subscriptions.Renews in | BLOCKED | BLOCKED (now from Next charge) |
| F17 to F19 | Money Goals | BLOCKED | BLOCKED |
| F20 to F22 | Contacts birthdays | BLOCKED | BLOCKED |
| F23 | Documents.Expiry | BLOCKED | BLOCKED |
| New | Budget.Saved or repaid, Actual this month, Budget status | N/A | BLOCKED. Expected Rent and Savings "✓ Fully used"; Groceries "On track: 197.45 left" |
| New | Goals.Goal health | N/A | BLOCKED. Expected 4 "On track", Pottery "Not enough information" |
| New | Subscriptions.Next charge, Due this week | N/A | BLOCKED. Expected Due this week = Streaming, Gym, Weekend newspaper |
| New | Money Goals.Remaining, Goal status | N/A | BLOCKED. Expected 3850 / 900 / 2900, all In progress |

## What is verified for every changed formula

Every new or changed formula was accepted by Notion's formula type checker when saved. Notion rejects formulas with type or parse errors at save time (this happened several times during the original build). This shows the formulas are well formed. It does not show their values are right, so their status stays BLOCKED, not PASS.

## Edge-case tests still to run (need temporary records plus probes)

Listed with expected outcomes at the end of `tools/expected_values.py` output: Feb 29 birthday, Dec 31 birthday, subscription roll-forward (two cases), weekly subscription cost, paused subscription, overpaid money goal, empty Every, canceled task, decreasing number goal. Also: end-of-month transaction (Oct 31 vs Nov 1) and a time-zone check of "Spent this month" near midnight on the 1st.

## How to unblock

1. Wait for the Notion connector quota to reset, then re-run each probe in this file (about 30 probes), or
2. Open each view in the Notion app and compare against `python3 -I tools/expected_values.py <date>`.
