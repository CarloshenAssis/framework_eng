# Reference Cycle 5 — Paralelismo, Join Implícito, Retry e Compensação (Saga)

*Companion de `components/core/workflow.release-readiness.yaml`.*

---

## 1. O que os quatro ciclos anteriores nunca tocaram

| Mecanismo | Onde está definido | Exercitado antes deste ciclo? |
|---|---|---|
| Steps paralelos (sem precedência declarada) | Execution §10, regra EX3 | Não |
| Join implícito na fronteira de Phase | Execution §9 (`BuildTrace`) | Não |
| `Skill` sem `templates[]` | Skill §5, ESCOLHA DE DESIGN | Não |
| `RETRY(n)` | Domain Model §8 ("nova tentativa = nova Execution"); Workflow §4 | Não |
| `Compensation` / Saga | Workflow §4; Execution §9, algoritmo `Rollback` | Não |

---

## 2. Despacho paralelo — sem campo novo

```
Scheduler chega a phase.parallel-checks
  → dois Steps declarados, NENHUMA aresta de precedência entre eles
  → EX3 (Execution §10): "Steps sem dependência topológica MUST despachar em paralelo"
  → step.run-code-review  → Execution#A, Context{ orchestration_id, phase_id, step_id: run-code-review }
  → step.run-dependency-audit → Execution#B, Context{ MESMO orchestration_id, step_id: run-dependency-audit }
  → A e B executam concorrentemente, cada uma com seu próprio Context Snapshot imutável
```

O paralelismo não é uma propriedade que se **declara** — é a ausência de uma
propriedade (dependência) que já bastava para o Scheduler decidir despachar
concorrentemente. Nenhum campo `parallel: true` existe em nenhum documento de
arquitetura, e nenhum foi adicionado aqui.

## 3. Join — a fronteira de Phase já era o Join

```
phase.readiness-gate.steps = []   (Decision Point puro, Workflow §6.3 do Ciclo 2)
  → Scheduler só avalia os `condition` de `next` quando TODOS os Steps de
    phase.parallel-checks estão em estado terminal (Completed | Failed | Aborted)
  → isso É a semântica de Join — nenhuma Phase "join.aggregate" vazia e
    redundante foi necessária
```

**Nota deliberada sobre `step.run-dependency-audit.min_certification_level=L1`:**
`core/skill.security.dependency-audit` ainda não tem registro em
`records/certification/` além da L1 automática — diferente da Skill de
revisão de código, que chegou a L4 no Ciclo 3. Isso é **intencional**: mostra
que Workflows distintos podem exigir níveis de rigor distintos por Slot,
proporcionalmente ao risco de cada capacidade — exatamente o princípio
constitucional de fricção proporcional, sem exigir que toda Skill do
repositório atinja o nível mais alto antes de ser utilizável em algum lugar.

---

## 4. Retry e Compensação — o caminho de falha completo

```
step.deploy despachado → Execution#1 → Failed
  failure_policy.on_failure = RETRY, retry_count = 2
  → Execution#2 (nova Execution — Domain Model §8, nunca reabertura da #1) → Failed
  → Execution#3 → Failed
  → 3 tentativas esgotadas, Step definitivamente Failed

Execution Architecture §9, ALGORITMO Rollback(orchestration_id, failed_phase=phase.deploy):
  FOR phase IN completed_phases_before(phase.deploy) REVERSED:
     # única phase completada antes: phase.create-record
     FOR step IN phase.create-record.steps WHERE step.compensated_by IS NOT NULL:
        # step.create-deployment-record.compensated_by = step.revert-deployment-record
        Dispatch(step.revert-deployment-record, orchestration_id, attempt=0)
           → NOVA Execution#4, kind=COMPENSATION
           → Context{ MESMO orchestration_id, phase_id: phase.revert }
           → failure_policy.on_failure=ABORT (WF4 — obrigatório para Compensation)
```

**Nenhuma das quatro Executions de `step.deploy` (#1, #2, #3) é reaberta ou
editada** — cada tentativa é um evento imutável e independente, exatamente
como Domain Model §8 e a regra EX1 (Execution §12) já exigiam antes de
qualquer conteúdo real existir. A Compensação (#4) também é uma Execution
nova, nunca uma "correção" das anteriores.

---

## 5. Rastreabilidade do episódio completo

```
Observability.trace(orchestration_id)
  → Trace{ spans: [
        run-code-review (Completed),
        run-dependency-audit (Completed),
        create-deployment-record (Completed),
        deploy#1 (Failed), deploy#2 (Failed), deploy#3 (Failed),
        revert-deployment-record (Completed)
     ], complete: true }
```

As sete Executions — incluindo as três tentativas falhas e a compensação —
permanecem, cada uma, individualmente auditável e correlacionada pelo mesmo
`orchestration_id`. Nenhuma foi descartada; a falha e a recuperação são
parte do registro histórico, não um detalhe apagado.

---

## 6. O que este ciclo prova, em conjunto com os quatro anteriores

Com cinco ciclos publicados, todo o vocabulário central de Workflow
Architecture (§4) — `Phase`, `Step`, `Gate` (automático e de aprovação),
`Branch`, paralelismo, `Retry`, `Compensation`, `Failure Policy` — está
exercitado sobre conteúdo real, não apenas descrito em arquitetura.
**Nenhum mecanismo além dos já ratificados nos 20 documentos foi necessário.**
