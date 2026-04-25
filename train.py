import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score


def load_data(path):
    df = pd.read_csv(path)

    # Clean column names
    df.columns = df.columns.str.strip().str.replace(" ", "_")

    print("📊 Columns in dataset:", df.columns.tolist())
    return df


def build_pipeline(numeric_features):
    # Only numeric features in your dataset
    numeric_transformer = Pipeline(steps=[
        ("scaler", StandardScaler())
    ])

    preprocessor = ColumnTransformer(transformers=[
        ("num", numeric_transformer, numeric_features)
    ])

    model = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("regressor", RandomForestRegressor(n_estimators=100, random_state=42))
    ])

    return model


def train():
    df = load_data("data/sales_data.csv")

    # ❌ Drop useless column
    if "Unnamed:_0" in df.columns:
        df = df.drop("Unnamed:_0", axis=1)

    # Remove missing values
    df = df.dropna()

    # ✅ Correct features based on YOUR dataset
    numeric_features = ["TV", "Radio", "Newspaper"]

    # Check required columns
    for col in numeric_features + ["Sales"]:
        if col not in df.columns:
            raise ValueError(f"❌ Missing column: {col}")

    X = df[numeric_features]
    y = df["Sales"]

    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = build_pipeline(numeric_features)

    print("🚀 Training model...")
    model.fit(X_train, y_train)

    preds = model.predict(X_test)

    # Evaluation
    mae = mean_absolute_error(y_test, preds)
    r2 = r2_score(y_test, preds)

    print("\n📈 Model Performance:")
    print(f"MAE: {mae:.2f}")
    print(f"R2 Score: {r2:.2f}")

    # Save model
    joblib.dump(model, "model/model.pkl")
    print("\n✅ Model saved at: model/model.pkl")


if __name__ == "__main__":
    train()