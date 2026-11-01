
function DailyErrorAnalysis({ records }) {
  const sortedRecords = [...records].sort(
    (a, b) => b.mae - a.mae
  );

  return (
    <div className="chart-card">
      <div className="chart-heading">
        <div>
          <h2>Daily Forecast Error Analysis</h2>
          <p>Days ranked by mean absolute error (MAE)</p>
        </div>
      </div>

      <div className="error-table-wrapper">
        <table className="error-table">
          <thead>
            <tr>
              <th>Date</th>
              <th>Actual (MW)</th>
              <th>Forecast (MW)</th>
              <th>MAE (MW)</th>
              <th>Bias (MW)</th>
              <th>MAPE (%)</th>
            </tr>
          </thead>

          <tbody>
            {sortedRecords.map((record) => (
              <tr key={record.date}>
                <td>{record.date}</td>

                <td>
                  {record.actual_generation.toLocaleString()}
                </td>

                <td>
                  {record.forecast_generation.toLocaleString()}
                </td>

                <td className="error-value">
                  {record.mae.toLocaleString()}
                </td>

                <td>
                  {record.bias > 0 ? "+" : ""}
                  {record.bias.toLocaleString()}
                </td>

                <td>
                  {record.mape == null
                    ? "N/A"
                    : record.mape.toFixed(2) + "%"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default DailyErrorAnalysis;