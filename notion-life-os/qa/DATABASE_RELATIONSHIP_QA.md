# Database Relationship QA

| Test | Method | Status | Notes |
|---|---|---|---|
| All relations in dev point to dev databases | Fetched every changed schema; checked `dataSourceUrl` and rollup targets | PASS | No production IDs referenced |
| Two-way relations wired | Child-side writes populated parent side (sample data) | PASS | |
| New rollups resolve to the right relation and target | Read back after save (Tasks → Done "checked", Tasks → Canceled "checked", Tasks → Name "count", Projects → Progress "average", Transactions → Saved or repaid this month "sum") | PASS (config) | |
| Goal progress via projects (rollup of a formula) | Saved and read back | PASS (config), output BLOCKED | Was the D-13 fix; previously impossible via formula |
| Tick task → project and goal progress change (R-REL-1) | Needs write + filtered read | BLOCKED (quota) | Expected: ticking "Tempo run, 20 min" moves 10K goal 50% → 75% |
| Unlink task → denominator drops (R-REL-2) | | BLOCKED | |
| Re-categorize transaction (R-REL-3) | | BLOCKED | |
| Delete task leaves rollup (R-REL-4) | | BLOCKED | |
| Cancel a task excluded from progress | | BLOCKED | Expected: 4 tasks, 3 done, 1 canceled → 100% |
| Double counting | Design review | PASS | Each transaction has one Category; each task counts once per parent |
| Temporary test records created and removed | | NOT TESTED | None created, because creating them without a way to read results would leave untested clutter |
