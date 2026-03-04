"""Pydantic models for ARGOS-HALE-BOPP API."""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class Decision(str, Enum):
    PASS = "pass"
    FAIL = "fail"


class PolicyLevel(str, Enum):
    DEFAULT = "default"
    STRICT = "strict"
    PERMISSIVE = "permissive"


class UniversalEvent(BaseModel):
    event_id: str
    timestamp: str
    source: str
    event_type: str
    payload: dict[str, Any] = Field(default_factory=dict)


class GateRequest(BaseModel):
    event: UniversalEvent
    policy: PolicyLevel = PolicyLevel.DEFAULT


class Violation(BaseModel):
    rule: str
    message: str
    severity: str = "error"


class GatePassResponse(BaseModel):
    decision: Decision = Decision.PASS
    reason: str = ""


class GateFailResponse(BaseModel):
    decision: Decision = Decision.FAIL
    violations: list[Violation]


class EventAckResponse(BaseModel):
    accepted: bool = True
    event_id: str


class HealthResponse(BaseModel):
    status: str = "ok"
    version: str
