"""Provider-neutral request/response types for the LLM layer."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class ToolSpec:
    name: str
    description: str
    parameters: dict[str, Any]
    strict: bool = True

    def to_responses_tool(self) -> dict[str, Any]:
        return {"type": "function", "name": self.name, "description": self.description,
                "parameters": self.parameters, "strict": self.strict}


@dataclass
class FunctionCall:
    call_id: str
    name: str
    arguments: str

    def parsed(self) -> dict[str, Any]:
        try:
            v = json.loads(self.arguments or "{}")
        except json.JSONDecodeError as exc:
            raise ValueError(f"tool {self.name} arguments are not valid JSON: {exc}") from exc
        if not isinstance(v, dict):
            raise ValueError(f"tool {self.name} arguments must be a JSON object")
        return v


@dataclass
class Usage:
    input_tokens: int = 0
    output_tokens: int = 0
    reasoning_tokens: int = 0
    cached_tokens: int = 0

    @property
    def total(self) -> int:
        return self.input_tokens + self.output_tokens

    def add(self, other: "Usage") -> None:
        self.input_tokens += other.input_tokens
        self.output_tokens += other.output_tokens
        self.reasoning_tokens += other.reasoning_tokens
        self.cached_tokens += other.cached_tokens


@dataclass
class ModelResponse:
    response_id: str
    deployment: str
    model: str
    output_items: list[dict[str, Any]]
    text: str = ""
    usage: Usage = field(default_factory=Usage)
    status: str = "completed"
    cached: bool = False
    failover: bool = False
    latency_ms: int = 0

    @property
    def function_calls(self) -> list[FunctionCall]:
        return [FunctionCall(i["call_id"], i["name"], i.get("arguments", ""))
                for i in self.output_items if i.get("type") == "function_call"]

    def to_json(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_json(cls, d: dict[str, Any]) -> "ModelResponse":
        d = dict(d)
        d["usage"] = Usage(**d.get("usage", {}))
        return cls(**d)
