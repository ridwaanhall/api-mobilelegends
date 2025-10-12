"""
Hero Endpoints

This module contains all hero-related API endpoints.
"""

from typing import Dict, Any
from fastapi import APIRouter, HTTPException, Query, status
from requests.exceptions import RequestException

from app.core.config import settings
from app.core.logging import get_logger
from app.services import get_mlbb_service

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
    "/hero-list/",
    summary="Get hero list",
    description="Retrieve complete list of Mobile Legends heroes",
    response_description="List of heroes with basic information"
)
async def get_hero_list(
    lang: str = Query(
        default="en",
        description="Language code (e.g., en, id, ru)",
        example="en"
    )
) -> Dict[str, Any]:
    """
    Get complete hero list.
    
    Args:
        lang: Language code for response
        
    Returns:
        Dict[str, Any]: Hero list data
        
    Raises:
        HTTPException: If API is unavailable or request fails
    """
    check_api_availability()
    
    mlbb_service = get_mlbb_service()
    
    try:
        data = await mlbb_service.fetch_hero_list(lang=lang)
        return data
    except RequestException as e:
        logger.error(f"Failed to fetch hero list: {e}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail={
                "error": "External API Error",
                "message": "Failed to fetch data from MLBB API"
            }
        )


@router.get(
    "/hero-rank/",
    summary="Get hero rankings",
    description="Retrieve hero rankings by win rate, pick rate, or ban rate",
    response_description="Hero rankings with statistics"
)
async def get_hero_rank(
    days: str = Query(
        default="1",
        description="Time period (1, 3, 7, 15, 30 days)",
        example="7"
    ),
    rank: str = Query(
        default="all",
        description="Rank tier (all, epic, legend, mythic, honor, glory)",
        example="mythic"
    ),
    size: int = Query(
        default=20,
        ge=1,
        le=100,
        description="Number of heroes to return",
        example=20
    ),
    index: int = Query(
        default=1,
        ge=1,
        description="Page index",
        example=1
    ),
    sort_field: str = Query(
        default="win_rate",
        description="Sort field (win_rate, pick_rate, ban_rate)",
        example="win_rate"
    ),
    sort_order: str = Query(
        default="desc",
        description="Sort order (asc, desc)",
        example="desc"
    ),
    lang: str = Query(
        default="en",
        description="Language code",
        example="en"
    )
) -> Dict[str, Any]:
    """
    Get hero rankings.
    
    Args:
        days: Time period for statistics
        rank: Rank tier to filter
        size: Number of results per page
        index: Page index
        sort_field: Field to sort by
        sort_order: Sort order
        lang: Language code
        
    Returns:
        Dict[str, Any]: Hero ranking data
        
    Raises:
        HTTPException: If API is unavailable or request fails
    """
    check_api_availability()
    
    mlbb_service = get_mlbb_service()
    
    try:
        data = await mlbb_service.fetch_hero_rank(
            days=days,
            rank=rank,
            page_size=size,
            page_index=index,
            sort_field=sort_field,
            sort_order=sort_order,
            lang=lang
        )
        return data
    except RequestException as e:
        logger.error(f"Failed to fetch hero rank: {e}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail={
                "error": "External API Error",
                "message": "Failed to fetch data from MLBB API"
            }
        )


@router.get(
    "/hero-position/",
    summary="Get heroes by position",
    description="Retrieve heroes filtered by role and lane",
    response_description="Heroes matching the specified position criteria"
)
async def get_hero_position(
    role: str = Query(
        default="all",
        description="Hero role (all, tank, fighter, ass, mage, mm, supp)",
        example="mage"
    ),
    lane: str = Query(
        default="all",
        description="Hero lane (all, exp, mid, roam, jungle, gold)",
        example="mid"
    ),
    size: int = Query(
        default=21,
        ge=1,
        le=100,
        description="Number of heroes to return",
        example=21
    ),
    index: int = Query(
        default=1,
        ge=1,
        description="Page index",
        example=1
    ),
    lang: str = Query(
        default="en",
        description="Language code",
        example="en"
    )
) -> Dict[str, Any]:
    """
    Get heroes by role and lane position.
    
    Args:
        role: Hero role filter
        lane: Hero lane filter
        size: Number of results per page
        index: Page index
        lang: Language code
        
    Returns:
        Dict[str, Any]: Filtered hero data
        
    Raises:
        HTTPException: If API is unavailable or request fails
    """
    check_api_availability()
    
    mlbb_service = get_mlbb_service()
    
    try:
        data = await mlbb_service.fetch_hero_by_position(
            role=role,
            lane=lane,
            page_size=size,
            page_index=index,
            lang=lang
        )
        return data
    except RequestException as e:
        logger.error(f"Failed to fetch heroes by position: {e}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail={
                "error": "External API Error",
                "message": "Failed to fetch data from MLBB API"
            }
        )


@router.get(
    "/hero-detail/{hero_id}",
    summary="Get hero details",
    description="Retrieve detailed information about a specific hero",
    response_description="Detailed hero information"
)
async def get_hero_detail(
    hero_id: int,
    lang: str = Query(
        default="en",
        description="Language code",
        example="en"
    )
) -> Dict[str, Any]:
    """
    Get detailed hero information.
    
    Args:
        hero_id: Unique hero identifier
        lang: Language code
        
    Returns:
        Dict[str, Any]: Hero detail data
        
    Raises:
        HTTPException: If API is unavailable or request fails
    """
    check_api_availability()
    
    mlbb_service = get_mlbb_service()
    
    try:
        data = await mlbb_service.fetch_hero_detail(
            hero_id=hero_id,
            lang=lang
        )
        return data
    except RequestException as e:
        logger.error(f"Failed to fetch hero detail: {e}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail={
                "error": "External API Error",
                "message": "Failed to fetch data from MLBB API"
            }
        )


@router.get(
    "/hero-detail-stats/{main_heroid}",
    summary="Get hero statistics",
    description="Retrieve detailed statistics for a specific hero",
    response_description="Hero statistics including win rate, pick rate, etc."
)
async def get_hero_stats(
    main_heroid: int,
    lang: str = Query(
        default="en",
        description="Language code",
        example="en"
    )
) -> Dict[str, Any]:
    """
    Get hero statistics.
    
    Args:
        main_heroid: Main hero identifier
        lang: Language code
        
    Returns:
        Dict[str, Any]: Hero statistics data
        
    Raises:
        HTTPException: If API is unavailable or request fails
    """
    check_api_availability()
    
    mlbb_service = get_mlbb_service()
    
    try:
        data = await mlbb_service.fetch_hero_stats(
            main_heroid=main_heroid,
            lang=lang
        )
        return data
    except RequestException as e:
        logger.error(f"Failed to fetch hero stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail={
                "error": "External API Error",
                "message": "Failed to fetch data from MLBB API"
            }
        )


@router.get(
    "/hero-skill-combo/{hero_id}",
    summary="Get hero skill combos",
    description="Retrieve recommended skill combo sequences for a hero",
    response_description="Hero skill combo information"
)
async def get_hero_skill_combo(
    hero_id: int,
    lang: str = Query(
        default="en",
        description="Language code",
        example="en"
    )
) -> Dict[str, Any]:
    """
    Get hero skill combo information.
    
    Args:
        hero_id: Unique hero identifier
        lang: Language code
        
    Returns:
        Dict[str, Any]: Hero skill combo data
        
    Raises:
        HTTPException: If API is unavailable or request fails
    """
    check_api_availability()
    
    mlbb_service = get_mlbb_service()
    
    try:
        data = await mlbb_service.fetch_hero_skill_combo(
            hero_id=hero_id,
            lang=lang
        )
        return data
    except RequestException as e:
        logger.error(f"Failed to fetch hero skill combo: {e}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail={
                "error": "External API Error",
                "message": "Failed to fetch data from MLBB API"
            }
        )


@router.get(
    "/hero-rate/{main_heroid}",
    summary="Get hero rate over time",
    description="Retrieve hero statistics over a specified time period",
    response_description="Hero rate trends"
)
async def get_hero_rate(
    main_heroid: int,
    past_days: str = Query(
        default="7",
        alias="past-days",
        description="Time period (7, 15, 30 days)",
        example="7"
    ),
    lang: str = Query(
        default="en",
        description="Language code",
        example="en"
    )
) -> Dict[str, Any]:
    """
    Get hero rate over time.
    
    Args:
        main_heroid: Main hero identifier
        past_days: Time period for statistics
        lang: Language code
        
    Returns:
        Dict[str, Any]: Hero rate data
        
    Raises:
        HTTPException: If API is unavailable or request fails
    """
    check_api_availability()
    
    mlbb_service = get_mlbb_service()
    
    try:
        data = await mlbb_service.fetch_hero_rate(
            main_heroid=main_heroid,
            past_days=past_days,
            lang=lang
        )
        return data
    except RequestException as e:
        logger.error(f"Failed to fetch hero rate: {e}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail={
                "error": "External API Error",
                "message": "Failed to fetch data from MLBB API"
            }
        )


@router.get(
    "/hero-relation/{hero_id}",
    summary="Get hero relations",
    description="Retrieve hero relationship information",
    response_description="Hero relation data"
)
async def get_hero_relation(
    hero_id: int,
    lang: str = Query(
        default="en",
        description="Language code",
        example="en"
    )
) -> Dict[str, Any]:
    """
    Get hero relation information.
    
    Args:
        hero_id: Unique hero identifier
        lang: Language code
        
    Returns:
        Dict[str, Any]: Hero relation data
        
    Raises:
        HTTPException: If API is unavailable or request fails
    """
    check_api_availability()
    
    mlbb_service = get_mlbb_service()
    
    try:
        data = await mlbb_service.fetch_hero_relation(
            hero_id=hero_id,
            lang=lang
        )
        return data
    except RequestException as e:
        logger.error(f"Failed to fetch hero relation: {e}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail={
                "error": "External API Error",
                "message": "Failed to fetch data from MLBB API"
            }
        )


@router.get(
    "/hero-counter/{main_heroid}",
    summary="Get hero counters",
    description="Retrieve heroes that counter the specified hero",
    response_description="Hero counter information"
)
async def get_hero_counter(
    main_heroid: int,
    lang: str = Query(
        default="en",
        description="Language code",
        example="en"
    )
) -> Dict[str, Any]:
    """
    Get hero counter information.
    
    Args:
        main_heroid: Main hero identifier
        lang: Language code
        
    Returns:
        Dict[str, Any]: Hero counter data
        
    Raises:
        HTTPException: If API is unavailable or request fails
    """
    check_api_availability()
    
    mlbb_service = get_mlbb_service()
    
    try:
        data = await mlbb_service.fetch_hero_counter(
            main_heroid=main_heroid,
            lang=lang
        )
        return data
    except RequestException as e:
        logger.error(f"Failed to fetch hero counter: {e}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail={
                "error": "External API Error",
                "message": "Failed to fetch data from MLBB API"
            }
        )


@router.get(
    "/hero-compatibility/{main_heroid}",
    summary="Get hero compatibility",
    description="Retrieve heroes that synergize well with the specified hero",
    response_description="Hero compatibility information"
)
async def get_hero_compatibility(
    main_heroid: int,
    lang: str = Query(
        default="en",
        description="Language code",
        example="en"
    )
) -> Dict[str, Any]:
    """
    Get hero compatibility information.
    
    Args:
        main_heroid: Main hero identifier
        lang: Language code
        
    Returns:
        Dict[str, Any]: Hero compatibility data
        
    Raises:
        HTTPException: If API is unavailable or request fails
    """
    check_api_availability()
    
    mlbb_service = get_mlbb_service()
    
    try:
        data = await mlbb_service.fetch_hero_compatibility(
            main_heroid=main_heroid,
            lang=lang
        )
        return data
    except RequestException as e:
        logger.error(f"Failed to fetch hero compatibility: {e}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail={
                "error": "External API Error",
                "message": "Failed to fetch data from MLBB API"
            }
        )
