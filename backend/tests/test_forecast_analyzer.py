
import pandas as pd

from services.forecast_analyzer import (
    prepare_actuals,
    select_decision_forecasts,
    calculate_accuracy,
)


def test_prepare_actuals_aggregates_half_hourly_records():
    records = [
        {
            "startTime": "2026-01-01T00:00:00Z",
            "publishTime": "2026-01-01T01:00:00Z",
            "generation": 1000,
        },
        {
            "startTime": "2026-01-01T00:30:00Z",
            "publishTime": "2026-01-01T01:00:00Z",
            "generation": 1200,
        },
    ]

    result = prepare_actuals(records)

    assert len(result) == 1
    assert result.iloc[0]["actual_generation"] == 1100


def test_select_decision_forecasts_uses_latest_eligible_publication():
    forecasts = pd.DataFrame([
        {
            "startTime": pd.Timestamp("2026-01-02T12:00:00Z"),
            "publishTime": pd.Timestamp("2026-01-01T08:00:00Z"),
            "generation": 1000,
        },
        {
            "startTime": pd.Timestamp("2026-01-02T12:00:00Z"),
            "publishTime": pd.Timestamp("2026-01-01T09:00:00Z"),
            "generation": 1100,
        },
        {
            "startTime": pd.Timestamp("2026-01-02T12:00:00Z"),
            "publishTime": pd.Timestamp("2026-01-01T11:00:00Z"),
            "generation": 1200,
        },
    ])

    result = select_decision_forecasts(forecasts)

    assert len(result) == 1
    assert result.iloc[0]["generation"] == 1100


def test_calculate_accuracy_returns_correct_metrics():
    actuals = pd.DataFrame({
        "startTime": [
            pd.Timestamp("2026-01-01T00:00:00Z"),
            pd.Timestamp("2026-01-01T01:00:00Z"),
        ],
        "actual_generation": [1000, 2000],
    })

    forecasts = pd.DataFrame({
        "startTime": [
            pd.Timestamp("2026-01-01T00:00:00Z"),
            pd.Timestamp("2026-01-01T01:00:00Z"),
        ],
        "generation": [1100, 1800],
        "publishTime": [
            pd.Timestamp("2025-12-31T08:00:00Z"),
            pd.Timestamp("2025-12-31T08:00:00Z"),
        ],
        "decision_cutoff": [
            pd.Timestamp("2025-12-31T10:00:00Z"),
            pd.Timestamp("2025-12-31T10:00:00Z"),
        ],
    })

    result = calculate_accuracy(actuals, forecasts)
    summary = result["summary"]

    assert summary["actual_periods"] == 2
    assert summary["matched_periods"] == 2
    assert summary["coverage_percent"] == 100
    assert summary["mae"] == 150
    assert summary["bias"] == -50


def test_calculate_accuracy_handles_missing_forecast():
    actuals = pd.DataFrame({
        "startTime": [
            pd.Timestamp("2026-01-01T00:00:00Z"),
            pd.Timestamp("2026-01-01T01:00:00Z"),
        ],
        "actual_generation": [1000, 2000],
    })

    forecasts = pd.DataFrame({
        "startTime": [
            pd.Timestamp("2026-01-01T00:00:00Z"),
        ],
        "generation": [1100],
        "publishTime": [
            pd.Timestamp("2025-12-31T08:00:00Z"),
        ],
        "decision_cutoff": [
            pd.Timestamp("2025-12-31T10:00:00Z"),
        ],
    })

    result = calculate_accuracy(actuals, forecasts)
    summary = result["summary"]

    assert summary["actual_periods"] == 2
    assert summary["matched_periods"] == 1
    assert summary["coverage_percent"] == 50


from services.analytics_service import get_daily_analysis


def test_daily_analysis_returns_31_days():
    records = get_daily_analysis()

    assert len(records) == 31
    assert records[0]["date"] == "2026-01-01"
    assert records[-1]["date"] == "2026-01-31"


def test_daily_analysis_has_required_fields():
    records = get_daily_analysis()

    required_fields = {
        "date",
        "actual_generation",
        "forecast_generation",
        "mae",
        "rmse",
        "bias",
        "mape",
        "matched_periods",
    }

    for record in records:
        assert required_fields.issubset(record.keys())


def test_daily_analysis_has_valid_metrics():
    records = get_daily_analysis()

    for record in records:
        assert record["actual_generation"] >= 0
        assert record["forecast_generation"] >= 0
        assert record["mae"] >= 0
        assert record["rmse"] >= 0
        assert record["mape"] >= 0
        assert record["matched_periods"] > 0
