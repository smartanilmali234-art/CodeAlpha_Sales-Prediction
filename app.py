import streamlit as st
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="🚀 Sales Intelligence Dashboard",
    layout="wide"
)

# -------------------------------
# Load Model
# -------------------------------
@st.cache_resource
def load_model():
    return joblib.load("model/model.pkl")

model = load_model()

# -------------------------------
# Title
# -------------------------------
st.title("🚀 Sales Intelligence Dashboard")
st.markdown("Analyze and predict sales using advertising data")

# -------------------------------
# Sidebar Inputs
# -------------------------------
st.sidebar.header("📥 Input Budget")

tv = st.sidebar.slider("TV Budget", 0, 300, 120)
radio = st.sidebar.slider("Radio Budget", 0, 50, 25)
newspaper = st.sidebar.slider("Newspaper Budget", 0, 100, 40)

input_df = pd.DataFrame({
    "TV": [tv],
    "Radio": [radio],
    "Newspaper": [newspaper]
})

# -------------------------------
# Prediction
# -------------------------------
prediction = model.predict(input_df)[0]

# -------------------------------
# KPI Dashboard
# -------------------------------
col1, col2, col3 = st.columns(3)

col1.metric("📺 TV Budget", tv)
col2.metric("📻 Radio Budget", radio)
col3.metric("📰 Newspaper Budget", newspaper)

st.metric("📊 Predicted Sales", f"{prediction:.2f}")

# -------------------------------
# Budget Distribution Chart
# -------------------------------
st.subheader("📊 Budget Distribution")

fig, ax = plt.subplots()
channels = ["TV", "Radio", "Newspaper"]
values = [tv, radio, newspaper]

ax.pie(values, labels=channels, autopct="%1.1f%%")
st.pyplot(fig)

# -------------------------------
# Feature Importance
# -------------------------------
st.subheader("🧠 Feature Importance")

try:
    importances = model.named_steps["regressor"].feature_importances_

    df_imp = pd.DataFrame({
        "Feature": ["TV", "Radio", "Newspaper"],
        "Importance": importances
    }).sort_values(by="Importance", ascending=True)

    fig2, ax2 = plt.subplots()
    ax2.barh(df_imp["Feature"], df_imp["Importance"])
    st.pyplot(fig2)

except:
    st.warning("Feature importance not available.")

# -------------------------------
# Scenario Comparison
# -------------------------------
st.subheader("🔍 Compare Scenarios")

colA, colB = st.columns(2)

with colA:
    st.write("Scenario A")
    tv_a = st.number_input("TV A", 0, 300, 100)
    radio_a = st.number_input("Radio A", 0, 50, 20)
    news_a = st.number_input("News A", 0, 100, 30)

with colB:
    st.write("Scenario B")
    tv_b = st.number_input("TV B", 0, 300, 150)
    radio_b = st.number_input("Radio B", 0, 50, 30)
    news_b = st.number_input("News B", 0, 100, 50)

if st.button("Compare"):
    data_a = pd.DataFrame({"TV":[tv_a],"Radio":[radio_a],"Newspaper":[news_a]})
    data_b = pd.DataFrame({"TV":[tv_b],"Radio":[radio_b],"Newspaper":[news_b]})

    pred_a = model.predict(data_a)[0]
    pred_b = model.predict(data_b)[0]

    st.success(f"Scenario A Sales: {pred_a:.2f}")
    st.success(f"Scenario B Sales: {pred_b:.2f}")

# -------------------------------
# Upload Dataset
# -------------------------------
st.subheader("📂 Upload Your Dataset")

file = st.file_uploader("Upload CSV", type=["csv"])

if file:
    df = pd.read_csv(file)
    st.write("Preview Data:", df.head())

    if {"TV", "Radio", "Newspaper"}.issubset(df.columns):
        preds = model.predict(df[["TV","Radio","Newspaper"]])
        df["Predicted_Sales"] = preds

        st.write("📊 Predictions:", df.head())

        st.download_button(
            "⬇️ Download Results",
            df.to_csv(index=False),
            file_name="predictions.csv"
        )
    else:
        st.error("CSV must contain TV, Radio, Newspaper columns")

# -------------------------------
# Insights
# -------------------------------
st.subheader("💡 Insights")

if tv > radio and tv > newspaper:
    st.success("📺 TV is driving most sales impact")
elif radio > tv:
    st.success("📻 Radio campaigns are strong")
else:
    st.success("📰 Newspaper ads contributing significantly")

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.caption("Built for ML Internship Project 🚀")