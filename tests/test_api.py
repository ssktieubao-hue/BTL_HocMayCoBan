import json

import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture()
def client(tmp_path):
    art = {
        "meta": {"k_max": 2, "built_on": "2026-10-10", "n_invoices": 100},
        "items": ["A1", "B2", "C3"],
        "descriptions": ["RED BAG", "BLUE BAG", "GREEN MUG"],
        "invoice_count": [30, 20, 5],
        "neighbors": [[1, 2], [0], []],
        "scores": [[0.8, 0.1], [0.8], []],
        "popular": ["A1", "B2"],
    }
    path = tmp_path / "m.json"
    path.write_text(json.dumps(art), encoding="utf-8")
    (tmp_path / "final_test.csv").write_text("model,K,hit_rate\nitem_invoice,10,0.2\n",
                                             encoding="utf-8")
    return TestClient(create_app(path, reports=tmp_path))


def test_health(client):
    r = client.get("/api/health")
    assert r.status_code == 200 and r.json()["n_items"] == 3


def test_similar_items_ok(client):
    r = client.get("/api/similar-items", params={"stock_code": "A1", "k": 2})
    body = r.json()
    assert r.status_code == 200
    assert [x["stock_code"] for x in body["recommendations"]] == ["B2", "C3"]
    assert body["recommendations"][0]["rank"] == 1
    assert body["recommendations"][0]["cosine"] == 0.8
    assert body["returned"] == 2 and body["note"] is None


def test_fewer_neighbors_is_reported(client):
    body = client.get("/api/similar-items", params={"stock_code": "B2", "k": 2}).json()
    assert body["returned"] == 1 and body["note"]


def test_unknown_code_is_not_silently_replaced(client):
    r = client.get("/api/similar-items", params={"stock_code": "a1", "k": 1})
    assert r.status_code == 404
    assert r.json()["error"]["code"] == "unknown_stock_code"
    assert r.json()["error"]["suggestions"] == ["A1"]


@pytest.mark.parametrize("params", [
    {"stock_code": "A1", "k": 0}, {"stock_code": "A1", "k": 3},
    {"stock_code": "A1", "k": "abc"}, {"k": 2}, {"stock_code": " A1"},
])
def test_invalid_input_returns_422(client, params):
    r = client.get("/api/similar-items", params=params)
    assert r.status_code == 422 and "error" in r.json()


def test_search_ranks_by_popularity(client):
    r = client.get("/api/search", params={"q": "bag"})
    assert [x["stock_code"] for x in r.json()] == ["A1", "B2"]


def test_search_rejects_short_query(client):
    assert client.get("/api/search", params={"q": "b"}).status_code == 422


def test_openapi_documents_error_schema(client):
    spec = client.get("/openapi.json").json()
    r422 = spec["paths"]["/api/similar-items"]["get"]["responses"]["422"]
    assert "ErrorResponse" in r422["content"]["application/json"]["schema"]["$ref"]


def test_dashboard(client):
    d = client.get("/api/dashboard").json()
    assert d["test_results"][0]["K"] == "10"
    assert d["popular"][0] == {"stock_code": "A1", "description": "RED BAG",
                               "invoice_count": 30, "share": 0.3}
    assert d["error_analysis"] == []


def test_home_page_is_served(client):
    r = client.get("/")
    assert r.status_code == 200 and "Gợi ý mua kèm" in r.text