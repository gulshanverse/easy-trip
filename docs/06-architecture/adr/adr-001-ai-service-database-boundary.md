---
title: "ADR-001: AI Service Must Not Access the Database Directly"
category: "Architecture"
status: "Approved"
priority: "Critical"
owner: "Founding CTO"
last_updated: "2026-07-05"
---

# ADR-001: AI Service Must Not Access the Database Directly

## Status

**Approved** (2026-07-05) — implemented same day.

## Purpose

Record the decision to remove direct database access from `ai-service`, and the reasoning, so future contributors don't reintroduce it under time pressure.

## Context

`docker-compose.yml` initially gave `ai-service` its own `DATABASE_URL`, letting the AI layer read/write Postgres directly — the same tables `core-api` owns. This was flagged in the Architecture Audit Report (2026-07-05) as a Critical issue: two independent writers to one system of record breaks the bounded-context principle the architecture docs already assume (`system-architecture-overview.md`, `ai-agent-architecture.md`).

## Decision

`ai-service` has no database credentials. All data access from the AI layer goes through a typed internal HTTP client (`app/clients/core_api_client.py`) calling `core-api`'s internal API. `core-api` remains the single owner of data integrity for the system of record.

## Options Considered

| Option | Description | Verdict |
|---|---|---|
| A. Shared DB access | Both services connect to Postgres directly | Rejected — breaks bounded contexts, two writers to one schema |
| **B. AI service calls core-api over internal HTTP** | `ai-service` has zero DB credentials; all data access is mediated by core-api | **Chosen** |
| C. Read-only replica for ai-service | Fast reads for embeddings/context, bypassing core-api | Deferred — revisit if/when the Memory Agent's read volume justifies the added infra |

## Consequences

- **Positive:** Single source of truth for data integrity; core-api can evolve its schema without coordinating with ai-service; matches DDD bounded-context principles already implicit in the docs.
- **Negative:** Adds one network hop for any data ai-service needs — acceptable at current scale (internal network, low latency); to be monitored if agent workflows become latency-sensitive.
- **Follow-up:** core-api does not yet expose the endpoints ai-service will eventually need (user profile, trip budget, provider search). `CoreApiClient` currently only wraps `/api/v1/health` as a connectivity proof; real methods are added as those core-api endpoints are built.

## Implementation

- Removed `DATABASE_URL` from `ai-service` in `docker-compose.yml`.
- Added `app/clients/core_api_client.py`: typed async client wrapping `httpx`, normalizing errors into `CoreApiError`, with a 5-second timeout default.
- Added `tests/test_core_api_client.py`: covers success, upstream error, and unreachable-host cases (3 tests, all passing).

## Revisit When

- Memory Agent ships and its embedding-read volume is measured — re-evaluate Option C (read replica) at that point, not before.

## References

- `docs/06-architecture/architecture-audit-2026-07-05.md`
- `docs/06-architecture/system-architecture-overview.md`
- `docs/06-architecture/ai-agent-architecture.md`
