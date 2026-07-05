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

## Local Development

```bash
# Start Postgres + Redis + all three apps
docker compose up --build

# Or run apps individually:
cd apps/web && npm install && npm run dev        # http://localhost:3000
cd apps/core-api && npm install && npm run start:dev   # http://localhost:3001/health
cd apps/ai-service && python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt && uvicorn app.main:app --reload   # http://localhost:8000/health
```

## Repository Structure

```
apps/
  web/          # Next.js frontend
  core-api/     # NestJS backend (booking, users, provider abstraction, payments)
  ai-service/   # FastAPI AI agent layer (Planner, Budget, Notification agents)
docs/           # Living documentation (see docs/00-index/DOCUMENTATION_INDEX.md)
docker-compose.yml
.github/workflows/ci.yml
```
