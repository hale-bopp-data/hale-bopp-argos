---
title: "Agents Master"
tags: []
---

# AGENTS.md — hale-bopp-argos

> Motore rule-based per data quality e policy gating.
> Guardrails e regole: vedi `.cursorrules` nello stesso repo.
> Workspace map: vedi `factory.yml` nella root workspace (mappa completa repos, stack, deploy).

## Identità
| Campo | Valore |
|---|---|
| Cosa | Python app — rule engine per data quality, policy validation |
| Linguaggio | Python 3.11, Docker |
| Branch | `feat→main` (NO develop) — PR target: `main` |
- **Tests**: 14

## Comandi rapidi
```bash
ewctl commit
# Run tests
pytest
# Docker build + run
docker compose up -d
```

## Struttura
```text
app/                 # Application code
docs/                # Documentation
docker-compose.yml   # Dev environment
Dockerfile           # Container image
pyproject.toml       # Package metadata
```

## Regole specifiche hale-bopp-argos
| Regola | Dettaglio |
|---|---|
| Determinismo | Rule engine deterministico |
| Test | `pytest` con coverage |
| Deploy | Libreria, non servizio — nessun deploy diretto |

## Workflow & Connessioni
| Cosa | Dove |
|---|---|
| ADO operations (WI, PR) | → vedi `easyway-wiki/guides/agents/agent-ado-operations.md` |
| PR flusso standard | → vedi `easyway-wiki/guides/polyrepo-git-workflow.md` |
| PAT/secrets/gateway | → vedi `easyway-wiki/guides/connection-registry.md` |
| Branch strategy | → vedi `easyway-wiki/guides/branch-strategy-config.md` |
| Tool unico | `bash /c/old/easyway/agents/scripts/connections/ado.sh` — MAI curl inline, MAI az login |


---
> Context Sync Engine | Master: `easyway-wiki/templates/agents-master.md`
> Override: `easyway-wiki/templates/repo-overrides.yml` | Sync: 2026-03-19T12:00:13Z
