# model.py

import joblib
import os

from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier

# ---------------- LOAD DATA ----------------
iris = load_iris()
X = iris.data
y = iris.target

# ---------------- CREATE MODELS ----------------
models = {
    "random_forest": RandomForestClassifier(),
    "svm": SVC(probability=True),
    "knn": KNeighborsClassifier()
}

# ---------------- TRAIN MODELS ----------------
trained_models = {}

for name, model in models.items():
    model.fit(X, y)
    trained_models[name] = model

# ---------------- CREATE MODELS FOLDER ----------------
os.makedirs("models", exist_ok=True)

# ---------------- SAVE MODELS ----------------
for name, model in trained_models.items():
    joblib.dump(model, f"models/{name}.pkl")

# ---------------- SAVE LABELS ----------------
joblib.dump(iris.target_names, "models/labels.pkl")

print("✅ All models trained and saved successfully!")