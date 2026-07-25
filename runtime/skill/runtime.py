"""Skill Architecture §9 — ALGORITMO InvokeSkillStep, implemented as pure
orchestration of already-defined algorithms, exactly as §9 states: "Nenhum
algoritmo novo é necessário... prova de que Skill não exige lógica própria."

Elaboration made explicit, not invented: §9's pseudocode writes a single
generic `skill_ref#template.<kind>` step, but §6.1-6.3 (prose) describes TWO
distinct template roles at two distinct moments — a PROMPT Template expanded
BEFORE the opaque processing (§6.3, becomes its input) and an OUTPUT Template
expanded AFTER it (§6.2, shaped by its result). This module expands §9's
one-line sketch into that already-documented two-moment flow; it does not
add a role Templates don't already have.

"ProcessamentoEfetivoDaSkill" is explicitly opaque to Skill Architecture
(§9: "opaco a este documento — Execution §5, 'Running'"). This module's
default implementation is a clearly-labeled deterministic stand-in, not a
claim of having implemented real Skill cognition — see `_stub_processing`.
"""

from __future__ import annotations

from typing import Any, Callable, Optional

from runtime.composition.resolver import Assembly, SlotError, resolve_slot
from runtime.composition.slot import Slot
from runtime.contracts.identity import VersionedIdentifier
from runtime.execution.model import Artifact, Execution, ExecutionState
from runtime.execution.scheduler import dispatch
from runtime.registry.registry import Registry
from runtime.template.engine import bind_variables, expand, make_template_lookup, resolve_effective_template
from runtime.template.model import TemplateKind, parse_template
from runtime.validation.certification import CertificationStore

ProcessingFn = Callable[[Execution, Optional[dict[str, Any]], dict[str, Any]], Any]


class SkillInvocationError(Exception):
    pass


def _stub_processing(execution: Execution, expanded_prompt: Optional[dict[str, Any]],
                      params: dict[str, Any]) -> Any:
    """Deliberate stand-in for the opaque 'Running' step (Skill §9). Skill
    Architecture does not define what happens inside Running — that's the
    Skill's own business logic (an LLM call, a deterministic function,
    whatever the Skill author wrote). This stub does a small, clearly
    illustrative pattern check so the demo has something concrete to bind
    into the OUTPUT Template, without pretending to be a real analysis
    engine. Callers of invoke_skill_step MAY pass their own `processing_fn`
    to replace this entirely."""
    diff = params.get("diff", "")
    findings = []
    if "sk-live-" in diff or "sk_live_" in diff:
        findings.append({
            "file": "(diff)", "line": 1, "severity": "blocker", "category": "secret",
            "description": "plaintext value matching a live API key pattern",
            "suggestion": "move to environment variable / secret manager; rotate the key",
        })
    return {"findings": findings}


def invoke_skill_step(
    slot: Slot,
    step_params: dict[str, Any],
    orchestration_id: str,
    phase_id: str,
    step_id: str,
    requester_namespace: str,
    registry: Registry,
    certification_store: CertificationStore,
    performed_by: str = "role.system.skill-runtime",
    processing_fn: ProcessingFn = _stub_processing,
) -> tuple[Execution, Artifact]:
    """ALGORITMO InvokeSkillStep(step, ctx, at) — Skill §9, verbatim structure."""

    slot_result = resolve_slot(slot, registry, certification_store, requester_namespace)  # Composition §7
    if isinstance(slot_result, SlotError):
        raise SkillInvocationError(str(slot_result))
    if slot_result is None:  # SKIPPED (optional slot, no candidate)
        raise SkillInvocationError("slot SKIPPED but caller required a result")

    skill_ref: VersionedIdentifier = slot_result
    execution = dispatch(  # Execution §7 — Context, Context Snapshot, Initiated -> Running
        step_id=step_id, phase_id=phase_id, orchestration_id=orchestration_id,
        performed_by=performed_by,
    )

    resolved = registry.resolve(str(skill_ref))
    manifest = resolved.manifest
    assembly = Assembly(resolved_slots={slot.required_capability: skill_ref})
    lookup = make_template_lookup(registry)
    ctx_snapshot = execution.captured_as.captured_context

    expanded_prompt: Optional[dict[str, Any]] = None
    prompt_templates = [t for t in manifest.templates if t["kind"] == TemplateKind.PROMPT.value]
    if prompt_templates:
        prompt_ref = f"{skill_ref}#template.{prompt_templates[0]['local_id']}"
        eff_tpl = resolve_effective_template(prompt_ref, registry, lookup)          # Template §11.1
        bindings = bind_variables(eff_tpl, step_params, ctx_snapshot, assembly)      # Template §11.2
        expanded_prompt = expand(eff_tpl, bindings)                                 # Template §11.3

    try:
        result = processing_fn(execution, expanded_prompt, step_params)             # opaque, §9
    except Exception as exc:  # noqa: BLE001 - failure is a first-class outcome here
        execution.transition(ExecutionState.FAILED, failure_reason=str(exc))
        raise

    output_templates = [t for t in manifest.templates if t["kind"] == TemplateKind.OUTPUT.value]
    if output_templates:
        output_ref = f"{skill_ref}#template.{output_templates[0]['local_id']}"
        eff_out = resolve_effective_template(output_ref, registry, lookup)
        out_params = dict(result) if isinstance(result, dict) else {"result": result}
        out_bindings = bind_variables(eff_out, out_params, ctx_snapshot, assembly)
        expanded_output = expand(eff_out, out_bindings)
        artifact_content = expanded_output["content"]
    else:
        # No OUTPUT Template — Skill relies solely on Kernel Contract's `outputs`
        # (Skill §5: templates[] is optional; Kernel §2.5 already governs shape).
        artifact_content = result

    artifact = Artifact.create(kind="SkillOutput", content=artifact_content,
                                produced_by_execution=execution.instance_id)
    execution.produced_artifacts.append(artifact.instance_id)
    execution.transition(ExecutionState.COMPLETED)                                   # Domain Model §8
    return execution, artifact
