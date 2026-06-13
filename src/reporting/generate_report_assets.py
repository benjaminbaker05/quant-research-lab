from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


PROCESSED_DATA_DIR = Path("data/processed")
FIGURES_DIR = Path("reports/figures")


FEATURE_COLUMNS = [
    "return_1d",
    "log_return_1d",
    "volatility_5",
    "volatility_20",
    "volume_change_1d",
    "close_to_ma_5",
    "close_to_ma_20",
]


def find_feature_file() -> Path:
    feature_files = sorted(PROCESSED_DATA_DIR.glob("features_*.parquet"))

    if not feature_files:
        raise FileNotFoundError(
            "No feature files found. Run python -m src.features.build_features first."
        )

    return feature_files[0]


def save_returns_distribution(df: pd.DataFrame, output_path: Path) -> None:
    plt.figure(figsize=(10, 6))
    plt.hist(df["return_1d"].dropna(), bins=50)
    plt.title("Distribution of Daily Returns")
    plt.xlabel("Daily return")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def save_feature_correlation_plot(df: pd.DataFrame, output_path: Path) -> None:
    corr = df[FEATURE_COLUMNS].corr()

    plt.figure(figsize=(10, 8))
    plt.imshow(corr, aspect="auto")
    plt.colorbar(label="Correlation")

    plt.xticks(
        ticks=range(len(FEATURE_COLUMNS)),
        labels=FEATURE_COLUMNS,
        rotation=45,
        ha="right",
    )
    plt.yticks(
        ticks=range(len(FEATURE_COLUMNS)),
        labels=FEATURE_COLUMNS,
    )

    plt.title("Feature Correlation Matrix")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def save_feature_summary(df: pd.DataFrame, output_path: Path) -> None:
    summary = df[FEATURE_COLUMNS].describe().T
    summary.to_csv(output_path)


def main() -> None:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    feature_file = find_feature_file()
    df = pd.read_parquet(feature_file)

    returns_plot = FIGURES_DIR / "returns_distribution.png"
    correlation_plot = FIGURES_DIR / "feature_correlation.png"
    feature_summary = FIGURES_DIR / "feature_summary.csv"

    save_returns_distribution(df, returns_plot)
    save_feature_correlation_plot(df, correlation_plot)
    save_feature_summary(df, feature_summary)

    print(f"Feature file used: {feature_file}")
    print(f"Saved returns plot to {returns_plot}")
    print(f"Saved feature correlation plot to {correlation_plot}")
    print(f"Saved feature summary to {feature_summary}")


if __name__ == "__main__":
    main()