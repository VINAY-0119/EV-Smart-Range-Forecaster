import streamlit as st
import pandas as pd
import joblib
import time
import random

# --- App Configuration ---
st.set_page_config(
    page_title="EV Range Predictor",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

@st.cache_resource
def load_model():
    return joblib.load("ev_range_predictor_reduced.pkl")

model = load_model()

# --- Professional Modern CSS (No Blocks, Clean Layout) ---
st.markdown("""
<style>
    /* Global */
    .main {
        background-color: #FFFFFF;
        color: #111827;
        font-family: 'Inter', sans-serif;
    }

    /* Hero Header */
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

    /* Section Titles */
    .section-title {
        font-size: 18px;
        font-weight: 600;
        color: #1E293B;
        margin-top: 10px;
        margin-bottom: 10px;
    }

    /* Button */
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

    /* Footer */
    .footer {
        text-align: center;
        font-size: 12px;
        margin-top: 50px;
        color: #6B7280;
    }
</style>
""", unsafe_allow_html=True)

# --- Hero Section ---
st.markdown("""
<div class="hero">
    <div class="hero-title">⚡ EV Vehicle Range Predictor 🚗</div>
    <div class="hero-subtitle">
        Estimate your electric vehicle's driving range instantly.  
        Adjust speed, terrain, and weather to see how they affect performance and battery life.
    </div>
</div>
""", unsafe_allow_html=True)

# --- Layout ---
col1, col2, col3 = st.columns([1.2, 2.3, 1.2])

# LEFT PANEL – EV Insights
with col1:
    st.markdown("<div class='section-title'>⚙️ EV Insights</div>", unsafe_allow_html=True)
    st.markdown("""
    - Typical Battery Capacity: **40–75 kWh**  
    - Average Driving Range: **300–500 km**  
    - Charging Time: **30–60 minutes**  
    - Optimal Temperature: **20–25°C**  
    - Efficiency improves with **moderate speeds**
    """)

    # --- Smart Driving Tips Section (Enhanced) ---
    st.markdown("<div class='section-title'>💡 Smart Driving Tip</div>", unsafe_allow_html=True)

    tips = [
        # Efficiency
        "Maintain steady speeds — avoid aggressive acceleration and braking.",
        "Use Eco or Efficiency mode during highway drives to reduce consumption.",
        "Turn off climate control when not needed; it can drain up to 15% of range.",
        "Avoid idling with AC or heater on when parked — it consumes battery power.",
        "Plan routes with minimal elevation gain to reduce energy usage.",
        "Keep windows closed at high speeds to minimize drag.",
        "Remove roof racks or cargo boxes when not in use to improve aerodynamics.",

        # Battery Health
        "Avoid charging to 100% or discharging below 20% regularly.",
        "Use fast charging sparingly; it can shorten long-term battery life.",
        "If storing your EV for weeks, keep battery around 50–60%.",
        "Precondition the battery before charging in cold conditions.",
        "Charge during cooler hours to reduce thermal stress on the battery.",
        "Don’t leave your EV parked in direct sunlight for extended periods.",

        # Driving & Terrain
        "Use regenerative braking in city driving to recover lost energy.",
        "On steep downhill routes, let regen braking slow you naturally.",
        "When climbing hills, maintain moderate speed to save energy.",
        "Avoid sudden lane changes or jerky movements — they waste power.",

        # Tire & Maintenance
        "Check tire pressure monthly — low pressure increases rolling resistance.",
        "Use low-resistance tires if available for your model.",
        "Wheel alignment and balanced tires improve efficiency and comfort.",
        "Keep brakes serviced; regenerative systems work best with clean pads.",

        # Climate & Weather
        "Preheat or precool your cabin while the EV is plugged in.",
        "Use seat warmers instead of cabin heating to conserve energy.",
        "Keep defrosters off when not needed — they draw noticeable power.",
        "Cold weather can reduce range by up to 30%; drive gently in winter.",
        "In hot weather, park in shade to prevent battery overheating.",

        # Charging & Planning
        "Plan long trips with charging stations mapped ahead of time.",
        "Use smart charging timers to take advantage of off-peak electricity rates.",
        "Charge little and often instead of running battery low.",
        "Keep your home charger clean and properly ventilated.",
        "Monitor your battery health using your EV’s companion app.",

        # Advanced habits
        "Use cruise control on highways for consistent energy use.",
        "Avoid unnecessary accessories that consume 12V power.",
        "Keep your EV software updated — updates often improve efficiency."
    ]

    if "tip_index" not in st.session_state:
        st.session_state.tip_index = random.randint(0, len(tips)-1)
        st.session_state.last_update = time.time()

    if time.time() - st.session_state.last_update > 10:
        st.session_state.tip_index = (st.session_state.tip_index + 1) % len(tips)
        st.session_state.last_update = time.time()
        st.experimental_rerun()

    current_tip = tips[st.session_state.tip_index]
    st.markdown(f"""
    <div style='background:#EFF6FF; padding:14px 18px; border-radius:10px; box-shadow:0 1px 4px rgba(0,0,0,0.06);'>
        <p style='color:#1E3A8A; font-weight:600; font-size:16px; margin-bottom:6px;'>✅ Smart Tip</p>
        <p style='color:#1E293B; font-size:15px; margin:0;'>{current_tip}</p>
    </div>
    """, unsafe_allow_html=True)

# CENTER PANEL – Main Prediction Form
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

    st.markdown("<br>", unsafe_allow_html=True)
    predict_btn = st.button("🚀 Predict Range")

    if predict_btn:
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

        with st.spinner("Calculating optimal range..."):
            time.sleep(1)
            predicted_SoC = model.predict(input_data)[0]

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
            battery_capacity_kwh = 40
            remaining_energy_kwh = (predicted_SoC / 100) * battery_capacity_kwh
            predicted_range_km = remaining_energy_kwh / rate

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

# RIGHT PANEL – Quick Stats
with col3:
    st.markdown("<div class='section-title'>📈 Quick Stats</div>", unsafe_allow_html=True)
    st.markdown("""
    - **Energy Efficiency:** 91%  
    - **Charging Infrastructure:** 82% coverage  
    - **Top Efficient Models:** Model 3, Kona, Leaf  
    - **Avg User Range:** 412 km  
    """)

# --- Footer ---
st.markdown("<div class='footer'>© 2025 AutoRange Technologies | Precision EV Range Intelligence</div>", unsafe_allow_html=True)
