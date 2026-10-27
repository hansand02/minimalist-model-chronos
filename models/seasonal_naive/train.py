"""Nothing to train: the forecast is read straight from the history at predict time."""

import argparse


def train(train_data_path, model_path):
    with open(model_path, "w") as f:
        f.write("seasonal-naive")
    print(f"Nothing to train, placeholder saved to {model_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train a disease prediction model")
    parser.add_argument("train_data", help="Path to training data CSV file")
    parser.add_argument("model", help="Path to save the trained model")
    args = parser.parse_args()

    train(args.train_data, args.model)
