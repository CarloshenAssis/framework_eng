# Testing Architecture
### Framework Eng — A Formalização de Geração, Execução, Cobertura e Regressão de Teste

*Versão 1.0.0 · Base normativa (congelada): Constitution · Kernel · Governance · Domain Model v1.1.0 · RFC-DM-001 · Identity & Namespace · Registry & Discovery · Validation & Certification · Composition · Workflow · Execution · Standards · Policy · Template Architecture · Skill Architecture · Observability Architecture · Agent Architecture · Organization & Tenancy*

> **Tese central, provada seção a seção:** Testing Architecture fecha três `[LACUNA proposital]` já pré-comprometidas — Standards §19 e Template §19 ("geração de casos de teste a partir de `Variable.constraint`"), e Skill §7.3 ("Testing MUST consistir em uma ou mais Executions... sob Input variados", descrito sem estrutura formal). Um `Test Case` é uma Execução comum (Domain Model §8) com `Input` declarado e uma comparação; um "Test Run" é um `Artifact` genérico agregando `Evidence` já definida (`evidence_kind = TEST_RESULT`, Standards §4.6); Cobertura e Regressão são **projeções de leitura efêmeras**, na mesma classe de `Trace`/`Provenance Chain` (Observability §4.2) — nunca persistidas, sempre recomputáveis.

---

## 1. Posição Arquitetural

`Testing` — já classificado por Validation & Certification §1 como *"a atividade que produz Evidence consumida por Verification/Validation"* — permanece exatamente essa atividade. Este documento não redefine Testing; formaliza **a estrutura** dessa atividade (o que é um caso de teste, como ele se relaciona a `Inputs`/`Outputs`/`Constraint`, como seus resultados se agregam, como cobertura e regressão são computadas) sobre mecanismos já ratificados.

### 1.1 Posição na cadeia já estabelecida

```
Manifest declara Constraint (Kernel §2.10)
   │
   ▼
GenerateTestCases (§9.1) — deriva Test Case por análise de fronteira/classe de equivalência
   │
   ▼
Test Case = Input + Assertion (Value Object, escopado ao Manifest — mesma classe de Template §4)
   │
   ▼
ExecuteTestSuite → Execution comum (Domain Model §8) por Test Case, correlacionada por test_run_id
   │  (mesma convenção de correlação já usada por orchestration_id — Execution §4)
   ▼
Evidence{evidence_kind=TEST_RESULT} (Standards §4.6 — já existente)
   │
   ▼
Test Run Report = Artifact genérico (mesma classe de Assembly/Execution Plan/Conformance Claim)
   │
   ├──► Certification L2 (Validation & Certification §5) — "Functional Validated"
   ├──► Coverage Report (projeção efêmera, §6.2)
   └──► Regression detection (projeção efêmera, §6.3, via Observability §9.2)
```

**Nenhum elo da cadeia é novo.** Este documento adiciona apenas a estrutura de `Test Case`/`Assertion` e os algoritmos que percorrem a cadeia — nunca um novo tipo de dado persistido além de `Test Run Report` (Artifact genérico, mesma classe já usada quatro vezes).

### 1.2 Fronteiras negativas (invioláveis)

| Fronteira | Regra |
|---|---|
| Testing não é Certificação | Um `Test Run Report` é **insumo** de Certificação (Validation & Certification §5); Testing Architecture não concede, suspende ou revoga nível algum |
| Testing não é Compliance | Testing avalia um Component contra sua própria especificação declarada (`Inputs`/`Outputs`/`Constraint`); Compliance (não ratificada) avaliaria conformidade contínua a normas externas — domínios distintos, sem sobreposição |
| Testing não cria novo Lifecycle | `Test Run` é uma `Execution` comum — Domain Model §8, sem exceção |
| Testing não cria novo mecanismo de orquestração | Suítes complexas (multi-step) reutilizam Workflow §4 integralmente — nenhum "Test Orchestrator" paralelo |
| Cobertura e Regressão não são persistidas | Projeções efêmeras, mesma classe de `Trace`/`Provenance Chain` (Observability §4.2) |

---

## 2. Objetivos

| # | Objetivo | Mecanismo |
|---|---|---|
| O1 | Fechar Standards §19 / Template §19 — geração de casos de teste a partir de `Constraint` | `GenerateTestCases` (§9.1) |
| O2 | Fechar Skill §7.3 — formalizar estrutura do que antes era só prosa ("Execution sob Input variados") | `TestCase`/`Assertion` (§5) |
| O3 | Definir Cobertura sem persistência nova | `CoverageReport`, projeção efêmera (§6.2) |
| O4 | Definir Regressão reutilizando `ClassifyChange` + Observability | `DetectRegression` (§9.4) |
| O5 | Fechar o critério operacional de L2 (Validation & Certification §5) | §6.4 |

---

## 3. Escopo

### 3.1 Pertence

Estrutura de `Test Case`/`Assertion`; derivação automática de casos de teste a partir de `Constraint`; execução de suíte (simples, via Executions correlacionadas; complexa, via Workflow); `Test Run Report`; Cobertura; Regressão; fechamento do critério de L2.

### 3.2 Não pertence — com justificativa

| Excluído | Justificativa |
|---|---|
| Concessão de nível de Certificação | Validation & Certification §5 — Testing produz insumo, nunca decide |
| Framework de execução física de testes (runner, sandbox) | Opaco ao Framework — mesma fronteira já aplicada ao "processamento efetivo" de uma Skill (Skill §6.3); Kernel §9, Contract declara o quê, nunca o como |
| Testes de carga/performance como categoria normativa separada | Expressável como `Assertion.kind = PREDICATE` com `Constraint` de limite — reuso direto, sem categoria nova |
| Ambientes de teste físicos | Já reservados por Identity §3.1/§8 (`env.<environment>`) e Organization §17; este documento apenas os referencia |

---

## 4. Modelo Conceitual

### 4.1 Tabela de proveniência — prova de minimalidade

| Conceito usado por Testing | Natureza | Já definido em |
|---|---|---|
| `Execution` | **Reutilizado, sem alteração** | Domain Model §8 |
| `Evidence`, `evidence_kind = TEST_RESULT` | **Reutilizado — já enumerado** | Standards §4.6 (`EvidenceRequirement.evidence_kind`) |
| `Artifact` genérico (Test Run Report) | **Reutilizado, mesma classe de Assembly/Execution Plan/Conformance Claim/EPS** | Domain Model §2 #7 |
| `Constraint` | **Reutilizado como fonte de derivação de casos de teste** | Kernel §2.10 |
| `Variable`, `Placeholder`, `VariableBindingSet` | **Reutilizado para Input parametrizado** | Template Architecture §4.2, §11.2 |
| `Predicate<X>` | **Reutilizado — 4ª aplicação do padrão (`Predicate<Context>` em Workflow, Composition, Policy → agora `Predicate<Artifact>`)** | Workflow §4; Composition §4; Policy §5.2 |
| `Decision`/`Decision Record` | **Reutilizado para `Assertion.kind = HUMAN_REVIEW`** | Domain Model §14 |
| `EvaluationMethod.kind = DYNAMIC` | **Reutilizado — já definia exatamente esta necessidade** | Standards §4.6 |
| Correlação via `orchestration_id`-style Context field | **Reutilizado, novo nome de campo (`test_run_id`), mesmo mecanismo** | Execution Architecture §4 |
| `Workflow` (Phase/Step/Gate) | **Reutilizado para suítes complexas** | Workflow §4 |
| `trace()`/`provenance()`/`query_events()` | **Reutilizado para Regressão** | Observability §7.1, §9.2, §9.5 |
| `ClassifySkillChange`/`ClassifyTemplateChange`/`ClassifyStandardChange` | **Reutilizado, mesmo padrão de composição de classificadores** | Skill §9.1; Template §11.4; Standards §12.2 |
| `RequirementIdentifier`/`TemplateIdentifier` (padrão de qualificação) | **Reutilizado — 3ª aplicação** | Standards §5.1; Template §5.1 |

**Nenhuma linha introduz entidade ou relação nova.** `TestCase`, `Assertion`, `CoverageReport`, `RegressionReport` são Value Objects/projeções efêmeras — mesma classificação já usada nos documentos anteriores.

### 4.2 Test Case e Assertion — Value Objects escopados ao Manifest

```
TestCase {                                          [Value Object — campo test_suite[] do Manifest]
  local_id      : TestCaseIdentifier                [§5.1]
  input         : VariableBindingSet | Literal      [Template §11.2, ou literal conforme Kernel §2.4]
  assertion     : Assertion
  kind          : FUNCTIONAL | REGRESSION | BEHAVIORAL
  covers        : [QualifiedRequirementIdentifier]?  (vínculo a NRs — base de Cobertura, §6.2)
  generated_by  : MANUAL | DERIVED                    (§9.1 — se derivado de Constraint)
}

Assertion {
  kind           : EXACT_MATCH | SCHEMA_MATCH | PREDICATE | HUMAN_REVIEW
  expected_value : Literal?
  predicate      : Predicate<Artifact>?               (4ª aplicação do padrão)
  constraint     : Constraint?                          [Kernel §2.10 — reutilizado]
  reviewer_role_class : RoleClass?                       (obrigatório se kind=HUMAN_REVIEW — Governance §2)
}
```

---

## 5. Estrutura

### 5.1 `TestCaseIdentifier`

```
TestCaseIdentifier ::= <local-id>
QualifiedTestCaseIdentifier ::= <owner-coordinate> "@" <version> "#test." <local-id>
```

**3ª aplicação** do mesmo padrão de fragmento qualificado — após `RequirementIdentifier` (Standards §5.1) e `TemplateIdentifier` (Template §5.1). Encoding herda Identity §4.4, sem extensão.

### 5.2 Test Run Report

```
TestRunReport (Artifact) {                          [mesma classe de Assembly/Execution Plan/Conformance Claim/EPS]
  test_run_id       : InstanceIdentifier             [Identity §4.2 — ULID já existente]
  subject           : VersionedIdentifier
  results           : [ (QualifiedTestCaseIdentifier, Outcome, EvidenceId) ]
  outcome           : PASS | FAIL | INCONCLUSIVE
  started_at, ended_at : Timestamp
  context_snapshot_ref : ArtifactId                   [RFC-DM-001 §3.2]
}

Outcome ::= PASS | FAIL | PENDING_HUMAN_REVIEW | FLAKY_DETECTED
```

`INCONCLUSIVE` (nível de `TestRunReport`) ocorre quando qualquer `TestCase` resulta em `PENDING_HUMAN_REVIEW` ou `FLAKY_DETECTED` — mesma disciplina já aplicada por Standards §8.3 (`indeterminate` obrigatoriamente vazio para um Conformance Claim válido): um Test Run Report **MUST NOT** declarar `PASS` global com resultados pendentes.

---

## 6. Geração, Execução, Cobertura, Regressão e Certificação Operacional

### 6.1 Geração de Test Case a partir de Constraint — fechamento de Standards §19 / Template §19

`[ESCOLHA DE DESIGN]`

**Motivação:** decidir como derivar casos de teste automaticamente, sem exigir que todo Test Case seja autorado manualmente.

**Alternativas rejeitadas:** exigir que 100% dos Test Cases sejam declarados manualmente (`generated_by = MANUAL` sempre).

**Justificativa técnica:** Kernel §2.10 (`Constraint`) e Template §4.2 (`Variable.constraint`) já carregam informação suficiente para técnicas clássicas de análise de fronteira e classe de equivalência — um `Constraint` do tipo "intervalo [1,100]" já contém, implicitamente, os valores de fronteira (0, 1, 50, 100, 101) que uma suíte de teste deveria cobrir. Derivar esses casos automaticamente (`generated_by = DERIVED`) evita exigir autoria manual redundante de algo já implícito no Contract — coerente com Constitution (Automação sempre que segura).

**Precedentes arquitetônicos:** geração de casos por análise de fronteira a partir de schema/tipo declarado é técnica padrão de *property-based testing* (QuickCheck, Hypothesis) — aqui aplicada sobre `Constraint` já existente, não sobre um novo formato de especificação.

### 6.2 Cobertura — projeção efêmera, nunca persistida

`[ESCOLHA DE DESIGN]`

**Motivação:** decidir se `CoverageReport` deveria ser um `Artifact` persistido (como `TestRunReport`) ou uma projeção de consulta.

**Alternativas rejeitadas:** modelar `CoverageReport` como `Artifact` produzido por uma "Execution de cálculo de cobertura".

**Justificativa técnica:** exatamente o mesmo raciocínio já formalizado em Observability §4.2 para `Trace`/`Provenance Chain` — Cobertura é **inteiramente recomputável** a partir de dados já persistidos (`TestRunReport.results[].covers` cruzado com `resolve_effective_requirements`, Standards §12.1), sem nenhuma perda de informação se nunca for persistida. Persisti-la criaria uma cópia derivada redundante, sujeita a divergir da fonte — exatamente o problema que a mesma decisão já evitou em Observability.

```
CoverageReport {                                     [Value Object efêmero — nunca persistido]
  subject                  : VersionedIdentifier
  requirements_covered     : [QualifiedRequirementIdentifier]
  requirements_uncovered   : [QualifiedRequirementIdentifier]
  capabilities_covered     : [CapabilitySignature]
  coverage_ratio           : Float
}
```

### 6.3 Regressão — reuso de `ClassifyChange` + Observability

Regressão é definida formalmente como: *um `TestCase` cujo `Outcome` era `PASS` em `prev_version` e é `FAIL` em `next_version`, sem que `ClassifySkillChange`/`ClassifyTemplateChange` (Skill §9.1, Template §11.4) tenha classificado a mudança como `MAJOR`*.

```
RegressionReport {                                    [Value Object efêmero]
  subject      : Coordinate
  prev_version, next_version : SemVer
  regressions  : [ (QualifiedTestCaseIdentifier, expected_class, actual_break) ]
}
```

`[ESCOLHA DE DESIGN]`

**Motivação:** decidir se Regressão precisa de um algoritmo de detecção próprio, independente de `ClassifyChange`.

**Alternativas rejeitadas:** um classificador de regressão isolado, sem referência à classificação SemVer já calculada.

**Justificativa técnica:** uma regressão **é**, por definição, uma quebra de compatibilidade não anunciada — exatamente o que `ClassifySkillChange` (Skill §9.1) já existe para prever. Se um teste que passava em uma versão `PATCH` ou `MINOR` falha na seguinte, isso **é** evidência de que a classificação da mudança estava **errada** — o algoritmo de Regressão, portanto, não precisa de lógica própria de detecção; precisa apenas **cruzar** o `TestRunReport` com o resultado já calculado de `ClassifySkillChange`. Isso evita duplicar a lógica de "o que é uma mudança quebrada", já resolvida.

### 6.4 Fechamento do critério operacional de L2

Validation & Certification §5 já declara L2 ("Functional Validated") como *"Testing cobre Inputs/Outputs declarados, incl. modos de falha"* — este documento fecha o critério exato de suficiência, **sem alterar aquele documento**:

> **Regra (TS9):** L2 **MUST** exigir `TestRunReport.outcome = PASS` **E** `CoverageReport.coverage_ratio` cobrindo 100% dos `NormativeRequirement` com `normative_keyword ∈ {MUST, MUST_NOT}` cujo `target.applies_to ∈ {EXECUTION, ARTIFACT}` — Test Cases com `Assertion.kind = HUMAN_REVIEW` pendente **MUST NOT** satisfazer esse critério (mesma disciplina de Standards ST18, `indeterminate` bloqueia o Claim).

---

## 7. Modelo Operacional

**Serviço:** nenhum serviço de substrato novo. `ExecuteTestSuite` reutiliza integralmente o `Scheduler` já definido por Execution Architecture §5 — cada `TestCase` é despachado exatamente como um `Step` (Workflow §4), correlacionado por `test_run_id` (mesmo mecanismo de `orchestration_id`, Execution §4, novo nome de campo, zero mecanismo novo).

```
execute_test_suite(subject: VersionedIdentifier) → TestRunReport
  PRE:  subject.manifest.test_suite ≠ ∅
  POST: uma Execution por TestCase, correlacionada por test_run_id;
        Evidence{evidence_kind=TEST_RESULT} produzida por Execution;
        TestRunReport materializado como Artifact imutável

compute_coverage(test_run_report) → CoverageReport            # puramente derivado, §6.2
detect_regression(coordinate, prev_v, next_v) → RegressionReport   # puramente derivado, §6.3
```

---

## 8. Fluxo de Execução

```
1. GenerateTestCases(manifest) deriva casos a partir de Constraint (opcional, §9.1)          [§6.1]
2. subject.manifest.test_suite = TestCase[] (manuais + derivados)
3. execute_test_suite(subject):
   a. test_run_id ← novo ULID                                                                [Identity §4.2]
   b. PARA CADA TestCase EM test_suite (paralelizável — sem dependência entre casos):
      i.   Context{test_run_id, test_case_id} montado; Context Snapshot capturado              [RFC-DM-001 §3.2]
      ii.  Execution do subject sob TestCase.input (via Template.BindVariables se aplicável)   [Template §11.2]
      iii. Artifact produzido comparado contra TestCase.assertion
      iv.  SE assertion.kind = HUMAN_REVIEW: Decision solicitada a Role                         [Domain Model §14]
      v.   Evidence{TEST_RESULT} produzida
   c. TestRunReport materializado (Artifact)
4. compute_coverage(report) — sob demanda                                                      [§6.2]
5. detect_regression(...) — sob demanda, cruza com ClassifySkillChange                          [§6.3]
6. TestRunReport.outcome=PASS + Coverage completa ⟹ satisfaz critério de L2                     [§6.4]
```

---

## 9. Algoritmos

### 9.1 Geração de casos de teste a partir de Constraint

```
ALGORITMO GenerateTestCases(manifest):
  casos ← []
  PARA CADA input_field EM manifest.inputs:
     PARA CADA constraint EM (input_field.constraint ∪ TemplateVariableConstraints(manifest)):
        SE constraint.kind = RANGE(min, max):
           casos += TestCase(input={field: min-1}, assertion=REJECT, generated_by=DERIVED)
           casos += TestCase(input={field: min},   assertion=ACCEPT, generated_by=DERIVED)
           casos += TestCase(input={field: max},   assertion=ACCEPT, generated_by=DERIVED)
           casos += TestCase(input={field: max+1}, assertion=REJECT, generated_by=DERIVED)
        SE constraint.kind = ENUM(valores):
           PARA CADA v EM valores: casos += TestCase(input={field: v}, assertion=ACCEPT, generated_by=DERIVED)
           casos += TestCase(input={field: fora_do_enum}, assertion=REJECT, generated_by=DERIVED)
        SE constraint.kind = REQUIRED ∧ ¬default_value:
           casos += TestCase(input={field: ausente}, assertion=REJECT, generated_by=DERIVED)
  RETORNA casos
  # TERMINAÇÃO: número finito de constraints, número finito de casos por classe — sem recursão
```

### 9.2 Execução de suíte

```
ALGORITMO ExecuteTestSuite(subject):
  test_run_id ← NovoULID()
  resultados ← []
  PARA CADA tc EM subject.manifest.test_suite EM PARALELO:            # sem dependência entre casos
     ctx ← Context{test_run_id, test_case_id: tc.local_id}
     snap ← CaptureContextSnapshot(ctx)                                # RFC-DM-001 §3.2
     exec ← Dispatch(subject, input=Resolve(tc.input), ctx=snap)       # Execution §7
     artifact ← exec.produced_artifact
     outcome ← EvaluateAssertion(tc.assertion, artifact)
     ev ← Evidence(evidence_kind=TEST_RESULT, substantiates=exec)      # Standards §4.6
     resultados += (tc.local_id, outcome, ev.id)
  outcome_global ← SE ∃ r EM resultados: r.outcome ∈ {FAIL}: FAIL
                    SENÃO SE ∃ r: r.outcome ∈ {PENDING_HUMAN_REVIEW, FLAKY_DETECTED}: INCONCLUSIVE
                    SENÃO: PASS
  RETORNA Artifact(TestRunReport, {test_run_id, subject, results: resultados, outcome: outcome_global})

FUNÇÃO EvaluateAssertion(assertion, artifact):
  CASO assertion.kind:
     EXACT_MATCH:  RETORNA (artifact = assertion.expected_value) ? PASS : FAIL
     SCHEMA_MATCH: RETORNA Conforms(artifact, assertion.expected_value) ? PASS : FAIL
     PREDICATE:    RETORNA Evaluate(assertion.predicate, artifact) ? PASS : FAIL   # determinístico, puro
     HUMAN_REVIEW: RETORNA PENDING_HUMAN_REVIEW   # aguarda Decision de Role — Domain Model §14
```

### 9.3 Cobertura

```
ALGORITMO ComputeCoverage(report):
  eps ← PolicyEval.resolve_effective_policy_set(report.subject, ..., plane=EXECUTION)  # Policy §11.1
  nrs_aplicaveis ← ∪ StandardResolver.resolve_effective_requirements(b.standard, b.level)   # Standards §12.1
                    PARA b EM eps.bindings
  cobertos ← ∪ tc.covers PARA (tc,_,_) EM report.results
  RETORNA CoverageReport{
     requirements_covered: cobertos ∩ nrs_aplicaveis,
     requirements_uncovered: nrs_aplicaveis \ cobertos,
     coverage_ratio: |cobertos ∩ nrs_aplicaveis| / |nrs_aplicaveis|
  }
  # TERMINAÇÃO: conjuntos finitos, sem I/O além de leituras já garantidas terminantes
```

### 9.4 Regressão

```
ALGORITMO DetectRegression(coordinate, prev_v, next_v):
  prev_report ← Observability.query_events(filter={subject=coordinate@prev_v, kind=TestRunReport})  # Observability §9.5
  next_report ← ExecuteTestSuite(coordinate@next_v)
  classe ← Skill.ClassifySkillChange(prev_manifest, next_manifest)                                     # Skill §9.1
  regressoes ← []
  PARA CADA (tc_id, outcome_next, _) EM next_report.results:
     outcome_prev ← Lookup(prev_report, tc_id)
     SE outcome_prev = PASS ∧ outcome_next = FAIL ∧ classe ≠ MAJOR:
        regressoes += (tc_id, classe, outcome_next)
  RETORNA RegressionReport{coordinate, prev_v, next_v, regressions: regressoes}
```

---

## 10. Diagramas

### 10.1 UML — proveniência

```
┌────────────────────────┐
│ Manifest                │  templates[], test_suite[]   [Kernel §9 — habilita ambos]
└────┬────────────────────┘
     │0..*
     ▼
┌────────────┐   1    ┌────────────┐
│ TestCase   │────────►│ Assertion  │
│ «VO»       │         │ «VO»       │
│ covers[] ──┼──► QualifiedRequirementIdentifier  [Standards §5.1]
└─────┬──────┘         └────────────┘
      │ dispatch (Execution §5)
      ▼
┌────────────┐  produces  ┌──────────┐  substantiates  ┌───────────────────┐
│ Execution   ├───────────►│ Artifact │◄─────────────────┤ Evidence           │
└────────────┘            └──────────┘  evidence_kind=  │  TEST_RESULT       │
                                          TEST_RESULT     │  [Standards §4.6]  │
                                                          └─────────┬─────────┘
                                                                    │ agrega
                                                                    ▼
                                                          ┌───────────────────┐
                                                          │ TestRunReport      │  «Artifact» genérico
                                                          └─────────┬─────────┘
                                                       ┆ projeção efêmera     ┆ projeção efêmera
                                                       ▼                       ▼
                                              CoverageReport «VO»    RegressionReport «VO»
```

### 10.2 Sequência — execução completa e cobertura

```
Owner          TestingSvc         Execution           Observability         StandardResolver
   │                │                  │                    │                     │
   ├─ExecuteTestSuite(subject)────────►│                    │                     │
   │                ├─PARA CADA TestCase (paralelo)──────►  │                     │
   │                │    Context+Snapshot, Dispatch          │                     │
   │                │◄───Artifact, Evidence(TEST_RESULT)──── │                     │
   │◄─TestRunReport──┤                                        │                     │
   │                                                                                │
   ├─ComputeCoverage(report)──────────►│                    │                     │
   │                ├─resolve_effective_policy_set/requirements ──────────────────►│
   │                │◄─NRs aplicáveis───────────────────────────────────────────────┤
   │◄─CoverageReport─┤                                                              │
   │                                                                                │
   ├─DetectRegression(coord, v1, v2)──►│                    │                     │
   │                ├─query_events(prev report)──────────────►│                     │
   │                │◄─prev_report──────────────────────────┤                     │
   │                ├─ClassifySkillChange (Skill §9.1)                             │
   │◄─RegressionReport                                                             │
```

### 10.3 Estados

`TestRunReport` segue o Lifecycle de `Artifact` já definido (`Generated → Verified → Retained | Superseded`, Domain Model §8). Cada `Execution` de teste segue o Kernel Lifecycle de Execution sem exceção. **Nenhum estado novo.**

---

## 11. Casos Extremos

| # | Caso | Tratamento |
|---|---|---|
| T1 | `Assertion.kind = PREDICATE` não determinística (retorna resultados diferentes em execuções idênticas) | `Outcome = FLAKY_DETECTED` — **MUST NOT** ser silenciosamente reexecutada até passar; sinaliza defeito de Test Case (predicado deveria ser puro, mesma exigência de Template §7 TP2) |
| T2 | `HUMAN_REVIEW` pendente sem `Role` disponível | `PENDING_HUMAN_REVIEW` — mesma semântica de bloqueio (não bypass) já estabelecida em Agent §11/E10 |
| T3 | Regressão detectada entre versão `PATCH` | Sinal de que `ClassifySkillChange` classificou incorretamente — **MUST** ser tratado como defeito de versionamento, não apenas de código (§6.3) |
| T4 | `TestCase.covers` referencia `RequirementIdentifier` aposentado (tombstone, Standards §5.3) | `CoverageReport` **MUST** excluir o requisito do denominador — mesma regra de resolução de tombstone já aplicada em Standards §7.4 |
| T5 | Suíte de teste vazia (`test_suite = []`) | Válido estruturalmente, `coverage_ratio = 0` se houver NRs `MUST` aplicáveis — bloqueia L2 por TS9, não é erro de definição |
| T6 | Dois `TestCase`s com o mesmo `local_id` | Rejeitado na validação estrutural (mesma unicidade já exigida para `RequirementIdentifier`/`TemplateIdentifier`) |
| T7 | Teste de comportamento multi-turno de um Agent | Expresso como Workflow cujos Steps invocam o Agent repetidamente — reuso de Workflow §4, sem mecanismo de Testing próprio para esse caso (§1.1) |
| T8 | `GenerateTestCases` produz caso redundante a um já autorado manualmente | Deduplicado por `(input, assertion)` equivalente — comportamento aceitável e não bloqueante; redundância em teste não é o mesmo defeito arquitetural que redundância em Component (Governance §7) |

---

## 12. Performance

| Operação | Cache/Complexidade |
|---|---|
| `ExecuteTestSuite` | Paralelizável — `TestCase`s são independentes por construção (sem dependência topológica declarada); O(N) Executions concorrentes |
| `ComputeCoverage` | Cacheável indefinidamente para `TestRunReport` em estado terminal (imutável) — mesma prova de Observability §12.1 |
| `DetectRegression` | O(N) sobre o menor dos dois conjuntos de resultados; `query_events` segue o regime de consistência já normatizado (Observability §6.2) |
| `GenerateTestCases` | O(Constraints declaradas) — determinístico, sem I/O |

Nenhuma política de cache ou complexidade nova além da reaplicação já estabelecida.

---

## 13. Eventos

| Evento | Ocorre quando |
|---|---|
| `TestSuiteExecuted(subject, test_run_id, outcome)` | `ExecuteTestSuite` concluída |
| `FlakyTestDetected(test_case_id)` | T1 |
| `HumanReviewPending(test_case_id)` | T2 |
| `CoverageComputed(subject, ratio)` | `ComputeCoverage` |
| `RegressionDetected(coordinate, test_case_id)` | `DetectRegression` encontra quebra |
| `TestCasesGenerated(subject, count)` | `GenerateTestCases` |

Mesma classe operacional já usada por todos os documentos anteriores — não são Domain Model Event Entities.

---

## 14. Regras Normativas (RFC 2119)

| # | Regra | Nível |
|---|---|---|
| TS1 | `TestCase`/`Assertion` MUST ser Value Objects escopados ao Manifest, sem Identity própria além de `TestCaseIdentifier` local | MUST |
| TS2 | `Assertion.predicate` MUST ser puro e determinístico, salvo `kind = HUMAN_REVIEW` | MUST |
| TS3 | `TestRunReport` MUST ser imutável uma vez materializado | MUST |
| TS4 | `TestRunReport.outcome = PASS` MUST NOT ser declarado com qualquer resultado `PENDING_HUMAN_REVIEW` ou `FLAKY_DETECTED` pendente | MUST NOT |
| TS5 | `CoverageReport`/`RegressionReport` MUST NOT ser persistidos como Artifact — projeções efêmeras apenas | MUST NOT |
| TS6 | Teste marcado `FLAKY_DETECTED` MUST NOT ser reexecutado automaticamente até passar | MUST NOT |
| TS7 | `DetectRegression` MUST reutilizar `ClassifySkillChange`/`ClassifyTemplateChange`, nunca lógica de detecção paralela | MUST |
| TS8 | `GenerateTestCases` MUST derivar exclusivamente de `Constraint` já declarado — MUST NOT inferir critério não presente no Manifest | MUST / MUST NOT |
| TS9 | L2 (Validation & Certification §5) MUST exigir `outcome=PASS` e cobertura de 100% dos NRs `MUST`/`MUST_NOT` aplicáveis a EXECUTION/ARTIFACT | MUST |
| TS10 | Testing MUST NOT conceder, suspender ou revogar Certificação — apenas produz insumo | MUST NOT |

---

## 15. Integrações

| Documento | Contrato de integração |
|---|---|
| **Kernel** | `Constraint` (§2.10) fonte de geração; `Inputs`/`Outputs` (§2.4-§2.5) alvo de asserção |
| **Governance** | `HUMAN_REVIEW` produz `Decision`/`Decision Record` sob autoridade já delegada (§8) |
| **Domain Model v1.1.0** | `TestRunReport` = Artifact genérico; `Evidence{TEST_RESULT}` já existente |
| **RFC-DM-001** | Context Snapshot obrigatório em cada Execution de teste |
| **Identity & Namespace** | `TestCaseIdentifier` qualificado, mesmo padrão de fragmento (3ª aplicação) |
| **Registry & Discovery** | Nenhuma interação direta — Testing opera sobre instâncias, não definições (mesma fronteira de Observability §1.2) |
| **Validation & Certification** | Fecha o critério operacional de L2 (§6.4); `EvaluationMethod.kind=DYNAMIC` (§4.6) plenamente operacionalizado |
| **Composition** | Nenhuma alteração — testes operam sobre um `subject` já resolvido |
| **Workflow** | Suítes complexas (multi-step) reutilizam Phase/Step integralmente (T7) |
| **Execution** | `Dispatch` reutilizado sem alteração; correlação via `test_run_id`, mesmo mecanismo de `orchestration_id` |
| **Standards** | Fecha §19 (`GenerateTestCases`); `covers[]` referencia `QualifiedRequirementIdentifier` |
| **Policy** | `resolve_effective_policy_set` usado por `ComputeCoverage` para determinar NRs aplicáveis |
| **Template Architecture** | `VariableBindingSet` usado para `TestCase.input` parametrizado; fecha §19 |
| **Skill Architecture** | Fecha §7.3 (estrutura formal do que antes era descrito em prosa); `ClassifySkillChange` reutilizado por Regressão |
| **Observability** | `query_events`/`trace()` fonte primária de `DetectRegression`; fecha dependência declarada em Skill §17 |
| **Agent Architecture** | Testes comportamentais de Agent usam `Assertion.kind=HUMAN_REVIEW`, mesma exigência de coautorização humana já formalizada para L4 |
| **Organization & Tenancy** | Ambientes de teste isolados via `env.<environment>` já reservado |

---

## 16. Validação Institucional

| Documento base | Resultado |
|---|---|
| Constitution | **PASS** |
| Kernel | **PASS** |
| Governance | **PASS** |
| Domain Model v1.1.0 | **PASS** — zero entidades/relações/estados |
| RFC-DM-001 | **PASS** |
| Identity & Namespace | **PASS** |
| Registry & Discovery | **PASS** |
| Validation & Certification | **PASS** — fecha critério de L2 sem redefinir a escada |
| Composition | **PASS** |
| Workflow | **PASS** — suítes complexas reutilizam Phase/Step |
| Execution | **PASS** |
| Standards | **PASS** — fecha §19 |
| Policy | **PASS** |
| Template Architecture | **PASS** — fecha §19 |
| Skill Architecture | **PASS** — fecha §7.3, §17; `ClassifySkillChange` reutilizado |
| Observability Architecture | **PASS** — fonte de `DetectRegression` |
| Agent Architecture | **PASS** — `HUMAN_REVIEW` alinhado à exigência de L4 |
| Organization & Tenancy | **PASS** |
| **Exige RFC?** | **NÃO** |

---

## 17. Dependências Futuras

| Consumidor | O que consome | Estado |
|---|---|---|
| **Packaging & Distribution Architecture** (próximo) | `TestRunReport`/`CoverageReport` como critério de empacotamento (ex.: não distribuir Component sem L2) | Desbloqueado |
| **Compliance Architecture** (downstream, não ratificada) | `Evidence{TEST_RESULT}` como uma das fontes de `EvaluationMethod` quando ratificada | Sem bloqueio |

---

## 18. Critério de Aceitação

### ✔ Checklist Institucional

| Critério | Status |
|---|---|
| Geração de casos de teste formalizada | ✔ §6.1, §9.1 |
| Execução de suítes | ✔ §6, §9.2 |
| Cobertura sem persistência nova | ✔ §6.2, §9.3 |
| Regressão sem detector paralelo | ✔ §6.3, §9.4 |
| Fechamento do critério operacional de L2 | ✔ §6.4, TS9 |
| Zero entidade/relação/estado/mecanismo de orquestração novo | ✔ §16 |
| UML, sequência, algoritmos, casos extremos, RFC2119 | ✔ §9-§14 |
| Nenhuma RFC necessária | ✔ §16 |

### ✔ Confirmação Explícita

Nenhum documento da base normativa foi alterado. `TestCase`/`Assertion` são Value Objects (mesma classe de `Capability`/`Phase`/`NormativeRequirement`); `TestRunReport` é `Artifact` genérico; Cobertura e Regressão são projeções efêmeras (mesma classe de `Trace`/`Provenance Chain`); Regressão reutiliza os classificadores de mudança já existentes em vez de introduzir um novo. **Três `[LACUNA proposital]` fecham-se neste documento (Standards §19, Template §19, Skill §7.3) sem alteração retroativa a nenhum dos três.**
