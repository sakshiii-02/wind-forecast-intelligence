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