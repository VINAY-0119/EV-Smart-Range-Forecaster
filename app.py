import streamlit as st
import pandas as pd
import joblib
import time
from google.ai import generativelanguage as glm

# --- PATCH sklearn _RemainderColsList ISSUE ---
import sklearn.compose._column_transformer as ctf
if not hasattr(ctf, '_RemainderColsList'):
    class _RemainderColsList(list):
        pass
    ctf._RemainderColsList = _RemainderColsList

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="EV Range Predictor",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- LOAD ML MODEL ---
@st.cache_resource
def load_model():
    try:
        model = joblib.load("ev_range_predictor_reduced.pkl")
        return model
    except FileNotFoundError:
        st.error("❌ Model file not found. Please upload 'ev_range_predictor_reduced.pkl'.")
        return None
    except Exception as e:
        st.error(f"❌ Error loading model: {type(e).__name__} - {e}")
        return None

model = load_model()

# --- HELPER FUNCTION FOR ENERGY RATE ---
def energy_rate(speed, terrain, weather, braking, acceleration):
    rate = 0.15
    if speed <= 50: rate = 0.12
    elif speed > 80: rate = 0.18
    if terrain == "Hilly": rate *= 1.2
    if weather == "Hot": rate *= 1.1
    if weather == "Cold": rate *= 1.15
    rate *= 1 + 0.05 * braking + 0.07 * acceleration
    return rate

# --- SETUP GOOGLE GENERATIVE LANGUAGE CLIENT ---
google_api_available = False
google_client = None

if "google" in st.secrets and "api_key" in st.secrets["google"]:
    try:
        google_client = glm.TextServiceClient(
            client_options={"api_key": st.secrets["google"]["api_key"]}
        )
        google_api_available = True
    except Exception as e:
        st.warning(f"⚠️ Google Generative Language API client init error: {type(e).__name__} - {e}")
else:
    st.warning("⚠️ Google Generative Language API key not found in secrets. Chatbot disabled.")

def google_generate_text(prompt_text, model_name="models/gemini-1"):
    if not google_api_available:
        return "⚠️ Google API key not configured."
    try:
        request = glm.GenerateTextRequest(
            model=model_name,
            prompt=glm.TextPrompt(text=prompt_text),
            temperature=0.7,
            max_output_tokens=300
        )
        response = google_client.generate_text(request=request)
        return response.candidates[0].output
    except Exception as e:
        return f"⚠️ Google API error: {type(e).__name__} - {e}"

# --- PAGE CONTENT ---
st.title("⚡ EV Vehicle Range Predictor 🚗")

# Input section
with st.form("input_form"):
    SoC = st.number_input("State of Charge (%)", 0.0, 100.0, 80.0, step=1.0)
    Speed = st.number_input("Speed (Km/h)", 0.0, 200.0, 60.0, step=1.0)
    Temperature = st.number_input("Temperature (°C)", -20.0, 60.0, 25.0, step=0.1)
    Terrain = st.selectbox("Terrain Type", ["Flat", "Hilly"])
    Braking = st.number_input("Braking (m/s²)", 0.0, 10.0, 0.5, step=0.1)
    Acceleration = st.number_input("Acceleration (m/s²)", 0.0, 10.0, 1.0, step=0.1)
    Weather = st.selectbox("Weather Condition", ["Normal", "Hot", "Cold", "Rainy"])
    Prev_SoC = st.number_input("Previous SoC (%)", 0.0, 100.0, 85.0, step=1.0)

    submitted = st.form_submit_button("🚀 Predict Range")

if submitted:
    if model is None:
        st.error("Model not loaded. Cannot predict.")
    else:
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
            try:
                predicted_SoC = model.predict(input_data)[0]
                rate = energy_rate(Speed, Terrain, Weather, Braking, Acceleration)
                battery_capacity_kwh = 40
                remaining_energy_kwh = (predicted_SoC / 100) * battery_capacity_kwh
                predicted_range_km = remaining_energy_kwh / rate

                st.subheader("📊 Prediction Results")
                st.metric("Predicted SoC (%)", f"{predicted_SoC:.2f}")
                st.metric("Estimated Range (km)", f"{predicted_range_km:.1f}")
                st.write(f"Remaining Battery Energy: {remaining_energy_kwh:.2f} kWh")
                st.write(f"Energy Consumption Rate: {rate:.3f} kWh/km")
                st.success("✅ Prediction complete!")
            except Exception as e:
                st.error(f"Error during prediction: {type(e).__name__} - {e}")

# --- CHATBOT SECTION ---
st.markdown("---")
st.header("🤖 EV Chat Assistant (Google Gemini)")

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []
if "processing" not in st.session_state:
    st.session_state.processing = False

for msg in st.session_state.chat_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Ask me about EV range, efficiency, or anything EV-related...", disabled=st.session_state.processing)

if prompt:
    st.session_state.processing = True
    st.session_state.chat_messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Thinking..."):
        ai_text = google_generate_text(prompt)

    with st.chat_message("assistant"):
        st.markdown(ai_text)

    st.session_state.chat_messages.append({"role": "assistant", "content": ai_text})
    st.session_state.processing = False

# --- FOOTER ---
st.markdown("<hr><center>© 2025 EV Predictor | Powered by Streamlit + Google Gemini</center>", unsafe_allow_html=True)
