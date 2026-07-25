"""Kernel Architecture §7 — "Como detectar ciclos": one shared cycle-detection
mechanism, reused verbatim everywhere the base cites it as reapplied rather
than reimplemented (dependências de Component; RFC-DM-001 §3.3 `derives_from`;
Workflow §7 grafo de fases; Composition §7 grafo de composição; Standards §6.3
`extends/includes/replaces`; Policy §7.3 `overrides`; Template §6.3
`extends/includes` — the 6th application per Template's own preamble).

This module is that one mechanism's single implementation. Every other module
in this runtime that needs cycle detection or a topological order imports
from here instead of writing its own — the point being made structurally,
not just stated in a comment.
"""

from __future__ import annotations

from typing import Optional


def detect_cycle(graph: dict[str, list[str]]) -> Optional[list[str]]:
    """DFS with a recursion stack. Returns the cycle path if one exists,
    else None. No document gives a different concrete algorithm to reuse
    instead of this standard graph technique — Kernel §7 mandates the
    *guarantee* (acyclicity), not a specific implementation."""
    visited: set[str] = set()
    stack: set[str] = set()
    path: list[str] = []

    def visit(node: str) -> Optional[list[str]]:
        visited.add(node)
        stack.add(node)
        path.append(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                cycle = visit(neighbor)
                if cycle:
                    return cycle
            elif neighbor in stack:
                return path[path.index(neighbor):] + [neighbor]
        stack.discard(node)
        path.pop()
        return None

    for node in list(graph.keys()):
        if node not in visited:
            cycle = visit(node)
            if cycle:
                return cycle
    return None


def topological_sort(graph: dict[str, list[str]]) -> list[str]:
    """Used by Execution §7 Plan() ("topological_sort(graph)") and by
    ResolveEffectiveTemplate (§11.1, "TopologicalOrder(graph)"). PRE: graph
    is acyclic — call detect_cycle first and handle a cycle as a named
    error, never feed a cyclic graph in here."""
    visited: set[str] = set()
    order: list[str] = []

    def visit(node: str) -> None:
        if node in visited:
            return
        visited.add(node)
        for neighbor in graph.get(node, []):
            visit(neighbor)
        order.append(node)

    for node in graph:
        visit(node)
    return order
