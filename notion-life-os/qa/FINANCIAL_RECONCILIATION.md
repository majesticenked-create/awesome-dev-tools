# Financial Reconciliation

Reference date 2026-10-14. Independent values from `tools/expected_values.py`. Notion outputs could not be read back (connector quota), so the "Notion output" column is BLOCKED except where noted.

## Definitions (now in the product)

| Type | Counts as spending | Shown as | In budget Actual |
|---|---|---|---|
| Expense | Yes | Spent this month | Yes |
| Refund | Reduces spending | Spent this month (negative) | Yes |
| Savings | No | Saved or repaid | Yes (for the savings category) |
| Debt payment | No | Saved or repaid | Yes |
| Transfer | No | Not in budgets | No |
| Income | No | Not in budgets | No |

Spending excludes savings and transfers. Moving money into savings is not a loss of net worth, so it is not counted as spending.

## Category reconciliation (October 2026 sample)

| Category | Budget | Independent spent | Historical reference | Saved or repaid | Actual | Expected status | Notion output |
|---|---:|---:|---:|---:|---:|---|---|
| Rent | 1,200.00 | 1,200.00 | | 0.00 | 1,200.00 | ✓ Fully used | BLOCKED |
| Groceries | 400.00 | 202.55 | 202.55 ✓ | 0.00 | 202.55 | On track: 197.45 left | BLOCKED |
| Transport | 150.00 | 113.50 | 113.50 ✓ | 0.00 | 113.50 | On track: 36.5 left | BLOCKED |
| Eating out | 150.00 | 73.80 | 73.80 ✓ | 0.00 | 73.80 | On track: 76.2 left | BLOCKED |
| Fun & hobbies | 100.00 | 93.00 | | 0.00 | 93.00 | On track: 7 left | BLOCKED |
| Savings | 300.00 | 0.00 (was 300.00) | | 300.00 | 300.00 | ✓ Fully used | BLOCKED |
| Salary (income) | none | 0.00 | | 0.00 | 0.00 | No budget set | BLOCKED |
| **Consumption spending** | | **1,682.85** (was 1,982.85) | | | | | BLOCKED |

All three historical reference values match the independent recalculation. Nothing is hard-coded.

Discrepancy fixed: before the change, the $300 savings transfer was counted as spending, overstating consumption by 17.8% and drawing Savings as a spending bar. Corrective action: Type "Savings", separate column, chart filter.

## Subscriptions (conversion basis: weekly × 52 ÷ 12, quarterly ÷ 3, yearly ÷ 12)

| Item | Cost | Cycle | Expected monthly avg | Expected yearly | Status rule |
|---|---:|---|---:|---:|---|
| Weekend newspaper | 5.00 | Weekly | 21.67 | 260.00 | Cancel soon still counts |
| Streaming | 12.99 | Monthly | 12.99 | 155.88 | |
| Music | 10.99 | Monthly | 10.99 | 131.88 | |
| Cloud storage | 29.99 | Yearly | 2.50 | 29.99 | |
| Gym | 35.00 | Monthly (Trial) | 35.00 | 420.00 | |
| Any | | | 0 when Paused or Cancelled | 0 | |

Average monthly cost is not the cash due in a given month. A yearly plan shows 2.50/month but charges 29.99 once. This is stated in the column description and in Start Here.

## Savings and debt goals

| Goal | Kind | Target | Current | Remaining | Progress | Per month (to target date) | Status |
|---|---|---:|---:|---:|---:|---:|---|
| Emergency fund | Emergency fund | 6,000 | 2,150 | 3,850 | 36% | 770 | In progress |
| Credit card payoff | Debt payoff | 1,800 | 900 paid off | 900 still owed | 50% | 300 | In progress |
| Japan trip fund | Savings | 3,500 | 600 | 2,900 | 17% | 290 | In progress |

Debt rule: Current = amount paid off, so progress rises as the debt falls. A larger remaining balance never shows as more complete.

Edge cases (expected; BLOCKED): fully paid (Current = Target) → 100%, Remaining 0, "✓ Reached". Overpaid (Current > Target) → bar 100%, Remaining 0, Per month 0, "✓ Reached". Zero target → "Set a target", no division error.

## Budget edge cases (expected behavior; BLOCKED)

| Case | Expected |
|---|---|
| Zero or empty budget | "No budget set"; Used blank; no error |
| Over budget | "⚠ Over by X" (text, not colour only) |
| Transaction dated last month | Not in this month's Spent |
| Re-categorized transaction | Moves between category rows |
| Deleted transaction | Leaves the rollup |
| Refund larger than spending in a category | Spent can go negative; status shows "On track" with more than the budget left |
