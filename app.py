import streamlit as st
import pandas as pd
import joblib
from pathlib import Path



# -----------------------------
# Load Model
# -----------------------------
model = joblib.load("delivery_time_model.pkl")


# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Swiggy Delivery Time Prediction",
    layout="wide"
)




# -----------------------------
# Title
# -----------------------------
import base64

image_path = Path(__file__).parent / "swiggy_banner.png"

with open(image_path, "rb") as img:
    encoded = base64.b64encode(img.read()).decode()

st.markdown(f"""
<style>
.hero-banner {{
    background-image: url("data:image/png;base64,{encoded}");
    background-size: 100% 100%;
    background-position: center;
    background-repeat: no-repeat;
    min-height: 420px;
    border-radius: 14px;
    display: flex;
    align-items: center;
    padding: 35px;
    box-sizing: border-box;
    margin-bottom: 25px;
}}

.hero-text {{
    max-width: 48%;
}}

.hero-text h1 {{
    color: #252525;
    font-size: 38px;
    font-weight: 800;
    line-height: 1.2;
    margin-bottom: 16px;
}}

.hero-text p {{
    color: #444444;
    font-size: 17px;
    line-height: 1.6;
}}
</style>

<div class="hero-banner">
    <div class="hero-text">
        <h1> Swiggy Delivery Time Prediction</h1>
        <p>
            Predict food delivery time using Machine Learning.
            Smarter predictions for faster, more reliable deliveries.
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Input Section
# -----------------------------
st.subheader("Enter Delivery Details")


col1, col2, col3 = st.columns(3)


# =====================================================
# CUSTOMER / PARTNER + WEATHER
# =====================================================

with col1:

    age = st.number_input(
        "Delivery Partner Age",
        min_value=18,
        max_value=60,
        value=25
    )

    ratings = st.number_input(
        "Delivery Partner Rating",
        min_value=1.0,
        max_value=5.0,
        value=4.5,
        step=0.1
    )

    weather = st.selectbox(
        "Weather",
        [
            "sunny",
            "stormy",
            "sandstorms",
            "cloudy",
            "fog"
        ]
    )

    traffic = st.selectbox(
        "Traffic",
        [
            "low",
            "medium",
            "high",
            "jam"
        ]
    )


# =====================================================
# ORDER DETAILS
# =====================================================

with col2:

    vehicle_condition = st.selectbox(
        "Vehicle Condition",
        [0, 1, 2]
    )

    type_of_order = st.selectbox(
        "Type of Order",
        [
            "drinks",
            "buffet",
            "meal",
            "snack"
        ]
    )

    type_of_vehicle = st.selectbox(
        "Type of Vehicle",
        [
            "motorcycle",
            "scooter",
            "electric_scooter"
        ]
    )

    multiple_deliveries = st.selectbox(
        "Multiple Deliveries",
        [0, 1, 2, 3]
    )


# =====================================================
# OTHER DETAILS
# =====================================================

with col3:

    festival = st.selectbox(
        "Festival",
        [
            "no",
            "yes"
        ]
    )

    city_type = st.selectbox(
        "City Type",
        [
            "urban",
            "metropolitian",
            "semi-Urban"
        ]
    )

    city_name = st.selectbox(
        "City Name",
        [
            "AGR",
            "ALH",
            "AURG",
            "BANG",
            "BHP",
            "CHEN",
            "COIMB",
            "DEH",
            "GOA",
            "HYD",
            "INDO",
            "JAP",
            "KNP",
            "KOC",
            "KOL",
            "LUDH",
            "MUM",
            "MYS",
            "PUNE",
            "RANCHI",
            "SUR",
            "VAD"
        ]
    )

    distance = st.number_input(
        "Distance (km)",
        min_value=0.1,
        max_value=50.0,
        value=5.0,
        step=0.1
    )


st.divider()


# =====================================================
# TIME DETAILS
# =====================================================

st.subheader("🕒 Location & Time Details")

col4, col5, col6 = st.columns(3)


with col4:

    pickup_time_minutes = st.number_input(
        "Pickup Time (minutes)",
        min_value=0,
        max_value=60,
        value=10
    )

    order_time_hour = st.number_input(
        "Order Hour",
        min_value=0,
        max_value=23,
        value=13
    )


with col5:

    order_day = st.number_input(
        "Order Day",
        min_value=1,
        max_value=31,
        value=15
    )

    order_month = st.number_input(
        "Order Month",
        min_value=1,
        max_value=12,
        value=6
    )


with col6:

    order_day_of_week = st.selectbox(
        "Day of Week",
        [
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday"
        ]
    )

    is_weekend = st.selectbox(
        "Weekend?",
        [0, 1]
    )


order_time_of_day = st.selectbox(
    "Time of Day",
    [
        "morning",
        "afternoon",
        "evening",
        "night"
    ]
)


st.divider()


# =====================================================
# PREDICTION
# =====================================================

if st.button(
    "🚀 Predict Delivery Time",
    use_container_width=True
):

    input_data = pd.DataFrame({

        "age": [age],

        "ratings": [ratings],

        "weather": [weather],

        "traffic": [traffic],

        "vehicle_condition": [vehicle_condition],

        "type_of_order": [type_of_order],

        "type_of_vehicle": [type_of_vehicle],

        "multiple_deliveries": [multiple_deliveries],

        "festival": [festival],

        "city_type": [city_type],

        "city_name": [city_name],

        "order_day": [order_day],

        "order_month": [order_month],

        "order_day_of_week": [order_day_of_week],

        "is_weekend": [is_weekend],

        "pickup_time_minutes": [pickup_time_minutes],

        "order_time_hour": [order_time_hour],

        "order_time_of_day": [order_time_of_day],

        "distance": [distance]
    })


    # -----------------------------
    # Prediction
    # -----------------------------

    prediction = model.predict(input_data)

    predicted_time = float(prediction[0])


    # -----------------------------
    # Delivery Status
    # -----------------------------

    if predicted_time <= 30:

        status = "🟢 Fast Delivery"

    elif predicted_time <= 45:

        status = "🟡 Moderate Delivery"

    else:

        status = "🔴 Longer Delivery"


    # -----------------------------
    # Result
    # -----------------------------

    st.success(
        f"🍔 Estimated Delivery Time: "
        f"**{predicted_time:.0f} minutes**"
    )