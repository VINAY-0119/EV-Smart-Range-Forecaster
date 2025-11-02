# ⚡ EV Range Predictor 🚗

A professional **Streamlit web application** that predicts the **driving range of an electric vehicle (EV)** under different driving and environmental conditions such as speed, temperature, terrain, and weather.  
It provides real-time insights into battery performance and helps users understand how driving behavior affects efficiency.

---

## 🧭 Overview

The **EV Range Predictor** uses a trained **machine learning model** to estimate the *remaining State of Charge (SoC)* and *expected range (km)* of an electric vehicle.  
It allows users to input variables like speed, terrain, and weather to see how these affect range and battery life.

This tool is useful for:
- EV owners optimizing driving range  
- Researchers testing vehicle efficiency  
- Manufacturers simulating driving conditions  

---

## 🚀 Features

- **Real-time range prediction** using ML model (`ev_range_predictor_reduced.pkl`)
- **Interactive Streamlit dashboard** for easy input and live feedback
- **Professional UI design** with custom CSS and clean layout
- **Dynamic insights** on SoC, energy use, and driving range
- **Smart energy formula** that adapts to speed, terrain, and weather

---

## ⚙️ Installation & Running the App

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/ev-range-predictor.git
cd ev-range-predictor
Step 2: Install Dependencies
bash
Copy code
pip install streamlit pandas joblib
(Optional: Create a virtual environment before installing dependencies)

bash
Copy code
python -m venv venv
source venv/bin/activate  # On Mac/Linux
venv\Scripts\activate     # On Windows
pip install -r requirements.txt
Step 3: Run the Application
bash
Copy code
streamlit run app.py
Step 4: Open in Browser
arduino
Copy code
http://localhost:8501
🧮 How the App Works
The app loads a trained machine learning regression model stored as ev_range_predictor_reduced.pkl.

You input driving and environmental variables such as:

Speed (Km/h)

Temperature (°C)

Terrain (Flat / Hilly)

Weather (Normal, Hot, Cold, Rainy)

Acceleration / Braking

SoC and Previous SoC (%)

The model predicts the remaining State of Charge (SoC).

The app calculates estimated range (km) using a custom energy rate formula.

🔋 Energy Formula
python
Copy code
remaining_energy_kWh = (predicted_SoC / 100) * battery_capacity_kWh
predicted_range_km = remaining_energy_kWh / energy_rate
Where:

battery_capacity_kWh = 40 (default)

energy_rate changes with:

Speed

Terrain type (higher for hilly)

Weather condition (higher for hot)

🧠 Example Usage
Input Parameters
Parameter	Value
SoC	80%
Speed	60 km/h
Temperature	25°C
Terrain	Flat
Weather	Normal
Acceleration	1.0 m/s²
Braking	0.5 m/s²
Prev_SoC	85%

Model Output Example
Metric	Result
Predicted SoC	72.4 %
Estimated Range	193.1 km
Remaining Battery Energy	28.96 kWh
Energy Consumption Rate	0.15 kWh/km

Interpretation:
The model predicts your battery will have 72.4% charge left after your drive.

You can drive approximately 193 km before the battery is depleted.

Efficiency improves with lower speeds and flat terrain.

💡 Smart Driving Tips (Shown in App)
Maintain optimal tire pressure for better efficiency

Avoid harsh acceleration or braking

Preheat or precool your EV while charging

Use regenerative braking effectively

Plan routes that avoid steep inclines

Each app session displays one random smart driving tip.

🧾 Example Run (Step-by-Step)
1. Launch the App
Run:

bash
Copy code
streamlit run app.py
2. Open in Your Browser
You’ll see a clean dashboard with:

Left panel → EV insights & driving tips

Center panel → Input fields for model prediction

Right panel → Quick stats

3. Enter Example Values:
Input	Example
State of Charge (%)	80
Speed (Km/h)	60
Temperature (°C)	25
Terrain Type	Flat
Braking (m/s²)	0.5
Acceleration (m/s²)	1.0
Weather Condition	Normal
Previous SoC (%)	85

Click "🚀 Predict Range".

4. Output Example:
yaml
Copy code
Predicted SoC: 72.4%
Estimated Range: 193.1 km
Remaining Energy: 28.96 kWh
Energy Rate: 0.15 kWh/km
✅ You’ll also see metrics displayed in colored boxes on the dashboard.
