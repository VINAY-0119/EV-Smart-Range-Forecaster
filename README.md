# ⚡ EV Range Predictor 🚗

[![Streamlit](https://img.shields.io/badge/Framework-Streamlit-FF4B4B?logo=streamlit)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)](#)
[![Made with ❤️](https://img.shields.io/badge/Made_with-❤️_and_Python-blue.svg)](#)

A **Streamlit web application** that predicts the estimated **electric vehicle (EV) driving range** based on various environmental and driving parameters such as speed, temperature, terrain, and weather.  

This project helps EV owners, developers, and researchers analyze how different driving conditions affect range, efficiency, and energy consumption.

---

## 🌍 Live Demo

> Coming Soon — you can easily deploy this app using [Streamlit Cloud](https://streamlit.io/cloud) or host it on your own server.

---

## 🚀 Features

- ✅ **Real-time EV Range Prediction** using a trained ML model (`ev_range_predictor_reduced.pkl`)
- 🎛️ **Interactive Parameter Input** for:
  - Speed (Km/h)
  - Temperature (°C)
  - Terrain Type (Flat / Hilly)
  - Weather Condition (Normal / Hot / Cold / Rainy)
  - Braking & Acceleration
  - State of Charge (SoC) and Previous SoC
- 🎨 **Professional UI** with modern, responsive CSS
- 💡 **Dynamic Smart Driving Tips** to improve battery efficiency
- 📊 **Performance Metrics Display:**
  - Predicted SoC (%)
  - Estimated Range (km)
  - Remaining Battery Energy (kWh)
  - Energy Consumption Rate (kWh/km)

---

## 🧩 Requirements

Install dependencies before running:

```bash
pip install streamlit pandas joblib
📦 Project Structure
bash
Copy code
EV-Range-Predictor/
│
├── ev_range_predictor_reduced.pkl     # Trained machine learning model
├── app.py                             # Streamlit main application file
└── README.md                          # Documentation file
▶️ How to Run the App
Follow these steps to run the app locally:

Clone this repository or download it:

bash
Copy code
git clone https://github.com/yourusername/ev-range-predictor.git
cd ev-range-predictor
Place your trained model file (ev_range_predictor_reduced.pkl) in the same directory as app.py.

Run the Streamlit app:

bash
Copy code
streamlit run app.py
Open your browser and go to:

arduino
Copy code
http://localhost:8501
That’s it — your EV Predictor will be up and running 🚗💨

⚙️ How It Works
Loads a pre-trained regression model using Joblib.

Captures user inputs through the Streamlit interface.

Converts inputs to a Pandas DataFrame.

Uses the model to predict remaining State of Charge (SoC).

Calculates estimated driving range and energy efficiency based on a dynamic consumption rate.

Displays easy-to-read metrics and tips.

📊 Example Calculation
If your EV has:

SoC: 80%

Speed: 60 km/h

Terrain: Flat

Temperature: 25°C

Then the model computes:

python
Copy code
remaining_energy_kWh = (predicted_SoC / 100) * battery_capacity_kwh
predicted_range_km = remaining_energy_kWh / energy_rate
Where energy_rate depends on:

Speed (higher speed = higher consumption)

Terrain (hilly = +20% energy usage)

Weather (hot/cold increases energy draw)

💡 Smart Driving Tips (shown in the app)
✅ Keep tire pressure optimal to maximize efficiency

🚦 Avoid harsh acceleration for better range

❄️ Preheat or precool your EV while charging

🔋 Use regenerative braking in traffic

🗺️ Plan routes that avoid steep inclines

These are randomized each time for variety.

🧠 Best Practices
Use realistic input values (e.g., 40–100% SoC, 20–120 km/h).

Avoid extreme combinations unless you’re testing edge cases.

Make sure the .pkl model file is in the same folder as app.py.

For production use, deploy via Streamlit Cloud, Heroku, or Docker.

🛠️ Customization Options
You can easily modify the app for your needs:

🎨 Change the design: Edit the CSS section inside app.py.

⚙️ Replace the model: Retrain and export your own .pkl file.

🔋 Adjust the battery specs: Change battery_capacity_kwh in the script.

📈 Add new inputs: Include parameters like wind, payload, tire type, or road gradient.

📈 Key Metrics Displayed
Metric	Description
Predicted SoC (%)	Battery charge after driving conditions
Estimated Range (km)	Distance the EV can travel
Remaining Energy (kWh)	Battery energy left after usage
Energy Rate (kWh/km)	Consumption rate based on terrain and weather
