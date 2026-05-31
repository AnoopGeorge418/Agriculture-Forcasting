"use client";

import React, { useState } from 'react';
import axios from 'axios';
import { Loader2, TrendingUp } from 'lucide-react';

const PredictionForm = () => {
  const [inputs, setInputs] = useState<string[]>(Array(12).fill(''));
  const [prediction, setPrediction] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    
    const numericInputs = inputs.map(v => parseFloat(v));
    if (numericInputs.some(isNaN)) {
      setError("Please fill all 12 months with valid numbers.");
      setLoading(false);
      return;
    }

    try {
      const res = await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/predict`, {
        last_12_months: numericInputs
      });
      setPrediction(res.data.prediction);
    } catch {
      setError("Failed to get prediction. Ensure backend is running.");
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (index: number, value: string) => {
    const newInputs = [...inputs];
    newInputs[index] = value;
    setInputs(newInputs);
  };

  return (
    <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-100">
      <h3 className="text-lg font-semibold mb-4 text-slate-800 flex items-center gap-2">
        <TrendingUp className="w-5 h-5 text-blue-600" />
        Real-time Inference
      </h3>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-4 gap-2">
          {inputs.map((val, i) => (
            <div key={i}>
              <label className="text-[10px] uppercase font-bold text-slate-400 block mb-1">M-{12-i}</label>
              <input
                type="number"
                value={val}
                onChange={(e) => handleInputChange(i, e.target.value)}
                placeholder="Price"
                className="w-full p-2 border border-slate-200 rounded text-sm focus:ring-2 focus:ring-blue-500 outline-none"
              />
            </div>
          ))}
        </div>
        <button
          type="submit"
          disabled={loading}
          className="w-full py-2 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition disabled:opacity-50 flex items-center justify-center gap-2"
        >
          {loading ? <Loader2 className="animate-spin w-4 h-4" /> : "Predict Next Month"}
        </button>
      </form>
      
      {prediction && (
        <div className="mt-4 p-4 bg-blue-50 rounded-lg border border-blue-100">
          <p className="text-sm text-blue-800 font-medium">Forecasted Price:</p>
          <p className="text-2xl font-bold text-blue-600">${prediction.toFixed(2)}</p>
        </div>
      )}
      
      {error && <p className="mt-2 text-red-500 text-sm">{error}</p>}
    </div>
  );
};

export default PredictionForm;
