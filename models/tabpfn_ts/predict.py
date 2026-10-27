"""Forecast with TabPFN-TS locally, using rainfall and temperature as known-future covariates.

Needs a Prior Labs licence acceptance: set TABPFN_TOKEN (see README.md).
"""

import argparse
import os

os.environ.setdefault("TABPFN_DISABLE_TELEMETRY", "1")

import numpy as np
import pandas as pd
from tabpfn_time_series import TabPFNMode, TabPFNTSPipeline

COVARIATES = ["rainfall", "mean_temperature"]
# Same output grid as the Chronos model: 100 quantiles written as sample_0..sample_99
OUTPUT_LEVELS = [round(float(q), 4) for q in np.linspace(0.01, 0.99, 100)]


def predict(model_path, historic_data_path, future_data_path, out_file_path):
    # LOCAL runs the model on this machine; CLIENT would send the data to Prior Labs' API
    pipeline = TabPFNTSPipeline(tabpfn_mode=TabPFNMode.LOCAL)

    past = pd.read_csv(historic_data_path)
    future = pd.read_csv(future_data_path)
    covariates = [c for c in COVARIATES if c in past.columns and c in future.columns]

    # Forecast log(1 + cases) so outbreak peaks are not huge outliers; undone with expm1 below.
    # The upper quantiles blow up when transformed back, so cap them at 10x the location's record.
    cap = np.log1p(10 * past.groupby("location")["disease_cases"].max().fillna(0))
    context = pd.DataFrame(
        {
            "item_id": past["location"],
            "timestamp": pd.to_datetime(past["time_period"]),
            "target": np.log1p(past["disease_cases"]),
            **{c: past[c] for c in covariates},
        }
    )
    future_df = pd.DataFrame(
        {
            "item_id": future["location"],
            "timestamp": pd.to_datetime(future["time_period"]),
            **{c: future[c] for c in covariates},
        }
    )
    pred = pipeline.predict_df(context, future_df=future_df, quantiles=OUTPUT_LEVELS).reset_index()

    quantile_cols = [c for c in pred.columns if c not in ("item_id", "timestamp", "target")]
    quantile_cols = sorted(quantile_cols, key=float)
    location_cap = pred["item_id"].map(cap).values[:, None]
    samples = np.expm1(np.clip(pred[quantile_cols].values.astype(float), 0, location_cap))

    out = pd.DataFrame(samples, columns=[f"sample_{i}" for i in range(len(quantile_cols))])
    out.insert(0, "time_period", pd.to_datetime(pred["timestamp"]).dt.strftime("%Y-%m"))
    out.insert(0, "location", pred["item_id"].values)
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
