from fastapi import FastAPI

from app.routes import health

app = FastAPI(
    title="Easy Trip AI Service",
    description="Agent orchestration layer for Easy Trip (Planner, Budget, Notification agents).",
    version="0.1.0",
)

app.include_router(health.router)
