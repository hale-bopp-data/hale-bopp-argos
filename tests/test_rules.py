"""Tests for ARGOS rule engine."""

from app.core.rules import evaluate
from app.models.schemas import PolicyLevel, UniversalEvent


def _make_event(event_type: str, payload: dict | None = None) -> UniversalEvent:
    return UniversalEvent(
        event_id="test-001",
        timestamp="2026-03-03T12:00:00Z",
        source="test",
        event_type=event_type,
        payload=payload or {},
    )


def test_pipeline_failure_blocked():
    event = _make_event("etl.pipeline.failed", {"pipeline_name": "daily_load"})
    violations = evaluate(event, PolicyLevel.DEFAULT)
    assert len(violations) == 1
    assert violations[0].rule == "pipeline_failure"


def test_pipeline_started_passes():
    event = _make_event("etl.pipeline.started")
    violations = evaluate(event, PolicyLevel.DEFAULT)
    assert len(violations) == 0


def test_high_risk_blocked_strict():
    event = _make_event("db.schema.diff.completed", {"risk_level": "medium"})
    violations = evaluate(event, PolicyLevel.STRICT)
    assert len(violations) == 1
    assert violations[0].rule == "high_risk_deploy"


def test_medium_risk_passes_default():
    event = _make_event("db.schema.diff.completed", {"risk_level": "medium"})
    violations = evaluate(event, PolicyLevel.DEFAULT)
    assert len(violations) == 0


def test_high_risk_blocked_default():
    event = _make_event("db.schema.diff.completed", {"risk_level": "high"})
    violations = evaluate(event, PolicyLevel.DEFAULT)
    assert len(violations) == 1


def test_drift_detected_warning_default():
    event = _make_event("db.drift.detected", {"diffs": [{"col": "x"}]})
    violations = evaluate(event, PolicyLevel.DEFAULT)
    assert len(violations) == 1
    assert violations[0].severity == "warning"


def test_drift_ignored_permissive():
    event = _make_event("db.drift.detected", {"diffs": [{"col": "x"}]})
    violations = evaluate(event, PolicyLevel.PERMISSIVE)
    assert len(violations) == 0


def test_null_ratio_pass():
    event = _make_event("etl.quality_gate.request", {"null_ratio": 0.05})
    violations = evaluate(event, PolicyLevel.DEFAULT)
    assert len(violations) == 0


def test_null_ratio_fail():
    event = _make_event("etl.quality_gate.request", {"null_ratio": 0.5})
    violations = evaluate(event, PolicyLevel.DEFAULT)
    assert len(violations) == 1
    assert violations[0].rule == "null_ratio_exceeded"


def test_null_ratio_strict_threshold():
    event = _make_event("etl.quality_gate.request", {"null_ratio": 0.15})
    # Default threshold 0.3 → pass
    assert len(evaluate(event, PolicyLevel.DEFAULT)) == 0
    # Strict threshold 0.1 → fail
    assert len(evaluate(event, PolicyLevel.STRICT)) == 1
