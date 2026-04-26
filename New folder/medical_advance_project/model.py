from __future__ import annotations

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split


FEATURE_COLUMNS = [
    "age",
    "bmi",
    "systolic_bp",
    "diastolic_bp",
    "glucose",
    "cholesterol",
    "heart_rate",
    "oxygen_saturation",
    "physical_activity",
    "smoking",
    "family_history",
    "stress_level",
]


def train_risk_model(data: pd.DataFrame):
    x = data[FEATURE_COLUMNS]
    y = data["disease_risk"]

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=250,
        max_depth=8,
        min_samples_split=8,
        random_state=42,
    )
    model.fit(x_train, y_train)

    predictions = model.predict(x_test)
    probabilities = model.predict_proba(x_test)[:, 1]

    metrics = {
        "accuracy": accuracy_score(y_test, predictions),
        "precision": precision_score(y_test, predictions),
        "recall": recall_score(y_test, predictions),
        "roc_auc": roc_auc_score(y_test, probabilities),
    }

    feature_importance = (
        pd.DataFrame(
            {"feature": FEATURE_COLUMNS, "importance": model.feature_importances_}
        )
        .sort_values("importance", ascending=False)
        .reset_index(drop=True)
    )

    return model, metrics, feature_importance


def predict_patient_risk(model, patient_input: pd.DataFrame) -> tuple[float, str]:
    probability = float(model.predict_proba(patient_input[FEATURE_COLUMNS])[0][1])

    if probability < 0.35:
        label = "Low"
    elif probability < 0.65:
        label = "Moderate"
    else:
        label = "High"

    return probability, label


def build_clinical_explanation(patient_input: pd.DataFrame) -> pd.DataFrame:
    row = patient_input.iloc[0]
    contributions = []

    def add(feature: str, value: float):
        contributions.append({"factor": feature, "impact_score": value})

    add("Age", max(0, (row["age"] - 45) * 0.05))
    add("BMI", max(0, (row["bmi"] - 25) * 0.25))
    add("Systolic BP", max(0, (row["systolic_bp"] - 120) * 0.04))
    add("Glucose", max(0, (row["glucose"] - 100) * 0.03))
    add("Cholesterol", max(0, (row["cholesterol"] - 180) * 0.015))
    add("Smoking", 2.5 if row["smoking"] else 0)
    add("Family History", 2.0 if row["family_history"] else 0)
    add("Stress", row["stress_level"] * 0.18)
    add("Physical Activity", -row["physical_activity"] * 0.25)
    add("Oxygen Saturation", -max(0, (row["oxygen_saturation"] - 95) * 0.4))

    explanation = pd.DataFrame(contributions).sort_values(
        "impact_score", ascending=False
    )
    return explanation.reset_index(drop=True)
