---
title: "Architecture Audit Report — July 2026"
category: "Architecture"
status: "Approved"
priority: "High"
owner: "Founding CTO"
last_updated: "2026-07-05"
---

# Architecture Audit Report — July 2026

## Purpose

Establish a factual, scored baseline of the Easy Trip codebase's architectural maturity before further feature work, so that engineering decisions from this point forward are made against known gaps rather than assumptions. This audit exists to be revisited — each future audit should diff against this one.

## Goals

1. Score every major architectural dimension against enterprise-grade criteria (not against "does it work for a demo").
2. Surface weaknesses the team may not yet be aware of, prioritized by blast radius if left unaddressed.
3. Produce a roadmap that fixes Critical/High items before they're load-bearing for other code (fixing an auth model after 40 endpoints depend on it is 10x the cost of fixing it now).

## Assumptions

- The repository is 3 commits old: (1) documentation skeleton, (2) 5 core docs drafted, (3) monorepo scaffold (web/core-api/ai-service) with health checks only.
- No user-facing feature has shipped. No real user or payment data exists yet.
- "Enterprise-grade" here means: what would not need to be re-architected if Easy Trip had 10M users — not that every line must be production-hardened today.

## Dependencies

- This audit assumes the tech stack decision in `tech-stack-decision.md` (NestJS / FastAPI / Next.js / Postgres+pgvector / Redis) stands. If that decision changes, several scores below (esp. shared libraries, dependency graph) need to be re-evaluated.

## Scope of Audit

Folder structure, scalability, naming conventions, package organization, dependency graph, database architecture, authentication architecture, authorization model, API versioning, AI service boundaries, shared libraries, configuration management, environment strategy, CI/CD readiness, observability, testing strategy, security posture.

---

## Scorecard

| # | Area | Score /10 | Rationale |
|---|---|---|---|
| 1 | Folder structure | 7 | Clean `apps/*` separation (web, core-api, ai-service) with independent dependency trees — correct instinct for a polyglot system. Gap: `core-api` has only a `health` module; no domain-oriented structure yet (`booking/`, `users/`, `providers/`) to validate the pattern scales. |
| 2 | Scalability | 3 | Well-reasoned on paper (`system-architecture-overview.md`, `provider-abstraction-layer.md`) — stateless service split, cache/queue chosen. Zero of it is implemented: no caching code, no queue code, no load test, no statelessness verified. Score reflects design intent, not proven capability. |
| 3 | Naming conventions | 6 | Consistent so far (NestJS module/service/controller suffixing, kebab-case docs, snake_case Python) but implicit — no written convention doc, so consistency is accidental, not enforced. |
| 4 | Package organization | 4 | Correct instinct to isolate `apps/*` with separate manifests. Missing: no shared contracts package — `AgentRequest`/`AgentResponse` exist only as a Python dataclass; there's no single source of truth shared with the (future) TypeScript side. |
| 5 | Dependency graph | 5 | Minimal, clean dependencies today (good — no premature bloat). No tooling exists to *keep* it clean once more modules exist (no import-boundary linting, no dependency-cruiser/Nx-style enforcement). |
| 6 | Database architecture | 1 | Postgres+pgvector chosen and containerized. **No schema. No ORM/query-builder decision. No migration tool decision.** Everything here is "Pending Decision." |
| 7 | Authentication architecture | 0 | Not designed, not stubbed. `auth-and-access-control.md` is an empty stub. This is the single biggest gap relative to "every feature must include security considerations." |
| 8 | Authorization model | 0 | No RBAC/ABAC model exists even as a diagram. Cannot safely build any user-facing feature until this has at least a decision recorded. |
| 9 | API versioning | 1 | **Violation of the team's own stated rule** ("every API must be versioned"). `main.ts` has no route prefix; FastAPI has no version prefix. Easy to fix now (2 endpoints), expensive to fix later (dozens of endpoints, live clients). |
| 10 | AI service boundaries | 5 | The *design* is genuinely good — `Agent`/`AgentRequest`/`AgentResponse` contract with a `requires_confirmation` guardrail is the right instinct (no agent can autonomously spend money). But the boundary is violated in infrastructure: see ADR-001 below. Score would be 8 once that's fixed. |
| 11 | Shared libraries | 2 | None exist. The core-api ↔ ai-service contract lives only as prose in a markdown doc, not as a generated/enforced schema. This will drift the moment both sides are built independently. |
| 12 | Configuration management | 3 | `docker-compose.yml` uses env vars (correct direction), but neither service has a centralized, validated config module (`ConfigModule` + schema in Nest; `pydantic-settings` in FastAPI). Both currently would read `process.env`/`os.environ` ad hoc if extended today. |
| 13 | Environment strategy | 2 | `environment-strategy.md` is an unstarted stub. No dev/staging/prod distinction exists anywhere in code or CI. |
| 14 | CI/CD readiness | 3 | Workflow is written and *locally verified* (lint+test+build pass for all 3 apps) but not yet merged — blocked on a token permission, which is a process gap, not a technical one. Even once merged: no registry push, no deploy stage, no environment gating, no secret scanning. |
| 15 | Observability | 0 | No structured logging, no correlation IDs, no metrics, no tracing. `/health` exists but conflates liveness and readiness (a booking-heavy system needs both, distinctly, before it scales). |
| 16 | Testing strategy | 4 | To the team's credit: the tests that exist are *real*, not placeholders (they assert actual response shape, not just "doesn't throw"). But coverage is limited to health checks, there's no e2e suite, and `test-strategy.md` itself is still an unstarted stub. |
| 17 | Security posture | 2 | `docker-compose.yml` has a literal password string (`easytrip_dev_password`) committed to git. It's a throwaway dev-only value, but the *pattern* is wrong — it should come from a gitignored `.env` from day one, so the habit is correct before real secrets exist. No security headers, no rate limiting, no CORS policy, no dependency vulnerability scanning. |

**Weighted overall maturity: ~2.9/10** against an enterprise-grade bar — which is the correct number for a 3-commit-old repo with two working health checks. The useful signal isn't the number; it's *which* items are Critical and need to be fixed before more code is written on top of them.

---

## Weaknesses by Priority

### Critical (block further feature work until addressed)

1. **No authentication or authorization design** — cannot safely build any endpoint touching user or booking data without this.
2. **No API versioning applied to actual routes** — cheap now, expensive to retrofit once clients depend on unversioned paths.
3. **No database schema/ORM/migration strategy** — blocks all persistence work; currently "Pending Decision."
4. **AI service has direct database credentials (ADR-001, below)** — violates the bounded-context design the team already agreed to on paper.
5. **Secrets pattern is wrong from the start** — plaintext value in a committed compose file, even if it's a dev throwaway.

### High (fix before the system has more than ~3 services or ~2 developers)

6. **No shared contracts package** between core-api and ai-service — will silently drift.
7. **Agent Orchestrator doesn't exist as code** — the most differentiated part of the architecture is design-only; needs one real agent wired end-to-end to validate the pattern before building six more agents on an unproven foundation.
8. **Zero observability foundation** — logging/metrics/tracing are far cheaper to bake in now (2 services) than to retrofit later (10+ services).
9. **CI not merged** — blocked on token scope; low effort, should not linger.

### Medium (fix before scaling the team or the environment count)

10. No dependency-boundary enforcement tooling.
11. No centralized, validated configuration module in either backend.
12. No environment strategy (dev/staging/prod) implemented anywhere.
13. Test strategy doc incomplete; no integration/e2e tests yet.

### Low (fix opportunistically)

14. No written naming-convention doc (current consistency is accidental).
15. No dependency vulnerability scanning (Dependabot/Snyk).
16. Public-facing legal docs (ToS/Privacy) still stubs — not an engineering blocker.

---

## Proposed ADR-001: AI Service Must Not Access the Database Directly

**Problem:** `docker-compose.yml` currently grants `ai-service` a `DATABASE_URL`. This lets the AI layer read/write Postgres tables that `core-api` also owns, creating two independent writers to the same system of record — a classic source of inconsistent state and un-debuggable bugs once booking/payment logic exists.

**Options considered:**

| Option | Description | Tradeoff |
|---|---|---|
| A. Shared DB access (current state) | Both services connect to Postgres directly | Simple short-term, but breaks bounded contexts; any schema change now requires coordinating two codebases; no single owner of data integrity |
| B. AI service calls Core API over internal HTTP | `ai-service` has zero DB credentials; all data access goes through `core-api`'s internal API | Matches the documented architecture (`system-architecture-overview.md` already describes this for provider calls — should apply to data too); adds network hop latency, mitigated by internal-network placement |
| C. AI service gets a read-only replica | Fast reads for embeddings/context without hitting `core-api` | Useful *later* for the Memory Agent's read-heavy embedding queries, but premature now — adds infra complexity before there's a proven read-heavy workload |

**Recommendation: Option B now, revisit Option C if/when the Memory Agent's read volume justifies it.** This matches the DDD bounded-context principle already implicit in the architecture docs, and requires no new infrastructure — just removing `DATABASE_URL` from `ai-service`'s environment and routing any data needs through `core-api`.

**Status:** Proposed — pending your approval before I make this change.

---

## Future Scalability Notes

- Item 6 (shared contracts) and item 7 (Agent Orchestrator) are the two items most likely to compound into real technical debt if postponed — they're structural, not cosmetic.
- Database choice (item 6 in scorecard) should be settled before any domain module is built, since retrofitting an ORM/migration tool across an existing schema is far more expensive than choosing one now.

## Version History

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-07-05 | Initial audit, post-Phase 2 scaffold |

## References

- `docs/06-architecture/system-architecture-overview.md`
- `docs/06-architecture/provider-abstraction-layer.md`
- `docs/06-architecture/ai-agent-architecture.md`
- `docs/06-architecture/tech-stack-decision.md`

## Action Items

- [x] Approve or amend ADR-001 (AI service DB access) — **Approved & implemented 2026-07-05, see `adr/adr-001-ai-service-database-boundary.md`**
- [ ] Decide ORM/migration tool for core-api (Prisma vs. TypeORM vs. Drizzle — comparison to follow if requested)
- [ ] Decide auth approach (build vs. managed IdP — comparison to follow if requested)
- [ ] Apply API versioning to existing `/health` routes before adding new ones
- [ ] Move `docker-compose.yml` secrets into a gitignored `.env` + `.env.example`
- [ ] Get CI workflow merged (needs `workflow`-scoped token)

## Open Questions

- **Pending Decision:** ORM/query layer for core-api.
- **Pending Decision:** Auth provider (build vs. buy).
- **Pending Decision:** Whether ai-service ever gets direct DB access (Option C) once Memory Agent ships, or stays API-only permanently.
