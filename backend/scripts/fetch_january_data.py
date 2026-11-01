
import asyncio
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

from services.elexon_client import fetch_dataset


DATA_DIR = Path("data/raw")
DATA_DIR.mkdir(parents=True, exist_ok=True)


async def fetch_month(dataset, start_date, end_date):

    all_records = []

    current = start_date

    while current < end_date:

        next_date = current + timedelta(days=1)

        start = datetime.combine(
            current, datetime.min.time(), tzinfo=timezone.utc
        )

        end = datetime.combine(
            next_date, datetime.min.time(), tzinfo=timezone.utc
        )

        print(f"{dataset}: Fetching {current}...")

        records = await fetch_dataset(dataset, start, end)

        print(f"  Retrieved {len(records)} records")

        all_records.extend(records)

        current = next_date

    return all_records


async def main():

    # Include previous-day publications for January 1 delivery.
    start_date = datetime(2025, 12, 30).date()
    end_date = datetime(2026, 2, 2).date()

    # Fetch actual generation.
    actual_records = await fetch_month(
        "FUELHH", start_date, end_date
    )

    # Keep only national wind generation.
    actual_wind = [
        record for record in actual_records
        if record.get("fuelType") == "WIND"
    ]

    # Fetch all historical wind forecast publications.
    forecast_records = await fetch_month(
        "WINDFOR", start_date, end_date
    )

    with open(DATA_DIR / "actual_wind_jan_2026.json", "w") as file:
        json.dump(actual_wind, file, indent=2)

    with open(DATA_DIR / "wind_forecasts_jan_2026.json", "w") as file:
        json.dump(forecast_records, file, indent=2)

    print("\nData ingestion completed.")
    print(f"Actual wind records: {len(actual_wind)}")
    print(f"Forecast records: {len(forecast_records)}")


if __name__ == "__main__":
    asyncio.run(main())
