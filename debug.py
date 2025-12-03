"""
Comprehensive debugging tool for DisasterScope
Run this to diagnose issues before starting the server
"""
import os
import sys
import pickle
import pandas as pd

def check_models():
    """Check if all models exist and can be loaded"""
    print("\n" + "="*60)
    print("🔍 CHECKING MODELS")
    print("="*60)
    
    model_dir = "models"
    required_models = ["earthquake_model.pkl", "flood_model.pkl", "wildfire_model.pkl"]
    all_ok = True
    
    for model_file in required_models:
        model_path = os.path.join(model_dir, model_file)
        if not os.path.exists(model_path):
            print(f"❌ {model_file} NOT FOUND at {model_path}")
            all_ok = False
        else:
            try:
                with open(model_path, "rb") as f:
                    model = pickle.load(f)
                print(f"✅ {model_file} loaded successfully (type: {type(model).__name__})")
            except Exception as e:
                print(f"❌ {model_file} FAILED to load: {str(e)}")
                all_ok = False
    
    return all_ok

def check_csv_files():
    """Check if CSV files exist and are readable"""
    print("\n" + "="*60)
    print("🔍 CHECKING CSV FILES")
    print("="*60)
    
    csv_files = ["earthquakes.csv", "floods.csv", "wildfires.csv"]
    all_ok = True
    
    for csv_file in csv_files:
        if not os.path.exists(csv_file):
            print(f"❌ {csv_file} NOT FOUND")
            all_ok = False
        else:
            try:
                df = pd.read_csv(csv_file)
                print(f"✅ {csv_file} loaded successfully ({len(df)} rows)")
                print(f"   Columns: {list(df.columns)}")
            except Exception as e:
                print(f"❌ {csv_file} FAILED to load: {str(e)}")
                all_ok = False
    
    return all_ok

def check_dependencies():
    """Check if all required packages are installed"""
    print("\n" + "="*60)
    print("🔍 CHECKING DEPENDENCIES")
    print("="*60)
    
    required = {
        "flask": "Flask",
        "flask_cors": "flask-cors",
        "pandas": "pandas",
        "sklearn": "scikit-learn",
        "numpy": "numpy"
    }
    
    all_ok = True
    for module, package in required.items():
        try:
            __import__(module)
            print(f"✅ {package} installed")
        except ImportError:
            print(f"❌ {package} NOT INSTALLED - Run: pip install {package}")
            all_ok = False
    
    return all_ok

def test_prediction():
    """Test a sample prediction"""
    print("\n" + "="*60)
    print("🔍 TESTING PREDICTIONS")
    print("="*60)
    
    try:
        model_dir = "models"
        earthquakes_df = pd.read_csv("earthquakes.csv")
        floods_df = pd.read_csv("floods.csv")
        wildfires_df = pd.read_csv("wildfires.csv")
        
        # Load models
        earthquake_model = pickle.load(open(os.path.join(model_dir, "earthquake_model.pkl"), "rb"))
        flood_model = pickle.load(open(os.path.join(model_dir, "flood_model.pkl"), "rb"))
        wildfire_model = pickle.load(open(os.path.join(model_dir, "wildfire_model.pkl"), "rb"))
        
        # Test coordinates
        lat, lng = 20.59, 78.96
        
        # Earthquake prediction
        eq_magnitude = earthquakes_df['magnitude'].mean() if 'magnitude' in earthquakes_df.columns else 5.0
        eq_depth = earthquakes_df['depth'].mean() if 'depth' in earthquakes_df.columns else 10.0
        eq_input = pd.DataFrame([[lat, lng, eq_magnitude, eq_depth]], 
                               columns=['latitude', 'longitude', 'magnitude', 'depth'])
        eq_prob = earthquake_model.predict_proba(eq_input)[0][1] * 100
        print(f"✅ Earthquake prediction: {eq_prob:.2f}%")
        
        # Flood prediction
        flood_rainfall = floods_df['rainfall'].mean() if 'rainfall' in floods_df.columns else 100.0
        flood_input = pd.DataFrame([[lat, lng, flood_rainfall]], 
                                 columns=['latitude', 'longitude', 'rainfall'])
        flood_prob = flood_model.predict_proba(flood_input)[0][1] * 100
        print(f"✅ Flood prediction: {flood_prob:.2f}%")
        
        # Wildfire prediction
        if 'Fires' in wildfires_df.columns:
            fires_series = pd.to_numeric(wildfires_df['Fires'].astype(str).str.replace(',', ''), errors='coerce')
            avg_fires = fires_series.mean() if not fires_series.isna().all() else 50000.0
        else:
            avg_fires = 50000.0
        wildfire_input = pd.DataFrame([[avg_fires]], columns=['Fires'])
        fire_prob = wildfire_model.predict_proba(wildfire_input)[0][1] * 100
        print(f"✅ Wildfire prediction: {fire_prob:.2f}%")
        
        return True
        
    except Exception as e:
        print(f"❌ Prediction test FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("\n" + "="*60)
    print("🐛 DISASTERSCOPE DEBUG TOOL")
    print("="*60)
    
    results = {
        "dependencies": check_dependencies(),
        "csv_files": check_csv_files(),
        "models": check_models(),
        "predictions": test_prediction()
    }
    
    print("\n" + "="*60)
    print("📊 SUMMARY")
    print("="*60)
    
    all_passed = all(results.values())
    
    for check, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {check.replace('_', ' ').title()}")
    
    if all_passed:
        print("\n🎉 All checks passed! Your setup is ready.")
        return 0
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

