"""Download the pretrained TimesFM 3.0 model (zero-shot, nothing is trained)."""

import argparse

from timesfm3 import ModelConfig, TimesFM3Evaluator

MODEL_ID = "google/timesfm-3.0-pytorch"


def train(train_data_path, model_path):
    TimesFM3Evaluator(ModelConfig(checkpoint_path=MODEL_ID, device="cpu"))  # fills the Hugging Face cache
    with open(model_path, "w") as f:
        f.write(MODEL_ID)
    print(f"Model id saved to {model_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train a disease prediction model")
    parser.add_argument("train_data", help="Path to training data CSV file")
    parser.add_argument("model", help="Path to save the trained model")
    args = parser.parse_args()

    train(args.train_data, args.model)
