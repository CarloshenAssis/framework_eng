"""Not the required demo — a small supplementary check that the negative
paths (named errors, invariants) actually hold, not just the happy path.
Run: python3 -m runtime.demo.check_error_paths
"""

from __future__ import annotations

from pathlib import Path

from runtime.composition.resolver import SlotError, resolve_slot
from runtime.composition.slot import Slot
from runtime.execution.model import Execution, ExecutionError, ExecutionState
from runtime.execution.scheduler import dispatch
from runtime.registry.loader import load_manifest
from runtime.registry.registry import Registry, Unauthorized
from runtime.validation.certification import CertificationLevel, CertificationStore

REPO_ROOT = Path(__file__).resolve().parents[2]


def check(label: str, condition: bool) -> None:
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {label}")
    if not condition:
        raise SystemExit(1)


def main() -> None:
    manifest = load_manifest(REPO_ROOT / "components/core/skill.static-analysis.code-review.yaml")
    registry = Registry()

    # 1) R1 / Unauthorized — register() without decision_record_ref
    try:
        registry.register(manifest, decision_record_ref="")
        check("register() rejects empty decision_record_ref (Registry §5, R1)", False)
    except Unauthorized:
        check("register() rejects empty decision_record_ref (Registry §5, R1)", True)

    registry.register(manifest, decision_record_ref="demo-decision-record-001")
    versioned = manifest.versioned_identifier()
    digest = registry.digest_of(versioned)

    # 2) Composition §7 — SlotError when min_certification_level is not met
    certification_store = CertificationStore()
    certification_store.grant(versioned, CertificationLevel.L1, digest,
                               "role.governance-area.code-quality.reviewer", "2026-07-25T10:00:00Z")
    slot = Slot(required_capability="static-analysis.code-review", version_range=">=1.0.0",
                min_certification_level=CertificationLevel.L2)
    result = resolve_slot(slot, registry, certification_store, requester_namespace="core")
    check("ResolveSlot returns SlotError when candidate is below min_certification_level (Composition §7)",
          isinstance(result, SlotError))

    # 3) Composition §9 — optional Slot with no candidate is SKIPPED, not an error
    optional_slot = Slot(required_capability="nonexistent.capability", version_range="*", optional=True)
    skipped = resolve_slot(optional_slot, registry, certification_store, requester_namespace="core")
    from runtime.composition.resolver import SKIPPED
    check("optional Slot with no candidate returns SKIPPED, not SlotError (Composition CP5)",
          skipped is SKIPPED)

    # 4) Execution §12 EX1 — MUST NOT reopen a terminal Execution
    execution = dispatch(step_id="s1", phase_id="p1", orchestration_id="o1", performed_by="role.system.test")
    execution.transition(ExecutionState.COMPLETED)
    try:
        execution.transition(ExecutionState.RUNNING)
        check("Execution MUST NOT be reopened once terminal (EX1)", False)
    except ExecutionError:
        check("Execution MUST NOT be reopened once terminal (EX1)", True)

    # 5) Execution §12 EX2 — Running always has a preceding Context Snapshot (by construction)
    check("every dispatched Execution carries a Context Snapshot before Running (EX2)",
          execution.captured_as is not None and execution.captured_as.instance_id)

    print("\nTodos os caminhos negativos verificados.")


if __name__ == "__main__":
    main()
