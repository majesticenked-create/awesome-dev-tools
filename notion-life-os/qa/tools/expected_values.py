"""Independent expected values for the Notion Life Hub sample data.

Computed from the raw sample inputs only (never from Notion formula output).
Reference date is passed on the command line so the baseline can be re-run.
Usage: python3 expected_values.py 2026-10-14
"""
import sys
from datetime import date, timedelta
from calendar import isleap

TODAY = date.fromisoformat(sys.argv[1] if len(sys.argv) > 1 else "2026-10-14")
d = date.fromisoformat


def days(a, b):
    return (a - b).days


def months_between(later, earlier):
    # Notion dateBetween(..., "months") counts whole calendar months, truncated.
    m = (later.year - earlier.year) * 12 + (later.month - earlier.month)
    if later.day < earlier.day:
        m -= 1
    return m


def bar(p, n=10):
    k = round(p * n)
    return "▰" * k + "▱" * (n - k)


print(f"# Expected values for {TODAY}\n")

print("## Tasks.Status Label")
tasks = [
    ("Easy 4K run", True, "2026-10-12"), ("Tempo run 20 min", False, "2026-10-14"),
    ("Long run 7K", False, "2026-10-18"), ("Buy new running shoes", True, "2026-10-05"),
    ("Set up payday auto-transfer", True, "2026-10-03"),
    ("Cancel unused streaming trial", False, "2026-10-13"),
    ("Declutter wardrobe", False, "2026-10-17"), ("Pick paint swatches", False, "2026-10-20"),
    ("Finish current book", False, "2026-10-16"), ("Call Grandma", False, "2026-10-14"),
    ("Book dentist appointment", False, None), ("Renew passport", False, "2026-10-15"),
]
for name, done, do in tasks:
    if done:
        lab = "✓ Done"
    elif do is None:
        lab = "Inbox"
    else:
        dd = days(d(do), TODAY)
        lab = "⚠ Overdue" if dd < 0 else "Today" if dd == 0 else "Upcoming"
    print(f"- {name}: {lab}")

print("\n## Goals / Projects progress (share of linked tasks done)")
for name, total, done in [("Run a 10K", 4, 2), ("Emergency fund", 2, 1), ("Read 24 books", 1, 0),
                          ("Redecorate bedroom", 2, 0), ("Pottery (no tasks)", 0, 0),
                          ("P: 10K training plan", 4, 2), ("P: Bedroom refresh", 2, 0),
                          ("P: Automate savings", 2, 1)]:
    p = done / total if total else 0
    print(f"- {name}: {p:.4f} -> {bar(p)}  {round(p*100)}%")

print("\n## Daily Log.Habits Done")
logs = {"2026-10-08": (1,1,0,1,0), "2026-10-09": (1,0,1,0,0), "2026-10-10": (1,1,1,1,1),
        "2026-10-11": (1,1,1,0,1), "2026-10-12": (1,1,0,1,0), "2026-10-13": (0,0,1,0,0),
        "2026-10-14": (1,0,0,1,1)}
for k, v in logs.items():
    print(f"- {k}: {sum(v)} -> {'◆'*sum(v)}{'◇'*(5-sum(v))}")

print("\n## Home Care.Next due / Due")
for name, every, last in [("Change bedsheets",7,"2026-10-09"),("Clean bathroom",7,"2026-10-04"),
                          ("Wipe out fridge",30,"2026-09-20"),("Vacuum + mop",7,"2026-10-11"),
                          ("Water plants",4,"2026-10-12"),("Smoke alarm batteries",365,"2026-01-15"),
                          ("Descale kettle",60,"2026-08-30"),("Tyre pressure",30,"2026-09-25")]:
    nd = d(last) + timedelta(days=every)
    dd = days(nd, TODAY)
    lab = f"⚠ {abs(dd)}d overdue" if dd < 0 else "Due today" if dd == 0 else f"In {dd}d"
    print(f"- {name}: next {nd} -> {lab}")

print("\n## Contacts birthdays")
def next_bday(b):
    try:
        nb = b.replace(year=TODAY.year)
    except ValueError:  # Feb 29 in a non-leap year
        nb = date(TODAY.year, 2, 28)
    if nb < TODAY:
        try:
            nb = b.replace(year=TODAY.year + 1)
        except ValueError:
            nb = date(TODAY.year + 1, 2, 28)
    return nb
for name, b in [("Grandma Rose","1946-10-22"),("Maya","1994-03-14"),("Sam Carter","1992-11-02"),
                ("Priya Shah","1990-06-30")]:
    nb = next_bday(d(b)); dd = days(nb, TODAY)
    print(f"- {name}: next {nb}, in {dd} days, soon(<=14)={dd <= 14}")

print("\n## Documents.Expiry")
for name, e in [("Passport","2026-12-01"),("Car insurance","2027-04-12"),
                ("Home insurance","2027-07-01"),("Laptop warranty","2027-05-20")]:
    dd = days(d(e), TODAY)
    print(f"- {name}: {dd} days -> {'⚠ Expired' if dd < 0 else 'Renew soon' if dd < 60 else 'OK'}")

print("\n## Subscriptions (average monthly = weekly*52/12, quarterly/3, yearly/12)")
for name, cost, cyc, nxt in [("Streaming",12.99,"Monthly","2026-10-19"),("Music",10.99,"Monthly","2026-10-28"),
                             ("Cloud storage",29.99,"Yearly","2027-02-03"),("Gym",35,"Monthly","2026-10-16"),
                             ("Weekend newspaper",5,"Weekly","2026-10-17")]:
    m = {"Weekly": cost*52/12, "Monthly": cost, "Quarterly": cost/3, "Yearly": cost/12}[cyc]
    print(f"- {name}: monthly {m:.4f}, yearly {m*12:.2f}, renews in {days(d(nxt), TODAY)} days")

print("\n## Budget (expenses dated in the current calendar month only)")
tx = [("Salary",3200,"Income","2026-10-01"),("Rent",1200,"Expense","2026-10-01"),
      ("Savings",300,"Expense","2026-10-01"),("Groceries",86.40,"Expense","2026-10-03"),
      ("Groceries",92.15,"Expense","2026-10-10"),("Groceries",24.00,"Expense","2026-10-11"),
      ("Transport",95.00,"Expense","2026-10-02"),("Transport",18.50,"Expense","2026-10-09"),
      ("Eating out",42.00,"Expense","2026-10-04"),("Eating out",31.80,"Expense","2026-10-09"),
      ("Fun & hobbies",65.00,"Expense","2026-10-06"),("Fun & hobbies",28.00,"Expense","2026-10-12")]
budgets = {"Rent":1200,"Groceries":400,"Transport":150,"Eating out":150,"Fun & hobbies":100,"Savings":300,"Salary":None}
for cat, b in budgets.items():
    spent = round(sum(a for c,a,t,dt in tx if c==cat and t=="Expense" and d(dt).year==TODAY.year and d(dt).month==TODAY.month), 2)
    if b:
        print(f"- {cat}: budget {b}, spent {spent:.2f}, remaining {b-spent:.2f}, used {round(spent/b*100)}% {bar(min(spent/b,1))}")
    else:
        print(f"- {cat}: no budget, spent {spent:.2f}")
tot_exp = sum(a for c,a,t,dt in tx if t=="Expense")
print(f"- Total outflow incl. savings transfer: {tot_exp:.2f}; consumption spending excl. savings: {tot_exp-300:.2f}; income: 3200.00")

print("\n## Money Goals")
for name, tgt, cur, td in [("Emergency fund",6000,2150,"2027-03-31"),("Credit card payoff",1800,900,"2027-01-31"),
                           ("Japan trip fund",3500,600,"2027-09-01")]:
    p = min(cur/tgt, 1); m = months_between(d(td), TODAY)
    pm = (tgt-cur) if m <= 0 else round((tgt-cur)/m)
    print(f"- {name}: progress {p:.4f} {bar(p)} {round(p*100)}%, months left {m}, per month {pm}")

print("\n## Life Areas.Balance")
for name, s in [("Health",6),("Mind",7),("Relationships",8),("Career",6),("Money",5),("Home",6),("Fun & Creativity",4),("Growth",7)]:
    print(f"- {name}: {'●'*s}{'○'*(10-s)}")
