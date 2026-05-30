# Agricultural Price Forecasting System (AgriPrice Predict)

AgriPrice Predict is an enterprise-grade forecasting platform designed to mitigate supply chain risks in the agricultural sector. It combines a robust Python-based predictive engine with a modern Next.js dashboard to provide real-time price intelligence and actionable business strategies.

## 🏗️ Architecture Overview

- **Backend**: FastAPI (Python 3.12) serving a machine learning pipeline that includes SARIMA, XGBoost, and LSTM models.
- **Frontend**: Next.js (TypeScript) dashboard utilizing Recharts for visualization and Tailwind CSS for a premium UI.
- **Data Pipeline**: Automated cleaning, EDA, model training, and evaluation cycles.
- **Deployment**: Fully containerized with Docker and Docker Compose.

## 🚀 Getting Started

### Prerequisites
- Docker & Docker Compose
- Python 3.12+ (if running locally without Docker)
- Node.js 20+ (if running locally without Docker)

### Quick Start (Docker)
The easiest way to run the entire stack is using Docker Compose:

```bash
docker-compose up --build
```

- **Frontend**: `http://localhost:3000`
- **Backend API**: `http://localhost:8000`
- **API Docs**: `http://localhost:8000/docs`

### Local Development Setup

#### Backend
1. Navigate to the `backend/` directory.
2. Install dependencies using `uv` or `pip`:
   ```bash
   uv sync
   # OR
   pip install -r requirements.txt
   ```
3. Run the data pipeline to generate models and forecasts:
   ```bash
   python main.py pipeline
   ```
4. Start the FastAPI server:
   ```bash
   python main.py server
   ```

#### Frontend
1. Navigate to the `frontend/` directory.
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```

## 📊 Data Pipeline & Models

The system follows a sequential pipeline:
1. **Cleaning (`Q1`)**: Handles missing values via time-interpolation and removes outliers using the IQR method.
2. **EDA & Training (`Q2`)**: Performs seasonal decomposition and trains three models:
   - **SARIMA**: Statistical model for capturing seasonality.
   - **XGBoost**: Gradient boosted trees for capturing non-linear patterns.
   - **LSTM**: Deep learning model for long-term sequence dependencies.
3. **Evaluation (`Q3`)**: Compares models using MAE, RMSE, and MAPE metrics.
4. **Integration (`Q7`)**: Exposes the XGBoost model via a REST API for real-time inference.

## 🛠️ Production Readiness

### Environment Variables
Configure these in your production environment or `.env` files:

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Backend server port | `8000` |
| `ALLOWED_ORIGINS` | CORS allowed origins (comma-separated) | `*` |
| `DATA_RAW` | Path to raw input CSV | `data/raw/agricultural_prices.csv` |
| `MODELS_DIR` | Directory to store trained models | `models/` |
| `NEXT_PUBLIC_API_URL` | Frontend pointer to Backend API | `http://localhost:8000` |

### Security
- **CORS**: In production, set `ALLOWED_ORIGINS` to your frontend domain.
- **Secrets**: Change `SECRET_KEY` in `backend/.env` to a secure random string.
- **Docker**: The provided `Dockerfile`s use multi-stage builds and non-root users (where applicable) for security.

### Monitoring
- **Health Check**: Monitor `GET /health` for backend status.
- **Logs**: Backend uses standard Python logging for easier integration with ELK or CloudWatch.

## 📈 Dashboard Features
- **Price Trends**: Interactive line charts showing historical vs. forecasted prices.
- **What-if Analysis**: A custom prediction form to test "what-if" scenarios based on the last 12 months of price data.
- **Risk Mitigation**: AI-driven strategy cards providing procurement and supply chain advice based on volatility forecasts.

## 🤝 Contributing
1. Fork the repo.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
