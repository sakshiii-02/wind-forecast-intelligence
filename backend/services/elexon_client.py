
from datetime import datetime, timezone

import httpx

BASE_URL = "https://data.elexon.co.uk/bmrs/api/v1/datasets"


async def fetch_dataset(
    dataset: str,
    start: datetime,
    end: datetime,
) -> list[dict]:

    params = {
        "publishDateTimeFrom": start.astimezone(timezone.utc).isoformat(),
        "publishDateTimeTo": end.astimezone(timezone.utc).isoformat(),
    }

    url = f"{BASE_URL}/{dataset}/stream"

    async with httpx.AsyncClient(timeout=90.0) as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        payload = response.json()

    if isinstance(payload, list):
        return payload

    if isinstance(payload, dict) and isinstance(payload.get("data"), list):
        return payload["data"]

    raise ValueError(f"Unexpected response from {dataset}")
