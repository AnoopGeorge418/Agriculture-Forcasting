import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.statespace.sarimax import SARIMAX
import xgboost as xgb
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import joblib
import os
from dotenv import load_dotenv

load_dotenv()


def perform_eda(df, plot_dir=None):
    plot_dir = plot_dir or os.getenv("OUTPUTS_DIR", "outputs/plots/")
    os.makedirs(plot_dir, exist_ok=True)

    print("Performing Seasonal Decomposition...")
    result = seasonal_decompose(df["avg_monthly_price"], model="additive")
    fig = result.plot()
    fig.set_size_inches(12, 10)
    plt.tight_layout()
    plt.savefig(os.path.join(plot_dir, "seasonal_decomposition.png"))
    plt.close()

    fig, ax = plt.subplots(2, 1, figsize=(12, 8))
    plot_acf(df["avg_monthly_price"], ax=ax[0])
    plot_pacf(df["avg_monthly_price"], ax=ax[1])
    plt.savefig(os.path.join(plot_dir, "acf_pacf.png"))
    plt.close()


def train_sarima(df, model_dir=None):
    model_dir = model_dir or os.getenv("MODELS_DIR", "models/")
    os.makedirs(model_dir, exist_ok=True)
    print("Training SARIMA...")
    model = SARIMAX(
        df["avg_monthly_price"], order=(1, 1, 1), seasonal_order=(1, 1, 1, 12)
    )
    results = model.fit(disp=False)
    results.save(os.path.join(model_dir, "sarima_model.pkl"))
    return results


def train_xgboost(df, model_dir=None):
    model_dir = model_dir or os.getenv("MODELS_DIR", "models/")
    os.makedirs(model_dir, exist_ok=True)
    print("Training XGBoost...")
    data = df.copy()
    for i in range(1, 13):
        data[f"lag_{i}"] = data["avg_monthly_price"].shift(i)
    data["rolling_mean"] = data["avg_monthly_price"].shift(1).rolling(window=3).mean()
    data = data.dropna()

    X = data.drop("avg_monthly_price", axis=1)
    y = data["avg_monthly_price"]
    model = xgb.XGBRegressor(objective="reg:squarederror", n_estimators=100)
    model.fit(X, y)
    joblib.dump(model, os.path.join(model_dir, "xgb_model.pkl"))
    return model


def train_lstm(df, model_dir=None):
    model_dir = model_dir or os.getenv("MODELS_DIR", "models/")
    os.makedirs(model_dir, exist_ok=True)
    print("Training LSTM...")
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(df[["avg_monthly_price"]])
    joblib.dump(scaler, os.path.join(model_dir, "scaler.pkl"))

    def create_sequences(data, seq_length):
        X, y = [], []
        for i in range(len(data) - seq_length):
            X.append(data[i : i + seq_length])
            y.append(data[i + seq_length])
        return np.array(X), np.array(y)

    X, y = create_sequences(scaled_data, 12)
    model = Sequential(
        [
            LSTM(50, activation="relu", input_shape=(12, 1), return_sequences=True),
            Dropout(0.2),
            LSTM(50, activation="relu"),
            Dense(1),
        ]
    )
    model.compile(optimizer="adam", loss="mse")
    model.fit(X, y, epochs=20, batch_size=16, verbose=0)
    model.save(os.path.join(model_dir, "lstm_model.keras"))
    return model


if __name__ == "__main__":
    input_path = os.getenv("DATA_CLEANED", "data/cleaned/cleaned_prices.csv")
    df = pd.read_csv(input_path, index_col="date", parse_dates=True)
    perform_eda(df)
    train_sarima(df)
    train_xgboost(df)
    train_lstm(df)
