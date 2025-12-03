import csv
from datetime import datetime

def validate_row(row, line_num):
    errors = []

    def is_float(v):
        try: float(v); return True
        except: return False

    def is_int(v):
        try: int(v); return True
        except: return False

    def get(field):
        return row.get(field, "").strip()

    # title
    if not get('title'):
        errors.append("title missing or invalid")

    # magnitude
    if not is_float(get('magnitude')):
        errors.append("magnitude not a valid float")

    # date_time
    date_val = get('date_time')
    valid_dt = False
    for fmt in ["%d-%m-%Y %H:%M", "%d-%m-%Y %H:%M:%S"]:
        try:
            datetime.strptime(date_val, fmt)
            valid_dt = True; break
        except:
            pass
    if not valid_dt:
        errors.append("date_time wrong format")

    # cdi
    cdi = get('cdi')
    if cdi and not is_int(cdi):
        errors.append("cdi not an integer or empty")

    # mmi
    mmi = get('mmi')
    if mmi and not is_int(mmi):
        errors.append("mmi not an integer or empty")

    # alert
    alert = get('alert').lower()
    if alert and alert not in ['green', 'yellow', 'red']:
        errors.append("alert invalid")

    # tsunami & sig
    if not is_int(get('tsunami')):
        errors.append("tsunami not integer")

    if not is_int(get('sig')):
        errors.append("sig not integer")

    # net
    if not get('net'):
        errors.append("net empty")

    # nst
    nst = get('nst')
    if nst and not is_int(nst):
        errors.append("nst not integer or empty")

    # dmin
    dmin = get('dmin')
    if dmin and not is_float(dmin):
        errors.append("dmin not float")

    # gap
    gap = get('gap')
    if gap and not is_int(gap):
        errors.append("gap not integer")

    # magType
    if not get('magType'):
        errors.append("magType empty")

    # depth, lat, long
    for col in ['depth', 'latitude', 'longitude']:
        if not is_float(get(col)):
            errors.append(f"{col} not float")

    # location
    if not get('location'):
        errors.append("location empty")

    return errors


def validate_csv(file_path):
    errors_found = False
    
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for line_num, row in enumerate(reader, start=2):  # start at 2 (line 1 = headers)
            errors = validate_row(row, line_num)
            if errors:
                errors_found = True
                print(f"❌ Row {line_num}: {', '.join(errors)}")

    if not errors_found:
        print("✅ CSV is valid. No issues found!")

# Run validation
if __name__ == "__main__":
    validate_csv("earthquakes.csv")  # change to your path
