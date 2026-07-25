"""Execution Architecture §7 — ALGORITMO Plan, Dispatch, Recover, Rollback,
implemented against docs/architecture/11-execution-architecture.md §7
verbatim. The Scheduler is a substrate service (§4), not a Component."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Optional

from runtime.contracts.graph import detect_cycle, topological_sort
from runtime.execution.model import (
    Context,
    ContextSnapshot,
    Execution,
    ExecutionState,
    capture_context_snapshot,
)


class SchedulerError(Exception):
    pass


@dataclass
class PlannedStep:
    """One node of an Execution Plan — the minimal shape Plan()/Dispatch()
    need; Workflow's own Step (workflow/model.py) carries the rest (slot,
    kind, failure_policy) and is adapted into this by workflow/engine.py."""

    step_id: str
    phase_id: str
    depends_on: list[str] = field(default_factory=list)


@dataclass
class ExecutionPlan:
    """§4 — Execution Plan: "Novo construto interno, modelado como Artifact
    genérico, produzido pela Execution-pai antes de transicionar a Running."""

    orchestration_id: str
    ordered_step_ids: list[str]
    steps_by_id: dict[str, PlannedStep]


def plan(orchestration_id: str, steps: list[PlannedStep]) -> ExecutionPlan:
    """ALGORITMO Plan(orchestration_definition) — §7."""
    graph = {s.step_id: list(s.depends_on) for s in steps}
    cycle = detect_cycle(graph)  # "já validado em Doc 2, revalidado defensivamente"
    if cycle:
        raise SchedulerError(f"cyclic step graph: {' -> '.join(cycle)}")
    order = topological_sort(graph)
    return ExecutionPlan(
        orchestration_id=orchestration_id,
        ordered_step_ids=order,
        steps_by_id={s.step_id: s for s in steps},
    )


def ready_steps(plan_: ExecutionPlan, completed_step_ids: set[str]) -> list[str]:
    """§6.2 — "ready = steps com deps satisfeitas". EX3: steps without a
    topological dependency edge between them MUST dispatch in parallel by
    default; this runtime executes them concurrently-in-spirit by returning
    all ready steps at once rather than one at a time."""
    ready = []
    for step_id in plan_.ordered_step_ids:
        if step_id in completed_step_ids:
            continue
        step = plan_.steps_by_id[step_id]
        if all(dep in completed_step_ids for dep in step.depends_on):
            ready.append(step_id)
    return ready


def dispatch(
    step_id: str,
    phase_id: str,
    orchestration_id: str,
    performed_by: str,
    attempt: int = 0,
) -> Execution:
    """ALGORITMO Dispatch(step, orchestration_id, attempt) — §7, verbatim:
    Context -> Context Snapshot (mandatory, RFC-DM-001 C2) -> Initiated ->
    Running. EX2: Running MUST have a preceding Context Snapshot — enforced
    here by construction, not by a separate check, since Execution.__init__
    requires captured_as."""
    ctx = Context(orchestration_id=orchestration_id, phase_id=phase_id, step_id=step_id, attempt=attempt)
    snapshot = capture_context_snapshot(ctx)
    execution = Execution(
        instance_id=_new_execution_id(),
        performed_by=performed_by,
        occurs_within=ctx,
        captured_as=snapshot,
    )
    execution.transition(ExecutionState.RUNNING)
    return execution


def _new_execution_id() -> str:
    from runtime.contracts.identity import new_instance_identifier
    return new_instance_identifier()


def recover(plan_: ExecutionPlan, completed_step_ids: set[str],
            dispatch_fn: Callable[[str], Execution]) -> list[Execution]:
    """ALGORITMO Recover(orchestration_id) — §7: checkpoint = reuse of what's
    already Completed (EX4); never re-executes a Completed step."""
    pending = [s for s in plan_.ordered_step_ids if s not in completed_step_ids]
    to_dispatch = ready_steps(plan_, completed_step_ids)
    to_dispatch = [s for s in to_dispatch if s in pending]
    return [dispatch_fn(step_id) for step_id in to_dispatch]


def rollback(completed_phase_steps_reversed: list[PlannedStep],
             compensated_by: dict[str, str],
             dispatch_fn: Callable[[str], Execution]) -> list[Execution]:
    """ALGORITMO Rollback(orchestration_id, failed_phase) — §7: for each
    completed phase before the failed one, in reverse order, dispatch the
    compensation Step of any Step that declares one. Always a NEW Execution
    (EX1) — never reopens the original."""
    dispatched = []
    for step in completed_phase_steps_reversed:
        compensation_step_id = compensated_by.get(step.step_id)
        if compensation_step_id is not None:
            dispatched.append(dispatch_fn(compensation_step_id))
    return dispatched
