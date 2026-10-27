"""Seasonal naive baseline: a month is forecast as the spread of that calendar month in past years."""

import argparse

import numpy as np
import pandas as pd

# Same output grid as the Chronos model: 100 quantiles written as sample_0..sample_99
OUTPUT_LEVELS = np.linspace(0.01, 0.99, 100)


def predict(model_path, historic_data_path, future_data_path, out_file_path):
    past = pd.read_csv(historic_data_path)
    future = pd.read_csv(future_data_path)
    past["month"] = past["time_period"].str[-2:]

    rows = []
    for _, row in future[["location", "time_period"]].drop_duplicates().iterrows():
        same_month = past[(past["location"] == row["location"]) & (past["month"] == row["time_period"][-2:])]
        history = same_month["disease_cases"].dropna().values
        if len(history) == 0:  # no observation of this month yet: use everything we have
            history = past.loc[past["location"] == row["location"], "disease_cases"].dropna().values
        samples = np.quantile(history, OUTPUT_LEVELS) if len(history) else np.zeros(len(OUTPUT_LEVELS))
        rows.append([row["location"], row["time_period"], *samples])
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
