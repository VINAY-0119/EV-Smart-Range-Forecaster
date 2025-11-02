import streamlit as st
import pandas as pd
import joblib
import time
import random
import plotly.graph_objects as go

# ---------------------------------------------------------
# APP CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="EV Range Predictor",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# LOAD MODEL
# ---------------------------------------------------------
@st.cache_resource
def load_model():
    return joblib.load("ev_range_predictor_reduced.pkl")

model = load_model()

# ---------------------------------------------------------
# STYLING (CLEAN, MODERN, PROFESSIONAL)
# ---------------------------------------------------------
st.markdown("""
<style>
    .main {
        background-color: #FFFFFF;
        color: #111827;
        font-family: 'Inter', sans-serif;
    }

    .hero {
        text-align: center;
        background: linear-gradient(90deg, #E0F2FE, #F8FAFC);
        padding: 35px 15px;
        border-radius: 12px;
        margin-bottom: 40px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.08);
    }

    .hero-title {
        font-size: 42px;
        font-weight: 800;
        color: #0F172A;
        letter-spacing: 0.5px;
        margin-bottom: 10px;
    }

    .hero-subtitle {
        font-size: 16px;
        color: #475569;
        font-weight: 400;
        max-width: 650px;
        margin: 0 auto;
    }

    .section-title {
        font-size: 18px;
        font-weight: 600;
        color: #1E293B;
        margin-top: 10px;
        margin-bottom: 10px;
    }

    .stButton>button {
        background-color: #2563EB;
        color: #FFFFFF;
        border-radius: 6px;
        font-weight: 600;
        border: none;
        padding: 0.6rem 1.4rem;
        transition: background 0.2s ease, transform 0.15s ease;
    }

    .stButton>button:hover {
        background-color: #1E40AF;
        transform: scale(1.02);
    }

    .footer {
        text-align: center;
        font-size: 12px;
        margin-top: 50px;
        color: #6B7280;
    }

    [data-testid='stSidebar'] {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# HERO SECTION
# ---------------------------------------------------------
st.markdown("""
<div class="hero">
    <div class="hero-title">⚡ EV Vehicle Range Predictor 🚗</div>
    <div class="hero-subtitle">
        Estimate your electric vehicle's driving range instantly.  
        Adjust speed, terrain, and weather to see how they affect performance and battery life.
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# LAYOUT: 3 COLUMNS
# ---------------------------------------------------------
col1, col2, col3 = st.columns([1.2, 2.3, 1.2])

# LEFT PANEL – EV INSIGHTS
with col1:
    st.markdown("<div class='section-title'>⚙️ EV Insights</div>", unsafe_allow_html=True)
    st.markdown("""
    - Typical Battery Capacity: **40–75 kWh**  
    - Average Driving Range: **300–500 km**  
    - Charging Time: **30–60 minutes**  
    - Optimal Temperature: **20–25°C**  
    - Efficiency improves with **moderate speeds**
    """)

    st.markdown("<div class='section-title'>💡 Smart Driving Tip</div>", unsafe_allow_html=True)
    tips = [
        "Keep tire pressure optimal to maximize efficiency.",
        "Avoid harsh acceleration for longer range.",
        "Preheat or precool your EV while charging.",
        "Use regenerative braking effectively in traffic.",
        "Plan routes that avoid steep inclines."
    ]
    st.markdown(f"✅ {random.choice(tips)}")

# CENTER PANEL – MAIN PREDICTION FORM
with col2:
    st.markdown("<div class='section-title'>🧩 Input Parameters</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        SoC = st.number_input("State of Charge (%)", 0.0, 100.0, 80.0)
        Speed = st.number_input("Speed (Km/h)", 0.0, 200.0, 60.0)
        Temperature = st.number_input("Temperature (°C)", -20.0, 60.0, 25.0)
        Terrain = st.selectbox("Terrain Type", ["Flat", "Hilly"])
    with c2:
        Braking = st.number_input("Braking (m/s²)", 0.0, 10.0, 0.5)
        Acceleration = st.number_input("Acceleration (m/s²)", 0.0, 10.0, 1.0)
        Weather = st.selectbox("Weather Condition", ["Normal", "Hot", "Cold", "Rainy"])
        Prev_SoC = st.number_input("Previous SoC (%)", 0.0, 100.0, 85.0)

    battery_capacity_kwh = st.slider("Battery Capacity (kWh)", 30, 120, 60)

    st.markdown("<br>", unsafe_allow_html=True)
    predict_btn = st.button("🚀 Predict Range")

    if predict_btn:
        # Prepare input safely
        input_data = pd.DataFrame([{
            "SoC": SoC,
            "Speed (Km/h)": Speed,
            "Temperature": Temperature,
            "Terrain": Terrain,
            "Braking (m/s²)": Braking,
            "Acceleration (m/s²)": Acceleration,
            "Weather": Weather,
            "Prev_SoC": Prev_SoC
        }])

        # Encode categorical variables if needed
        encoded_data = input_data.copy()
        encoded_data["Terrain"] = encoded_data["Terrain"].map({"Flat": 0, "Hilly": 1})
        encoded_data["Weather"] = encoded_data["Weather"].map({"Normal": 0, "Hot": 1, "Cold": 2, "Rainy": 3})

        with st.spinner("Calculating optimal range..."):
            progress = st.progress(0)
            for i in range(100):
                time.sleep(0.005)
                progress.progress(i + 1)

            try:
                predicted_SoC = float(model.predict(encoded_data)[0])
            except Exception as e:
                st.error(f"Prediction failed: {e}")
                st.stop()

            def energy_rate(speed, terrain, weather):
                rate = 0.15
                if speed <= 50:
                    rate = 0.12
                elif speed > 80:
                    rate = 0.18
                if terrain == "Hilly":
                    rate *= 1.2
                if weather == "Hot":
                    rate *= 1.1
                return rate

            rate = energy_rate(Speed, Terrain, Weather)
            remaining_energy_kwh = (predicted_SoC / 100) * battery_capacity_kwh
            predicted_range_km = remaining_energy_kwh / rate

        # ---------------------------------------------------------
        # DISPLAY RESULTS
        # ---------------------------------------------------------
        st.markdown("<div class='section-title'>📊 Prediction Results</div>", unsafe_allow_html=True)
        colA, colB = st.columns(2)
        with colA:
            st.metric("Predicted SoC (%)", f"{predicted_SoC:.2f}")
        with colB:
            st.metric("Estimated Range (km)", f"{predicted_range_km:.1f}")

        st.markdown(f"""
        **Remaining Battery Energy:** {remaining_energy_kwh:.2f} kWh  
        **Energy Consumption Rate:** {rate:.3f} kWh/km
        """)
        st.success("✅ Prediction complete! Check metrics above.")

        # Optional Gauge Visualization
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=predicted_SoC,
            title={'text': "Predicted SoC (%)"},
            gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "#2563EB"}}
        ))
        st.plotly_chart(fig, use_container_width=True)

# RIGHT PANEL – QUICK STATS
with col3:
    st.markdown("<div class='section-title'>📈 Quick Stats</div>", unsafe_allow_html=True)
    st.markdown("""
    - **Energy Efficiency:** 91%  
    - **Charging Infrastructure:** 82% coverage  
    - **Top Efficient Models:** Model 3, Kona, Leaf  
    - **Avg User Range:** 412 km  
    """)

# FOOTER
st.markdown("<div class='footer'>© 2025 EV Predictor | Powered by Streamlit</div>", unsafe_allow_html=True)

