from pathlib import Path
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report


PROCESSED_DATA_DIR = Path("data/processed")


FEATURE_COLUMNS = [
    "return_1d",
    "log_return_1d",
    "volatility_5",
    "volatility_20",
    "volume_change_1d",
    "close_to_ma_5",
    "close_to_ma_20",
]


def train_baseline_model(input_path: str | Path) -> dict:
    """
    Train a simple logistic regression model using a time-based split.
    """
    input_path = Path(input_path)
    df = pd.read_parquet(input_path)

    split_idx = int(len(df) * 0.8)

    train = df.iloc[:split_idx]
    test = df.iloc[split_idx:]

    X_train = train[FEATURE_COLUMNS]
    y_train = train["target_up"]

    X_test = test[FEATURE_COLUMNS]
    y_test = test["target_up"]

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)

    accuracy = accuracy_score(y_test, preds)

    report = classification_report(
        y_test,
        preds,
        output_dict=False,
        zero_division=0,
    )

    return {
        "accuracy": accuracy,
        "classification_report": report,
        "n_train": len(train),
        "n_test": len(test),
    }


if __name__ == "__main__":
    feature_files = list(PROCESSED_DATA_DIR.glob("features_*.parquet"))

    if not feature_files:
        raise FileNotFoundError("No feature files found")

    for file in feature_files:
        results = train_baseline_model(file)

        print(f"\nResults for {file}")
        print(f"Train rows: {results['n_train']}")
        print(f"Test rows: {results['n_test']}")
        print(f"Accuracy: {results['accuracy']:.4f}")
        print(results["classification_report"])