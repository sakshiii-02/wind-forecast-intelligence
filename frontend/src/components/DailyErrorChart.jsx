
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from "recharts";

function DailyErrorChart({ records }) {
  const chartData = records.map((record) => ({
    date: record.date.slice(8),
    mae: record.mae
  }));

  return (
    <div className="chart-card">
      <div className="chart-heading">
        <div>
          <h2>Daily Forecast Error (MAE)</h2>
          <p>Mean absolute error for each day · MW</p>
        </div>
      </div>

      <div className="chart-container">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={chartData}>
            <CartesianGrid
              strokeDasharray="3 3"
              vertical={false}
            />

            <XAxis
              dataKey="date"
              tickFormatter={(value) => `${value} Jan`}
              interval={2}
            />

            <YAxis
              width={75}
              tickFormatter={(value) =>
                `${(value / 1000).toFixed(1)}k`
              }
            />

            <Tooltip
              labelFormatter={(value) => `January ${value}`}
              formatter={(value) => [
                `${Number(value).toLocaleString()} MW`,
                "MAE"
              ]}
            />

            <Bar
              dataKey="mae"
              name="Daily MAE"
              fill="#3978d4"
              radius={[4, 4, 0, 0]}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default DailyErrorChart;
