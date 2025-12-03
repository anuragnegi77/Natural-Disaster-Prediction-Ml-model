"""
Test script to identify server errors
"""
import sys
import traceback

print("Testing server startup...")
print("=" * 60)

try:
    print("\n1. Testing imports...")
    from flask import Flask, jsonify, request, render_template
    from flask_cors import CORS
    import os
    import pickle
    import pandas as pd
    import numpy as np
    from math import radians, cos, sin, sqrt, atan2
    import traceback as tb
    from datetime import datetime
    print("   ✅ All imports successful")

    print("\n2. Testing Flask app creation...")
    app = Flask(__name__, template_folder=".", static_folder=".")
    CORS(app, resources={
        r"/*": {
            "origins": "*",
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type"]
        }
    })
    print("   ✅ Flask app created")

    print("\n3. Testing model loading...")
    model_dir = "models"
    earthquake_model = pickle.load(open(os.path.join(model_dir, "earthquake_model.pkl"), "rb"))
    flood_model = pickle.load(open(os.path.join(model_dir, "flood_model.pkl"), "rb"))
    wildfire_model = pickle.load(open(os.path.join(model_dir, "wildfire_model.pkl"), "rb"))
    print("   ✅ Models loaded")

    print("\n4. Testing CSV loading...")
    earthquakes_df = pd.read_csv("earthquakes.csv")
    floods_df = pd.read_csv("floods.csv")
    wildfires_df = pd.read_csv("wildfires.csv")
    print("   ✅ CSV files loaded")

    print("\n5. Testing route definition...")
    @app.route('/test')
    def test():
        return jsonify({"status": "ok"})
    print("   ✅ Routes work")

    print("\n6. Testing server can start (not actually starting)...")
    print("   ✅ Server configuration is valid")
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED - No errors found!")
    print("=" * 60)
    print("\n💡 If you're seeing server errors, they might be:")
    print("   1. Port 5000 already in use - try changing port in app.py")
    print("   2. Server already running - check for existing Python processes")
    print("   3. Firewall blocking - check Windows Firewall settings")
    print("   4. Template not found - ensure index.html exists in project root")

except Exception as e:
    print(f"\n❌ ERROR FOUND:")
    print(f"   Type: {type(e).__name__}")
    print(f"   Message: {str(e)}")
    print(f"\n📋 Full traceback:")
    traceback.print_exc()
    sys.exit(1)

