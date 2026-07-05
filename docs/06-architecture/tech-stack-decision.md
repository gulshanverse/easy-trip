---
title: "Tech Stack Decision Record (ADR)"
category: "Architecture"
status: "Draft"
priority: "High"
owner: "Unassigned"
last_updated: "2026-07-05"
---

# Tech Stack Decision Record (ADR)

> **Status:** Draft
> **Purpose:** Rationale and tradeoffs behind the chosen frontend, backend, AI layer, and data stack.

## Context

Easy Trip is an AI-powered travel intelligence platform requiring:
- A pluggable provider abstraction layer (flights, hotels, buses, rail, maps, weather, payments, notifications)
- A multi-agent AI layer (Planner, Booking, Budget, Safety, Local Guide, Notification, Memory agents)
- Production-grade scalability, security, and maintainability from day one

## Decision

| Layer | Choice | Notes |
|---|---|---|
| Frontend | Next.js (React) + TypeScript | SSR/SSG for SEO on search/landing pages, App Router, React Server Components |
| Styling / UI | Tailwind CSS + shadcn/ui | Fast iteration, accessible primitives, consistent design tokens |
| Core Backend | Node.js + NestJS (TypeScript) | Modular, DI-based architecture — natural fit for the provider abstraction layer and clean architecture requirements |
| AI / Agent Layer | Python + FastAPI (separate service) | Python has the strongest AI/agent tooling ecosystem; kept isolated from core backend so agent logic can evolve independently |
| Primary Database | PostgreSQL | Strong relational guarantees for bookings, payments, users |
| Vector Store | pgvector (Postgres extension) | Powers the Memory Agent and semantic search without adding a new database to operate, initially |
| Cache / Sessions | Redis | Session storage, rate limiting, hot-path caching |
| Async / Queues | BullMQ (Redis-backed) | Booking workflows, notification dispatch, agent task queues |
| Containerization | Docker + Docker Compose (dev) | Kubernetes-ready service boundaries for later |
| CI/CD | GitHub Actions | Native to the repo, sufficient for current scale |

## Rationale

**Why split core backend (Node/NestJS) from AI layer (Python/FastAPI)?**
Booking orchestration, payments, and provider integrations benefit from NestJS's strict module boundaries and dependency injection — this directly supports the "provider abstraction layer" requirement (each provider is a swappable module behind an interface). AI agent orchestration, prompt management, and model evaluation benefit from Python's ecosystem. Splitting them means the AI layer can iterate fast (prompts, agent logic change often) without risking the stability of booking/payment code, and vice versa.

**Why Postgres + pgvector instead of a dedicated vector DB?**
At current scale, one fewer operational dependency is worth more than the marginal performance gain of a dedicated vector database. This is documented as revisitable: if the Memory Agent's embedding volume grows significantly, migrate to a dedicated vector store (e.g., Pinecone, Qdrant) — the AI layer should access embeddings through an interface, not directly through Postgres calls, to keep this swap low-cost.

## Alternatives Considered

- **Single monolith (NestJS only, calling AI APIs directly)** — simpler initially, but conflates fast-moving agent logic with stable transactional code; rejected for maintainability at scale.
- **Serverless-first (Lambda/Vercel functions)** — good for cost at low scale, but complicates long-running agent workflows and stateful booking sagas; revisit for specific stateless endpoints later.

## Consequences

- Two backend codebases to maintain (Node + Python) — mitigated by clear API contracts and shared OpenAPI specs between them.
- Requires an internal service-to-service auth mechanism between NestJS and FastAPI (see `07-security/auth-and-access-control.md`).

## Open Questions

- Managed Kubernetes provider (GKE vs EKS vs AKS) — deferred until infra document (`08-devops/infrastructure-overview.md`) is drafted.
- Whether Memory Agent embeddings volume will require migrating off pgvector within year 1.

## Related Documents

- `06-architecture/provider-abstraction-layer.md`
- `06-architecture/ai-agent-architecture.md`
- `06-architecture/system-architecture-overview.md`
- `07-security/auth-and-access-control.md`
