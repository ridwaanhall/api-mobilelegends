from __future__ import annotations

from urllib.parse import urlparse
from xml.etree import ElementTree

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_docs_and_redoc_available() -> None:
    docs_response = client.get("/docs")
    redoc_response = client.get("/redoc")

    assert docs_response.status_code == 200
    assert redoc_response.status_code == 200


def test_api_docs_redirects_to_swagger() -> None:
    response = client.get("/api/docs", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/docs"


def test_api_index_exposes_only_mlbb_and_academy_services() -> None:
    response = client.get("/api")
    payload = response.json()

    assert response.status_code == 200
    assert payload["meta"]["available_services"] == ["mlbb_api", "mlbb_academy"]
    assert "mpl_id" not in payload["services"]


def test_openapi_documents_mlbb_query_constraints() -> None:
    openapi = client.get("/openapi.json").json()
    params = openapi["paths"]["/api/hero-rank"]["get"]["parameters"]
    hero_detail_params = openapi["paths"]["/api/hero-detail/{hero_identifier}"]["get"]["parameters"]

    days_param = next(param for param in params if param["name"] == "days")
    rank_param = next(param for param in params if param["name"] == "rank")
    hero_identifier_param = next(param for param in hero_detail_params if param["name"] == "hero_identifier")

    assert "Allowed: 1, 3, 7, 15, 30" in days_param["description"]
    assert rank_param["schema"]["enum"] == ["all", "epic", "legend", "mythic", "honor", "glory"]
    assert "validated dynamically" in hero_identifier_param["description"]


def test_openapi_documents_academy_path_and_query_constraints() -> None:
    openapi = client.get("/openapi.json").json()
    op = openapi["paths"]["/api/academy/guide/{hero_id}/trends"]["get"]
    params = op["parameters"]

    hero_id_param = next(param for param in params if param["name"] == "hero_id")
    days_param = next(param for param in params if param["name"] == "days")

    assert "validated dynamically" in hero_id_param["description"]
    assert days_param["schema"]["enum"] == ["7", "15", "30"]


def test_robots_txt_allows_all_crawlers() -> None:
    response = client.get("/robots.txt")
    content = response.text

    assert response.status_code == 200
    assert "User-agent: *" in content
    assert "Allow: /" in content
    assert "Sitemap:" in content


def test_sitemap_uses_latest_api_urls() -> None:
    response = client.get("/sitemap.xml")
    content = response.text
    xml_root = ElementTree.fromstring(content)
    namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    loc_paths = {
        urlparse(node.text).path
        for node in xml_root.findall("sm:url/sm:loc", namespace)
        if node.text
    }

    assert response.status_code == 200
    assert "/api/hero-rank" in loc_paths
    assert "/api/academy/guide" in loc_paths
    assert "/docs" in loc_paths
    assert "/hero-rank" not in loc_paths
