from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/api/addon", tags=["addon"])


@router.get("/win-rate", summary="Win Rate Calculator for Consecutive Wins")
def win_rate(
    match_now: Annotated[
        str | None,
        Query(alias="match-now", description="Current total matches. Must be an integer >= 0."),
    ] = None,
    wr_now: Annotated[
        str | None,
        Query(alias="wr-now", description="Current win rate in percent. Range: 0-100."),
    ] = None,
    wr_future: Annotated[
        str | None,
        Query(
            alias="wr-future",
            description="Target win rate in percent. Range: >0 to 100 and must be greater than wr-now.",
        ),
    ] = None,
) -> object:
    missing_params = [
        param
        for param, value in [("match-now", match_now), ("wr-now", wr_now), ("wr-future", wr_future)]
        if value is None or value == ""
    ]
    if missing_params:
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "match_now": match_now,
                "wr_now": wr_now,
                "wr_future": wr_future,
                "required_no_lose_matches": None,
                "message": (
                    f"Missing required parameter(s): {', '.join(missing_params)}. "
                    "Please provide all required parameters: match-now, wr-now, and wr-future."
                ),
            },
        )

    try:
        if "." in str(match_now):
            raise ValueError("match-now must be an integer (no decimals allowed).")
        match_now_int = int(str(match_now))
        wr_now_float = float(str(wr_now))
        wr_future_float = float(str(wr_future))
    except ValueError:
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "match_now": match_now,
                "wr_now": wr_now,
                "wr_future": wr_future,
                "required_no_lose_matches": None,
                "message": "Invalid input. Ensure match-now is an integer and wr-now, wr-future are numeric values.",
            },
        )

    if match_now_int < 0:
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "match_now": match_now_int,
                "wr_now": wr_now_float,
                "wr_future": wr_future_float,
                "required_no_lose_matches": None,
                "message": "match-now must be a non-negative integer.",
            },
        )

    if not (0 <= wr_now_float <= 100) or not (0 < wr_future_float <= 100):
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "match_now": match_now_int,
                "wr_now": wr_now_float,
                "wr_future": wr_future_float,
                "required_no_lose_matches": None,
                "message": "Win rates must be between 0 and 100 (wr-future must be greater than 0).",
            },
        )

    if wr_future_float <= wr_now_float:
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "match_now": match_now_int,
                "wr_now": wr_now_float,
                "wr_future": wr_future_float,
                "required_no_lose_matches": None,
                "message": "The target win rate (wr-future) must be greater than the current win rate (wr-now).",
            },
        )

    current_wins = match_now_int * wr_now_float / 100.0
    wr_future_ratio = wr_future_float / 100.0
    denominator = wr_future_ratio - 1.0
    numerator = current_wins - match_now_int * wr_future_ratio

    if denominator == 0:
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "match_now": match_now_int,
                "wr_now": wr_now_float,
                "wr_future": wr_future_float,
                "required_no_lose_matches": None,
                "message": f"It is not possible to reach a {wr_future_float}% win rate with a finite number of matches.",
            },
        )

    required_matches = numerator / denominator
    required_matches_int = int(required_matches) + (1 if required_matches % 1 > 0 else 0)

    if required_matches_int < 0:
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "match_now": match_now_int,
                "wr_now": wr_now_float,
                "wr_future": wr_future_float,
                "required_no_lose_matches": None,
                "message": "The target win rate cannot be achieved with only consecutive wins from your current record.",
            },
        )

    return {
        "status": "success",
        "match_now": match_now_int,
        "wr_now": wr_now_float,
        "wr_future": wr_future_float,
        "required_no_lose_matches": required_matches_int,
        "message": (
            f"To achieve a win rate of {wr_future_float}%, "
            f"you need {required_matches_int} consecutive wins without any losses."
        ),
    }
