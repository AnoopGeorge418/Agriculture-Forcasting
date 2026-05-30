"use client";

import React from 'react';
import { ShieldCheck, ArrowRightLeft, LayoutGrid, Database } from 'lucide-react';

const strategies = [
  {
    title: "Dynamic Hedging",
    desc: "Utilize futures and options contracts to lock in prices during high volatility phases.",
    icon: <ShieldCheck className="w-6 h-6 text-emerald-600" />,
    bg: "bg-emerald-50"
  },
  {
    title: "Contract Indexed Pricing",
    desc: "Shift from fixed-price to indexed contracts incorporating price floors and caps.",
    icon: <ArrowRightLeft className="w-6 h-6 text-blue-600" />,
    bg: "bg-blue-50"
  },
  {
    title: "Geographic Diversification",
    desc: "Source from alternative regions with different seasonal patterns to offset local spikes.",
    icon: <LayoutGrid className="w-6 h-6 text-purple-600" />,
    bg: "bg-purple-50"
  },
  {
    title: "Buffer Management",
    desc: "Optimized inventory levels based on predicted surges to minimize spot market exposure.",
    icon: <Database className="w-6 h-6 text-amber-600" />,
    bg: "bg-amber-50"
  }
];

const StrategyCards = () => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {strategies.map((s, i) => (
        <div key={i} className="p-4 bg-white rounded-xl border border-slate-100 shadow-sm hover:border-blue-200 transition group">
          <div className={`w-12 h-12 ${s.bg} rounded-lg flex items-center justify-center mb-3 group-hover:scale-110 transition`}>
            {s.icon}
          </div>
          <h4 className="font-semibold text-slate-800 mb-1">{s.title}</h4>
          <p className="text-sm text-slate-500 leading-relaxed">{s.desc}</p>
        </div>
      ))}
    </div>
  );
};

export default StrategyCards;
