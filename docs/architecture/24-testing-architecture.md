# Testing Architecture
### Framework Eng — A Realização Concreta de "Testing" em Validation & Certification

*Versão 1.0.0 · Base normativa (congelada): Constitution · Kernel · Governance · Domain Model v1.1.0 · RFC-DM-001 · Identity & Namespace · Registry & Discovery · Validation & Certification · Composition Architecture · Workflow Architecture · Execution Architecture · Standards Architecture · Policy Architecture · Template Architecture · Skill Architecture · Agent Architecture · RFC-COMP-001*

> **Tese central deste documento, provada seção a seção:** `Testing` não é um Component, não é uma entidade, não é um mecanismo paralelo — é a **realização concreta** de uma caixa já nomeada e já contratada em Validation & Certification §10.1 (`Pipeline -> Testing : execute(test_suite)` → `Testing --> Pipeline : Evidence[] (via Execution)`), sem que aquele documento jamais tenha especificado *como* essa caixa opera por dentro. Este documento fecha exatamente esse forward-reference, e mais dois análogos (Skill §7.3, Agent §7.3), sem alterar nenhum deles. Testing não define — **integra**.

---

## 1. Posição Arquitetural

Validation & Certification §1 já nomeia `Testing` como um dos dez termos com responsabilidade própria: *"Testing — 'O que acontece quando eu executo isto?' — Atividade que produz Evidence — Novo (mecanismo, não julgamento)."* Aquele mesmo documento, em §10.1, já desenha a sequência de solicitação de certificação com uma caixa literal chamada `Testing`, contratada como:

```
Pipeline -> Testing : execute(test_suite)
Testing --> Pipeline : Evidence[] (via Execution)
```

**Este é o contrato de topo que Testing Architecture formaliza — nada além dele.** `execute(test_suite) → Evidence[]`, produzido "via Execution" — ou seja, o próprio documento-base já mandata que Testing não inventa um segundo motor de execução; ele **usa** o Execution Runtime já ratificado.

**Posição na cadeia já estabelecida:**

```
Governance (Admission/Certification, Governance §7/§11)
   │  solicita
   ▼
Validation & Certification §10.1 — request_certification(coordinate@version, target_level)
   │  invoca
   ▼
Testing  ◄── este documento
   │  executa Test Case[] via
   ▼
Execution Runtime (Dispatch, InvokeSkillStep, InvokeAgent — reutilizados, inalterados)
   │  produz
   ▼
Evidence[]  (Domain Model §13)
   │  alimenta
   ▼
Validation & Certification (score, threshold, Decision de Certificação)
```

**Fronteira exata:** Testing nunca decide se um Component está certificado — isso é, e permanece, autoridade exclusiva de Validation & Certification (§5-§6) e de Governance (§11, Certifier). Testing apenas **produz o insumo** (`Evidence[]`) sobre o qual aquela decisão já sabia, desde antes deste documento existir, que seria tomada.

---

## 2. Objetivos

| # | Objetivo | Como este documento o realiza |
|---|---|---|
| O1 | Fechar o forward-reference de Validation & Certification §10.1 (a caixa "Testing") | §7, §8, §9 |
| O2 | Fechar o forward-reference de Skill Architecture §7.3 (Testing de uma Skill = Executions sob Input variados) | §7.3 (generaliza, não reescreve) |
| O3 | Fechar o forward-reference de Agent Architecture §7.3 (Testing de um Agent = cenários comportamentais) | §7.3 (idem) |
| O4 | Formalizar `test_suite[]` — campo já usado informalmente como convenção de implementação, nunca antes normatizado por documento ratificado | §5 |
| O5 | Modelar Test Case, Test Suite, Test Result e Coverage inteiramente como composições de construtos já existentes, sem entidade nova | §4 |
| O6 | Demonstrar a sequência institucional de Quality Gates (Lint→...→Publication) como uma instância de Workflow já ratificado, não como mecanismo novo | §8.2 |
| O7 | Fechar o critério de Conformance de Standards §7 para `EvaluationMethod.kind = DYNAMIC` ("Requer Execution real do sujeito") — Testing é essa Execution | §6.3 |

---

## 3. Escopo

### 3.1 Pertence

Como Test Case é modelado; como um Test Suite é executado; como produz Evidence; como essa Evidence alimenta Certification; como se relaciona com Standards (Evaluation Method, Evidence Requirement) e Policy (enforcement em `applies_at=EXECUTION`); como reutiliza integralmente o Execution Runtime, `InvokeSkillStep` e `InvokeAgent`; a formalização de `test_suite[]`.

### 3.2 Não pertence — com justificativa individual

| Excluído | Justificativa técnica |
|---|---|
| **Framework de testes de qualquer linguagem** (pytest, JUnit, Vitest, Jest, NUnit, Go Test etc.) | Este documento especifica estrutura lógica institucional, não ferramenta. Nenhuma tecnologia é mandatada — mesma fronteira que Standards §3.2 já traça para "formato físico de serialização", deferido a Packaging & Distribution |
| **O algoritmo interno de uma Skill/Agent sob teste** | Já opaco por definição em Skill §9/Agent §9 ("processamento efetivo", "algoritmo de decisão") — Testing não abre essa caixa, apenas a invoca e observa seu resultado |
| **Decisão de conceder, suspender ou revogar Certificação** | Autoridade exclusiva de Validation & Certification §5-§6 e Governance §11 — Testing produz Evidence, nunca decide sobre ela |
| **Novo Runtime, Scheduler, Registry, Lifecycle, Manifest, mecanismo de descoberta, composição, execução, Policy ou Standards** | Nenhum destes é criado — prova exaustiva em §16 |
| **CI/CD, Observability de séries de testes, SDK de execução, Marketplace de test suites** | `[LACUNA proposital]`, deferida — ver §17 |

---

## 4. Modelo Conceitual

### 4.1 Prova de minimalidade — tabela de proveniência

**Este documento introduz zero entidades e zero Value Objects verdadeiramente novos.** As quatro construções que o mandato pede para modelar (`Test Case`, `Test Suite`, `Test Result`, `Coverage`) são, cada uma, resolvidas como reuso ou composição trivial — nunca como algo paralelo a uma entidade do Domain Model.

| Conceito pedido | Resolução | Provado em |
|---|---|---|
| **Test Result** | **É** `Evidence` (Domain Model §13) — nenhuma especialização, nenhum campo além do que Evidence já possui | §4.2 |
| **Coverage** | **É** `Metric` (Domain Model §2 #14, corrigido por RFC-DM-001 C4: `measures → {Component, Namespace}`) | §4.3 |
| **Test Case** | Value Object escopado ao Contract (mesma classe de `Slot`, `Step`, `Variable`) — habilitado por Kernel §9 Extension Model | §4.4 |
| **Test Suite** | `TestCase[]` — uma lista, não uma entidade própria; hospedada no campo aditivo `test_suite[]` do Manifest | §4.4, §5 |

| Conceito usado por Testing | Definido em |
|---|---|
| `Component`, `Manifest`, `Contract`, `Lifecycle` | Kernel §1-§3 |
| Extension Model (conteúdo interno type-specific) | Kernel §9 |
| `Constraint` | Kernel §2.10 |
| `Execution`, `Artifact`, `Evidence`, `Context`, `Context Snapshot` | Domain Model §2; RFC-DM-001 §3.2 |
| `Metric`, relação `measures` | Domain Model §2 #14; RFC-DM-001 §3.4 (C4) |
| `Decision`, `Decision Record`, autoridade de Certifier | Domain Model §14; Governance §2, §11 |
| `VersionedIdentifier`, `manifest_digest` | Identity & Namespace §4; Registry & Discovery §6 |
| `Registry.resolve()`, `search()` | Registry & Discovery §6.1-§6.2 |
| Pipeline de Certificação, L0-L4, Score por dimensão, Integrity | Validation & Certification §4-§6, §10.1 |
| `Slot`, `ResolveSlot`, `Assembly`, `EnumerateSlots` | Composition Architecture §4, §7; RFC-COMP-001 §4 |
| `Phase`, `Step`, `GATE_AUTO`, `FailurePolicy` | Workflow Architecture §4 |
| `Dispatch`, `Recover`, `Rollback` | Execution Architecture §7 |
| `NormativeRequirement`, `EvaluationMethod`, `EvidenceRequirement`, `ClassifyStandardChange` | Standards Architecture §4.6, §12.2 |
| `PolicyScope.applies_at = EXECUTION`, `enforcement_mode = BLOCKING` | Policy Architecture §5.2, §5.4 |
| `Template`, `Expand`, `ClassifyTemplateChange` | Template Architecture §11 |
| `InvokeSkillStep`, `ClassifySkillChange` | Skill Architecture §9 |
| `InvokeAgent`, `ClassifyAgentChange` | Agent Architecture §9 |

### 4.2 Test Result = Evidence

`[ESCOLHA DE DESIGN]`

**Motivação:** decidir como representar o resultado de uma execução de teste.

**Alternativa rejeitada:** criar uma entidade `TestResult` própria, com seus próprios campos de resultado, status e proveniência.

**Justificativa técnica:** Validation & Certification §3 já resolveu exatamente este problema para "Validation Result", pela mesma razão que se aplica aqui palavra por palavra: *"Validation Result = Evidence (Domain Model, especialização de Artifact). Satisfaz exatamente a definição existente... testar um componente é uma Execution; seu resultado é Evidence. Nenhuma nova especialização de Artifact é necessária."* Um `TestResult` seria, por definição, a mesma coisa com nome diferente — exatamente o anti-padrão que a Constitution (Regra Imutável nº10) e a própria revisão institucional anterior (achado C1, `Knowledge`/`Knowledge Component`) já penalizaram. **`Test Result` não existe como conceito à parte — é o nome coloquial para uma `Evidence` cujo `evidence_kind` é `TEST_RESULT`** (vocabulário já existente, Standards §4.6).

### 4.3 Coverage = Metric

`[ESCOLHA DE DESIGN]`

**Motivação:** decidir como representar cobertura de testes.

**Alternativa rejeitada:** criar uma entidade `Coverage` própria, ou um campo de primeira classe no Component Contract.

**Justificativa técnica:** Domain Model §2 entidade #14 já define `Metric` como "uma medida quantificável e recorrente sobre o estado de um Component" — e RFC-DM-001 §3.4 (C4) já corrigiu a relação `measures` para `Metric → {Component, Namespace}`, exatamente o alvo que Coverage precisa medir. Coverage é, portanto, **uma instância de `Metric`** (`metric.testing.coverage`, seguindo a convenção de nomenclatura já fixada em Identity & Namespace §5, `<namespace>/metric.<domínio>.<nome>`), nunca uma entidade nova. Coverage **MAY** informar a dimensão Functional do Score de Certificação (Validation & Certification §6) — mas **MUST NOT** redefinir a regra de "mínimo por dimensão, nunca média" já estabelecida ali (C2).

### 4.4 Test Case e Test Suite — Value Object escopado ao Contract, não entidade nova

`[ESCOLHA DE DESIGN]`

**Motivação:** decidir como representar um caso de teste individual e sua agregação em um Manifest.

**Alternativas rejeitadas:** (a) `TestCase` como entidade do Domain Model, exigindo RFC de emenda (Domain Model §18.1); (b) um `component_type` próprio para "teste".

**Justificativa técnica:** exatamente a mesma classe de construto que `Slot` (Composition §4), `Step` (Workflow §4), `Variable` (Template §4.2) e `Action`/reuso-de-`Step` (Agent §4.3) já ocupam — um Value Object escopado ao Contract de quem o declara, habilitado por Kernel §9, sem Identity própria, sem Lifecycle próprio, endereçado apenas através do Component que o contém.

```
TestCase {
  id
  kind: UNIT | INTEGRATION | CONTRACT | REGRESSION | GOLDEN | SNAPSHOT |
        SMOKE | ACCEPTANCE | PERFORMANCE | SECURITY | MUTATION      (§4.5)
  input: dict                                    (mesma forma de Step.params, Workflow §4)
  expected_output: dict?                          (comparado contra Artifact.content)
  constraint: Constraint?                         [Kernel §2.10 — reutilizado, tolerância/threshold]
  standard_ref: QualifiedRequirementIdentifier?   [Standards §5.1 — qual NR este caso evidencia]
  deterministic: boolean = true                   [mesmo campo conceitual de Template §4.2 e
                                                    Standards §4.6 EvaluationMethod.deterministic]
}
```

`test_suite: TestCase[]` é apenas uma lista — a mesma relação de cardinalidade 1:N que `templates[]` (Skill §5) e `actions[]` (Agent §5) já têm com seu Component hospedeiro. Nenhuma entidade "Test Suite" existe além dessa lista.

### 4.5 `TestKind` — classificação, nunca entidade

Os onze tipos pedidos são, cada um, **apenas um valor do enum `kind`** de `TestCase` — a mesma técnica já usada por `StepKind` (Workflow §4), `BindingSource` (Template §5.2) e `EvaluationMethod.kind` (Standards §4.6). Nenhum dos onze é uma entidade, um Component, ou exige mecanismo próprio:

| `TestKind` | Realização institucional | `EvaluationMethod.kind` correspondente (Standards §4.6) |
|---|---|---|
| `UNIT` | Execution de um Component isolado (`pinned_coordinate`, Composition §4 CP3), sem Assembly | `DYNAMIC` |
| `INTEGRATION` | Execution sobre uma `Assembly` resolvida (Composition §5) | `DYNAMIC` |
| `CONTRACT` | Verificação de que `inputs`/`outputs` (Kernel §2.4-§2.5) são respeitados pelo Artifact produzido | `DYNAMIC` ou `STATIC` (quando checável por inspeção de Manifest) |
| `REGRESSION` | Disparado por `ClassifyXChange` (Standards §12.2, Template §11.4, Skill §9.1, Agent §9.1) retornando MAJOR — reexecuta casos já existentes contra a nova versão | `DYNAMIC` |
| `GOLDEN` | `expected_output` é um `Artifact` anterior já `Retained` (Domain Model §8, ciclo de vida de Artifact) | `DYNAMIC` |
| `SNAPSHOT` | Caso particular de `GOLDEN` — mesma realização, nome de uso corrente | `DYNAMIC` |
| `SMOKE` | `expected_output = null` — `EvaluateResult` apenas confirma que a Execution produziu Artifact (Domain Model §12, "toda Execution que termina em Completed produz ao menos um Artifact") | `DYNAMIC` |
| `ACCEPTANCE` | Evidence funcional exigida por Validation & Certification §5, nível L2 | `DYNAMIC` |
| `PERFORMANCE` | `constraint` do tipo `RANGE`/temporal (Kernel §2.10, mesmo padrão já usado para `max_lines` em conteúdo institucional existente) | `DYNAMIC` |
| `SECURITY` | `standard_ref` aponta a um Standard de domínio de segurança (Standards Architecture, sem mecanismo novo) | `DYNAMIC` ou `ATTESTED` |
| `MUTATION` | Execution que avalia a sensibilidade do próprio `test_suite[]` a alterações deliberadas do Component — ainda uma Execution comum, Evidence comum | `DYNAMIC` |

`Lint` e `Type Check` (usados em §8.2) **não são `TestKind`** — são `EvaluationMethod.kind = STATIC` (Standards §4.6: "Inspeção do Manifest/Assembly sem execução... Verdict determinável sem Evidence externa"), produzindo Evidence `STRUCTURAL` diretamente da Validação Estrutural já existente (Kernel §8) — nenhuma Execution é despachada para eles, e nenhum `TestCase` é necessariamente instanciado (embora `TestCase.kind` pudesse, opcionalmente, ser estendido a incluir `STATIC_CHECK` sem que isso altere qualquer mecanismo — omitido aqui por não ser exigido pelo mandato).

---

## 5. Manifest

| Campo do Component Contract (Kernel §2) | Uso por Testing |
|---|---|
| Os quinze campos (identity...validation) | Inalterados — Testing nunca é, ele próprio, um `component_type`; é um mecanismo que opera sobre qualquer Component |
| `test_suite[]` | **Campo aditivo, habilitado por Kernel §9 Extension Model — este documento é quem formaliza o que já existia como convenção de implementação não ratificada.** Mesma classe de `templates[]` (Skill/Agent) e `actions[]` (Agent) — lista de `TestCase` (§4.4), nunca obrigatória |

`[ESCOLHA DE DESIGN]`

**Motivação:** decidir se `test_suite[]` é obrigatório para todo Component.

**Alternativa rejeitada:** exigir ao menos um `TestCase` para qualquer Component em `Active`.

**Justificativa técnica:** Kernel §3 já define `Active` sem exigir Evidence de teste — apenas Certificação (Validation & Certification, opcional e aditiva sobre Active) exige Evidence de Testing, e apenas a partir de L2. Forçar `test_suite[]` não vazio universalmente violaria Constitution (Simplicidade) e contradiria a fronteira Approval/Certification (Validation & Certification §1: "eventos independentes"). Um Component sem `test_suite[]` é válido em `Active`, apenas incapaz de progredir além de L1 (ver §11, CE8-CE9).

---

## 6. Contract

### 6.1 Como `test_suite[]` se relaciona com Inputs/Outputs

Um `TestCase.input` é validado contra `inputs` (Kernel §2.4), refinado quando presente por `INPUT Template` (Template §6.1, Skill §6.1) exatamente como qualquer invocação real seria. Um `TestCase.expected_output` é comparado contra o `Artifact` produzido, cuja forma é a mesma `outputs` (Kernel §2.5) que qualquer invocação real produziria — Testing não introduz uma segunda noção de forma de saída.

### 6.2 Como `constraint` participa da avaliação

`TestCase.constraint` reutiliza `Constraint` (Kernel §2.10) tal qual — o mesmo Value Object que já expressa `Variable.constraint` (Template §4.2) e `Step.timeout` (Workflow §4). Nenhuma gramática de constraint nova é introduzida para Testing.

### 6.3 Como `standard_ref` fecha Standards §7 para `EvaluationMethod.kind = DYNAMIC`

Standards Architecture §4.6 já definia: *"DYNAMIC | Requer Execution real do sujeito | TEST_RESULT, EXECUTION_TRACE | Verdict MUST ser indeterminado (§8.3) [na ausência de Evidence]."* Este documento fecha esse forward-reference: a "Execution real do sujeito" que produz a `Evidence` exigida por um `EvaluationMethod.kind = DYNAMIC` **é**, precisamente, uma execução de `TestCase` via `ExecuteTestCase` (§9), cujo resultado é empacotado como `Evidence` referenciando o `QualifiedRequirementIdentifier` declarado em `TestCase.standard_ref`. Nenhuma mudança a Standards Architecture — apenas a instanciação que aquele documento já previa precisar de um mecanismo concreto em algum lugar.

---

## 7. Modelo Operacional

| Operação | Definida em | Especialização para Testing |
|---|---|---|
| Admissão / aprovação | Governance §7 | Nenhuma — `test_suite[]` é conteúdo do Manifest, aprovado junto com o Component |
| Verificação estrutural | Kernel §8 | `test_suite[]` validado por Kernel §8 (bem-formação) — realiza `EvaluationMethod.kind = STATIC` |
| Registro / Descoberta | Registry & Discovery §5, §6.2 | Nenhuma — Testing não é descoberto por Capability; é invocado por quem já resolveu o Component |
| Dispatch/Execução | Execution §5, §7 | `Dispatch`/`InvokeSkillStep`/`InvokeAgent` — reutilizados, ver §9 |
| Certificação | Validation & Certification §5, §10.1 | Ver §7.3 — Testing é a caixa `Testing` do próprio §10.1 |
| Avaliação normativa | Standards §10 | `EvaluationMethod.kind = DYNAMIC` — ver §6.3 |
| Aplicabilidade | Policy §8, `applies_at = EXECUTION` | Uma execução de `TestCase` é uma `Execution` comum — sujeita a `BLOCKING` como qualquer outra (ver §11, CE6) |

### 7.3 Fechamento consolidado dos três forward-references

| Forward-reference | Texto original | Fechamento |
|---|---|---|
| Validation & Certification §10.1 | `Pipeline -> Testing : execute(test_suite)` / `Testing --> Pipeline : Evidence[] (via Execution)` | `ExecuteTestSuite(test_suite, component_ref) → Evidence[]` (§9) — assinatura idêntica |
| Skill Architecture §7.3 | *"Testing MUST consistir em uma ou mais Executions da própria Skill sob Input variados... via `EvaluationMethod` do tipo DYNAMIC"* | Instância de `ExecuteTestCase` com `component_type = Skill`, despachando via `InvokeSkillStep` (§9) — caso particular, não reescrito |
| Agent Architecture §7.3 | *"Testing MUST consistir em uma ou mais Executions do próprio Agent sob finalidades... por um Reviewer humano"* | Instância de `ExecuteTestCase` com `component_type = Agent`, despachando via `InvokeAgent` (§9); avaliação humana quando `TestCase.deterministic = false` ou o critério exigir julgamento (`EvaluationMethod.kind = ATTESTED`, Standards §4.6) — caso particular, não reescrito |

---

## 8. Fluxo

### 8.1 Fluxo de uma solicitação de Certificação (fecha Validation & Certification §10.1)

```
1. Owner solicita: request_certification(coordinate@version, target_level)      [Validation & Certification §10.1]
2. Certification Pipeline invoca: ExecuteTestSuite(manifest.test_suite, coordinate@version)   [§9]
   a. PARA CADA TestCase: ExecuteTestCase → EvaluateResult → CollectEvidence
3. Evidence[] retornado ao Pipeline                                             [Domain Model §13]
4. Pipeline calcula score por dimensão (Validation & Certification §6), aplica mínimo-por-dimensão (C2)
5. SE target_level = L4: Certifier humano solicitado (Validation & Certification §5, C3;
   generalizado por Agent §6.5 quando o sujeito é um Agent)
6. GrantCertification produz Decision(CertificationGrant) → Decision Record      [Governance §18]
7. Registry notificado (read-through, Registry & Discovery §12)
```

### 8.2 Quality Gates — instância de Workflow, não mecanismo novo

A sequência Lint → Type Check → Unit Test → Integration Test → Contract Test → Regression → Security → Coverage → Certification → Publication **é uma instância concreta de Workflow (Workflow Architecture §4)**, não uma entidade ou gramática nova:

```
Phase(id=static-checks, next=[dynamic-tests]):
   Step(id=lint,       kind=GATE_AUTO, slot=Slot(capability="lint"))                     # EvaluationMethod=STATIC
   Step(id=type-check, kind=GATE_AUTO, slot=Slot(capability="type-check"))               # EvaluationMethod=STATIC

Phase(id=dynamic-tests, next=[regression-security]):
   Step(id=unit,        kind=GATE_AUTO, slot=Slot(capability="testing.unit"))            # TestKind=UNIT
   Step(id=integration, kind=GATE_AUTO, slot=Slot(capability="testing.integration"))     # TestKind=INTEGRATION
   Step(id=contract,    kind=GATE_AUTO, slot=Slot(capability="testing.contract"))        # TestKind=CONTRACT

Phase(id=regression-security, next=[coverage-cert]):
   Step(id=regression, kind=GATE_AUTO, slot=Slot(capability="testing.regression"),
         failure_policy=FailurePolicy(ABORT))                                            # TS4
   Step(id=security,   kind=GATE_AUTO, slot=Slot(capability="testing.security"))         # TestKind=SECURITY

Phase(id=coverage-cert, next=[publication]):
   Step(id=coverage,      kind=GATE_AUTO,     slot=Slot(capability="testing.coverage"))  # §4.3, Metric
   Step(id=certification, kind=GATE_APPROVAL, role_class="role.governance-area.certifier")  # Validation & Certification §5

Phase(id=publication):
   Step(id=publish, kind=INVOCATION, slot=Slot(capability="registry.publish_version"))   # Registry & Discovery §5
```

Cada `Step(kind=GATE_AUTO)` acima é **exatamente** o que Workflow §4 já define: *"realizado como uma Execution que produz Evidence."* A Execution por trás de cada um desses Steps **é** `ExecuteTestCase`/`ExecuteTestSuite` (§9) — Testing Architecture fecha, aqui, o que era opaco dentro de um `GATE_AUTO`, sem alterar uma linha de Workflow Architecture. Nenhum novo `StepKind`, nenhuma nova `FailurePolicy`, nenhum novo tipo de Gate.

---

## 9. Algoritmos

**Nenhum algoritmo novo com lógica de decisão própria é introduzido.** Os cinco nomes pedidos são composição pura sobre algoritmos já ratificados.

```
ALGORITMO ExecuteTestCase(test_case, component_ref, requester_ns):
  resolved ← Registry.resolve(component_ref)                                    # Registry §6.1
  SE test_case precisa apenas de inspeção (EvaluationMethod.kind = STATIC):
     RETORNA (null, resolved.manifest)                                          # Kernel §8, sem Execution

  slot ← Slot(required_capability = resolved.manifest.capabilities[0],
              pinned_coordinate = component_ref)                                # Composition §4, CP3 — pin
  SE resolved.manifest.component_type = Skill:
     (exec, artifact) ← InvokeSkillStep(slot, test_case.input, ...)              # Skill §9 — verbatim
  SENÃO SE resolved.manifest.component_type = Agent:
     (exec, artifact) ← InvokeAgent(component_ref, goal=test_case.input, ...)    # Agent §9 — verbatim
  SENÃO:
     exec ← Dispatch(...)                                                       # Execution §7 — verbatim
     artifact ← exec.produced_artifacts[0]
  RETORNA (exec, artifact)


ALGORITMO EvaluateResult(test_case, artifact):
  SE test_case.expected_output É null:
     RETORNA (artifact ≠ null) ? PASS : FAIL                                     # SMOKE — Domain Model §12
  SE ¬SatisfiesConstraint(artifact, test_case.expected_output, test_case.constraint):  # Kernel §2.10
     RETORNA FAIL
  RETORNA PASS


ALGORITMO CollectEvidence(test_case, execution_ou_null, resultado):
  RETORNA Evidence.create(                                                       # Domain Model §13
     evidence_kind = MapTestKindToEvidenceKind(test_case.kind),                  # Standards §4.6, vocabulário reutilizado
     result = resultado,
     reproducible = test_case.deterministic,
     subject_execution = execution_ou_null?.instance_id,
  )


ALGORITMO ExecuteTestSuite(test_suite, component_ref, requester_ns):
  # ASSINATURA IDÊNTICA a Validation & Certification §10.1: execute(test_suite) → Evidence[]
  evidences ← []
  PARA CADA test_case EM test_suite:
     (exec, artifact) ← ExecuteTestCase(test_case, component_ref, requester_ns)
     resultado ← EvaluateResult(test_case, artifact)
     evidences.append(CollectEvidence(test_case, exec, resultado))
  RETORNA evidences


ALGORITMO GrantCertification(component_ref, evidences, target_level):
  # nenhuma lógica nova — invoca, sem alteração, a sequência já definida em
  # Validation & Certification §10.1: score por dimensão (§6), mínimo-por-dimensão (C2),
  # sign-off do Certifier humano quando target_level = L4 (C3; generalizado por Agent §6.5)
  RETORNA CertificationStore.grant(component_ref, target_level, evidences, ...)   # Validation & Certification §5-§6
```

### 9.1 Detecção de Breaking Change — reuso composto, sem novo classificador

Testing não define um sexto `ClassifyXChange`. `REGRESSION` (§4.5) é disparado quando `ClassifyStandardChange` (Standards §12.2), `ClassifyTemplateChange` (Template §11.4), `ClassifySkillChange` (Skill §9.1) ou `ClassifyAgentChange` (Agent §9.1) — já existentes, cada um aplicado ao seu próprio tipo — retornam `MAJOR`. Testing apenas consome o resultado desses quatro classificadores já ratificados; não introduz um quinto.

---

## 10. Diagramas

### 10.1 UML — Testing como mecanismo, não Component

```
┌─────────────────────────────────────────────────────────┐
│ «substrate» Testing                                        │  mesma classe arquitetural de
│   (não é Component — não tem Identity, Lifecycle próprio)  │  Composition Resolver, Scheduler,
└───────┬─────────────────────────────────────────┬──────────┘  Policy Evaluation Service
        │0..*                                     │1
        ▼                                         ▼
┌───────────────┐                          ┌─────────────┐
│ TestCase «VO» │──produces (via Execution)─►│ Evidence   │  [Domain Model §13 — reutilizado]
│  kind          │                          │ (Test Result)│
│  input         │                          └─────────────┘
│  expected_output│
│  constraint ───┼──► Constraint [Kernel §2.10]
│  standard_ref ──┼──► QualifiedRequirementIdentifier [Standards §5.1]
└───────┬───────┘
        │ hospedado em
        ▼
  Manifest.test_suite[]   ◄── campo aditivo, Kernel §9

┌─────────────┐
│ Metric «Ent.» │──measures──► Component   [Domain Model §2 #14; RFC-DM-001 C4]
│ (Coverage)    │
└─────────────┘
```

### 10.2 Sequência — `ExecuteTestSuite` dentro de uma solicitação de Certificação

```
Owner       CertificationPipeline    Testing         Registry       Execution/Skill/Agent Runtime
  │                 │                  │                 │                     │
  ├─request_certification(coord@v,L)─►│                  │                     │
  │                 ├─ExecuteTestSuite(test_suite, coord@v)──────────────────►│
  │                 │                  ├─Registry.resolve(coord@v)────────────►│
  │                 │                  │◄─manifest──────────────────────────────┤
  │                 │                  │  loop para cada TestCase              │
  │                 │                  ├─ExecuteTestCase──────────────────────►│
  │                 │                  │    (Dispatch | InvokeSkillStep | InvokeAgent — reutilizados)
  │                 │                  │◄─Execution + Artifact─────────────────┤
  │                 │                  ├─EvaluateResult (puro, sem I/O)         │
  │                 │                  ├─CollectEvidence──────────────────────►│ (Evidence.create)
  │                 │◄─Evidence[]───────┤                                       │
  │                 ├─score por dimensão, mínimo-por-dimensão (Validation & Certification §6)
  │                 ├─GrantCertification──►Decision(CertificationGrant)──►Decision Record
  │                 ├─notify Registry (read-through)
  │◄─CertificationGrant{level, evidence_refs}─┤
```

### 10.3 Estados

Testing **não possui Lifecycle próprio** — não é um Component (§1). Cada `TestCase` executado produz uma `Execution` sob o Lifecycle já existente (Domain Model §8, `Initiated→Running→Completed|Failed|Aborted`), sem exceção, e cada resultado é uma `Evidence` sob seu próprio ciclo já existente (Domain Model §13, `Captured→Validated→Retained`). Nenhum terceiro diagrama de estados é introduzido — mesma disciplina de Standards §11.4, Policy §12.4, Template §10.3, Skill §10.3, Agent §10.3.

---

## 11. Casos Extremos

| # | Caso | Tratamento |
|---|---|---|
| CE1 | Teste interrompido | A Execution do teste transita a `Aborted` (Domain Model §8) — mesma regra de qualquer interrupção externa, nenhum estado novo |
| CE2 | Timeout | `Constraint` violada (Kernel §2.10 anexada ao `Step` que despacha o teste, Workflow §4) → Execution transita a `Failed` — mesmo tratamento já definido em Execution §9 |
| CE3 | Execution Failed (o Component sob teste falha durante a Execution) | `CollectEvidence` ainda executa, registrando `result=FAIL` — o resultado nunca é engolido silenciosamente; a Evidence de falha é tão válida institucionalmente quanto a de sucesso |
| CE4 | Evidence inconsistente (diverge de uma Evidence anterior para o mesmo `coordinate@version`) | Regra de Integrity (Validation & Certification §6): o `manifest_digest` atual é a referência — qualquer Evidence associada a um digest divergente é lida como inválida, nunca reconciliada silenciosamente |
| CE5 | Coverage insuficiente | Coverage (`Metric`, §4.3) **MAY** informar a dimensão Functional do Score — mas só bloqueia avanço de nível se um `Standard`/`Policy` vinculado declarar um NR exigindo um `minimum_artifacts`/threshold explícito (Standards §4.6); ausência de threshold declarado nunca é bloqueio implícito |
| CE6 | Policy bloqueando teste (`enforcement_mode = BLOCKING`, `applies_at = EXECUTION`) | `ExecuteTestCase`, sendo uma Execution comum, **MUST NOT** prosseguir (Policy §5.4, §8) — mesmo mecanismo já previsto para qualquer dispatch, sem tratamento condicional de Testing |
| CE7 | Standard obrigatório vinculado ao Component sob teste | Avaliado via `TestCase.standard_ref` (§4.4, §6.3) sob `EvaluationMethod.kind = DYNAMIC` — sem novo mecanismo de Standards |
| CE8 | Skill sem testes (`test_suite[] = ∅`) | Válido em `Active` (Skill §11, S1) — apenas incapaz de progredir além de L1 (Validation & Certification §5, L2 exige Test Evidence) |
| CE9 | Agent sem testes | Idem CE8 — Agent §7.3 exige Evidence comportamental apenas a partir de L2/L4; ausência de `test_suite[]` não invalida o Agent, apenas trava seu nível de Certificação |
| CE10 | Workflow parcialmente testado (alguns Providers referenciados sem Test Evidence suficiente) | Validation & Certification §7, linha Workflow: *"Verificação de que todo Provider referenciado está em ≥L2"* — se algum Provider não atingiu L2 por falta de Testing, o próprio Workflow não avança na Certificação que dependa disso; nenhuma regra nova |
| CE11 | Template alterado | `ClassifyTemplateChange` (Template §11.4) classifica a mudança; se `MAJOR`, dispara `REGRESSION` (§9.1) antes de qualquer herança de Certificação (Validation & Certification §8, "MAJOR MUST recertificar integralmente") |
| CE12 | Breaking Change (qualquer `ClassifyXChange` retorna MAJOR) | **MUST** possuir Test Case do tipo `REGRESSION` reexecutado antes de a Certificação valer para a nova versão — TS4, §14 |
| CE13 | Retry | Sempre uma nova Execution (EX1, Execution §12; WF5, Workflow §12) — a Execution de um teste nunca é reaberta, mesma regra sem exceção |
| CE14 | Flaky Test | `TestCase.deterministic = false` (declarado ou inferido por reexecução divergente) → `Evidence.reproducible = false` — **MUST NOT**, isoladamente, justificar avanço a L4 (Validation & Certification C8; Standards ST22) |
| CE15 | Teste não determinístico (por natureza, ex.: dependente de timestamp/rede) | Mesmo tratamento de CE14 — `deterministic = false` é a declaração honesta, nunca corrigida silenciosamente para `true` |

---

## 12. Performance

| Recurso | Regra de cache/complexidade | Origem |
|---|---|---|
| Resolução de `component_ref` dentro de `ExecuteTestCase` | Cache indefinido | Registry §8 |
| `ResolveEffectiveTemplate`/`Expand` (quando o Component sob teste usa Templates) | Cache indefinido por `(template_digest[, bindings_digest])` | Template §12 |
| Resolução de Assembly para `TestKind=INTEGRATION` | Cache indefinido enquanto Slots não mudarem | Composition §10 |
| Effective Policy Set aplicável em `applies_at=EXECUTION` | Cache com TTL/invalidação por evento | Policy §15.1 |
| `ExecuteTestSuite` | O(número de `TestCase`) — mesma ordem de grandeza já aceita para `run_workflow` (Workflow §10) e `ready_steps` (Execution §10) | Workflow §10, Execution §10 |

**Nenhuma política de cache nova.** Testing herda inteiramente as políticas já normatizadas para cada mecanismo que reutiliza.

---

## 13. Eventos

**Testing não define nenhum tipo de evento próprio.** Tabela de eventos existentes aplicáveis:

| Evento | Origem | Ocorre quando |
|---|---|---|
| `StepDispatched` / `StepCompleted` / `StepFailed` | Execution §11 | Cada `ExecuteTestCase` que dispara uma Execution real |
| `AssemblyResolved` / `SlotUnsatisfied` | Composition §11 | Resolução do Component sob teste (`TestKind=INTEGRATION`) |
| `TemplateExpanded` | Template §16 | Expansão de Template do Component sob teste |
| `EffectiveRequirementsResolved` | Standards §16 | Avaliação de `standard_ref` de um `TestCase` |
| `EffectivePolicySetResolved` | Policy §16 | Avaliação de `applies_at=EXECUTION` sobre o teste |
| `StandardDefinitionValidated`/`PartialConformanceClaimed` | Standards §16 | Quando um `TestCase` produz Evidence para um Conformance Claim |

---

## 14. Regras Normativas (RFC 2119)

| # | Regra | Nível |
|---|---|---|
| TS1 | Todo Component SHOULD possuir `test_suite[]` não vazio | SHOULD |
| TS2 | Toda Skill que pretenda atingir Certificação ≥L2 MUST possuir ao menos um `TestCase` funcional (`kind ∈ {UNIT, ACCEPTANCE}`) | MUST |
| TS3 | Breaking Changes (qualquer `ClassifyXChange` = MAJOR) MUST possuir um `TestCase` do tipo `REGRESSION` reexecutado antes da Certificação valer para a nova versão | MUST |
| TS4 | L4 MUST exigir `reproducible = true` em toda Evidence que o justifique — Evidence com `reproducible = false` MUST NOT, isoladamente, justificar L4 | MUST / MUST NOT |
| TS5 | Toda `Evidence` produzida por Testing MUST ser preservada per a regra de retenção já existente (Domain Model §13; Standards §4.6, `retention`) | MUST |
| TS6 | `ExecuteTestCase` MUST despachar exclusivamente via `Dispatch`, `InvokeSkillStep` ou `InvokeAgent` — MUST NOT introduzir um caminho de execução paralelo | MUST / MUST NOT |
| TS7 | `Test Result` MUST ser modelado como `Evidence` — MUST NOT ser uma especialização nova de `Artifact` | MUST / MUST NOT |
| TS8 | `Coverage` MUST ser modelado como `Metric` — MUST NOT ser uma entidade nova | MUST / MUST NOT |
| TS9 | `test_suite[]` MUST ser conteúdo aditivo sob Kernel §9 Extension Model — MUST NOT tornar-se um décimo-sexto campo obrigatório do Component Contract | MUST / MUST NOT |
| TS10 | Um Component com `test_suite[] = ∅` MUST NOT ser tratado como inválido — apenas MUST NOT progredir além de Certificação L1 | MUST NOT |
| TS11 | Uma `Policy` com `enforcement_mode = BLOCKING` em `applies_at = EXECUTION` MUST impedir o dispatch de `ExecuteTestCase`, exatamente como impediria qualquer outra Execution | MUST |
| TS12 | Este documento MUST NOT mandatar tecnologia, linguagem ou framework de teste específico | MUST NOT |
| TS13 | `TestCase.deterministic = false` MUST propagar-se como `Evidence.reproducible = false` — MUST NOT ser silenciosamente tratado como determinístico | MUST / MUST NOT |

---

## 15. Integrações

| Documento | Como Testing o consome — sem alteração |
|---|---|
| **Kernel** | `test_suite[]` habilitado por §9; Validação Estrutural (§8) realiza `EvaluationMethod.kind=STATIC` |
| **Governance** | Certifier (§2, §11) permanece a única autoridade de concessão; Testing apenas alimenta |
| **Domain Model v1.1.0** | `Evidence` (§13), `Metric` (§2 #14), `Execution` (§8, §12) reutilizados sem alteração |
| **RFC-DM-001** | Context Snapshot (§3.2) obrigatório em toda Execution de teste, sem exceção |
| **Identity & Namespace** | Convenção `<ns>/metric.<domínio>.<nome>` (§5) usada por Coverage |
| **Registry & Discovery** | `resolve()` (§6.1) usado por `ExecuteTestCase`; nenhum índice novo |
| **Validation & Certification** | Fecha §10.1 (§7.3, §9); L0-L4 e Score (§5-§6) inalterados; Integrity (§6) referenciada em CE4 |
| **Composition** | `Slot`/`ResolveSlot`/`Assembly`/`EnumerateSlots` reutilizados para `TestKind=INTEGRATION` |
| **Workflow** | Quality Gates (§8.2) é instância de `Phase`/`Step`/`GATE_AUTO` — zero alteração |
| **Execution** | `Dispatch` é o único caminho de despacho real |
| **Standards** | Fecha `EvaluationMethod.kind=DYNAMIC` (§6.3); `ClassifyStandardChange` consumido em §9.1 |
| **Policy** | `applies_at=EXECUTION`/`BLOCKING` aplicado sem exceção a testes (CE6) |
| **Template Architecture** | `Expand`/`ClassifyTemplateChange` consumidos sem alteração |
| **Skill Architecture** | Fecha §7.3; `InvokeSkillStep`/`ClassifySkillChange` reutilizados |
| **Agent Architecture** | Fecha §7.3; `InvokeAgent`/`ClassifyAgentChange` reutilizados |
| **RFC-COMP-001** | `EnumerateSlots` consumido sem reabertura |

---

## 16. Validação Institucional

| Documento base | Resultado |
|---|---|
| Constitution | **PASS** — Regra Imutável nº10 justifica Test Result=Evidence e Coverage=Metric (nenhuma duplicação) |
| Kernel | **PASS** — `test_suite[]` habilitado por §9, sem 16º campo obrigatório |
| Governance | **PASS** — autoridade de Certifier intocada |
| Domain Model v1.1.0 | **PASS** — zero entidades novas; Evidence/Metric/Execution reutilizados |
| RFC-DM-001 | **PASS** — Context Snapshot obrigatório, sem exceção |
| Identity & Namespace | **PASS** — convenção de nomenclatura de Metric reutilizada |
| Registry & Discovery | **PASS** — `resolve()` reutilizado sem extensão |
| Validation & Certification | **PASS** — fecha §10.1 sem reescrevê-lo; L0-L4/Score/Integrity intocados |
| Composition | **PASS** — `Slot`/`ResolveSlot`/`Assembly` reutilizados |
| Workflow | **PASS** — Quality Gates é instância de Phase/Step, zero StepKind novo |
| Execution | **PASS** — `Dispatch` único caminho real de execução |
| Standards | **PASS** — fecha `EvaluationMethod.kind=DYNAMIC`; `ClassifyStandardChange` reutilizado |
| Policy | **PASS** — `applies_at=EXECUTION` aplicado sem exceção |
| Template Architecture | **PASS** — `Expand`/`ClassifyTemplateChange` reutilizados |
| Skill Architecture | **PASS** — fecha §7.3; `InvokeSkillStep` único caminho para Skill |
| Agent Architecture | **PASS** — fecha §7.3; `InvokeAgent` único caminho para Agent |
| RFC-COMP-001 | **PASS** — `EnumerateSlots` consumido sem reabertura |
| **Exige RFC?** | **NÃO** |

**Prova formal de que Testing não adiciona:**

| Item vedado pelo mandato | Verificação |
|---|---|
| Nova entidade | Nenhuma — `Test Result`=Evidence (§4.2), `Coverage`=Metric (§4.3) |
| Novo Value Object independente | Nenhum — `TestCase` reutiliza a mesma classe de `Slot`/`Step`/`Variable`; `Test Suite` é apenas uma lista |
| Novo Runtime / Scheduler / Dispatcher | Nenhum — `Dispatch`, `InvokeSkillStep`, `InvokeAgent` reutilizados tal qual (§9) |
| Nova Execution / Artifact / Evidence | Nenhuma — mesmas entidades, mesmo Lifecycle (§10.3) |
| Novo Lifecycle | Nenhum — Kernel §3 e Domain Model §8, sem exceção |
| Novo Registry / mecanismo de descoberta | Nenhum — `Registry.resolve()`/`search()` reutilizados (§15) |
| Novo mecanismo de Certificação | Nenhum — `GrantCertification` invoca Validation & Certification §10.1 sem alterá-lo |
| Novo mecanismo de Composição / Workflow / Execução | Nenhum — `Slot`, `Phase`/`Step`, `Dispatch` reutilizados |
| Novo mecanismo de Policy / Standards | Nenhum — `applies_at`, `EvaluationMethod` reutilizados sem novo valor de enum |
| Sistema de testes paralelo | Nenhum — Testing é, por definição (§1), a realização de uma caixa já contratada em outro documento |

---

## 17. Dependências Futuras

| Consumidor | O que consome | Estado |
|---|---|---|
| **Quality Gate / CI/CD** (futuro) | A sequência de §8.2 já é uma instância válida de Workflow — nenhuma extensão estrutural necessária, apenas orquestração operacional externa | Desbloqueado |
| **Observability & Provenance Storage** | Séries de `StepCompleted`/`StepFailed` de execuções de teste em escala | `[LACUNA proposital]` já declarada em Execution §14 |
| **Security Architecture** (futuro) | `TestKind=SECURITY` já reserva o slot; nenhuma extensão necessária quando aquele documento existir | Sem bloqueio |
| **SDK** (futuro) | Empacotamento de `test_suite[]` para distribuição — consome a forma canônica já fixada por Identity & Namespace §4.5 | Sem bloqueio |
| **Marketplace** (futuro) | Coverage (`Metric`) e Certification já fornecem sinal de confiança suficiente para listagem — nenhuma extensão necessária | Sem bloqueio |

---

## 18. Critério de Aceitação

### ✔ Checklist Institucional

| Critério do mandato | Status |
|---|---|
| Testing é especialização do processo de Validation já definido | ✔ §1, §7.3 |
| Nenhum framework de testes criado | ✔ §3.2, TS12 |
| Test Case, Test Suite, Test Result, Coverage modelados como composição de Execution/Artifact/Evidence/Validation/Certification | ✔ §4 |
| Onze tipos de teste como classificações, nunca entidades | ✔ §4.5 |
| Algoritmos (`ExecuteTestSuite`, `ExecuteTestCase`, `EvaluateResult`, `CollectEvidence`, `GrantCertification`) são pura composição | ✔ §9 |
| Quality Gates como instância de Workflow (Phase/Step) | ✔ §8.2 |
| Casos extremos exaustivos, incluindo os quinze pedidos | ✔ §11 |
| RFC2119 completo | ✔ §14 |
| Performance/Eventos sem novidade | ✔ §12, §13 |
| Integrações completas com Validation, Certification, Execution, Skill, Agent, Workflow, Standards, Policy | ✔ §15 |
| UML e diagramas de sequência | ✔ §10 |
| Prova de reutilização e tabela de proveniência completa | ✔ §4.1 |
| Tabela institucional de validação | ✔ §16 |
| Nenhuma alteração a documento anterior — RFC separada se necessário | ✔ §16 — nenhuma mudança encontrada; nenhuma RFC necessária |

### ✔ Confirmação Explícita

**Nenhum documento da base normativa congelada foi alterado.** Testing Architecture, como Skill e Agent Architecture antes dela, é construída inteiramente por prova de reutilização — as duas construções que poderiam parecer novas (`Test Result`, `Coverage`) foram resolvidas como identidade exata com `Evidence` e `Metric`, já existentes; as duas que exigiam alguma estrutura (`Test Case`, `Test Suite`) foram resolvidas como Value Object e lista, na mesma classe já sancionada por Kernel §9 para `Slot`/`Step`/`Variable`.

### ✔ Próximo Documento Desbloqueado

Com Testing Architecture fechando o último dos três forward-references (`Testing`, Validation & Certification §10.1) que ainda restava aberto na base normativa original, os próximos documentos — **Quality Gate/CI/CD operacional, Observability, Security, SDK, Marketplace** — podem agora ser escritos sem nenhuma dependência conceitual pendente sobre "como um teste efetivamente roda".

---

*Fim do documento. Versão 1.0.0.*
