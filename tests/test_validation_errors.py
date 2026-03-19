from __future__ import annotations

from fastapi.testclient import TestClient

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
