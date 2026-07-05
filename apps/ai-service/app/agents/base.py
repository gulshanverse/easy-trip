"""
Common agent contract, per docs/06-architecture/ai-agent-architecture.md.

Concrete agents (Planner, Budget, Notification, etc.) implement `Agent`.
Agents must not call external providers directly -- only through the
Tool Layer, which wraps the Core Backend's Provider Abstraction Layer.
"""
from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel


class AgentRequest(BaseModel):
    session_id: str
    user_id: str
    input: Any
    context: dict[str, Any] = {}


class ToolCall(BaseModel):
    tool_name: str
    arguments: dict[str, Any]
    result: Any = None


class AgentResponse(BaseModel):
    output: dict[str, Any]
    tool_calls: list[ToolCall] = []
    confidence: float | None = None
    requires_confirmation: bool = False


class Agent(ABC):
    name: str
    allowed_tools: list[str] = []

    @abstractmethod
    async def handle(self, request: AgentRequest) -> AgentResponse:
        raise NotImplementedError
