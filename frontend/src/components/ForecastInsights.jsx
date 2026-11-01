
import { TrendingUp, TrendingDown, Activity } from "lucide-react";

function ForecastInsights({ records }) {
  if (!records || records.length === 0) {
    return null;
  }

  const highestErrorDay = [...records].sort(
    (a, b) => b.mae - a.mae
  )[0];

  const overForecastDay = [...records]
    .filter((record) => record.bias > 0)
    .sort((a, b) => b.bias - a.bias)[0];

  const underForecastDay = [...records]
    .filter((record) => record.bias < 0)
    .sort((a, b) => a.bias - b.bias)[0];

  const insights = [
    {
      title: "Highest forecast error",
      date: highestErrorDay.date,
      value: `${highestErrorDay.mae.toLocaleString()} MW`,
      description: "Highest daily MAE",
      icon: Activity,
      className: "insight-error"
    },
    {
      title: "Largest over-forecast",
      date: overForecastDay?.date ?? "N/A",
      value: overForecastDay
        ? `+${overForecastDay.bias.toLocaleString()} MW`
        : "N/A",
      description: "Forecast exceeded actual generation",
      icon: TrendingUp,
      className: "insight-over"
    },
    {
      title: "Largest under-forecast",
      date: underForecastDay?.date ?? "N/A",
      value: underForecastDay
        ? `${underForecastDay.bias.toLocaleString()} MW`
        : "N/A",
      description: "Forecast was below actual generation",
      icon: TrendingDown,
      className: "insight-under"
    }
  ];

  return (
    <section className="insights-section">
      <div className="section-heading">
        <h2>Key Forecast Insights</h2>
        <p>Important findings from January 2026</p>
      </div>

      <div className="insights-grid">
        {insights.map((insight) => {
          const Icon = insight.icon;

          return (
            <div
              className={`insight-card ${insight.className}`}
              key={insight.title}
            >
              <div className="insight-icon">
                <Icon size={20} />
              </div>

              <p className="insight-title">{insight.title}</p>

              <h3>{insight.value}</h3>

              <p className="insight-description">
                {insight.description}
              </p>

              <span className="insight-date">
                {insight.date}
              </span>
            </div>
          );
        })}
      </div>
    </section>
  );
}

export default ForecastInsights;
