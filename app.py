import streamlit as st
import pandas as pd
import joblib
import random
import time

st.set_page_config(
    page_title="EV Range Prediction App",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

@st.cache_resource
def load_model():
    return joblib.load('ev_range_predictor_reduced.pkl')

model = load_model()

# --- Professional Modern CSS ---
st.markdown("""
<style>
    :root {
        --primary: #2563eb;
        --secondary: #1e293b;
        --bg-light: #f8fafc;
        --text-dark: #0f172a;
        --text-light: #e2e8f0;
    }

    @media (prefers-color-scheme: dark) {
        .main {
            background: linear-gradient(180deg, #0f172a, #1e293b);
            color: var(--text-light);
        }
        .card {
            background: rgba(30, 41, 59, 0.9);
            border: 1px solid rgba(255, 255, 255, 0.08);
        }
    }

    @media (prefers-color-scheme: light) {
        .main {
            background: linear-gradient(180deg, #f9fafb, #e2e8f0);
            color: var(--text-dark);
        }
        .card {
            background: white;
            border: 1px solid #e2e8f0;
        }
    }

    .header {
        text-align: center;
        padding: 1.5rem;
        font-size: 30px;
        font-weight: 800;
        color: var(--primary);
        margin-bottom: 20px;
    }

    .card {
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 18px rgba(0,0,0,0.12);
    }

    .section-title {
        font-weight: 700;
        color: var(--primary);
        font-size: 18px;
        margin-bottom: 12px;
    }

    .stButton>button {
        background: var(--primary);
        color: white;
        border-radius: 10px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        border: none;
        transition: all 0.2s ease;
    }

    .stButton>button:hover {
        background: #1e40af;
        transform: scale(1.03);
    }

    .prediction-box {
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        margin-top: 10px;
    }

    .charging-bar-container {
        width: 100%;
        height: 20px;
        background-color: rgba(255,255,255,0.1);
        border-radius: 10px;
        overflow: hidden;
        margin-top: 10px;
    }

    .charging-bar {
        height: 100%;
        background: var(--primary);
        width: 0%;
        border-radius: 10px;
        animation: fill 2s forwards;
    }

    @keyframes fill {
        from { width: 0%; }
        to { width: 100%; }
    }

    .footer {
        text-align: center;
        font-size: 13px;
        margin-top: 40px;
        opacity: 0.7;
    }
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("<div class='header'>EV Range Prediction Dashboard</div>", unsafe_allow_html=True)

# --- Layout: Left | Center | Right ---
col_left, col_center, col_right = st.columns([1.3, 2.2, 1.3])

# LEFT COLUMN – Insights
with col_left:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>⚙️ Vehicle Insights</div>", unsafe_allow_html=True)
    st.markdown("""
    - **Battery Capacity:** 40–75 kWh  
    - **Avg Range:** 300–500 km  
    - **Charging Time:** 30–60 mins  
    - **Optimal Temp:** 20–25°C  
    - **Max Speed:** 200 km/h  
    """)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='card' style='margin-top:20px;'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>📊 System Info</div>", unsafe_allow_html=True)
    st.markdown("""
    - **Model Version:** v1.2.0  
    - **ML Framework:** Scikit-Learn  
    - **Update Cycle:** Weekly  
    - **Developer:** AutoRange Labs  
    """)
    st.markdown("</div>", unsafe_allow_html=True)

# CENTER COLUMN – Main Functionality
with col_center:
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

    st.markdown("---")
    predict_btn = st.button("Predict Range")

    if predict_btn:
        input_data = pd.DataFrame([{
            'SoC': SoC,
            'Speed (Km/h)': Speed,
            'Temperature': Temperature,
            'Terrain': Terrain,
            'Braking (m/s²)': Braking,
            'Acceleration (m/s²)': Acceleration,
            'Weather': Weather,
            'Prev_SoC': Prev_SoC
        }])

        with st.spinner("Calculating range..."):
            time.sleep(1)
            predicted_SoC = model.predict(input_data)[0]

            def energy_rate(speed, terrain, weather):
                rate = 0.15
                if speed <= 50:
                    rate = 0.12
                elif speed > 80:
                    rate = 0.18
                if terrain == 'Hilly':
                    rate *= 1.2
                if weather == 'Hot':
                    rate *= 1.1
                return rate

            battery_capacity_kwh = 40
            rate = energy_rate(Speed, Terrain, Weather)
            remaining_energy_kwh = (predicted_SoC / 100) * battery_capacity_kwh
            predicted_range_km = remaining_energy_kwh / rate

        st.markdown("<div class='section-title'>📈 Prediction Results</div>", unsafe_allow_html=True)
        st.markdown("<div class='prediction-box'>", unsafe_allow_html=True)
        cA, cB = st.columns(2)
        cA.metric("Predicted SoC (%)", f"{predicted_SoC:.2f}")
        cB.metric("Estimated Range (km)", f"{predicted_range_km:.1f}")

        st.markdown("<div class='charging-bar-container'><div class='charging-bar'></div></div>", unsafe_allow_html=True)
        st.markdown(
            f"**Remaining Energy:** {remaining_energy_kwh:.2f} kWh  \n"
            f"**Consumption Rate:** {rate:.3f} kWh/km"
        )
        st.markdown("</div>", unsafe_allow_html=True)
        st.success("Prediction complete!")

# RIGHT COLUMN – Driving Tips
with col_right:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>💡 Efficiency Tips</div>", unsafe_allow_html=True)
    tips = [
        "Keep tires inflated for optimal range.",
        "Use gentle acceleration and braking.",
        "Plan routes with minimal elevation changes.",
        "Preheat or cool your EV while charging.",
        "Avoid high speeds for better efficiency."
    ]
    st.write(f"👉 {random.choice(tips)}")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
st.markdown("<div class='footer'>© 2025 AutoRange Labs | EV Range Prediction Suite</div>", unsafe_allow_html=True)
