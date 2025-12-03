import pickle
import pandas as pd
import os

# Paths
model_dir = "backend/models"
flood_model_path = os.path.join(model_dir, "flood_model.pkl")
earth_model_path = os.path.join(model_dir, "earthquake_model.pkl")
fire_model_path = os.path.join(model_dir, "wildfire_model.pkl")

# Load models
flood_model = pickle.load(open(flood_model_path, "rb"))
earth_model = pickle.load(open(earth_model_path, "rb"))
fire_model = pickle.load(open(fire_model_path, "rb"))

def predict_disaster(lat, lon, rainfall=None, seismic=None, fires=None):
    results = {}
    
    # Flood Prediction
    if rainfall is not None:
        flood_df = pd.DataFrame([[lat, lon, rainfall]], columns=['latitude', 'longitude', 'rainfall'])
        flood_prob = flood_model.predict_proba(flood_df)[0][1]
        results["Flood Risk"] = round(flood_prob * 100, 2)
    
    # Earthquake Prediction
    if seismic is not None:
        earth_df = pd.DataFrame([[lat, lon, seismic]], columns=['latitude', 'longitude', 'seismic_index'])
        earth_prob = earth_model.predict_proba(earth_df)[0][1]
        results["Earthquake Risk"] = round(earth_prob * 100, 2)
    
    # Wildfire Prediction
    if fires is not None:
        fire_df = pd.DataFrame([[fires]], columns=['Fires'])
        fire_prob = fire_model.predict_proba(fire_df)[0][1]
        results["Wildfire Risk"] = round(fire_prob * 100, 2)
    
    return results



