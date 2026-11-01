
import pandas as pd

from zoneinfo import ZoneInfo

UK_TZ = ZoneInfo("Europe/London")

DELIVERY_START = pd.Timestamp("2026-01-01", tz=UK_TZ)
DELIVERY_END = pd.Timestamp("2026-02-01", tz=UK_TZ)



def prepare_actuals(records):
    """Convert half-hourly actuals into hourly average generation."""

    df = pd.DataFrame(records)

    if df.empty:
        return pd.DataFrame(
            columns=["startTime", "actual_generation"]
        )

    df["startTime"] = pd.to_datetime(
        df["startTime"], utc=True, errors="coerce"
    )

    df["publishTime"] = pd.to_datetime(
        df["publishTime"], utc=True, errors="coerce"
    )

    df["generation"] = pd.to_numeric(
        df["generation"], errors="coerce"
    )

    df = df.dropna(
        subset=["startTime", "generation"]
    )

    local_delivery = df["startTime"].dt.tz_convert(
        "Europe/London"
    )

    df = df[
        (local_delivery >= DELIVERY_START)
        & (local_delivery < DELIVERY_END)
    ].copy()

    # Keep the latest published actual for each half-hour period.
    df = df.sort_values("publishTime")

    df = df.drop_duplicates(
        subset=["startTime"],
        keep="last"
    )

    # Group half-hourly observations into hourly periods.
    df["hour"] = df["startTime"].dt.floor("h")

    hourly = (
        df.groupby("hour")
        .agg(
            actual_generation=("generation", "mean"),
            half_hour_count=("generation", "count")
        )
        .reset_index()
    )

    # Require both half-hourly observations for a complete hour.
    hourly = hourly[
        hourly["half_hour_count"] == 2
    ].copy()

    return hourly.rename(
        columns={"hour": "startTime"}
    )

def prepare_forecasts(records):
    """Prepare historical wind forecast publications."""

    df = pd.DataFrame(records)

    if df.empty:
        return pd.DataFrame(
            columns=[
                "startTime",
                "publishTime",
                "generation"
            ]
        )

    df["startTime"] = pd.to_datetime(
        df["startTime"], utc=True, errors="coerce"
    )

    df["publishTime"] = pd.to_datetime(
        df["publishTime"], utc=True, errors="coerce"
    )

    df["generation"] = pd.to_numeric(
        df["generation"], errors="coerce"
    )

    df = df.dropna(
        subset=["startTime", "publishTime", "generation"]
    )

    local_delivery = df["startTime"].dt.tz_convert(
        "Europe/London"
    )

    df = df[
        (local_delivery >= DELIVERY_START)
        & (local_delivery < DELIVERY_END)
    ].copy()

    return df


def select_decision_forecasts(forecasts):
    """
    Select the latest forecast published by 10:00 AM UK time
    on the calendar day before each delivery date.
    """

    if forecasts.empty:
        return forecasts.copy()

    df = forecasts.copy()

    local_delivery = df["startTime"].dt.tz_convert(
        "Europe/London"
    )

    delivery_dates = local_delivery.dt.date

    cutoff_dates = pd.to_datetime(
        delivery_dates
    ) - pd.Timedelta(days=1)

    cutoff_times = [
        pd.Timestamp(date).tz_localize(
            UK_TZ
        ) + pd.Timedelta(hours=10)
        for date in cutoff_dates
    ]

    df["decision_cutoff"] = pd.to_datetime(
        cutoff_times, utc=True
    )

    # Only forecasts available at the decision cutoff.
    df = df[
        df["publishTime"] <= df["decision_cutoff"]
    ].copy()

    # Select the latest eligible publication for each delivery period.
    df = df.sort_values(
        ["startTime", "publishTime"]
    )

    df = df.drop_duplicates(
        subset=["startTime"],
        keep="last"
    )

    return df


def calculate_accuracy(actuals, selected_forecasts):
    """Match forecasts with actuals and calculate accuracy metrics."""

    merged = actuals.merge(
        selected_forecasts[
            ["startTime", "generation", "publishTime",
             "decision_cutoff"]
        ],
        on="startTime",
        how="left"
    )

    merged = merged.rename(
        columns={"generation": "forecast_generation"}
    )

    matched = merged.dropna(
        subset=["forecast_generation"]
    ).copy()

    if matched.empty:
        return {
            "summary": {
                "actual_periods": len(actuals),
                "matched_periods": 0,
                "coverage_percent": 0,
                "mae": None,
                "rmse": None,
                "bias": None,
                "mape": None
            },
            "records": []
        }

    matched["error"] = (
        matched["forecast_generation"]
        - matched["actual_generation"]
    )

    matched["absolute_error"] = matched["error"].abs()

    matched["squared_error"] = matched["error"] ** 2

    nonzero_actuals = matched[
        matched["actual_generation"] != 0
    ]

    mape = None

    if not nonzero_actuals.empty:
        mape = (
            (
                nonzero_actuals["error"].abs()
                / nonzero_actuals["actual_generation"].abs()
            ).mean() * 100
        )

    summary = {
        "actual_periods": int(len(actuals)),
        "matched_periods": int(len(matched)),
        "coverage_percent": round(
            len(matched) / len(actuals) * 100, 2
        ) if len(actuals) else 0,
        "mae": round(matched["absolute_error"].mean(), 2),
        "rmse": round(
            matched["squared_error"].mean() ** 0.5, 2
        ),
        "bias": round(matched["error"].mean(), 2),
        "mape": round(mape, 2) if mape is not None else None
    }

    return {
        "summary": summary,
        "records": matched.to_dict(orient="records")
    }
