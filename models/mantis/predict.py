"""Forecast with Mantis from the case history alone, one location at a time."""

import argparse

import numpy as np
import pandas as pd
from mantis.inference import Mantis

MANTIS_LEVELS = [0.05, 0.1, 0.25, 0.4, 0.5, 0.6, 0.75, 0.9, 0.95]
# Same output grid as the Chronos model; levels outside 0.05-0.95 get the outermost Mantis quantile
OUTPUT_LEVELS = np.linspace(0.01, 0.99, 100)


def predict(model_path, historic_data_path, future_data_path, out_file_path):
    with open(model_path) as f:
        model = Mantis(forecast_horizon=8, use_covariate=False, model_dir=f.read().strip())

    past = pd.read_csv(historic_data_path)
    future = pd.read_csv(future_data_path)
    future_periods = sorted(future["time_period"].unique())
    if len(future_periods) > 8:
        raise ValueError(f"Mantis forecasts at most 8 steps, got {len(future_periods)}")

    rows = []
    for location, group in past.sort_values("time_period").groupby("location"):
        # Mantis was trained on weekly data with 112 steps of context; we give it months.
        # It can't take missing values, so fill them in.
        cases = group["disease_cases"].interpolate(limit_direction="both").fillna(0).values[-112:]
        population = group["population"].dropna()
        population = population.iloc[-1] if len(population) else None
        quantiles = model.predict(cases, population=population, target_type=0)
        for h, period in enumerate(future_periods):
            samples = np.interp(OUTPUT_LEVELS, MANTIS_LEVELS, quantiles[h])
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
