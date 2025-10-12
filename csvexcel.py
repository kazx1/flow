#!/usr/bin/env python3

import pandas as pd
from pathlib import Path

print("📁 File Converter - CSV ↔ Excel")
print("1️⃣  CSV → Excel (.xlsx)")
print("2️⃣  Excel → CSV (.csv)")

choice = input("Choose 1 or 2: ").strip()

if choice == "1":
    csv_path = Path(input("Enter the path of the CSV file: ").strip('" '))
    if not csv_path.exists():
        print("❌ File not found:", csv_path)
    else:
        out_path = csv_path.with_suffix(".xlsx")
        pd.read_csv(csv_path).to_excel(out_path, index=False)
        print(f"✅ Converted to Excel: {out_path}")

elif choice == "2":
    xlsx_path = Path(input("Enter the path of the Excel file: ").strip('" '))
    if not xlsx_path.exists():
        print("❌ File not found:", xlsx_path)
    else:
        out_path = xlsx_path.with_suffix(".csv")
        pd.read_excel(xlsx_path).to_csv(out_path, index=False)
        print(f"✅ Converted to CSV: {out_path}")

else:
    print("⚠️ Invalid choice. Please enter 1 or 2.")
