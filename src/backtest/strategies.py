from __future__ import annotations

import numpy as np
import pandas as pd


def add_strategy_signals(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add simple baseline strategy signals.

    Signals are interpreted as:
    - 1 = long
    - 0 = flat
    - -1 = short

    These are deliberately simple strategies. They are baselines, not claims
    of tradable alpha.
    """
    df = df.copy()

    required_columns = [
        "return_1d",
        "volatility_20",
        "close_to_ma_5",
        "close_to_ma_20",
    ]

    missing = [column for column in required_columns if column not in df.columns]

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    # Baseline 1: always long.
    df["signal_long_only"] = 1

    # Baseline 2: trend-following using 20-day moving average.
    df["signal_trend_ma_20"] = np.where(
        df["close_to_ma_20"] > 0,
        1,
        -1,
    )

    # Baseline 3: mean reversion.
    # If price is meaningfully below the moving average, go long.
    # If price is meaningfully above the moving average, go short.
    df["signal_mean_reversion_ma_20"] = np.where(
        df["close_to_ma_20"] < -0.01,
        1,
        np.where(df["close_to_ma_20"] > 0.01, -1, 0),
    )

    # Baseline 4: simple volatility breakout.
    # Go long after a large positive return, short after a large negative return.
    df["signal_volatility_breakout"] = np.where(
        df["return_1d"] > df["volatility_20"],
        1,
        np.where(df["return_1d"] < -df["volatility_20"], -1, 0),
    )

    # Baseline 5: short-term reversal.
    # Go against the previous day's return.
    df["signal_short_term_reversal"] = np.where(
        df["return_1d"] < 0,
        1,
        np.where(df["return_1d"] > 0, -1, 0),
    )

    return df