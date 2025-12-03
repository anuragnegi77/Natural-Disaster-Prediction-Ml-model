import os
import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

print("🔥 Starting wildfire model training...")

data_path = "wildfires.csv"     # file from preprocessing step
model_dir = "models"
os.makedirs(model_dir, exist_ok=True)
model_path = os.path.join(model_dir, "wildfire_model.pkl")

df = pd.read_csv(data_path)

# Ensure required columns exist
required_cols = ['lat', 'lon', 'label']
missing = [c for c in required_cols if c not in df.columns]
if missing:
    raise ValueError(f"Missing columns: {missing}")

# Features and labels
X = df[['lat', 'lon']]
y = df['label']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Model
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# Evaluate
preds = model.predict(X_test)
print("✅ Wildfire Model Accuracy:", round(accuracy_score(y_test, preds), 3))

# Save model
with open(model_path, "wb") as f:
    pickle.dump(model, f)

print(f"✅ Wildfire model saved at: {model_path}")
