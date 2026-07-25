"""Registry & Discovery Architecture §5, §6.2 — Discovery Service.

Kept as a thin, separately-named entry point because the request calls out
Discovery as its own deliverable ("Implementar: search(capability)"), even
though Registry & Discovery is a single ratified document and `search()`
itself lives on the Registry (registry.py) — Discovery Service and
Resolution Service are two named *services* over the same index (§5 table),
not two separate algorithms. This module does not reimplement search(); it
exposes it.
"""

from __future__ import annotations

from runtime.contracts.identity import VersionedIdentifier
from runtime.registry.registry import Registry


def search(registry: Registry, capability: str, include_deprecated: bool = False) -> list[VersionedIdentifier]:
    """Kernel §5 operationalized by Registry & Discovery §6.2 — discovery by
    Capability, never by manual navigation or memorized names."""
    return registry.search(capability, include_deprecated=include_deprecated)
