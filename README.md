# hale-bopp-argos

Policy gating and data quality engine — rule-based governance, audit logging.

ARGOS is the decision layer: it listens to events from DB and ETL modules, evaluates policies, and gates pipeline execution.

## Features

- **Gate Checking**: Evaluate events against configurable policies (DEFAULT, STRICT, PERMISSIVE)
- **Rule Engine**: Pipeline failure, high-risk deploy, drift detection, null ratio checks
- **Audit Logging**: Append-only JSONL audit trail for all policy evaluations
- **Universal Events**: Receives and processes events from the HALE-BOPP ecosystem

## Quick Start

```bash
# Docker Compose
docker compose up

# Or install locally
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8200
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/v1/gate/check` | Evaluate event against policy |
| `POST` | `/api/v1/events` | Log event for audit trail |
| `GET` | `/api/v1/health` | Service health check |

## Testing

```bash
pip install -r requirements.txt
pytest tests/ -v
```

## Part of HALE-BOPP

HALE-BOPP is an open-source ecosystem of deterministic data governance engines:

- [hale-bopp-db](https://github.com/hale-bopp-data/hale-bopp-db) — Schema governance
- [hale-bopp-etl](https://github.com/hale-bopp-data/hale-bopp-etl) — Data orchestration
- **hale-bopp-argos** (this repo) — Policy gating

## License

Apache License 2.0 — see [LICENSE](LICENSE).
