
import { useEffect, useState } from "react";

import Sidebar from "./components/Sidebar";
import Header from "./components/Header";
import MetricCard from "./components/MetricCard";
import GenerationChart from "./components/GenerationChart";
import {
  getJanuaryAnalytics,
  getDailyAnalytics
} from "./services/analyticsApi";

import DailyPerformanceChart from "./components/DailyPerformanceChart";
import DailyErrorAnalysis from "./components/DailyErrorAnalysis";
import ForecastInsights from "./components/ForecastInsights";
import DailyErrorChart from "./components/DailyErrorChart";
import { exportDailyAnalytics } from "./utils/exportCsv";

import "./App.css";

function App() {
  const [analytics, setAnalytics] = useState(null);
  const [dailyAnalytics, setDailyAnalytics] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [selectedDate, setSelectedDate] = useState("2026-01-01");
  const [startDate, setStartDate] = useState("2026-01-01");
  const [endDate, setEndDate] = useState("2026-01-31");


useEffect(() => {
  async function loadAnalytics() {
    try {
      const [monthlyData, dailyData] = await Promise.all([
        getJanuaryAnalytics(),
        getDailyAnalytics()
      ]);

      setAnalytics(monthlyData);
      setDailyAnalytics(dailyData);

    } catch (err) {
      setError(err.message);

    } finally {
      setLoading(false);
    }
  }

  loadAnalytics();
}, []);


  if (loading) {
    return <div className="loading">Loading wind analytics...</div>;
  }

  if (error) {
    return <div className="error">{error}</div>;
  }

  const summary = analytics.summary;
  const filteredRecords = analytics.records.filter((record) => {
  const recordDate = new Date(record.startTime)
    .toLocaleDateString("en-CA", {
      timeZone: "Europe/London"
    });

  return recordDate === selectedDate;
});

const filteredDailyAnalytics = dailyAnalytics.filter(
  (record) => record.date >= startDate && record.date <= endDate
);

  return (
    <div className="app-layout">
      <Sidebar />

      <main className="main-content">
        <Header />

        <section className="metrics-grid">
          <MetricCard
            title="Mean Absolute Error"
            value={summary.mae?.toLocaleString()}
            unit="MW"
            description="Average absolute forecast error"
          />

          <MetricCard
            title="Root Mean Square Error"
            value={summary.rmse?.toLocaleString()}
            unit="MW"
            description="Penalises larger forecast errors"
          />

          <MetricCard
            title="Forecast Bias"
            value={`${summary.bias > 0 ? "+" : ""}${summary.bias?.toLocaleString()}`}
            unit="MW"
            description={
              summary.bias > 0
                ? "Average over-forecast"
                : summary.bias < 0
                ? "Average under-forecast"
                : "No average bias"
            }
          />

          <MetricCard
            title="Data Coverage"
            value={`${summary.coverage_percent}%`}
            description={`${summary.matched_periods} of ${summary.actual_periods} hourly periods matched`}
          />
        </section>

        <div className="filter-section">
        <div>
          <label htmlFor="start-date">Start Date</label>
          <input
            id="start-date"
            type="date"
            min="2026-01-01"
            max={endDate}
            value={startDate}
            onChange={(event) => setStartDate(event.target.value)}
          />
        </div>

          <div>
            <label htmlFor="end-date">End Date</label>
            <input
              id="end-date"
              type="date"
              min={startDate}
              max="2026-01-31"
              value={endDate}
              onChange={(event) => setEndDate(event.target.value)}
            />
          </div>

          <button
            className="export-button"
            onClick={() => exportDailyAnalytics(filteredDailyAnalytics)}
          >
            Download CSV
          </button>
        </div>

        <ForecastInsights records={filteredDailyAnalytics} />

        <div className="filter-section">
          <label htmlFor="delivery-date">Select delivery date</label>

          <input
            id="delivery-date"
            type="date"
            min="2026-01-01"
            max="2026-01-31"
            value={selectedDate}
            onChange={(event) => setSelectedDate(event.target.value)}
          />
        </div>

        <GenerationChart records={filteredRecords} />

        <DailyPerformanceChart records={filteredDailyAnalytics} />
        <DailyErrorChart records={filteredDailyAnalytics} />
        <DailyErrorAnalysis records={filteredDailyAnalytics} />
        <div className="methodology-note">
          <h3>Forecast selection methodology</h3>
          <p>
            For each delivery period, the latest WINDFOR forecast
            published by 10:00 AM UK time on the previous calendar
            day is selected. This is an analytical assumption.
          </p>
        </div>
      </main>
    </div>
  );
}

export default App;
