"""Workflow Architecture §7 — ALGORITMO ValidateWorkflowGraph,
EvaluateDecisionPoint, verbatim. Plus `run_workflow`: the top-level
orchestration Workflow -> Phase -> Step -> Slot -> Skill -> Artifact ->
Execution History the request asks the Workflow Runtime to perform — built
by composing Composition.ResolveSlot + Skill.InvokeSkillStep + Execution's
own bookkeeping, exactly as Skill §8's Fluxo de Execução already lays out
step by step, never introducing a parallel orchestration idea of its own.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from runtime.contracts.graph import detect_cycle
from runtime.execution.model import Evidence, Execution
from runtime.registry.registry import Registry
from runtime.skill.runtime import invoke_skill_step
from runtime.validation.certification import CertificationStore
from runtime.workflow.model import Phase, StepKind


class WorkflowValidationError(Exception):
    pass


def validate_workflow_definition(phases: list[Phase]) -> None:
    """ALGORITMO ValidateWorkflowGraph — §7."""
    graph = {p.id: list(p.next) for p in phases}
    cycle = detect_cycle(graph)  # WF1 — reused, 3rd reapplication per Composition preamble's count
    if cycle:
        raise WorkflowValidationError(f"WF1 violation: cyclic Phase graph: {' -> '.join(cycle)}")

    compensation_referencers: dict[str, int] = {}
    for phase in phases:
        for step in phase.steps:
            if step.compensated_by:
                compensation_referencers[step.compensated_by] = compensation_referencers.get(step.compensated_by, 0) + 1

    all_step_ids = {s.id for p in phases for s in p.steps}
    for phase in phases:
        for step in phase.steps:
            if step.kind == StepKind.COMPENSATION:
                referencers = compensation_referencers.get(step.id, 0)
                if referencers != 1:
                    raise WorkflowValidationError(
                        f"a COMPENSATION step MUST be referenced by exactly one non-compensation "
                        f"step; {step.id!r} is referenced {referencers} time(s)"
                    )
                if step.failure_policy.on_failure.value != "ABORT":
                    raise WorkflowValidationError(
                        f"WF4 violation: Compensation step {step.id!r} MUST have Failure Policy = ABORT"
                    )
            if step.kind == StepKind.GATE_APPROVAL and not step.role_class:
                raise WorkflowValidationError(
                    f"GATE_APPROVAL step {step.id!r} MUST reference a resolvable Role class (Governance §2)"
                )
            if step.compensated_by and step.compensated_by not in all_step_ids:
                raise WorkflowValidationError(f"{step.id!r}.compensated_by references unknown step")

    # WF6 — every Join's predecessors must be reachable from the initial Phase.
    if phases:
        reachable = _reachable_from(phases[0].id, graph)
        referenced_as_next = {target for p in phases for target in p.next}
        unreachable = referenced_as_next - reachable - {phases[0].id}
        if unreachable:
            raise WorkflowValidationError(f"WF6 violation: unreachable phase(s): {unreachable}")


def _reachable_from(start: str, graph: dict[str, list[str]]) -> set[str]:
    seen = {start}
    stack = [start]
    while stack:
        node = stack.pop()
        for neighbor in graph.get(node, []):
            if neighbor not in seen:
                seen.add(neighbor)
                stack.append(neighbor)
    return seen


def evaluate_decision_point(phase: Phase, context: dict[str, Any]) -> bool:
    """ALGORITMO EvaluateDecisionPoint — §7. A pure predicate evaluates
    without an Execution; this runtime does not implement the "predicate
    depends on Component output" branch (it would require awaiting a Step's
    Execution first) since the demo's single-Phase chain never needs a
    Branch — kept as a narrower, honestly-scoped implementation rather than
    a speculative one."""
    if phase.entry_predicate is None:
        return True
    return phase.entry_predicate(context)


@dataclass
class WorkflowRunResult:
    """Execution History — Domain Model §9: the record of what actually
    happened, assembled from the same Executions/Artifacts/Evidence any
    Step already produces; not a new persisted entity."""

    orchestration_id: str
    executions: list[Execution] = field(default_factory=list)
    artifacts: list[Any] = field(default_factory=list)
    evidence: list[Evidence] = field(default_factory=list)
    completed_phase_ids: list[str] = field(default_factory=list)


def run_workflow(
    phases: list[Phase],
    registry: Registry,
    certification_store: CertificationStore,
    orchestration_id: str,
    requester_namespace: str,
    context: Optional[dict[str, Any]] = None,
) -> WorkflowRunResult:
    """Top-level Workflow Runtime: Workflow -> Phase -> Step -> Slot -> Skill
    -> Artifact -> Execution History (Skill §8 Fluxo de Execução, applied
    phase by phase). Only StepKind.INVOCATION is dispatched through
    Composition+Skill here — GATE_AUTO/GATE_APPROVAL/COMPENSATION are
    validated (engine.py above) but not exercised by this runtime's demo,
    since GATE_APPROVAL requires a Role resolvable to an Agent/human
    (Agent Runtime is explicitly out of scope for this task)."""
    validate_workflow_definition(phases)
    context = context or {}
    result = WorkflowRunResult(orchestration_id=orchestration_id)

    phases_by_id = {p.id: p for p in phases}
    current = phases[0] if phases else None
    visited_ids: set[str] = set()

    while current is not None and current.id not in visited_ids:
        visited_ids.add(current.id)
        if not evaluate_decision_point(current, context):
            break

        for step in current.steps:
            if step.kind != StepKind.INVOCATION:
                continue  # GATE_AUTO/GATE_APPROVAL/COMPENSATION: validated, not dispatched here
            execution, artifact = invoke_skill_step(
                slot=step.slot,
                step_params=step.params,
                orchestration_id=orchestration_id,
                phase_id=current.id,
                step_id=step.id,
                requester_namespace=requester_namespace,
                registry=registry,
                certification_store=certification_store,
            )
            result.executions.append(execution)
            result.artifacts.append(artifact)

        result.completed_phase_ids.append(current.id)
        current = phases_by_id.get(current.next[0]) if current.next else None

    return result
