"""Validation & Certification Architecture (docs/architecture/08) — §5, §6.

Deliberately minimal: this runtime does not implement the Certification
pipeline (Evidence collection, multi-dimension scoring, human Certifier
workflow for L4, Suspension/Revocation) — that is Testing/Governance
machinery explicitly out of scope for this Runtime. What Composition's own
documented algorithm (Composition §7) actually needs from Certification is
a single read: "what level does this Coordinate@version currently hold,
honoring Integrity" (§6: a grant is void if today's manifest_digest doesn't
match the one signed at grant time). This module implements exactly that
read, nothing upstream of it.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum

from runtime.contracts.identity import VersionedIdentifier


class CertificationLevel(IntEnum):
    """§5 — L0 Unverified .. L4 Institutionally Certified. Ordered: a higher
    IntEnum value MUST always mean "at least as certified", never the reverse
    (Composition §7 compares with >=)."""

    L0 = 0  # Unverified — default on entering Active
    L1 = 1  # Structurally Valid
    L2 = 2  # Functionally Validated
    L3 = 3  # Standards Certified
    L4 = 4  # Institutionally Certified


@dataclass
class CertificationGrant:
    """§6 — "todo CertificationGrant MUST incluir { certifier_role_id,
    timestamp, manifest_digest }"."""

    level: CertificationLevel
    manifest_digest: str
    certifier_role_id: str
    granted_at: str


class CertificationStore:
    """Read/write surface reduced to exactly what §5/§6 and Composition §7
    require. No Suspended/Revoked/Expired state machine (§5 diagram) —
    out of scope; a missing grant simply reads as L0, the documented default."""

    def __init__(self) -> None:
        self._grants: dict[str, CertificationGrant] = {}  # keyed by str(VersionedIdentifier)

    def grant(self, versioned: VersionedIdentifier, level: CertificationLevel,
              manifest_digest: str, certifier_role_id: str, granted_at: str) -> CertificationGrant:
        grant = CertificationGrant(
            level=level, manifest_digest=manifest_digest,
            certifier_role_id=certifier_role_id, granted_at=granted_at,
        )
        self._grants[str(versioned)] = grant
        return grant

    def current_level(self, versioned: VersionedIdentifier, actual_manifest_digest: str) -> CertificationLevel:
        """§6 Integrity rule: "se o Manifest resolvido hoje não bate com o
        digest assinado, a Certificação é automaticamente inválida
        independentemente do status registrado — Integrity é verificada em
        tempo de leitura, não apenas em tempo de escrita." A digest mismatch
        reads as L0, never as an exception — L0 is already the documented
        floor (§5), so this introduces no new state."""
        grant = self._grants.get(str(versioned))
        if grant is None:
            return CertificationLevel.L0
        if grant.manifest_digest != actual_manifest_digest:
            return CertificationLevel.L0
        return grant.level

    def current_level_as_int(self, versioned: VersionedIdentifier, actual_manifest_digest: str) -> int:
        """Convenience for Registry's certification_lookup callback (registry.py
        expects a plain int for sorting, to stay free of a validation/ import)."""
        return int(self.current_level(versioned, actual_manifest_digest))
