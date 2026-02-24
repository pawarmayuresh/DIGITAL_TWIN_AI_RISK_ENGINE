# AI Strategic Risk Engine - Frontend

React-based frontend for the disaster simulation and risk management system.

## Features

- **City Overview**: Real-time city metrics and status
- **Spatial Grid**: Visualize spatial disaster propagation
- **Disaster Simulation**: Run and analyze disaster scenarios
- **Infrastructure Graph**: Network dependencies and cascading failures
- **Policy Comparison**: Compare different response strategies
- **Resilience Dashboard**: City resilience metrics and trends
- **Risk Heatmap**: Spatial risk distribution
- **Decision Explainability**: Understand AI decision-making

## Tech Stack

- React 18
- Vite
- React Router
- Axios
- Lucide React (icons)
- Recharts (charts)

## Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start development server:
```bash
npm run dev
```

The app will be available at http://localhost:8081

## API Configuration

The frontend connects to the backend API at `http://localhost:8000` by default.

To change this, create a `.env` file:
```
VITE_API_URL=http://your-api-url:8000
```

## Build for Production

```bash
npm run build
```

The built files will be in the `dist` directory.

## Project Structure

```
frontend/
├── src/
│   ├── components/     # Reusable components
│   ├── pages/          # Page components
│   ├── services/       # API services
│   ├── App.jsx         # Main app component
│   └── main.jsx        # Entry point
├── index.html
├── package.json
└── vite.config.js
```

## Development

- All pages are in `src/pages/`
- Shared components in `src/components/`
- API calls in `src/services/api.js`
- Routing configured in `src/App.jsx`
