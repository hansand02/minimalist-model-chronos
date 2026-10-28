"""Forecast with T0-gamma, using rainfall and temperature as known-future covariates."""

import argparse

import numpy as np
import pandas as pd
import torch
from t0 import T0Forecaster

COVARIATES = ["rainfall", "mean_temperature"]
# Same output grid as the Chronos model: 100 quantiles written as sample_0..sample_99
OUTPUT_LEVELS = np.round(np.linspace(0.01, 0.99, 100), 4).tolist()


def predict(model_path, historic_data_path, future_data_path, out_file_path):
    with open(model_path) as f:
        model = T0Forecaster.from_pretrained(f.read().strip()).eval()

    past = pd.read_csv(historic_data_path)
    future = pd.read_csv(future_data_path)
    both = pd.concat([past, future])

    # Forecast log(1 + cases) so outbreak peaks are not huge outliers; undone with expm1 below.
    # The upper quantiles blow up when transformed back, so cap them at 10x the location's record.
    past["disease_cases"] = np.log1p(past["disease_cases"])
    context = past.pivot(index="location", columns="time_period", values="disease_cases")
    cap = np.log1p(10 * np.expm1(context.max(axis=1).fillna(0).values))
    locations = context.index
    future_periods = sorted(future["time_period"].unique())
    covariates = [c for c in COVARIATES if c in both.columns]
    known = np.stack(
        [both.pivot(index="location", columns="time_period", values=c).loc[locations].values for c in covariates],
        axis=1,
    )  # (location, covariate, past + future periods)

    with torch.no_grad():
        out = model.predict(
            torch.tensor(context.values, dtype=torch.float32),
            horizon=len(future_periods),
            quantile_levels=OUTPUT_LEVELS,
            future_covariates=torch.tensor(known, dtype=torch.float32),
        )
    quantiles = np.expm1(np.clip(out.quantiles.cpu().numpy(), 0, cap[:, None, None]))  # (location, horizon, 100)

    rows = [
        [location, period, *quantiles[i, h]]
        for i, location in enumerate(locations)
        for h, period in enumerate(future_periods)
    ]
    columns = ["location", "time_period"] + [f"sample_{i}" for i in range(len(OUTPUT_LEVELS))]
    pd.DataFrame(rows, columns=columns).to_csv(out_file_path, index=False)
    print(f"Predictions saved to {out_file_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate disease predictions")
    parser.add_argument("model", help="Path to trained model file")
    parser.add_argument("historic_data", help="Path to historic data CSV file")
    parser.add_argument("future_data", help="Path to future climate data CSV file")
    parser.add_argument("out_file", help="Path to save predictions CSV file")
    args = parser.parse_args()

    predict(args.model, args.historic_data, args.future_data, args.out_file)
