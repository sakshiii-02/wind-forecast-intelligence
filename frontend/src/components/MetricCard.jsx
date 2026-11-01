
function MetricCard({ title, value, unit, description }) {
  return (
    <div className="metric-card">
      <p className="metric-title">{title}</p>

      <div className="metric-value">
        {value}
        {unit && <span>{unit}</span>}
      </div>

      <p className="metric-description">{description}</p>
    </div>
  );
}

export default MetricCard;
