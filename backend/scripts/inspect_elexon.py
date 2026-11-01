
import asyncio
import json
from datetime import datetime, timezone

from services.elexon_client import fetch_dataset


async def main():
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    end = datetime(2026, 1, 2, tzinfo=timezone.utc)

    for dataset in ("FUELHH", "WINDFOR"):
        print(f"\nInspecting {dataset}...")

        try:
            records = await fetch_dataset(dataset, start, end)

            print(f"Records returned: {len(records)}")

            if records:
                print("First record:")
                print(json.dumps(records[0], indent=2))

                print("Available fields:")
                print(sorted(records[0].keys()))
            else:
                print("No records returned for this window.")

        except Exception as exc:
            print(f"Request failed: {type(exc).__name__}: {exc}")


if __name__ == "__main__":
    asyncio.run(main())
