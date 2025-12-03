import csv
import os

columns = ["Year", "Fires", "Acres", "ForestService", "DOIAgencies", "Total"]

def clean_number(value):
    if value is None:
        return ""
    return value.replace(",", "").replace("$", "").strip()

def is_valid_int(value):
    try:
        int(value)
        return True
    except (ValueError, TypeError):
        return False

def is_valid_float(value):
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False

def validate_row(row, line_num):
    errors = []

    # Year
    year = clean_number(row.get("Year", ""))
    if not is_valid_int(year):
        errors.append(f"Invalid Year: {row.get('Year')}")

    # Fires
    fires = clean_number(row.get("Fires", ""))
    if not is_valid_int(fires):
        errors.append(f"Invalid Fires count: {row.get('Fires')}")

    # Acres
    acres = clean_number(row.get("Acres", ""))
    if not is_valid_int(acres):
        errors.append(f"Invalid Acres count: {row.get('Acres')}")

    # ForestService
    fs = clean_number(row.get("ForestService", ""))
    if not is_valid_float(fs):
        errors.append(f"Invalid ForestService amount: {row.get('ForestService')}")

    # DOIAgencies
    doi = clean_number(row.get("DOIAgencies", ""))
    if not is_valid_float(doi):
        errors.append(f"Invalid DOIAgencies amount: {row.get('DOIAgencies')}")

    # Total
    total = clean_number(row.get("Total", ""))
    if not is_valid_float(total):
        errors.append(f"Invalid Total amount: {row.get('Total')}")

    return errors

def validate_wildfire_csv(filepath):
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        return

    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        if not reader.fieldnames:
            print("❌ CSV has no header row.")
            return

        # Clean header spaces
        header = [h.strip() for h in reader.fieldnames]

        missing_cols = [col for col in columns if col not in header]
        if missing_cols:
            print(f"❌ Missing columns: {missing_cols}")
            print(f"📌 Found columns: {header}")
            return

        all_errors = []
        for line_num, row in enumerate(reader, start=2):
            errors = validate_row(row, line_num)
            if errors:
                all_errors.append(f"Line {line_num}: {', '.join(errors)}")

        if all_errors:
            print("⚠️ Wildfire Dataset Validation Errors:")
            for err in all_errors:
                print(" -", err)
        else:
            print("✅ No errors found in Wildfire dataset!")

        print("✅ Wildfire CSV validation complete.")

if __name__ == "__main__":
    validate_wildfire_csv("wildfires.csv")
