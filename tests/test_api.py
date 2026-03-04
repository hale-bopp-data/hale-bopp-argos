"""Tests for ARGOS-HALE-BOPP API endpoints."""

from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    resp = client.get("/api/v1/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


@patch("app.api.routes.log_event")
def test_gate_pass(mock_log):
    resp = client.post("/api/v1/gate/check", json={
        "event": {
            "event_id": "e-001",
            "timestamp": "2026-03-03T12:00:00Z",
            "source": "etl",
            "event_type": "etl.pipeline.started",
            "payload": {},
        },
        "policy": "default",
    })
    assert resp.status_code == 200
    assert resp.json()["decision"] == "pass"


@patch("app.api.routes.log_event")
def test_gate_fail(mock_log):
    resp = client.post("/api/v1/gate/check", json={
        "event": {
            "event_id": "e-002",
            "timestamp": "2026-03-03T12:00:00Z",
            "source": "etl",
            "event_type": "etl.pipeline.failed",
            "payload": {"pipeline_name": "daily_load"},
        },
        "policy": "default",
    })
    assert resp.status_code == 403
    data = resp.json()
    assert data["decision"] == "fail"
    assert len(data["violations"]) == 1


@patch("app.api.routes.log_event")
def test_event_accepted(mock_log):
    resp = client.post("/api/v1/events", json={
        "event_id": "e-003",
        "timestamp": "2026-03-03T12:00:00Z",
        "source": "db",
        "event_type": "db.schema.deploy.completed",
        "payload": {},
    })
    assert resp.status_code == 202
    assert resp.json()["accepted"] is True
