"use client";

import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { LayoutDashboard, AlertCircle, RefreshCcw } from 'lucide-react';
import PriceChart from '@/components/PriceChart';
import PredictionForm from '@/components/PredictionForm';
import StrategyCards from '@/components/StrategyCards';

interface HistoricalPrice {
  date: string;
  avg_monthly_price: number;
}

interface ForecastPrice {
  date: string;
  forecasted_price: number;
}

interface DataState {
  historical: HistoricalPrice[];
  forecast: ForecastPrice[];
}

export default function Dashboard() {
  const [data, setData] = useState<DataState | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = async () => {
    setLoading(true);
    try {
      const res = await axios.get(`${process.env.NEXT_PUBLIC_API_URL}/data`);
      setData(res.data);
      setError(null);
    } catch {
      setError("Unable to connect to the prediction engine. Please ensure the backend is running.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    fetchData();
  }, []);

  return (
    <main className="min-h-screen bg-slate-50 font-sans text-slate-900">
      {/* Header */}
      <nav className="bg-white border-b border-slate-200 px-8 py-4 sticky top-0 z-10 shadow-sm">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
              <RefreshCcw className="text-white w-5 h-5" />
            </div>
            <h1 className="text-xl font-bold tracking-tight">AgriPrice <span className="text-blue-600">Predict</span></h1>
          </div>
          <div className="text-sm font-medium text-slate-500 bg-slate-100 px-3 py-1 rounded-full border border-slate-200">
            v1.0.0 Alpha
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-8 py-8">
        <div className="flex items-center gap-2 mb-8">
          <LayoutDashboard className="w-6 h-6 text-slate-400" />
          <h2 className="text-2xl font-bold text-slate-800">Supply Chain Intelligence Dashboard</h2>
        </div>

        {error && (
          <div className="mb-8 p-4 bg-red-50 border border-red-100 rounded-xl flex items-center gap-3 text-red-700">
            <AlertCircle className="w-5 h-5" />
            <p className="text-sm font-medium">{error}</p>
            <button onClick={fetchData} className="ml-auto underline font-bold">Retry</button>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left/Middle: Charts and Strategies */}
          <div className="lg:col-span-2 space-y-8">
            {loading ? (
              <div className="h-[400px] bg-slate-100 animate-pulse rounded-xl" />
            ) : data ? (
              <PriceChart historical={data.historical} forecast={data.forecast} />
            ) : (
              <div className="h-[400px] bg-white border border-dashed border-slate-300 rounded-xl flex items-center justify-center text-slate-400">
                Data unavailable. Run backend pipeline.
              </div>
            )}

            <section>
              <h3 className="text-lg font-semibold mb-4 text-slate-800">Mitigation Strategies</h3>
              <StrategyCards />
            </section>
          </div>

          {/* Right: Prediction Form & Quick Metrics */}
          <div className="space-y-8">
            <PredictionForm />
            
            <div className="bg-slate-900 rounded-xl p-6 text-white shadow-xl">
              <h4 className="text-slate-400 text-xs font-bold uppercase mb-4 tracking-wider">Model Status</h4>
              <div className="space-y-4">
                <div className="flex justify-between items-center border-b border-slate-800 pb-2">
                  <span className="text-sm text-slate-300">Active Model</span>
                  <span className="text-sm font-mono text-emerald-400">XGBoost v2.1</span>
                </div>
                <div className="flex justify-between items-center border-b border-slate-800 pb-2">
                  <span className="text-sm text-slate-300">Last Training</span>
                  <span className="text-sm text-slate-400">May 30, 2026</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-slate-300">Confidence Score</span>
                  <span className="text-sm font-bold text-blue-400">94.2%</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
