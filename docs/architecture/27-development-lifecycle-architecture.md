# Development Lifecycle Architecture
### Framework Eng — O Processo Institucional Único de Ideation a Archive

*Versão 1.0.0 · Base normativa (congelada): Constitution · Kernel · Governance · Domain Model v1.1.0 · RFC-DM-001 · Identity & Namespace · Registry & Discovery · Validation & Certification · Composition Architecture · Workflow Architecture · Execution Architecture · Standards Architecture · Policy Architecture · Template Architecture · Skill Architecture · Observability Architecture · Organization & Tenancy Architecture · Packaging & Distribution Architecture · Compliance Architecture v1.1.0 · RFC-COMP-001 · Agent Architecture (23) · Testing Architecture (24) · Quality Gate Architecture (25) · Security Architecture (26)*

> **Tese central deste documento, provada seção a seção:** uma "Fase de Desenvolvimento" é **exatamente** um `Phase` (Workflow Architecture §4) — nada além disso. Este documento não introduz uma segunda gramática de orquestração paralela a Workflow, nem um segundo Lifecycle paralelo ao de Kernel §3. Ele nomeia **um único Workflow de referência**, com dezenove Phases, cuja maior parte já está inteiramente catalogada por Quality Gate Architecture (Documento 25) e Security Architecture (Documento 26) — e cujas fases restantes (antes de existir Component, e depois de `Active`) são compostas, sem exceção, de mecanismos já ratificados: Kernel §3-§4, Governance §7/§9/§13, Execution §7 `Plan()`, Observability, e os classificadores de mudança já existentes. O Framework Eng passa a ter, com este documento, um processo oficial de desenvolvimento de ponta a ponta — sem que uma única linha de nenhum dos vinte e quatro documentos anteriores precise mudar.

---

## 1. Posição Arquitetural

Este é o quarto documento consecutivo nesta mesma disciplina recursiva — cada um nomeando, sobre o anterior, uma catalogação mais ampla do que já existe:

```
Workflow Architecture (Documento 10)
   gramática genérica: Phase, Step, Gate, Branch, Join, Compensation, Failure Policy
        │ instanciada e nomeada por
        ▼
Quality Gate Architecture (Documento 25)
   18 Gates nomeados — a sequência pré-Active (Lint → ... → Publication)
        │ especializada por conteúdo em
        ▼
Security Architecture (Documento 26)
   21 controles — conteúdo de domínio de segurança dentro desses mesmos Gates
        │
        │ todos os três tornam-se um trecho contíguo de
        ▼
Development Lifecycle Architecture  ◄── este documento
   19 Phases — o arco inteiro, de antes de existir Component até Archive
```

**Regra de posicionamento central:** assim como Quality Gate Architecture já provou que "Gate é apenas um Workflow especializado", este documento prova a mesma tese em escopo maior: **"Fase de Desenvolvimento" é apenas um `Phase` de Workflow, nomeado**. Onde Quality Gate catalogou dezoito Steps de um trecho da sequência, este documento cataloga o Workflow de referência inteiro — usando, para o trecho que Quality Gate já cobre (fases 9-14 abaixo), exatamente as mesmas Phases já definidas no Documento 25, sem redefini-las.

### 1.1 Três regiões, três conjuntos de documentos consumidos, um único Workflow contínuo

| Região | Fases | O que já existe, integralmente, para cobri-la |
|---|---|---|
| **Antes de existir Component** | 1 (Ideation) | Kernel §4 — "antes do Contract preenchido, é apenas uma ideia, fora do domínio do Kernel" |
| **Draft → Review → Approved** | 2-8 (Requirements → Implementation) | Kernel §3-§4, Governance §7 (passos 1-2), Execution §7 `Plan()` — nenhum destes catalogado por Quality Gate, todos já ratificados |
| **Já coberto pelo catálogo de Quality Gate** | 9-14 (Testing → Publication) | Quality Gate Architecture §4.3, §8.2 (Documento 25) + Security Architecture §8.2 (Documento 26) — **mesmas Phases, zero redefinição** |
| **Pós-Active** | 15-19 (Monitoring → Archive) | Observability Architecture, Governance §13/§10, `ClassifyXChange` (Standards/Template/Skill/Agent), Kernel §3 (Deprecated/Archived/Removed), Identity §3.2 |

---

## 2. Objetivos

| # | Objetivo | Como este documento o realiza |
|---|---|---|
| O1 | Fornecer o Workflow de referência único, Ideation → Archive | §5, §6, §7 |
| O2 | Provar que "Fase" = `Phase` (Workflow §4), zero construto novo | §4 |
| O3 | Resolver, sem RFC, a tensão aparente entre a ordem pedida (Certification antes de Publication) e a regra já ratificada de que a escada L0-L4 é pós-`Active` (Validation & Certification §4) | §6, nota de ordenação |
| O4 | Provar zero duplicação com Workflow — Workflow permanece o mecanismo genérico; este documento é mais um catálogo nomeado, como Quality Gate e Security já foram | §1, §17 |
| O5 | Demonstrar que Evolution (fase 17) é recorrência das fases 8-14 para uma nova versão, nunca uma fase de natureza distinta | §6, §7.2 |
| O6 | Dar ao Framework um processo oficial de desenvolvimento de ponta a ponta (**Objetivo Prático**) | §7, §19 |

---

## 3. Escopo

### 3.1 Pertence

O catálogo de dezenove fases; o Workflow de referência que as encadeia; como cada fase reutiliza mecanismo já existente; o modelo de recorrência de versão (Evolution); a resolução da tensão de ordenação Certification/Publication.

### 3.2 Não pertence — com justificativa individual

| Excluído | Justificativa técnica |
|---|---|
| **Metodologia de gestão de projeto (Scrum, Kanban, Waterfall, cadência de sprint)** | Este documento nomeia **checkpoints institucionais**, não uma disciplina de calendário. Uma equipe pode percorrer as dezenove fases em qualquer cadência de projeto — o Framework não impõe ritmo, apenas a sequência de portões de qualidade institucional já mandatada pela Constitution, Regra Imutável nº3 |
| **Ferramenta específica de CI/CD** | `[LACUNA proposital]`, deferida — mesma fronteira já traçada por Quality Gate §3.2 |
| **Um segundo Lifecycle de Component, paralelo ao de Kernel §3** | Explicitamente **não** — ver §4.3. O Component percorre, sempre e apenas, os sete estados de Kernel §3; as dezenove fases são rótulos de processo sobre um Workflow em andamento, nunca um segundo estado persistido do Component |
| **Novo critério de quando uma mudança é Breaking** | Reutiliza `ClassifyStandardChange`/`ClassifyTemplateChange`/`ClassifySkillChange`/`ClassifyAgentChange`, já existentes — nenhum quinto classificador |

---

## 4. Modelo Conceitual

### 4.1 Prova de minimalidade — tabela de proveniência

**Este documento introduz zero entidades, zero Value Objects, zero algoritmos com corpo lógico próprio, zero estado novo.**

| Conceito usado por Lifecycle | Definido em |
|---|---|
| "Antes do Contract preenchido... fora do domínio do Kernel" (Ideation) | Kernel §4 |
| `Lifecycle` (Draft→Review→Approved→Active→Deprecated→Archived→Removed) | Kernel §3 |
| Admission Process (funil de sete passos) | Governance §7 |
| RFC Process (cinco etapas) | Governance §9 |
| Compliance contínua | Governance §13 |
| Breaking Change Process | Governance §10 |
| `Phase`, `Step`, `GATE_AUTO`, `GATE_APPROVAL`, `entry_predicate` (Decision Point) | Workflow Architecture §4 |
| `ValidateWorkflowGraph`, `EvaluateDecisionPoint` | Workflow Architecture §7 |
| `Plan`, `Dispatch`, `Recover`, `Rollback` | Execution Architecture §7 |
| `Decision`, `Decision Record` | Domain Model §14 |
| `ClassifyStandardChange`/`ClassifyTemplateChange`/`ClassifySkillChange`/`ClassifyAgentChange` | Standards §12.2; Template §11.4; Skill §9.1; Agent §9.1 |
| L0-L4, Score, Integrity | Validation & Certification §4-§6 |
| Catálogo de 18 Gates | Quality Gate Architecture §4.3 |
| Catálogo de 21 controles de segurança | Security Architecture §4.5 |
| `TestKind`, `ExecuteTestSuite` | Testing Architecture §4.5, §9 |
| `InvokeSkillStep` / `InvokeAgent` | Skill Architecture §9; Agent Architecture §9 |
| `resolve()`, `register()`/`publish_version()` | Registry & Discovery §6.1, §5 |
| `trace()`/`provenance()`/`query_events()` | Observability Architecture §7.1, §9.2, §9.5 |
| Reserva permanente de nome (tombstone) | Identity & Namespace §3.2 |
| `EnumerateSlots` | RFC-COMP-001 §4 |

### 4.2 "Fase de Desenvolvimento" = `Phase` de Workflow — nenhum construto novo

`[ESCOLHA DE DESIGN]`

**Motivação:** decidir como representar as dezenove fases pedidas sem introduzir uma segunda gramática de orquestração.

**Alternativa rejeitada:** um construto `LifecyclePhase`, distinto de `Phase` (Workflow §4), com campos próprios (ex.: `stage_number`, `methodology_hint`).

**Justificativa técnica:** exatamente a mesma decisão que Quality Gate Architecture já tomou para "Gate" — *"nenhum documento anterior é alterado; Quality Gate apenas nomeia dezoito configurações concretas... do mesmo Step"* (Quality Gate §4.2). Este documento faz o idêntico, em escopo maior: cada uma das dezenove fases **é** um `Phase` (Workflow §4), com seus próprios `Step`s configurados segundo a convenção descrita em §6. Nenhuma "Fase" tem propriedade, comportamento ou ciclo de vida que `Phase` já não possua.

### 4.3 Por que este documento não é um segundo Lifecycle

**Ponto que precisa ser absolutamente explícito, dado o nome deste documento:** "Development Lifecycle" não compete com Kernel §3. O Component sob desenvolvimento percorre, do início ao fim, exatamente os sete estados já definidos (`Draft→Review→Approved→Active→Deprecated→Archived→Removed`) — nunca um oitavo estado, nunca um estado paralelo. As dezenove fases catalogadas aqui são **rótulos de processo sobre um Workflow em execução**, não um segundo campo de estado persistido no Manifest do Component. A tabela abaixo torna essa correspondência explícita e verificável:

| Fase (Workflow, rótulo de processo) | `lifecycle_state` real do Component (Kernel §3) durante a fase |
|---|---|
| 1. Ideation | **Nenhum** — o Component ainda não existe (Kernel §4) |
| 2-8. Requirements → Implementation | `Draft` |
| 9-12. Testing → Review | `Draft` (maior parte) transicionando para `Review` |
| 13. Certification | Ver nota de ordenação, §6 — o `lifecycle_state` já é `Approved`/`Active` no momento em que a Certificação é de fato concedida |
| 14. Publication | Transição `Approved → Active` (Governance §7, passo 6) |
| 15-17. Monitoring, Maintenance, Evolution | `Active` |
| 18. Deprecation | Transição `Active → Deprecated` |
| 19. Archive | Transição `Deprecated → Archived` (e, eventualmente, `Removed`) |

Nenhuma célula desta tabela introduz um estado que Kernel §3 não já possua.

---

## 5. Estrutura do Lifecycle

O Workflow de referência tem, no máximo, dezoito `Phase`s formalmente orquestradas (a fase 1, Ideation, é por definição anterior a qualquer Component — logo anterior a qualquer Workflow, ver §4.3) mais um sub-ciclo recorrente para as fases 15-19:

```
ReferenceDevelopmentWorkflow.phases = [
  Phase(id=requirements,       next=[analysis]),
  Phase(id=analysis,           next=[architecture]),          # Governance §7 passo 2 — dedup gate
  Phase(id=architecture,       next=[rfc_gate]),
  Phase(id=rfc_gate,           entry_predicate=NeedsRFC,        # Decision Point — Workflow §7
                                next=[planning]),                # RFC em si é Governance §9, fora do Workflow
  Phase(id=planning,           next=[prototype]),
  Phase(id=prototype,          next=[implementation]),
  Phase(id=implementation,     next=[quality_gate_pipeline]),

  # ── fases 9-14: MESMAS Phases já definidas em Quality Gate §8, sem redefinição ──
  Phase(id=quality_gate_pipeline, next=[monitoring]),   # = pre-review ∪ static-checks ∪
                                                          #   implementation-review ∪ dynamic-tests ∪
                                                          #   quality-and-risk ∪ approval ∪ publication
                                                          #   (Quality Gate §8, Documento 25 — importado, não repetido)

  # ── fases 15-19: pós-Active, recorrente ──
  Phase(id=monitoring,         next=[maintenance]),
  Phase(id=maintenance,        entry_predicate=FindingRequiresChange,
                                next=[evolution, deprecation]),   # Branch — Workflow §6.2
  Phase(id=evolution,          next=[implementation]),            # ciclo: nova versão reentra em Implementation
  Phase(id=deprecation,        next=[archive]),
  Phase(id=archive,            next=[]),
]
```

`ValidateWorkflowGraph` (Workflow §7) aplica-se sem alteração — inclusive ao ciclo aparente `evolution → implementation`: não é um ciclo real no grafo de **Phases de uma única Execution**, porque cada passagem por `evolution` inicia uma **nova** Execution de Workflow (uma nova versão, Kernel §8) — mesma regra já usada por Execution EX1/Workflow WF5 ("retry/nova tentativa é sempre nova Execution, nunca reabertura"). O grafo entre `evolution` e `implementation` nunca é avaliado como um único Workflow-Execution circular; são duas invocações distintas do mesmo Workflow de referência, uma por versão.

---

## 6. Fases do Desenvolvimento

Cada linha é uma **especialização nomeada** de `Phase` (Workflow §4) — nunca mecanismo novo.

| # | Fase | Realização institucional | Provido por |
|---|---|---|---|
| 1 | **Ideation** | Precede qualquer Contract preenchido — "fora do domínio do Kernel". Produz, como saída, um `purpose` (Kernel §2.2) rascunhado, que dispara a fase seguinte | Kernel §4 |
| 2 | **Requirements** | Primeiro preenchimento do Contract (Kernel §2) — o Component nasce em `Draft` (Kernel §4) | Kernel §2-§4 |
| 3 | **Analysis** | `Step(GATE_AUTO)`, `Registry.search(capability, purpose)` — checagem de duplicação obrigatória (Governance §5, §7 passo 2) | Registry & Discovery §6.2; Governance §7 |
| 4 | **Architecture** | `Phase(pre-review)` de Quality Gate — Gates 1-2 (`Architecture Review`, `Design Review`) | Quality Gate §4.3 (Gates 1-2) |
| 5 | **RFC** | **Condicional** (`entry_predicate = NeedsRFC`) — ativada apenas quando a mudança toca Kernel/Governance/Standards de alto impacto, ou quando `ClassifyXChange = MAJOR` (Governance §9, §10) | Governance §9, §10 |
| 6 | **Planning** | `ALGORITMO Plan(orchestration_definition)` — `build_dag` + `Kernel§7.CycleDetection` + `topological_sort` | Execution Architecture §7 |
| 7 | **Prototype** | Lifecycle state `Draft` — *"existe apenas para permitir iteração antes do compromisso formal com o sistema"* | Kernel §3 |
| 8 | **Implementation** | `InvokeSkillStep`/`InvokeAgent` — processamento opaco (mesma fronteira já estabelecida, Skill §9/Agent §9) | Skill §9; Agent §9 |
| 9 | **Testing** | `Phase(dynamic-tests)` de Quality Gate — `TestKind ∈ {UNIT, INTEGRATION, CONTRACT}` | Testing §4.5; Quality Gate §4.3 (Gates 8-10) |
| 10 | **Quality Gates** | `Phase(static-checks)` + `Phase(quality-and-risk)` de Quality Gate — Lint, Formatting, Type Check, Static Analysis, Regression, Performance, Coverage | Quality Gate §4.3 (Gates 4-7, 11, 14-15) |
| 11 | **Security Validation** | Rows de segurança já dentro de `Phase(quality-and-risk)` — Security Scan, Dependency Audit, Secrets Scan | Security §8.2; Quality Gate §4.3 (Gates 12-13) |
| 12 | **Review** | `Phase(implementation-review)` + `Phase(approval)` de Quality Gate — Gate 3 (`Implementation Review`), Gate 16 (`Documentation Review`), Gate 17 (`Approval`) | Quality Gate §4.3 (Gates 3, 16-17); Governance §7 (passos 3-5) |
| 13 | **Certification** | Ver **Nota de Ordenação** abaixo — Evidence já produzida pelas fases 9-11 torna o Component certification-ready; a concessão formal segue Validation & Certification §4 | Validation & Certification §5-§6; Quality Gate §9.1 (reuso de Evidence) |
| 14 | **Publication** | `Step(INVOCATION)`, capability `registry.publish_version` — transição `Approved→Active` | Registry & Discovery §5; Governance §7 (passo 6); Quality Gate §4.3 (Gate 18) |
| 15 | **Monitoring** | `trace()`/`provenance()`/`query_events()` sobre as Executions do Component em produção | Observability Architecture §7.1, §9.2, §9.5 |
| 16 | **Maintenance** | Compliance contínua — reavaliação disparada por mudança em Standard/Policy vinculado | Governance §13 |
| 17 | **Evolution** | **Recorrência** das fases 8-14 para uma nova versão — nunca uma fase de natureza distinta (ver §7.2) | Kernel §8 (nova versão); `ClassifyXChange` |
| 18 | **Deprecation** | Transição `Active → Deprecated`, com sucessor indicado quando aplicável | Kernel §3; Governance §16 |
| 19 | **Archive** | Transição `Deprecated → Archived` (e, eventualmente, `Removed`); nome reservado permanentemente | Kernel §3; Identity & Namespace §3.2 |

### 6.1 Nota de Ordenação — Certification (13) e Publication (14)

**Tensão real, resolvida com citação, não silenciada:** Validation & Certification §4 declara, sem ambiguidade, que a escada L0-L4 é *"opcional, aditiva, pós-Active"* — e §5 ancora o próprio pedido de certificação (`request_certification`) ao estado `Active`. Isto pareceria contradizer a ordem pedida (Certification antes de Publication).

**Resolução, sem alterar Validation & Certification:** a Evidence que a Certificação consome já foi inteiramente produzida pelas fases 9-11 (Testing, Quality Gates, Security Validation) — e Quality Gate §9.1 já estabelece a regra exata que este documento reutiliza: *"GrantCertification MUST consumir a mesma Evidence[] já produzida pelos Gates... sem recoleta redundante."* A fase 13 (Certification), portanto, **não executa nenhuma nova coleta de Evidence** — ela é o ponto em que o Component se torna **certification-ready**: toda Evidence exigida por L1 (e potencialmente L2-L3, se as fases 9-11 já cobriram Standards/Policy vinculados) já existe. A **concessão formal** de qualquer nível segue, sem exceção, Validation & Certification §4-§5 — e portanto ocorre no instante em que `Active` é alcançado (fase 14) ou continuamente depois (fase 15, Monitoring). A ordem numérica pedida (13 antes de 14) é preservada como ordem de **prontidão**, nunca de **concessão formal** — nenhuma regra de Validation & Certification é violada ou reescrita.

---

## 7. Fluxo Completo do Projeto

### 7.1 Ideation → Archive (primeira versão)

```
1.  Ideation: purpose rascunhado                                                    [Kernel §4]
2.  Requirements: Contract preenchido → Draft                                        [Kernel §2-§4]
3.  Analysis: Registry.search(capability, purpose) → sem sobreposição relevante       [Registry §6.2]
4.  Architecture: Gate(Architecture Review) + Gate(Design Review) → PASS              [Quality Gate §4.3]
5.  RFC (condicional): SE toca Kernel/Governance/Standards-alto-impacto OU
    ClassifyXChange=MAJOR → Governance §9 (Draft RFC → Discussão → Revisão → Decisão)  [Governance §9]
    SENÃO: fase pulada (entry_predicate=false, Workflow §7)
6.  Planning: Plan(orchestration_definition) → Execution Plan (Artifact)               [Execution §7]
7.  Prototype: iteração em Draft, sem compromisso formal                              [Kernel §3]
8.  Implementation: InvokeSkillStep/InvokeAgent → Artifact                             [Skill §9; Agent §9]
9.  Testing: ExecuteTestSuite → Evidence[]                                             [Testing §9]
10. Quality Gates: Lint, Type Check, Static Analysis, Regression, Coverage → PASS       [Quality Gate §9]
11. Security Validation: Secrets Scan, Dependency Audit, Security Scan → PASS           [Security §9]
12. Review: Implementation Review + Documentation Review + Approval → Decision Record   [Quality Gate §4.3; Governance §7]
13. Certification: Evidence de 9-11 já satisfaz L1 (e L2/L3 se aplicável) — certification-ready
14. Publication: register()/publish_version() → Active                                 [Registry §5; Governance §7]
    → Certification formalmente concedida no instante em que Active é alcançado (§6.1)
15. Monitoring: trace()/provenance()/query_events() contínuos                           [Observability]
16. Maintenance: Compliance contínua (Governance §13) — nenhuma mudança necessária por ora
17. Evolution: (quando necessário) — ver §7.2
18. Deprecation: (eventualmente) Active → Deprecated, sucessor indicado                 [Kernel §3; Governance §16]
19. Archive: Deprecated → Archived → (eventualmente) Removed, nome reservado            [Kernel §3; Identity §3.2]
```

### 7.2 Evolution como recorrência — nunca uma fase de natureza distinta

```
Monitoring (15) detecta necessidade (Compliance drift, novo requisito, defeito)  [Observability; Governance §13]
   │
   ▼
Maintenance (16): FindingRequiresChange = true (entry_predicate, Workflow §7)
   │
   ▼
Evolution (17): NOVA versão do Component — reentra em Implementation (8)
   │  Kernel §8: "evolui por meio de novas versões de si mesmo, nunca edição silenciosa de Active"
   ▼
Implementation (8) → Testing (9) → Quality Gates (10) → Security Validation (11) →
Review (12) → Certification (13) → Publication (14)
   │  ClassifyXChange determina PATCH | MINOR | MAJOR (Standards §12.2; Template §11.4; Skill §9.1; Agent §9.1)
   │  SE MAJOR: RFC (5) reativada — Breaking Change Process, Governance §10
   ▼
Nova versão Active — Lineage estendida (Identity & Namespace §7), versão anterior
permanece Active até janela de transição decorrer, se a mudança for Breaking (Governance §10)
```

**Nenhuma lógica de detecção de "quando evoluir" é nova** — `FindingRequiresChange` é um `Predicate<Context>` (mesmo padrão já usado quatro vezes: `Slot.condition`, `Phase.entry_predicate`, `PolicyCondition`, `Assertion.predicate`-equivalente), avaliado por `EvaluateDecisionPoint` (Workflow §7), nunca um algoritmo de decisão próprio.

---

## 8. Algoritmos

**Nenhum algoritmo novo com lógica de decisão própria.** Os cinco a seguir são composição pura.

```
ALGORITMO AdvanceLifecycle(workflow_execution, current_phase):
  # idêntico à travessia já feita por run_workflow (Workflow engine) — nenhuma
  # lógica de avanço de fase própria a este documento
  gate_output ← ExecuteGate(current_phase.steps, ctx)                    # Quality Gate §9
  SE EvaluateGate(gate_output) = PASS:                                    # Quality Gate §9 / Workflow §6.1
     RETORNA next_phase(workflow_execution, current_phase)
  SENÃO:
     RETORNA RejectGate(workflow_execution, gate_output)                 # Quality Gate §9


ALGORITMO EvaluatePhaseGate(phase, context):
  RETORNA EvaluateDecisionPoint(phase, context)                          # Workflow §7 — verbatim,
                                                                           # usado para RFC (5) e Maintenance (16)


ALGORITMO TriggerRFC(component_ref, change_class):
  SE change_class = MAJOR OU component_ref.manifest.metadata.touches_frozen_base:
     RETORNA Governance.RFCProcess(component_ref)                        # Governance §9 — inalterado
  RETORNA SKIP                                                            # mesma semântica de Composition CP5


ALGORITMO PromoteVersion(component_ref, next_manifest):
  classe ← Max(ClassifyStandardChange | ClassifyTemplateChange |
               ClassifySkillChange | ClassifyAgentChange)(prev, next_manifest)  # já existente, por tipo
  SE classe = MAJOR: TriggerRFC(component_ref, MAJOR)
  RETORNA Registry.register(next_manifest, decision_record_ref)          # Registry §5 — verbatim


ALGORITMO RetireComponent(component_ref, successor_ref?):
  Registry.deprecate(component_ref, redirect_to=successor_ref, decision_record_ref)  # Registry §7.3/§13
  # decorrida a janela de transição (Governance §10):
  Registry.archive(component_ref, decision_record_ref)                    # Registry §7.3
  # nome permanece reservado para sempre (Identity §3.2) — nenhuma lógica nova
```

---

## 9. Diagramas UML

### 9.1 Fase como `Phase`, nunca entidade nova

```
┌──────────────────────────────────────────┐
│ ReferenceDevelopmentWorkflow                │  «Workflow» — instância, Workflow Architecture §4
└───────┬──────────────────────────────────┘
        │1..*
        ▼
┌─────────────┐
│   Phase      │   [Workflow §4 — reutilizado tal qual]
│   id ∈ {requirements, analysis, architecture, rfc_gate, planning,
│         prototype, implementation, quality_gate_pipeline,
│         monitoring, maintenance, evolution, deprecation, archive}
└──────┬──────┘
       │ rótulo institucional (§6), nunca tipo novo
       ▼
  "Fase de Desenvolvimento" (1 de 19 nomes catalogados)

┌────────────────┐         ┌──────────────────┐        ┌───────────────────┐
│ Kernel Lifecycle │◄───────┤ ReferenceDevelopment│──────►│ Certification L0-L4 │
│  (§3, 7 estados) │  espelha │ Workflow (Phase atual)│ dispara│ (Validation & Cert. │
└────────────────┘         └──────────────────┘        │  §4-§6, pós-Active) │
                                                          └───────────────────┘
```

### 9.2 Camadas de nomeação (recapitulação de §1)

```
Workflow (genérico) ⊂ Quality Gate (18 Gates) ⊂ Security (21 controles, mesmo espaço de Gates)
                                    │
                                    └──── Development Lifecycle (19 Phases, engloba os 18 Gates
                                          como um trecho contíguo + 8 Phases pré-existentes)
```

---

## 10. Diagramas de Sequência

### 10.1 Sequência completa — Ideation até primeira Publication

```
Owner        Governance      Registry      Execution       QualityGate/Testing/Security   Certification
  │              │               │              │                       │                      │
  ├─(Ideation, prosa, sem Component)             │                       │                      │
  ├─Requirements: preenche Contract──────────────►│ (Draft)               │                      │
  ├─Analysis────►│─search(cap,purpose)──────────►│                       │                      │
  │              │◄─sem sobreposição──────────────┤                       │                      │
  ├─Architecture (Gate Architecture/Design Review)───────────────────────►│                      │
  │              │  alt precisa RFC                                       │                      │
  │              ├─RFCProcess (Governance §9)                             │                      │
  ├─Planning─────────────────────────────────────►│ Plan() → Execution Plan│                      │
  ├─Prototype (iteração em Draft)                  │                       │                      │
  ├─Implementation────────────────────────────────►│ InvokeSkillStep/Agent │                      │
  │                                                │                       ├─Testing──────────────►│
  │                                                │                       ├─Quality Gates─────────►│
  │                                                │                       ├─Security Validation────►│
  │              │◄─Decision Record (Review/Approval)──────────────────────┤                       │
  │                                                                        ├─Evidence já pronta──────►│ (certification-ready)
  ├─Publication──►│─register()/publish_version()──►│                       │                       │
  │              │  (Approved → Active)                                    │                       │
  │                                                                        │  Certificação formal──►│ (L1..L4, pós-Active)
  │              │  [contínuo, a partir daqui]                             │                       │
  │              │◄─Monitoring: trace()/provenance()/query_events()────────┤                       │
```

### 10.2 Sequência — Evolution (recorrência)

```
Monitoring        Maintenance        Evolution         (reentra em) Implementation...Publication
    │                  │                  │                              │
    ├─finding──────────►│                  │                              │
    │            EvaluatePhaseGate(FindingRequiresChange)                  │
    │                  ├─true─────────────►│                              │
    │                  │            nova versão (Kernel §8)                │
    │                  │                  ├─ClassifyXChange = MAJOR?       │
    │                  │                  │  sim → TriggerRFC (Governance §9/§10)
    │                  │                  ├────────────────────────────────►│ (mesma cadeia 8-14, §7.1)
```

---

## 11. Estados

**Nenhum estado novo.** Prova exaustiva:

| Camada | Estados usados | Origem |
|---|---|---|
| Component | `Draft, Review, Approved, Active, Deprecated, Archived, Removed` | Kernel §3 |
| Execution (cada Step dispatched) | `Initiated, Running, Completed, Failed, Aborted` | Domain Model §8 |
| Certification | `L0..L4, Pending, Expired, Suspended, Revoked` | Validation & Certification §5 |
| Decision (RFC, Approval) | `Proposed, Authorized, Recorded` | Domain Model §8, §14 |

As "dezenove fases" **não são estados** — são posições de um Workflow em execução (rótulos de processo), nunca persistidas como um campo de estado do Component. Um Component não tem `current_lifecycle_phase` como campo de Manifest; ele tem `lifecycle_state` (Kernel §3), ponto.

---

## 12. Casos Extremos

| # | Caso | Tratamento |
|---|---|---|
| CE1 | Ideia rejeitada na Analysis (duplicidade encontrada) | `Registry.search` encontra sobreposição relevante — Governance §7 devolve a `Draft` ou rejeita antes mesmo de existir Contract completo; mesma regra de Admission, sem exceção |
| CE2 | RFC necessária, mas não aprovada | Fase 5 permanece em `Proposed` (Domain Model §8) — Workflow não avança (WF1, sem contornar gate obrigatório, Constitution Regra Imutável nº3) |
| CE3 | Prototype descartado sem avançar | Válido — `Draft` "existe apenas para permitir iteração" (Kernel §3); nenhuma penalidade institucional por abandonar um Draft |
| CE4 | Implementation abandonada indefinidamente | Componente permanece em `Draft` — sujeito a Governance §6 (Órfãos/Abandonados) se o Owner também se tornar inacessível |
| CE5 | Regressão de segurança encontrada tardiamente (após fase 11 já ter passado) | Fase 10/11 é reexecutada (mesma disciplina de Quality Gate CE2/Security CE9) — Publication (14) não é alcançada até `PASS` |
| CE6 | Certificação nunca solicitada após Active | Válido — Certification (Validation & Certification §1) é "evento independente" de Approval; Component permanece `Active` em L0 indefinidamente, sem penalidade estrutural, apenas sinalizado como não certificado no Registry (§7.3) |
| CE7 | Deprecation sem sucessor identificável | Órfão/Abandonado (Governance §6) — Steward assume interinamente, mesmo tratamento de qualquer Component sem Owner |
| CE8 | Archive tentado com Consumers ainda ativos | **MUST NOT** ser permitido — Kernel §3: *"Nenhum Consumer ativo pode depender de um componente Archived"* — violação resolvida pela Governance antes do arquivamento se completar |
| CE9 | Evolution que é, na prática, Breaking Change não reconhecido como tal | `ClassifyXChange` é a fonte de verdade, não a intenção do autor — se o algoritmo classifica MAJOR, RFC (5) e janela de transição (Governance §10) são obrigatórias independentemente do que o Owner pretendia |
| CE10 | Maintenance detecta Compliance drift | Governance §13 — prazo de resposta proporcional ao risco; se não resolvido, suspensão de descoberta ativa até regularização |
| CE11 | Component nunca sai de `Draft` (abandonado antes de Review) | Mesmo tratamento de CE4 — nenhuma fase além de 1-7 é sequer alcançada |
| CE12 | RFC bloqueada indefinidamente em discussão | Governance §9 não define prazo máximo — mesma ambiguidade já presente (e aceita) naquele documento; este documento não a resolve nem a agrava |
| CE13 | Duas versões evoluindo em paralelo (branch de manutenção + nova feature) | Seguro por construção — cada Evolution (17) é uma nova Execution de Workflow (§5), correlacionada por `orchestration_id` distinto; Lineage (Identity §7) admite múltiplas branches de versão sem conflito |

---

## 13. Performance

| Recurso | Regra de cache/complexidade | Origem |
|---|---|---|
| Todas as fases 9-14 | Idêntica à já normatizada em Quality Gate §12 — nenhuma política nova | Quality Gate §12 |
| `Plan()` (fase 6) | O(V+E) sobre o grafo de Steps — mesma ordem já aceita em Execution §10 | Execution §10 |
| `Registry.search` (fase 3) | Cache eventual para índices secundários — Registry §8, sem alteração | Registry §8 |
| `trace()`/`query_events()` (fase 15) | Regime de consistência já normatizado por Observability | Observability |

**Nenhuma política de cache nova.**

---

## 14. Eventos

**Nenhum evento novo.** Toda fase emite, exclusivamente, eventos já catalogados:

| Evento | Origem | Fase(s) |
|---|---|---|
| `ComponentRegistered`/`VersionPublished` | Registry §11 | 2, 14, 17 |
| `WorkflowDefinitionValidated`, `GatePassed`/`GateBlocked` | Workflow §11 | 4, 9-14 |
| `ExecutionPlanCreated` | Execution §11 | 6 |
| Eventos de `ExecuteTestCase`/`ExecuteTestSuite` | Testing §13 | 9 |
| Eventos de Quality Gate/Security (reutilizados) | Quality Gate §13; Security §13 | 10, 11 |
| `EffectiveRequirementsResolved`/`EffectivePolicySetResolved` | Standards §16; Policy §16 | 10-13 |
| `ComponentDeprecated`/`ComponentArchived` | Registry §11 | 18, 19 |

---

## 15. Regras Normativas (RFC 2119)

| # | Regra | Nível |
|---|---|---|
| DL1 | Uma "Fase de Desenvolvimento" MUST ser representada exclusivamente como `Phase` (Workflow §4) — MUST NOT introduzir um construto `LifecyclePhase` distinto | MUST / MUST NOT |
| DL2 | Ideation (fase 1) MUST NOT ser modelada como `Phase` orquestrada — precede a existência do Component (Kernel §4) | MUST NOT |
| DL3 | A fase RFC (5) MUST ser condicional, ativada exclusivamente quando a mudança toca Kernel/Governance/Standards de alto impacto ou quando `ClassifyXChange = MAJOR` | MUST |
| DL4 | A fase Certification (13) MUST NOT antecipar concessão formal de nível — a concessão MUST seguir Validation & Certification §4-§5 (pós-`Active`), reutilizando a Evidence já produzida sem recoleta | MUST / MUST NOT |
| DL5 | Evolution (17) MUST ser modelada como recorrência das fases 8-14 para uma nova versão — MUST NOT ser uma fase de natureza distinta ou um mecanismo de versionamento novo | MUST / MUST NOT |
| DL6 | Deprecation (18) e Archive (19) MUST seguir integralmente Kernel §3 e Governance §16 — MUST NOT introduzir estado ou processo paralelo | MUST / MUST NOT |
| DL7 | Este documento MUST NOT introduzir uma segunda máquina de estados de Component paralela a Kernel §3 | MUST NOT |
| DL8 | Este documento MUST NOT mandatar metodologia de gestão de projeto, cadência ou ferramenta específica | MUST NOT |
| DL9 | Este documento MUST NOT introduzir novo mecanismo de Registry, Versionamento, Policy, Standards, Execution ou Composition | MUST NOT |
| DL10 | As fases 9-14 MUST reutilizar, sem redefinição, as Phases já catalogadas por Quality Gate Architecture (Documento 25) | MUST |
| DL11 | `FindingRequiresChange`/`NeedsRFC` MUST ser expressos como `Predicate<Context>` (`entry_predicate`, Workflow §4) — MUST NOT introduzir um novo tipo de predicado | MUST / MUST NOT |
| DL12 | Archive (19) MUST NOT ocorrer enquanto existirem Consumers ativos declarados (Kernel §3) | MUST NOT |

---

## 16. Integrações

| Documento | Como Lifecycle o consome — sem alteração |
|---|---|
| **Constitution** | Regra Imutável nº3 (gate obrigatório) fundamenta DL7-DL9; Hierarquia das Decisões (§6) é a ordem que justifica a sequência RFC→Planning |
| **Kernel** | §3 (Lifecycle) e §4 (nascimento do Component) são a espinha dorsal de §4.3, §6 |
| **Governance** | §7 (Admission), §9 (RFC), §10 (Breaking Change), §13 (Compliance), §16 (Deprecation Lifecycle) — cada um mapeado a uma ou mais fases, sem alteração |
| **Domain Model v1.1.0** | `Decision`/`Decision Record`, ciclo de `Execution` reutilizados sem exceção |
| **RFC-DM-001** | Context Snapshot obrigatório em toda Execution de qualquer fase |
| **Identity & Namespace** | Lineage (§7) suporta múltiplas versões (Evolution); tombstone (§3.2) rege Archive |
| **Registry & Discovery** | `search()` (Analysis), `register()`/`publish_version()` (Publication), `deprecate()`/`archive()` (Deprecation/Archive) |
| **Validation & Certification** | Certification (13) e a nota de ordenação (§6.1) — nenhuma regra daquele documento é alterada |
| **Composition** | `EnumerateSlots`/`ResolveSlot` usados por Steps de Implementation/Testing/Quality Gates |
| **Workflow** | Fornece a gramática inteira (`Phase`/`Step`/`entry_predicate`) que este documento apenas nomeia |
| **Execution** | `Plan()` (fase 6), `Dispatch` (todas as fases com Step INVOCATION/GATE_AUTO) |
| **Standards / Policy** | Fonte de critério e aplicabilidade consumida pelas fases 10-13 |
| **Template Architecture** | Reutilizado por Skills/Agents invocados durante Implementation |
| **Skill / Agent Architecture** | `InvokeSkillStep`/`InvokeAgent` realizam Implementation (8) |
| **Observability Architecture** | `trace()`/`provenance()`/`query_events()` realizam Monitoring (15) |
| **Organization & Tenancy** | Namespace/organização do Component percorre as mesmas fases sem tratamento condicional |
| **Packaging & Distribution** | Bundle consome o resultado de Publication (14) para distribuição |
| **Compliance Architecture** | Maintenance (16) é, precisamente, a Compliance contínua daquele documento |
| **RFC-COMP-001** | `EnumerateSlots` consumido indiretamente via Composition |
| **Agent Architecture (23)** | Implementation (8) pode ser realizada por um Agent, não apenas por uma Skill |
| **Testing Architecture (24)** | Testing (9) é, precisamente, aquele documento |
| **Quality Gate Architecture (25)** | Fases 9-14 são, precisamente, o catálogo daquele documento — importado, não repetido |
| **Security Architecture (26)** | Security Validation (11) é, precisamente, aquele documento |

---

## 17. Validação Institucional

| Documento base | Resultado |
|---|---|
| Constitution | **PASS** — Regra Imutável nº3 é o fundamento direto |
| Kernel | **PASS** — §3-§4 reutilizados sem exceção; nenhum oitavo estado |
| Governance | **PASS** — §7, §9, §10, §13, §16 reutilizados sem redefinição |
| Domain Model v1.1.0 | **PASS** — zero entidades novas |
| RFC-DM-001 | **PASS** — Context Snapshot obrigatório, sem exceção |
| Identity & Namespace | **PASS** — Lineage/tombstone reutilizados |
| Registry & Discovery | **PASS** — `search`/`register`/`deprecate`/`archive` reutilizados |
| Validation & Certification | **PASS** — nota de ordenação resolve tensão sem alterar §4-§5 |
| Composition | **PASS** — `ResolveSlot`/`EnumerateSlots` reutilizados |
| Workflow | **PASS** — fornece a gramática inteira, intocada |
| Execution | **PASS** — `Plan`/`Dispatch` reutilizados |
| Standards | **PASS** — `ClassifyStandardChange` reutilizado |
| Policy | **PASS** — sem alteração |
| Template Architecture | **PASS** — sem alteração direta |
| Skill Architecture | **PASS** — `InvokeSkillStep` reutilizado |
| Observability Architecture | **PASS** — `trace`/`provenance`/`query_events` reutilizados |
| Organization & Tenancy | **PASS** — sem tratamento condicional |
| Packaging & Distribution | **PASS** — consome Publication sem alteração |
| Compliance Architecture | **PASS** — Maintenance é a Compliance contínua já definida |
| RFC-COMP-001 | **PASS** — `EnumerateSlots` consumido sem reabertura |
| Agent Architecture (23) | **PASS** — Implementation reutiliza `InvokeAgent` |
| Testing Architecture (24) | **PASS** — fase 9 é aquele documento |
| Quality Gate Architecture (25) | **PASS** — fases 9-14 são aquele catálogo, importado |
| Security Architecture (26) | **PASS** — fase 11 é aquele documento |
| **Exige RFC?** | **NÃO** |

**Prova formal de que Lifecycle não adiciona:**

| Item vedado pelo mandato | Verificação |
|---|---|
| Nova entidade / Value Object | Nenhuma — §4.1, §4.2 |
| Novo estado | Nenhum — §11, tabela exaustiva |
| Novo algoritmo | Nenhum — §8, cinco funções, todas composição pura |
| Duplicação com Workflow | Nenhuma — §1, §4.2: Fase = Phase, sem exceção |
| Novo Registry/Versionamento/Policy/Standards/Execution/Composition | Nenhum — §17 |

---

## 18. Dependências Futuras

| Consumidor | O que consome | Estado |
|---|---|---|
| **CI/CD** (futuro, operacional) | O Workflow de referência (§5, §7) é diretamente traduzível para um pipeline executável de ponta a ponta | Desbloqueado — Objetivo Prático |
| **Observability — implementação em Runtime** | Monitoring (15) ganha sentido pleno quando há órbita de execução mais rica para consultar | Sem bloqueio adicional |
| **Marketplace** | Publication (14) + Certification (13) já fornecem o sinal de confiança necessário para listagem | Sem bloqueio |
| **SDK** | Empacotamento do resultado de cada fase para consumo externo | Sem bloqueio |
| **Multi-Agent Architecture** (futuro) | Implementation (8) realizada por múltiplos Agents coordenados — este documento não pressupõe nem bloqueia essa extensão | Sem bloqueio |

---

## 19. Critério de Aceitação

### ✔ Checklist Institucional

| Critério do mandato | Status |
|---|---|
| Dezenove fases modeladas, cada uma reutilizando mecanismo já existente | ✔ §6 |
| Prova de que Lifecycle não cria sistema de desenvolvimento novo | ✔ §1, §4, §17 |
| Prova de que nenhum documento anterior precisa ser alterado | ✔ §17 |
| Prova de que não há duplicação entre Workflow e Lifecycle | ✔ §4.2, §17 |
| Prova de que Lifecycle organiza processos enquanto Workflow permanece o mecanismo genérico | ✔ §1.1, §4.2 |
| Prova de que o Framework agora possui um processo oficial de desenvolvimento ponta a ponta | ✔ §7, §19 |
| Posição arquitetural, Objetivos, Escopo, Modelo Conceitual, Estrutura, Fases, Fluxo, Algoritmos, UML, Sequência, Estados, Casos Extremos, Performance, Eventos, RFC2119, Integrações, Validação, Dependências Futuras, Critério de Aceitação | ✔ §1-§19, todas presentes |
| Tabela de proveniência completa | ✔ §4.1 |
| Nenhuma alteração a documento anterior — RFC separada se necessário | ✔ §17 — nenhuma mudança encontrada; nenhuma RFC necessária |

### ✔ Objetivo Prático Realizado

O Framework Eng possui, a partir deste documento, um processo institucional único e executável cobrindo o arco inteiro de um projeto de software: de uma ideia ainda fora do domínio do Kernel (fase 1) até o arquivamento permanente de um Component que deixou de fazer sentido (fase 19) — passando por Requirements, Analysis, Architecture, RFC condicional, Planning, Prototype, Implementation, Testing, Quality Gates, Security Validation, Review, Certification, Publication, Monitoring, Maintenance e Evolution recorrente. Cada uma das dezenove fases é rastreável, sem exceção, a um mecanismo já ratificado — nenhuma delas exigiu invenção.

### ✔ Confirmação Explícita

**Nenhum dos vinte e quatro documentos ativos da base normativa foi alterado.** "Fase de Desenvolvimento" é `Phase` (Workflow §4); as fases 9-14 são, literalmente, o catálogo já publicado por Quality Gate Architecture e Security Architecture; Evolution é recorrência, não mecanismo novo; a tensão de ordenação entre Certification e Publication foi resolvida com citação exata a Validation & Certification §4, nunca por reescrita silenciosa. **Development Lifecycle Architecture fecha o arco institucional completo do Framework Eng.**

---

*Fim do documento. Versão 1.0.0.*
