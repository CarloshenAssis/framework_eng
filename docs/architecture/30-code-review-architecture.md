# Code Review Architecture
### Framework Eng — A Elaboração Completa do Gate 3 (Implementation Review)

*Versão 1.0.0 · Base normativa (congelada): Constitution · Kernel · Governance · Domain Model v1.1.0 · RFC-DM-001 · Identity & Namespace · Registry & Discovery · Validation & Certification · Composition Architecture · Workflow Architecture · Execution Architecture · Standards Architecture · Policy Architecture · Template Architecture · Skill Architecture · Observability Architecture · Organization & Tenancy Architecture · Packaging & Distribution Architecture · Compliance Architecture v1.1.0 · RFC-COMP-001 · Agent Architecture (23) · Testing Architecture (24) · Quality Gate Architecture (25) · Security Architecture (26) · Development Lifecycle Architecture (27) · Project Architecture (28) · Documentation Architecture (29)*

> **Tese central deste documento, provada seção a seção:** Code Review não é um mecanismo novo — é a elaboração completa de algo que Quality Gate Architecture já nomeou, mas nunca especificou por dentro: *"Implementation Review | GATE_APPROVAL, informado por Evidence de uma Skill de análise... | Decision Record + Evidence de insumo"* (Quality Gate §4.3, Gate 3). Este documento faz, para o Gate 3, exatamente o que Testing Architecture já fez para a caixa "Testing" de Validation & Certification §10.1, e o que Security Architecture já fez para os Gates de segurança de Quality Gate — fecha um forward-reference, sem reabrir o documento que o contém. `Review Request`, `Review Session`, `Finding`, `Recommendation`, `Approval`, `Request Changes`, `Comment` e `Review Evidence` são, cada um, nomes para algo que Domain Model, Workflow, Execution, Standards, Policy, Testing ou Security **já** definem — nunca uma nona/décima entidade.

---

## 1. Posição Arquitetural

### 1.1 O forward-reference que faltava fechar

```
Quality Gate Architecture §4.3, Gate 3 — Implementation Review:
  "GATE_APPROVAL, informado por Evidence de uma Skill de análise de código
   (ex.: core/skill.static-analysis.code-review, Reference Cycle 1) invocada
   via InvokeSkillStep como insumo à Decision | Decision Record, informado
   por Evidence | ATTESTED (decisão), DYNAMIC (insumo)"
```

Esta linha já existia, integralmente, antes deste documento. O que faltava era: como um `Finding` é estruturado; como sua severidade deriva de Standards/Policy; o que distingue Approval de Request Changes; como Re-review funciona. **Este documento fecha exatamente essas lacunas, sem alterar Quality Gate §4.3.**

### 1.2 Prova de que o conteúdo já roda de verdade

Diferente de todo documento anterior, Code Review Architecture não precisa argumentar que seu mecanismo *poderia* funcionar — ele já **rodou**, nesta mesma sessão institucional:

- `core/skill.static-analysis.code-review@1.0.0` (Reference Cycle 1) já produz `Artifact.content.findings[]` com a forma exata que este documento formaliza (`file`, `line`, `severity`, `category`, `description`, `suggestion`).
- `.claude/agents/code-reviewer.md` (Caminho B, tradução executável) foi **invocado de verdade** e produziu um veredito `REQUEST_CHANGES`, citando evidência concreta, verificando autoria (regra de não-autoaprovação, §11), e sinalizando risco alto para revisão humana — exatamente o fluxo que §5, §10 e §11 formalizam.
- O Runtime (`runtime/skill/runtime.py`, `_stub_processing`) já detecta o mesmo padrão de segredo (`sk-live-`) usado como exemplo real em Security Architecture §4.5.

Este documento nomeia um comportamento **já observado**, não um comportamento hipotético.

### 1.3 Posição na cadeia recursiva de nomeação (recapitulação)

```
Workflow ⊂ Quality Gate ⊂ Security ⊂ Development Lifecycle ⊂ Project ⊂ Documentation
                    │
                    └── Gate 3 (Implementation Review) ──► Code Review Architecture ◄── este documento
                         (mesma técnica de elaboração já usada por Testing e Security
                          para outras caixas/Gates deixados abertos)
```

### 1.4 Fronteiras negativas (invioláveis)

| Fronteira | Regra |
|---|---|
| Code Review não cria novo processo de aprovação | `Approval`/`Request Changes` **são** `Decision Record{grant\|deny}` já definido por Workflow §6.1 para `GATE_APPROVAL` |
| Code Review não cria nova Governance | Autoridade de quem pode aprovar/rejeitar é exatamente Governance §2/§8 (Reviewer, não-concentração) |
| Code Review não cria novo mecanismo de Testing | `Review Evidence` **é** `Evidence` (Domain Model §13); a Execução que a produz **é** `ExecuteTestCase`/`ExecuteGate` já existentes |
| Code Review não cria novo mecanismo de Security | Findings de segurança encontrados durante Code Review são, sem exceção, Security Findings já catalogados (Security Architecture §4.4-§4.5) |
| Code Review não cria novo mecanismo de Quality Gate | Code Review **é** a elaboração de um Gate já catalogado (Gate 3) — nunca um Gate paralelo |

---

## 2. Objetivos

| # | Objetivo | Mecanismo |
|---|---|---|
| O1 | Fechar o forward-reference de Quality Gate §4.3, Gate 3 (Implementation Review) | §5, §13 |
| O2 | Definir `Finding`/`Recommendation`/`Comment` como uma única estrutura reutilizada, já em produção real | §7 |
| O3 | Derivar as seis severidades de Standards (`normative_keyword`) + Policy (`enforcement_mode`, `precedence_level`) — nenhum eixo de julgamento novo | §8 |
| O4 | Definir Approval/Request Changes como o mesmo `Decision Record{grant\|deny}` de Workflow §6.1 | §10, §11 |
| O5 | Definir Re-review como recorrência (EX1/WF5), nunca reabertura | §12 |
| O6 | Provar que Registry e Documentation registram o resultado sem mecanismo novo | §22 |
| O7 | Dar ao Framework Eng um processo oficial de revisão de código (**Objetivo Prático**) | §25 |

---

## 3. Escopo

### 3.1 Pertence

Estrutura de Review Request/Session/Finding/Evidence; derivação de Severity; fluxo Approval/Request Changes/Re-review; os dezesseis critérios mínimos de revisão e sua proveniência; registro em Registry/Documentation.

### 3.2 Não pertence — com justificativa individual

| Excluído | Justificativa técnica |
|---|---|
| Ferramenta específica de code review (GitHub PR, Gerrit, GitLab MR) | Mesma fronteira já traçada por Testing §3.2 e Development Lifecycle §3.2 — nenhuma tecnologia mandatada |
| O algoritmo interno de "como julgar se um código é bom" | Opaco a este documento — mesma fronteira já estabelecida para o processamento efetivo de uma Skill/Agent (Skill §9; Agent §3.2, AG12) |
| Critérios de estilo de linguagem específica | Delegado ao Standard de code-quality vinculado (ex.: `core/standard.code-quality.review-baseline`, já existente) — este documento não define regras de estilo, apenas onde elas vivem |
| Um novo nível de Certificação para "código revisado" | Já coberto — Review é a fase 12 do Development Lifecycle, anterior e independente de Certification (fase 13); nenhum nível novo é necessário |

---

## 4. Modelo Conceitual

### 4.1 Prova de minimalidade — tabela de proveniência

**Este documento introduz zero entidades, zero Value Objects, zero algoritmos com corpo lógico próprio, zero estado novo.**

| Conceito pedido | Resolução | Provado em |
|---|---|---|
| **Review Request** | Conteúdo de `Context` (Domain Model §2 #5) — mesma técnica já usada para `Goal` (Agent §4.2) | §5 |
| **Review Session** | `Execution` (Domain Model §8) do Step que realiza o Gate 3 | §5 |
| **Finding** | Item estruturado dentro de `Artifact.content` — mesma forma já usada por Security Finding (Security §4.4) | §7 |
| **Recommendation** | `Finding` com `severity ∈ {Info, Suggestion}` e `suggestion` preenchido | §7 |
| **Comment** | `Finding` com `severity = Info`, `category = comment`, sem `standard_ref` | §7 |
| **Severity** | Enum de classificação sobre `Finding` — mesma técnica de `TestKind` (Testing §4.5) | §8 |
| **Approval** | `Decision(outcome=grant)` — Workflow §6.1 | §10 |
| **Request Changes** | `Decision(outcome=deny)` — Workflow §6.1 | §11 |
| **Review Evidence** | `Evidence` (Domain Model §13), `evidence_kind ∈ {TEST_RESULT, ANALYSIS_OUTPUT, ATTESTATION}` (Standards §4.6) | §9 |

| Conceito usado por Code Review | Definido em |
|---|---|
| `Context` (base de Review Request) | Domain Model §2 #5; Agent §4.2 |
| `Execution` (base de Review Session) | Domain Model §8 |
| `Artifact.content` (base de Finding) | Domain Model §2 #7; Security §4.4 |
| `Decision`, `Decision Record`, `grant\|deny` | Domain Model §14; Workflow §6.1 |
| `NormativeRequirement`, `normative_keyword`, `Strength()` | Standards §4.3, §12.1 |
| `enforcement_mode`, `precedence_level` | Policy §5.4; Standards §4.2 |
| `ExecuteGate`, `EvaluateGate`, Gate 3 (Implementation Review) | Quality Gate §4.3, §9 |
| `InvokeSkillStep`/`InvokeAgent` | Skill §9; Agent §9 |
| `ExecuteTestCase`, `CollectEvidence` | Testing §9 |
| Governança §2 (não-autoaprovação), §6.5 (Agent) | Governance §2; Agent §6.5 |
| `ClassifyXChange` (base de Breaking Changes) | Standards §12.2; Template §11.4; Skill §9.1; Agent §9.1 |
| `Coverage` (=`Metric`) | Testing §4.3 |
| `Constraint` (base de limite de complexidade/diff) | Kernel §2.10 |
| Gate 16 (Documentation Review) | Quality Gate §4.3 |
| EX1/WF5 (base de Re-review) | Execution §12; Workflow §12 |
| Documentação como classe hand-authored/Artifact | Documentation Architecture §5 |

**Nenhuma linha introduz entidade, relação ou estado novo.**

---

## 5. Fluxo de Revisão

```
Review Request (Context)                                              [Domain Model §2 #5; Agent §4.2]
      │
      ▼
Review Session (Execution — dispatch do Gate 3, Quality Gate §9)       [ExecuteGate]
      │
      ├──► invoca Skill/Agent de análise (InvokeSkillStep/InvokeAgent)  [Skill §9; Agent §9]
      │        │
      │        ▼
      │   Artifact.content.findings[] produzido                        [Finding — §7]
      │
      ▼
CollectEvidence → Review Evidence (Evidence)                            [Testing §9]
      │
      ▼
EvaluateReviewOutcome(findings) → PASS | BLOCK                          [Quality Gate §9; Workflow §6.1]
      │
      ├── PASS  → ApproveReview  → Decision(grant) → Approval           [§10]
      └── BLOCK → RequestChanges → Decision(deny)  → Request Changes    [§11]
                        │
                        ▼
                  (mudança) → TriggerReReview → nova Review Session      [§12, EX1/WF5]
```

---

## 6. Critérios de Revisão

Os dezesseis critérios pedidos, cada um mapeado a mecanismo já existente — nenhum critério introduz avaliação nova:

| # | Critério | Realização institucional | Provido por |
|---|---|---|---|
| 1 | **Arquitetura** | Gate 1 (Architecture Review) — já catalogado | Quality Gate §4.3 |
| 2 | **Design** | Gate 2 (Design Review) — já catalogado | Quality Gate §4.3 |
| 3 | **Legibilidade** | `NormativeRequirement` de um Standard de code-quality (ex.: `core/standard.code-quality.review-baseline`, já existente neste repositório) | Standards §4.3 |
| 4 | **Complexidade** | Idem — NR do mesmo Standard, ou `Constraint(RANGE)` sobre tamanho/profundidade (Kernel §2.10) | Standards §4.3; Kernel §2.10 |
| 5 | **Segurança** | Security Validation (Development Lifecycle fase 11) — Security Architecture inteira | Security Architecture |
| 6 | **Performance** | `TestKind=PERFORMANCE` / Gate 14 (Performance Budget) | Testing §4.5; Quality Gate §4.3 |
| 7 | **Testabilidade** | Regra TS2/TS3 (Testing §14) — presença e adequação de `test_suite[]` | Testing Architecture |
| 8 | **Manutenibilidade** | Idem Legibilidade/Complexidade — NR do Standard de code-quality | Standards §4.3 |
| 9 | **Compatibilidade** | `compatibility` (Kernel §2.13) + `ClassifyXChange` | Kernel §2.13 |
| 10 | **Breaking Changes** | `ClassifyXChange = MAJOR` → Governance §10 + Development Lifecycle fase 5 (RFC) + MIGRATION GUIDE (Documentation §5, linha 17) | Governance §10; Development Lifecycle §6 |
| 11 | **Standards** | Conformance Claim (Standards §8.1) | Standards Architecture |
| 12 | **Policies** | Effective Policy Set (Policy §9) | Policy Architecture |
| 13 | **Quality Gates** | O próprio catálogo de 18 Gates — Code Review não substitui os demais, apenas coordena o Gate 3 | Quality Gate §4.3 |
| 14 | **Cobertura de testes** | `Coverage` = `Metric` (Testing §4.3) | Testing Architecture |
| 15 | **Dependências** | `dependencies` (Kernel §2.6) + Dependency Audit (Gate 13, Security §4.5 #2) + Cycle Detection (Kernel §7) | Kernel §2.6, §7; Security §4.5 |
| 16 | **Documentação** | Gate 16 (Documentation Review) + Documentation Architecture inteira | Quality Gate §4.3; Documentation Architecture |

Cada critério produz, quando aplicável, um ou mais `Finding` (§7) — nenhum critério tem seu próprio mecanismo de avaliação distinto do já catalogado.

---

## 7. Classificação de Findings

`[ESCOLHA DE DESIGN]`

**Motivação:** decidir como representar um achado de revisão sem introduzir uma entidade nova, dado que o mandato explicitamente pede `Finding`, `Recommendation` e `Comment` como três construtos nomeados.

**Alternativa rejeitada:** três estruturas de dados distintas (`Finding`, `Recommendation`, `Comment`), cada uma com seu próprio schema.

**Justificativa técnica:** Security Architecture §4.4 já resolveu este problema exatamente — *"um 'achado' de segurança não é uma Evidence — é o conteúdo bruto que uma Skill/Agent... produz como Artifact... já em produção institucional"*. Este documento generaliza essa mesma estrutura, sem alteração de forma, para qualquer domínio de revisão (não apenas segurança):

```
Finding {                                              [item dentro de Artifact.content — Domain Model §2 #7]
  file          : Text
  line          : Integer?
  severity      : Severity                              [§8 — enum, não entidade]
  category      : Text                                  (ex.: "style", "architecture", "complexity",
                                                            "security", "testability", "comment")
  description   : Text
  suggestion    : Text?
  standard_ref  : QualifiedRequirementIdentifier?        [Standards §5.1 — quando aplicável]
}
```

**`Recommendation` ≡ `Finding` com `severity ∈ {Info, Suggestion}` e `suggestion` preenchido.** **`Comment` ≡ `Finding` com `severity = Info`, `category = "comment"`, sem `standard_ref`.** Nenhuma das duas exige um campo além dos já declarados acima — a diferença entre os três nomes é inteiramente de **severidade e conteúdo**, nunca de estrutura.

**Precedente real, não hipotético:** esta é exatamente a forma já produzida por `core/skill.static-analysis.code-review@1.0.0` (`findings[]` com `file`, `line`, `severity`, `category`, `description`, `suggestion`) — este documento não inventa o schema, **nomeia** o que já está em produção.

---

## 8. Severidades

Seis níveis pedidos, derivados — não inventados — da combinação de três dimensões já existentes: `Strength(normative_keyword)` (Standards §12.1), `enforcement_mode` (Policy §5.4) e `precedence_level` (Standards §4.2).

| Severity | Condição (derivação, não julgamento novo) | Fonte |
|---|---|---|
| **Info** | Nenhum `NormativeRequirement` associado — observação pura | — |
| **Suggestion** | Idem Info, com `Finding.suggestion` preenchido | — |
| **Minor** | `NR` com `normative_keyword ∈ {SHOULD, SHOULD_NOT}` não satisfeito — `Strength() = 2` | Standards §12.1 |
| **Major** | `NR` com `normative_keyword ∈ {MUST, MUST_NOT}` não satisfeito (`Strength() = 4`), mas `enforcement_mode ≠ BLOCKING` (ou ausente) | Standards §12.1; Policy §5.4 |
| **Critical** | `Strength() = 4` ∧ `enforcement_mode = BLOCKING` ∧ `Standard.precedence_level ≠ GLOBAL` | Standards §4.2, §12.1; Policy §5.4 |
| **Blocker** | `Strength() = 4` ∧ `enforcement_mode = BLOCKING` ∧ `Standard.precedence_level = GLOBAL` | Standards §4.2, §12.1; Policy §5.4 |

**Nenhum eixo de julgamento novo.** A tabela acima é uma **função determinística** de três valores que Standards e Policy já calculam — nunca uma segunda régua de severidade paralela. `Blocker`, notavelmente, é exatamente a severidade que `core/skill.static-analysis.code-review` já atribui, na prática, a um segredo em texto plano (`sk-live-`) — um NR de segurança tipicamente `MUST_NOT`, `precedence_level=GLOBAL`, `enforcement_mode=BLOCKING` (Security Architecture §4.5, controle #1, Secrets Management).

### 8.1 Algoritmo de derivação (não julgamento — cálculo)

Ver `ClassifyFindingSeverity` (§14) — função total sobre as três dimensões, determinística, sem exceção.

---

## 9. Evidências

`Review Evidence` **é** `Evidence` (Domain Model §13), produzida por `CollectEvidence` (Testing §9) — nenhuma extensão. `evidence_kind` (Standards §4.6) já cobre os três casos relevantes:

| Situação | `evidence_kind` |
|---|---|
| Achado de uma Skill de análise estática (ex.: `code-review`) | `ANALYSIS_OUTPUT` |
| Achado de uma execução real de teste (ex.: falha de contrato revelada durante Review) | `TEST_RESULT` |
| Julgamento humano ou de Agent sob `Assertion`/`EvaluationMethod.kind=ATTESTED` | `ATTESTATION` |

A Evidence referencia a `Execution` que a produziu (`subject_execution`, Domain Model §13) — nunca duplica o conteúdo do `Finding`, apenas o confirma institucionalmente, mesma disciplina já aplicada por Security §4.4 e Documentation §7 (DOC5, nunca duplicar).

---

## 10. Aprovação

`Approval` **é**, sem extensão, `Decision(outcome=grant)` produzindo `Decision Record` — exatamente o sub-fluxo já definido por Workflow §6.1 para `Step[kind=GATE_APPROVAL]`: *"Decision solicitada ao Role → Decision Record{grant|deny} → PASS"*.

**Regra de não-autoaprovação (RC5, §21):** o `Role` que aprova **MUST NOT** ser o mesmo que o `owner` (Kernel §2.3) do Component sob revisão — mesma regra já estabelecida por Governance §2 (*"ninguém pode ser simultaneamente Reviewer e Owner do mesmo componente"*) e generalizada por Agent Architecture §6.5 para Roles ocupados por Agent. Nenhuma exceção, humano ou Agent.

**Precedente real:** `.claude/agents/code-reviewer.md`, ao ser invocado nesta sessão, verificou explicitamente autoria antes de decidir — comportamento já observado, não apenas normatizado aqui.

---

## 11. Rejeição

`Request Changes` **é**, sem extensão, `Decision(outcome=deny, cites=findings)` — mesmo sub-fluxo de Workflow §6.1, ramo `BLOCK`. A `Decision Record` resultante **MUST** referenciar (Domain Model §14, `references`) todo `Finding` com `severity ∈ {Critical, Blocker}` que motivou a rejeição — nunca uma rejeição sem causa nomeada (mesma exigência de transparência já normatizada em toda a série, ex.: Standards ST8 para `PARTIAL`).

**Precedente real:** o mesmo `.claude/agents/code-reviewer.md`, na invocação já realizada nesta sessão, produziu veredito `REQUEST_CHANGES` citando o achado concreto (segredo em texto plano) como motivo — exatamente o comportamento este parágrafo normatiza.

---

## 12. Re-review

Re-review **MUST** ser uma **nova** `Review Session` (nova `Execution`) — nunca reabertura da Execution anterior, já terminal. Mesma regra sem exceção: EX1 (Execution §12), WF5 (Workflow §12), já aplicada por Testing (Retry, CE13), Quality Gate (CE4) e Security (CE12).

```
ALGORITMO TriggerReReview(prior_session, updated_component_ref):
  nova_review_request ← RequestReview(updated_component_ref, ...)      # §5, §14
  nova_sessao ← ExecuteReviewSession(nova_review_request)               # §5, §14 — Execution nova, EX1
  RETORNA nova_sessao
```

**Regra (RC6, §21):** um Re-review **SHOULD** verificar, no mínimo, todo `Finding` de `severity ∈ {Critical, Blocker}` da sessão anterior — mesma técnica conceitual de `TestKind=REGRESSION` (Testing §4.5), aplicada como foco de atenção, não como um algoritmo de comparação automática obrigatório (o julgamento de "está corrigido" permanece opaco, mesma fronteira de §3.2).

---

## 13. Fluxo Operacional

```
1. Component/mudança atinge a fase 12 (Review) do Development Lifecycle           [Documento 27, §6]
2. RequestReview(component_ref, requester) → Review Request (Context)              [§5]
3. ExecuteReviewSession → ExecuteGate(Gate 3) → Execution                          [Quality Gate §9]
   a. ResolveSlot(capability="static-analysis.code-review" ou "review.decision")   [Composition §7]
   b. InvokeSkillStep (Skill de análise) e/ou InvokeAgent (Agent decisório)        [Skill §9; Agent §9]
   c. Artifact.content.findings[] produzido, cada um classificado por §8           [§7, §8]
4. CollectEvidence → Review Evidence                                               [Testing §9]
5. EvaluateReviewOutcome(findings) → PASS | BLOCK                                   [Quality Gate §9]
6. ApproveReview (PASS) ou RequestChanges (BLOCK)                                   [§10, §11]
7. SE Request Changes: mudança revisada → TriggerReReview                          [§12]
8. Registry/Documentation registram o resultado (§22) — nenhum mecanismo novo
```

---

## 14. Algoritmos

**Nenhum algoritmo novo com lógica de decisão própria.**

```
ALGORITMO RequestReview(component_ref, requester):
  RETORNA Context{ review_subject: component_ref, requested_by: requester }   # mesma técnica de Goal, Agent §4.2


ALGORITMO ExecuteReviewSession(review_request):
  RETORNA ExecuteGate(step_implementation_review, review_request)              # Quality Gate §9 — verbatim


ALGORITMO ClassifyFindingSeverity(finding, nr_ref, policy_ref):
  SE nr_ref = null:
     RETORNA (finding.suggestion ≠ null) ? SUGGESTION : INFO
  forca ← Strength(nr_ref.normative_keyword)                                    # Standards §12.1 — verbatim
  SE forca < 4: RETORNA MINOR
  SE policy_ref = null ∨ policy_ref.enforcement_mode ≠ BLOCKING:
     RETORNA MAJOR
  SE nr_ref.standard.precedence_level = GLOBAL:
     RETORNA BLOCKER
  RETORNA CRITICAL


ALGORITMO EvaluateReviewOutcome(findings):
  bloqueantes ← [f PARA f EM findings SE f.severity ∈ {CRITICAL, BLOCKER}]
  RETORNA (bloqueantes = ∅) ? PASS : BLOCK                                       # Workflow §6.1 — verbatim


ALGORITMO ApproveReview(review_session, findings, decided_by):
  ASSERT decided_by ≠ Registry.resolve(review_session.review_request.review_subject).manifest.owner  # RC5
  SE EvaluateReviewOutcome(findings) = PASS:
     RETORNA Decision(outcome=grant).produces(DecisionRecord)                   # Approval — §10
  RETORNA RequestChanges(review_session, findings, decided_by)


ALGORITMO RequestChanges(review_session, findings, decided_by):
  criticos ← [f PARA f EM findings SE f.severity ∈ {CRITICAL, BLOCKER}]
  RETORNA Decision(outcome=deny, cites=criticos).produces(DecisionRecord)        # Request Changes — §11


ALGORITMO TriggerReReview(prior_session, updated_component_ref):
  nova_rr ← RequestReview(updated_component_ref, ...)
  RETORNA ExecuteReviewSession(nova_rr)                                          # nova Execution — EX1/WF5
```

**Terminação/determinismo:** `ClassifyFindingSeverity` é uma função total sobre um espaço finito de combinações (§8); `EvaluateReviewOutcome`/`ApproveReview`/`RequestChanges` delegam integralmente a `EvaluateGate`/`Decision` já provados terminantes; `TriggerReReview` delega a `ExecuteReviewSession`, sem recursão.

---

## 15. Diagramas UML

### 15.1 Finding/Recommendation/Comment — uma estrutura, três nomes

```
┌─────────────────────────────────────┐
│ Artifact (produzido por Review Session)│   [Domain Model §2 #7]
│  content.findings[] : Finding[]         │
└──────────────────┬────────────────────┘
                    │ 0..*
                    ▼
             ┌─────────────┐
             │  Finding      │  severity ∈ {Info, Suggestion, Minor, Major, Critical, Blocker}  [§8]
             │  category      │
             │  standard_ref? │──► QualifiedRequirementIdentifier  [Standards §5.1]
             └──────┬────────┘
                    │ classificação por conteúdo/severidade — mesma estrutura
        ┌───────────┼───────────────┐
        ▼           ▼               ▼
  "Finding"    "Recommendation"   "Comment"
  (uso geral)  (severity∈{Info,   (severity=Info,
               Suggestion} +      category="comment")
               suggestion≠null)
```

### 15.2 Aprovação/Rejeição = Decision já existente

```
Review Session (Execution) ──produces──► Artifact{findings[]} ──substantiated by──► Evidence (Review Evidence)
        │                                                                                  │
        │ dispatch de Step(GATE_APPROVAL)                                                  │ informa
        ▼                                                                                  ▼
     Role (Reviewer, ≠ Owner — RC5) ────authorizes────► Decision{outcome=grant|deny} ────produces────► Decision Record
                                                              │
                                          grant ──► "Approval" (§10)      deny ──► "Request Changes" (§11)
```

---

## 16. Diagramas de Sequência

### 16.1 Ciclo completo — Findings bloqueantes → Request Changes → Re-review → Approval

```
Owner        Workflow(Gate 3)   Composition   Skill/Agent      Testing        Registry/Governance
  │                │                │              │              │                  │
  ├─RequestReview──►│                │              │              │                  │
  │                ├─ExecuteGate────►│              │              │                  │
  │                │                ├─ResolveSlot──►│              │                  │
  │                │                │◄─candidato────┤              │                  │
  │                ├─InvokeSkillStep/InvokeAgent────►│              │                  │
  │                │                │◄─Artifact{findings: [Blocker]}┤                  │
  │                ├─CollectEvidence─────────────────────────────►│                  │
  │                │◄─Review Evidence─────────────────────────────┤                  │
  │                ├─EvaluateReviewOutcome = BLOCK                                     │
  │                ├─RequestChanges──────────────────────────────────────────────────►│
  │◄─Decision Record (deny, cites=[Blocker finding])──────────────────────────────────┤
  │                                                                                    │
  │  [mudança aplicada]                                                               │
  ├─TriggerReReview────────────────────────────────────────────────────────────────►│
  │                (nova Execution — EX1/WF5)                                         │
  │                ├─ExecuteGate (repete fluxo)────►│              │                  │
  │                │◄─Artifact{findings: []}         │              │                  │
  │                ├─EvaluateReviewOutcome = PASS                                      │
  │                ├─ApproveReview───────────────────────────────────────────────────►│
  │◄─Decision Record (grant)───────────────────────────────────────────────────────────┤
```

---

## 17. Estados

**Nenhum estado novo.**

| Camada | Estados usados | Origem |
|---|---|---|
| Review Session (Execution) | `Initiated, Running, Completed, Failed, Aborted` | Domain Model §8 |
| Approval/Request Changes (Decision) | `Proposed, Authorized, Recorded` | Domain Model §8, §14 |
| Component sob revisão | Permanece em `Draft`/`Review` (Kernel §3) durante todo o ciclo — Code Review não transiciona o Component sozinho; apenas informa a Decision de Governance §7 passo 4-5 | Kernel §3 |

`Finding`/`Severity`/`Recommendation`/`Comment` **não têm estado** — são conteúdo estático de um `Artifact` imutável (Domain Model §8, `Generated → Verified → Retained`).

---

## 18. Casos Extremos

| # | Caso | Tratamento |
|---|---|---|
| RC-E1 | Reviewer é o próprio Owner do Component | Rejeitado por `ApproveReview`/`RequestChanges` (RC5, §21) — mesma regra de Governance §2, sem exceção |
| RC-E2 | Nenhum Finding produzido | `EvaluateReviewOutcome([]) = PASS` — Approval trivial, válido |
| RC-E3 | Todos os Findings são Info/Suggestion | `PASS` — nenhum bloqueia (§8, apenas Critical/Blocker bloqueiam) |
| RC-E4 | Finding classificado Major, mas a Policy que o vincularia é `ADVISORY` | Permanece Major (nunca escala a Critical/Blocker sem `enforcement_mode=BLOCKING`) — mesma regra de derivação, §8, não uma exceção |
| RC-E5 | Dois Reviewers (humano e Agent) discordam sobre o mesmo achado | Cada um produz sua própria `Decision` — conflito resolvido por Governance §17 (Conflict Resolution), nunca por um terceiro mecanismo de arbitragem de Code Review |
| RC-E6 | Re-review não resolve os Findings anteriores | Nova Execution ainda produz os mesmos Findings (ou piores) — `EvaluateReviewOutcome` reavalia do zero, `BLOCK` persiste até correção real |
| RC-E7 | Timeout do Reviewer (Agent indisponível) | Mesma semântica de Agent §11, CE7 (`Unauthorized`) ou execução com timeout (`Constraint`, Kernel §2.10) — Execution transita a `Failed`, nunca aprovação por omissão |
| RC-E8 | Breaking Change não reconhecido como tal pelo autor da mudança | `ClassifyXChange` é a fonte de verdade (mesma regra de Development Lifecycle CE9) — se `MAJOR`, critério 10 (§6) exige RFC/MIGRATION GUIDE independentemente da intenção declarada |
| RC-E9 | Security Finding descoberto durante Code Review geral, fora da fase 11 dedicada | Roteado sem exceção ao mesmo mecanismo de Security Architecture (§4.4-§4.5) — a origem (qual Gate encontrou) não muda a classificação nem o tratamento |
| RC-E10 | Diff excessivamente grande/complexo | `Constraint(RANGE)` sobre tamanho (Kernel §2.10) — mesmo padrão já usado por `max_lines` no Standard de code-quality já existente neste repositório |
| RC-E11 | Component sem `test_suite[]` sob revisão | Válido (Testing §11, CE8) — critério 7 (Testabilidade) produz Finding de severidade proporcional (tipicamente Minor/Major, nunca Blocker, salvo Standard `MUST` explícito) |

---

## 19. Performance

| Recurso | Regra de cache/complexidade | Origem |
|---|---|---|
| `ExecuteReviewSession` | Idêntica à já normatizada em Quality Gate §12 — nenhuma política nova | Quality Gate §12 |
| `ClassifyFindingSeverity` | O(1) por Finding — leitura de três valores já calculados | Standards §15.1; Policy §15.1 |
| Review Evidence reutilizada por Certificação | Reuso sem recoleta enquanto `manifest_digest` não mudar (mesma regra de Quality Gate §9.1) | Quality Gate §9.1 |

**Nenhuma política de cache nova.**

---

## 20. Eventos

**Nenhum evento novo.**

| Evento | Origem | Ocorre quando |
|---|---|---|
| `GatePassed`/`GateBlocked` | Workflow §11 | `EvaluateReviewOutcome` |
| `StepDispatched`/`StepCompleted`/`StepFailed` | Execution §11 | Review Session |
| Eventos de `ExecuteTestCase`/`CollectEvidence` | Testing §13 | Produção de Review Evidence |
| `DecisionRecorded` | Domain Model §14; Governance §18 | Approval/Request Changes |

---

## 21. Regras Normativas (RFC 2119)

| # | Regra | Nível |
|---|---|---|
| RC1 | `Finding`, `Recommendation` e `Comment` MUST ser representados pela mesma estrutura (§7) — MUST NOT introduzir schemas distintos | MUST / MUST NOT |
| RC2 | `Severity` MUST ser derivada de `Strength(normative_keyword)` + `enforcement_mode` + `precedence_level` (§8) — MUST NOT introduzir critério de julgamento independente | MUST / MUST NOT |
| RC3 | `Approval`/`Request Changes` MUST ser `Decision(outcome=grant\|deny)` (Workflow §6.1) — MUST NOT introduzir um mecanismo de aprovação paralelo | MUST / MUST NOT |
| RC4 | `Review Evidence` MUST ser `Evidence` (Domain Model §13) — MUST NOT duplicar o conteúdo do `Finding` que a origina | MUST / MUST NOT |
| RC5 | O Role que decide `Approval`/`Request Changes` MUST NOT ser o `owner` do Component sob revisão | MUST NOT |
| RC6 | Re-review SHOULD verificar, no mínimo, todo Finding `Critical`/`Blocker` da sessão anterior | SHOULD |
| RC7 | Re-review MUST ser uma nova Execution — MUST NOT reabrir a Review Session anterior | MUST / MUST NOT |
| RC8 | `Request Changes` MUST referenciar explicitamente todo Finding `Critical`/`Blocker` que a motivou | MUST |
| RC9 | Code Review MUST NOT introduzir um Gate paralelo ao Gate 3 já catalogado por Quality Gate Architecture | MUST NOT |
| RC10 | Este documento MUST NOT introduzir Registry, Governance, Testing, Security, Workflow, Standards ou Policy novos | MUST NOT |

---

## 22. Integrações

| Documento | Como Code Review o consome — sem alteração |
|---|---|
| **Constitution** | Regra Imutável nº3 (gate obrigatório) e nº9 (nenhum executor acima da verificação) fundamentam RC5/RC9 |
| **Kernel** | `owner` (§2.3) base de RC5; `Constraint` (§2.10) base de limite de diff (RC-E10) |
| **Governance** | §2 (não-autoaprovação), §7-§8 (autoridade de Reviewer), §17 (Conflict Resolution) reutilizados sem exceção |
| **Domain Model v1.1.0** | `Context`, `Execution`, `Artifact`, `Decision`, `Decision Record`, `Evidence` — todos reutilizados |
| **RFC-DM-001** | Context Snapshot obrigatório em toda Review Session |
| **Identity & Namespace** | `QualifiedRequirementIdentifier` (Standards §5.1) referenciado por `Finding.standard_ref` |
| **Registry & Discovery** | Nenhum novo índice — a Decision Record de Approval/Request Changes é registrada exatamente como qualquer outra (Registry §11, eventos) |
| **Validation & Certification** | Review (fase 12) precede e informa Certification (fase 13) — Review Evidence pode ser reutilizada, sem recoleta, na escalada L0-L4 |
| **Composition** | `ResolveSlot` resolve a Skill/Agent que realiza a análise |
| **Workflow** | `GATE_APPROVAL`, `Decision Record{grant\|deny}` (§6.1) são o mecanismo inteiro de Approval/Request Changes |
| **Execution** | `Dispatch`, EX1 — Review Session e Re-review, sem exceção |
| **Standards** | Fonte exclusiva de `normative_keyword`/`Strength()` — base de Severity |
| **Policy** | Fonte exclusiva de `enforcement_mode` — base de Severity |
| **Template Architecture** | `PROMPT Template` de um Agent-reviewer, quando presente, reutilizado sem alteração |
| **Skill Architecture** | `InvokeSkillStep` é o caminho de Skills de análise (ex.: `code-review`) |
| **Agent Architecture (23)** | `InvokeAgent` é o caminho de Agents decisórios (ex.: `code-reviewer`); §6.5 fundamenta RC5 para Agent |
| **Observability Architecture** | `trace`/`provenance` auditam Review Sessions históricas sem mecanismo novo |
| **Organization & Tenancy** | Nenhuma alteração |
| **Packaging & Distribution** | Review Evidence **MAY** acompanhar um Bundle como suporte, mesma regra de Packaging §6.2 |
| **Compliance Architecture** | Nenhuma alteração direta |
| **RFC-COMP-001** | `EnumerateSlots` consumido indiretamente via Composition |
| **Testing Architecture (24)** | `ExecuteTestCase`/`CollectEvidence` realizam Review Evidence; critério 7 (Testabilidade) |
| **Quality Gate Architecture (25)** | Gate 3 é, precisamente, o que este documento elabora — zero alteração à linha do catálogo |
| **Security Architecture (26)** | Security Finding é o mesmo `Finding` deste documento, já generalizado; critério 5 |
| **Development Lifecycle Architecture (27)** | Review é a fase 12; Re-review ocorre dentro da mesma fase, ou reentra nela via Evolution (fase 17) |
| **Project Architecture (28)** | Decision Records de revisão organizados por Namespace de Project (§13 daquele documento) |
| **Documentation Architecture (29)** | Gate 16 (Documentation Review, critério 16); MIGRATION GUIDE referenciado por Request Changes de Breaking Change |

---

## 23. Validação Institucional

| Documento base | Resultado |
|---|---|
| Constitution | **PASS** — Regras Imutáveis nº3 e nº9 fundamentam o desenho |
| Kernel | **PASS** — `owner`/`Constraint` reutilizados sem alteração |
| Governance | **PASS** — não-autoaprovação e autoridade de Reviewer intocadas |
| Domain Model v1.1.0 | **PASS** — zero entidades novas |
| RFC-DM-001 | **PASS** — Context Snapshot obrigatório |
| Identity & Namespace | **PASS** — `QualifiedRequirementIdentifier` reutilizado |
| Registry & Discovery | **PASS** — nenhum índice novo |
| Validation & Certification | **PASS** — Review Evidence reutilizável sem recoleta |
| Composition | **PASS** — `ResolveSlot` reutilizado |
| Workflow | **PASS** — `GATE_APPROVAL`/`Decision Record{grant\|deny}` reutilizados tal qual |
| Execution | **PASS** — EX1 sem exceção |
| Standards | **PASS** — fonte exclusiva de `Strength()`, base de Severity |
| Policy | **PASS** — fonte exclusiva de `enforcement_mode`, base de Severity |
| Template Architecture | **PASS** |
| Skill Architecture | **PASS** — `InvokeSkillStep` reutilizado |
| Agent Architecture (23) | **PASS** — `InvokeAgent` e §6.5 reutilizados |
| Observability Architecture | **PASS** |
| Organization & Tenancy | **PASS** |
| Packaging & Distribution | **PASS** |
| Compliance Architecture | **PASS** |
| RFC-COMP-001 | **PASS** |
| Testing Architecture (24) | **PASS** — `CollectEvidence` reutilizado tal qual |
| Quality Gate Architecture (25) | **PASS** — Gate 3 elaborado, nunca alterado |
| Security Architecture (26) | **PASS** — Security Finding generalizado, não redefinido |
| Development Lifecycle Architecture (27) | **PASS** — Review é a fase 12, sem redefinição |
| Project Architecture (28) | **PASS** — sem alteração |
| Documentation Architecture (29) | **PASS** — Gate 16/MIGRATION GUIDE reutilizados |
| **Exige RFC?** | **NÃO** |

**Prova formal de que Code Review não adiciona:**

| Item vedado pelo mandato | Verificação |
|---|---|
| Novo processo de aprovação | Nenhum — `Decision Record{grant\|deny}` (Workflow §6.1) |
| Nova Governance | Nenhuma — Governance §2/§7/§8/§17 reutilizados |
| Novo mecanismo de Testing | Nenhum — `ExecuteTestCase`/`CollectEvidence` (Testing §9) |
| Novo mecanismo de Security | Nenhum — Security Finding generalizado (Security §4.4) |
| Novo mecanismo de Quality Gate | Nenhum — Gate 3 (Quality Gate §4.3), elaborado, não redefinido |
| Novo Registry/Documentation | Nenhum — Registry §11 (eventos), Documentation §7 (referência, nunca duplicação) |

---

## 24. Dependências Futuras

| Consumidor | O que consome | Estado |
|---|---|---|
| **Multi-Agent Architecture** (futuro) | Múltiplos Agents revisando em paralelo (ex.: um Agent de segurança + um Agent de estilo) — este documento não pressupõe nem bloqueia | Sem bloqueio |
| **Observability — implementação em Runtime** | Séries históricas de Review Sessions/Findings em escala | `[LACUNA proposital]` já declarada em Execution §14 |
| **CI/CD** (futuro, operacional) | O fluxo de §13 é diretamente traduzível para um bot de revisão automatizada | Desbloqueado — Objetivo Prático |
| **Marketplace** (futuro) | Histórico de Review Evidence como sinal adicional de confiança, complementar à Certificação | Sem bloqueio |

---

## 25. Critério de Aceitação

### ✔ Checklist Institucional

| Critério do mandato | Status |
|---|---|
| Review Request, Review Session, Finding, Recommendation, Approval, Request Changes, Comment, Severity, Review Evidence definidos, todos como reuso | ✔ §4.1, §5, §7-§11 |
| Dezesseis critérios mínimos de revisão, cada um com proveniência | ✔ §6 |
| Seis severidades derivadas de Standards/Policy/Testing | ✔ §8 |
| Prova de que Code Review não cria novo processo de aprovação | ✔ §10, §11, §23 |
| Prova de que Code Review reutiliza Governance para decisões | ✔ §10, §11, §22 |
| Prova de que Code Review reutiliza Testing para evidências | ✔ §9, §22 |
| Prova de que Code Review reutiliza Security para achados de segurança | ✔ §7 (generalização), §22 |
| Prova de que Code Review reutiliza Quality Gates para bloqueios | ✔ §5, §22 |
| Prova de que Code Review reutiliza Registry e Documentation para registrar resultados | ✔ §22 |
| UML, sequência, algoritmos, casos extremos, RFC2119, performance, eventos | ✔ §14-§21 |
| Tabela de proveniência completa | ✔ §4.1 |
| Integração documento a documento (vinte e nove anteriores) | ✔ §22 |
| Nenhuma alteração a documento anterior — RFC separada se necessário | ✔ §23 — nenhuma mudança encontrada; nenhuma RFC necessária |

### ✔ Objetivo Prático Realizado

O Framework Eng possui, a partir deste documento, um processo oficial de revisão de código — não hipotético: `core/skill.static-analysis.code-review` e `.claude/agents/code-reviewer.md` já produzem, hoje, exatamente os Findings, severidades e veredictos (`REQUEST_CHANGES`, citando evidência, verificando autoria) que este documento formaliza. Code Review Architecture nomeia um comportamento observado, na mesma disciplina que Documentation Architecture já usou para o próprio fluxo documental.

### ✔ Confirmação Explícita

**Nenhum dos vinte e nove documentos anteriores foi alterado.** Code Review Architecture fecha o forward-reference deixado aberto por Quality Gate §4.3 (Gate 3, Implementation Review) — a terceira vez, nesta série, que um documento fecha exatamente uma caixa que outro já nomeou sem especificar (depois de Testing fechar "Testing" de Validation & Certification, e Security fechar os Gates de segurança de Quality Gate). `Finding`/`Recommendation`/`Comment` são uma única estrutura já em produção real; `Severity` deriva mecanicamente de Standards e Policy; `Approval`/`Request Changes` são o `Decision Record{grant|deny}` que Workflow já definia desde o início.

---

*Fim do documento. Versão 1.0.0.*
