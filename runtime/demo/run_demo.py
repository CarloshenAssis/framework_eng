"""End-to-end demonstration required by the task:

    Skill -> Template -> Workflow -> Slot -> Execution -> Artifact -> Evidence

Loads the REAL institutional Manifest already committed at
components/core/skill.static-analysis.code-review.yaml (Reference Cycle 1,
certified L1-L4 in Reference Cycle 3) — nothing here is fabricated demo
data at the Skill level. A minimal single-Phase, single-Step Workflow is
constructed fresh (the pilot's own Workflows all involve an Agent decision
gate, which is explicitly out of scope for this Runtime), requiring exactly
the capability that Skill already declares.

Run: python3 -m runtime.demo.run_demo   (from the repo root)
"""

from __future__ import annotations

import json
from pathlib import Path

from runtime.composition.slot import Cardinality, Slot
from runtime.contracts.identity import VersionedIdentifier
from runtime.execution.model import Evidence
from runtime.registry.loader import load_manifest
from runtime.registry.registry import Registry, manifest_digest as compute_manifest_digest
from runtime.skill.runtime import invoke_skill_step
from runtime.registry.discovery import search as discovery_search
from runtime.validation.certification import CertificationLevel, CertificationStore
from runtime.workflow.model import FailurePolicy, OnFailure, Phase, Step, StepKind
from runtime.workflow.engine import run_workflow

REPO_ROOT = Path(__file__).resolve().parents[2]


def line(title: str) -> None:
    print(f"\n{'─' * 8} {title} {'─' * max(0, 60 - len(title))}")


def main() -> None:
    print("=" * 70)
    print("Framework Eng — Runtime mínimo — demonstração ponta a ponta")
    print("=" * 70)

    # ── 1. Registry: carregar e registrar o Manifest real da Skill ──────────
    line("1. Registry — load, register, digest, structural validation")
    skill_path = REPO_ROOT / "components/core/skill.static-analysis.code-review.yaml"
    manifest = load_manifest(skill_path)
    print(f"Manifest carregado de: {skill_path.relative_to(REPO_ROOT)}")
    print(f"  identity            = {manifest.identity}")
    print(f"  component_type      = {manifest.component_type.value}")
    print(f"  capabilities        = {manifest.capabilities}")
    print(f"  templates[].kind    = {[t['kind'] for t in manifest.templates]}")

    certification_store = CertificationStore()
    versioned = manifest.versioned_identifier()

    def cert_lookup_int(vid: VersionedIdentifier) -> int:
        try:
            digest = registry.digest_of(vid)
        except Exception:
            return 0
        return certification_store.current_level_as_int(vid, digest)

    registry = Registry(certification_lookup=cert_lookup_int)
    entry = registry.register(
        manifest,
        decision_record_ref="demo-decision-record-001 (Governance Admission — out of this Runtime's scope; "
                             "register() still enforces the precondition, ref is not fabricated silently)",
    )
    digest = registry.digest_of(versioned)
    recomputed = compute_manifest_digest(manifest)
    assert digest == recomputed, "manifest_digest MUST be deterministic"
    print(f"  manifest_digest     = {digest}")
    print(f"  lifecycle_state     = {entry.lifecycle_state.value}")

    # A second, real Standard is also registered — proves the Registry indexes
    # more than one component_type, even though Composition (below) never
    # queries it directly (Composition §3 — Standards/Policy are out of its
    # algorithm, folded into Certification level instead; see composition/resolver.py docstring).
    standard_path = REPO_ROOT / "components/core/standard.code-quality.review-baseline.yaml"
    standard_manifest = load_manifest(standard_path)
    registry.register(standard_manifest, decision_record_ref="demo-decision-record-002")
    print(f"Também registrado (não consultado pela Composition — ver nota no código): "
          f"{standard_manifest.identity}")

    # ── 2. Validation & Certification (minimal) — grant L2 ──────────────────
    line("2. Certification — minimal grant, real digest (not the illustrative placeholder)")
    certification_store.grant(
        versioned, CertificationLevel.L2, manifest_digest=digest,
        certifier_role_id="role.governance-area.code-quality.reviewer",
        granted_at="2026-07-25T11:30:00Z",
    )
    print(f"Certification concedida: {versioned} -> "
          f"{certification_store.current_level(versioned, digest).name}")

    # ── 3. Discovery — search(capability) ────────────────────────────────────
    line("3. Discovery — search(capability)")
    candidates = discovery_search(registry, "static-analysis.code-review")
    print(f"search('static-analysis.code-review') -> {[str(c) for c in candidates]}")

    # ── 4. Workflow: uma Phase, um Step, um Slot ─────────────────────────────
    line("4. Workflow — uma Phase, um Step, um Slot (min_certification_level=L2)")
    slot = Slot(
        required_capability="static-analysis.code-review",
        version_range=">=1.0.0",
        min_certification_level=CertificationLevel.L2,
        cardinality=Cardinality.EXACTLY_ONE,
    )
    step = Step(
        id="step.run-code-review",
        slot=slot,
        kind=StepKind.INVOCATION,
        failure_policy=FailurePolicy(on_failure=OnFailure.ABORT),
        params={
            "diff": "const apiKey = 'sk-live-abc123456789';",  # same sample as the Skill's own test_suite
            "language": "javascript",
        },
    )
    phase = Phase(id="phase.static-review", steps=[step], next=[])
    print(f"Phase({phase.id}) -> Step({step.id}, kind={step.kind.value}) -> "
          f"Slot(capability={slot.required_capability!r}, min_level={slot.min_certification_level.name})")

    # ── 5. Execução ponta a ponta: Composition -> Execution -> Template -> Skill -> Artifact ─
    line("5. run_workflow — Composition.ResolveSlot + Execution.Dispatch + Template + Skill")
    result = run_workflow(
        phases=[phase],
        registry=registry,
        certification_store=certification_store,
        orchestration_id="demo-orchestration-0001",
        requester_namespace="core",
    )

    execution = result.executions[0]
    artifact = result.artifacts[0]

    print(f"Composition.ResolveSlot -> resolveu para: {versioned}  (único candidato certificado L2)")
    print(f"Execution.instance_id   = {execution.instance_id}")
    print(f"Execution.state         = {execution.state.value}")
    print(f"Execution.transitions (Timeline intrínseca desta Execution):")
    for state, ts in execution.transitions:
        print(f"    {ts}  {state}")
    print(f"Context Snapshot (RFC-DM-001 C2, capturado antes de Running):")
    print(f"    {json.dumps(execution.captured_as.captured_context, indent=4, ensure_ascii=False)}")

    line("Artifact produzido (OUTPUT Template expandido)")
    print(json.dumps(artifact.content, indent=2, ensure_ascii=False) if isinstance(artifact.content, (dict, list))
          else artifact.content)

    # ── 6. Evidence ───────────────────────────────────────────────────────────
    line("6. Evidence — verificação estrutural mínima (não é o pipeline de Testing Architecture)")
    findings = json.loads(artifact.content)["findings"] if isinstance(artifact.content, str) else artifact.content.get("findings", [])
    has_secret_finding = any(f.get("category") == "secret" and f.get("severity") == "blocker" for f in findings)
    evidence = Evidence.create(
        evidence_kind="STRUCTURAL",
        description=(
            "Artifact produzido contém 'findings' e 'generated_at' conforme outputs declarados "
            "pela Skill (Kernel §2.5), e o achado de segredo esperado (mesmo caso do test_suite "
            "institucional da própria Skill) foi detectado."
        ),
        result="PASS" if has_secret_finding else "FAIL",
        reproducible=True,
        subject_execution=execution.instance_id,
    )
    print(f"Evidence.evidence_kind  = {evidence.evidence_kind}")
    print(f"Evidence.result         = {evidence.result}")
    print(f"Evidence.description    = {evidence.description}")

    # ── 7. Skill Runtime SEM Templates (o outro ramo explicitamente pedido) ──
    line("7. Skill Runtime — o outro ramo: uma Skill SEM templates[] (Skill §5, ESCOLHA DE DESIGN)")
    audit_manifest = load_manifest(REPO_ROOT / "components/core/skill.security.dependency-audit.yaml")
    print(f"Manifest carregado: {audit_manifest.identity}  (templates[] = {audit_manifest.templates!r} — vazio)")
    registry.register(audit_manifest, decision_record_ref="demo-decision-record-003")
    audit_versioned = audit_manifest.versioned_identifier()
    audit_digest = registry.digest_of(audit_versioned)
    certification_store.grant(audit_versioned, CertificationLevel.L1, audit_digest,
                               "role.governance-area.code-quality.reviewer", "2026-07-25T10:00:00Z")

    def audit_processing(execution, expanded_prompt, params):
        # No PROMPT Template exists for this Skill, so expanded_prompt is None here —
        # exactly the "sem Templates" branch (Skill §5's ESCOLHA DE DESIGN).
        assert expanded_prompt is None
        manifest_text = params.get("dependency_manifest", "")
        vulnerable = [line_ for line_ in manifest_text.splitlines() if "event-stream@3.3.6" in line_]
        return {"audit_report": {"vulnerabilities": [
            {"package": "event-stream", "version": "3.3.6", "severity": "critical"}
        ] if vulnerable else []}}

    audit_slot = Slot(required_capability="security.dependency-audit", version_range=">=1.0.0",
                       min_certification_level=CertificationLevel.L1)
    audit_execution, audit_artifact = invoke_skill_step(
        slot=audit_slot,
        step_params={"dependency_manifest": "left-pad@1.0.0\nevent-stream@3.3.6"},
        orchestration_id="demo-orchestration-0002",
        phase_id="phase.dependency-audit",
        step_id="step.run-dependency-audit",
        requester_namespace="core",
        registry=registry,
        certification_store=certification_store,
        processing_fn=audit_processing,
    )
    print(f"Execution.state         = {audit_execution.state.value}  (sem nenhuma expansão de Template)")
    print(f"Artifact.content        = {audit_artifact.content}")

    print("\n" + "=" * 70)
    print("Cadeia completa executada: Skill -> Template -> Workflow -> Slot -> "
          "Execution -> Artifact -> Evidence")
    print("=" * 70)


if __name__ == "__main__":
    main()
