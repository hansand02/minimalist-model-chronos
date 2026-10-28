"""Download the pretrained T0-gamma model (zero-shot, nothing is trained)."""

import argparse

from t0 import T0Forecaster

MODEL_ID = "theforecastingcompany/t0-gamma"


def train(train_data_path, model_path):
    T0Forecaster.from_pretrained(MODEL_ID)  # fills the Hugging Face cache
    with open(model_path, "w") as f:
        f.write(MODEL_ID)
    print(f"Model id saved to {model_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train a disease prediction model")
    parser.add_argument("train_data", help="Path to training data CSV file")
    parser.add_argument("model", help="Path to save the trained model")
    args = parser.parse_args()

    train(args.train_data, args.model)
