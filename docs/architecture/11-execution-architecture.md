# DOCUMENTO 3 — Execution Architecture

## 1. Posição Arquitetural

Execution Architecture é o **runtime substrate** — o mecanismo que transforma uma Orchestration Definition (Doc 2) + uma Assembly (Doc 1) em `Execution`s reais do Domain Model. Aplica-se não só a Workflows, mas a **qualquer** invocação de Component, orquestrada ou isolada — é a camada mais geral dos três documentos.

**Fronteira:** Execution Architecture nunca redefine o Lifecycle de `Execution` (Domain Model §8: `Initiated→Running→Completed|Failed|Aborted`) — apenas orquestra transições dentro dele.

## 2. Objetivos e Motivação
Definir scheduler, plano de execução, rastreamento de estado, checkpoint/recovery, rollback e provenance — fechando H6 na sua dimensão de runtime, sem jamais introduzir um segundo Lifecycle.

## 3. Escopo
**Pertence:** planejamento e despacho de Steps; correlação de Executions; rastreamento agregado; recovery. **NÃO pertence:** armazenamento físico em escala de milhões de Executions (Provenance Service aqui define apenas o **contrato conceitual**; escalonamento físico é `[LACUNA proposital]` — ver §14).

## 4. Modelo Conceitual

| Conceito | Natureza |
|---|---|
| `Execution` (Lifecycle) | **Reutilizado integralmente**, zero alteração |
| **Orchestration Correlation** (`orchestration_id`, `phase_id`, `step_id`, `attempt`) | **Especializado** — convenção semântica sobre o conteúdo de `Context` (ver preâmbulo do bloco); `orchestration_id` **é** o Instance Identifier (ULID, Identity §4.2) da própria Execution-pai — nenhum esquema de ID novo |
| **Execution Plan** | **Novo construto interno**, modelado como `Artifact` genérico, produzido pela Execution-pai antes de transicionar a `Running` |
| **Scheduler** | **Novo serviço interno**, substrato (mesma classe do Registry Resolver) |
| **Provenance Service** | **Novo serviço interno** — contrato conceitual definido aqui; armazenamento físico deferido |
| **Checkpoint** | **Reutilizado por emergência** — nenhuma entidade nova; decorre diretamente da imutabilidade e terminalidade já garantidas de `Execution` (Domain Model §8) |
| **Rollback** | **Especializado** — invocação de Steps `COMPENSATION` (Doc 2), cada um uma nova `Execution` |
| **Recovery** | **Novo algoritmo interno** — sem novo estado externo |

## 5. Modelo Operacional

```
plan(workflow_execution_id, orchestration_definition, assembly) → ExecutionPlan (Artifact)
  PRE:  workflow Execution está em Initiated
  POST: ExecutionPlan contém o grafo topologicamente ordenado de Steps prontos para despacho

dispatch(step, plan) → Execution
  PRE:  todas as dependências topológicas do step estão Completed (per plan)
  POST: nova Execution criada { Initiated → captured_as Context Snapshot → Running }
        Context contém { orchestration_id, phase_id, step_id, attempt }
        (regra herdada e obrigatória: RFC-DM-001 C2 — sem Context Snapshot, MUST NOT entrar em Running)

track_state(orchestration_id) → AggregateState
  POST: derivado por consulta ao Provenance Service — nunca armazenado redundantemente
```

**Invariante central:** nenhuma `Execution` é reaberta para "corrigir" seu resultado — falha é sempre tratada por uma **nova** Execution (retry) ou por uma Execution de compensação — jamais por mutação (herdado diretamente de Domain Model §8, sem exceção).

## 6. Diagramas

### 6.1 Máquina de estados — projeção fiel do Kernel/Domain Model (nenhum estado novo exposto)
```
Initiated ──(Context Snapshot capturado)──► Running ──► Completed
                                               │            │
                                               └──► Failed  └─(se compensável)─► dispara COMPENSATION (nova Execution)
                                               └──► Aborted
```
Sub-estados internos do Scheduler (Queued, Dispatched) **MUST NOT** ser expostos como estados de `Execution` — são detalhe interno, análogo às fases internas de um container dentro de um Pod `Running` no Kubernetes.

### 6.2 Sequência — planejamento e despacho
```
WorkflowExecution -> Scheduler : plan(orchestration_definition, assembly)
Scheduler -> Scheduler : topological_sort(phases, steps)
Scheduler --> WorkflowExecution : ExecutionPlan (Artifact)
loop enquanto houver steps não-terminais:
  Scheduler -> Scheduler : ready = steps com deps satisfeitas (via Provenance Service)
  par para cada step em ready:
    Scheduler -> Step : dispatch() → nova Execution
  Scheduler -> EventBus : StepDispatched
  Execution --> Scheduler : Completed | Failed (evento)
  alt Failed:
    Scheduler -> FailurePolicy : resolve(step)
Scheduler -> WorkflowExecution : todas terminais → Completed | Failed
```

### 6.3 Execution Graph (runtime, derivado da Orchestration Definition + Assembly)
```
[Step A: Execution#01J..] ──► [Step B: Execution#01K..] ─┐
                                                            ├──► [Step D: Execution#01M..]
[Step C: Execution#01L..] ─────────────────────────────────┘
   ▲ todos referenciam orchestration_id = Execution-pai do Workflow
```

## 7. Algoritmos

```
ALGORITMO Plan(orchestration_definition):
  graph = build_dag(orchestration_definition.phases, .steps)
  REUSA Kernel§7.CycleDetection(graph)                     # já validado em Doc 2, revalidado defensivamente
  RETURN topological_sort(graph)   # Execution Plan

ALGORITMO Dispatch(step, orchestration_id, attempt=0):
  ctx = Context{ orchestration_id, phase_id: step.phase, step_id: step.id, attempt }
  snap = capture_context_snapshot(ctx)          # RFC-DM-001 §3.2 — obrigatório
  exec = Execution.Initiated(performed_by=resolve_role(step), occurs_within=ctx, captured_as=snap)
  exec.transition(Running)
  RETURN exec

ALGORITMO Recover(orchestration_id):
  completed = Provenance.query(orchestration_id, state=Completed)
  plan = reconstruct_plan(orchestration_id)      # a partir do Execution Plan Artifact já produzido
  pending = plan.steps - completed.steps         # checkpoint = reuso do que já é Completed
  RETURN Dispatch(ready_subset(pending))          # nenhum step Completed é re-executado

ALGORITMO Rollback(orchestration_id, failed_phase):
  FOR phase IN completed_phases_before(failed_phase) REVERSED:
     FOR step IN phase.steps WHERE step.compensated_by IS NOT NULL:
        Dispatch(step.compensated_by, orchestration_id, attempt=0)   # nova Execution, sempre
```

## 8. Integrações

| Documento | Contrato |
|---|---|
| Domain Model §8 | Lifecycle de Execution intocado; retry/compensação usam exatamente a regra já escrita "nova tentativa = nova Execution". |
| RFC-DM-001 C2 | Context Snapshot é precondição estrutural de `Running` — reaproveitado sem alteração. |
| Identity & Namespace | `orchestration_id` é literalmente o Instance Identifier ULID já especificado (§4.2) — zero esquema novo. |
| Composition (Doc 1) | Consome Assembly como entrada do Plan; nunca resolve Providers por conta própria. |
| Workflow (Doc 2) | Consome Orchestration Definition como entrada do Plan; nunca reinterpreta Phase/Step. |
| Validation & Certification | Certificação L4 de Agent exige Certifier humano (Fase 4 §5) — Scheduler **MUST** respeitar isso ao resolver `role` para GATE_APPROVAL de alto risco. |

## 9. Casos Extremos

| Caso | Tratamento |
|---|---|
| Execução concorrente de duas instâncias do mesmo Workflow | Seguro por construção — `orchestration_id` distintos, Context Snapshots independentes e imutáveis, nenhum estado mutável compartilhado. |
| Falha parcial (alguns Steps completos, um falha) | Recovery via `Recover()` — nunca repete Steps `Completed`. |
| Provider indisponível em runtime (Certificado mas Execution falha/timeout) | Failure Policy do Step decide: RETRY(n) → nova Execution; COMPENSATE → §7 Rollback; ABORT → propaga Failed ao Workflow. |
| Timeout excedido | Execution transita a `Failed` por Constraint violada (Kernel §2.10) — tratada como falha comum pela Failure Policy. |
| Dependência quebrada em runtime (Coordinate resolvido virou Archived entre plan() e dispatch()) | Scheduler revalida contra Registry no momento do dispatch, não confia cegamente no Plan antigo se o intervalo excede um limiar configurável — reabre resolução via Composition Resolver (Doc 1). |
| Deadlock estrutural não capturado estaticamente (predicados dinâmicos) | Scheduler aplica timeout institucional no nível do Workflow inteiro — Constraint de última linha. |

## 10. Performance

**Consistência:** forte para o estado terminal de cada `Execution` individual (nunca ambíguo se terminou ou não); eventual, com SLA declarado, para `AggregateState` via Provenance Service — mesma filosofia já adotada pelo Registry (Fase 3 §9). **Particionamento:** por `orchestration_id` (afinidade natural — todas as Executions de uma mesma orquestração tendem a ser consultadas juntas). **Paralelismo:** Steps sem dependência topológica **MUST** ser despachados concorrentemente por padrão (não sequencialmente) — omitir isso seria uma escolha de design pior sem justificativa, dado que o grafo já captura precedência explicitamente.

## 11. Eventos
`ExecutionPlanCreated`, `StepDispatched`, `StepCompleted`, `StepFailed`, `CompensationTriggered`, `WorkflowExecutionCompleted`, `WorkflowExecutionFailed`, `RecoveryInitiated`.

## 12. Regras Normativas

| # | Regra | Nível |
|---|---|---|
| EX1 | Execution MUST NOT ser reaberta — falha gera nova Execution ou compensação | MUST NOT |
| EX2 | Running MUST ter Context Snapshot precedente (RFC-DM-001 C2) | MUST |
| EX3 | Steps sem dependência topológica MUST despachar em paralelo | MUST |
| EX4 | Recovery MUST NOT re-executar Steps já Completed | MUST NOT |
| EX5 | orchestration_id MUST ser o Instance Identifier da Execution-pai, nunca um ID novo | MUST |
| EX6 | Sub-estados internos do Scheduler MUST NOT ser expostos como Lifecycle de Execution | MUST NOT |

## 13. Validação Institucional

**PASS** contra Domain Model §8, RFC-DM-001 C2, Identity §4.2, Composition e Workflow (Docs 1-2). **Nenhuma RFC necessária.**

## 14. Dependências Futuras
`[LACUNA proposital]`: armazenamento físico e escala do Provenance Service (consultas por `orchestration_id` sobre milhões de Executions) é deferido a uma futura **Observability & Provenance Storage Architecture** — o contrato conceitual (`query by orchestration_id/coordinate/time_range`) já está fixado aqui e não deve mudar quando aquele documento for escrito.
