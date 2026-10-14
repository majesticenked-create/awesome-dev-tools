# 02 Formula Audit

## Method

1. Expected values were computed independently in Python from the raw sample inputs (`qa/tools/expected_values.py`, reference date 2026-10-14). The script never reads Notion formula output.
2. Actual values were observed with server-side filters: Notion is asked for the rows whose formula result equals the expected value, and the returned rows are compared with the expected set. This exercises Notion's real formula engine. It does not rely on any formula's own output to validate itself.
3. The free-plan connector quota for filtered queries ran out after 11 probes. Formulas not yet probed are marked BLOCKED, not passed.

Formula expressions below come from the build record (`BUILD_SPEC.md`, build log section). The connector cannot read formula code back, so a final check in the Notion UI is recommended.

Status key: PASS, FAIL, BLOCKED (could not execute), DESIGN (works as written but the behavior is a defect), N/T (not tested).

## Results

| # | Database.Property | Expression (summary) | Expected (sample) | Observed | Status |
|---|---|---|---|---|---|
| F1 | Tasks.Status Label | ifs(Done, "✓ Done", empty(Do date), "Inbox", days<0, "⚠ Overdue", days==0, "Today", "Upcoming") | Today: 2, Upcoming: 5, Done: 3, Overdue: 1, Inbox: 1 | Today: exactly the 2 expected rows; Upcoming: exactly the 5 expected; Done + Overdue + Inbox: exactly the 5 expected; Overdue alone: exactly "Cancel unused streaming trial" | PASS |
| F2 | Goals.Progress (rollup, percent checked) | Tasks → Done → percent checked | 10K 50%, Emergency 50%, Read 0%, Bedroom 0%, Pottery (no tasks) 0% | Verified through F3 | PASS |
| F3 | Goals.Progress Bar | repeat("▰", round(p×10)) + repeat("▱", …) + "  " + round(p×100) + "%" | "▰▰▰▰▰▱▱▱▱▱  50%" for 10K and Emergency; "▱…▱  0%" for Read, Bedroom, Pottery | 50%: exactly 10K and Emergency. 0%: exactly Read, Bedroom, Pottery | PASS, but see D-11 (no-task goal shows "0%" instead of a not-configured state) |
| F4 | Projects.Progress + Progress Bar | same as goals | 10K plan 50%, Automate savings 50%, Bedroom refresh 0% | 50%: exactly 10K plan and Automate savings. 0% row: not probed | PASS (2/3 rows), 1 row BLOCKED |
| F5 | Daily Log.Habits Done | sum of 5 checkboxes as numbers | 3,2,5,4,3,1,3 | Quota exhausted on this probe | BLOCKED |
| F6 | Daily Log.Habit Bar | repeat("◆", n) + repeat("◇", 5−n) | ◆◆◆◇◇ ×3 rows | Quota exhausted | BLOCKED |
| F7 | Life Areas.Balance | repeat("●", s) + repeat("○", 10−s) | 8 bars | Not probed | BLOCKED |
| F8 | Home Care.Next due | dateAdd(Last done, Every, "days") | see script | Not probed | BLOCKED |
| F9 | Home Care.Due | label from days to Next due | 1 overdue ("⚠ 3d overdue"), 7 "In Nd" | Not probed | BLOCKED |
| F10 | Budget.Remaining | Monthly budget − Spent this month | Groceries 197.45, Transport 36.50, Eating out 76.20 | Not probed | BLOCKED |
| F11 | Budget.Used | bar + % | Groceries 51%, Transport 76%, Eating out 49% | Not probed | BLOCKED |
| F12 | Transactions.Month | formatDate(Date, "MMMM YYYY") | "October 2026" ×12 | Not probed | BLOCKED |
| F13 | Transactions.Spent this month | Amount if Expense and same month as now(), else 0 | Groceries rows sum 202.55, Transport 113.50, Eating out 73.80 | Not probed | BLOCKED, and DESIGN defect D-08 (savings transfers count as spending) |
| F14 | Subscriptions.Monthly cost | Weekly ×52/12, Quarterly /3, Yearly /12, else Cost | Newspaper $5 weekly = 21.6667 | Not probed | BLOCKED. Expression matches the required basis. |
| F15 | Subscriptions.Yearly cost | Monthly cost × 12 | Newspaper 260.00 | Not probed | BLOCKED |
| F16 | Subscriptions.Renews in (days) | dateBetween(Next renewal, today) | 5, 14, 112, 2, 3 | Not probed | BLOCKED, DESIGN defect D-14 (goes negative after the date passes) |
| F17 | Money Goals.Progress | min(Current/Target, 1), 0 if Target is 0 | 0.3583, 0.5, 0.1714 | Not probed | BLOCKED |
| F18 | Money Goals.Progress Bar | bar + % | 36%, 50%, 17% | Not probed | BLOCKED |
| F19 | Money Goals.Per month needed | (Target−Current)/months left | 770, 300, 290 | Not probed | BLOCKED, DESIGN defect D-16 (negative when overpaid) |
| F20 | Contacts.Next birthday | Birthday moved to this year, or next year if passed | Grandma 2026-10-22 | Not probed | BLOCKED, D-19 (Feb 29 policy undefined) |
| F21 | Contacts.Days to birthday | dateBetween(Next birthday, today) | 8, 151, 19, 259 | Not probed | BLOCKED |
| F22 | Contacts.Birthday soon | Days to birthday ≤ 14 | Only Grandma Rose | Not probed | BLOCKED |
| F23 | Documents.Expiry | "⚠ Expired" / "Renew soon" (<60 days) / "OK" / "—" | Passport "Renew soon", others "OK" | Not probed | BLOCKED |

Totals: 4 PASS, 1 partial PASS, 18 BLOCKED, 0 FAIL observed.

## Edge-case analysis (from expressions, to be confirmed by probes)

| Edge case | Affected formulas | Expected behavior per expression | Risk |
|---|---|---|---|
| Empty dates | Status Label, Next due, Due, Renews in, Days to birthday, Expiry, Per month needed | Status Label → "Inbox"; Due → "Set last done"; Expiry → "—"; Renews in and Days to birthday → blank; Per month needed → full remaining amount | Low |
| Empty number (Every) | Home Care Next due / Due | dateAdd with empty interval likely returns Last done, so a chore with no interval shows as overdue | D-17 |
| Zero denominator | Budget Used, Money Goals Progress | Both guard Target/Monthly budget = 0 | OK |
| Empty Monthly budget | Budget Remaining | Empty minus Spent likely shows −Spent | D-10 (low impact; Income row hidden) |
| No related records | Goals/Projects Progress | Rollup returns 0, bar shows "0%" | D-11 |
| Satisfaction > 10 or < 0 | Life Areas Balance | repeat with negative count | D-18 |
| Current > Target | Money Goals Per month needed | Negative amount | D-16 |
| Month and year rollover | Spent this month | Compares formatDate(Date, "YYYY-MM") with now(); resets on the 1st | Works as designed; D-09 for sample data going stale |
| Feb 29 birthday | Next birthday | Depends on Notion dateAdd behavior for Feb 29 + years in non-leap years | D-19 |
| Date with time | Status Label | dateBetween in days truncates; a task due later today stays "Today" | OK |
| Archived records | All rollups | Notion excludes archived pages from relations | N/T |
| Duplicate Daily Log rows | Habit chart | Both rows count | D-22 |

## Unblocking

Re-run `qa/tools/expected_values.py` with the probe date and repeat the BLOCKED probes once the Notion connector quota resets, or check the values by eye in the Notion UI (each check is listed in 06_Regression_Baseline.md).
