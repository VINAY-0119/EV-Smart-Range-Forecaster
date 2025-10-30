# EV Range Prediction - Full Project

This repository contains a complete end-to-end project for predicting electric vehicle (EV) driving range from vehicle specs.

## Structure
- `model_utils.py` - helper functions to build pipelines, train, save, load, and predict.
- `train.py` - script to train a final Gradient Boosting model from `EV_cars.csv` and save as a joblib file.
- `api.py` - FastAPI backend that exposes `/predict` endpoint.
- `streamlit_app.py` - Streamlit frontend for interactive input and prediction.
- `requirements.txt` - Python dependencies.

## Quickstart (local)
1. Create virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # or .venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```
2. Place your dataset `EV_cars.csv` in the project root (same folder as `train.py`)
3. Train model:
   ```bash
   python train.py --csv EV_cars.csv --out ev_range_model.joblib
   ```
4. Run API server (optional):
   ```bash
   # uses ev_range_model.joblib in CWD
   python api.py
   # server runs at http://0.0.0.0:8000
   ```
5. Run Streamlit frontend:
   ```bash
   streamlit run streamlit_app.py
   ```

## Notes
- The training script auto-detects a target column (e.g., `Range`) and picks up to 12 sensible features automatically.
- The Streamlit app can either call the FastAPI `/predict` endpoint or use the local model directly.
- For production, consider containerizing with Docker and adding authentication & input validation.
