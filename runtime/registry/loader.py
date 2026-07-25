"""Loads the real institutional YAML Manifests already committed under
components/ into this runtime's Manifest dataclass (contracts/component.py).

This is plumbing, not a new rule: components/core/*.yaml already IS a
Kernel §6 Manifest (identity, purpose, owner, version, lifecycle_state,
inputs, outputs, capabilities, constraints, metadata, templates[]) written
in YAML. This module only parses that YAML into the dataclasses the rest
of the runtime operates on — it does not change field names or semantics.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from runtime.contracts.component import Constraint, ComponentType, Dependency, IOField, LifecycleState, Manifest
from runtime.contracts.identity import Coordinate


def load_manifest(path: str | Path) -> Manifest:
    raw: dict[str, Any] = yaml.safe_load(Path(path).read_text())

    inputs = [IOField(name=i["name"], type=i["type"], required=i.get("required", True), default=i.get("default"))
              for i in raw.get("inputs", [])]
    outputs = [IOField(name=o["name"], type=o["type"], required=o.get("required", True), default=o.get("default"))
               for o in raw.get("outputs", [])]
    dependencies = [
        Dependency(coordinate=Coordinate.parse(d["coordinate"] if "coordinate" in d else d["standard"].split("@")[0]),
                   version_range=d.get("version_range", "*"))
        for d in raw.get("dependencies", [])
    ]
    constraints = [
        Constraint(name=c["name"], kind=c.get("kind", ""), detail={k: v for k, v in c.items() if k not in ("name", "kind")})
        for c in raw.get("constraints", [])
    ]

    return Manifest(
        identity=Coordinate.parse(raw["identity"]),
        component_type=ComponentType(raw["component_type"]),
        purpose=raw["purpose"].strip(),
        owner=raw["owner"],
        version=raw["version"],
        lifecycle_state=LifecycleState(raw["lifecycle_state"]),
        inputs=inputs,
        outputs=outputs,
        dependencies=dependencies,
        consumers=[],
        providers=[Coordinate.parse(p) for p in raw.get("providers", [])],
        capabilities=list(raw.get("capabilities", [])),
        constraints=constraints,
        compatibility=raw.get("compatibility", {}),
        metadata=raw.get("metadata", {}),
        validation=raw.get("validation", {}),
        templates=list(raw.get("templates", [])),
        test_suite=list(raw.get("test_suite", [])),
    )
