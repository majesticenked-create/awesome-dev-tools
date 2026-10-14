# Customer Package Inventory

Product: **LifeOS - All-in-One Life Planner** (secondary description: "A Notion template"). Not affiliated with Notion Labs, Inc.

## Editions (approved 2026-10-14)

**The Example edition is the master.** Every fix is made there, in the dev copy, and nowhere else. For each release a **Blank edition** is generated from the master. Neither edition may be released until each is tested on its own.

### Release procedure

1. Finish and verify the master (buttons, templates, polish, refreshed sample dates).
2. Duplicate the master. Rename the copy "LifeOS - All-in-One Life Planner" (no DEV marker). This is the **Example release candidate**.
3. Duplicate the master again. Rename it "LifeOS - All-in-One Life Planner (Blank)". In this copy only, delete the sample rows in all 21 databases. Keep the databases, views, formulas, buttons and templates. Deleting rows is destructive, so it needs your go-ahead when the time comes. This is the **Blank release candidate**.
4. In the Blank candidate, check:
   - Every database shows 0 rows. Life Areas: decide whether to keep the 8 area names as a starter (recommended) or delete them too.
   - Hub, Today, Plan and Money views show empty states, not errors.
   - The Start Here "Remove the sample data" section reads correctly for a blank start (edit the text only in the Blank candidate).
   - Add one task, one goal, one expense and one log row; each formula fills in.
5. Test both candidates separately in a free Notion account (`CUSTOMER_DUPLICATION_QA.md`).
6. Only then publish with "Allow duplicate as template" and create the delivery links. **Not done; needs your explicit approval.**

### Status

| Edition | State | Tested |
|---|---|---|
| Example (master = dev copy) | Built; formulas verified (Phase 9B); buttons and templates missing | Not tested in a separate account |
| Blank | **Not generated.** It would have to be regenerated after buttons and templates are added, and creating it involves bulk deletion, which needs your approval | Not tested |

## Delivery files

| File | Status | Notes |
|---|---|---|
| Duplicate link: Example edition | **Not created** | Needs publishing approval and a passed duplication test |
| Duplicate link: Blank edition | **Not created** | As above |
| START_HERE.pdf | Not created | Source: dev Start Here page (now LifeOS wording) |
| QUICK_START.pdf | Not created | One page: open link, Duplicate, open Start Here, do the first five steps |
| FEATURE_GUIDE.pdf | Not created | Can be built from Start Here sections |

No placeholder or private development links have been created. No public link exists.

## Customer-facing copy rules (checked in Phase 9)

- Name: "LifeOS - All-in-One Life Planner". "A Notion template" only as the secondary line.
- Non-affiliation notice: Start Here → About LifeOS.
- No em dashes in customer pages (re-checked on the pages edited in Phase 9).
- No PurplePiece Studio branding.
- Listing copy (Etsy) not written or published. Publishing needs your approval.

## Before packaging

- [ ] Buttons B1 to B4 and templates T1 to T11 built and verified (`BUTTON_AND_TEMPLATE_QA.md`)
- [ ] View polish and visual design (seller checklist sections 4 and 5)
- [ ] Sample dates refreshed (D-21)
- [ ] Example and Blank candidates generated
- [ ] Both pass the free-account duplication test, including the chart check
- [ ] Phone check
