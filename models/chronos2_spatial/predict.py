"""Chronos-2 (log1p) plus a 'flow' covariate: outbreak pressure spreading from neighbouring provinces.

Each month, a province takes in its neighbours' incidence plus a share ALPHA of their existing
pressure, so outbreaks flow one border per month and fade as they travel:

    p_i(t) = mean over neighbours j of [ x_j(t) + ALPHA * p_j(t-1) ],   x = log1p(cases per 100k)

The pressure is a past-only covariate (it is in the history, not in the future data), so
Chronos-2 never needs future values of it. Neighbours come from adjacency.json.
"""

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from chronos import Chronos2Pipeline

ALPHA = 0.5  # how much pressure survives each month; fixed in advance, not tuned
ADJACENCY = json.loads((Path(__file__).parent / "adjacency.json").read_text())


def flow_pressure(past):
    """Neighbour pressure per (location, time_period), 0 for locations without known neighbours."""
    incidence = past.pivot(index="time_period", columns="location", values="disease_cases").sort_index()
    population = past.pivot(index="time_period", columns="location", values="population").sort_index()
    x = np.log1p(incidence / population * 1e5).ffill().fillna(0)

    locations = list(x.columns)
    weights = np.zeros((len(locations), len(locations)))  # row-normalised: mean over neighbours
    for i, location in enumerate(locations):
        neighbours = [locations.index(n) for n in ADJACENCY.get(location, []) if n in locations]
        weights[i, neighbours] = 1 / len(neighbours) if neighbours else 0

    pressure = np.zeros_like(x.values)
    for t in range(len(x)):
        previous = pressure[t - 1] if t > 0 else 0
        pressure[t] = weights @ (x.values[t] + ALPHA * previous)
    return pd.DataFrame(pressure, index=x.index, columns=locations).stack().rename("flow_pressure")


def predict(model_path, historic_data_path, future_data_path, out_file_path):
    model = Chronos2Pipeline.from_pretrained(model_path, device_map="cpu")

    past_data = pd.read_csv(historic_data_path)
    future_df = pd.read_csv(future_data_path)

    # Computed on raw counts, before the log1p below
    past_data = past_data.merge(flow_pressure(past_data).reset_index(), on=["time_period", "location"])

    # Forecast log(1 + cases) so outbreak peaks are not huge outliers; undone with expm1 below.
    # The upper quantiles blow up when transformed back, so cap them at 10x the location's record.
    cap = np.log1p(10 * past_data.groupby("location")["disease_cases"].max().fillna(0))
    past_data["disease_cases"] = np.log1p(past_data["disease_cases"])

    future_count = len(pd.unique(future_df["time_period"]))
    quantile_levels = np.round(np.linspace(0.01, 0.99, 100), 4).tolist()

    pred_df = model.predict_df(
        past_data,
        future_df,  # has no flow_pressure column, so Chronos-2 treats it as a past-only covariate
        prediction_length=future_count,
        target="disease_cases",
        id_column="location",
        quantile_levels=quantile_levels,
        timestamp_column="time_period",
        cross_learning=True,
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
