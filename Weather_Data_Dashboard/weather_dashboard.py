#  Streamlit App: Real-Time Weather Dashboard
# Author: Priyanka Malavade (Enhanced as Weather Forecasting Dashboard)

import streamlit as st
import requests
import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. Page Config
st.set_page_config(page_title="Weather Dashboard", page_icon="🌤️", layout="wide")

# 2. CSS
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to right, #667eea, #764ba2);
        color: white;
    }
    .title {
        font-size: 2.5rem;
        font-weight: 700;
        color: white;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric {
        font-size: 1.1rem;
        background: rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    .map-box, .chart-box {
    background: rgba(255, 255, 255, 0.9);
    border-radius: 15px;
    padding: 1rem 1.5rem;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
    margin-top: 2rem;
    }
        

    .metric b {
        color: #f1c40f;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Constants
API_KEY = "746e9991aa7c2ed7173ca31d752db5fc"
WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast"

# 4. Sidebar
with st.sidebar:
    st.header("🔍 Search Weather")
    city = st.text_input("Enter a city name:", "Mumbai")
    unit = st.selectbox("Temperature Unit", ["Celsius", "Fahrenheit"])
    unit_param = "metric" if unit == "Celsius" else "imperial"
    unit_symbol = "°C" if unit == "Celsius" else "°F"

# 5. Title
st.markdown('<div class="title">🌤️ Real-Time Weather Forecast Dashboard</div>', unsafe_allow_html=True)

# 6. Fetch Data
if city:
    res = requests.get(WEATHER_URL, params={'q': city, 'appid': API_KEY, 'units': unit_param})
    if res.status_code == 200:
        data = res.json()
        name = data['name']
        country = data['sys']['country']
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        desc = data['weather'][0]['description'].title()
        wind = data['wind']['speed']
        icon = f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png"
        lat, lon = data['coord']['lat'], data['coord']['lon']
        time_now = datetime.datetime.now().strftime("%d %b %Y, %I:%M %p")

        # Dashboard Layout
        st.markdown(f"#### 📍 Weather Report for {name}, {country}")
        col1, col2, col3 = st.columns([1, 2, 2])

        with col1:
            st.image(icon, width=100)
        with col2:
            st.markdown(f"<div class='metric'>🕒 <b>Time:</b> {time_now}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='metric'>🌡️ <b>Temperature:</b> {temp} {unit_symbol}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='metric'>☁️ <b>Condition:</b> {desc}</div>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"<div class='metric'>💧 <b>Humidity:</b> {humidity}%</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='metric'>🌬️ <b>Wind Speed:</b> {wind} m/s</div>", unsafe_allow_html=True)

        # Map
        st.markdown('<div class="map-box">', unsafe_allow_html=True)
        st.markdown("### 📍 City Location on Map")
        st.map(data={"lat": [lat], "lon": [lon]})
        st.markdown('</div>', unsafe_allow_html=True)


        # Forecast Chart
        st.markdown("### 📊 5-Day Forecast")
        fore = requests.get(FORECAST_URL, params={'q': city, 'appid': API_KEY, 'units': unit_param})
        if fore.status_code == 200:
            forecast_list = fore.json()['list']
            df_fore = pd.DataFrame([{
                'datetime': item['dt_txt'],
                'temperature': item['main']['temp']
            } for item in forecast_list])

            df_fore['datetime'] = pd.to_datetime(df_fore['datetime'])
            fig = px.line(df_fore, x='datetime', y='temperature', title="5-Day Temperature Forecast",
                          labels={'temperature': f"Temp ({unit_symbol})"}, line_shape='spline')
            st.plotly_chart(fig, use_container_width=True)

        # Footer
        with st.expander("📘 About this App"):
            st.markdown("""
                Built using Streamlit + OpenWeatherMap API.
                Real-time forecast, temperature, humidity, and wind metrics.
                Created by Priyanka Malavade.
            """)
    else:
        st.error("❌ City not found or API issue.")