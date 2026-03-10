# hale-bopp-argos

[![CI](https://github.com/hale-bopp-data/hale-bopp-argos/actions/workflows/ci.yml/badge.svg)](https://github.com/hale-bopp-data/hale-bopp-argos/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-green.svg)](https://python.org)

Policy gating and data quality engine — rule-based governance, audit logging, zero AI.

ARGOS is the decision layer: it evaluates events against configurable policies and gates pipeline execution.

## Architecture

```
  Events from DB/ETL          ARGOS                     Decision
  ┌──────────────┐      ┌──────────────┐          ┌──────────────┐
  │ schema.deploy│      │              │          │              │
  │ pipeline.fail│─────►│  Rule Engine │─────────►│  PASS / FAIL │
  │ drift.detect │      │  :8200       │          │  + audit log │
  │ dq.check     │      │              │          │              │
  └──────────────┘      └──────────────┘          └──────────────┘
```

## Features

- **Gate Checking**: Evaluate events against configurable policies (DEFAULT, STRICT, PERMISSIVE)
- **Rule Engine**: Pipeline failure, high-risk deploy, drift detection, null ratio checks
- **Audit Logging**: Append-only JSONL audit trail for all policy evaluations
- **Universal Events**: Receives and processes events from the entire HALE-BOPP ecosystem
- **Policy Profiles**: Switch between strictness levels without code changes

## Quick Start

```bash
# Install
pip install -e .

# Start the API server
uvicorn app.main:app --host 0.0.0.0 --port 8200

# Or use Docker Compose
docker compose up
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/v1/gate/check` | Evaluate event against policy |
| `POST` | `/api/v1/events` | Log event for audit trail |
| `GET` | `/api/v1/health` | Service health check |

### Gate Check Example

```bash
curl -X POST http://localhost:8200/api/v1/gate/check \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "db.schema.deploy.completed",
    "source": "hale-bopp-db",
    "payload": {"risk_level": "high", "changes_count": 5},
    "policy": "STRICT"
  }'

# Response: {"gate": "FAIL", "reason": "high-risk deploy blocked by STRICT policy"}
```

## Testing

```bash
pip install -e .
pip install pytest httpx
pytest tests/ -v
```

14 tests covering gate evaluation, rule engine, event processing, audit logging, and API endpoints.

## Part of HALE-BOPP

> *Sovereign by design. Cloud by choice.*

HALE-BOPP is an open-source ecosystem of deterministic data engines — the "muscles" that do the heavy lifting, no AI required. Portable, replicable, and sovereign: your policy governance runs where you decide, not where a vendor tells you.

```
  ┌──────────┐     event      ┌──────────┐     gate      ┌──────────┐
  │ DB :8100 │ ─────────────► │ETL :3001 │ ◄──────────── │ARGOS:8200│
  │ schema   │                │ pipeline │               │ policy   │
  │ govern.  │                │ runner   │               │ gating   │
  └──────────┘                └──────────┘               └──────────┘
```

- [hale-bopp-db](https://github.com/hale-bopp-data/hale-bopp-db) — Schema governance for PostgreSQL
- [hale-bopp-etl](https://github.com/hale-bopp-data/hale-bopp-etl) — Config-driven data orchestration
- **hale-bopp-argos** (this repo) — Policy gating and quality checks
- [marginalia](https://github.com/hale-bopp-data/marginalia) — Markdown vault quality scanner

## License

Apache License 2.0 — see [LICENSE](LICENSE).
