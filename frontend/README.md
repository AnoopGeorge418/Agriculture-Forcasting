# AgriPrice Predict - Premium Dashboard

A modern, responsive supply chain intelligence dashboard for visualizing agricultural price forecasts and making data-driven decisions.

## Tech Stack
- **Framework**: Next.js 14 (App Router)
- **Styling**: Tailwind CSS
- **Charts**: Recharts
- **Icons**: Lucide React
- **API Client**: Axios
- **Deployment**: Vercel

## Features
- **Interactive Trends**: Visual historical and forecasted price comparisons.
- **Real-time Prediction**: On-the-fly inference form to test model predictions.
- **Strategy Insights**: Actionable corporate mitigation strategies.
- **Responsive Design**: Optimized for desktop and mobile environments.

## Getting Started

### Local Setup
1. Install dependencies:
   ```bash
   npm install
   ```
2. Configure environment:
   ```bash
   cp .env.example .env.local
   # Set NEXT_PUBLIC_API_URL to your backend URL (default: http://localhost:8000)
   ```
3. Run development server:
   ```bash
   npm run dev
   ```

## Deployment
This frontend is optimized for **Vercel**. Connect your repository and ensure `NEXT_PUBLIC_API_URL` is set to your production backend.
