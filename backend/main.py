import os
import sys
import argparse
from dotenv import load_dotenv

# Add the current directory to sys.path to allow imports from src
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.Q1_data_cleaning import clean_data
from src.Q2_eda_and_model import perform_eda, train_sarima, train_xgboost, train_lstm
from src.Q3_evaluation import evaluate_models, generate_forecast

def run_pipeline():
    print("--- Starting Data Pipeline ---")
    df = clean_data()
    perform_eda(df)
    train_sarima(df)
    train_xgboost(df)
    train_lstm(df)
    evaluate_models(df)
    generate_forecast(df)
    print("--- Pipeline Completed Successfully ---")

def start_server():
    print("--- Starting FastAPI Server ---")
    import uvicorn
    from src.Q7_fastapi_integration import app
    port = int(os.getenv('PORT', 8000))
    host = os.getenv('HOST', '0.0.0.0')
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    load_dotenv()
    
    parser = argparse.ArgumentParser(description="AgriPrice Forecasting Backend Control")
    parser.add_argument("command", choices=["pipeline", "server", "all"], help="Command to run")
    
    args = parser.parse_args()
    
    if args.command == "pipeline":
        run_pipeline()
    elif args.command == "server":
        start_server()
    elif args.command == "all":
        run_pipeline()
        start_server()
