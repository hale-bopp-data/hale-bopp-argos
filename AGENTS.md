---
title: "Agents Master"
tags: []
---

# AGENTS.md — hale-bopp-argos

> Motore rule-based per data quality e policy gating.
> Guardrails e regole: vedi `.cursorrules` nello stesso repo.

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

## ADO Workflow
```bash
# Tool UNICO — MAI curl inline, MAI az login
bash /c/old/easyway/ado/scripts/ado-remote.sh wi-create "titolo" "PBI" "tag1;tag2"
bash /c/old/easyway/ado/scripts/ado-remote.sh pr-create hale-bopp-argos <src> main "AB#NNN titolo" NNN
bash /c/old/easyway/ado/scripts/ado-remote.sh pr-autolink-wi <pr_id> hale-bopp-argos
bash /c/old/easyway/ado/scripts/ado-remote.sh pat-health-check
```
Repo ADO: `easyway-portal`, `easyway-wiki`, `easyway-agents`, `easyway-infra`, `easyway-ado`, `easyway-n8n`

## PR — Flusso standard
```bash
cd /c/old/hale-bopp/argos && git push -u origin feat/nome-descrittivo
bash /c/old/easyway/ado/scripts/ado-remote.sh pr-create hale-bopp-argos feat/nome-descrittivo main "AB#NNN titolo" NNN
```


## Connessioni
- **PAT/secrets**: SOLO su server `/opt/easyway/.env.secrets` — MAI in locale
- **Guida**: `easyway-wiki/guides/connection-registry.md`
- **`.env.local`**: solo OPENROUTER_API_KEY e QDRANT

---
> Context Sync Engine | Master: `easyway-wiki/templates/agents-master.md`
> Override: `easyway-wiki/templates/repo-overrides.yml` | Sync: 2026-03-15T03:00:04Z
