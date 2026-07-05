# Easy Trip

AI-powered Travel Intelligence Platform for intelligent trip planning, booking orchestration, and personalized travel assistance.

## Documentation

All project documentation — product, architecture, security, DevOps, testing, legal, and AI/ML — lives in [`/docs`](./docs/00-index/DOCUMENTATION_INDEX.md).

Start here: **[Documentation Index](./docs/00-index/DOCUMENTATION_INDEX.md)**

Documentation is treated as the single source of truth. Code should follow what's documented; if you find a gap or inconsistency, update the relevant document rather than working around it.

## Status

🚧 Pre-implementation — documentation foundation phase.

## Tech Stack (proposed, see ADR)

- **Frontend:** Next.js (React) + TypeScript, Tailwind, shadcn/ui
- **Core Backend:** Node.js + NestJS
- **AI/Agent Layer:** Python + FastAPI
- **Data:** PostgreSQL + pgvector, Redis
- **Infra:** Docker, GitHub Actions

See [`docs/06-architecture/tech-stack-decision.md`](./docs/06-architecture/tech-stack-decision.md) for full rationale.
