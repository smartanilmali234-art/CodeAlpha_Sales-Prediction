import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_js_eval import get_geolocation

from utils.weather_api import (
    search_cities,
    get_city_by_coordinates,
    get_current_weather_by_coords,
    get_5_day_forecast_by_coords
)
from utils.export_word import create_weather_doc


st.set_page_config(
    page_title="Worldwide Weather App",
    page_icon="🌍",
    layout="wide"
)

st.markdown("""
<style>
.main-title {
    font-size: 42px;
    font-weight: 800;
    text-align: center;
}
.sub-title {
    text-align: center;
    color: gray;
    font-size: 18px;
}
.weather-card {
    background: linear-gradient(135deg, #1e88e5, #42a5f5);
    padding: 25px;
    border-radius: 20px;
    color: white;
    margin-bottom: 20px;
}
.forecast-card {
    background: #f8f9fa;
    padding: 18px;
    border-radius: 16px;
    margin-bottom: 12px;
    border-left: 5px solid #1e88e5;
}
</style>
""", unsafe_allow_html=True)


st.markdown('<div class="main-title">🌍 Worldwide Real-Time Weather App</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Auto Location • Smart City Search • Daily Forecast • Word Report</div>', unsafe_allow_html=True)

st.sidebar.header("🔍 Search Weather")

use_location = st.sidebar.button("📍 Use My Current Location")

search_text = st.sidebar.text_input(
    "Search city",
    placeholder="Type city: Mumbai, London, Tokyo..."
)

selected_city = None

if search_text.strip():
    city_results = search_cities(search_text)

    if city_results:
        city_labels = [city["label"] for city in city_results]

        selected_label = st.sidebar.selectbox(
            "Select city",
            city_labels
        )

        selected_city = city_results[city_labels.index(selected_label)]
    else:
        st.sidebar.error("No city found.")

search_btn = st.sidebar.button("🌦️ Search Weather")

lat = None
lon = None
display_name = None

if use_location:
    location = get_geolocation()

    if location and "coords" in location:
        lat = location["coords"]["latitude"]
        lon = location["coords"]["longitude"]

        detected = get_city_by_coordinates(lat, lon)
        display_name = detected["label"] if detected else "Your Location"

        st.sidebar.success(f"Detected: {display_name}")
    else:
        st.sidebar.error("Location permission denied or unavailable.")

elif search_btn:
    if selected_city:
        lat = selected_city["lat"]
        lon = selected_city["lon"]
        display_name = selected_city["label"]
    else:
        st.warning("Please search and select a city from sidebar.")

if lat and lon:
    current = get_current_weather_by_coords(lat, lon)

    if current is None:
        st.error("Weather data not found.")
    else:
        icon_url = f"https://openweathermap.org/img/wn/{current['icon']}@2x.png"

        st.markdown('<div class="weather-card">', unsafe_allow_html=True)

        col_img, col1, col2, col3, col4 = st.columns([1, 2, 2, 2, 2])

        with col_img:
            st.image(icon_url, width=90)

        col1.metric("Temperature", f"{current['temperature']} °C")
        col2.metric("Feels Like", f"{current['feels_like']} °C")
        col3.metric("Humidity", f"{current['humidity']}%")
        col4.metric("Wind", f"{current['wind']} m/s")

        st.markdown(
            f"### 📍 {current['city']}, {current['country']} | {current['condition'].title()}",
            unsafe_allow_html=True
        )

        st.markdown("</div>", unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        c1.metric("Pressure", f"{current['pressure']} hPa")
        c2.metric("Visibility", f"{current['visibility']} km" if current["visibility"] != "N/A" else "N/A")
        c3.metric("Clouds", f"{current['clouds']}%")

        st.divider()

        forecast_df = get_5_day_forecast_by_coords(lat, lon)

        if forecast_df.empty:
            st.error("Forecast not available.")
        else:
            forecast_df["datetime"] = pd.to_datetime(forecast_df["datetime"])
            forecast_df["date"] = forecast_df["datetime"].dt.date

            daily_df = forecast_df.groupby("date").agg({
                "temperature": "mean",
                "temp_min": "min",
                "temp_max": "max",
                "humidity": "mean",
                "wind": "mean",
                "condition": lambda x: x.mode()[0],
                "icon": lambda x: x.mode()[0]
            }).reset_index()

            daily_df["temperature"] = daily_df["temperature"].round(1)
            daily_df["temp_min"] = daily_df["temp_min"].round(1)
            daily_df["temp_max"] = daily_df["temp_max"].round(1)
            daily_df["humidity"] = daily_df["humidity"].round(0)
            daily_df["wind"] = daily_df["wind"].round(1)

            daily_df["icon_url"] = daily_df["icon"].apply(
                lambda icon: f"https://openweathermap.org/img/wn/{icon}@2x.png"
            )

            st.subheader("📅 Daily Forecast")

            for _, row in daily_df.iterrows():
                st.markdown('<div class="forecast-card">', unsafe_allow_html=True)

                col1, col2, col3, col4 = st.columns([1, 2, 2, 2])

                with col1:
                    st.image(row["icon_url"], width=65)

                with col2:
                    st.write(f"**📅 {row['date']}**")
                    st.write(f"🌥️ {row['condition'].title()}")

                with col3:
                    st.write(f"🌡️ Avg: **{row['temperature']} °C**")
                    st.write(f"🔻 Min: **{row['temp_min']} °C**")
                    st.write(f"🔺 Max: **{row['temp_max']} °C**")

                with col4:
                    st.write(f"💧 Humidity: **{int(row['humidity'])}%**")
                    st.write(f"💨 Wind: **{row['wind']} m/s**")

                st.markdown("</div>", unsafe_allow_html=True)

            st.subheader("📊 Temperature Chart")

            fig = px.line(
                daily_df,
                x="date",
                y=["temp_min", "temperature", "temp_max"],
                title="Daily Min / Average / Max Temperature",
                markers=True
            )

            st.plotly_chart(fig, use_container_width=True)

            st.subheader("📄 Download Report")

            file_path = create_weather_doc(current["city"], current, daily_df)

            with open(file_path, "rb") as file:
                st.download_button(
                    label="📄 Download Word Report",
                    data=file,
                    file_name=file_path,
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )

else:
    st.info("👈 Use current location or search any city from the sidebar.")