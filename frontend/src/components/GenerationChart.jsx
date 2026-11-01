
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend
} from "recharts";

function GenerationChart({ records }) {
  const chartData = records.map((record) => ({
    time: new Date(record.startTime).toLocaleString("en-GB", {
      day: "2-digit",
      hour: "2-digit",
      minute: "2-digit",
      timeZone: "Europe/London"
    }),
    actual: record.actual_generation,
    forecast: record.forecast_generation
  }));

  return (
    
    <div className="chart-card">
      <div className="chart-heading">
        <div>
          <h2>Actual vs Forecast Generation</h2>
          <p>Hourly wind generation · January 2026</p>
        </div>
      </div>

      <div className="chart-container">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} />

            <XAxis
              dataKey="time"
              minTickGap={40}
            />

            <YAxis
              width={75}
              tickFormatter={(value) => `${(value / 1000).toFixed(0)}k`}
            />

            <Tooltip
              formatter={(value) => [
                `${Number(value).toLocaleString()} MW`
              ]}
            />

            <Legend />

            <Line
              type="monotone"
              dataKey="actual"
              name="Actual"
              stroke="#16a36a"
              strokeWidth={2}
              dot={false}
            />

            <Line
              type="monotone"
              dataKey="forecast"
              name="Forecast"
              stroke="#3978d4"
              strokeWidth={2}
              dot={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default GenerationChart;
