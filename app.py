import streamlit as st
import pandas as pd
import joblib

# Page configuration
st.set_page_config(
    page_title="EV Range Prediction App",
    page_icon="🚗",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Load model with caching
@st.cache_resource
def load_model():
    return joblib.load('ev_range_predictor_reduced.pkl')

model = load_model()

# Custom CSS for cleaner UI
st.markdown("""
    <style>
        .main {
            background-color: #F9FAFB;
        }
        .stTextInput>div>div>input, .stNumberInput>div>div>input {
            border-radius: 8px;
        }
        .stButton>button {
            background-color: #2563EB;
            color: white;
            border-radius: 10px;
            padding: 0.6rem 1rem;
            font-weight: 600;
        }
        .stButton>button:hover {
            background-color: #1E40AF;
            color: white;
        }
        .stSelectbox>div>div>div {
            border-radius: 8px;
        }
        .prediction-box {
            background-color: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        }
        .section-title {
            color: #1E3A8A;
            font-weight: 600;
            font-size: 18px;
            margin-bottom: 10px;
        }
        .ev-card {
            background-color: white;
            padding: 10px;
            border-radius: 15px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.08);
            text-align: center;
        }
        .ev-card img {
            border-radius: 12px;
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("🚗 EV Range Prediction App")
st.caption("Estimate your electric vehicle's range based on driving and environmental conditions.")

# --- EV Showcase Section ---
st.markdown("<div class='section-title'>⚡ Featured Electric Vehicles</div>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("<div class='ev-card'><img src='https://cdn.motor1.com/images/mgl/xZ8k0/s1/tesla-model-3.jpg' width='100%'><p><b>Tesla Model 3</b></p></div>", unsafe_allow_html=True)
with col2:
    st.markdown("<div class='ev-card'><img src='https://cdn.motor1.com/images/mgl/YZ4qB/s1/hyundai-ioniq-5.jpg' width='100%'><p><b>Hyundai Ioniq 5</b></p></div>", unsafe_allow_html=True)
with col3:
    st.markdown("<div class='ev-card'><img src='https://cdn.motor1.com/images/mgl/Vm0Z1/s1/nissan-leaf.jpg' width='100%'><p><b>Nissan Leaf</b></p></div>", unsafe_allow_html=True)

# --- Input Section ---
st.markdown("<div class='section-title'>🔧 Input Parameters</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    SoC = st.number_input("State of Charge (SoC) (%)", min_value=0.0, max_value=100.0, value=80.0)
    Speed = st.number_input("Speed (Km/h)", min_value=0.0, max_value=200.0, value=60.0)
    Temperature = st.number_input("Temperature (°C)", min_value=-20.0, max_value=60.0, value=25.0)
    Terrain = st.selectbox("Terrain Type", options=["Flat", "Hilly"])
with col2:
    Braking = st.number_input("Braking (m/s²)", min_value=0.0, max_value=10.0, value=0.5)
    Acceleration = st.number_input("Acceleration (m/s²)", min_value=0.0, max_value=10.0, value=1.0)
    Weather = st.selectbox("Weather Condition", options=["Normal", "Hot", "Cold", "Rainy"])
    Prev_SoC = st.number_input("Previous SoC (%)", min_value=0.0, max_value=100.0, value=85.0)

# --- Dynamic EV Image ---
st.markdown("<div class='section-title'>🚙 Driving Scenario</div>", unsafe_allow_html=True)

if Terrain == "Hilly":
    st.image("https://cdn.motor1.com/images/mgl/jjjjW/s1/tesla-model-y-mountain.jpg", caption="EV on Hilly Terrain", use_container_width=True)
elif Weather == "Rainy":
    st.image("https://cdn.motor1.com/images/mgl/OO7op/s1/tesla-model-3-rain.jpg", caption="EV in Rainy Weather", use_container_width=True)
elif Weather == "Hot":
    st.image("https://cdn.motor1.com/images/mgl/vmmZr/s1/ev-sunny-highway.jpg", caption="EV on Sunny Road", use_container_width=True)
else:
    st.image("https://cdn.motor1.com/images/mgl/xZ8k0/s1/tesla-model-3.jpg", caption="EV on Normal Terrain", use_container_width=True)

# --- Prediction Section ---
st.markdown("---")
predict_btn = st.button("🔮 Predict Range")

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

    predicted_SoC = model.predict(input_data)[0]

    # Dynamic energy rate function
    def dynamic_energy_consumption_rate(speed_kmh, terrain, weather):
        rate = 0.15
        if speed_kmh <= 50:
            rate = 0.12
        elif speed_kmh > 80:
            rate = 0.18
        if terrain == 'Hilly':
            rate *= 1.2
        if weather == 'Hot':
            rate *= 1.1
        return rate

    battery_capacity_kwh = 40  # Example battery capacity
    rate = dynamic_energy_consumption_rate(Speed, Terrain, Weather)
    remaining_energy_kwh = (predicted_SoC / 100) * battery_capacity_kwh
    predicted_range_km = remaining_energy_kwh / rate

    # Results display
    st.markdown("<div class='section-title'>📊 Prediction Results</div>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='prediction-box'>", unsafe_allow_html=True)
        colA, colB = st.columns(2)
        colA.metric(label="Predicted SoC (%)", value=f"{predicted_SoC:.2f}")
        colB.metric(label="Estimated Range (km)", value=f"{predicted_range_km:.2f}")

        st.progress(predicted_SoC / 100)
        st.markdown(
            f"🔋 **Remaining Battery Energy:** {remaining_energy_kwh:.2f} kWh  \n"
            f"⚙️ **Energy Consumption Rate:** {rate:.3f} kWh/km"
        )
        st.markdown("</div>", unsafe_allow_html=True)

    st.success("✅ Prediction complete! Scroll above to review the results.")

# --- Footer ---
st.markdown("---")
st.caption("Built with ❤️ using Streamlit & Machine Learning")
