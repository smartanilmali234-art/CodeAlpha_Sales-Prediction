import streamlit as st
import joblib
import pandas as pd
import matplotlib.pyplot as plt
import os

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(page_title="🚀 Sales Dashboard", layout="wide")

# -------------------------------
# 🔥 Load Model (BULLETPROOF)
# -------------------------------
@st.cache_resource
def load_model():
    possible_paths = [
        "model/model.pkl",
        "model.pkl",
        "./model/model.pkl",
        "./model.pkl"
    ]

    for path in possible_paths:
        if os.path.exists(path):
            st.success(f"✅ Model loaded from: {path}")
            return joblib.load(path)

    # 🔥 Auto-train if missing
    st.warning("⚠️ Model not found. Training new model...")

    if os.path.exists("sales_data.csv"):
        df = pd.read_csv("sales_data.csv")

        # clean
        df.columns = df.columns.str.strip().str.replace(" ", "_")

        if "Unnamed:_0" in df.columns:
            df = df.drop("Unnamed:_0", axis=1)

        from sklearn.model_selection import train_test_split
        from sklearn.ensemble import RandomForestRegressor

        X = df[["TV", "Radio", "Newspaper"]]
        y = df["Sales"]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        model = RandomForestRegressor(n_estimators=100)
        model.fit(X_train, y_train)

        os.makedirs("model", exist_ok=True)
        joblib.dump(model, "model/model.pkl")

        st.success("✅ Model trained and saved automatically!")
        return model

    else:
        st.error("❌ No model or dataset found!")
        st.stop()


model = load_model()

# -------------------------------
# Title
# -------------------------------
st.title("🚀 Sales Intelligence Dashboard")

# -------------------------------
# Sidebar Inputs
# -------------------------------
st.sidebar.header("📥 Advertising Budget")

tv = st.sidebar.slider("TV Budget", 0, 300, 120)
radio = st.sidebar.slider("Radio Budget", 0, 50, 25)
news = st.sidebar.slider("Newspaper Budget", 0, 100, 40)

input_df = pd.DataFrame({
    "TV": [tv],
    "Radio": [radio],
    "Newspaper": [news]
})

# -------------------------------
# Prediction
# -------------------------------
prediction = model.predict(input_df)[0]

# -------------------------------
# KPI Section
# -------------------------------
col1, col2, col3 = st.columns(3)
col1.metric("📺 TV", tv)
col2.metric("📻 Radio", radio)
col3.metric("📰 Newspaper", news)

st.metric("📊 Predicted Sales", f"{prediction:.2f}")

# -------------------------------
# Chart
# -------------------------------
st.subheader("📊 Budget Distribution")

fig, ax = plt.subplots()
ax.bar(["TV", "Radio", "Newspaper"], [tv, radio, news])
st.pyplot(fig)

# -------------------------------
# Scenario Comparison
# -------------------------------
st.subheader("🔍 Scenario Comparison")

scenarios = {
    "TV Heavy": {"TV": 200, "Radio": 20, "Newspaper": 30},
    "Balanced": {"TV": 120, "Radio": 25, "Newspaper": 40},
    "Radio Focus": {"TV": 80, "Radio": 40, "Newspaper": 20}
}

col1, col2 = st.columns(2)

with col1:
    sA = st.selectbox("Scenario A", list(scenarios.keys()))
    tv_a = st.number_input("TV A", value=scenarios[sA]["TV"])
    radio_a = st.number_input("Radio A", value=scenarios[sA]["Radio"])
    news_a = st.number_input("News A", value=scenarios[sA]["Newspaper"])

with col2:
    sB = st.selectbox("Scenario B", list(scenarios.keys()))
    tv_b = st.number_input("TV B", value=scenarios[sB]["TV"])
    radio_b = st.number_input("Radio B", value=scenarios[sB]["Radio"])
    news_b = st.number_input("News B", value=scenarios[sB]["Newspaper"])

if st.button("Compare"):
    data_a = pd.DataFrame({"TV":[tv_a],"Radio":[radio_a],"Newspaper":[news_a]})
    data_b = pd.DataFrame({"TV":[tv_b],"Radio":[radio_b],"Newspaper":[news_b]})

    pred_a = model.predict(data_a)[0]
    pred_b = model.predict(data_b)[0]

    st.success(f"Scenario A: {pred_a:.2f}")
    st.success(f"Scenario B: {pred_b:.2f}")

# -------------------------------
# Upload CSV
# -------------------------------
st.subheader("📂 Upload Dataset")

file = st.file_uploader("Upload CSV", type=["csv"])

if file:
    df = pd.read_csv(file)
    st.write(df.head())

    if {"TV","Radio","Newspaper"}.issubset(df.columns):
        df["Predicted_Sales"] = model.predict(df[["TV","Radio","Newspaper"]])
        st.write(df.head())

        st.download_button("Download", df.to_csv(index=False))
    else:
        st.error("CSV must contain TV, Radio, Newspaper")

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.caption("ML Internship Project 🚀")

# -------------------------------
# Sidebar Inputs
# -------------------------------
st.sidebar.header("📥 Advertising Budget")

tv = st.sidebar.slider("TV Budget", 0, 300, 120)
radio = st.sidebar.slider("Radio Budget", 0, 50, 25)
news = st.sidebar.slider("Newspaper Budget", 0, 100, 40)

input_df = pd.DataFrame({
    "TV": [tv],
    "Radio": [radio],
    "Newspaper": [news]
})

# -------------------------------
# Prediction
# -------------------------------
prediction = model.predict(input_df)[0]

# -------------------------------
# KPI Section
# -------------------------------
col1, col2, col3 = st.columns(3)
col1.metric("📺 TV", tv)
col2.metric("📻 Radio", radio)
col3.metric("📰 Newspaper", news)

st.metric("📊 Predicted Sales", f"{prediction:.2f}")

# -------------------------------
# Chart
# -------------------------------
st.subheader("📊 Budget Distribution")

fig, ax = plt.subplots()
ax.bar(["TV", "Radio", "Newspaper"], [tv, radio, news])
st.pyplot(fig)

# -------------------------------
# Scenario Comparison
# -------------------------------
st.subheader("🔍 Scenario Comparison")

scenarios = {
    "TV Heavy": {"TV": 200, "Radio": 20, "Newspaper": 30},
    "Radio Focus": {"TV": 80, "Radio": 40, "Newspaper": 20},
    "Balanced": {"TV": 120, "Radio": 25, "Newspaper": 40}
}

colA, colB = st.columns(2)

with colA:
    sA = st.selectbox("Scenario A", list(scenarios.keys()))
    tv_a = st.number_input("TV A", value=scenarios[sA]["TV"])
    radio_a = st.number_input("Radio A", value=scenarios[sA]["Radio"])
    news_a = st.number_input("News A", value=scenarios[sA]["Newspaper"])

with colB:
    sB = st.selectbox("Scenario B", list(scenarios.keys()))
    tv_b = st.number_input("TV B", value=scenarios[sB]["TV"])
    radio_b = st.number_input("Radio B", value=scenarios[sB]["Radio"])
    news_b = st.number_input("News B", value=scenarios[sB]["Newspaper"])

if st.button("Compare"):
    data_a = pd.DataFrame({"TV":[tv_a],"Radio":[radio_a],"Newspaper":[news_a]})
    data_b = pd.DataFrame({"TV":[tv_b],"Radio":[radio_b],"Newspaper":[news_b]})

    pred_a = model.predict(data_a)[0]
    pred_b = model.predict(data_b)[0]

    st.success(f"Scenario A: {pred_a:.2f}")
    st.success(f"Scenario B: {pred_b:.2f}")

# -------------------------------
# Upload CSV
# -------------------------------
st.subheader("📂 Upload Dataset")

file = st.file_uploader("Upload CSV", type=["csv"])

if file:
    df = pd.read_csv(file)
    st.write(df.head())

    if {"TV","Radio","Newspaper"}.issubset(df.columns):
        df["Predicted_Sales"] = model.predict(df[["TV","Radio","Newspaper"]])
        st.write(df.head())

        st.download_button("Download", df.to_csv(index=False))
    else:
        st.error("CSV must contain TV, Radio, Newspaper")

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.caption("ML Internship Project 🚀")