
import json
import pandas as pd
from pathlib import Path

DATA_DIR = Path("data/raw")


def load_data(filename):
    with open(DATA_DIR / filename, "r") as file:
        return json.load(file)


def inspect_timestamps(name, records):

    df = pd.DataFrame(records)

    df["startTime"] = pd.to_datetime(
        df["startTime"], utc=True
    )

    print(f"\n========== {name} ==========")
    print("Total records:", len(df))

    print("\nFirst 10 delivery timestamps:")
    print(df["startTime"].sort_values().head(10).to_string(index=False))

    print("\nMinute distribution:")
    print(
        df["startTime"].dt.minute.value_counts().sort_index()
    )

    print("\nUnique delivery hours:")
    print(
        df["startTime"].dt.hour.value_counts().sort_index()
    )

    print("\nTime difference distribution:")

    differences = (
        df["startTime"]
        .drop_duplicates()
        .sort_values()
        .diff()
        .value_counts()
    )

    print(differences.head(10))


def main():

    actuals = load_data("actual_wind_jan_2026.json")
    forecasts = load_data("wind_forecasts_jan_2026.json")

    inspect_timestamps("ACTUALS", actuals)
    inspect_timestamps("FORECASTS", forecasts)


if __name__ == "__main__":
    main()
