"""
Utility Endpoints

This module contains utility API endpoints like win rate calculator.
"""

from typing import Optional
from fastapi import APIRouter, HTTPException, Query, status
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.logging import get_logger
from app.services import get_calculation_service
from app.models.response import WinRateCalculation

logger = get_logger(__name__)
router = APIRouter()


def check_api_availability() -> None:
    """
    Check if API endpoints are available.
    
    Raises:
        HTTPException: If API is not available
    """
    if not settings.IS_AVAILABLE:
        status_info = settings.api_status_messages["limited"]
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "error": "Service Unavailable",
                "status": status_info["status"],
                "message": status_info["message"],
                "available_endpoints": status_info["available_endpoints"]
            }
        )


@router.get(
    "/win-rate/",
    summary="Calculate win rate",
    description="Calculate required matches to reach target win rate",
    response_description="Win rate calculation result",
    response_model=WinRateCalculation
)
async def calculate_win_rate(
    match_now: Optional[int] = Query(
        None,
        alias="match-now",
        ge=0,
        description="Current number of matches played",
        example=100
    ),
    wr_now: Optional[float] = Query(
        None,
        alias="wr-now",
        ge=0,
        le=100,
        description="Current win rate percentage (0-100)",
        example=50.0
    ),
    wr_future: Optional[float] = Query(
        None,
        alias="wr-future",
        gt=0,
        le=100,
        description="Target win rate percentage (0-100)",
        example=75.0
    )
) -> JSONResponse:
    """
    Calculate required consecutive wins to reach target win rate.
    
    This endpoint helps players determine how many consecutive wins
    they need to achieve their desired win rate.
    
    Args:
        match_now: Current number of matches played
        wr_now: Current win rate percentage
        wr_future: Target win rate percentage
        
    Returns:
        JSONResponse: Calculation result with required wins
        
    Raises:
        HTTPException: If API is unavailable or parameters are invalid
    """
    check_api_availability()
    
    # Validate required parameters
    missing_params = []
    if match_now is None:
        missing_params.append("match-now")
    if wr_now is None:
        missing_params.append("wr-now")
    if wr_future is None:
        missing_params.append("wr-future")
    
    if missing_params:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "status": "error",
                "match_now": match_now,
                "wr_now": wr_now,
                "wr_future": wr_future,
                "required_no_lose_matches": None,
                "message": (
                    f"Missing required parameter(s): {', '.join(missing_params)}. "
                    "Please provide all required parameters: match-now, wr-now, "
                    "and wr-future."
                )
            }
        )
    
    calculation_service = get_calculation_service()
    
    try:
        result = calculation_service.calculate_required_wins(
            current_matches=match_now,
            current_win_rate=wr_now,
            target_win_rate=wr_future
        )
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=result
        )
    except ValueError as e:
        logger.warning(f"Invalid calculation parameters: {e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "status": "error",
                "match_now": match_now,
                "wr_now": wr_now,
                "wr_future": wr_future,
                "required_no_lose_matches": None,
                "message": str(e)
            }
        )
    except Exception as e:
        logger.error(f"Unexpected error in win rate calculation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Calculation Error",
                "message": "An unexpected error occurred during calculation"
            }
        )
