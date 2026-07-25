# Quality Gate Architecture
### Framework Eng — A Institucionalização de Quando um Component Pode Evoluir

*Versão 1.0.0 · Base normativa (congelada): Constitution · Kernel · Governance · Domain Model v1.1.0 · RFC-DM-001 · Identity & Namespace · Registry & Discovery · Validation & Certification · Composition Architecture · Workflow Architecture · Execution Architecture · Standards Architecture · Policy Architecture · Template Architecture · Skill Architecture · Agent Architecture · Testing Architecture · RFC-COMP-001*

> **Tese central deste documento, provada seção a seção:** um `Quality Gate` é **exatamente** um `Step` (Workflow Architecture §4) de `kind ∈ {GATE_AUTO, GATE_APPROVAL}`, configurado segundo uma das dezoito convenções nomeadas catalogadas aqui — nunca um mecanismo, entidade, Runtime, Scheduler ou estado novo. Este documento não cria um pipeline: **nomeia e organiza**, em uma única sequência coerente, dezoito instâncias já inteiramente expressáveis pela gramática de Workflow, Testing, Validation & Certification e Governance já ratificadas — e amarra essa sequência, explicitamente, às transições de Kernel Lifecycle (§3) e à escalada de Certificação (Validation & Certification §4-§5) que já existiam, separadamente, antes deste documento.

---

## 1. Posição Arquitetural

Constitution, Regra Imutável nº3: *"Nenhum Workflow pode remover ou contornar um gate de qualidade obrigatório para atingir velocidade."* Esta regra existe desde o documento fundacional — mas, até este documento, "gate de qualidade obrigatório" era uma frase sem mecanismo concreto de amarração: Workflow §4 já definia `GATE_AUTO`/`GATE_APPROVAL` como construtos genéricos; Kernel §3 já exigia verificação antes de `Review→Approved`; Governance §7 já descrevia o funil de Admission em prosa; Validation & Certification §4 já desenhava a escalada L0-L4 como "opcional, aditiva, pós-Active." **Nenhum dos quatro, sozinho, nomeava a sequência concreta e completa que um Component percorre.** Este documento é essa nomeação — nada além dela.

**Posição na cadeia já estabelecida:**

```
Kernel §3 (Lifecycle)         Governance §7 (Admission)      Validation & Certification §4 (Certification Pipeline)
Draft → Review → Approved → Active                            Active → L0 → L1 → L2 → L3 → L4
        └───────────────┬───────────────┘                              └──────────┬──────────┘
                         │                                                        │
                    Quality Gate  ◄── este documento: nomeia a sequência
                    (Workflow §4, Phase/Step)                concreta de Steps que já satisfaz,
                                                              em ambos os trechos, o que os quatro
                                                              documentos acima já exigiam em prosa
```

**Fronteira exata:** Quality Gate Architecture não introduz uma quinta camada de decisão. Toda autoridade permanece exatamente onde já estava — Governance decide Admission (§7-§8), Validation & Certification decide nível de confiança (§5-§6), Workflow decide orquestração (§4), Kernel decide forma e transição (§3). Este documento apenas **cataloga, nomeadamente**, dezoito instâncias já expressáveis por essa gramática, e as organiza em uma sequência de referência.

---

## 2. Objetivos

| # | Objetivo | Como este documento o realiza |
|---|---|---|
| O1 | Nomear institucionalmente os dezoito Gates pedidos, cada um como convenção de `Step`, nunca mecanismo novo | §4.3 |
| O2 | Amarrar explicitamente a sequência de Gates às transições de Kernel Lifecycle e à escalada de Certificação | §4.4, §8 |
| O3 | Demonstrar que "Gate" é inteiramente reutilização de Workflow §4 (`GATE_AUTO`/`GATE_APPROVAL`), nunca um terceiro tipo de Step | §4.2 |
| O4 | Fornecer o processo de referência completo que um Component percorre antes de ser apto para produção (**Objetivo Prático**) | §8, §18 |
| O5 | Servir de base direta, sem tradução adicional, para automação de pipelines de CI/CD e para orientação de Agentes de IA durante desenvolvimento | §17, §18 |

---

## 3. Escopo

### 3.1 Pertence

Como um Component progride durante o desenvolvimento (catálogo de Gates, §4.3); o que cada Gate exige (Slot/capability/Standard vinculado); como cada Gate produz Evidence ou Decision Record; como o resultado de cada Gate influencia Certification; a sequência de referência ponta a ponta (§8).

### 3.2 Não pertence — com justificativa individual

| Excluído | Justificativa técnica |
|---|---|
| **Ferramenta ou tecnologia específica de CI/CD** | `[LACUNA proposital]`, deferida — este documento define a estrutura institucional; a automação operacional (GitHub Actions, Jenkins, etc.) é implementação, não arquitetura — mesma fronteira que Standards §3.2 traça para serialização física |
| **Um quinto tipo de Step ou uma máquina de estados de Gate própria** | Já resolvido — Workflow §4 já define `GATE_AUTO`/`GATE_APPROVAL`; introduzir um terceiro violaria a mesma disciplina que impediu Policy de ganhar lifecycle próprio (Policy §5.5, PL10) |
| **Novo critério normativo de segurança, performance ou cobertura** | Standards Architecture e Policy Architecture já são a única fonte de critério (Standards §1: "responsabilidade institucional exclusiva: ser a única fonte de definição normativa") — Quality Gate consome, nunca define, threshold |
| **Nova forma de Certification** | Validation & Certification permanece autoridade exclusiva sobre L0-L4 — Quality Gate apenas alimenta a Evidence que aquele pipeline já consumia (Testing §7.3) |

---

## 4. Modelo Conceitual

### 4.1 Prova de minimalidade — tabela de proveniência

**Este documento introduz zero entidades, zero Value Objects, zero algoritmos com corpo lógico próprio.**

| Conceito usado por Quality Gate | Definido em |
|---|---|
| `Phase`, `Step`, `GATE_AUTO`, `GATE_APPROVAL`, `FailurePolicy` | Workflow Architecture §4 |
| `ValidateWorkflowGraph`, `EvaluateDecisionPoint` | Workflow Architecture §7 |
| `Decision`, `Decision Record`, autoridade de `Role` | Domain Model §14; Governance §2, §7-§8 |
| `Execution`, `Artifact`, `Evidence`, `Context Snapshot` | Domain Model §2, §8, §13; RFC-DM-001 §3.2 |
| `Lifecycle` (Draft→Review→Approved→Active→...) | Kernel §3 |
| Admission Process (funil de sete passos) | Governance §7 |
| Certification Pipeline (L0-L4, Score, Integrity) | Validation & Certification §4-§6 |
| `Slot`, `ResolveSlot`, `Assembly` | Composition Architecture §4, §7 |
| `Dispatch`, `Recover`, `Rollback` | Execution Architecture §7 |
| `NormativeRequirement`, `ComplianceTarget`, `ClassifyStandardChange` | Standards Architecture §4, §12.2 |
| `enforcement_mode`, `applies_at = WORKFLOW`/`EXECUTION`, "Workflow Policy" | Policy Architecture §5.4, §6, §8 |
| `Template`, `Expand` | Template Architecture §11 |
| `InvokeSkillStep`, `ClassifySkillChange` | Skill Architecture §9 |
| `InvokeAgent`, `ClassifyAgentChange` | Agent Architecture §9 |
| `TestCase`, `TestKind`, `ExecuteTestSuite`, `ExecuteTestCase`, `EvaluateResult`, `CollectEvidence`, `Coverage`(=`Metric`) | Testing Architecture §4, §9 |
| `EnumerateSlots` | RFC-COMP-001 §4 |

### 4.2 Gate = convenção nomeada de `Step`, nunca um terceiro tipo

`[ESCOLHA DE DESIGN]`

**Motivação:** decidir como representar "Quality Gate" sem introduzir uma entidade `Gate` própria.

**Alternativa rejeitada:** um `component_type` ou Value Object `Gate`, com seu próprio ciclo de vida.

**Justificativa técnica:** Workflow §4 já resolveu, exaustivamente, o que um Gate é estruturalmente: *"Gate (automatizado) — realizado como uma Execution que produz Evidence"*; *"Gate (aprovação) — realizado como uma Decision que produz Decision Record, autorizada por um Role."* E Workflow §6.1 já dá o sub-fluxo exato: `Step[kind=GATE_AUTO]: Dispatched → Execution produz Evidence → PASS | BLOCK`; `Step[kind=GATE_APPROVAL]: Dispatched → Decision solicitada ao Role → Decision Record{grant|deny} → PASS | BLOCK`. Nada disso precisa ser reescrito. Este documento apenas **nomeia** dezoito configurações concretas e recorrentes desse mesmo `Step` — exatamente a mesma técnica que Policy §6 já usa para suas cinco "classes nomeadas" (*"não são subtipos. São padrões de uso, distinguidos exclusivamente pela combinação de scope e applies_at. Nenhum component_type novo é introduzido"*) e que Testing §4.5 usa para `TestKind` (classificação, não entidade).

### 4.3 Catálogo institucional dos dezoito Gates

Cada linha é uma **convenção de configuração de `Step`** (Workflow §4) — nunca um `StepKind`, `EvaluationMethod.kind` ou entidade nova. A coluna "Realização" aponta ao mecanismo já ratificado que efetivamente executa o Gate.

| # | Gate | Realização (via `Step`) | Produz | `EvaluationMethod` (Standards §4.6) |
|---|---|---|---|---|
| 1 | Architecture Review | `GATE_APPROVAL`, `role_class = Reviewer` (foco arquitetural) | Decision Record | `ATTESTED` |
| 2 | Design Review | `GATE_APPROVAL`, `role_class = Reviewer` (foco de design) — mesma Review de Governance §7 passo 3-4, escopo distinto | Decision Record | `ATTESTED` |
| 3 | Implementation Review | `GATE_APPROVAL`, informado por Evidence de uma Skill de análise (ex.: `core/skill.static-analysis.code-review`, já existente) invocada via `InvokeSkillStep` | Decision Record + Evidence de insumo | `ATTESTED` (decisão), `DYNAMIC` (insumo) |
| 4 | Static Analysis | `GATE_AUTO`, `slot.required_capability = "static-analysis.*"` | Evidence(`STRUCTURAL`/`ANALYSIS_OUTPUT`) | `STATIC` ou `DYNAMIC` |
| 5 | Lint | `GATE_AUTO`, `STATIC` (Testing §4.5) | Evidence(`STRUCTURAL`) | `STATIC` |
| 6 | Formatting | `GATE_AUTO`, `STATIC` — mesmo padrão de Lint, Standard vinculado distinto | Evidence(`STRUCTURAL`) | `STATIC` |
| 7 | Type Checking | `GATE_AUTO`, `STATIC` (Testing §4.5) | Evidence(`STRUCTURAL`) | `STATIC` |
| 8 | Unit Test | `GATE_AUTO`, `TestKind = UNIT` (Testing §4.5) via `ExecuteTestSuite` | Evidence(`TEST_RESULT`) | `DYNAMIC` |
| 9 | Integration Test | `GATE_AUTO`, `TestKind = INTEGRATION` | Evidence(`TEST_RESULT`) | `DYNAMIC` |
| 10 | Contract Test | `GATE_AUTO`, `TestKind = CONTRACT` | Evidence(`TEST_RESULT`) | `DYNAMIC` ou `STATIC` |
| 11 | Regression Test | `GATE_AUTO`, `TestKind = REGRESSION`, disparado quando `ClassifyXChange` (Standards §12.2/Template §11.4/Skill §9.1/Agent §9.1) = `MAJOR` | Evidence(`TEST_RESULT`) | `DYNAMIC` |
| 12 | Security Scan | `GATE_AUTO`, `TestKind = SECURITY`, `standard_ref` a Standard de domínio de segurança | Evidence(`TEST_RESULT`/`ANALYSIS_OUTPUT`) | `DYNAMIC` |
| 13 | Dependency Audit | `GATE_AUTO`, `slot.required_capability = "security.dependency-audit"` (Skill já existente) via `InvokeSkillStep` | Evidence(`ANALYSIS_OUTPUT`) | `DYNAMIC` |
| 14 | Performance Budget | `GATE_AUTO`, `TestKind = PERFORMANCE`, `constraint` do tipo `RANGE`/temporal (Kernel §2.10) | Evidence(`TEST_RESULT`) | `DYNAMIC` |
| 15 | Coverage Verification | `GATE_AUTO`, avalia `Metric` (Coverage, Testing §4.3) contra `constraint` de threshold | Evidence(`ANALYSIS_OUTPUT`) referenciando o `Metric` | `STATIC` (leitura de série já calculada) |
| 16 | Documentation Review | `GATE_AUTO` (checagem estrutural de `purpose`/`validation` não vazios, Kernel §8) **ou** `GATE_APPROVAL` (julgamento humano de completude) | Evidence(`STRUCTURAL`) ou Decision Record | `STATIC` ou `ATTESTED` |
| 17 | Approval | `GATE_APPROVAL`, `role_class = Governance Area Steward` — Governance §7 passo 5 | Decision Record (`Approved`) | `ATTESTED` |
| 18 | Publication | `INVOCATION`, `slot.required_capability = "registry.publish_version"` — Governance §7 passo 6 | `RegistryEntry` (Registry & Discovery §5, `register()`) | N/A — não é avaliação normativa, é efetivação de uma Decision já tomada |

Nenhum dos dezoito exige um `EvaluationMethod.kind`, `evidence_kind` ou `TestKind` além dos já catalogados por Standards §4.6 e Testing §4.5.

### 4.4 Amarração à Lifecycle e à Certificação

| Trecho da sequência (§4.3) | Transição/escalada que gateia |
|---|---|
| Gates 1-3 (Reviews humanas) + 17 (Approval) | Kernel §3 `Draft → Review → Approved`; Governance §7 passos 3-5 |
| Gates 4-16 (automatizados) | Kernel §8 Validação Estrutural/de Conformidade, dentro de `Review`; e, quando repetidos pós-`Active`, a escalada L1→L4 (Validation & Certification §4-§5) — mesma Evidence, dois consumidores já existentes (Admission e Certification), nenhuma duplicação de coleta (ver §9) |
| Gate 18 (Publication) | Kernel §3 `Approved → Active`; Governance §7 passo 6 |
| Reexecução contínua pós-`Active` de qualquer Gate 4-16 | Governance §13 (Compliance contínua) — disparada quando um Standard/Policy vinculado muda, exatamente como aquele documento já mandata |

**Nenhuma nova relação entre Lifecycle e Certificação é criada.** Validation & Certification §4 já desenhava a Certificação como "opcional, aditiva, pós-Active" — este documento apenas mostra que a *mesma* Evidence produzida pelos Gates 4-16 durante `Review` **MAY** ser reaproveitada, sem nova coleta, quando o Component solicitar Certificação após `Active` (sujeito à janela de validade já normatizada em Validation & Certification §5).

---

## 5. Manifest

**Nenhum campo novo.** Quality Gate Architecture não introduz um campo de Manifest, porque a aplicabilidade de cada Gate já é inteiramente derivável dos mecanismos existentes:

| O que decidiria "quais Gates se aplicam a este Component" | Já resolvido por |
|---|---|
| Quais Standards este Component deve satisfazer (o que determina Gates 4-16) | `metadata.standards_bound` (Kernel §2.14) |
| Sob quais condições/organizações (o que determina se um Gate é `BLOCKING` ou `ADVISORY`) | Effective Policy Set, `applies_at = WORKFLOW`, classe nomeada "Workflow Policy" (Policy §6) |
| Se `test_suite[]` está presente para produzir Evidence de Gates 8-14 | `test_suite[]` (Testing §5) |

`[ESCOLHA DE DESIGN]` Não introduzir `metadata.quality_gates` ou campo equivalente. Alternativa rejeitada: um campo explícito listando quais dos dezoito Gates se aplicam a um Component. Rejeitada porque duplicaria, com um segundo mecanismo, exatamente o que `standards_bound` + Effective Policy Set já respondem de forma determinística — a mesma razão pela qual Policy §4.2 proíbe critério normativo inline (evitar dois lugares onde a mesma pergunta é respondida).

---

## 6. Contract

Nenhuma refinação de `inputs`/`outputs` é necessária além da já existente (Skill §6.1-§6.2, Agent §6.1). O "contrato" de um Gate é inteiramente o contrato do `Step` que o realiza (Workflow §4) mais o `NormativeRequirement`/`PolicyBinding` que o torna obrigatório ou opcional (Standards §4.3, Policy §5.3) — nenhuma terceira camada de contrato é introduzida.

---

## 7. Modelo Operacional

| Operação | Definida em | Especialização para Quality Gate |
|---|---|---|
| Validação do grafo de Gates | `ValidateWorkflowGraph` (Workflow §7) | Aplicada tal qual sobre as Phases da sequência de referência (§8) |
| Execução de um Gate | `Dispatch`/`InvokeSkillStep`/`InvokeAgent`/`ExecuteTestCase` | Ver §9 — nenhuma nova assinatura |
| Avaliação de resultado | `EvaluateResult` (Testing §9); `Decision Record{grant|deny}` (Workflow §6.1) | Ver §9 |
| Certificação | Validation & Certification §5-§6, §10.1 | Consome a Evidence já produzida pelos Gates automatizados, sem recoleta |
| Aplicabilidade condicional | Policy §8, `applies_at = WORKFLOW` | Um Gate cuja Policy vinculada seja `ADVISORY` não bloqueia — apenas sinaliza |

---

## 8. Fluxo

Sequência de referência completa — a resposta institucional a "o que um código precisa percorrer antes de ser considerado apto para produção" (Objetivo Prático):

```
Phase(pre-review):
   Step(architecture-review,   kind=GATE_APPROVAL, role_class=reviewer.architecture)
   Step(design-review,         kind=GATE_APPROVAL, role_class=reviewer.design)

Phase(static-checks, next=[implementation-review]):
   Step(lint,            kind=GATE_AUTO, slot=Slot(capability="lint"))
   Step(formatting,      kind=GATE_AUTO, slot=Slot(capability="formatting"))
   Step(type-check,      kind=GATE_AUTO, slot=Slot(capability="type-check"))
   Step(static-analysis, kind=GATE_AUTO, slot=Slot(capability="static-analysis.code-review"))
   Step(doc-review,      kind=GATE_AUTO, slot=Slot(capability="documentation.completeness"))

Phase(implementation-review, next=[dynamic-tests]):
   Step(impl-review, kind=GATE_APPROVAL, role_class=reviewer.implementation)

Phase(dynamic-tests, next=[quality-and-risk]):
   Step(unit,        kind=GATE_AUTO, slot=Slot(capability="testing.unit"))
   Step(integration, kind=GATE_AUTO, slot=Slot(capability="testing.integration"))
   Step(contract,    kind=GATE_AUTO, slot=Slot(capability="testing.contract"))

Phase(quality-and-risk, next=[approval]):
   Step(regression,   kind=GATE_AUTO, slot=Slot(capability="testing.regression"),
         failure_policy=FailurePolicy(ABORT))                       # QG2
   Step(security,     kind=GATE_AUTO, slot=Slot(capability="security.scan"))
   Step(dep-audit,    kind=GATE_AUTO, slot=Slot(capability="security.dependency-audit"))
   Step(performance,  kind=GATE_AUTO, slot=Slot(capability="testing.performance"))
   Step(coverage,     kind=GATE_AUTO, slot=Slot(capability="testing.coverage"))

Phase(approval, next=[publication]):
   Step(approve, kind=GATE_APPROVAL, role_class="role.governance-area.steward")   # Governance §7 passo 5

Phase(publication):
   Step(publish, kind=INVOCATION, slot=Slot(capability="registry.publish_version"))  # Governance §7 passo 6
```

Todas as Phases acima já são validadas por `ValidateWorkflowGraph` (Workflow §7, WF1/WF4/WF6) sem nenhuma extensão. A ordem escolhida (estática antes de dinâmica, revisão de implementação entre os dois, risco/qualidade antes de aprovação humana final) é uma **convenção de referência**, não uma regra normativa nova — qualquer reordenação que ainda satisfaça WF1 (acíclico) permanece válida; o único ordenamento realmente mandatado é QG2/QG3 (§14): Regression antes de Publication quando há Breaking Change, e todo Gate marcado `BLOCKING` antes de Publication.

---

## 9. Algoritmos

**Nenhum algoritmo novo com lógica de decisão própria.** Os cinco nomes pedidos são composição pura.

```
ALGORITMO ExecuteGate(step, ctx):
  SE step.kind = GATE_AUTO:
     slot_result ← Composition.ResolveSlot(step.slot, requester_ns)      # Composition §7
     SE slot_result é SlotError: RETORNA Falha(slot_result)
     resolved ← Registry.resolve(slot_result)
     CASO resolved.manifest.component_type:
        Skill  → (exec, artifact) ← InvokeSkillStep(step, ...)           # Skill §9
        Agent  → (exec, artifact) ← InvokeAgent(step, ...)               # Agent §9
        OUTRO  → (exec, artifact) ← ExecuteTestCase(test_case, slot_result, requester_ns)  # Testing §9
     evidence ← CollectEvidence(test_case, exec, EvaluateResult(test_case, artifact))       # Testing §9
     RETORNA (exec, evidence)
  SENÃO SE step.kind = GATE_APPROVAL:
     decision ← Role.decide(step.role_class, ctx)                        # Governance §8, opaco quanto ao julgamento
     decision_record ← Decision.produce(decision)                        # Domain Model §14
     RETORNA (decision, decision_record)


ALGORITMO EvaluateGate(gate_output):
  SE gate_output É Evidence:
     RETORNA (gate_output.result = "PASS") ? PASS : BLOCK                 # Workflow §6.1
  SENÃO SE gate_output É Decision Record:
     RETORNA (gate_output.outcome = "grant") ? PASS : BLOCK               # Workflow §6.1


ALGORITMO AdvanceGate(workflow_execution, gate_output):
  SE EvaluateGate(gate_output) = PASS:
     RETORNA run_workflow.next_phase(workflow_execution)                 # Workflow engine, já existente
  SENÃO:
     RETORNA RejectGate(workflow_execution, gate_output)


ALGORITMO RejectGate(workflow_execution, gate_output):
  RETORNA FailurePolicy.resolve(step, gate_output)                        # Workflow §7 — ABORT/SKIP/RETRY/COMPENSATE,
                                                                            # nenhuma lógica nova; RETRY sempre nova
                                                                            # Execution (EX1/WF5)


ALGORITMO ApprovePublication(component_ref, gate_results):
  obrigatorios ← [g PARA g EM gate_results SE g.enforcement_mode = BLOCKING]   # Policy §5.4
  SE ∃ g EM obrigatorios COM EvaluateGate(g) = BLOCK:
     RETORNA RejectGate(...)
  RETORNA Registry.register(component_ref.manifest, decision_record_ref)       # Registry §5 — Gate 18, inalterado
```

### 9.1 Reuso de Evidence entre Admission e Certification — sem recoleta

`GrantCertification` (Testing §9) **MUST** consumir a mesma `Evidence[]` já produzida pelos Gates 4-16 durante Admission, quando a janela de validade (Validation & Certification §5) ainda estiver aberta — nenhuma segunda execução do mesmo `TestCase` é disparada apenas porque o consumidor mudou de Governance §7 para Validation & Certification §10.1. Isto não é um algoritmo novo; é a aplicação literal da regra de cache já normatizada em Registry §8 e reafirmada por Testing §12: Evidence associada a um `manifest_digest` imutável é reutilizável enquanto esse digest não mudar.

---

## 10. Diagramas

### 10.1 UML — Gate como configuração de Step, nunca entidade

```
┌──────────────────────────────────────────┐
│ Workflow (Quality Gate — instância)         │  [Workflow Architecture §4]
└───────┬──────────────────────────────────┘
        │1..*
        ▼
┌─────────────┐
│   Phase      │   [Workflow §4]
└──────┬──────┘
       │1..*
       ▼
┌─────────────────────────────┐
│   Step                        │   [Workflow §4]
│   kind: GATE_AUTO|GATE_APPROVAL│ ◄── nenhum terceiro kind introduzido
│   slot ──────────────────────┼──► Composition Slot [Composition §4]
│   role_class (se GATE_APPROVAL)│
└──────┬────────────────────────┘
       │ realiza um dos 18 nomes do catálogo (§4.3) — rótulo, não tipo
       ▼
┌─────────────┐         ┌──────────────────┐
│  Evidence    │   ou    │  Decision Record  │   [Domain Model §13, §14]
└─────────────┘         └──────────────────┘
       │                          │
       └──────────informa─────────┘
                   ▼
     Validation & Certification (Score, L0-L4)   [inalterado]
```

### 10.2 Sequência — um Gate automatizado até a Certificação

```
Workflow(Phase)   Composition   Registry   Testing        Execution     Validation&Certification
     │                │            │           │                │                │
     ├─Step(GATE_AUTO)►│           │           │                │                │
     │                ├─ResolveSlot►│          │                │                │
     │                │◄─candidate─┤           │                │                │
     │                │                        │                │                │
     ├─ExecuteGate──────────────────────────────►│                │                │
     │                                          ├─ExecuteTestCase►│                │
     │                                          │◄─Execution+Artifact──────────────┤
     │                                          ├─EvaluateResult                    │
     │                                          ├─CollectEvidence──────────────────►│ (Evidence)
     ├─EvaluateGate(evidence) = PASS|BLOCK       │                                  │
     │  PASS  → AdvanceGate → próxima Phase      │                                  │
     │  BLOCK → RejectGate → FailurePolicy       │                                  │
     │                                                                              │
     │  [mais tarde, sob demanda de Certificação]                                  │
     │                                          GrantCertification consome a mesma Evidence[] (§9.1)
```

### 10.3 Estados

Nenhum diagrama de estados novo. Cada Gate produz uma `Execution` sob o Lifecycle já existente (Domain Model §8) ou uma `Decision` sob seu próprio ciclo já existente (Domain Model §8, `Proposed→Authorized→Recorded`). O `Workflow` que orquestra a sequência de referência usa exatamente `Initiated→Running→Completed|Failed|Aborted` (Domain Model §8), sem exceção — mesma disciplina de Standards §11.4, Policy §12.4, Template §10.3, Skill §10.3, Agent §10.3, Testing §10.3.

---

## 11. Casos Extremos

| # | Caso | Tratamento |
|---|---|---|
| CE1 | Gate interrompido | Execution transita a `Aborted` (Domain Model §8) — mesma regra de qualquer interrupção, nenhum estado novo |
| CE2 | Gate reprovado (`BLOCK`) | `RejectGate` invoca `FailurePolicy` (Workflow §7) — `ABORT` propaga; `SKIP` avança se a Policy vinculada permitir (`ADVISORY`); nunca contornado silenciosamente (Constitution, Regra Imutável nº3) |
| CE3 | Gate parcialmente aprovado | Mapeado sobre Partial Conformance já existente (Standards §8.2): todo `MUST` satisfeito + algum `SHOULD` não satisfeito → Gate ainda `PASS` (ST7 — falha de `MUST` nunca é gradual), mas o `SHOULD` pendente é reportado, nunca ocultado (ST8) |
| CE4 | Retry | Sempre nova Execution (EX1, Execution §12; WF5, Workflow §12) — nunca reabertura do Gate anterior |
| CE5 | Evidence conflitante (diverge de Evidence anterior para o mesmo `manifest_digest`) | Regra de Integrity (Validation & Certification §6) — o digest atual é a referência; Evidence associada a digest divergente é lida como inválida, nunca reconciliada silenciosamente |
| CE6 | Policy bloqueando o Gate | `enforcement_mode = BLOCKING`, `applies_at = WORKFLOW` (Policy §6, classe "Workflow Policy") — o Gate **MUST NOT** prosseguir; mesmo mecanismo de qualquer `Step`, sem tratamento condicional |
| CE7 | Standard obrigatório vinculado a um Gate | Avaliado via `NormativeRequirement.target.applies_to = WORKFLOW`/`EXECUTION` (Standards §4.5) — sem mecanismo novo |
| CE8 | Execution Failed (o Component sob Gate falha durante a Execution) | Evidence de falha ainda é coletada e preservada (Testing CE3) — `EvaluateGate` retorna `BLOCK`, nunca omite o resultado |
| CE9 | Coverage insuficiente | Reuso de Testing CE5 — só bloqueia se um NR/Policy explícito declarar threshold; ausência de threshold nunca é bloqueio implícito |
| CE10 | Security Scan falhou | Evidence com `result = FAIL` em `TestKind = SECURITY` → `EvaluateGate = BLOCK` — mesma disciplina de qualquer Gate automatizado |
| CE11 | Dependency Audit crítico | A Evidence produzida por `security.dependency-audit` (Skill já existente) sinaliza severidade `critical` no seu próprio conteúdo (mesma Skill/exemplo já usado em Reference Cycles anteriores) — `EvaluateResult` classifica isso como `FAIL` quando o `Constraint` do `TestCase` declarar severidade máxima tolerada |
| CE12 | Performance abaixo do orçamento | `Constraint` do tipo `RANGE`/temporal (Kernel §2.10) violado — mesmo tratamento de qualquer `TestKind = PERFORMANCE` (Testing §4.5) |
| CE13 | Documentação ausente | `purpose`/`validation` vazios falha a Validação Estrutural já existente (Kernel §8, Registry §5 `validate_structural`) — Gate 16 (`Documentation Review`, realização `GATE_AUTO`/`STATIC`) apenas expõe esse resultado já produzido, não o recalcula |
| CE14 | Breaking Change sem Regression | `ClassifyXChange = MAJOR` sem `TestCase(kind=REGRESSION)` correspondente executado → `ApprovePublication` **MUST** rejeitar (QG2, §14) — nenhuma Publication acontece sem essa Evidence |

---

## 12. Performance

| Recurso | Regra de cache/complexidade | Origem |
|---|---|---|
| Resolução de Slot de cada Gate | Cache indefinido | Registry §8; Composition §10 |
| Evidence de Gates 4-16 reutilizada por Certificação | Reuso sem recoleta enquanto `manifest_digest` não mudar (§9.1) | Registry §8; Testing §12 |
| Effective Policy Set (`applies_at=WORKFLOW`) | TTL/invalidação por evento, nunca indefinido | Policy §15.1 |
| Sequência completa de referência (§8) | O(número de Steps) — mesma ordem já aceita para `run_workflow` (Workflow §10) | Workflow §10 |

**Nenhuma política de cache nova.**

---

## 13. Eventos

**Nenhum evento novo.** Tabela de eventos já existentes, aplicáveis sem modificação:

| Evento | Origem |
|---|---|
| `WorkflowDefinitionValidated`/`GateEvaluated`/`GatePassed`/`GateBlocked` | Workflow §11 |
| `StepDispatched`/`StepCompleted`/`StepFailed` | Execution §11 |
| Eventos de `ExecuteTestCase`/`ExecuteTestSuite` (herdados de Execution/Composition) | Testing §13 |
| `EffectiveRequirementsResolved` | Standards §16 |
| `EffectivePolicySetResolved` | Policy §16 |
| `ComponentRegistered`/`VersionPublished` (Gate 18, Publication) | Registry §11 |

---

## 14. Regras Normativas (RFC 2119)

| # | Regra | Nível |
|---|---|---|
| QG1 | Todo Component SHOULD passar pela sequência de referência de Quality Gates (§8) antes de `Active` | SHOULD |
| QG2 | Breaking Changes (qualquer `ClassifyXChange = MAJOR`) MUST possuir um Gate de Regression com resultado `PASS` antes de Publication | MUST |
| QG3 | Publication (Gate 18) MUST exigir que todo Gate marcado `BLOCKING` (via Policy/Standard vinculado) tenha resultado `PASS` | MUST |
| QG4 | Evidence produzida por qualquer Gate MUST ser preservada (Domain Model §13; Standards §4.6 `retention`) | MUST |
| QG5 | Certification MUST considerar a Evidence já produzida pelos Gates executados, sem recoleta redundante quando o `manifest_digest` não mudou | MUST |
| QG6 | Um Gate MUST ser realizado exclusivamente como `Step(kind=GATE_AUTO\|GATE_APPROVAL)` — MUST NOT introduzir um `StepKind` novo | MUST / MUST NOT |
| QG7 | A sequência de Gates MUST respeitar a aciclicidade já exigida do grafo de Phases (WF1, Workflow §12) | MUST |
| QG8 | Um Gate reprovado MUST impedir a transição de Lifecycle associada — MUST NOT ser contornado silenciosamente (Constitution, Regra Imutável nº3) | MUST / MUST NOT |
| QG9 | Retry de um Gate MUST ser uma nova Execution — MUST NOT reabrir a anterior | MUST / MUST NOT |
| QG10 | Um Gate cuja Policy vinculada declare `enforcement_mode = ADVISORY` MUST NOT bloquear a transição — apenas sinalizar | MUST NOT |
| QG11 | Este documento MUST NOT introduzir Runtime, Scheduler, Registry, Execution ou mecanismo de Certificação paralelo | MUST NOT |
| QG12 | O catálogo de dezoito Gates (§4.3) MUST ser lido como convenção de configuração de `Step` — MUST NOT ser tratado como novo `component_type` ou entidade | MUST / MUST NOT |
| QG13 | A ordem específica apresentada em §8 é referência, não mandato — qualquer ordenação que satisfaça WF1 (aciclicidade) e QG2/QG3 permanece válida | — |

---

## 15. Integrações

| Documento | Como Quality Gate o consome — sem alteração |
|---|---|
| **Constitution** | Regra Imutável nº3 é o mandato constitucional direto que este documento operacionaliza |
| **Kernel** | `Lifecycle` (§3) gateado pela sequência; Validação Estrutural (§8) realiza Gates 4-7, 16 |
| **Governance** | Admission Process (§7) é literalmente Gates 1-3, 17-18; Compliance (§13) dispara reexecução pós-`Active` |
| **Domain Model v1.1.0** | `Evidence`, `Decision`, `Decision Record`, `Execution` reutilizados sem alteração |
| **RFC-DM-001** | Context Snapshot obrigatório em toda Execution de Gate |
| **Registry & Discovery** | Gate 18 é `register()`/`publish_version()`, inalterado |
| **Validation & Certification** | Consome Evidence dos Gates 4-16 sem recoleta (§9.1); Score/threshold permanecem sua autoridade exclusiva |
| **Composition** | `ResolveSlot` resolve o Provider de cada Gate automatizado |
| **Workflow** | Gate É `Step(GATE_AUTO\|GATE_APPROVAL)` — nenhuma extensão de gramática |
| **Execution** | `Dispatch` é o único caminho real de despacho |
| **Standards** | Fonte exclusiva de threshold/critério normativo consumido pelos Gates |
| **Policy** | `applies_at=WORKFLOW`, "Workflow Policy" (§6), `enforcement_mode` determinam obrigatoriedade |
| **Skill** | `InvokeSkillStep` é o caminho de Gates cujo Provider é uma Skill (ex.: Implementation Review, Dependency Audit) |
| **Agent** | `InvokeAgent` é o caminho de Gates cujo Provider é um Agent |
| **Testing Architecture** | `TestCase`/`TestKind`/`ExecuteTestSuite`/`ExecuteTestCase`/`EvaluateResult`/`CollectEvidence` realizam integralmente os Gates 8-15 |

---

## 16. Validação Institucional

| Documento base | Resultado |
|---|---|
| Constitution | **PASS** — Regra Imutável nº3 é a base direta; nenhuma outra tocada |
| Kernel | **PASS** — Lifecycle e Validação Estrutural reutilizados sem alteração |
| Governance | **PASS** — Admission Process reutilizado tal qual; nenhuma autoridade nova |
| Domain Model v1.1.0 | **PASS** — zero entidades novas |
| RFC-DM-001 | **PASS** — Context Snapshot obrigatório, sem exceção |
| Identity & Namespace | **PASS** — nenhuma extensão de esquema |
| Registry & Discovery | **PASS** — Gate 18 é `register()` inalterado |
| Validation & Certification | **PASS** — autoridade de Score/nível intocada; consome Evidence sem recoleta |
| Composition | **PASS** — `ResolveSlot` reutilizado sem modificação |
| Workflow | **PASS** — `GATE_AUTO`/`GATE_APPROVAL` reutilizados tal qual; nenhum `StepKind` novo |
| Execution | **PASS** — `Dispatch` único caminho real |
| Standards | **PASS** — fonte exclusiva de critério, nunca redefinida |
| Policy | **PASS** — `applies_at=WORKFLOW` reutilizado sem novo enum |
| Template Architecture | **PASS** — não referenciada diretamente além do já reutilizado por Skill/Agent |
| Skill Architecture | **PASS** — `InvokeSkillStep` reutilizado |
| Agent Architecture | **PASS** — `InvokeAgent` reutilizado |
| Testing Architecture | **PASS** — `TestCase`/`TestKind`/algoritmos de Testing reutilizados tal qual, sem reabertura |
| RFC-COMP-001 | **PASS** — `EnumerateSlots` consumido indiretamente via Composition, sem reabertura |
| **Exige RFC?** | **NÃO** |

**Prova formal de que Quality Gate não adiciona:**

| Item vedado pelo mandato | Verificação |
|---|---|
| Runtime novo | Nenhum — `Dispatch`/`InvokeSkillStep`/`InvokeAgent`/`ExecuteTestCase` reutilizados (§9) |
| Scheduler novo | Nenhum — Execution §7 Scheduler, inalterado |
| Execution nova | Nenhuma — mesma `Execution`, mesmo Lifecycle (§10.3) |
| Registry novo | Nenhum — Registry & Discovery §5, Gate 18 |
| Lifecycle novo | Nenhum — Kernel §3 e Domain Model §8, sem exceção |
| Mecanismo paralelo de Validation/Testing/Certification | Nenhum — Gates 8-16 são instâncias de Testing Architecture; Certification permanece autoridade exclusiva de Validation & Certification |

---

## 17. Dependências Futuras

| Consumidor | O que consome | Estado |
|---|---|---|
| **CI/CD** (futuro, operacional) | A sequência de §8 é diretamente traduzível para um pipeline executável, sem tradução conceitual adicional | Desbloqueado — Objetivo Prático |
| **Security Architecture** (futuro) | Gates `Security Scan`/`Dependency Audit` já reservam o slot conceitual; nenhuma extensão estrutural necessária | Sem bloqueio |
| **Observability** | Séries históricas de `GatePassed`/`GateBlocked` em escala | `[LACUNA proposital]` já declarada em Execution §14 |
| **Deployment** (futuro) | Gate 18 (Publication) já é o ponto de transição `Approved→Active` que um pipeline de deployment consumiria diretamente | Sem bloqueio |
| **Marketplace** (futuro) | Certificação e Coverage já fornecem o sinal de confiança necessário para listagem | Sem bloqueio |

---

## 18. Critério de Aceitação

### ✔ Checklist Institucional

| Critério do mandato | Status |
|---|---|
| Quality Gate é especialização de Workflow, sem Runtime/Scheduler/Execution/Registry/Validation/Testing/Certification próprios | ✔ §1, §16 |
| Dezoito Gates modelados como Workflow+Step+Execution, nunca mecanismo próprio | ✔ §4.3, §8 |
| Gate produz apenas Evidence (ou Decision Record); nenhum estado novo | ✔ §4.2, §10.3 |
| Algoritmos (`ExecuteGate`, `EvaluateGate`, `AdvanceGate`, `RejectGate`, `ApprovePublication`) são pura composição | ✔ §9 |
| Casos extremos exaustivos, incluindo os catorze pedidos | ✔ §11 |
| RFC2119 completo | ✔ §14 |
| Performance/Eventos sem novidade | ✔ §12, §13 |
| Integração completa com Workflow, Testing, Execution, Validation, Certification, Standards, Policy, Skill, Agent | ✔ §15 |
| UML e diagramas de sequência | ✔ §10 |
| Prova de reutilização e tabela de proveniência completa | ✔ §4.1 |
| Tabela institucional de validação | ✔ §16 |
| Nenhuma alteração a documento anterior — RFC separada se necessário | ✔ §16 — nenhuma mudança encontrada; nenhuma RFC necessária |

### ✔ Objetivo Prático Realizado

Com este documento, está formalizado o processo institucional completo que um Component percorre entre `Draft` e `Active` — e, além dele, a escalada opcional de Certificação até L4 — inteiramente por reutilização. Duas consequências diretas, ambas já antecipadas no pedido:

1. **Automação de CI/CD:** a sequência de §8 é, sem tradução conceitual adicional, um roteiro executável — cada `Step` já resolve, por si, o Provider concreto que o executa (Composition §7), e cada resultado já é `Evidence`/`Decision Record` auditável (Domain Model §13-§14).
2. **Orientação de Agentes de IA durante o desenvolvimento:** um Agent (Agent Architecture) que precise decidir "meu trabalho está pronto?" possui, agora, uma resposta institucional explícita e verificável — a mesma sequência de dezoito Gates, nunca um critério tácito ou heurística própria do Agent.

### ✔ Confirmação Explícita

**Nenhum documento da base normativa congelada foi alterado.** Quality Gate Architecture, como Skill, Agent e Testing Architecture antes dela, é construída inteiramente por prova de reutilização — os dezoito nomes pedidos foram, cada um, resolvidos como uma configuração já expressável de `Step`, nunca como conceito novo.

---

*Fim do documento. Versão 1.0.0.*
