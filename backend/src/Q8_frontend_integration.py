"""
Agricultural Price Forecasting - Frontend Integration Modules
"""

# 1. Next.js / TypeScript API Service
NEXTJS_CLIENT = """
import axios from 'axios';

interface ForecastData {
  prediction: number;
  model_type: string;
}

export const fetchPrediction = async (data: number[]): Promise<ForecastData> => {
  try {
    const response = await axios.post('http://localhost:8000/predict', {
      last_12_months: data
    });
    return response.data;
  } catch (error) {
    console.error('Inference Error:', error);
    throw error;
  }
};
"""

# 2. React Native Hook for Mobile
REACT_NATIVE_HOOK = """
import { useState, useEffect } from 'react';
import axios from 'axios';

export const useAgriForecast = (historicalData) => {
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const getForecast = async () => {
      try {
        const res = await axios.post('https://api.yourdomain.com/predict', {
          last_12_months: historicalData
        });
        setPrediction(res.data.prediction);
      } catch (err) {
        setError('Failed to fetch forecast');
      } finally {
        setLoading(false);
      }
    };

    if (historicalData && historicalData.length === 12) {
      getForecast();
    }
  }, [historicalData]);

  return { prediction, loading, error };
};
"""

if __name__ == "__main__":
    print("Frontend Integration Blocks Generated.")
    print("--- Next.js Client ---")
    print(NEXTJS_CLIENT)
    print("\n--- React Native Hook ---")
    print(REACT_NATIVE_HOOK)
