
from fastapi import APIRouter, HTTPException

from services.analytics_service import (
    get_january_analysis,
    get_daily_analysis,
)

router = APIRouter(
    prefix="/api/analytics",
    tags=["Analytics"]
)


@router.get("/january")
def get_january_analytics():
    try:
        return get_january_analysis()

    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="January 2026 dataset not found."
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to calculate analytics: {str(error)}"
        )

@router.get("/january/daily")
def get_january_daily_analytics():
    try:
        return get_daily_analysis()

    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="January 2026 dataset not found."
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to calculate daily analytics: {str(error)}"
        )
