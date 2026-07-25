# DOCUMENTO 2 — Workflow Architecture

## 1. Posição Arquitetural

Um `Workflow` é uma especialização de **Operational Component** (categoria já nomeada em Domain Model §3). Workflow Architecture define **a estrutura declarativa interna** (o "como") de um Workflow — nunca sua execução runtime (Documento 3) nem sua resolução de Providers (Documento 1, do qual é consumidor direto).

**Fronteira:** um Workflow *declara* um grafo de Phases/Steps. Ele não *é* uma execução — a mesma distinção Component/Execution já estabelecida pelo Domain Model se aplica aqui sem exceção.

## 2. Objetivos e Motivação

Fechar H6 na sua dimensão estrutural: dar a Workflows uma gramática formal (Phase, Step, Gate, Branch, Join, Parallel, Retry, Timeout, Compensation, Failure Policy, Approval) sem introduzir uma segunda máquina de estados paralela ao Kernel Lifecycle e sem duplicar Decision/Execution do Domain Model.

## 3. Escopo

**Pertence:** gramática estrutural do grafo de orquestração; regras de validação estática (aciclicidade, resolubilidade de Slots); classificação de Gates.

**NÃO pertence:** despacho real de Steps, scheduling, rollback em tempo de execução (→ Documento 3); resolução de quem satisfaz um Slot (→ Documento 1, reusado, não redefinido aqui).

## 4. Modelo Conceitual

| Conceito | Natureza |
|---|---|
| `Workflow` | **Especializado** — Operational Component, Domain Model §3 |
| **Phase** | **Novo construto interno**, Value Object escopado ao Contract do Workflow (habilitado por Kernel §9) |
| **Step** | **Novo construto interno**, Value Object escopado a uma Phase; invoca exatamente um `Composition Slot` (Documento 1) |
| "Stage" | **Rejeitado explicitamente** como sinônimo redundante de Phase — um único termo canônico, per Constitution (Consistência) |
| **Gate (automatizado)** | **Especializado** — realizado como uma `Execution` que produz `Evidence` (Domain Model, já existente) |
| **Gate (aprovação)** | **Especializado** — realizado como uma `Decision` que produz `Decision Record`, autorizada por um `Role` (Governance §2; humano ou Agent per Domain Model §20, com a restrição de L4/Certificação já herdada de Validation & Certification §5) |
| **Branch / Decision Point / Join** | **Novos construtos internos**, propriedades de topologia do grafo de Phases (Value Objects) |
| **Parallel execution** | Propriedade de topologia (ausência de aresta de precedência entre Phases) — não é uma entidade |
| **Retry** | **Reutilizado integralmente** — Domain Model §8: "uma nova tentativa é uma nova Execution" |
| **Timeout** | **Reutilizado** — expresso como `Constraint` (Kernel §2.10) anexado a um Step |
| **Compensation** | **Novo construto interno** — um Step marcado `kind: compensation`, referenciado por outro Step via `compensated_by` |
| **Failure Policy** | **Novo construto interno**, Value Object: `{ on_failure: ABORT \| SKIP \| RETRY(n) \| COMPENSATE }` |

**Estrutura formal da Orchestration Definition** (conteúdo interno do Manifest de um Workflow, per Kernel §9):
```
Phase {
  id, sequence_hint
  steps: Step[]
  entry_predicate: Predicate<Context>?     (Decision Point)
  next: [PhaseRef]  (múltiplos = Branch; convergência de múltiplos = Join)
}
Step {
  id
  slot: CompositionSlot                    (Documento 1)
  kind: INVOCATION | GATE_AUTO | GATE_APPROVAL | COMPENSATION
  failure_policy: FailurePolicy
  timeout: Constraint
  compensated_by: StepRef?
}
```

## 5. Modelo Operacional

```
validate_workflow_definition(manifest) → ValidationResult
  PRE:  manifest.component_type = Workflow
  POST: grafo de Phases é acíclico (Kernel §7)
        E todo Step.slot é resolúvel em princípio (Documento 1, sem exigir resolução real ainda)
        E todo GATE_APPROVAL referencia um Role class válido (Governance §2)
        E todo COMPENSATION é referenciado por exatamente um Step não-compensation
```

**Invariante:** um Workflow **MUST NOT** entrar em `Review` (Kernel Lifecycle) sem passar em `validate_workflow_definition` — reaproveita exatamente o gate de Verification já definido em Validation & Certification §4.

## 6. Diagramas

### 6.1 Estados de um Gate (não um novo Lifecycle — um sub-fluxo local ao Step)
```
Step[kind=GATE_AUTO]:    Dispatched ──► Execution produz Evidence ──► PASS | BLOCK
Step[kind=GATE_APPROVAL]: Dispatched ──► Decision solicitada ao Role ──► Decision Record{grant|deny} ──► PASS | BLOCK
```

### 6.2 Grafo de fases com Branch/Join/Parallel
```
Phase A ──► Phase B ─┐
        └─► Phase C ─┴──► Phase D (Join)      [B,C paralelas — sem aresta entre si]
Phase A.entry_predicate=(risco>0.7) → Branch para Phase C' em vez de C   [Decision Point]
```

### 6.3 Sequência — Step com falha e compensação
```
Scheduler -> Step(kind=INVOCATION) : dispatch
Step --> Scheduler : Execution=Failed
Scheduler -> FailurePolicy : lookup(step) = COMPENSATE
Scheduler -> Step.compensated_by : dispatch (nova Execution)
Compensation Step --> Scheduler : Execution=Completed
Scheduler -> Workflow Execution : mark phase reverted, propagate ABORT upstream se configurado
```

## 7. Algoritmos

```
ALGORITMO ValidateWorkflowGraph(phases):
  REUSA Kernel§7.CycleDetection(phases)                 # 3ª reaplicação — ver preâmbulo do bloco
  FOR EACH step IN all_steps(phases):
     IF step.kind == COMPENSATION:
        assert exactly_one_referencer(step)
     IF step.kind == GATE_APPROVAL:
        assert step.role_class resolvable via Governance§2
  RETURN OK | ValidationError(detalhe)

ALGORITMO EvaluateDecisionPoint(phase, context):
  IF phase.entry_predicate is PureExpression:
     RETURN evaluate(phase.entry_predicate, context)     # sem Execution
  ELSE:  # predicate depende de output de Component
     RETURN awaits Step Execution referenciado, então avalia
```

## 8. Integrações

| Documento | Contrato |
|---|---|
| Kernel §7, §9 | Cycle detection reaplicado; Orchestration Definition habilitada pelo Extension Model. |
| Governance | GATE_APPROVAL usa exatamente o mecanismo de Role/Decision já existente — nenhuma autoridade nova criada. |
| Domain Model | Gate automatizado = Execution+Evidence; Gate de aprovação = Decision+Decision Record. Zero entidades novas. |
| Composition (Doc 1) | Todo Step.slot é resolvido exclusivamente via Composition Resolver — Workflow nunca resolve Providers por conta própria. |
| Validation & Certification | `validate_workflow_definition` é literalmente o critério de Conformance já anunciado em Fase 4 §7 para o tipo Workflow — fechamento do forward-reference. |

## 9. Casos Extremos

| Caso | Tratamento |
|---|---|
| Ciclo entre Phases | Rejeitado em `validate_workflow_definition` — Workflow nunca sai de `Draft`. |
| Join aguardando um ramo que nunca completará (deadlock estrutural) | Detectável estaticamente: todo Join **MUST** ter todos os seus predecessores alcançáveis a partir da única Phase inicial — verificação de alcançabilidade, parte da mesma validação. |
| GATE_APPROVAL cujo Role não tem ocupante no momento | `SlotUnsatisfied`-equivalente a nível de Step — Execution do Workflow bloqueia a Phase, não aborta o Workflow inteiro (Failure Policy decide). |
| Compensation que também falha | Escalada — não há "compensação da compensação" automática; Failure Policy da Compensation **MUST** ser `ABORT` (regra normativa, evita recursão infinita). |

## 10. Performance

Validação estática é O(V+E) sobre o grafo de Phases (detecção de ciclo padrão) — trivial mesmo em Workflows com centenas de Steps. Nenhuma preocupação de escala nova além da já coberta por Composition (Doc 1) para resolução de Slots.

## 11. Eventos
`WorkflowDefinitionValidated`, `WorkflowDefinitionRejected(reason)`, `GateEvaluated`, `GatePassed`, `GateBlocked`, `CompensationTriggered`.

## 12. Regras Normativas

| # | Regra | Nível |
|---|---|---|
| WF1 | Grafo de Phases MUST ser acíclico | MUST |
| WF2 | "Stage" MUST NOT ser usado como sinônimo de Phase na documentação institucional | MUST NOT |
| WF3 | GATE_APPROVAL MUST produzir um Decision Record | MUST |
| WF4 | Compensation Step MUST ter Failure Policy = ABORT | MUST |
| WF5 | Retry MUST criar uma nova Execution, nunca reabrir a anterior | MUST |
| WF6 | Todo Join MUST ser estaticamente alcançável de todos os seus predecessores declarados | MUST |

## 13. Validação Institucional

**PASS** contra Kernel, Governance, Domain Model, Composition. **Nenhuma RFC necessária.**

## 14. Dependências Futuras
Execution Architecture (Doc 3) consome a Orchestration Definition para gerar o Execution Plan real.
