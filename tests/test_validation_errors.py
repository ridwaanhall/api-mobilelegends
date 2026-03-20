from __future__ import annotations

from fastapi.testclient import TestClient


import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.core import hero_limits
from app.main import app


client = TestClient(app)


def test_mlbb_hero_rank_rejects_invalid_days_enum() -> None:
    response = client.get("/api/hero-rank?days=2")

    assert response.status_code == 422
    payload = response.json()
    assert payload["code"] == "VALIDATION_ERROR"
    assert payload["status"] == "error"


def test_mlbb_hero_rank_rejects_size_below_minimum() -> None:
    response = client.get("/api/hero-rank?size=0")

    assert response.status_code == 422
    payload = response.json()
    assert payload["code"] == "VALIDATION_ERROR"
    assert payload["status"] == "error"


def test_academy_guide_stats_rejects_hero_id_below_range() -> None:
    response = client.get("/api/academy/guide/0/stats")

    assert response.status_code == 422
    payload = response.json()
    assert payload["code"] == "VALIDATION_ERROR"
    assert payload["status"] == "error"


def test_academy_guide_trends_rejects_invalid_days_enum() -> None:
    response = client.get("/api/academy/guide/1/trends?days=5")

    assert response.status_code == 422
    payload = response.json()
    assert payload["code"] == "VALIDATION_ERROR"
    assert payload["status"] == "error"


def test_validation_error_payload_contains_details_list() -> None:
    response = client.get("/api/hero-position?role=invalid-role")

    assert response.status_code == 422
    payload = response.json()
    assert payload["code"] == "VALIDATION_ERROR"
    assert isinstance(payload["details"], list)
    assert len(payload["details"]) > 0


def test_academy_dynamic_max_hero_id_rejects_above_live_total(monkeypatch) -> None:
    def fake_fetch(endpoint_id: str, payload: dict, lang: str) -> object:
        if endpoint_id == "2766683":
            return {"code": 0, "message": "OK", "data": {"total": 132}}
        return {"code": 0, "message": "OK", "data": []}

    hero_limits.clear_hero_max_cache()
    monkeypatch.setattr(hero_limits, "fetch_academy_post", fake_fetch)

    response = client.get("/api/academy/guide/133/stats")

    assert response.status_code == 422
    payload = response.json()
    assert payload["code"] == "VALIDATION_ERROR"
    assert payload["status"] == "error"


def test_academy_dynamic_max_hero_id_accepts_current_live_total(monkeypatch) -> None:
    def fake_fetch(endpoint_id: str, payload: dict, lang: str) -> object:
        if endpoint_id == "2766683":
            return {"code": 0, "message": "OK", "data": {"total": 132}}
        return {"code": 0, "message": "OK", "data": []}

    hero_limits.clear_hero_max_cache()
    monkeypatch.setattr(hero_limits, "fetch_academy_post", fake_fetch)

    response = client.get("/api/academy/guide/132/stats")

    assert response.status_code == 200


def test_mlbb_dynamic_max_hero_id_rejects_above_live_total(monkeypatch) -> None:
    def fake_fetch(endpoint_id: str, payload: dict, lang: str) -> object:
        if endpoint_id == "2756564":
            return {
                "code": 0,
                "message": "OK",
                "data": {
                    "records": [
                        {
                            "data": {
                                "hero_id": 132,
                            }
                        }
                    ]
                },
            }
        return {"code": 0, "message": "OK", "data": []}

    hero_limits.clear_hero_max_cache()
    monkeypatch.setattr(hero_limits, "fetch_mlbb_post", fake_fetch)

    response = client.get("/api/hero-detail/133")

    assert response.status_code == 422
    payload = response.json()
    assert payload["code"] == "VALIDATION_ERROR"
    assert payload["status"] == "error"


def test_win_rate_missing_params_returns_standardized_error() -> None:
    response = client.get("/api/addon/win-rate")

    assert response.status_code == 400
    payload = response.json()
    assert payload["status"] == "error"
    assert payload["code"] == "BAD_REQUEST"
    assert "timestamp" in payload
    assert "support" in payload
    assert payload["required_no_lose_matches"] is None


def test_win_rate_invalid_input_returns_standardized_error() -> None:
    response = client.get("/api/addon/win-rate?match-now=abc&wr-now=50&wr-future=60")

    assert response.status_code == 400
    payload = response.json()
    assert payload["status"] == "error"
    assert payload["code"] == "BAD_REQUEST"
    assert "timestamp" in payload
    assert "support" in payload


def test_win_rate_negative_match_now_returns_standardized_error() -> None:
    response = client.get("/api/addon/win-rate?match-now=-1&wr-now=50&wr-future=60")

    assert response.status_code == 400
    payload = response.json()
    assert payload["status"] == "error"
    assert payload["code"] == "BAD_REQUEST"
    assert "timestamp" in payload
    assert "support" in payload


def test_win_rate_future_wr_not_greater_than_now_returns_standardized_error() -> None:
    response = client.get("/api/addon/win-rate?match-now=100&wr-now=60&wr-future=50")

    assert response.status_code == 400
    payload = response.json()
    assert payload["status"] == "error"
    assert payload["code"] == "BAD_REQUEST"
    assert "timestamp" in payload
    assert "support" in payload


def test_win_rate_wr_out_of_range_returns_standardized_error() -> None:
    # wr-now above 100 should trigger win-rate range validation
    response = client.get("/api/addon/win-rate?match-now=100&wr-now=150&wr-future=160")

    assert response.status_code == 400
    payload = response.json()
    assert payload["status"] == "error"
    assert payload["code"] == "BAD_REQUEST"
    assert "timestamp" in payload
    assert "support" in payload
    # domain extra field should be present in standardized error
    assert "required_no_lose_matches" in payload


def test_win_rate_future_100_denominator_zero_returns_standardized_error() -> None:
    # wr-future=100 is a special case that can cause a zero denominator in calculations
    response = client.get("/api/addon/win-rate?match-now=100&wr-now=50&wr-future=100")

    assert response.status_code == 400
    payload = response.json()
    assert payload["status"] == "error"
    assert payload["code"] == "BAD_REQUEST"
    assert "timestamp" in payload
    assert "support" in payload
    assert "required_no_lose_matches" in payload


def test_win_rate_negative_required_matches_returns_standardized_error() -> None:
    # Parameter combination intended to reach the branch where required_matches_int < 0
    response = client.get("/api/addon/win-rate?match-now=1&wr-now=99&wr-future=100")

    assert response.status_code == 400
    payload = response.json()
    assert payload["status"] == "error"
    assert payload["code"] == "BAD_REQUEST"
    assert "timestamp" in payload
    assert "support" in payload
    assert "required_no_lose_matches" in payload

def test_mlbb_dynamic_max_hero_id_accepts_current_live_total(monkeypatch) -> None:
    def fake_fetch(endpoint_id: str, payload: dict, lang: str) -> object:
        if endpoint_id == "2756564":
            return {
                "code": 0,
                "message": "OK",
                "data": {
                    "records": [
                        {
                            "data": {
                                "hero_id": 132,
                            }
                        }
                    ]
                },
            }
        return {"code": 0, "message": "OK", "data": []}

    hero_limits.clear_hero_max_cache()
    monkeypatch.setattr(hero_limits, "fetch_mlbb_post", fake_fetch)

    response = client.get("/api/hero-detail/132")

    assert response.status_code == 200
