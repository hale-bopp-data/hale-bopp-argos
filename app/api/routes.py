"""ARGOS-HALE-BOPP REST API routes."""

from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.core.audit import log_event
from app.core.rules import evaluate
from app.models.schemas import (
    EventAckResponse,
    GateFailResponse,
    GatePassResponse,
    GateRequest,
    HealthResponse,
    UniversalEvent,
)

router = APIRouter(prefix="/api/v1")

VERSION = "0.1.0"


@router.post("/gate/check")
def gate_check(req: GateRequest):
    violations = evaluate(req.event, req.policy)
    log_event(req.event, decision="fail" if violations else "pass")

    if violations:
        return JSONResponse(
            status_code=403,
            content=GateFailResponse(violations=violations).model_dump(),
        )
    return GatePassResponse(reason="All checks passed")


@router.post("/events", response_model=EventAckResponse, status_code=202)
def receive_event(event: UniversalEvent):
    log_event(event)
    return EventAckResponse(event_id=event.event_id)


@router.get("/health", response_model=HealthResponse)
def health():
    return HealthResponse(version=VERSION)
