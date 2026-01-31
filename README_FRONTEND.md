# Engine Health Monitoring System - Frontend

Modern, user-friendly web interface for the Adaptive Engine Health Monitoring System.

## Features

- 🎨 Beautiful, modern UI with Tailwind CSS
- 📊 Real-time engine health metrics visualization
- 🚗 Multi-vehicle support with easy selection
- 📈 Interactive dashboard with health scores
- 💡 AI-powered explanations and recommendations
- 🔄 Auto-refresh every 5 seconds
- 📱 Responsive design for all devices

## Getting Started

### Prerequisites

- Node.js 18+ installed
- Backend API running on http://localhost:8000

### Installation

```bash
npm install
```

### Development

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Build for Production

```bash
npm run build
npm start
```

## Deployment to Vercel

1. Push your code to GitHub
2. Go to [vercel.com](https://vercel.com)
3. Import your repository
4. Configure environment variables:
   - `NEXT_PUBLIC_API_URL`: Your backend API URL
5. Deploy!

Or use Vercel CLI:

```bash
npm i -g vercel
vercel
```

## Environment Variables

Create a `.env.local` file:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

For production, set this in Vercel dashboard.

## Project Structure

```
app/
  page.tsx          # Main page
  layout.tsx        # Root layout
  globals.css       # Global styles
components/
  Dashboard.tsx     # Main dashboard
  VehicleSelector.tsx
  HealthScoreCard.tsx
  MetricCard.tsx
  StatusBadge.tsx
  ExplanationCard.tsx
  LoadingSpinner.tsx
```

## API Integration

The frontend connects to the FastAPI backend at the URL specified in `NEXT_PUBLIC_API_URL`.

Required endpoints:
- `GET /vehicles` - Get list of vehicles
- `GET /engine-status?vehicle_id={id}` - Get engine status


