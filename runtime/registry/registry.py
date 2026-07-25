"""Registry & Discovery Architecture (docs/architecture/07).

§1: "O Registry nunca decide; ele reflete." It indexes Components (§3.1) and
explicitly does NOT index Execution/Artifact/Evidence/Knowledge/Decision
Record instances (§3.2, R8) — those use their Instance Identifier directly.

Implements, verbatim, §6.1 resolve() and §6.2 search(). Certification-level
lookup is injected (Callable), not imported directly, so this module stays
independent of runtime/validation/ per the requested module boundaries —
Registry only needs to *read* a level for sorting (§6.2 step 3), it never
computes or grants one (that boundary is Validation & Certification's, §12
"Registry apenas surfaces o resultado; não executa validação").
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Callable, Optional

from runtime.contracts.component import LifecycleState, Manifest, MANDATORY_FIELDS
from runtime.contracts.identity import Coordinate, VersionedIdentifier

MAX_REDIRECT_DEPTH = 5  # Identity §6.6; Registry §6.1 step 4, R6


class RegistryError(Exception):
    """Base for the named errors in §13: NotFound, Ambiguous,
    RedirectLoopExceeded, IntegrityViolation, Unauthorized."""


class NotFound(RegistryError):
    pass


class Unauthorized(RegistryError):
    pass


class RedirectLoopExceeded(RegistryError):
    pass


class StructuralValidationError(RegistryError):
    """Kernel §8 — Validação Estrutural failed."""


@dataclass
class RegistryEntry:
    """§4 — Registry Entry: 1:1 with a Coordinate. Lifecycle state is a
    read-only projection of the Kernel Lifecycle (§7.3), never an
    independently-mutated field."""

    coordinate: Coordinate
    lineage: list[Manifest] = field(default_factory=list)  # ordered by version, §4 Lineage Index
    redirect_to: Optional[Coordinate] = None
    aliases: list[str] = field(default_factory=list)
    manifest_digests: dict[str, str] = field(default_factory=dict)  # version -> digest

    @property
    def lifecycle_state(self) -> LifecycleState:
        return self.lineage[-1].lifecycle_state if self.lineage else LifecycleState.REMOVED

    def manifest_for(self, version: str) -> Optional[Manifest]:
        for m in self.lineage:
            if m.version == version:
                return m
        return None

    def current_active(self) -> Optional[Manifest]:
        """§6.1 step 2 — "current" = highest version with lifecycle_state=Active."""
        actives = [m for m in self.lineage if m.lifecycle_state == LifecycleState.ACTIVE]
        if not actives:
            return None
        return max(actives, key=lambda m: VersionedIdentifier(self.coordinate, m.version).semver_tuple())


@dataclass
class ResolvedIdentity:
    """§6.1 step 6 — return shape of resolve()."""

    canonical_urn: str
    lifecycle_state: LifecycleState
    manifest: Manifest
    resolution_path: list[str]
    certification_level: Optional[str] = None


def manifest_digest(manifest: Manifest) -> str:
    """§12 (Template Architecture) / Validation & Certification §6 — "hash sobre
    a serialização canônica". Canonical serialization reuses Identity §4.4's
    own rule (deterministic field order, no insignificant whitespace); this
    runtime picks SHA-256 as the concrete hash, since no document mandates one
    specific algorithm, only that the digest be a deterministic content hash."""
    canonical = {
        "identity": str(manifest.identity),
        "component_type": manifest.component_type.value,
        "purpose": manifest.purpose,
        "owner": manifest.owner,
        "version": manifest.version,
        "lifecycle_state": manifest.lifecycle_state.value,
        "inputs": [(f.name, f.type, f.required, f.default) for f in manifest.inputs],
        "outputs": [(f.name, f.type, f.required, f.default) for f in manifest.outputs],
        "dependencies": [(str(d.coordinate), d.version_range) for d in manifest.dependencies],
        "consumers": [str(c) for c in manifest.consumers],
        "providers": [str(p) for p in manifest.providers],
        "capabilities": sorted(manifest.capabilities),
        "constraints": [(c.name, c.kind, c.detail) for c in manifest.constraints],
        "compatibility": manifest.compatibility,
        "metadata": manifest.metadata,
        "validation": manifest.validation,
        "templates": manifest.templates,
        "test_suite": manifest.test_suite,
    }
    serialized = json.dumps(canonical, sort_keys=True, separators=(",", ":"))
    return "sha256:" + hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def validate_structural(manifest: Manifest) -> None:
    """Kernel §8 — Validação Estrutural: all fifteen Contract fields present
    and well-formed. dataclass field presence already guarantees "present";
    this checks the "well-formed" half the dataclass constructor doesn't."""
    for name in MANDATORY_FIELDS:
        if not hasattr(manifest, name):
            raise StructuralValidationError(f"missing mandatory field {name!r} (Kernel §2)")
    if not manifest.purpose.strip():
        raise StructuralValidationError("purpose (§2.2) MUST NOT be empty")
    if not manifest.owner.strip():
        raise StructuralValidationError("owner (§2.3) MUST be identifiable — Kernel §2.3")
    if manifest.lifecycle_state == LifecycleState.ACTIVE and not manifest.capabilities and not manifest.dependencies:
        # Not a hard rule from any document; deliberately NOT enforced as an error —
        # Kernel §2.9/§2.10 allow an empty Capabilities/Constraints declaration.
        pass


class Registry:
    """§1 — substrate service, not itself a Component (avoids the regression
    Kubernetes' API server avoids by not being an ordinary etcd object)."""

    def __init__(self, certification_lookup: Optional[Callable[[VersionedIdentifier], int]] = None) -> None:
        self._entries: dict[str, RegistryEntry] = {}  # keyed by str(coordinate)
        self._capability_index: dict[str, set[str]] = {}  # capability -> {coordinate str}
        # §6.2 step 3 needs certification_level for sort order; §12 keeps Registry from
        # ever computing/deciding it itself. Default: everything ranks equal (L0).
        self._certification_lookup = certification_lookup or (lambda vid: 0)

    def register(self, manifest: Manifest, decision_record_ref: str) -> RegistryEntry:
        """§5 register()/publish_version() — PRE: decision_record_ref references
        a valid Admission Decision (Governance §7); R1: Registration Service
        MUST reject writes without one. This runtime does not implement the
        Governance Admission workflow (out of scope) — it enforces exactly the
        precondition Registry itself states, treating decision_record_ref as
        an opaque required reference, never fabricating one."""
        if not decision_record_ref or not decision_record_ref.strip():
            raise Unauthorized("register() requires a decision_record_ref (Registry §5 register(), R1)")
        validate_structural(manifest)

        key = str(manifest.identity)
        entry = self._entries.get(key)
        if entry is None:
            entry = RegistryEntry(coordinate=manifest.identity)
            self._entries[key] = entry
        else:
            existing = entry.manifest_for(manifest.version)
            if existing is not None:
                raise RegistryError(f"version {manifest.version} already registered for {key}")

        entry.lineage.append(manifest)
        entry.lineage.sort(key=lambda m: VersionedIdentifier(manifest.identity, m.version).semver_tuple())
        entry.manifest_digests[manifest.version] = manifest_digest(manifest)

        for capability in manifest.capabilities:
            self._capability_index.setdefault(capability, set()).add(key)

        return entry

    def resolve(self, reference: str) -> ResolvedIdentity:
        """§6.1 — resolve() canonical algorithm, verbatim."""
        resolution_path: list[str] = [reference]

        # step 1: fully-qualified Versioned Identifier -> direct lineage lookup
        if "@" in reference:
            vid = VersionedIdentifier.parse(reference)
            entry = self._entries.get(str(vid.coordinate))
            if entry is None:
                raise NotFound(f"{reference} not found in Registry")
            manifest = entry.manifest_for(vid.version)
            if manifest is None:
                raise NotFound(f"version {vid.version} of {vid.coordinate} not found")
            return self._finish_resolve(entry, manifest, resolution_path)

        # step 2: Coordinate without version -> resolve "current" (highest Active)
        coordinate = Coordinate.parse(reference)
        entry = self._entries.get(str(coordinate))
        if entry is None:
            raise NotFound(f"{reference} not found in Registry")

        # step 4: follow redirect chain (bounded depth, §6.1 step 4 / R6)
        depth = 0
        while entry.redirect_to is not None:
            depth += 1
            if depth > MAX_REDIRECT_DEPTH:
                raise RedirectLoopExceeded(f"redirect chain from {reference} exceeded {MAX_REDIRECT_DEPTH} hops")
            resolution_path.append(str(entry.redirect_to))
            entry = self._entries[str(entry.redirect_to)]

        # step 5: tombstone
        if entry.lifecycle_state == LifecycleState.REMOVED:
            return ResolvedIdentity(
                canonical_urn=f"urn:framework-eng:{entry.coordinate}",
                lifecycle_state=LifecycleState.REMOVED,
                manifest=entry.lineage[-1] if entry.lineage else None,  # type: ignore[arg-type]
                resolution_path=resolution_path,
            )

        manifest = entry.current_active()
        if manifest is None:
            raise NotFound(f"{reference} has no Active version")
        return self._finish_resolve(entry, manifest, resolution_path)

    def _finish_resolve(self, entry: RegistryEntry, manifest: Manifest, resolution_path: list[str]) -> ResolvedIdentity:
        vid = VersionedIdentifier(entry.coordinate, manifest.version)
        return ResolvedIdentity(
            canonical_urn=f"urn:framework-eng:{vid}",
            lifecycle_state=manifest.lifecycle_state,
            manifest=manifest,
            resolution_path=resolution_path,
            certification_level=_level_name(self._certification_lookup(vid)),
        )

    def search(self, capability: str, include_deprecated: bool = False) -> list[VersionedIdentifier]:
        """§6.2 — search(): capability index -> filter lifecycle -> sort by
        certification_level DESC, version DESC -> return candidates."""
        allowed_states = {LifecycleState.ACTIVE}
        if include_deprecated:
            allowed_states.add(LifecycleState.DEPRECATED)

        candidates: list[VersionedIdentifier] = []
        for key in self._capability_index.get(capability, set()):
            entry = self._entries[key]
            manifest = entry.current_active()
            if manifest is None and include_deprecated:
                deprecated = [m for m in entry.lineage if m.lifecycle_state == LifecycleState.DEPRECATED]
                manifest = max(
                    deprecated,
                    key=lambda m: VersionedIdentifier(entry.coordinate, m.version).semver_tuple(),
                    default=None,
                )
            if manifest is None or manifest.lifecycle_state not in allowed_states:
                continue
            candidates.append(VersionedIdentifier(entry.coordinate, manifest.version))

        candidates.sort(
            key=lambda vid: (self._certification_lookup(vid), vid.semver_tuple()),
            reverse=True,
        )
        return candidates

    def lineage(self, coordinate: Coordinate) -> list[Manifest]:
        entry = self._entries.get(str(coordinate))
        if entry is None:
            raise NotFound(f"{coordinate} not found in Registry")
        return list(entry.lineage)

    def digest_of(self, versioned: VersionedIdentifier) -> str:
        entry = self._entries.get(str(versioned.coordinate))
        if entry is None or versioned.version not in entry.manifest_digests:
            raise NotFound(f"{versioned} not found in Registry")
        return entry.manifest_digests[versioned.version]


_LEVEL_NAMES = ["L0", "L1", "L2", "L3", "L4"]


def _level_name(level: int) -> str:
    return _LEVEL_NAMES[level] if 0 <= level < len(_LEVEL_NAMES) else "L0"
