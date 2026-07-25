"""Kernel Architecture (docs/architecture/02) — §2 Component Contract (15 fields),
§3 Lifecycle, §6 Manifest.

This module implements ONLY the form the Kernel mandates. It does not add a
sixteenth field, a new lifecycle state, or a new relation. `templates[]` and
`test_suite[]` are modeled as separate, explicitly-optional attributes because
Kernel §9 (Extension Model) says exactly that: the Contract declares the
*what*, extensions are the *how* — additive, never part of the 15 mandatory
fields (§2, closing rule: "nenhum componente é admitido... com qualquer um
destes quinze campos ausente").
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from runtime.contracts.identity import Coordinate, VersionedIdentifier


class LifecycleState(str, Enum):
    """Kernel §3 — Draft → Review → Approved → Active → Deprecated → Archived → Removed.
    The only formal exception to "no skipping": Review MAY return to Draft."""

    DRAFT = "Draft"
    REVIEW = "Review"
    APPROVED = "Approved"
    ACTIVE = "Active"
    DEPRECATED = "Deprecated"
    ARCHIVED = "Archived"
    REMOVED = "Removed"


_LIFECYCLE_ORDER = [
    LifecycleState.DRAFT,
    LifecycleState.REVIEW,
    LifecycleState.APPROVED,
    LifecycleState.ACTIVE,
    LifecycleState.DEPRECATED,
    LifecycleState.ARCHIVED,
    LifecycleState.REMOVED,
]


def is_valid_transition(current: LifecycleState, target: LifecycleState) -> bool:
    """Kernel §3 — "nenhum componente pula estados. A única exceção formal é
    retorno de Review para Draft." """
    if current == LifecycleState.REVIEW and target == LifecycleState.DRAFT:
        return True
    current_idx = _LIFECYCLE_ORDER.index(current)
    target_idx = _LIFECYCLE_ORDER.index(target)
    return target_idx == current_idx + 1


class ComponentType(str, Enum):
    """Kernel §1: 'a diferença entre eles é o tipo (component_type), não a
    forma' — open set by design (§9, Extension Model). Only the types this
    runtime's demo exercises are enumerated; the Kernel itself never closes
    this list."""

    STANDARD = "Standard"
    POLICY = "Policy"
    SKILL = "Skill"
    AGENT = "Agent"
    WORKFLOW = "Workflow"


@dataclass
class IOField:
    """One entry of Inputs (§2.4) or Outputs (§2.5) — name, type, required/optional."""

    name: str
    type: str
    required: bool = True
    default: Any = None


@dataclass
class Dependency:
    """Kernel §2.6 — Identity + compatible version range."""

    coordinate: Coordinate
    version_range: str


@dataclass
class Constraint:
    """Kernel §2.10 — conditions under which the component MUST NOT be used,
    or the limits within which its correctness guarantee holds."""

    name: str
    kind: str
    detail: dict[str, Any] = field(default_factory=dict)


@dataclass
class Manifest:
    """Kernel §6 — the declarative materialization of the Component Contract.
    Exactly the same structure for a Standard, a Skill, or a Workflow (§6,
    "Regra de uniformidade") — only field *content* differs by component_type.
    """

    # 1. identity (§2.1) — permanent, namespace + local name; component_type is
    #    classification metadata riding alongside it, not part of Namespace (Identity §3.1)
    identity: Coordinate
    component_type: ComponentType
    # 2. purpose (§2.2)
    purpose: str
    # 3. owner (§2.3)
    owner: str
    # 4. version (§2.11)
    version: str
    # 5. lifecycle_state (§2.12)
    lifecycle_state: LifecycleState
    # 6. inputs (§2.4)
    inputs: list[IOField] = field(default_factory=list)
    # 7. outputs (§2.5)
    outputs: list[IOField] = field(default_factory=list)
    # 8. dependencies (§2.6)
    dependencies: list[Dependency] = field(default_factory=list)
    # 9. consumers (§2.7) — system-maintained, never authored
    consumers: list[Coordinate] = field(default_factory=list)
    # 10. providers (§2.8)
    providers: list[Coordinate] = field(default_factory=list)
    # 11. capabilities (§2.9)
    capabilities: list[str] = field(default_factory=list)
    # 12. constraints (§2.10)
    constraints: list[Constraint] = field(default_factory=list)
    # 13. compatibility (§2.13)
    compatibility: dict[str, Any] = field(default_factory=dict)
    # 14. metadata (§2.14)
    metadata: dict[str, Any] = field(default_factory=dict)
    # 15. validation (§2.15)
    validation: dict[str, Any] = field(default_factory=dict)

    # Additive, enabled by Kernel §9 Extension Model — NOT part of the 15 (Template §1,
    # Skill §5 field table: "templates[] — campo adicional já normatizado por Template
    # Architecture §4.2, não introduzido aqui"). Raw dicts here; runtime/template/model.py
    # parses them into Template value objects on demand.
    templates: list[dict[str, Any]] = field(default_factory=list)
    test_suite: list[dict[str, Any]] = field(default_factory=list)

    def versioned_identifier(self) -> VersionedIdentifier:
        return VersionedIdentifier(coordinate=self.identity, version=self.version)


MANDATORY_FIELDS = (
    "identity", "purpose", "owner", "version", "lifecycle_state",
    "inputs", "outputs", "dependencies", "consumers", "providers",
    "capabilities", "constraints", "compatibility", "metadata", "validation",
)
assert len(MANDATORY_FIELDS) == 15, "Kernel §2 — Component Contract has exactly 15 fields"
