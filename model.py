import pickle
import os
import pandas as pd

current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, "models", "earthquake_model.pkl")  # ✅ Correct path

if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file not found: {model_path}")

with open(model_path, "rb") as f:
    ml_model = pickle.load(f)

def ml_predict_earthquake_risk(lat, lng):
    data = pd.DataFrame([[lat, lng]], columns=["lat", "lon"])
    prob = ml_model.predict_proba(data)[0][1]
    return round(prob * 100, 2)
