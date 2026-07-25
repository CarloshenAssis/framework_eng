# Reference Cycle 3 — Certificação Ponta a Ponta

*Companion de `records/certification/core.skill.static-analysis.code-review.yaml`.*

---

## A lacuna que este ciclo fecha

Os dois Workflows já publicados exigem certificação sem que nada no repositório
mostrasse **como uma Skill chega lá**:

```
core/workflow.pull-request-review@1.0.0
  → step.run-code-review.slot.min_certification_level = L2

org.acme-corp/workflow.pull-request-review-strict@1.0.0
  → phase.human-only-gate.step.slot.min_certification_level = L4
```

`records/certification/core.skill.static-analysis.code-review.yaml` mostra a
cadeia real: L1 (automática) → L2 (Testing) → L3 (Standards) → L4 (Certifier
humano) — cada nível usando exatamente a Evidence que Validation &
Certification §5 já exigia, sem nenhuma invenção de critério.

---

## Como o Registry lê isto sem armazenar nada

```
Registry.resolve(core/skill.static-analysis.code-review@1.0.0)
  → RegistryEntry{
       coordinate, lifecycle_state: Active,
       certification_status: <read-through — Registry §12>
    }

certification_status é computado, não armazenado:
  = a Decision Record de subtype=CertificationGrant mais recente,
    não superada, para este subject
  = { level: L4, valid_until: "2026-10-25T15:00:00Z", ... }   ← lido do arquivo acima
```

**Nenhum campo é adicionado ao Manifest da Skill** — consistente com a regra já
estabelecida (Registry & Discovery §12; Validation & Certification §3): o
Registry nunca é dono do dado de certificação, apenas o reflete.

---

## Consequência prática nos dois Workflows

```
core/workflow.pull-request-review@1.0.0, step.run-code-review:
  min_certification_level = L2
  Skill atual: L4  →  L4 ≥ L2  →  ELEGÍVEL (Composition §7, ResolveSlot)

org.acme-corp/workflow...strict, phase.human-only-gate, step.human-decision:
  min_certification_level = L4
  candidato = core/agent.code-reviewer@1.0.0 — AINDA SEM registro de
  certificação neste repositório
  →  SlotUnsatisfied (Composition §9) até que um ciclo de certificação
     equivalente seja produzido para o Agent — próximo item natural de conteúdo
```

Este é um resultado **correto**, não um defeito: o Framework recusa
explicitamente permitir que o gate humano-obrigatório resolva para um Provider
sem prova de nível suficiente — exatamente o comportamento que Composition §9
(`SlotUnsatisfied`) e Standards §14 (nunca conformidade trivial por ausência de
prova) foram desenhados para garantir.

---

## Verificação de janelas de validade (Governance §14, rigor proporcional)

| Nível | `valid_until` | Duração da janela |
|---|---|---|
| L1 | `null` (perpétua) | — |
| L2 | 6 meses | risco médio |
| L3 | 4 meses | domínio de segurança — mais curta que L2 |
| L4 | 3 meses | nível mais alto — janela mais curta de todas |

Ordem estritamente decrescente de janela conforme o nível sobe — consistente
com a regra já estabelecida de que rigor cresce com consequência, nunca o
contrário.
