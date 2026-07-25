# Reference Cycle 4 — Correção de Nomenclatura, Certificação do Agent, Fechamento do Gate

*Companion de `records/certification/core.agent.code-reviewer.yaml` e `records/role-assignment/reviewer.yaml`.*

---

## 1. Correção registrada (não silenciosa)

`org.acme-corp/workflow.pull-request-review-strict.yaml` chamava uma fase de
`phase.human-only-gate`. Isso era **factualmente incorreto**: Composition
Slot (`required_capability`, `min_certification_level`, `cardinality`) não
tem campo `occupant_kind` — nada impede estruturalmente um Agent de resolver
aquele Slot. Renomeado para `phase.high-risk-gate`, com nota explicando que a
garantia real é **AG4** (coautorização humana obrigatória na própria
`Decision`, independente de quem a ocupa), não exclusão de Agent.

Isso é o mesmo padrão de correção já usado nos documentos de arquitetura
(nunca reescrever silenciosamente — registrar o quê, por quê, e a partir de
quando) aplicado agora ao conteúdo, não só à especificação.

---

## 2. RoleAssignment ↔ Certificação: dois requisitos independentes

Formalizei `records/role-assignment/reviewer.yaml`, que até este ciclo
existia só em prosa. Ao formalizar, um erro apareceu: `GrantRoleAssignment`
(Agent §9) verifica `Certification.current_level ≥ MinimumLevelFor(risk_tier)`
**antes** de conceder — a versão anterior (só narrativa) dizia "certificação
pendente", o que teria sido uma concessão inválida. Corrigido:

```
09:00Z — Agent atinge L2 (records/certification/core.agent.code-reviewer.yaml)
09:30Z — RoleAssignment concedida (L2 ≥ MinimumLevelFor(MEDIO)=L2 — AG2 satisfeita)
13:00Z — Agent atinge L3
16:00Z — Agent atinge L4
```

A tabela `minimum_level_by_risk_tier` (BAIXO→L1, MEDIO→L2, ALTO→L4) fica
registrada no arquivo — é a primeira instanciação concreta de algo que os
documentos de arquitetura deixaram como parâmetro aberto.

---

## 3. Por que a certificação do Agent não é simétrica à da Skill

| | Skill (Ciclo 3) | Agent (este ciclo) |
|---|---|---|
| L2 — Evidence | `test_suite[]` inteiramente `FUNCTIONAL`, todos determinísticos | 1 caso `FUNCTIONAL` + 1 caso `BEHAVIORAL/HUMAN_REVIEW` — o segundo fica `PENDING_HUMAN_REVIEW` e **não bloqueia** L2 porque a cobertura de NR `MUST`/`MUST_NOT` já estava satisfeita pelo caso determinístico (TS9) |
| L4 — Reprodutibilidade | Expansão de Template determinística = suficiente | Mesma prova, mas com nota explícita: a **expansão** é determinística; o **raciocínio** do Agent não precisa ser, e não é — distinção que Template §7 já estabelecia, agora aplicada literalmente a um caso onde a diferença importa |
| L4 — Fecha o quê | Nenhuma pendência anterior | Fecha `test.ambiguous-severity-mix`, que ficou `PENDING_HUMAN_REVIEW` desde L2 — outcome atualizado para `PASS` só quando o humano efetivamente revisou |

---

## 4. O gate agora resolve

```
Composition.ResolveSlot(phase.high-risk-gate.step.high-risk-decision.slot):
  required_capability = role-eligibility.reviewer
  min_certification_level = L4
  candidatos = Registry.search(capability=role-eligibility.reviewer)
             = [core/agent.code-reviewer@1.0.0]
  Certification.level(core/agent.code-reviewer@1.0.0) em t > 16:00Z = L4
  L4 ≥ L4  →  RESOLVIDO (antes: SlotUnsatisfied, Ciclo 3)

  Ao ser efetivamente invocado neste gate:
  ClassifyAgentOutput (Agent §9):
    ResolveCurrentOccupant(reviewer, at=ctx.timestamp) = core/agent.code-reviewer  [RoleAssignment vigente]
    RequiresCoAuthorization(risk_tier=MEDIO) = true
    co_authorized_by já presente na RoleAssignment (role.governance-area.code-quality.human-lead)
    → resultado ⟹ Decision, produz Decision Record
```

O que o Ciclo 3 sinalizou como "próximo item natural" está fechado. **Nenhum
mecanismo além dos já ratificados foi necessário** — o único trabalho real
foi produzir a Evidence e corrigir uma inconsistência de nomenclatura que a
formalização (não a arquitetura) expôs.
