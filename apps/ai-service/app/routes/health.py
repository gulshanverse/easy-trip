import time
from datetime import datetime, timezone

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/health", tags=["health"])

_started_at = time.time()


class HealthStatus(BaseModel):
    status: str
    uptime_seconds: int
    timestamp: str
    service: str


@router.get("", response_model=HealthStatus)
def get_health() -> HealthStatus:
    return HealthStatus(
        status="ok",
        uptime_seconds=int(time.time() - _started_at),
        timestamp=datetime.now(timezone.utc).isoformat(),
        service="ai-service",
    )
