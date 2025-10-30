import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
import joblib
from typing import Tuple, List

def infer_target_column(df: pd.DataFrame) -> str:
    candidates = [c for c in df.columns if c.lower() in ['range','driving_range','range_km','range_miles','wltp_range','epa_range']]
    if candidates:
        return candidates[0]
    range_like = [c for c in df.columns if 'range' in c.lower()]
    if range_like:
        return range_like[0]
    # fallback to last numeric column
    num = df.select_dtypes(include=[np.number]).columns.tolist()
    if not num:
        raise ValueError('No numeric columns to infer target from.')
    return num[-1]

def choose_features(df: pd.DataFrame, target: str, max_features: int = 12) -> List[str]:
    # Preferred feature keywords
    keys = {
        'battery': ['battery','kwh'],
        'efficiency': ['efficiency','wh/km','whperkm','consumption'],
        'motor': ['motor','power','kw','hp'],
        'weight': ['weight','kg'],
        'charging': ['charge','charging','charger'],
        'drivetrain': ['drive','drivetrain']
    }
    chosen = []
    for k, kws in keys.items():
        for col in df.columns:
            for kw in kws:
                if kw in col.lower() and col != target:
                    chosen.append(col)
                    break
            if len(chosen) and chosen[-1] == col:
                break
    # add remaining numeric columns
    num_cols = [c for c in df.select_dtypes(include=[np.number]).columns if c != target]
    for c in num_cols:
        if c not in chosen:
            chosen.append(c)
    # add categorical if present
    cat_cols = [c for c in df.select_dtypes(exclude=[np.number]).columns if c not in chosen]
    chosen += cat_cols
    return list(dict.fromkeys(chosen))[:max_features]

def build_pipeline(numeric_features: list, categorical_features: list, model_type: str = 'gb') -> Pipeline:
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse=False))
    ])
    preprocessor = ColumnTransformer(transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ])
    if model_type == 'gb':
        model = GradientBoostingRegressor(random_state=42)
    elif model_type == 'rf':
        model = RandomForestRegressor(random_state=42, n_jobs=-1)
    else:
        model = LinearRegression()
    pipe = Pipeline(steps=[('pre', preprocessor), ('model', model)])
    return pipe

def train_and_save(df: pd.DataFrame, model_path: str = 'ev_range_model.joblib') -> Tuple[Pipeline, str]:
    target = infer_target_column(df)
    features = choose_features(df, target)
    df = df.dropna(subset=[target])
    X = df[features]
    y = df[target].astype(float)
    # split is handled in training script; here we just train on full provided df for final model
    numeric_feats = X.select_dtypes(include=[np.number]).columns.tolist()
    categorical_feats = X.select_dtypes(exclude=[np.number]).columns.tolist()
    pipe = build_pipeline(numeric_feats, categorical_feats, model_type='gb')
    pipe.fit(X, y)
    joblib.dump({'pipeline': pipe, 'features': features, 'target': target}, model_path)
    return pipe, model_path

def load_model(model_path: str = 'ev_range_model.joblib') -> dict:
    data = joblib.load(model_path)
    return data

def predict_from_dict(model_data: dict, payload: dict) -> float:
    # payload keys must match model_data['features']
    features = model_data['features']
    df = pd.DataFrame([ {k: payload.get(k, None) for k in features} ])
    pred = model_data['pipeline'].predict(df)[0]
    return float(pred)
