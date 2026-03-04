"""Rule engine for ARGOS gating decisions.

MVP: hardcoded rules. Future: load from YAML/DB.
"""

from __future__ import annotations

from app.models.schemas import PolicyLevel, UniversalEvent, Violation


def evaluate(event: UniversalEvent, policy: PolicyLevel) -> list[Violation]:
    """Evaluate an event against the active policy. Return violations (empty = pass)."""
    violations: list[Violation] = []

    for rule_fn in _RULES:
        v = rule_fn(event, policy)
        if v:
            violations.append(v)

    return violations


# --- Individual rules ---

def _rule_pipeline_failure(event: UniversalEvent, policy: PolicyLevel) -> Violation | None:
    """Block if an ETL pipeline has failed."""
    if event.event_type != "etl.pipeline.failed":
        return None
    return Violation(
        rule="pipeline_failure",
        message=f"Pipeline failed: {event.payload.get('pipeline_name', 'unknown')}",
        severity="error",
    )


def _rule_high_risk_deploy(event: UniversalEvent, policy: PolicyLevel) -> Violation | None:
    """Block high-risk schema deploys under strict policy."""
    if event.event_type != "db.schema.diff.completed":
        return None
    risk = event.payload.get("risk_level", "low")
    if policy == PolicyLevel.STRICT and risk in ("medium", "high"):
        return Violation(
            rule="high_risk_deploy",
            message=f"Schema change has {risk} risk — blocked by strict policy",
            severity="error",
        )
    if policy == PolicyLevel.DEFAULT and risk == "high":
        return Violation(
            rule="high_risk_deploy",
            message="Schema change has high risk — requires manual approval",
            severity="error",
        )
    return None


def _rule_drift_detected(event: UniversalEvent, policy: PolicyLevel) -> Violation | None:
    """Flag drift as a violation under strict policy."""
    if event.event_type != "db.drift.detected":
        return None
    if policy in (PolicyLevel.STRICT, PolicyLevel.DEFAULT):
        diffs = event.payload.get("diffs", [])
        return Violation(
            rule="drift_detected",
            message=f"Schema drift detected: {len(diffs)} difference(s)",
            severity="warning" if policy == PolicyLevel.DEFAULT else "error",
        )
    return None


def _rule_null_ratio(event: UniversalEvent, policy: PolicyLevel) -> Violation | None:
    """Block if null ratio exceeds threshold (data quality gate)."""
    if event.event_type != "etl.quality_gate.request":
        return None
    null_ratio = event.payload.get("null_ratio", 0.0)
    threshold = 0.1 if policy == PolicyLevel.STRICT else 0.3
    if null_ratio > threshold:
        return Violation(
            rule="null_ratio_exceeded",
            message=f"Null ratio {null_ratio:.1%} exceeds threshold {threshold:.0%}",
            severity="error",
        )
    return None


_RULES = [
    _rule_pipeline_failure,
    _rule_high_risk_deploy,
    _rule_drift_detected,
    _rule_null_ratio,
]
