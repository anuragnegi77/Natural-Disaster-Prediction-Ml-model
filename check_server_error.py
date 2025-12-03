"""
Quick script to check what server error is occurring
Run this while the server is running or trying to start
"""
import sys
import traceback

print("🔍 Checking for server errors...")
print("=" * 60)

errors_found = []

# Test 1: Import check
try:
    import app
    print("✅ App module imports successfully")
except Exception as e:
    print(f"❌ Import error: {e}")
    errors_found.append(f"Import: {e}")
    traceback.print_exc()

# Test 2: Check if we can create app instance
try:
    from app import app as flask_app
    print("✅ Flask app instance accessible")
except Exception as e:
    print(f"❌ Flask app error: {e}")
    errors_found.append(f"Flask app: {e}")

# Test 3: Check models
try:
    from app import earthquake_model, flood_model, wildfire_model
    print("✅ All models accessible")
except Exception as e:
    print(f"❌ Model access error: {e}")
    errors_found.append(f"Models: {e}")

# Test 4: Check dataframes
try:
    from app import earthquakes_df, floods_df, wildfires_df
    print("✅ All dataframes accessible")
    print(f"   - Earthquakes: {len(earthquakes_df)} rows")
    print(f"   - Floods: {len(floods_df)} rows")
    print(f"   - Wildfires: {len(wildfires_df)} rows")
except Exception as e:
    print(f"❌ DataFrame access error: {e}")
    errors_found.append(f"DataFrames: {e}")

# Test 5: Try a test prediction
try:
    import pandas as pd
    from app import safe_predict_proba, earthquake_model, flood_model, wildfire_model
    from app import earthquakes_df, floods_df, wildfires_df
    
    lat, lng = 20.59, 78.96
    
    # Test earthquake
    eq_mag = float(earthquakes_df['magnitude'].mean()) if not earthquakes_df.empty else 5.0
    eq_depth = float(earthquakes_df['depth'].mean()) if not earthquakes_df.empty else 10.0
    eq_input = pd.DataFrame([[lat, lng, eq_mag, eq_depth]], 
                           columns=['latitude', 'longitude', 'magnitude', 'depth'])
    eq_result = safe_predict_proba(earthquake_model, eq_input)
    print(f"✅ Test earthquake prediction: {eq_result}%")
    
    # Test flood
    flood_rain = float(floods_df['rainfall'].mean()) if not floods_df.empty else 100.0
    flood_input = pd.DataFrame([[lat, lng, flood_rain]], 
                             columns=['latitude', 'longitude', 'rainfall'])
    flood_result = safe_predict_proba(flood_model, flood_input)
    print(f"✅ Test flood prediction: {flood_result}%")
    
    # Test wildfire
    if not wildfires_df.empty and 'Fires' in wildfires_df.columns:
        fires_series = pd.to_numeric(wildfires_df['Fires'].astype(str).str.replace(',', ''), errors='coerce')
        avg_fires = float(fires_series.mean()) if not fires_series.isna().all() else 50000.0
    else:
        avg_fires = 50000.0
    fire_input = pd.DataFrame([[avg_fires]], columns=['Fires'])
    fire_result = safe_predict_proba(wildfire_model, fire_input)
    print(f"✅ Test wildfire prediction: {fire_result}%")
    
except Exception as e:
    print(f"❌ Test prediction error: {e}")
    errors_found.append(f"Prediction: {e}")
    traceback.print_exc()

print("\n" + "=" * 60)
if errors_found:
    print("❌ ERRORS FOUND:")
    for err in errors_found:
        print(f"   - {err}")
    print("\n💡 Please share these errors for debugging")
else:
    print("✅ No errors detected in app module!")
    print("\n💡 If server still has errors, check:")
    print("   1. Terminal output when running 'python app.py'")
    print("   2. Browser console (F12) for frontend errors")
    print("   3. Network tab (F12) for API response errors")

