"""Audit log for ARGOS events — append-only JSONL file."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone

from app.models.schemas import UniversalEvent

AUDIT_LOG_PATH = os.environ.get("ARGOS_AUDIT_LOG", "/var/log/argos/audit.jsonl")


def log_event(event: UniversalEvent, decision: str = "audit") -> None:
    """Append event to audit log (JSONL format)."""
    os.makedirs(os.path.dirname(AUDIT_LOG_PATH), exist_ok=True)

    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "event_id": event.event_id,
        "source": event.source,
        "event_type": event.event_type,
        "decision": decision,
    }

    with open(AUDIT_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
