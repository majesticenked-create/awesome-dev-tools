"""Phase 9B: independent expected values for the dev copy, built from live inputs.

Inputs below were read from the dev databases on 2026-10-14 with quota-free
view-mode queries (raw properties only, never formula output). This script
computes every expected formula value with its own logic, then prints one
view filter (Notion view DSL) per database. Each filter is an OR of one group
per row: (title = row AND formula = expected ...). If the view returns every
row, every live value equals the expected value. A missing row is a mismatch.

Usage: python3 -I verify_dev_formulas.py 2026-10-14 [--text-only]

--text-only drops every "zz QA probe" condition, so the filters check only
the visible text formulas (status labels, bars, Budget status, Due, Expiry and
so on). Use it to verify a customer edition without adding probe columns.
"""
import sys
from datetime import date, timedelta

ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
TEXT_ONLY = "--text-only" in sys.argv
TODAY = date.fromisoformat(ARGS[0] if ARGS else "2026-10-14")
d = date.fromisoformat


def fmt(x):
    """Notion format() of a number: integers without decimals, others as-is."""
    x = round(x, 4)
    return str(int(x)) if x == int(x) else repr(x)


def r2(x):
    return fmt(round(x * 100 + 1e-9) / 100)


def r4(x):
    return fmt(round(x * 10000 + 1e-9) / 10000)


def bar(p):
    k = round(min(p, 1) * 10 + 1e-9)
    return "▰" * k + "▱" * (10 - k)


def months_between(later, earlier):
    m = (later.year - earlier.year) * 12 + (later.month - earlier.month)
    if later.day < earlier.day:
        m -= 1
    return m


def q(s):
    return '"' + s.replace('"', '\\"') + '"'


def dsl(title_prop, rows):
    groups = []
    for title, conds in rows:
        parts = [f"{q(title_prop)} = {q(title)}"]
        for prop, op, val in conds:
            if TEXT_ONLY and prop == "zz QA probe":
                continue
            parts.append(f"{q(prop)} IS EMPTY" if op == "empty" else f"{q(prop)} {op} {q(val)}")
        groups.append("(" + " AND ".join(parts) + ")")
    return "FILTER " + " OR ".join(groups)


out = {}

# Tasks: (name, done, canceled, do date)
tasks = [("Tempo run, 20 min", 0, 0, "2026-10-14"), ("Easy 4K run", 1, 0, "2026-10-12"),
         ("Finish current book", 0, 0, "2026-10-16"), ("Renew passport", 0, 0, "2026-10-15"),
         ("Cancel unused streaming trial", 0, 0, "2026-10-13"), ("Set up payday auto-transfer", 1, 0, "2026-10-03"),
         ("Long run, 7K", 0, 0, "2026-10-18"), ("Pick paint swatches", 0, 0, "2026-10-20"),
         ("Buy new running shoes", 1, 0, "2026-10-05"), ("Book dentist appointment", 0, 0, None),
         ("Declutter wardrobe", 0, 0, "2026-10-17"), ("Call Grandma", 0, 0, "2026-10-14")]
rows = []
for n, done, canc, do in tasks:
    if canc:
        lab = "Canceled"
    elif done:
        lab = "✓ Done"
    elif do is None:
        lab = "Inbox"
    else:
        dd = (d(do) - TODAY).days
        lab = "⚠ Overdue" if dd < 0 else "Today" if dd == 0 else "Upcoming"
    rows.append((n, [("Status Label", "=", lab)]))
out["Tasks"] = ("Name", rows)

# Projects: (name, linked task names)
done_set = {n for n, done, c, _ in tasks if done}
canc_set = {n for n, done, c, _ in tasks if c}
projects = {"Automate savings": ["Set up payday auto-transfer", "Cancel unused streaming trial"],
            "10K training plan": ["Easy 4K run", "Tempo run, 20 min", "Long run, 7K", "Buy new running shoes"],
            "Bedroom refresh": ["Declutter wardrobe", "Pick paint swatches"]}
proj_progress = {}
rows = []
for n, ts in projects.items():
    tot, dn, cn = len(ts), sum(t in done_set for t in ts), sum(t in canc_set for t in ts)
    open_ = tot - cn
    p = 0 if open_ <= 0 else min(dn / open_, 1)
    proj_progress[n] = p
    pb = "No tasks linked yet" if open_ <= 0 else f"{bar(p)}  {round(min(p, 1) * 100)}%"
    rows.append((n, [("zz QA probe", "=", f"{tot}|{dn}|{cn}|{r4(p)}"), ("Progress Bar", "=", pb)]))
out["Projects"] = ("Name", rows)

# Goals: (name, measure, tasks, projects, start, target, current, target date, status)
goals = [("Read 24 books this year", "Number", ["Finish current book"], [], 0, 24, 14, "2026-12-31", "In progress"),
         ("Redecorate the bedroom", "Tasks", ["Declutter wardrobe", "Pick paint swatches"], ["Bedroom refresh"], None, None, None, "2026-12-20", "Not started"),
         ("Run a 10K", "Tasks", ["Easy 4K run", "Tempo run, 20 min", "Long run, 7K", "Buy new running shoes"], ["10K training plan"], None, None, None, "2026-12-06", "In progress"),
         ("Build a 3-month emergency fund", "Tasks", ["Set up payday auto-transfer", "Cancel unused streaming trial"], ["Automate savings"], None, None, None, "2027-03-31", "In progress"),
         ("Start a pottery practice", "Tasks", [], [], None, None, None, None, "Not started")]
rows = []
for n, meas, ts, ps, s, t, c, td, st in goals:
    tot, dn, cn = len(ts), sum(x in done_set for x in ts), sum(x in canc_set for x in ts)
    pc = len(ps)
    pp = sum(proj_progress[x] for x in ps) / pc if pc else None
    s0 = s or 0
    if meas == "Number":
        cur = s0 if c is None else c
        ready = t is not None and t != s0
        p = max(0, (cur - s0) / (t - s0)) if ready else 0
    else:
        open_ = tot - cn
        ready = open_ > 0 or pc > 0
        p = min(dn / open_, 1) if open_ > 0 else (pp if pc > 0 else 0)
    pb = f"{bar(p)}  {round(p * 100)}%" if ready else ("Set start and target values" if meas == "Number" else "No tasks linked yet")
    dd = (d(td) - TODAY).days if td else None
    if st == "Achieved" or (ready and p >= 1):
        h = "✓ Completed"
    elif not ready:
        h = "Not enough information"
    elif dd is not None and dd < 0:
        h = "⚠ Needs attention: past target date"
    elif dd is not None and dd <= 14 and p < 0.75:
        h = "⚠ Needs attention: due soon"
    else:
        h = "On track"
    head = f"{tot}|{dn}|{cn}|{pc}|"
    conds = [("Progress Bar", "=", pb), ("Goal health", "=", h)]
    if pp is None:  # average of no projects: empty or 0 accepted, checked by prefix and suffix
        conds += [("zz QA probe", "STARTS WITH", head), ("zz QA probe", "ENDS WITH", f"|{r4(p)}")]
    else:
        conds += [("zz QA probe", "=", f"{head}{r4(pp)}|{r4(p)}")]
    rows.append((n, conds))
out["Goals"] = ("Name", rows)

# Transactions: (description, amount, type, date); one probe per row
tx = [("Weekly shop", 86.4, "Expense", "2026-10-03"), ("Friday takeaway", 31.8, "Expense", "2026-10-09"),
      ("Savings auto-transfer", 300, "Savings", "2026-10-01"), ("Taxi home", 18.5, "Expense", "2026-10-09"),
      ("Farmers market", 24, "Expense", "2026-10-11"), ("Paint set", 28, "Expense", "2026-10-12"),
      ("Concert tickets", 65, "Expense", "2026-10-06"), ("October salary", 3200, "Income", "2026-10-01"),
      ("Weekly shop", 92.15, "Expense", "2026-10-10"), ("Brunch with Maya", 42, "Expense", "2026-10-04"),
      ("Rent", 1200, "Expense", "2026-10-01"), ("Monthly transit pass", 95, "Expense", "2026-10-02")]


def tx_vals(a, ty, dt):
    this_month = d(dt).year == TODAY.year and d(dt).month == TODAY.month
    spent = (a if ty == "Expense" else -a if ty == "Refund" else 0) if this_month else 0
    saved = a if this_month and ty in ("Savings", "Debt payment") else 0
    return spent, saved


rows = []
seen = set()
for desc, a, ty, dt in tx:
    sp, sv = tx_vals(a, ty, dt)
    probe = f"{r2(sp)}|{r2(sv)}"
    if (desc, probe) in seen:
        continue
    seen.add((desc, probe))
    rows.append((desc, [("zz QA probe", "=", probe)]))
out["Transactions"] = ("Description", rows)

# Budget categories: category -> (budget, transaction indexes)
cat_tx = {"Groceries": [0, 4, 8], "Eating out": [1, 9], "Savings": [2], "Transport": [3, 11],
          "Fun & hobbies": [5, 6], "Salary": [7], "Rent": [10]}
budgets = {"Savings": 300, "Groceries": 400, "Eating out": 150, "Rent": 1200, "Salary": None,
           "Fun & hobbies": 100, "Transport": 150}
rows = []
for cat, b in budgets.items():
    sp = sum(tx_vals(tx[i][1], tx[i][2], tx[i][3])[0] for i in cat_tx[cat])
    sv = sum(tx_vals(tx[i][1], tx[i][2], tx[i][3])[1] for i in cat_tx[cat])
    act = sp + sv
    if not b:
        status, used = "No budget set", None
        conds = [("zz QA probe", "STARTS WITH", f"{r2(sp)}|{r2(sv)}|{r2(act)}|")]
    else:
        rem = b - act
        status = (f"⚠ Over by {r2(act - b)}" if act > b + 1e-9 else "✓ Fully used" if abs(act - b) < 1e-9
                  else f"On track: {r2(rem)} left")
        used = f"{bar(act / b)}  {round(act / b * 100)}%"
        conds = [("zz QA probe", "=", f"{r2(sp)}|{r2(sv)}|{r2(act)}|{r2(rem)}")]
    conds.append(("Budget status", "=", status))
    conds.append(("Used", "empty", None) if used is None else ("Used", "=", used))
    rows.append((cat, conds))
out["Budget Categories"] = ("Category", rows)

# Subscriptions: (name, cost, cycle, next renewal, status)
subs = [("Weekend newspaper", 5, "Weekly", "2026-10-17", "Cancel soon"), ("Cloud storage", 29.99, "Yearly", "2027-02-03", "Active"),
        ("Music app", 10.99, "Monthly", "2026-10-28", "Active"), ("Streaming service", 12.99, "Monthly", "2026-10-19", "Active"),
        ("Gym membership", 35, "Monthly", "2026-10-16", "Trial")]


def add_months(x, k):
    m = x.month - 1 + k
    y, m = x.year + m // 12, m % 12 + 1
    import calendar
    return date(y, m, min(x.day, calendar.monthrange(y, m)[1]))


def next_charge(n, cyc):
    n = d(n)
    if n >= TODAY:
        return n
    step = {"Weekly": 7}.get(cyc)
    c = n
    while c < TODAY:
        if step:
            c += timedelta(days=step)
        elif cyc == "Yearly":
            c = add_months(c, 12)
        else:
            c = add_months(c, 3 if cyc == "Quarterly" else 1)
    return c


rows = []
for n, cost, cyc, nr, st in subs:
    m = 0 if st in ("Paused", "Cancelled") else {"Weekly": cost * 52 / 12, "Monthly": cost, "Quarterly": cost / 3, "Yearly": cost / 12}[cyc]
    nc = next_charge(nr, cyc)
    days = (nc - TODAY).days
    due = "Yes" if st not in ("Paused", "Cancelled") and days <= 7 else ""
    conds = [("zz QA probe", "=", f"{r2(m)}|{r2(m * 12)}|{nc}|{days}")]
    conds.append(("Due this week", "=", due) if due else ("Due this week", "empty", None))
    rows.append((n, conds))
out["Subscriptions"] = ("Name", rows)

# Money goals: (name, target, current, target date)
mg = [("Emergency fund", 6000, 2150, "2027-03-31"), ("Japan trip fund", 3500, 600, "2027-09-01"),
      ("Credit card payoff", 1800, 900, "2027-01-31")]
rows = []
for n, t, c, td in mg:
    p = min(c / t, 1)
    m = months_between(d(td), TODAY)
    pm = max(0, (t - c) if m <= 0 else round((t - c) / m))
    rows.append((n, [("zz QA probe", "=", f"{r4(p)}|{fmt(max(0, t - c))}|{fmt(pm)}"),
                     ("Progress Bar", "=", f"{bar(p)}  {round(p * 100)}%"),
                     ("Goal status", "=", "✓ Reached" if c >= t else "In progress")]))
out["Money Goals"] = ("Name", rows)

# Contacts: (name, birthday)
contacts = [("Priya Shah", "1990-06-30"), ("Grandma Rose", "1946-10-22"), ("Maya (sister)", "1994-03-14"),
            ("Dr. Lee (dentist)", None), ("Sam Carter", "1992-11-02")]


def next_bday(b):
    def on(y):
        try:
            return b.replace(year=y)
        except ValueError:
            return date(y, 2, 28)
    nb = on(TODAY.year)
    return nb if nb >= TODAY else on(TODAY.year + 1)


rows = []
for n, b in contacts:
    if b is None:
        rows.append((n, [("Birthday soon", "empty", None)]))
        continue
    nb = next_bday(d(b))
    dd = (nb - TODAY).days
    conds = [("zz QA probe", "=", f"{nb}|{dd}")]
    conds.append(("Birthday soon", "=", "Soon") if dd <= 14 else ("Birthday soon", "empty", None))
    rows.append((n, conds))
out["Contacts"] = ("Name", rows)

# Home care: (task, every, last done)
hc = [("Water plants", 4, "2026-10-12"), ("Check tyre pressure", 30, "2026-09-25"), ("Clean bathroom", 7, "2026-10-04"),
      ("Descale kettle", 60, "2026-08-30"), ("Change bedsheets", 7, "2026-10-09"), ("Wipe out fridge", 30, "2026-09-20"),
      ("Replace smoke alarm batteries", 365, "2026-01-15"), ("Vacuum + mop floors", 7, "2026-10-11")]
rows = []
for n, every, last in hc:
    nd = d(last) + timedelta(days=every)
    dd = (nd - TODAY).days
    lab = f"⚠ {abs(dd)}d overdue" if dd < 0 else "Due today" if dd == 0 else f"In {dd}d"
    rows.append((n, [("zz QA probe", "=", str(nd)), ("Due", "=", lab)]))
out["Home Care"] = ("Task", rows)

# Documents: (name, expires)
docs = [("Home contents insurance", "2027-07-01"), ("Laptop warranty", "2027-05-20"), ("Passport", "2026-12-01"),
        ("Car insurance", "2027-04-12")]
rows = []
for n, e in docs:
    dd = (d(e) - TODAY).days
    rows.append((n, [("Expiry", "=", "⚠ Expired" if dd < 0 else "Renew soon" if dd < 60 else "OK")]))
out["Documents"] = ("Name", rows)

# Life areas: (name, satisfaction)
la = [("Mind", 7), ("Relationships", 8), ("Fun & Creativity", 4), ("Health", 6), ("Money", 5), ("Home", 6),
      ("Growth", 7), ("Career", 6)]
out["Life Areas"] = ("Name", [(n, [("Balance", "=", "●" * s + "○" * (10 - s))]) for n, s in la])

# Daily log: (day, water, move, read, meditate, no-phone)
dl = [("Fri 9 Oct", 1, 0, 1, 0, 0), ("Sun 11 Oct", 1, 1, 1, 0, 1), ("Thu 8 Oct", 1, 1, 0, 1, 0),
      ("Tue 13 Oct", 0, 0, 1, 0, 0), ("Wed 14 Oct", 1, 0, 0, 1, 1), ("Mon 12 Oct", 1, 1, 0, 1, 0),
      ("Sat 10 Oct", 1, 1, 1, 1, 1)]
out["Daily Log"] = ("Day", [(n, [("zz QA probe", "=", str(sum(v))), ("Habit Bar", "=", "◆" * sum(v) + "◇" * (5 - sum(v)))])
                            for n, *v in dl])

for db, (tp, rows) in out.items():
    print(f"## {db} ({len(rows)} rows expected)")
    for title, conds in rows:
        print(f"- {title}: " + "; ".join(f"{p} {op} {v!r}" if op != 'empty' else f"{p} is empty" for p, op, v in conds))
    print("DSL: " + dsl(tp, rows))
    print()
