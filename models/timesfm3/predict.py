"""Forecast with TimesFM 3.0, using rainfall and temperature as known-future covariates."""

import argparse

import numpy as np
import pandas as pd
from timesfm3 import ModelConfig, TimesFM3Evaluator

COVARIATES = ["rainfall", "mean_temperature"]
MODEL_LEVELS = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]  # the model's only quantiles
# Same output grid as the Chronos model: 100 quantiles written as sample_0..sample_99.
# Levels below 0.1 and above 0.9 are clamped to the 0.1 and 0.9 forecasts.
OUTPUT_LEVELS = np.linspace(0.01, 0.99, 100)


def predict(model_path, historic_data_path, future_data_path, out_file_path):
    with open(model_path) as f:
        model = TimesFM3Evaluator(ModelConfig(checkpoint_path=f.read().strip(), device="cpu"))

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
    ).astype(np.float32)  # (location, covariate, past + future periods)

    outputs = model.predict_batch(
        contexts=list(context.values.astype(np.float32)),
        horizon=len(future_periods),
        past_future_covariates=list(known),
    )
    quantiles = np.stack([np.atleast_3d(o.quantiles).reshape(len(future_periods), -1) for o in outputs])
    quantiles = np.expm1(np.clip(quantiles, 0, cap[:, None, None]))  # (location, horizon, 9)

    rows = []
    for i, location in enumerate(locations):
        for h, period in enumerate(future_periods):
            samples = np.interp(OUTPUT_LEVELS, MODEL_LEVELS, quantiles[i, h])
            rows.append([location, period, *samples])
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
