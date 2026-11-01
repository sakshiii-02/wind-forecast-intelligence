
function escapeCsvValue(value) {
  const safeValue = String(value ?? "");

  return `"${safeValue.replace(/"/g, '""')}"`;
}

export function exportDailyAnalytics(records) {
  if (!records || records.length === 0) {
    alert("No data available to export.");
    return;
  }

  const headers = [
    "Date",
    "Actual Generation (MW)",
    "Forecast Generation (MW)",
    "MAE (MW)",
    "RMSE (MW)",
    "Bias (MW)",
    "MAPE (%)",
    "Matched Periods"
  ];

  const rows = records.map((record) => [
    record.date,
    record.actual_generation,
    record.forecast_generation,
    record.mae,
    record.rmse,
    record.bias,
    record.mape,
    record.matched_periods
  ]);

  const csvContent = [
    headers.map(escapeCsvValue).join(","),
    ...rows.map((row) => row.map(escapeCsvValue).join(","))
  ].join("\r\n");

  const blob = new Blob(["\uFEFF", csvContent], {
    type: "text/csv;charset=utf-8;"
  });

  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");

  link.href = url;
  link.download = "wind-forecast-daily-analysis.csv";
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);

  URL.revokeObjectURL(url);
}
