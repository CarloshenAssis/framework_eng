"""Workflow Architecture §4 — Phase, Step, Failure Policy value objects,
verbatim structure (docs/architecture/10-workflow-architecture.md §4).

Note on `Step.params`: Workflow §4's struct listing does not itself list a
`params` field, but Template Architecture §5.2 ("PARAMETER | Valor explícito
fornecido pelo chamador (ex.: Step.params de um Workflow)") and Skill
Architecture §9 (`step.params`) both already reference it by name as
something Step carries. This is a one-field gap in Workflow §4's own struct
listing, not a missing concept — `params` is already named and relied upon
by two other ratified documents. Added here to make the already-assumed
field explicit; flagged in RUNTIME.md as a candidate one-line amendment to
Workflow Architecture §4, not treated as grounds to halt this implementation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Optional

from runtime.composition.slot import Slot


class StepKind(str, Enum):
    INVOCATION = "INVOCATION"
    GATE_AUTO = "GATE_AUTO"
    GATE_APPROVAL = "GATE_APPROVAL"
    COMPENSATION = "COMPENSATION"


class OnFailure(str, Enum):
    ABORT = "ABORT"
    SKIP = "SKIP"
    RETRY = "RETRY"
    COMPENSATE = "COMPENSATE"


@dataclass
class FailurePolicy:
    """§4 — Value Object: { on_failure: ABORT | SKIP | RETRY(n) | COMPENSATE }."""

    on_failure: OnFailure = OnFailure.ABORT
    retry_count: int = 0


@dataclass
class Step:
    """§4, verbatim fields, plus `params` — see module docstring."""

    id: str
    slot: Optional[Slot]  # None for GATE_APPROVAL steps that resolve a Role, not a Capability
    kind: StepKind = StepKind.INVOCATION
    failure_policy: FailurePolicy = field(default_factory=FailurePolicy)
    timeout_seconds: Optional[int] = None  # Constraint (Kernel §2.10) anchored to this Step
    compensated_by: Optional[str] = None  # StepRef
    params: dict[str, Any] = field(default_factory=dict)
    role_class: Optional[str] = None  # for GATE_APPROVAL (Governance §2)


@dataclass
class Phase:
    """§4, verbatim fields."""

    id: str
    steps: list[Step] = field(default_factory=list)
    entry_predicate: Optional[Callable[[dict], bool]] = None  # Predicate<Context> — Decision Point
    next: list[str] = field(default_factory=list)  # PhaseRef[]; >1 = Branch, convergent = Join
    sequence_hint: int = 0
