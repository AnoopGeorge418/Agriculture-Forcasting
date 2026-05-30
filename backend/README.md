# AgriPrice Forecast - Backend

This is the predictive engine for agricultural price forecasting. It uses a combination of statistical, machine learning, and deep learning models to provide accurate monthly price predictions.

## Tech Stack
- **Framework**: FastAPI
- **Data**: Pandas, Numpy, Scikit-learn
- **Modeling**: Statsmodels (SARIMA), XGBoost, TensorFlow (LSTM)
- **Deployment**: Docker, Railway

## Features
- **Automated Pipeline**: End-to-end data cleaning, EDA, and model training.
- **Inference API**: High-performance `/predict` endpoint for real-time forecasts.
- **Data Endpoint**: Exposes historical and forecasted data for frontend consumption.
- **Monitoring**: Built-in drift detection and latency tracking.

## Getting Started

### Local Setup
1. Install dependencies:
   ```bash
   uv sync
   ```
2. Configure environment:
   ```bash
   cp .env.example .env
   ```
3. Run the pipeline:
   ```bash
   python main.py pipeline
   ```
4. Start the server:
   ```bash
   python main.py server
   ```

### API Documentation
Once the server is running, visit `http://localhost:8000/docs` for interactive Swagger documentation.

## Deployment
This backend is optimized for **Railway**. Simply connect your GitHub repo and set the `PORT` environment variable.
