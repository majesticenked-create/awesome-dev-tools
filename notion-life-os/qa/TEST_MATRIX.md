# Test Matrix (as of 2026-10-14, end of Phase 9)

PASS means the test was run and the result was observed. Nothing is marked PASS on the strength of a formula being accepted by Notion. Details for each row are in the file named in "Evidence".

## Passed

| ID | Area | Test | Evidence |
|---|---|---|---|
| P-01 | Formulas | 12 databases, every changed formula, sample data: 79/79 rows equal the independent calculation | FORMULA_TEST_RESULTS.md |
| P-02 | Formulas | 46 edge cases (leap-day birthday, renewal roll-forward, refunds, overspend, canceled tasks, number goals, empty states, boundaries) | FORMULA_TEST_RESULTS.md (E-*) |
| P-03 | Harness | Negative control returns 0 rows | FORMULA_TEST_RESULTS.md |
| P-04 | Relations | Rollups update through relations: project from tasks; goal from tasks, and from projects when no tasks are linked; budget from transactions | E-P1, E-G1, E-B1 |
| P-05 | Data integrity | Production: 21/21 schemas match the baseline; relations point at production only; `noop_check` absent; 120/120 rows; 5/5 spot checks unchanged | PRODUCTION_INTEGRITY_CHECK.md |
| P-06 | Data integrity | Dev copy back to original sample data after tests: edge views empty, sample values re-checked, probe columns removed and schemas read back | FORMULA_TEST_RESULTS.md (Clean-up) |
| P-07 | Charts | Habit trend chart removed from Mind; Habit tracker and Habit Bar intact; full sweep of all 60 views finds exactly 1 chart | CHANGELOG.md, page and database fetches |
| P-12 | Name | No "Life Hub" text left on the 8 customer pages | Page fetches |
| P-08 | Name | LifeOS rename on Hub, Start Here, Databases page and seller notes; non-affiliation notice present; hub links and mentions resolve | CHANGELOG.md, NAVIGATION_AND_MOBILE_QA.md |
| P-09 | Copy | No em dashes in new customer copy | Page fetches |
| P-10 | Navigation | Hub has no link to seller-only pages | NAVIGATION_AND_MOBILE_QA.md |
| P-11 | Views | Birthdays soon filtered (Grandma Rose only); Renewing this week uses Due this week | Config read back plus Phase 9B values |

## Failed

| ID | Area | Test | Status |
|---|---|---|---|
| none | | No executed test failed in Phase 9 | |

## Blocked (needs something this session does not have)

| ID | Area | Test | Blocker |
|---|---|---|---|
| B-01 | Buttons | B1 to B4 created and clicked | No UI or browser tool. Spec: BUTTON_AND_TEMPLATE_QA.md |
| B-02 | Templates | T1 to T11 created and used | Same |
| B-03 | Duplication | Example edition duplicated into a separate free account | No second account |
| B-04 | Duplication | Blank edition generated and duplicated | Not generated (needs bulk deletion approval and should follow B-01/B-02); no second account |
| B-05 | Free plan | Chart in a free workspace with no other chart | No free test workspace |
| B-06 | Free plan | Chart in a free workspace that already has one chart | Same |

## Untested (possible later, by hand or on another date)

| ID | Area | Test | How |
|---|---|---|---|
| U-01 | Formulas | Budget reset on the 1st of the month | Manual matrix M1 |
| U-02 | Formulas | Feb 29 birthday in a leap year | M2 |
| U-03 | Formulas | Time-zone edge at midnight on the 1st | M3 |
| U-04 | Display | App shows the same values the filters matched | M4 |
| U-05 | Chart | Spending by category renders and totals 1,682.85 | M5 |
| U-06 | Mobile | Hub and Today on iOS and Android | NAVIGATION_AND_MOBILE_QA.md |
| U-07 | Visual | Fonts, spacing, dark mode, covers | Notion app |
| U-08 | Production | Production dashboard sub-pages (not just hub and databases) | Fetch, read only |
