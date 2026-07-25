"""Identity & Namespace Architecture (docs/architecture/06) — §3 Namespace Model,
§4 Identifier Specification.

Coordinate: <namespace>/<local-name>                         (§4.1)
VersionedIdentifier: <namespace>/<local-name>@<semver>        (§4.1)
InstanceIdentifier: ULID, 26 chars, Crockford Base32          (§4.2, §4.4)

Encoding (§4.4): namespace/local-name segments MUST use only [a-z0-9], '-', '.'.
"""

from __future__ import annotations

import os
import re
import time
from dataclasses import dataclass

_SEGMENT_RE = re.compile(r"^[a-z0-9]+(?:[-.][a-z0-9]+)*$")
_SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
_CROCKFORD_ALPHABET = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"  # Crockford Base32, no I L O U


class IdentityError(ValueError):
    pass


@dataclass(frozen=True)
class Coordinate:
    """<namespace>/<local-name> — permanent identity, independent of version (§4.1)."""

    namespace: str
    local_name: str

    def __post_init__(self) -> None:
        for segment in self.namespace.split("."):
            if not _SEGMENT_RE.match(segment):
                raise IdentityError(f"invalid namespace segment {segment!r} in {self.namespace!r} (§4.4)")
        if not _SEGMENT_RE.match(self.local_name):
            raise IdentityError(f"invalid local-name {self.local_name!r} (§4.4)")

    @classmethod
    def parse(cls, text: str) -> "Coordinate":
        if "@" in text:
            raise IdentityError(f"{text!r} carries a version — use VersionedIdentifier.parse (§4.1)")
        if "/" not in text:
            raise IdentityError(f"{text!r} is not a well-formed Coordinate (§4.1)")
        namespace, local_name = text.rsplit("/", 1)
        return cls(namespace=namespace, local_name=local_name)

    def __str__(self) -> str:
        return f"{self.namespace}/{self.local_name}"


@dataclass(frozen=True)
class VersionedIdentifier:
    """<namespace>/<local-name>@<semver> — identity + one specific version (§4.1)."""

    coordinate: Coordinate
    version: str

    def __post_init__(self) -> None:
        if not _SEMVER_RE.match(self.version):
            raise IdentityError(f"version {self.version!r} MUST be strict SemVer 2.0.0 (Kernel §2.11, §4.4)")

    @classmethod
    def parse(cls, text: str) -> "VersionedIdentifier":
        if "@" not in text:
            raise IdentityError(f"{text!r} has no version — use Coordinate.parse (§4.1)")
        coord_part, version = text.rsplit("@", 1)
        return cls(coordinate=Coordinate.parse(coord_part), version=version)

    def semver_tuple(self) -> tuple[int, int, int]:
        major, minor, patch = self.version.split(".")
        return int(major), int(minor), int(patch)

    def __str__(self) -> str:
        return f"{self.coordinate}@{self.version}"


def new_instance_identifier() -> str:
    """ULID, 26 chars, Crockford Base32 (§4.2, §4.4) — for Execution/Artifact/Evidence/
    Context Snapshot/Decision Record instances. No central coordination (§4.2 justification)."""
    timestamp_ms = int(time.time() * 1000)
    time_part = _encode_crockford(timestamp_ms, 10)
    randomness = int.from_bytes(os.urandom(10), "big")
    random_part = _encode_crockford(randomness, 16)
    return time_part + random_part


def _encode_crockford(value: int, length: int) -> str:
    chars = []
    for _ in range(length):
        chars.append(_CROCKFORD_ALPHABET[value % 32])
        value //= 32
    return "".join(reversed(chars))


def urn(versioned: VersionedIdentifier, entity_type: str | None = None, instance_id: str | None = None) -> str:
    """urn:framework-eng:<coordinate>[@<version>][:<entity-type>:<instance-id>]  (§4.3)."""
    base = f"urn:framework-eng:{versioned}"
    if entity_type and instance_id:
        return f"{base}:{entity_type}:{instance_id}"
    return base


def qualified_template_id(owner: VersionedIdentifier, local_id: str) -> str:
    """<owner-coordinate>@<version>#template.<local-id>  (Template Architecture §5.1).
    Templates have no Coordinate of their own (Template §1.1) — always addressed through
    their owning Component."""
    return f"{owner}#template.{local_id}"


def qualified_requirement_id(owner: VersionedIdentifier, rid: str) -> str:
    """<standard-coordinate>@<version>#<local-rid>  (Standards Architecture §5.1) —
    included for completeness; not exercised by this runtime's demo, kept for
    consistency with the same qualification pattern used throughout."""
    return f"{owner}#{rid}"
