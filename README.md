# Wind Forecast Intelligence

A data analytics dashboard for evaluating UK wind generation forecasts against actual generation during January 2026.

The application uses Elexon BMRS data to compare forecast and actual wind generation, measure forecast accuracy, identify daily performance patterns, and export analytical results.

## Features

- January 2026 wind generation analysis
- Actual vs. forecast generation comparison
- Forecast accuracy metrics:
  - Mean Absolute Error (MAE)
  - Root Mean Squared Error (RMSE)
  - Forecast Bias
  - Mean Absolute Percentage Error (MAPE)
- Forecast coverage measurement
- Daily performance and error analysis
- Date-based filtering
- CSV export of daily analytics
- Interactive charts and KPI cards
- Docker-based local setup

## Technology Stack

**Frontend**
- React
- Vite
- Recharts
- Lucide React

**Backend**
- Python
- FastAPI
- Pandas
- HTTPX

**Testing and Deployment**
- Pytest
- Docker
- Docker Compose
- Nginx

## Data Source

Data is sourced from the [Elexon BMRS API](https://data.elexon.co.uk/).

The analysis uses:

- `FUELHH` — actual generation data, filtered to the WIND fuel type.
- `WINDFOR` — wind generation forecast data.

The application analyses delivery periods in January 2026. Data is downloaded with a surrounding date range to support the forecast publication selection process, then filtered to the January delivery period.

## Methodology

### 1. Actual generation

FUELHH actual generation records are filtered to wind generation and January 2026 delivery periods.

The latest available published actual record is retained for each settlement period. Half-hourly generation values are then aggregated into hourly averages to align with the forecast analysis.

### 2. Forecast selection

Forecast records contain both a delivery timestamp and a publication timestamp.

To avoid using forecasts published after the delivery period, the analysis applies the following decision-time assumption:

**For each delivery date, select the latest forecast published on or before 10:00 AM UK local time on the previous calendar day.**

This is an analytical assumption used for consistent comparison; it is not presented as an official Elexon market deadline.

### 3. Accuracy calculation

Selected forecasts are matched with actual generation for the corresponding hourly delivery periods.

The following metrics are calculated:

| Metric | Description |
|---|---|
| MAE | Average absolute difference between forecast and actual generation |
| RMSE | Square root of the average squared forecast error |
| Bias | Average forecast minus actual generation; positive values indicate overforecasting |
| MAPE | Average absolute percentage error |
| Coverage | Percentage of actual hourly periods with a matching selected forecast |

Coverage measures data matching, not forecast accuracy.

### 4. Daily analysis

Hourly records are grouped by UK local delivery date. Daily generation values represent average MW across the matched hourly periods. Daily accuracy metrics are calculated from the hourly errors for each day.

## Project Structure
wind-forecast-intelligence/
├── backend/
│   ├── data/
│   │   └── raw/
│   ├── routes/
│   ├── scripts/
│   ├── services/
│   ├── tests/
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   └── utils/
│   ├── Dockerfile
│   └── nginx.conf
├── docker-compose.yml
└── README.md

## Run Locally

### Prerequisites

- Python 3.12 or later
- Node.js and npm
- Docker Desktop (optional, for containerized setup)

### 1. Clone the repository
git clone https://github.com/sakshiii-02/wind-forecast-intelligence.git
cd wind-forecast-intelligence

### 2. Start the backend
cd backend
python -m venv .venv

Activate the virtual environment:

Windows PowerShell:
.venv\Scripts\Activate.ps1

Install dependencies:
pip install -r requirements.txt

Start the API:
uvicorn main:app --reload

Backend URLs:

- Health check: `http://127.0.0.1:8000/health`
- API documentation: `http://127.0.0.1:8000/docs`

### 3. Start the frontend

Open another terminal:
cd frontend
npm install

Create a `.env` file in the frontend directory:

VITE_API_BASE_URL=http://127.0.0.1:8000

Start the development server:
npm run dev


Open `http://localhost:5173`.

## Run with Docker

From the project root:
docker compose up --build

The application will be available at:

- Frontend: `http://localhost:5173`
- Backend: `http://localhost:8000`
- API documentation: `http://localhost:8000/docs`

To stop the containers:
docker compose down

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Backend health check |
| GET | `/api/analytics/january` | January summary and hourly analysis |
| GET | `/api/analytics/january/daily` | Daily generation and accuracy metrics |

## Running Tests

From the backend directory, activate the virtual environment and run:
python -m pytest tests/ -v

The test suite covers hourly aggregation, forecast selection, accuracy calculations, coverage handling, and daily analytics.

## AI Tool Disclosure

ChatGPT was used as an AI-assisted development tool during this project for implementation guidance, code suggestions, debugging support, and documentation refinement.

The project code, analytical assumptions, and results were reviewed and tested during development.

## Notes and Limitations

- The analysis is limited to January 2026.
- Forecast selection uses the explicitly stated 10:00 AM previous-day decision-time assumption.
- Actual and forecast generation are compared at hourly resolution.
- Accuracy metrics are calculated only for matched hourly periods.
- Results depend on the source data available from Elexon BMRS at the time of retrieval.
