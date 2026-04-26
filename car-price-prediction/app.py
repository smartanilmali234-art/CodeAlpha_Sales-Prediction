import streamlit as st
import pandas as pd
import joblib
from datetime import datetime
import matplotlib.pyplot as plt
import os

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(page_title="Car Price AI", page_icon="🚗", layout="wide")

# -------------------------------
# Load Model + Data (SAFE)
# -------------------------------
st.write("📁 Root files:", os.listdir())

if os.path.exists("model"):
    st.write("📁 Model folder:", os.listdir("model"))
else:
    st.warning("⚠️ 'model' folder not found")

if os.path.exists("data"):
    st.write("📁 Data folder:", os.listdir("data"))
else:
    st.warning("⚠️ 'data' folder not found")

try:
    # Try loading from folders
    model = joblib.load("model/model.pkl")
    columns = joblib.load("model/columns.pkl")
    data = pd.read_csv("data/car_data.csv")

except:
    try:
        # Fallback: load from root
        model = joblib.load("model.pkl")
        columns = joblib.load("columns.pkl")
        data = pd.read_csv("car_data.csv")

    except Exception as e:
        st.error(f"❌ File loading failed: {e}")
        st.stop()

data.columns = data.columns.str.strip().str.lower()

# -------------------------------
# Car Image Mapping
# -------------------------------
car_images = {
    "ritz": "https://imgd.aeplcdn.com/664x374/n/cw/ec/14129/maruti-suzuki-ritz-left-front-three-quarter3.jpeg",
    "swift": "https://imgd.aeplcdn.com/664x374/n/cw/ec/54399/swift-exterior-right-front-three-quarter.jpeg",
    "ciaz": "https://imgd.aeplcdn.com/664x374/n/cw/ec/37811/maruti-suzuki-ciaz-right-front-three-quarter2.jpeg",
    "fortuner": "https://imgd.aeplcdn.com/664x374/n/cw/ec/11579/toyota-fortuner-right-front-three-quarter2.jpeg",
    "innova": "https://imgd.aeplcdn.com/664x374/n/cw/ec/51435/toyota-innova-crysta-right-front-three-quarter2.jpeg"
}

# -------------------------------
# Title
# -------------------------------
st.title("🚗 AI Car Price Predictor (Advanced)")
st.markdown("### Auto Search + Image + Price Prediction + Trend Graph")

# -------------------------------
# Auto Search
# -------------------------------
car_list = sorted(data['car_name'].unique())

selected_car = st.selectbox("🔍 Select Car", car_list)
car_data = data[data['car_name'] == selected_car].iloc[0]

# -------------------------------
# Show Image
# -------------------------------
st.image(
    car_images.get(selected_car.lower(), "https://via.placeholder.com/600x300?text=Car+Image"),
    caption=selected_car.upper(),
    use_container_width=True
)

# -------------------------------
# Layout
# -------------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("Car Inputs")

    year = st.slider("Year", 2000, datetime.now().year, int(car_data['year']))

    present_price = st.number_input(
        "Showroom Price (Lakhs)",
        value=float(car_data['present_price'])
    )

    driven_kms = st.number_input(
        "Kilometers Driven",
        value=int(car_data['driven_kms'])
    )

with col2:
    st.subheader("Features")

    fuel = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG"])
    seller = st.selectbox("Seller Type", ["Dealer", "Individual"])
    transmission = st.selectbox("Transmission", ["Manual", "Automatic"])
    owner = st.selectbox("Owner", [0, 1, 2, 3])

# -------------------------------
# Feature Engineering
# -------------------------------
car_age = datetime.now().year - year

fuel_map = {"Petrol": 0, "Diesel": 1, "CNG": 2}
seller_map = {"Dealer": 0, "Individual": 1}
trans_map = {"Manual": 0, "Automatic": 1}

input_dict = {
    "year": year,
    "present_price": present_price,
    "driven_kms": driven_kms,
    "fuel_type": fuel_map[fuel],
    "selling_type": seller_map[seller],
    "transmission": trans_map[transmission],
    "owner": owner,
    "car_age": car_age
}

input_df = pd.DataFrame([input_dict])
input_df = input_df.reindex(columns=columns, fill_value=0)

# -------------------------------
# Prediction
# -------------------------------
st.markdown("---")

if st.button("💰 Predict Price"):
    prediction = model.predict(input_df)[0]

    st.success(f"Estimated Price: ₹ {prediction:.2f} Lakhs")

    if prediction < 3:
        st.info("💡 Budget Car")
    elif prediction < 10:
        st.info("🚗 Mid Range Car")
    else:
        st.info("🔥 Premium Car")

    # Trend graph
    st.subheader("📊 Price Trend Analysis")

    years = list(range(year - 10, year + 1))
    trend_prices = [prediction * (0.85 + i * 0.02) for i in range(len(years))]

    fig, ax = plt.subplots()
    ax.plot(years, trend_prices, marker="o")
    ax.set_xlabel("Year")
    ax.set_ylabel("Price (Lakhs)")
    ax.set_title("Car Price Trend")

    st.pyplot(fig)

# -------------------------------
# Dataset Insights
# -------------------------------
st.markdown("---")

if st.checkbox("📊 Dataset Insights"):
    st.write(data.head())

    st.subheader("Selling Price Distribution")
    st.bar_chart(data['selling_price'])

    st.subheader("Top Cars")
    st.bar_chart(data['car_name'].value_counts().head(10))

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.caption("🚀 Advanced ML Project | Car Price AI")