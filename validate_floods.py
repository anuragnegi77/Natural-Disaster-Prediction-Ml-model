import csv
import os

def validate_floods_csv(filepath):
    expected_columns = [
        "MonsoonIntensity", "TopographyDrainage", "RiverManagement", "Deforestation", "Urbanization",
        "ClimateChange", "DamsQuality", "Siltation", "AgriculturalPractices", "Encroachments",
        "IneffectiveDisasterPreparedness", "DrainageSystems", "CoastalVulnerability", "Landslides",
        "Watersheds", "DeterioratingInfrastructure", "PopulationScore", "WetlandLoss",
        "InadequatePlanning", "PoliticalFactors", "FloodProbability"
    ]

    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        return False

    warnings = []

    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        if not reader.fieldnames:
            print("❌ File is empty or missing header row.")
            return False
        
        # Clean header spaces
        headers = [h.strip() for h in reader.fieldnames]

        missing = [c for c in expected_columns if c not in headers]
        if missing:
            print(f"❌ Missing columns: {missing}")
            print(f"📌 Found columns: {headers}")
            return False

        for row_num, row in enumerate(reader, start=2):
            for col in expected_columns[:-1]:  # integer columns
                cell = row.get(col, "")
                cell = cell.strip() if isinstance(cell, str) else ""

                try:
                    val = int(cell)
                    if not (0 <= val <= 10):
                        warnings.append(f"Row {row_num}: '{col}' = {val} out of range (0–10)")
                except ValueError:
                    warnings.append(f"Row {row_num}: '{col}' invalid integer: '{cell}'")

            # FloodProbability
            prob = row.get("FloodProbability", "")
            prob = prob.strip() if isinstance(prob, str) else ""

            try:
                p = float(prob)
                if not (0.0 <= p <= 1.0):
                    warnings.append(f"Row {row_num}: FloodProbability {p} out of range (0–1)")
            except ValueError:
                warnings.append(f"Row {row_num}: FloodProbability invalid float: '{prob}'")

    if warnings:
        print("⚠️ Validation Warnings:")
        for w in warnings:
            print(" -", w)
    else:
        print("✅ No issues. Flood CSV is valid!")

    print("✅ Flood CSV validation complete.")
    return True
