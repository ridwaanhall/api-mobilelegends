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
