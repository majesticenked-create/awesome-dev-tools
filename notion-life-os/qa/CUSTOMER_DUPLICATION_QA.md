# Customer Duplication QA

## Status: NOT PERFORMED

No second Notion account was available in this session. Rule 7.6 requires an independent account, ideally on the free plan.

## Partial evidence (same account, same workspace)

The dev copy was created with Notion's native Duplicate. Checked by API afterwards:

| Check | Result |
|---|---|
| All 10 pages copied | Yes |
| All 21 databases copied with records | Yes |
| Relations point to the copied databases, not the originals | Yes (every schema checked) |
| Rollups point to the copied databases | Yes |
| All 33 linked views point to copied databases | Yes |
| Formulas carried over | Yes (present in schema) |

Same-workspace duplication is not the same as a buyer duplicating a public template into their own workspace, so this does not replace the real test.

## Checklist for the real test (second free account)

1. In the release candidate: Share → Publish → Allow duplicate as template. Copy the link.
2. In a private window, sign in to the second free account and open the link. Click Duplicate.
3. Check:
   - [ ] All pages exist: Hub, Start Here, Today, Plan, Mind, Body & Home, Money, Life Admin, Databases
   - [ ] No SELLER NOTES or Finishing checklist
   - [ ] Each linked view opens the buyer's copy (edit a sample row in Today; it changes in Databases)
   - [ ] Tick a task Done; project and goal progress change
   - [ ] Add an expense; budget row updates
   - [ ] Buttons create rows in the buyer's databases (after D-02)
   - [ ] Templates appear under New ▾ (after D-03)
   - [ ] No upgrade prompt appears (watch for charts, D-24)
   - [ ] Start Here links open the buyer's pages
4. Record results here with date, account plan and device.
