
import json
from pathlib import Path

from services.forecast_analyzer import (
    prepare_actuals,
    prepare_forecasts,
    select_decision_forecasts,
    calculate_accuracy,
)


DATA_DIR = Path("data/raw")


def load_json(filename):
    with open(DATA_DIR / filename, "r") as file:
        return json.load(file)


def main():

    print("Loading historical Elexon data...")

    actual_records = load_json("actual_wind_jan_2026.json")
    forecast_records = load_json("wind_forecasts_jan_2026.json")

    print("Preparing actual generation...")
    actuals = prepare_actuals(actual_records)

    print("Preparing forecast publications...")
    forecasts = prepare_forecasts(forecast_records)

    print("Selecting decision-time forecasts...")
    selected = select_decision_forecasts(forecasts)

    print("Calculating accuracy...")
    results = calculate_accuracy(actuals, selected)

    print("\n========== JANUARY 2026 RESULTS ==========")

    for key, value in results["summary"].items():
        print(f"{key}: {value}")

    print("\nFirst five matched records:")

    for record in results["records"][:5]:
        print({
            "startTime": str(record["startTime"]),
            "actual": record["actual_generation"],
            "forecast": record["forecast_generation"],
            "error": record["error"],
        })

    print("\n==========================================")


if __name__ == "__main__":
    main()
