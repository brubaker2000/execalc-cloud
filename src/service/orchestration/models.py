from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, Dict, Literal, Optional

TurnClass = Literal[
    "conversational",
    "decision_seeking",
    "action_proposing",
    "execution_seeking",
    "evidence_seeking",
]


@dataclass(frozen=True)
class NavigationEnvelope:
    workspace_id: str = "workspace_default"
    project_id: Optional[str] = None
    chat_id: Optional[str] = None
    thread_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Optional[str]]:
        return {
            "workspace_id": self.workspace_id,
            "project_id": self.project_id,
            "chat_id": self.chat_id,
            "thread_id": self.thread_id,
        }


@dataclass(frozen=True)
class ScenarioEnvelope:
    scenario_id: str
    scenario_type: str
    governing_objective: str
    user_intent: TurnClass
    prompt: str
    relevant_constraints: Dict[str, Any] = field(default_factory=dict)
    decision_state: str = "not_requested"
    action_state: str = "not_requested"
    navigation: NavigationEnvelope = field(default_factory=NavigationEnvelope)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "scenario_id": self.scenario_id,
            "scenario_type": self.scenario_type,
            "governing_objective": self.governing_objective,
            "user_intent": self.user_intent,
            "prompt": self.prompt,
            "relevant_constraints": self.relevant_constraints,
            "decision_state": self.decision_state,
            "action_state": self.action_state,
            "navigation": self.navigation.to_dict(),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
