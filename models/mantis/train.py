"""Download the pretrained Mantis weights (zero-shot, nothing is trained)."""

import argparse
import urllib.request
from pathlib import Path

WEIGHTS = "mantis_8w_nocov.pt"  # 8-step horizon, no covariate
URL = f"https://github.com/carsondudley1/Mantis/releases/download/mantis-v1.0/{WEIGHTS}"
CACHE_DIR = Path.home() / ".cache" / "mantis"


def train(train_data_path, model_path):
    # The weights are 1.2 GB, so keep them in a shared cache instead of every chap run folder
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    if not (CACHE_DIR / WEIGHTS).exists():
        print(f"Downloading {URL}")
        urllib.request.urlretrieve(URL, CACHE_DIR / f"{WEIGHTS}.part")
        (CACHE_DIR / f"{WEIGHTS}.part").rename(CACHE_DIR / WEIGHTS)
    with open(model_path, "w") as f:
        f.write(str(CACHE_DIR))
    print(f"Model directory saved to {model_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train a disease prediction model")
    parser.add_argument("train_data", help="Path to training data CSV file")
    parser.add_argument("model", help="Path to save the trained model")
    args = parser.parse_args()

    train(args.train_data, args.model)
