# Customer Package Inventory

## Editions: recommendation

| Option | Pros | Cons |
|---|---|---|
| A. One template with sample data, plus "Remove the sample data" steps (current) | One thing to maintain; buyers learn from examples | Buyer spends about 5 minutes deleting rows |
| B. Two templates: Blank and Example | Clean start available | Every future fix must be made twice or re-derived; editions drift |
| C. One template, Example only, plus a blank duplicate made at release time from the same source | Single source of truth; blank edition re-created on each release by duplicating and bulk-deleting rows | Release step needs about 10 minutes and owner approval for the deletions |

**Recommended: C.** Keep one source (the release candidate with sample data). At each release, duplicate it and delete the sample rows in the copy to make the Blank edition. Never edit the Blank edition directly. Deleting rows is a destructive step, so it needs your go-ahead; it can be done through the connector, 20 rows per call.

## Delivery files

| File | Status | Notes |
|---|---|---|
| Duplicate link: Example edition | **Release blocker, not created** | Needs Publish → Allow duplicate as template, plus the duplication test |
| Duplicate link: Blank edition | **Release blocker, not created** | Depends on edition decision |
| START_HERE.pdf | Not created | Source text is the dev Start Here page; export after final review |
| QUICK_START.pdf | Not created | One page: open link, Duplicate, open Start Here, do the first five steps |
| FEATURE_GUIDE.pdf | Not created | Can be built from Start Here sections |

No placeholder links have been created. A private development link must never go into the delivery PDF.

## Before packaging

- Product name decision (D-26)
- Chart decision (D-24)
- Buttons and templates created (D-02, D-03)
- Sample dates refreshed (D-21)
- Duplication test passed (CUSTOMER_DUPLICATION_QA.md)
