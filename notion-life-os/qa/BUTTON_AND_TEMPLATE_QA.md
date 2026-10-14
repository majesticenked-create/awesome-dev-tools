# Button and Template QA

## Buttons

| Button | Exists | Tested | Status |
|---|---|---|---|
| Add task | No | No | BLOCKED: the Notion connector cannot create or click buttons |
| New journal entry | No | No | BLOCKED |
| Open today's log | No | No | BLOCKED |
| Log expense | No | No | BLOCKED |

Specs (target database, default values, after-click action, repeat-click behavior) are in the seller checklist, section 1. Notion buttons cannot prevent duplicates on repeat clicks; each click creates a new page. That limit is stated in the specs and the Start Here guide.

Interim, verified by page fetch: the Hub "Quick actions" callout links to Tasks, Today, Transactions and Daily Log, and its wording does not imply a one-click action.

## Database templates

| Database | Template(s) | Exists | Status |
|---|---|---|---|
| Daily Log | Default | No | BLOCKED (UI only); text ready |
| Reviews | Weekly, Monthly, Quarterly | No | BLOCKED; text ready |
| Journal | Evening reflection, Morning pages | No | BLOCKED; text ready |
| Trips | Trip | No | BLOCKED; text ready |
| Recipes | Recipe | No | BLOCKED; text ready |
| Projects | Project | No | BLOCKED; text ready |
| Goals | Task goal, Number goal | No | BLOCKED; text ready |

Text: `TEMPLATES_TO_CREATE.md`.

## Test plan once created (run in dev, twice per button)

1. Click the button. Check the new page's database, Date (today), Type/Status defaults, and that no relation is set by accident.
2. Click again. Expect a second page (Notion limitation). Delete both.
3. For each template: New → template. Check properties and body; check Date fills with the creation date, not the date the template was made.
