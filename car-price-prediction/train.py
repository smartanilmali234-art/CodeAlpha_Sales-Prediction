import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# -------------------------------
# Load Dataset
# -------------------------------
data = pd.read_csv("data/car_data.csv")

# Clean column names
data.columns = data.columns.str.strip().str.lower()

# -------------------------------
# Feature Engineering
# -------------------------------
# Create car_age
current_year = datetime.now().year
data['car_age'] = current_year - data['year']

# Encode categorical columns
data['fuel_type'] = data['fuel_type'].map({
    'Petrol': 0,
    'Diesel': 1,
    'CNG': 2
})

data['selling_type'] = data['selling_type'].map({
    'Dealer': 0,
    'Individual': 1
})

data['transmission'] = data['transmission'].map({
    'Manual': 0,
    'Automatic': 1
})

# -------------------------------
# Features & Target
# -------------------------------
X = data.drop(['selling_price', 'car_name'], axis=1)
y = data['selling_price']

# Save column order (IMPORTANT for app.py)
columns = X.columns

# -------------------------------
# Train Model
# -------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LinearRegression()
model.fit(X_train, y_train)

# -------------------------------
# Save Model + Columns
# -------------------------------
os.makedirs("model", exist_ok=True)

joblib.dump(model, "model/model.pkl")
joblib.dump(columns, "model/columns.pkl")

print("✅ Model trained and saved successfully!")
print("📁 Files created:")
print(" - model/model.pkl")
print(" - model/columns.pkl")