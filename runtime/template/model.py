"""Template Architecture (docs/architecture/14) §4.2 — Template, Variable,
Placeholder value objects, verbatim. A Template is explicitly NOT a
Component (§1.1): no Identity, no Coordinate, no Registry resolution, no
Lifecycle of its own — it lives in the templates[] field of its owning
Component's Manifest and is addressed only through a qualified reference
(§5.1)."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional

_PLACEHOLDER_RE = re.compile(r"\{\{\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\}\}")


class TemplateKind(str, Enum):
    PROMPT = "PROMPT"
    INPUT = "INPUT"
    OUTPUT = "OUTPUT"


class BindingSource(str, Enum):
    """§5.2 — four sources, precedence PARAMETER > CONTEXT >
    COMPOSITION_RESOLVED > LITERAL (TP1, strict, no exception)."""

    PARAMETER = "PARAMETER"
    CONTEXT = "CONTEXT"
    COMPOSITION_RESOLVED = "COMPOSITION_RESOLVED"
    LITERAL = "LITERAL"


@dataclass
class Placeholder:
    """§4.2 — resolves against a Variable in scope (§8, K1)."""

    variable_ref: str
    position: Any = None
    format_hint: Optional[str] = None


@dataclass
class Variable:
    """§4.2."""

    name: str
    type: str = "string"
    required: bool = False
    default_value: Any = None
    binding_source: BindingSource = BindingSource.LITERAL
    constraint: Optional[dict[str, Any]] = None


@dataclass
class Template:
    """§4.2 — Value Object, field of a Manifest's templates[]."""

    local_id: str
    kind: TemplateKind
    content: str  # opaque TemplateContent per §4.2 — this runtime treats it as
                  # text with inline {{var}} Placeholders, the simplest concrete
                  # realization of "opaque to this document"
    variables: list[Variable] = field(default_factory=list)
    extends: Optional[str] = None  # QualifiedTemplateIdentifier, §6.1
    includes: list[str] = field(default_factory=list)  # QualifiedTemplateIdentifier[], §6.2
    deterministic_expansion: bool = True  # §4.2 — MUST be true (§7, TP2); K7

    def placeholders(self) -> list[Placeholder]:
        """Extracts Placeholders from `content` by scanning for {{name}}
        occurrences — the concrete mechanism behind the opaque TemplateContent
        this document deliberately does not specify further (§4.2)."""
        return [Placeholder(variable_ref=name) for name in extract_placeholder_names(self.content)]


def extract_placeholder_names(content: str) -> list[str]:
    return [m.group(1) for m in _PLACEHOLDER_RE.finditer(content)]


def render_mechanico(content: str, bindings: dict[str, Any]) -> str:
    """RenderMecanico (Template §11.3) — pure syntactic substitution, no I/O (§7)."""
    def replace(match: "re.Match[str]") -> str:
        value = bindings[match.group(1)]
        return value if isinstance(value, str) else json.dumps(value)

    return _PLACEHOLDER_RE.sub(replace, content)


@dataclass
class EffectiveTemplate:
    """Output of ResolveEffectiveTemplate (§11.1) — the transitive closure of
    variables/content over extends ∪ includes, deduplicated."""

    qualified_id: str
    content: str
    variables: dict[str, Variable]  # keyed by qualified name (§8 K3)


@dataclass
class VariableBindingSet:
    """Output of BindVariables (§11.2)."""

    bindings: dict[str, Any]


def parse_template(raw: dict[str, Any]) -> Template:
    """Parses the templates[] dict entries already present in institutional
    Manifests (components/core/*.yaml) into the Template value object above —
    no new schema, just loading the one §4.2 already defines."""
    variables = [
        Variable(
            name=v["name"],
            type=v.get("type", "string"),
            required=v.get("required", False),
            default_value=v.get("default_value"),
            binding_source=BindingSource(v.get("binding_source", "LITERAL")),
            constraint=v.get("constraint"),
        )
        for v in raw.get("variables", [])
    ]
    return Template(
        local_id=raw["local_id"],
        kind=TemplateKind(raw["kind"]),
        content=raw["content"],
        variables=variables,
        extends=raw.get("extends"),
        includes=raw.get("includes", []) or [],
        deterministic_expansion=raw.get("deterministic_expansion", True),
    )
