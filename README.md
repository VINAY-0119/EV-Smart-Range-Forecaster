# ⚡ EV Range Predictor 🚗

[![Streamlit](https://img.shields.io/badge/Framework-Streamlit-FF4B4B?logo=streamlit)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)](#)

---

## 🧭 Overview

**EV Range Predictor** is a modern **Streamlit web application** that predicts the **driving range of an electric vehicle (EV)** based on environmental and driving conditions such as:

- Speed  
- Temperature  
- Terrain Type  
- Weather Conditions  
- Acceleration / Braking  
- State of Charge (SoC)

It helps users estimate real-world range and understand how conditions impact battery efficiency and performance.

---

## 🚀 Features

### 🧠 Smart Predictions
- Uses a trained **machine learning model** (`ev_range_predictor_reduced.pkl`)
- Calculates both **Predicted SoC (%)** and **Estimated Range (km)**

### 🎛️ Interactive Parameters
Adjust key inputs in real-time:
- Speed (Km/h)  
- Temperature (°C)  
- Terrain (Flat / Hilly)  
- Weather (Normal / Hot / Cold / Rainy)  
- Acceleration & Braking  
- State of Charge (SoC) and Previous SoC  

### 📊 Detailed Output
Displays:
- Predicted SoC  
- Estimated Range  
- Remaining Battery Energy (kWh)  
- Energy Consumption Rate (kWh/km)

### 🎨 Modern Design
- Professional and responsive UI using **custom CSS**
- Minimal, clean layout optimized for all devices

---

## 🧩 Requirements

Install the necessary dependencies before running the app:

```bash
pip install streamlit pandas joblib
