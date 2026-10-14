# 03 Database Relationship Audit

## Relation map

| From | Property | To | Reciprocal | Verified in dev copy points to dev |
|---|---|---|---|---|
| Goals | Area | Life Areas | Life Areas.Goals | Yes |
| Projects | Goal | Goals | Goals.Projects | Yes |
| Projects | Area | Life Areas | Life Areas.Projects | Yes |
| Tasks | Project | Projects | Projects.Tasks | Yes |
| Tasks | Goal | Goals | Goals.Tasks | Yes |
| Journal | Area | Life Areas | Life Areas.Journal | Yes (schema) |
| Ideas & Inspo | Area | Life Areas | Life Areas.Ideas | Yes (schema) |
| Transactions | Category | Budget Categories | Budget.Transactions | Yes |
| Meal Plan | Breakfast, Lunch, Dinner | Recipes | none (one-way) | Yes (schema) |
| Lists | For | Contacts | none (one-way) | Yes (schema) |

Verification method: fetched each dev data source schema and confirmed every `dataSourceUrl` and rollup `targetPropertyUrl` uses a dev collection ID (prefixes 78c5, 22e5, 2b25, b535, b835, 16a5 and so on), not a production ID (prefixes 4e28, 34f9, cc39, 41fb, 4247, 2c6f).

## Rollups

| Database | Rollup | Through | Target | Function | Status |
|---|---|---|---|---|---|
| Goals | Progress | Tasks | Done | percent checked | PASS (see 02 F2) |
| Projects | Progress | Tasks | Done | percent checked | PASS for 2 of 3 rows |
| Budget Categories | Spent this month | Transactions | Spent this month (formula) | sum | BLOCKED (quota) |
| Life Areas | Goal Count | Goals | Name | count | BLOCKED |

## Hierarchy behavior

Life Areas → Goals → Projects → Tasks.

1. **Goal progress counts only tasks linked directly to the goal.** A task linked to a project, where that project belongs to a goal, does not count toward the goal unless the task's own Goal field is also set. The sample data links every project task to both, so the sample looks right. A buyer who links tasks only to projects will see goal progress stuck at 0%. Defect D-13.
   - A formula that reads through the project relation was attempted during the build and rejected by the API. A rollup-of-rollup (average of project progress) is the candidate fix (Phase 2).
2. **Double counting.** A task linked to both a project and a goal is counted once in each. There is no path where one task is counted twice in the same total, so there is no double counting.
3. **Financial double counting.** Each transaction has a single Category relation. Rollup sums each transaction once. No double counting. Classification issue D-08 is separate.

## Change propagation test

| Test | Status |
|---|---|
| Tick a task Done, confirm project and goal progress update | BLOCKED (needs a write plus a filtered read; quota exhausted). Planned as regression R-REL-1. |
| Unlink a task, confirm progress denominator drops | BLOCKED, R-REL-2 |
| Move a transaction to another category, confirm both budget rows change | BLOCKED, R-REL-3 |
| Archive (delete) a task, confirm it leaves the rollup | BLOCKED, R-REL-4 |

Evidence available now: the sample data was created through the API with relations set on the child side only (for example Task.Goal), and the parent side (Goal.Tasks) filled in automatically, as seen in fetched rows. That confirms the two-way relations are wired.
