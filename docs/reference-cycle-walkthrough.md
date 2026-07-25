# Reference Cycle — Prova de Funcionamento

*Companion de `components/core/` — mostra a cadeia institucional completa se executando sobre os cinco artefatos do ciclo de referência.*

---

## 1. Pré-condição: RoleAssignment

Antes de o Workflow poder produzir uma `Decision` real (não apenas um Artifact opinativo), `core/agent.code-reviewer@1.0.0` precisa ocupar o `RoleClass=Reviewer` — via `RoleAssignment` (Agent Architecture §4.2, família nomeada de `Decision`).

```yaml
# Decision Record ilustrativo — produzido por GrantRoleAssignment (Agent §9)
decision_record:
  subtype: ROLE_ASSIGNMENT_GRANT
  role_class: reviewer
  occupant: core/agent.code-reviewer@1.0.0
  effective_from: "2026-07-25T00:00:00Z"
  expires_at: "2027-01-25T00:00:00Z"
  authorized_by: role.governance-area.code-quality.steward   # humano — risk_tier=BAIXO não exigiria,
                                                                # mas Reviewer já é tratado como MÉDIO por precaução
  co_authorized_by: role.governance-area.code-quality.human-lead   # AG4 — coautorização humana
```

**Verificação AG1** (Agent §9): `core/agent.code-reviewer` declara `role-eligibility.reviewer` em `capabilities[]` — condição satisfeita.
**Verificação AG2**: nível de Certificação do Agent (assumido L2 neste exemplo) ≥ mínimo exigido para `risk_tier=MÉDIO` — satisfeita.
**Verificação AG5**: o Agent não é `owner` de nenhum Component sendo revisado — satisfeita.

---

## 2. Disparo do Workflow

```
Entrada: pull_request_diff = "<diff real de um PR>"
```

### Fase 1 — `phase.static-review`

```
Composition.ResolveSlot(capability=static-analysis.code-review, min_L2)
  → candidatos: [core/skill.static-analysis.code-review@1.0.0]
  → Registry.search + Certification.filter(≥L2)          [Registry §6.2; Composition §7]
  → resolvido: core/skill.static-analysis.code-review@1.0.0

Execution.Dispatch(step.run-code-review)
  → Context{ orchestration_id: wf-01J..., phase_id: phase.static-review,
              step_id: step.run-code-review, attempt: 0 }
  → Context Snapshot capturado                              [RFC-DM-001 §3.2]

  → Policy check (BLOCKING, applies_at=EXECUTION):
      core/policy.code-quality.mandatory-review@1.0.0 aplicável
      (scope.capabilities=[static-analysis.code-review] ∩ Skill.capabilities ≠ ∅)
      → Effective Policy Set inclui binding a
        core/standard.code-quality.review-baseline@1.0.0 (BASE, STRICT)
      → dispatch só prossegue se Certificação atual satisfizer BASE STRICT

  → Template.ResolveEffectiveTemplate("...code-review@1.0.0#template.prompt.main")
  → Template.BindVariables(diff=pull_request_diff, language="auto-detect")
  → Template.Expand(...) → ExpandedTemplate (Artifact)
  → processamento efetivo (opaco) → findings[]
  → Template.Expand(output.review_report, {findings, generated_at=ctx.timestamp})
  → Artifact "review_report" produzido
  → Execution → Completed
```

### Fase 2 — `phase.decision-gate`

```
Composition.ResolveSlot(capability=role-eligibility.reviewer, min_L2)
  → resolvido: core/agent.code-reviewer@1.0.0

Execution.Dispatch(step.reviewer-decision)
  → Context{ orchestration_id: wf-01J... (MESMO da fase 1), phase_id: phase.decision-gate, ... }
  → Template.Expand(prompt.decision, {review_report}) → prompt renderizado
  → processamento efetivo (opaco) → verdict="APPROVE" | "REQUEST_CHANGES", rationale

  → ClassifyAgentOutput(execution, resultado)               [Agent §9]
      ResolveCurrentOccupant(role_class=reviewer, at=ctx.timestamp)
        → RoleAssignment de §1 está vigente nesse instante
      IsGovernanceClassifiedAction(resultado) = true (GATE_APPROVAL é ação de Governance §8)
      RequiresCoAuthorization(risk_tier=MÉDIO) = true, co_authorized_by já presente na
        RoleAssignment original — condição satisfeita
      → resultado ⟹ Decision, produz Decision Record
        { subtype: WORKFLOW_GATE_APPROVAL, verdict: "APPROVE",
          authorized_by: core/agent.code-reviewer (via RoleAssignment), ... }

  → Template.Expand(output.decision, {verdict, rationale, decided_at=ctx.timestamp})
  → Artifact "final_decision" produzido
  → Execution → Completed
```

---

## 3. O que fica observável depois

```
Observability.trace("wf-01J...")
  → Trace{ spans: [step.run-code-review, step.reviewer-decision], complete: true }

Observability.provenance(final_decision_artifact_id)
  → ProvenanceChain{
      origin: Execution de step.reviewer-decision,
      context: Context Snapshot daquela Execution,
      responsible: Role "reviewer", ocupado por core/agent.code-reviewer no instante T,
      against: core/agent.code-reviewer@1.0.0,
      affects: [core/policy.code-quality.mandatory-review@1.0.0 (referenciada via Compliance futura)]
    }
```

**As cinco perguntas de Domain Model §15 são respondíveis integralmente** — nenhuma delas exigiu mecanismo além do já ratificado.

---

## 4. O que este ciclo prova

| Camada | Provada por |
|---|---|
| Kernel (Contract, Lifecycle) | Todo Manifest usa exatamente os 15 campos + `templates[]`/`test_suite[]`/`phases[]` já normatizados |
| Identity & Registry | `Coordinate`s resolvidos, `search(capability)` usado duas vezes sem ambiguidade |
| Composition | Dois Slots resolvidos por capability + certificação mínima |
| Template | Prompt e Output expandidos deterministicamente, variável `CONTEXT` nunca lida "ao vivo" |
| Standards + Policy | Um NR `MUST_NOT` bloqueante realmente condiciona o dispatch |
| Agent + Governance | `RoleAssignment` real gate a produção de `Decision`; AG3/AG4/AG5 todas exercidas |
| Workflow + Execution | Duas Phases, uma `GATE_APPROVAL`, correlação por `orchestration_id` |
| Observability | `trace()`/`provenance()` reconstroem o ciclo inteiro sem nenhuma escrita nova |

**Nenhuma linha deste ciclo exigiu um mecanismo que os 20 documentos de arquitetura não já continham.**
