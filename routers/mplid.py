"""MPL ID API Router for FastAPI"""
from fastapi import APIRouter, HTTPException, Request
from typing import List, Dict, Any
import sys
import os

# Add apps directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'apps'))

from mpl_api import scraper, serializers

router = APIRouter(prefix="/mplid", tags=["MPL ID API"])


def serialize_data(serializer_class, data, many=False):
    """Serialize data using DRF serializers and return dict"""
    serializer = serializer_class(data, many=many)
    return serializer.data


@router.get("/")
async def mplid_api_list(request: Request):
    """List all MPL ID API endpoints"""
    base_url = str(request.base_url)
    api_list = [
        {"name": "Standings", "url": f"{base_url}api/mplid/standings/"},
        {"name": "Teams", "url": f"{base_url}api/mplid/teams/"},
        {"name": "Team Detail", "url": f"{base_url}api/mplid/teams/<team_id>/"},
        {"name": "Transfers", "url": f"{base_url}api/mplid/transfers/"},
        {"name": "Team Stats", "url": f"{base_url}api/mplid/team-stats/"},
        {"name": "Player Stats", "url": f"{base_url}api/mplid/player-stats/"},
        {"name": "Hero Stats", "url": f"{base_url}api/mplid/hero-stats/"},
        {"name": "Hero Pools", "url": f"{base_url}api/mplid/hero-pools/"},
        {"name": "Player Pools", "url": f"{base_url}api/mplid/player-pools/"},
        {"name": "Standings MVP", "url": f"{base_url}api/mplid/standings-mvp/"},
        {"name": "Schedule (All)", "url": f"{base_url}api/mplid/schedule/"},
        {"name": "Schedule by Week", "url": f"{base_url}api/mplid/schedule/week/<week_number>/"},
        {"name": "All Weeks", "url": f"{base_url}api/mplid/schedule/week/"},
    ]
    return api_list


@router.get("/standings/")
async def mplid_standings():
    """Get MPL ID standings"""
    try:
        data = scraper.MPLIDStandingsScraper().get_standings()
        return serialize_data(serializers.MPLIDStandingSerializer, data, many=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/teams/")
async def mplid_teams():
    """Get MPL ID teams"""
    try:
        data = scraper.MPLIDTeamScraper().get_teams()
        return serialize_data(serializers.MPLTeamIDSerializer, data, many=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/teams/{team_id}/")
async def mplid_team_detail(team_id: str):
    """Get MPL ID team details"""
    try:
        data = scraper.MPLIDTeamDetailScraper(team_id).get_team_details()
        return serialize_data(serializers.MPLIDTeamDetailSerializer, data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/transfers/")
async def mplid_transfers():
    """Get MPL ID transfers"""
    try:
        data = scraper.MPLIDTransferScraper().get_transfers()
        return serialize_data(serializers.MPLIDTransferSerializer, data, many=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/team-stats/")
async def mplid_team_stats():
    """Get MPL ID team stats"""
    try:
        data = scraper.MPLIDTeamStatsScraper().get_team_stats()
        return serialize_data(serializers.MPLIDTeamStatSerializer, data, many=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/player-stats/")
async def mplid_player_stats():
    """Get MPL ID player stats"""
    try:
        data = scraper.MPLIDPlayerStatsScraper().get_player_stats()
        return serialize_data(serializers.MPLIDPlayerStatSerializer, data, many=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/hero-stats/")
async def mplid_hero_stats():
    """Get MPL ID hero stats"""
    try:
        data = scraper.MPLIDHeroStatsScraper().get_hero_stats()
        return serialize_data(serializers.MPLIDHeroStatSerializer, data, many=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/hero-pools/")
async def mplid_hero_pools():
    """Get MPL ID hero pools"""
    try:
        data = scraper.MPLIDHeroPoolsScraper().get_hero_pools()
        return serialize_data(serializers.MPLIDHeroPoolSerializer, data, many=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/player-pools/")
async def mplid_player_pools():
    """Get MPL ID player pools"""
    try:
        data = scraper.MPLIDPlayerPoolsScraper().get_player_pools()
        return serialize_data(serializers.MPLIDPlayerPoolSerializer, data, many=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/standings-mvp/")
async def mplid_standings_mvp():
    """Get MPL ID standings MVP"""
    try:
        data = scraper.MPLIDStandingsMVPScraper().get_standings_mvp()
        return serialize_data(serializers.MPLIDStandingsMVPSerializer, data, many=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/schedule/")
async def mplid_schedule():
    """Get MPL ID schedule"""
    try:
        data = scraper.MPLIDScheduleScraper().get_schedule()
        return serialize_data(serializers.MPLIDScheduleSerializer, data, many=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/schedule/week/")
async def mplid_schedule_all_weeks():
    """Get all MPL ID schedule weeks"""
    try:
        data = scraper.MPLIDScheduleAllWeeksScraper().get_schedule_weeks()
        return serialize_data(serializers.MPLIDScheduleWeekSerializer, data, many=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/schedule/week/{week_number}/")
async def mplid_schedule_week(week_number: int):
    """Get MPL ID schedule for specific week"""
    try:
        data = scraper.MPLIDScheduleWeekScraper(week_number).get_schedule_week()
        return serialize_data(serializers.MPLIDScheduleSerializer, data, many=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
