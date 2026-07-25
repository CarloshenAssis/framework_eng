"""Execution Architecture (docs/architecture/11) §4, §6 + Domain Model §8 —
Execution, Context, Context Snapshot, Artifact, Evidence.

Execution Architecture §1: "nunca redefine o Lifecycle de Execution (Domain
Model §8: Initiated→Running→Completed|Failed|Aborted) — apenas orquestra
transições dentro dele." This module reuses that Lifecycle unmodified.

Scope note on "Timeline" (requested alongside Execution Runtime): the named
construct `Execution Timeline` (a cross-orchestration query projection) is
defined in Observability Architecture §5.3, which this Runtime is explicitly
told not to implement. What IS implemented here is narrower and does not
reach into Observability's territory: each Execution keeps its own ordered
list of (state, timestamp) transitions — intrinsic bookkeeping any Execution
already needs for its own Lifecycle (Domain Model §8), not a query service
over many Executions. See RUNTIME.md for this distinction spelled out.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional

from runtime.contracts.identity import new_instance_identifier


class ExecutionState(str, Enum):
    """Domain Model §8, reused without modification (Execution §1)."""

    INITIATED = "Initiated"
    RUNNING = "Running"
    COMPLETED = "Completed"
    FAILED = "Failed"
    ABORTED = "Aborted"


_TERMINAL_STATES = {ExecutionState.COMPLETED, ExecutionState.FAILED, ExecutionState.ABORTED}

_ALLOWED_TRANSITIONS = {
    ExecutionState.INITIATED: {ExecutionState.RUNNING, ExecutionState.ABORTED},
    ExecutionState.RUNNING: {ExecutionState.COMPLETED, ExecutionState.FAILED, ExecutionState.ABORTED},
}


class ExecutionError(Exception):
    pass


@dataclass
class Context:
    """Execution §4 — Orchestration Correlation as semantic content of
    Context (Composition/Workflow/Execution preamble's H6 resolution):
    orchestration_id, phase_id, step_id, attempt — NOT a new relation, a
    convention over the already-generic Context entity (Domain Model §2 #5).
    """

    orchestration_id: str
    phase_id: Optional[str] = None
    step_id: Optional[str] = None
    attempt: int = 0
    extra: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return {
            "orchestration_id": self.orchestration_id,
            "phase_id": self.phase_id,
            "step_id": self.step_id,
            "attempt": self.attempt,
            **self.extra,
        }


@dataclass
class ContextSnapshot:
    """RFC-DM-001 §3.2 (C2) — immutable capture of Context, mandatory before
    an Execution enters Running (EX2). Anything a Template binds via
    binding_source=CONTEXT (Template §5.2) comes from here, never from a
    live/mutable Context."""

    instance_id: str
    captured_context: dict[str, Any]
    captured_at: str


def capture_context_snapshot(context: Context) -> ContextSnapshot:
    snapshot_context = context.as_dict()
    snapshot_context.setdefault("generated_at", _now_iso())
    return ContextSnapshot(
        instance_id=new_instance_identifier(),
        captured_context=snapshot_context,
        captured_at=_now_iso(),
    )


@dataclass
class Artifact:
    """Domain Model §2 #7 — "qualquer resultado tangível e persistente
    produzido por uma Execution ou por uma Decision." Generic on purpose:
    Assembly, ExpandedTemplate, Execution Plan and a Skill's own output are
    all this same entity, per the "reuse Artifact, never specialize"
    pattern used throughout the ratified base."""

    instance_id: str
    kind: str
    content: Any
    produced_by_execution: str

    @classmethod
    def create(cls, kind: str, content: Any, produced_by_execution: str) -> "Artifact":
        return cls(instance_id=new_instance_identifier(), kind=kind, content=content,
                    produced_by_execution=produced_by_execution)


@dataclass
class Evidence:
    """Domain Model §2 #8 — "um Artifact cuja função específica é comprovar
    que um resultado declarado de fato ocorreu." Modeled as a specialization
    of Artifact, exactly per the Domain Model hierarchy (§3): Evidence IS-A
    Artifact, not a sibling entity."""

    instance_id: str
    evidence_kind: str  # STRUCTURAL | TEST_RESULT | ... (Standards §4.6 vocabulary, reused)
    description: str
    result: str  # PASS | FAIL
    reproducible: bool
    subject_execution: str

    @classmethod
    def create(cls, evidence_kind: str, description: str, result: str,
               reproducible: bool, subject_execution: str) -> "Evidence":
        return cls(instance_id=new_instance_identifier(), evidence_kind=evidence_kind,
                    description=description, result=result, reproducible=reproducible,
                    subject_execution=subject_execution)


@dataclass
class Execution:
    """Domain Model §2 #6 — "uma instância concreta e única de um Component
    sendo aplicado em um momento específico." EX1: never reopened; a retry
    or compensation is always a NEW Execution."""

    instance_id: str
    performed_by: str
    occurs_within: Context
    captured_as: ContextSnapshot
    state: ExecutionState = ExecutionState.INITIATED
    produced_artifacts: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    transitions: list[tuple[str, str]] = field(default_factory=list)  # intrinsic Timeline, see module docstring
    failure_reason: Optional[str] = None

    def __post_init__(self) -> None:
        self.transitions.append((self.state.value, _now_iso()))

    def transition(self, target: ExecutionState, failure_reason: Optional[str] = None) -> None:
        if self.state in _TERMINAL_STATES:
            raise ExecutionError(f"EX1 violation: Execution {self.instance_id} is terminal ({self.state}); "
                                  f"a retry or compensation MUST be a new Execution, never a reopen")
        if target not in _ALLOWED_TRANSITIONS.get(self.state, set()):
            raise ExecutionError(f"illegal transition {self.state} -> {target}")
        self.state = target
        self.transitions.append((target.value, _now_iso()))
        if target == ExecutionState.FAILED:
            self.failure_reason = failure_reason


def _now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
