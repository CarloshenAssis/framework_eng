# Reference Cycle 6 — Knowledge e Knowledge Asset

*Companion de `records/knowledge/deployment-rollback-pattern.yaml` e `components/core/playbook.incident-response.deployment-rollback.yaml`.*

---

## 1. A distinção que RFC-DM-001 corrigiu, agora em conteúdo real

RFC-DM-001, achado C1, resolveu uma colisão de nomenclatura: `Knowledge`
(entendimento derivado, Output Entity) e `Knowledge Component` (o que virou
`Knowledge Asset`, um Component que **codifica** Knowledge) compartilhavam
significado ambíguo. A correção introduziu a relação `codifies` (Knowledge
Asset → Knowledge, N:N) para separá-los formalmente. Nenhum conteúdo até
este ciclo havia instanciado essa relação.

```
records/knowledge/deployment-rollback-pattern.yaml         (Knowledge — Output Entity)
        ▲
        │ codifies
        │
components/core/playbook.incident-response.deployment-rollback.yaml   (Knowledge Asset/Playbook — Component)
```

---

## 2. `derives_from` — reaplicação da regra de RFC-DM-001 §3.3

O `Knowledge` deste ciclo deriva de **duas Executions**, ambas do episódio de
falha/compensação do Ciclo 5:

```
derives_from:
  - Execution de step.deploy (3ª tentativa, Failed)
  - Execution de step.revert-deployment-record (Compensation, Completed)
```

Isso satisfaz as duas restrições já mandatadas por RFC-DM-001 §3.3, sem
mecanismo novo:

- **Temporal monotonicidade**: `established_at` do Knowledge (18:00Z) é
  posterior às duas Executions que o originaram (necessariamente anteriores,
  já que o episódio do Ciclo 5 é hipoteticamente concluído antes desta
  observação ser formulada).
- **Aciclicidade**: o grafo `derives_from` sobre `{Execution, Research,
  Decision, Knowledge}` é verificado por `Kernel§7.CycleDetection` — mesma
  aplicação já reutilizada seis vezes ao longo da série de documentos de
  arquitetura, agora pela primeira vez sobre dado real.

---

## 3. Por que o Playbook não é "mais um Standard"

| | Standard | Playbook (Knowledge Asset) |
|---|---|---|
| Natureza | Normativo — o que **deve** ser verdade no futuro | Descritivo — o que **foi observado** no passado |
| Origem | Autorado deliberadamente por um Steward | **Derivado** de Execution real via Knowledge — nunca criado diretamente (Domain Model §11) |
| Consumido por | Policy (`bindings`), Certification (`Conformance Claim`) | Consulta humana ou de Agent — nenhum mecanismo de enforcement |
| Este ciclo prova | — | Que o caminho Execution → Knowledge → Knowledge Asset funciona sem exigir um único conceito além dos já ratificados |

Isso é a mesma distinção já estabelecida entre Standard (Standards §1.1: "o
que significa estar conforme") e Knowledge (Domain Model §11: "entendimento
acumulado... nunca é criada diretamente — é sempre derivada"), agora
observável em dois arquivos que não podem ser confundidos um com o outro.

---

## 4. Proveniência sem mecanismo novo

```
Observability.provenance(core/playbook.incident-response.deployment-rollback@1.0.0)
  → WalkForward por `codifies` → Knowledge (deployment-rollback-pattern)
  → WalkBack por `derives_from` → as duas Executions do Ciclo 5
  → responde as 5 perguntas de Domain Model §15 integralmente,
    exatamente como Observability §9.2 já formalizava antes de qualquer
    Playbook existir
```

**Nenhum mecanismo além dos já ratificados foi necessário.** Este é o sexto
ciclo consecutivo em que isso se verifica.
