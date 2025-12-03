import pandas as pd
import numpy as np
import os

# ✅ Auto-detect project folder
base_path = os.path.dirname(os.path.abspath(__file__))

# ✅ Dataset paths
earthquake_path = os.path.join(base_path, "earthquakes.csv")
wildfire_path = os.path.join(base_path, "wildfires.csv")
flood_path = os.path.join(base_path, "floods.csv")

# ✅ Load datasets
earthquakes = pd.read_csv(earthquake_path)
wildfires = pd.read_csv(wildfire_path)
floods = pd.read_csv(flood_path)

# ✅ Ensure consistency in column names
earthquakes = earthquakes.rename(columns={"latitude": "lat", "longitude": "lon"})
wildfires = wildfires.rename(columns={"latitude": "lat", "longitude": "lon"})
floods = floods.rename(columns={"Latitude": "lat", "Longitude": "lon"})

# ✅ Drop rows with missing coordinates
earthquakes = earthquakes.dropna(subset=["lat", "lon"])
wildfires = wildfires.dropna(subset=["lat", "lon"])
floods = floods.dropna(subset=["lat", "lon"])

# ✅ Label creation
earthquakes["label"] = earthquakes["magnitude"].apply(lambda x: 1 if x >= 6 else 0)

wildfires["Fires"] = pd.to_numeric(wildfires["Fires"], errors="coerce")
wildfires = wildfires.dropna(subset=["Fires"])
wildfires["label"] = wildfires["Fires"].apply(lambda x: 1 if x >= 70000 else 0)

floods["FloodProbability"] = pd.to_numeric(floods["FloodProbability"], errors="coerce")
floods = floods.dropna(subset=["FloodProbability"])
floods["label"] = floods["FloodProbability"].apply(lambda x: 1 if x >= 50 else 0)

# ✅ Keep only required columns
earthquakes = earthquakes[["lat", "lon", "label"]]
wildfires = wildfires[["lat", "lon", "label"]]
floods = floods[["lat", "lon", "label"]]

# ✅ Generate negative samples
def generate_negative_samples(df, count):
    np.random.seed(42)
    lat_min, lat_max = df["lat"].min(), df["lat"].max()
    lon_min, lon_max = df["lon"].min(), df["lon"].max()
    
    lat_range = (lat_min - 5, lat_max + 5)
    lon_range = (lon_min - 5, lon_max + 5)
    
    neg_samples = {
        "lat": np.random.uniform(lat_range[0], lat_range[1], count),
        "lon": np.random.uniform(lon_range[0], lon_range[1], count),
        "label": 0
    }
    return pd.DataFrame(neg_samples)

eq_neg = generate_negative_samples(earthquakes, len(earthquakes))
wf_neg = generate_negative_samples(wildfires, len(wildfires))
flood_neg = generate_negative_samples(floods, len(floods))

earthquake_data = pd.concat([earthquakes, eq_neg], ignore_index=True)
wildfire_data = pd.concat([wildfires, wf_neg], ignore_index=True)
flood_data = pd.concat([floods, flood_neg], ignore_index=True)

# ✅ Save updated datasets
earthquake_data.to_csv(os.path.join(base_path, "earthquakes.csv"), index=False)
wildfire_data.to_csv(os.path.join(base_path, "wildfires.csv"), index=False)
flood_data.to_csv(os.path.join(base_path, "floods.csv"), index=False)

print("✅ Preprocessing completed and datasets updated successfully!")
