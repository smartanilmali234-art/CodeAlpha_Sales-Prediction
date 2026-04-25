import streamlit as st
import joblib
import pandas as pd
import matplotlib.pyplot as plt
import os

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="🚀 Sales Intelligence Dashboard",
    layout="wide"
)

# -------------------------------
# Load Model (FIXED PATH)
# -------------------------------
@st.cache_resource
def load_model():
    model_path = os.path.join("model", "model.pkl")  # ✅ correct path

    if not os.path.exists(model_path):
        st.error("❌ model/model.pkl not found!")
        st.info("Make sure your model is inside 'model' folder and pushed to GitHub.")
        st.stop()

    return joblib.load(model_path)

model = load_model()

# -------------------------------
# Title
# -------------------------------
st.title("🚀 Sales Intelligence Dashboard")
st.markdown("Predict sales based on advertising spend")

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
col1.metric("📺 TV Budget", tv)
col2.metric("📻 Radio Budget", radio)
col3.metric("📰 Newspaper Budget", news)

st.metric("📊 Predicted Sales", f"{prediction:.2f}")

# -------------------------------
# Chart
# -------------------------------
st.subheader("📊 Budget Distribution")

fig, ax = plt.subplots()
ax.bar(["TV", "Radio", "Newspaper"], [tv, radio, news])
ax.set_ylabel("Budget")
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

colA, colB = st.columns(2)

with colA:
    st.markdown("### Scenario A")
    sA = st.selectbox("Select Scenario A", list(scenarios.keys()))
    tv_a = st.number_input("TV A", value=scenarios[sA]["TV"])
    radio_a = st.number_input("Radio A", value=scenarios[sA]["Radio"])
    news_a = st.number_input("News A", value=scenarios[sA]["Newspaper"])

with colB:
    st.markdown("### Scenario B")
    sB = st.selectbox("Select Scenario B", list(scenarios.keys()))
    tv_b = st.number_input("TV B", value=scenarios[sB]["TV"])
    radio_b = st.number_input("Radio B", value=scenarios[sB]["Radio"])
    news_b = st.number_input("News B", value=scenarios[sB]["Newspaper"])

if st.button("🚀 Compare Scenarios"):
    data_a = pd.DataFrame({"TV": [tv_a], "Radio": [radio_a], "Newspaper": [news_a]})
    data_b = pd.DataFrame({"TV": [tv_b], "Radio": [radio_b], "Newspaper": [news_b]})

    pred_a = model.predict(data_a)[0]
    pred_b = model.predict(data_b)[0]

    st.success(f"Scenario A Sales: {pred_a:.2f}")
    st.success(f"Scenario B Sales: {pred_b:.2f}")

    if pred_a > pred_b:
        st.success("🏆 Scenario A performs better")
    elif pred_b > pred_a:
        st.success("🏆 Scenario B performs better")
    else:
        st.info("Both scenarios perform equally")

# -------------------------------
# Upload CSV
# -------------------------------
st.subheader("📂 Upload Dataset")

file = st.file_uploader("Upload CSV", type=["csv"])

if file:
    df = pd.read_csv(file)
    st.write(df.head())

    if {"TV", "Radio", "Newspaper"}.issubset(df.columns):
        df["Predicted_Sales"] = model.predict(df[["TV", "Radio", "Newspaper"]])
        st.write(df.head())

        st.download_button("⬇️ Download Predictions", df.to_csv(index=False))
    else:
        st.error("CSV must contain TV, Radio, Newspaper columns")

# -------------------------------
# Insights
# -------------------------------
st.subheader("💡 Insights")

if tv > radio and tv > news:
    st.success("📺 TV advertising has the highest impact on sales")
elif radio > tv:
    st.success("📻 Radio campaigns are performing strongly")
else:
    st.success("📰 Newspaper ads are contributing significantly")

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.caption("Built for ML Internship 🚀")

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