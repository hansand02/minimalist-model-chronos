import torch
import pandas as pd

from chronos import Chronos2Pipeline


data = pd.read_csv("./input/trainData.csv")


pipeline = Chronos2Pipeline.from_pretrained("amazon/chronos-2", device_map="cpu")

pred_df = pipeline.predict_df(
    data,
    prediction_length=24,
    target="disease_cases",
    id_column="location",
    timestamp_column="time_period",
)

print(pred_df)