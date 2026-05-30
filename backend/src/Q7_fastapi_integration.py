from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
import os
import logging
from contextlib import asynccontextmanager
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global model cache
MODEL = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load model on startup
    global MODEL
    model_dir = os.getenv('MODELS_DIR', 'models/')
    model_path = os.path.join(model_dir, 'xgb_model.pkl')
    if os.path.exists(model_path):
        try:
            MODEL = joblib.load(model_path)
            logger.info(f"Model successfully loaded from {model_path}")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
    else:
        logger.warning(f"Model not found at {model_path}")
    
    yield
    # Clean up on shutdown if needed
    MODEL = None

app = FastAPI(title="AgriPrice Forecast API", lifespan=lifespan)

# Enable CORS for frontend integration
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PredictRequest(BaseModel):
    last_12_months: list[float]

class PredictResponse(BaseModel):
    prediction: float
    model_type: str

class MetricsResponse(BaseModel):
    historical: list[dict]
    forecast: list[dict]

@app.get("/")
async def root():
    return {"status": "online", "message": "Agricultural Price Forecasting API"}

@app.get("/health")
async def health():
    return {"status": "healthy", "model_loaded": MODEL is not None}

@app.get("/data", response_model=MetricsResponse)
async def get_data():
    """
    Returns historical and forecasted data for dashboard charts.
    """
    cleaned_path = os.getenv('DATA_CLEANED', 'data/cleaned/cleaned_prices.csv')
    forecast_path = os.getenv('DATA_FORECASTS', 'data/forecasts/12_month_forecast.csv')
    
    if not os.path.exists(cleaned_path) or not os.path.exists(forecast_path):
        logger.error("Data files not found")
        raise HTTPException(status_code=404, detail="Data files not found. Run the pipeline first.")
    
    try:
        df_hist = pd.read_csv(cleaned_path)
        df_fore = pd.read_csv(forecast_path)
        
        return {
            "historical": df_hist.tail(24).to_dict(orient='records'),
            "forecast": df_fore.to_dict(orient='records')
        }
    except Exception as e:
        logger.error(f"Error reading data: {e}")
        raise HTTPException(status_code=500, detail="Internal server error reading data")

@app.post("/predict", response_model=PredictResponse)
async def predict(request: PredictRequest):
    if MODEL is None:
        raise HTTPException(status_code=503, detail="Model not loaded or unavailable")
    
    if len(request.last_12_months) != 12:
        raise HTTPException(status_code=400, detail="Input must contain exactly 12 months of data")
    
    try:
        # Feature engineering (match Q2 training)
        lags = request.last_12_months[::-1]
        rolling_mean = np.mean(request.last_12_months[-3:])
        features = np.array(lags + [rolling_mean]).reshape(1, -1)
        
        prediction = float(MODEL.predict(features)[0])
        
        return PredictResponse(prediction=prediction, model_type="XGBoost")
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail="Prediction failed")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv('PORT', 8000))
    host = os.getenv('HOST', '0.0.0.0')
    uvicorn.run(app, host=host, port=port)
