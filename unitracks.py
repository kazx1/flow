
"""
Interactive University Application Tracker (USD)

- Prompts for fields on launch
- Detects duplicates (same University + Program + Degree + Term)
- If duplicate: show line(s) and offer:
    [U]pdate status
    [N]ew course on same university/college
    [S]kip
- Stores rows in myuniversity.csv (or uniapplications env)
- All costs showed in USD ($)

Run: python unitracks.py
"""

import csv, os, datetime as dt

CSV_PATH = os.getenv("uniapplications", "myuniversity.csv")

FIELDS = [
    "id",
    "University", "Program", "Degree",
    "Country", "City",
    "Term", "Deadline", "Status", "Portal",
    "Application fee", "Tuition", "Living cost", "Scholarship",
    "Total year",
    "Notes", "Last update",
]

STATUS_CHOICES = [
    "Planning","In-Progress","Submitted","Interview","Offer","Accepted","Rejected","Waitlisted","Withdrawn"
]

def now_iso():
    return dt.datetime.now().strftime("%Y-%m-%d %H:%M") 

def ensure_csv():
    if not os.path.exists(CSV_PATH):
        with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=FIELDS)
            w.writeheader()

def load_rows():
    ensure_csv()
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def save_rows(rows):
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for r in rows:
            clean = {k: r.get(k, "") for k in FIELDS} 
            w.writerow(clean)


def next_id(rows): 
    mx = 0 
    for r in rows:
        try:
            mx = max(mx, int(r.get("id","0"))) 
        except:
            pass 
    return str(mx + 1)

def parse_money(x: str) -> float:
    x = (x or "").strip()
    if x == "": return 0.0
    for ch in ", €$£₤₺₹¥₩":
        x = x.replace(ch, "")
    try:
        return float(x)
    except:
        return 0.0

def usd(v: str | float) -> str:
    """Format a number as USD string like $12,345.67"""
    try:
        f = float(v)
        return f"${f:,.2f}" 
    except:
        return "$0.00"

def fmt_row_line(r: dict) -> str:
    parts = [
        f"#{r.get('id','')}",
        r.get("University",""),
        r.get("Program",""),
        r.get("Degree",""),
        r.get("Term",""),
        r.get("City",""),
        r.get("Country",""),
        f"deadline={r.get('Deadline','')}",
        f"status={r.get('Status','')}",
        f"total/yr={usd(r.get('Total year','0'))}",
    ]
    return " | ".join(p for p in parts if p) 

def input_def(prompt, default=""): 
    msg = f"{prompt} [{default}]: " if default else f"{prompt}: "
    val = input(msg).strip() 
    return val if val else default 

def find_by_university(rows, uni):
    u = (uni or "").strip().lower() 
    return [r for r in rows if r.get("University","").strip().lower() == u]

def is_exact_duplicate(rows, uni, program, degree, term):  
    u = (uni or "").strip().lower()
    p = (program or "").strip().lower()
    d = (degree or "").strip().lower()
    t = (term or "").strip().lower()
    hits = []
    for r in rows:
        if (r.get("University","").strip().lower()==u and
            r.get("Program","").strip().lower()==p and
            r.get("Degree","").strip().lower()==d and
            r.get("Term","").strip().lower()==t):
            hits.append(r)
    return hits

def compute_estimate(tuition, living, scholarship):
    return max(0.0, tuition + living - scholarship)

def add_new_row(rows, base_defaults=None):
    """Create a new row"""
    r = {k:"" for k in FIELDS}
    r["id"] = next_id(rows)
    base_defaults = base_defaults or {}

    print("\n➡️  Add a new application")
    r["University"] = input_def("University", base_defaults.get("University",""))
    r["Program"]    = input_def("Program", "")
    r["Degree"]     = input_def("Degree", "")
    r["Country"]    = input_def("Country", base_defaults.get("Country",""))
    r["City"]       = input_def("City", base_defaults.get("City",""))
    r["Term"]       = input_def("Term", "")
    r["Deadline"]   = input_def("Application deadline (YYYY-MM-DD)", "")

    print("Status options:", ", ".join(STATUS_CHOICES))
    r["Status"]     = input_def("Status", "Planning")
    r["Portal"]     = input_def("Application portal URL (optional)", "")

    application_fee = parse_money(input_def("Application fee", "0"))
    tuition_year    = parse_money(input_def("Tuition per year", base_defaults.get("Tuition","0")))
    living_year     = parse_money(input_def("Living cost per year", base_defaults.get("Living cost","0")))
    scholarship     = parse_money(input_def("Expected scholarship per year", "0"))
    est_total       = compute_estimate(tuition_year, living_year, scholarship)

    r["Application fee"] = f"{application_fee:.2f}"
    r["Tuition"]         = f"{tuition_year:.2f}"
    r["Living cost"]     = f"{living_year:.2f}"
    r["Scholarship"]     = f"{scholarship:.2f}"
    r["Total year"]      = f"{est_total:.2f}"
    r["Notes"]           = input_def("Notes (optional)", "")
    r["Last update"]     = now_iso()

    rows.append(r)
    save_rows(rows)
    print(f"✅ Added: {fmt_row_line(r)}")
    return r

def update_status_flow(rows, candidates):
    """Pick a candidate ID & update his status"""
    print("\n📝 Matching records:")
    for r in candidates:
        print("   ", fmt_row_line(r))

    target_id = input_def("Enter the ID to update", candidates[0]["id"])
    target = None
    for r in rows:
        if r.get("id")==target_id:
            target = r; break
    if not target:
        print("❌ ID not found. Abort.")
        return

    print("Status options:", ", ".join(STATUS_CHOICES))
    new_status   = input_def(f"New status (current: {target.get('Status','')})", target.get("Status",""))
    new_deadline = input_def(f"New deadline YYYY-MM-DD (current: {target.get('Deadline','')})", target.get("Deadline",""))
    add_note     = input_def("Append note (optional)", "")

    if new_status:   target["Status"] = new_status
    if new_deadline: target["Deadline"] = new_deadline
    if add_note:
        target["Notes"] = (target.get("Notes","") + (" | " if target.get("Notes") else "") + add_note)

    target["Last update"] = now_iso() 
    save_rows(rows) #save to file
    print("✅ Updated:", fmt_row_line(target))

def main():
    rows = load_rows()

    print("🎓 University Track Application")
    print("Press Ctrl+C or leave 'University' empty to quit.")

    while True:
        try:
            uni = input_def("\nUniversity", "")
            if not uni:
                print("\nBye!"); break

            program = input_def("Program", "")
            degree  = input_def("Degree", "")
            term    = input_def("Term", "")

            dups = is_exact_duplicate(rows, uni, program, degree, term)
            same_uni = find_by_university(rows, uni)

            if dups:
                print("\n⚠️  Possible duplicate found:")
                for r in dups:
                    print("   ", fmt_row_line(r))
                choice = input_def("Choose: [U]pdate status / [N]ew course / [S]kip", "U").strip().lower()
                if choice.startswith("u"):
                    update_status_flow(rows, dups)
                elif choice.startswith("n"):
                    base = {}
                    if same_uni:
                        base = {
                            "University": same_uni[0].get("University",""),
                            "Country":    same_uni[0].get("Country",""),
                            "City":       same_uni[0].get("City",""),
                            "Tuition":    same_uni[0].get("Tuition","0"),
                            "Living cost":same_uni[0].get("Living cost","0"),
                        }
                    add_new_row(rows, base_defaults=base)
                else:
                    print("↩ Skipped.")
                continue

            base = {}
            if same_uni:
                print("\nℹ️  Existing records for this university:")
                for r in same_uni[:5]:
                    print("   ", fmt_row_line(r))
                use_defaults = input_def("Reuse location/cost defaults from this university? (y/n)", "y").lower()
                if use_defaults.startswith("y"):
                    base = {
                        "University": uni,
                        "Country":    same_uni[0].get("Country",""),
                        "City":       same_uni[0].get("City",""),
                        "Tuition":    same_uni[0].get("Tuition","0"),
                        "Living cost":same_uni[0].get("Living cost","0"),
                    }
                else:
                    base = {"University": uni}

            added = add_new_row(rows, base_defaults=base)

            if program and not added.get("Program"): added["Program"] = program
            if degree  and not added.get("Degree"):  added["Degree"]  = degree
            if term    and not added.get("Term"):    added["Term"]    = term
            added["Last update"] = now_iso()
            save_rows(rows)

            again = input_def("Add another application? (y/n)", "y").lower()
            if not again.startswith("y"):
                print("\nDone. All saved to:", os.path.abspath(CSV_PATH))
                break

        except KeyboardInterrupt:
            print("\n\nInterrupted. Goodbye!")
            break

if __name__ == "__main__":
    main()
