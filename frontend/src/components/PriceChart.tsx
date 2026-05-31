"use client";

import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

interface HistoricalPrice {
  date: string;
  avg_monthly_price: number;
}

interface ForecastPrice {
  date: string;
  forecasted_price: number;
}

interface PriceChartProps {
  historical: HistoricalPrice[];
  forecast: ForecastPrice[];
}

const PriceChart: React.FC<PriceChartProps> = ({ historical, forecast }) => {
  // Combine data for charting
  const data = [
    ...historical.map(d => ({ date: d.date, historical: d.avg_monthly_price })),
    ...forecast.map(d => ({ date: d.date, forecast: d.forecasted_price }))
  ];

  return (
    <div className="h-[400px] w-full bg-white p-4 rounded-xl shadow-sm border border-slate-100">
      <h3 className="text-lg font-semibold mb-4 text-slate-800">Price Trend & Forecast</h3>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
          <XAxis 
            dataKey="date" 
            tick={{ fontSize: 12 }} 
            tickFormatter={(str) => new Date(str).toLocaleDateString('en-US', { month: 'short', year: '2-digit' })}
          />
          <YAxis tick={{ fontSize: 12 }} />
          <Tooltip 
            contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
          />
          <Legend />
          <Line 
            type="monotone" 
            dataKey="historical" 
            stroke="#2563eb" 
            strokeWidth={2} 
            dot={false} 
            name="Historical" 
          />
          <Line 
            type="monotone" 
            dataKey="forecast" 
            stroke="#ef4444" 
            strokeWidth={2} 
            strokeDasharray="5 5" 
            name="Forecast" 
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default PriceChart;
