import numpy as np
import pandas as pd


def generate_patient_data(size: int = 600, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    age = rng.integers(18, 90, size)
    bmi = np.clip(rng.normal(27, 5, size), 16, 45)
    systolic_bp = np.clip(rng.normal(128, 18, size), 90, 210)
    diastolic_bp = np.clip(rng.normal(82, 12, size), 55, 130)
    glucose = np.clip(rng.normal(112, 30, size), 65, 260)
    cholesterol = np.clip(rng.normal(196, 34, size), 110, 360)
    heart_rate = np.clip(rng.normal(78, 12, size), 45, 140)
    oxygen_saturation = np.clip(rng.normal(96.5, 2, size), 82, 100)
    physical_activity = rng.integers(0, 8, size)
    smoking = rng.integers(0, 2, size)
    family_history = rng.integers(0, 2, size)
    stress_level = rng.integers(1, 11, size)

    risk_score = (
        (age - 18) * 0.03
        + (bmi - 25) * 0.18
        + (systolic_bp - 120) * 0.025
        + (glucose - 100) * 0.03
        + (cholesterol - 180) * 0.012
        + smoking * 2.4
        + family_history * 1.9
        + stress_level * 0.22
        - physical_activity * 0.35
        - (oxygen_saturation - 95) * 0.5
    )

    probability = 1 / (1 + np.exp(-(risk_score - 5.5) / 3.2))
    disease_risk = (probability > 0.52).astype(int)

    return pd.DataFrame(
        {
            "age": age,
            "bmi": np.round(bmi, 1),
            "systolic_bp": np.round(systolic_bp).astype(int),
            "diastolic_bp": np.round(diastolic_bp).astype(int),
            "glucose": np.round(glucose).astype(int),
            "cholesterol": np.round(cholesterol).astype(int),
            "heart_rate": np.round(heart_rate).astype(int),
            "oxygen_saturation": np.round(oxygen_saturation, 1),
            "physical_activity": physical_activity,
            "smoking": smoking,
            "family_history": family_history,
            "stress_level": stress_level,
            "disease_risk": disease_risk,
        }
    )
