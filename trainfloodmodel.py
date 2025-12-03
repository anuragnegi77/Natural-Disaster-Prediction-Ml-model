import os
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import pickle

print("Starting flood model training...")

csv_path = "floods.csv"   # ✅ same folder as your project/preprocessing output
model_dir = "models"
os.makedirs(model_dir, exist_ok=True)
model_path = os.path.join(model_dir, "flood_model.pkl")

df = pd.read_csv(csv_path)

required_columns = ['lat', 'lon', 'label']
missing = [col for col in required_columns if col not in df.columns]
if missing:
    raise ValueError(f"Missing columns in flood data: {missing}")

# ✅ Features = lat & lon only (FloodProbability already used to label)
X = df[['lat', 'lon']]
y = df['label']

model = Pipeline([
    ('scaler', StandardScaler()),
    ('logreg', LogisticRegression(max_iter=2000))
])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model.fit(X_train, y_train)

preds = model.predict(X_test)
print("Model Accuracy:", accuracy_score(y_test, preds))

with open(model_path, "wb") as f:
    pickle.dump(model, f)

print(f"✅ Flood model trained & saved to {model_path}")
