"""Generate predictions using a trained model."""

import argparse

import joblib
import pandas as pd
import torch
import numpy as np
from chronos import Chronos2Pipeline

COVARIATES = ["rainfall", "mean_temperature"]


def predict(model_path, historic_data_path, future_data_path, out_file_path):
    """Generate predictions using the trained model.

    Parameters
    ----------
    model_path : str
        Path to the trained model file.
    historic_data_path : str
        Path to historic data CSV file (unused in this simple model).
    future_data_path : str
        Path to future climate data CSV file.
    out_file_path : str
        Path where predictions will be saved.
    """
    model = Chronos2Pipeline.from_pretrained(model_path, device_map="cpu")

    # Same covariates as the other foundation models; chap's CSVs also carry an index column
    past_data = pd.read_csv(historic_data_path)[["location", "time_period", "disease_cases", *COVARIATES]]
    future_df = pd.read_csv(future_data_path)[["location", "time_period", *COVARIATES]]

    # Forecast log(1 + cases) so outbreak peaks are not huge outliers; undone with expm1 below.
    # The upper quantiles blow up when transformed back, so cap them at 10x the location's record.
    cap = np.log1p(10 * past_data.groupby("location")["disease_cases"].max().fillna(0))
    past_data["disease_cases"] = np.log1p(past_data["disease_cases"])


    future_count = len(pd.unique(future_df["time_period"]))

    n_samples = 100
    quantile_levels = np.round(np.linspace(0.01, 0.99, n_samples), 4).tolist()

    pred_df = model.predict_df(
        past_data,
        future_df,
        prediction_length=future_count,
        target="disease_cases",
        id_column="location",
        quantile_levels=quantile_levels,  # Quantile for probabilistic forecast
        timestamp_column="time_period",
        cross_learning=True
    )

    # Chronos returns full dates (2022-10-01), which chap reads as days; convert back to months
    pred_df["time_period"] = pd.to_datetime(pred_df["time_period"]).dt.strftime("%Y-%m")

    # chap only reads columns named sample_0..sample_N, so rename the quantile columns
    quantile_cols = [c for c in pred_df.columns if c not in ("location", "time_period", "target_name", "predictions")]
    out = pred_df[["location", "time_period"]].copy()
    location_cap = pred_df["location"].map(cap).values
    for i, col in enumerate(quantile_cols):
        out[f"sample_{i}"] = np.expm1(np.clip(pred_df[col].values, 0, location_cap))

    out.to_csv(out_file_path, index=False)
    print(f"Predictions saved to {out_file_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate disease predictions")
    parser.add_argument("model", help="Path to trained model file")
    parser.add_argument("historic_data", help="Path to historic data CSV file")
    parser.add_argument("future_data", help="Path to future climate data CSV file")
    parser.add_argument("out_file", help="Path to save predictions CSV file")
    args = parser.parse_args()

    predict(args.model, args.historic_data, args.future_data, args.out_file)
