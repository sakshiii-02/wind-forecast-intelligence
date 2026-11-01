
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

function DailyPerformanceChart({ records }) {
  const chartData = records.map((record) => ({
    date: record.date.slice(8),
    actual: record.actual_generation,
    forecast: record.forecast_generation
  }));

  return (
    <div className="chart-card">
      <div className="chart-heading">
        <div>
          <h2>Daily Generation Trend</h2>
          <p>Average daily actual vs forecast generation · MW</p>
        </div>
      </div>

      <div className="chart-container">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={chartData}>
            <CartesianGrid
              strokeDasharray="3 3"
              vertical={false}
            />

            <XAxis
              dataKey="date"
              label={{
                value: "January 2026",
                position: "insideBottom",
                offset: -5
              }}
            />

            <YAxis
              width={75}
              tickFormatter={(value) =>
                `${(value / 1000).toFixed(0)}k`
              }
            />

            <Tooltip
              formatter={(value) =>
                `${Number(value).toLocaleString()} MW`
              }
              labelFormatter={(label) => `January ${label}`}
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

export default DailyPerformanceChart;
