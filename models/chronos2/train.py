"""Train a simple linear regression model for disease prediction."""

import argparse

import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression
import torch

from chronos import Chronos2Pipeline


def train(train_data_path, model_path):
    """Train the model on the provided data.

    Parameters
    ----------
    train_data_path : str
        Path to the training data CSV file.
    model_path : str
        Path where the trained model will be saved.
    """


    pipeline = Chronos2Pipeline.from_pretrained("amazon/chronos-2", device_map="cpu")
    pipeline.model.save_pretrained(model_path)
    
    print(f"Model saved to {model_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train a disease prediction model")
    parser.add_argument("train_data", help="Path to training data CSV file")
    parser.add_argument("model", help="Path to save the trained model")
    args = parser.parse_args()

    train(args.train_data, args.model)
