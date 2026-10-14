# Release Readiness Report

## Verdict: NOT READY TO SELL

High-severity items remain open and essential functions are not yet verified.

## Blocking items

| # | Item | Severity | Who can clear it |
|---|---|---|---|
| 1 | No quick-add buttons (D-02) | High | Owner, in the Notion app (about 15 minutes, specs ready) |
| 2 | No database templates (D-03) | High | Owner, in the Notion app (about 30 minutes, text ready) |
| 3 | Two charts vs free-plan limit of one (D-24) | High | Owner decision, then a 1-minute change |
| 4 | Clean-account duplication not tested (D-27) | High | Owner, with a second free Notion account |
| 5 | Formula outputs unverified after changes (D-28) | Medium, but required by rule 15 | Re-run probes after the Notion connector quota resets, or check in the app |
| 6 | Product name (D-26) | Medium | Owner decision |
| 7 | Mobile not tested | Medium | Owner, on a phone |

## What is done and verified

- Dev copy created; production untouched apart from one reverted schema slip (CHANGELOG, D-29).
- Seller-only content removed from the customer hub (verified by fetch).
- Em dashes removed from customer copy (verified by fetch).
- Financial model corrected: savings no longer counted as spending; refunds, transfers and debt payments defined; overspend shown in words. Independent recalculation reproduces the historical references exactly (Transport 113.50, Groceries 202.55, Eating out 73.80).
- Goals support task and number measures, project fallback, empty states and a documented health rule.
- Canceled tasks have one consistent rule across all views and progress.
- Birthday, renewal, home care and money goal edge cases are handled in the formulas, with policies documented.
- Start Here rewritten with clear automatic vs manual guidance and troubleshooting.
- Every changed formula passed Notion's save-time type check, and every view change was read back.

## Phase 6 enhancement decisions

| Enhancement | Decision | Reason |
|---|---|---|
| A. Weekly command center | Deferred | The Hub's "Coming up this week", Plan's Focus and Calendar tabs, and the Weekly review template already cover it. A separate page would duplicate views. |
| B. Monthly reset | Done as a template (Monthly review) | A guided template avoids destructive reset buttons. |
| C. Focus mode | Done | "Focus: high priority" tab on Plan → Tasks. No artificial limit; buyers change the filter. |
| D. Goal health indicators | Done | On track / Needs attention / Completed / Not enough information, rules in the property description and Start Here. |
| E. Personalization | Done (documentation) | Start Here explains renaming areas, habits, options and prompts, and which formula to edit when adding a habit. |

## Path to release

1. Owner: approve chart removal (recommend removing Habit trend), choose the product name, choose the edition plan.
2. Owner (Notion app, about 1 hour): buttons, templates, view polish, font and covers, from the SELLER NOTES checklist.
3. Re-run formula and relation probes when the connector quota resets (about 30 probes listed in FORMULA_TEST_RESULTS.md), or check by eye using `tools/expected_values.py`.
4. Make the dev copy the release candidate: rename it, publish with "Allow duplicate as template".
5. Duplication test with a second free account; phone check.
6. Package (PDFs, links). Etsy listing only after your explicit approval.

When steps 1 to 5 pass with no open High items, the status can move to READY AFTER EXTERNAL TESTS, and then to READY TO SELL once the duplication and device tests pass.
