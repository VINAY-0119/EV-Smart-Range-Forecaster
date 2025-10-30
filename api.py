from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from model_utils import load_model, predict_from_dict
import os

MODEL_PATH = os.environ.get('EV_MODEL_PATH', 'ev_range_model.joblib')
model_data = None
try:
    model_data = load_model(MODEL_PATH)
except Exception as e:
    print('Warning: could not load model at startup:', e)

app = FastAPI(title='EV Range Prediction API')

class PredictRequest(BaseModel):
    # flexible payload: accept any keys
    __root__: dict

@app.get('/health')
def health():
    return {'status': 'ok', 'model_loaded': model_data is not None, 'model_path': MODEL_PATH}

@app.post('/predict')
def predict(req: PredictRequest):
    if model_data is None:
        raise HTTPException(status_code=503, detail='Model not loaded')
    payload = req.__root__
    try:
        pred = predict_from_dict(model_data, payload)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {'prediction': pred}

if __name__ == '__main__':
    uvicorn.run('api:app', host='0.0.0.0', port=8000, reload=True)
