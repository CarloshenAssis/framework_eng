"""Template Architecture §11 — ResolveEffectiveTemplate, BindVariables,
Expand, ClassifyTemplateChange. Implemented step-for-step against the
pseudocode in docs/architecture/14-template-architecture.md §11.1-§11.4;
line comments below cite the exact source line being mirrored.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any, Callable, Optional

from runtime.composition.resolver import Assembly
from runtime.contracts.component import LifecycleState
from runtime.contracts.graph import detect_cycle, topological_sort
from runtime.registry.registry import Registry
from runtime.template.model import (
    BindingSource,
    EffectiveTemplate,
    Template,
    VariableBindingSet,
    extract_placeholder_names,
    parse_template,
    render_mechanico,
)


class TemplateError(Exception):
    pass


class BindingError(Exception):
    pass


# Signature: given "<owner>@<version>#template.<local_id>", return the raw dict
# from that owner's Manifest.templates[]. Kept as an injected lookup so this
# module never needs to know how a Registry stores Manifests internally.
TemplateLookup = Callable[[str], dict[str, Any]]


def _split_qualified_id(qualified_id: str) -> tuple[str, str]:
    owner, _, local = qualified_id.partition("#template.")
    if not local:
        raise TemplateError(f"{qualified_id!r} is not a qualified Template id (§5.1)")
    return owner, local


def make_template_lookup(registry: Registry) -> TemplateLookup:
    """Default TemplateLookup backed by a Registry: resolves the owner
    Coordinate@version, then finds the templates[] entry with that local_id."""

    def lookup(qualified_id: str) -> dict[str, Any]:
        owner, local_id = _split_qualified_id(qualified_id)
        resolved = registry.resolve(owner)
        for raw in resolved.manifest.templates:
            if raw["local_id"] == local_id:
                return raw
        raise TemplateError(f"no template {local_id!r} on {owner} (§11.1)")

    return lookup


def resolve_effective_template(template_ref: str, registry: Registry, lookup: TemplateLookup) -> EffectiveTemplate:
    """ALGORITMO ResolveEffectiveTemplate(template_ref) — §11.1."""
    owner_coordinate, _ = _split_qualified_id(template_ref)               # line 1 (owner_entry)
    resolved = registry.resolve(owner_coordinate)
    if resolved.lifecycle_state not in (LifecycleState.ACTIVE, LifecycleState.DEPRECATED):  # line 2-3
        raise TemplateError("OWNER_NOT_BINDABLE")

    graph, nodes = _build_reference_graph(template_ref, lookup)            # line 5
    cycle = detect_cycle(graph)                                            # line 6 — Kernel §7, 6th reapplication
    if cycle:
        raise TemplateError(f"CYCLIC_TEMPLATE_GRAPH: {' -> '.join(cycle)}")  # line 7, K4

    order = topological_sort(graph)
    order.reverse()                                                        # line 10

    merged_vars: dict[str, Any] = {}                                       # line 9 (OrderedMap)
    for qid in order:                                                      # line 10
        node = nodes[qid]
        edge_kind = node["edge_kind"]
        for v in node["template"].variables:                               # line 11
            qname = f"{node['owner']}::{v.name}" if edge_kind == "includes" else v.name  # line 12, Qualify()
            if qname in merged_vars:                                       # line 13
                if edge_kind == "includes":
                    raise TemplateError(f"ILLEGAL_MODIFY_IN_INCLUDES: {qname}")  # line 14, K6
                existing = merged_vars[qname]
                if v.required and not existing.required:                   # line 15
                    raise TemplateError(f"ILLEGAL_REQUIREMENT_STRENGTHENING: {qname}")  # line 16, K5
            merged_vars[qname] = v                                         # line 17

    assert len(merged_vars) == len(set(merged_vars))                       # line 19, K3 (dict keys are already unique)
    root = nodes[template_ref]["template"]
    return EffectiveTemplate(qualified_id=template_ref, content=root.content, variables=merged_vars)  # line 20


def _build_reference_graph(root_id: str, lookup: TemplateLookup) -> tuple[dict[str, list[str]], dict[str, dict]]:
    graph: dict[str, list[str]] = {}
    nodes: dict[str, dict] = {}

    def visit(qid: str, owner: str, edge_kind: str) -> None:
        if qid in nodes:
            return
        raw = lookup(qid)
        template = parse_template(raw)
        nodes[qid] = {"template": template, "owner": owner, "edge_kind": edge_kind}
        edges = []
        if template.extends:
            edges.append(template.extends)
            owner_ext, _ = _split_qualified_id(template.extends)
            visit(template.extends, owner_ext, "extends")
        for inc in template.includes:
            edges.append(inc)
            owner_inc, _ = _split_qualified_id(inc)
            visit(inc, owner_inc, "includes")
        graph[qid] = edges

    owner_root, _ = _split_qualified_id(root_id)
    visit(root_id, owner_root, "self")
    return graph, nodes




def bind_variables(
    effective_template: EffectiveTemplate,
    params: dict[str, Any],
    ctx_snapshot: dict[str, Any],
    assembly: Optional[Assembly],
) -> VariableBindingSet:
    """ALGORITMO BindVariables — §11.2, precedence PARAMETER > CONTEXT >
    COMPOSITION_RESOLVED > LITERAL (TP1), verbatim order of checks."""
    bindings: dict[str, Any] = {}
    assembly_slots = assembly.resolved_slots if assembly else {}

    for name, v in effective_template.variables.items():
        value = _ABSENT
        if v.name in params:
            value = params[v.name]                              # PARAMETER
        elif v.binding_source == BindingSource.CONTEXT:
            value = ctx_snapshot.get(v.name, _ABSENT)            # CONTEXT
        elif v.binding_source == BindingSource.COMPOSITION_RESOLVED:
            value = assembly_slots.get(v.name, _ABSENT)          # COMPOSITION_RESOLVED
        elif v.default_value is not None:
            value = v.default_value                              # LITERAL

        if value is _ABSENT and v.required:
            raise BindingError(f"REQUIRED_VARIABLE_UNBOUND: {name}")  # K2
        if value is not _ABSENT:
            _assert_satisfies_constraint(value, v.constraint)
            bindings[name] = value

    return VariableBindingSet(bindings=bindings)


_ABSENT = object()


def _assert_satisfies_constraint(value: Any, constraint: Optional[dict[str, Any]]) -> None:
    """Kernel §2.10 — Constraint check on a bound value. No document gives a
    single canonical Constraint evaluator; this mirrors the RANGE-style
    constraint already used in this base's own content (e.g. max-diff-size,
    components/core/skill.static-analysis.code-review.yaml)."""
    if not constraint:
        return
    if constraint.get("kind") == "RANGE" and "max_lines" in constraint:
        if isinstance(value, str) and value.count("\n") + 1 > constraint["max_lines"]:
            raise BindingError(f"constraint violated: max_lines={constraint['max_lines']}")


def expand(effective_template: EffectiveTemplate, bindings: VariableBindingSet) -> dict[str, Any]:
    """ALGORITMO Expand — §11.3. Pure substitution, no I/O (TP2). Returns the
    shape of an Artifact(ExpandedTemplate, {...}) — this runtime's execution
    module wraps it as a real Artifact instance."""
    for placeholder_name in extract_placeholder_names(effective_template.content):
        if placeholder_name not in bindings.bindings:                      # line: ASSERT p.variable_ref ∈ bindings (K1)
            raise TemplateError(f"unresolved placeholder: {placeholder_name}")

    content = render_mechanico(effective_template.content, bindings.bindings)
    return {
        "content": content,
        "template_ref": effective_template.qualified_id,
        "bindings_digest": digest_of_bindings(bindings),
    }


def template_digest(template: Template) -> str:
    """§12 — same granularity-of-manifest_digest idea (Validation &
    Certification §6), applied to a single Template's canonical content."""
    canonical = {
        "local_id": template.local_id,
        "kind": template.kind.value,
        "content": template.content,
        "variables": [
            (v.name, v.type, v.required, v.default_value, v.binding_source.value)
            for v in template.variables
        ],
        "extends": template.extends,
        "includes": template.includes,
    }
    serialized = json.dumps(canonical, sort_keys=True, separators=(",", ":"))
    return "sha256:" + hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def digest_of_bindings(bindings: VariableBindingSet) -> str:
    serialized = json.dumps(bindings.bindings, sort_keys=True, separators=(",", ":"), default=str)
    return "sha256:" + hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def classify_template_change(prev: Optional[Template], next_: Optional[Template]) -> str:
    """ALGORITMO ClassifyTemplateChange — §11.4, verbatim branches."""
    if prev is None:
        return "MINOR"
    if next_ is None:
        return "MAJOR"

    prev_vars = {v.name: v for v in prev.variables}
    next_vars = {v.name: v for v in next_.variables}

    for name, v in prev_vars.items():
        nv = next_vars.get(name)
        if nv is None:
            return "MAJOR"
        if v.required is False and nv.required is True:
            return "MAJOR"
        if v.type != nv.type:
            return "MAJOR"
    for name, v in next_vars.items():
        if name not in prev_vars:
            if v.required and v.default_value is None:
                return "MAJOR"
            return "MINOR"
    if prev.content != next_.content:
        return "MINOR"
    return "PATCH"
