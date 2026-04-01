from __future__ import annotations

import os
import sys

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.main import app


client = TestClient(app)


def test_openapi_user_read_endpoints_use_get_and_authorization_header() -> None:
    openapi = client.get("/api/openapi.json").json()

    read_paths = [
        "/api/user/info",
        "/api/user/stats",
        "/api/user/season",
        "/api/user/matches",
        "/api/user/matches/{match_id}",
        "/api/user/heroes/frequent",
        "/api/user/friends",
    ]

    for path in read_paths:
        assert "get" in openapi["paths"][path]
        assert "post" not in openapi["paths"][path]
        assert {"HTTPBearer": []} in openapi["paths"][path]["get"]["security"]

    logout_op = openapi["paths"].get("/api/user/auth/logout", {}).get("post", {})
    assert {"HTTPBearer": []} in logout_op.get("security", [])
    assert "requestBody" not in logout_op
    logout_schema = logout_op.get("responses", {}).get("200", {}).get("content", {}).get("application/json", {}).get("schema", {})
    assert logout_schema.get("$ref") == "#/components/schemas/UserAuthSimpleResponse"

    login_op = openapi["paths"].get("/api/user/auth/login", {}).get("post", {})
    login_schema = login_op.get("responses", {}).get("200", {}).get("content", {}).get("application/json", {}).get("schema", {})
    assert login_schema.get("$ref") == "#/components/schemas/UserLoginResponse"


def test_user_info_endpoint_strips_bearer_before_forwarding_upstream(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, str] = {}

    def fake_fetch_user_post(path: str, headers: dict[str, str], payload: dict[str, object]) -> dict[str, object]:
        captured["path"] = path
        captured["authorization"] = headers["authorization"]
        captured["x-token"] = headers["x-token"]
        return {"code": 0, "data": "", "msg": "ok"}

    monkeypatch.setattr("app.api.routers.user.fetch_user_post", fake_fetch_user_post)

    response = client.get(
        "/api/user/info?lang=en",
        headers={"Authorization": "Bearer test-jwt-token"},
    )

    assert response.status_code == 200
    assert captured["path"] == "base/getBaseInfo"
    assert captured["authorization"] == "test-jwt-token"
    assert captured["x-token"] == "test-jwt-token"


def test_user_logout_uses_authorization_header(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, str] = {}

    def fake_fetch_user_post(path: str, headers: dict[str, str], payload: dict[str, object]) -> dict[str, object]:
        captured["path"] = path
        captured["authorization"] = headers["authorization"]
        captured["x-token"] = headers["x-token"]
        return {"code": 0, "data": "", "msg": "ok"}

    monkeypatch.setattr("app.api.routers.user.fetch_user_post", fake_fetch_user_post)

    response = client.post(
        "/api/user/auth/logout",
        headers={"Authorization": "Bearer test-jwt-token"},
    )

    assert response.status_code == 200
    assert captured["path"] == "base/logout"
    assert captured["authorization"] == "test-jwt-token"
    assert captured["x-token"] == "test-jwt-token"


def test_user_stats_invalid_upstream_shape_returns_standardized_error(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_fetch_user_actgateway(path: str, headers: dict[str, str], params: dict[str, object]) -> object:
        return ["invalid-shape"]

    monkeypatch.setattr("app.api.routers.user.fetch_user_actgateway", fake_fetch_user_actgateway)

    response = client.get(
        "/api/user/stats?lang=en",
        headers={"Authorization": "Bearer test-jwt-token"},
    )

    assert response.status_code == 502
    payload = response.json()
    assert payload["status"] == "error"
    assert payload["code"] == "UPSTREAM_INVALID_RESPONSE"
