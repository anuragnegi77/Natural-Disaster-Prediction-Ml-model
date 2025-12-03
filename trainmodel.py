import os
import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

print("Starting earthquake model training...")

data_path = "earthquakes.csv"
model_dir = "models"
os.makedirs(model_dir, exist_ok=True)
model_path = os.path.join(model_dir, "earthquake_model.pkl")

df = pd.read_csv(data_path)

required_cols = ['lat', 'lon', 'label']
missing = [col for col in required_cols if col not in df.columns]
if missing:
    raise ValueError(f"Missing columns: {missing}")

X = df[['lat', 'lon']]
y = df['label']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

preds = model.predict(X_test)
print("✅ Accuracy:", round(accuracy_score(y_test, preds), 3))

with open(model_path, "wb") as f:
    pickle.dump(model, f)

print(f"✅ Earthquake model saved to {model_path}")
