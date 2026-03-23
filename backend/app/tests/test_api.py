from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_healthcheck():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_dashboard_flow():
    client.post("/trading/signals")
    client.post("/trading/paper-trades")
    client.post("/trading/backtest")
    response = client.get("/dashboard")
    assert response.status_code == 200
    payload = response.json()
    assert len(payload["assets"]) >= 3
    assert "insights" in payload
