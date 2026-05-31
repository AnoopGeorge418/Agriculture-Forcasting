import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from dotenv import load_dotenv

load_dotenv()


def clean_data(input_path=None, output_path=None, plot_dir=None):
    """
    Automated pipeline to clean agricultural price data.
    """
    input_path = input_path or os.getenv("DATA_RAW", "data/raw/agricultural_prices.csv")
    output_path = output_path or os.getenv(
        "DATA_CLEANED", "data/cleaned/cleaned_prices.csv"
    )
    plot_dir = plot_dir or os.getenv("OUTPUTS_DIR", "outputs/plots/")

    print(f"Reading raw data from {input_path}...")
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found at {input_path}")

    df = pd.read_csv(input_path)

    # Ensure date column is datetime
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")
    df = df.set_index("date")

    # Ensure monthly frequency
    df = df.asfreq("MS")

    # 1. Missing Data Heatmap
    os.makedirs(plot_dir, exist_ok=True)
    plt.figure(figsize=(10, 4))
    sns.heatmap(df.isnull(), cbar=False, yticklabels=False, cmap="viridis")
    plt.title("Missing Data Heatmap")
    plt.savefig(os.path.join(plot_dir, "missing_data_heatmap.png"))
    plt.close()

    raw_series = df["avg_monthly_price"].copy()

    # 2. Handle Missing Values
    df["avg_monthly_price"] = (
        df["avg_monthly_price"].interpolate(method="time").ffill().bfill()
    )

    # 3. Handle Outliers (IQR Method)
    Q1 = df["avg_monthly_price"].quantile(0.25)
    Q3 = df["avg_monthly_price"].quantile(0.75)
    IQR = Q3 - Q1
    df["avg_monthly_price"] = df["avg_monthly_price"].clip(
        lower=Q1 - 1.5 * IQR, upper=Q3 + 1.5 * IQR
    )

    # 4. Plots
    plt.figure(figsize=(12, 6))
    plt.plot(raw_series, label="Raw Data", alpha=0.5, linestyle="--")
    plt.plot(df["avg_monthly_price"], label="Cleaned Data", color="green")
    plt.title("Raw vs Cleaned Price Time-Series")
    plt.legend()
    plt.savefig(os.path.join(plot_dir, "raw_vs_clean_lineplot.png"))
    plt.close()

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path)
    print(f"Cleaned data saved to {output_path}")
    return df


if __name__ == "__main__":
    clean_data()
