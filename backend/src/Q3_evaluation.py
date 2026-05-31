import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
from statsmodels.tsa.statespace.sarimax import SARIMAXResults
from tensorflow.keras.models import load_model
import os
from dotenv import load_dotenv

load_dotenv()


def mean_absolute_percentage_error(y_true, y_pred):
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100


def evaluate_models(df, model_dir=None, plot_dir=None):
    model_dir = model_dir or os.getenv("MODELS_DIR", "models/")
    plot_dir = plot_dir or os.getenv("OUTPUTS_DIR", "outputs/plots/")
    os.makedirs(plot_dir, exist_ok=True)

    train = df.iloc[:-12]
    test = df.iloc[-12:]
    actuals = test["avg_monthly_price"].values

    metrics = []

    # 1. SARIMA
    sarima_res = SARIMAXResults.load(os.path.join(model_dir, "sarima_model.pkl"))
    sarima_pred = sarima_res.get_forecast(steps=12).predicted_mean
    metrics.append(
        {
            "Model": "SARIMA",
            "MAE": mean_absolute_error(actuals, sarima_pred),
            "RMSE": np.sqrt(mean_squared_error(actuals, sarima_pred)),
            "MAPE": mean_absolute_percentage_error(actuals, sarima_pred),
        }
    )

    # 2. XGBoost
    xgb_model = joblib.load(os.path.join(model_dir, "xgb_model.pkl"))
    data = df.copy()
    for i in range(1, 13):
        data[f"lag_{i}"] = data["avg_monthly_price"].shift(i)
    data["rolling_mean"] = data["avg_monthly_price"].shift(1).rolling(window=3).mean()
    X_test = data.drop("avg_monthly_price", axis=1).iloc[-12:]
    xgb_pred = xgb_model.predict(X_test)
    metrics.append(
        {
            "Model": "XGBoost",
            "MAE": mean_absolute_error(actuals, xgb_pred),
            "RMSE": np.sqrt(mean_squared_error(actuals, xgb_pred)),
            "MAPE": mean_absolute_percentage_error(actuals, xgb_pred),
        }
    )

    # 3. LSTM
    lstm_model = load_model(os.path.join(model_dir, "lstm_model.keras"))
    scaler = joblib.load(os.path.join(model_dir, "scaler.pkl"))
    scaled_full = scaler.transform(df[["avg_monthly_price"]])
    X_lstm = [scaled_full[len(scaled_full) - 24 : len(scaled_full) - 12]]
    lstm_pred_scaled = lstm_model.predict(np.array(X_lstm))
    lstm_pred = scaler.inverse_transform(lstm_pred_scaled).flatten()
    # Placeholder for multi-step LSTM eval
    metrics.append(
        {
            "Model": "LSTM",
            "MAE": mean_absolute_error(actuals[:1], lstm_pred),
            "RMSE": np.sqrt(mean_squared_error(actuals[:1], lstm_pred)),
            "MAPE": mean_absolute_percentage_error(actuals[:1], lstm_pred),
        }
    )

    metrics_df = pd.DataFrame(metrics)
    plt.figure(figsize=(10, 6))
    sns.barplot(
        data=metrics_df.melt(id_vars="Model"), x="variable", y="value", hue="Model"
    )
    plt.title("Model Comparison")
    plt.savefig(os.path.join(plot_dir, "model_comparison_metrics.png"))
    plt.close()
    return metrics_df


def generate_forecast(df, model_dir=None, forecast_path=None, plot_dir=None):
    model_dir = model_dir or os.getenv("MODELS_DIR", "models/")
    forecast_path = forecast_path or os.getenv(
        "DATA_FORECASTS", "data/forecasts/12_month_forecast.csv"
    )
    plot_dir = plot_dir or os.getenv("OUTPUTS_DIR", "outputs/plots/")

    os.makedirs(os.path.dirname(forecast_path), exist_ok=True)
    sarima_res = SARIMAXResults.load(os.path.join(model_dir, "sarima_model.pkl"))
    forecast_df = (
        sarima_res.get_forecast(steps=12)
        .summary_frame()[["mean"]]
        .rename(columns={"mean": "forecasted_price"})
    )
    forecast_df.to_csv(forecast_path)

    plt.figure(figsize=(12, 6))
    plt.plot(df.index[-24:], df["avg_monthly_price"].iloc[-24:], label="Historical")
    plt.plot(
        forecast_df.index,
        forecast_df["forecasted_price"],
        label="Forecast",
        color="red",
    )
    plt.title("12-Month Forecast")
    plt.legend()
    plt.savefig(os.path.join(plot_dir, "final_forecast.png"))
    plt.close()


if __name__ == "__main__":
    df = pd.read_csv(
        os.getenv("DATA_CLEANED", "data/cleaned/cleaned_prices.csv"),
        index_col="date",
        parse_dates=True,
    )
    evaluate_models(df)
    generate_forecast(df)
