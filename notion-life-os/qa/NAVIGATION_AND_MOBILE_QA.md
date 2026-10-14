# Navigation and Mobile QA

Environment: Claude Code cloud session, Notion connector (API). No browser session into Notion, no phone, no Notion app.

## Navigation (dev copy)

| Check | Method | Status |
|---|---|---|
| Hub links to 8 pages (Today, Plan, Mind, Body & Home, Money, Life Admin, Start Here, Databases) | Fetched hub; each link is a child-page block that resolves | PASS |
| No seller-only page reachable from the hub | Fetched hub after the move | PASS |
| Quick-action mentions point at dev databases (Tasks, Transactions, Daily Log) and dev Today | Read mention URLs | PASS |
| All linked views use dev collections | Fetched every page and changed view | PASS |
| No links to production or deleted pages | Read all mention and page URLs on hub and Start Here | PASS |
| Hub section order: Welcome, Today at a glance, Quick actions, Life overview, Explore | Fetched hub after fix | PASS (first attempt came out mis-ordered and was corrected; see CHANGELOG) |

## Visual checks (from page structure only)

| Check | Status | Notes |
|---|---|---|
| Headings consistent (brown H2 sections, gray H3 sub-sections) | PASS (structure) | |
| Intro lines coloured consistently | PASS after fix | Two intro lines lost colour in an edit and were restored |
| Em dashes in customer copy | PASS (pages fetched) | |
| Broken images | N/A | Pages use one external cover URL; image rendering not checked |
| Rendering, spacing, dark mode | NOT TESTED | Needs the Notion app |

## Mobile

| Platform | Status |
|---|---|
| iOS app | NOT TESTED |
| Android app | NOT TESTED |
| Narrow browser window | NOT TESTED |

Structural expectations to confirm on a phone: the hub's 3-column navigation stacks to one column; Today is single-column; list views (Due today and overdue, Today's habits, Active projects) were chosen over tables on the hub so they don't need horizontal scrolling. Today still uses two table views (Today & overdue, Daily check-in) that will scroll sideways on a phone; consider switching them to list views after a phone check.
