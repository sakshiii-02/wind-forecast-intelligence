
import json
from pathlib import Path

from services.forecast_analyzer import (
    prepare_actuals,
    prepare_forecasts,
    select_decision_forecasts,
    calculate_accuracy,
)


DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"


def load_json(filename):
    file_path = DATA_DIR / filename

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def get_january_analysis():
    actual_records = load_json("actual_wind_jan_2026.json")
    forecast_records = load_json("wind_forecasts_jan_2026.json")

    actuals = prepare_actuals(actual_records)
    forecasts = prepare_forecasts(forecast_records)

    selected_forecasts = select_decision_forecasts(forecasts)

    results = calculate_accuracy(
        actuals,
        selected_forecasts
    )

    return results


import pandas as pd


def get_daily_analysis():
    """Calculate daily wind generation and forecast accuracy metrics."""

    results = get_january_analysis()

    df = pd.DataFrame(results["records"])

    if df.empty:
        return []

    df["startTime"] = pd.to_datetime(
        df["startTime"],
        utc=True
    )

    # Use UK local delivery dates.
    df["delivery_date"] = (
        df["startTime"]
        .dt.tz_convert("Europe/London")
        .dt.strftime("%Y-%m-%d")
    )

    df["percentage_error"] = (
        df["absolute_error"]
        / df["actual_generation"].abs().replace(0, float("nan"))
    ) * 100

    daily = (
        df.groupby("delivery_date")
        .agg(
            actual_generation=("actual_generation", "mean"),
            forecast_generation=("forecast_generation", "mean"),
            mae=("absolute_error", "mean"),
            mean_squared_error=("squared_error", "mean"),
            bias=("error", "mean"),
            mape=("percentage_error", "mean"),
            matched_periods=("startTime", "count"),
        )
        .reset_index()
    )

    daily["rmse"] = daily["mean_squared_error"] ** 0.5

    daily = daily.drop(columns=["mean_squared_error"])

    numeric_columns = [
        "actual_generation",
        "forecast_generation",
        "mae",
        "rmse",
        "bias",
        "mape",
    ]

    daily[numeric_columns] = daily[numeric_columns].round(2)

    daily = daily.rename(
        columns={"delivery_date": "date"}
    )

    return daily.where(pd.notna(daily), None).to_dict(
        orient="records"
    )
