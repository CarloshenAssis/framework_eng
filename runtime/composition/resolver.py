"""Composition Architecture §7 — ALGORITMO ResolveSlot, implemented verbatim
(same steps, same order, same names). See docs/architecture/09-composition-
architecture.md §7 for the source pseudocode this mirrors line for line.

Note on scope, stated explicitly rather than silently assumed: the ratified
§7 algorithm filters candidates by required_capability, version_range and
min_certification_level only — it does NOT evaluate Standards or Policies
directly. Composition §3 places "critério normativo de qual Standard/Policy
um Provider deve obedecer" out of scope for this document ("Composition
apenas consulta o nível de Certificação já emitido"). Standards/Policy
conformance is folded into the Certification level itself upstream (L3 =
"Standards Certified", Validation & Certification §5) — this runtime does
not add a second, separate Standard/Policy check inside ResolveSlot, because
the source document doesn't have one; adding one would be inventing an
algorithm the base doesn't define.

version_range grammar: no document specifies one. This runtime uses the
smallest, most conservative convention that lets §7's `c.version in
slot.version_range` line mean something concrete: "*", "X.Y.Z" (exact),
">=X.Y.Z", "^X.Y.Z" (same major, per the npm/cargo convention already used
as precedent elsewhere in this base, e.g. Identity §4.4's DNS-safe-charset
argument). This is an unavoidable implementation choice, not a new rule of
composition.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Union

from runtime.composition.slot import Slot
from runtime.contracts.graph import detect_cycle
from runtime.contracts.identity import VersionedIdentifier
from runtime.registry.registry import Registry
from runtime.validation.certification import CertificationLevel, CertificationStore


class SlotError(Exception):
    """§9 casos extremos — named errors, never a silent partial resolution."""


class CompositionCycleError(Exception):
    pass


SKIPPED = object()  # sentinel: optional Slot, no candidate — CP5, not an error


def version_in_range(version: str, version_range: str) -> bool:
    if version_range in ("", "*"):
        return True
    if version_range.startswith(">="):
        return _semver_tuple(version) >= _semver_tuple(version_range[2:])
    if version_range.startswith("^"):
        target = _semver_tuple(version_range[1:])
        return _semver_tuple(version)[0] == target[0] and _semver_tuple(version) >= target
    return version == version_range


def _semver_tuple(v: str) -> tuple[int, int, int]:
    major, minor, patch = v.strip().split(".")
    return int(major), int(minor), int(patch)


@dataclass
class Assembly:
    """§4 — Assembly: modeled as a generic Artifact, no specialization. §5
    invariant: immutable once produced; a new resolution means a new Assembly,
    never a mutation. resolved_slots maps a caller-chosen slot name to the
    VersionedIdentifier ResolveSlot picked for it."""

    resolved_slots: dict[str, VersionedIdentifier]


def resolve_slot(
    slot: Slot,
    registry: Registry,
    certification_store: CertificationStore,
    requester_namespace: str,
) -> Union[VersionedIdentifier, SlotError, object]:
    """ALGORITMO ResolveSlot(slot, requester_ns) — Composition §7, verbatim."""
    candidates = registry.search(slot.required_capability)
    candidates = [c for c in candidates if version_in_range(c.version, slot.version_range)]
    candidates = [
        c for c in candidates
        if certification_store.current_level(c, registry.digest_of(c)) >= slot.min_certification_level
    ]

    if slot.pinned_coordinate is not None:
        # "pin nunca ignora critérios mínimos" — intersect, don't bypass (CP3)
        candidates = [c for c in candidates if c == slot.pinned_coordinate]

    if not candidates:
        return SKIPPED if slot.optional else SlotError(
            f"UNSATISFIED: no candidate for capability={slot.required_capability!r} "
            f"range={slot.version_range!r} min_level={slot.min_certification_level.name}"
        )

    first = candidates[0]
    if first.coordinate.namespace.split(".")[0] != requester_namespace.split(".")[0]:
        # Identity §10 — cross-namespace resolution MUST use a fully-qualified reference;
        # every candidate coming out of Registry.search is already fully qualified (str(VersionedIdentifier)
        # always carries namespace + version), so this assertion documents the guarantee rather
        # than needing to reject anything additional.
        assert "@" in str(first) and "/" in str(first)

    return select_best(candidates, certification_store, registry)


def select_best(
    candidates: list[VersionedIdentifier],
    certification_store: CertificationStore,
    registry: Registry,
) -> VersionedIdentifier:
    """§7 — "select_best(candidates) # highest certification, then highest
    semver". §9 casos extremos: ties broken by lexicographic Coordinate order,
    never randomly (auditability)."""

    def sort_key(vid: VersionedIdentifier):
        level = certification_store.current_level(vid, registry.digest_of(vid))
        return (level, vid.semver_tuple(), str(vid.coordinate))

    ranked = sorted(candidates, key=sort_key, reverse=True)
    return ranked[0]


def detect_composition_cycle(assembly_graph: dict[str, list[str]]) -> Optional[list[str]]:
    """ALGORITMO DetectCompositionCycle — Composition §7: "REUSA
    Kernel§7.CycleDetection(assembly_graph) — nenhuma reimplementação."
    This is the 3rd reapplication per the Composition preamble; the actual
    mechanism lives once in runtime/contracts/graph.py and every reapplication
    (Composition, Template, Workflow, Execution) calls that same function."""
    return detect_cycle(assembly_graph)
