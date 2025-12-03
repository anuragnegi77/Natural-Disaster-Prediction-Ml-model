"""
Diagnostic script to check what features the models actually expect
"""
import pickle
import os
import pandas as pd

model_dir = "models"

print("=" * 60)
print("🔍 Checking Model Feature Requirements")
print("=" * 60)

# Check earthquake model
try:
    print("\n1. EARTHQUAKE MODEL:")
    eq_model = pickle.load(open(os.path.join(model_dir, "earthquake_model.pkl"), "rb"))
    print(f"   Model type: {type(eq_model)}")
    
    # Try to get feature names
    if hasattr(eq_model, 'feature_names_in_'):
        print(f"   Expected features: {list(eq_model.feature_names_in_)}")
    elif hasattr(eq_model, 'feature_importances_'):
        print(f"   Number of features: {len(eq_model.feature_importances_)}")
    
    # Try a test prediction to see what it expects
    try:
        test_df1 = pd.DataFrame([[20.0, 78.0]], columns=['lat', 'lon'])
        eq_model.predict(test_df1)
        print("   ✅ Works with: ['lat', 'lon']")
    except Exception as e1:
        print(f"   ❌ ['lat', 'lon'] failed: {str(e1)[:100]}")
        
    try:
        test_df2 = pd.DataFrame([[20.0, 78.0]], columns=['latitude', 'longitude'])
        eq_model.predict(test_df2)
        print("   ✅ Works with: ['latitude', 'longitude']")
    except Exception as e2:
        print(f"   ❌ ['latitude', 'longitude'] failed: {str(e2)[:100]}")
        
    try:
        test_df3 = pd.DataFrame([[20.0, 78.0, 5.0, 10.0]], 
                               columns=['latitude', 'longitude', 'magnitude', 'depth'])
        eq_model.predict(test_df3)
        print("   ✅ Works with: ['latitude', 'longitude', 'magnitude', 'depth']")
    except Exception as e3:
        print(f"   ❌ Full features failed: {str(e3)[:100]}")
        
except Exception as e:
    print(f"   ❌ Error loading model: {e}")

# Check flood model
try:
    print("\n2. FLOOD MODEL:")
    flood_model = pickle.load(open(os.path.join(model_dir, "flood_model.pkl"), "rb"))
    print(f"   Model type: {type(flood_model)}")
    
    if hasattr(flood_model, 'feature_names_in_'):
        print(f"   Expected features: {list(flood_model.feature_names_in_)}")
    elif hasattr(flood_model, 'steps'):
        # It's a pipeline
        print(f"   Pipeline steps: {[s[0] for s in flood_model.steps]}")
    
    try:
        test_df1 = pd.DataFrame([[20.0, 78.0]], columns=['lat', 'lon'])
        flood_model.predict(test_df1)
        print("   ✅ Works with: ['lat', 'lon']")
    except Exception as e1:
        print(f"   ❌ ['lat', 'lon'] failed: {str(e1)[:100]}")
        
    try:
        test_df2 = pd.DataFrame([[20.0, 78.0]], columns=['latitude', 'longitude'])
        flood_model.predict(test_df2)
        print("   ✅ Works with: ['latitude', 'longitude']")
    except Exception as e2:
        print(f"   ❌ ['latitude', 'longitude'] failed: {str(e2)[:100]}")
        
except Exception as e:
    print(f"   ❌ Error loading model: {e}")

# Check wildfire model
try:
    print("\n3. WILDFIRE MODEL:")
    fire_model = pickle.load(open(os.path.join(model_dir, "wildfire_model.pkl"), "rb"))
    print(f"   Model type: {type(fire_model)}")
    
    if hasattr(fire_model, 'feature_names_in_'):
        print(f"   Expected features: {list(fire_model.feature_names_in_)}")
    
    try:
        test_df1 = pd.DataFrame([[20.0, 78.0]], columns=['lat', 'lon'])
        fire_model.predict(test_df1)
        print("   ✅ Works with: ['lat', 'lon']")
    except Exception as e1:
        print(f"   ❌ ['lat', 'lon'] failed: {str(e1)[:100]}")
        
    try:
        test_df2 = pd.DataFrame([[20.0, 78.0]], columns=['latitude', 'longitude'])
        fire_model.predict(test_df2)
        print("   ✅ Works with: ['latitude', 'longitude']")
    except Exception as e2:
        print(f"   ❌ ['latitude', 'longitude'] failed: {str(e2)[:100]}")
        
except Exception as e:
    print(f"   ❌ Error loading model: {e}")

print("\n" + "=" * 60)

