import pandas as pd
import argparse
from model_utils import train_and_save, infer_target_column, choose_features
import json
def main(csv_path: str, out_model: str):
    print('Loading data from', csv_path)
    df = pd.read_csv(csv_path)
    target = infer_target_column(df)
    print('Inferred target column:', target)
    features = choose_features(df, target)
    print('Chosen features:', features)
    pipe, model_path = train_and_save(df, model_path=out_model)
    print('Model trained and saved to', model_path)
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv', type=str, default='EV_cars.csv', help='Path to CSV dataset')
    parser.add_argument('--out', type=str, default='ev_range_model.joblib', help='Output model path')
    args = parser.parse_args()
    main(args.csv, args.out)
