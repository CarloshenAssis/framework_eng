"""Composition Architecture (docs/architecture/09) §4 — Composition Slot,
verbatim structure. A Value Object scoped to the Contract of whoever
declares it (Kernel §9 Extension Model) — no Identity of its own, same
class as Capability (Identity §2.2)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Callable, Optional

from runtime.contracts.identity import VersionedIdentifier
from runtime.validation.certification import CertificationLevel


class Cardinality(str, Enum):
    EXACTLY_ONE = "EXACTLY_ONE"
    ONE_OF_MANY = "ONE_OF_MANY"
    ALL_OF_MANY = "ALL_OF_MANY"


@dataclass
class Slot:
    """§4 — Composition Slot structure, field for field."""

    required_capability: str
    version_range: str  # SemVer range, e.g. ">=1.0.0"; kept as a simple predicate below
    min_certification_level: CertificationLevel = CertificationLevel.L0
    cardinality: Cardinality = Cardinality.EXACTLY_ONE
    optional: bool = False
    condition: Optional[Callable[[dict], bool]] = None  # Predicate<Context>
    pinned_coordinate: Optional[VersionedIdentifier] = None
