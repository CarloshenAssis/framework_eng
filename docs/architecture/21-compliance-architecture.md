# Compliance Architecture

### Framework Eng — A Verificação Contínua de Conformidade Normativa

*Versão 1.0.0 · Base normativa (congelada): Constitution · Kernel · Governance · Domain Model v1.1.0 · RFC-DM-001 · Identity & Namespace · Registry & Discovery · Validation & Certification · Composition · Workflow · Execution · Standards · Policy · Template · Skill · Observability · Agent · Organization & Tenancy · Testing · Packaging & Distribution*

---

> **Nota de ratificação:** este documento **substitui integralmente** o rascunho de mesmo nome produzido no Bloco 4 (Documento 3 daquele bloco), que permanecia explicitamente não ratificado — consumidor downstream, base normativa congelada não incluía Compliance. A estrutura, o modelo conceitual e a quase totalidade do texto original são preservados; a ratificação exigiu validação contra os **sete documentos ratificados depois do rascunho** (Template, Skill, Observability, Agent, Organization & Tenancy, Testing, Packaging & Distribution) e contra a **versão final de Standards e Policy** (que substituiu integralmente o rascunho do próprio Bloco 4 sobre o qual a versão original de Compliance foi escrita). Essa validação encontrou uma inconsistência real, corrigida abaixo e não apagada: `PolicyBinding.conformance_mode` (Policy §5.3.1) não existia quando Compliance foi rascunhado, e o rascunho original não tinha como determinar se uma Partial Conformance satisfaz ou não um Binding específico. §4.4 (nova) fecha essa lacuna. Referências de seção a Standards e Policy foram corrigidas em todo o documento para apontar às versões ratificadas (`docs/architecture/12-standards-architecture.md`, `13-policy-architecture.md`), cujos números de seção divergem do rascunho do Bloco 4.

---

## 1. Posição Arquitetural

Compliance Architecture é o **substrato de verificação contínua** que fecha o ciclo normativo: dado um Effective Policy Set (Policy §9) e os Normative Requirements efetivos que ele implica (Standards §10.1), determina se um sujeito **continua** conforme ao longo do tempo, produzindo exclusivamente `Evidence`, `Decision` e `Artifact`.

**Distinção inegociável de Certification** (Governance §11/§13 já a antecipavam):

| | Certification (Validation & Certification) | Compliance (este documento) |
|---|---|---|
| Pergunta | "foi certificado?" | "continua conforme?" |
| Natureza | Evento pontual, atestado | Avaliação contínua, observada |
| Sujeito | Versioned Identity | Versioned Identity **× Effective Policy Set × tempo** |
| Produto | Decision Record da família Certification | Compliance Report (Artifact) + Conformance Claim (Standards §8.1) + Evidence; Decision apenas para Waiver/Risk Acceptance |
| Expira | Sim, por janela de validade declarada | Não expira; **drifta** |

Compliance **MUST NOT** conceder, suspender ou revogar Certificação. Pode apenas **fornecer Evidence** que a Governance ou o Certifier usarão para tal decisão — preservando integralmente a autoridade já estabelecida em Validation & Certification §5 e Governance §11. Em particular, Compliance é o mecanismo que **fecha operacionalmente** o forward-reference de Standards §8.4: "L3 MUST exigir Strict Conformance a todo Standard vinculado" pressupõe um produtor de Conformance Claims — Compliance é esse produtor (§4.3).

**Fronteira absoluta:** Compliance **MUST NOT** modificar Components. Produz apenas Evidence, Decisions e Artifacts.

---

## 2. Objetivos e Motivação

**Problema resolvido:** Governance §13 já mandatava Compliance como "verificação contínua (não pontual) de que componentes `Active` respeitam Standards e Policies vigentes — inclusive quando esses mudam depois que o componente já estava ativo", e já previa notificação de Owners e suspensão de descoberta ao fim do prazo. Faltava o mecanismo: como a avaliação ocorre, o que constitui evidência aceitável, como o drift é detectado, e como exceções entram no fluxo. Este documento fornece exatamente isso, sem redefinir nada de §13.

**Objetivos:** (a) tornar conformidade contínua observável e reproduzível; (b) detectar drift causado por mudança de norma, não apenas por mudança de componente; (c) integrar exceções (waiver, risk acceptance) ao Exception Process já existente (Governance §15) sem criar mecanismo paralelo; (d) alimentar Certification e Auditoria com Evidence estruturada; (e) determinar corretamente, para cada Binding do Effective Policy Set, se o resultado observado — Strict, Partial ou Non-Conformance — de fato **satisfaz** aquele Binding específico, dado seu `conformance_mode` (Policy §5.3.1).

---

## 3. Escopo

**Pertence:** Compliance Assessment; Compliance Report; Compliance Evidence; Conformance Claim (emissão, não definição); Policy Evaluation aplicada a um sujeito real; Binding Satisfaction; static vs. runtime compliance; drift detection; waiver e risk acceptance como especializações do Exception Process; remediação; ciclo de vida da avaliação.

**NÃO pertence, com justificativa:**

| Excluído | Justificativa |
|---|---|
| Definição de critério | Standard (Standards Architecture). |
| Definição de aplicabilidade | Policy (Policy Architecture). |
| Definição de Conformance Claim | Standards §8.1. Compliance **emite** Claims usando a estrutura já definida; não a redefine. |
| Concessão/revogação de Certificação | Validation & Certification §5 + Governance §11. Compliance fornece insumo, não decide. |
| Autoridade para aprovar exceções | Governance §15 já define: mesma autoridade que aprovaria a mudança formal equivalente. **MUST NOT** ser redefinida. |
| Novo lifecycle de avaliação | Uma Compliance Assessment **é** uma `Execution` (Domain Model §12, §8) — seu lifecycle é `Initiated→Running→Completed\|Failed\|Aborted`, sem exceção. |
| Armazenamento físico de histórico em escala | `[LACUNA proposital]` — já deferida em Execution §14 (Observability & Provenance Storage Architecture). Distinta de Observability Architecture (já ratificada, §14 abaixo), que fornece `query_events()`/`trace()` sobre a janela de retenção corrente — suficiente para drift entre assessments recentes, não para séries históricas em escala arbitrária. |

---

## 4. Modelo Conceitual

| Conceito | Natureza | Base normativa |
|---|---|---|
| **Compliance Assessment** | **Especializado** — é uma `Execution` (Domain Model §2 #6, §12) com convenção semântica no Context | Mesmo padrão de Execution §4 (Orchestration Correlation via Context) |
| **Compliance Evidence** | **Reutilizado sem especialização estrutural** — é `Evidence` (Domain Model §2 #8, §13) | Nenhuma subclasse nova |
| **Compliance Report** | **Novo construto interno**, materializado como `Artifact` genérico | Mesmo padrão de `Assembly` (Composition §4), `Execution Plan` (Execution §4), `Effective Policy Set` (Policy §9) |
| **Compliance Verdict** | **Novo construto interno** — Value Object; resultado por NR | — |
| **Conformance Claim** | **Reutilizado sem alteração** — Artifact já definido | Standards §8.1; Compliance é um dos Evaluators que o emite (§4.3) |
| **Binding Satisfaction** | **Novo construto interno** — Value Object; resultado por Binding | Consome `ResolvedBinding.conformance_mode` (Policy §5.3.1, §9) — §4.4 |
| **Compliance Drift** | **Novo construto interno** — Value Object; delta entre dois Reports | — |
| **Waiver** | **Especializado** — `Decision` + `Decision Record` sob Governance §15 (Exception Process) | Zero mecanismo novo |
| **Risk Acceptance** | **Especializado** — `Decision` da mesma família, com aceitação explícita de risco residual | Governance §14 (Risk Management) + §15 |
| **Remediation** | **Reutilizado** — é uma mudança de versão do Component sob Governance §7/§8 | Nenhum fluxo novo |
| Avaliação de Policy | **Reutilizado** | Policy §10 (`Policy Evaluation Service`) |
| Resolução de requisitos | **Reutilizado** | Standards §10 (`Standard Resolution Service`) |
| Context Snapshot | **Reutilizado** | RFC-DM-001 §3.2 |
| Notificação de Owners e prazo | **Reutilizado integralmente** | Governance §13 |

**Nenhum construto exige RFC.** Compliance Assessment é convenção semântica sobre `Execution` + `Context`; Report é `Artifact`; Conformance Claim é o `Artifact` já definido por Standards §8.1, apenas emitido por este documento; Verdict, Drift e Binding Satisfaction são Value Objects escopados ao Report; Waiver e Risk Acceptance são `Decision`.

### 4.1 Compliance Assessment como Execution

```
Compliance Assessment ≡ Execution {
  performed_by: Role                        (humano ou Agent — Domain Model §20; Agent §6.1/AG4
                                               governa o gradiente de autonomia permitido aqui)
  occurs_within: Context {
     assessment_kind: STATIC | RUNTIME
     subject: VersionedIdentifier | ExecutionInstanceId
     effective_policy_set_ref: ArtifactId    (Policy §9)
     assessment_id: <ULID>                   (Identity §4.2 — nenhum esquema novo)
  }
  captured_as: Context Snapshot             (RFC-DM-001 C2 — obrigatório)
  produces: [Compliance Evidence, Compliance Report, Conformance Claim*]
}
```

`*` — Conformance Claim é produzido condicionalmente; ver §4.3.

`[ESCOLHA DE DESIGN]` Modelar Assessment como Execution em vez de entidade própria: uma avaliação é literalmente "aplicação concreta de um Component (o avaliador) em um momento específico, sob um contexto, por um Role, produzindo Evidence" — a definição textual de `Execution` no Domain Model §12, sem forçar nada. Alternativa descartada: entidade `Assessment` própria — rejeitada por replicar um lifecycle que já existe. Precedente: OPA/Gatekeeper modela cada avaliação como um evento de admissão comum, não como um tipo de objeto novo.

### 4.2 Compliance Verdict — granularidade por Normative Requirement

```
ComplianceVerdict {
  nr_id: QualifiedRequirementIdentifier      (Standards §5.1 — forma qualificada, estável)
  standard: VersionedIdentifier
  outcome: CONFORMANT | NON_CONFORMANT | NOT_APPLICABLE | INDETERMINATE
  evidence_ref: EvidenceId                  (obrigatório salvo NOT_APPLICABLE)
  waiver_ref: DecisionRecordId?             (§4.7)
}
```

`INDETERMINATE` é obrigatório como resultado de primeira classe: quando `EvaluationMethod.kind = ATTESTED` (Standards §4.6) e nenhuma atestação existe, o verdict **MUST NOT** ser silenciosamente `CONFORMANT` nem `NON_CONFORMANT`. Justificativa: presumir conformidade sem evidência viola Constitution (Confiança verificável — "confiança não é concedida por reputação, é concedida por conformidade demonstrada"); presumir não-conformidade produziria falsos positivos que erodem o valor do sinal. Esta é a mesma disciplina que Standards §7.3 (ST12) já aplica a `rid` desconhecido em um Claim antigo, e que Standards §8.3 aplica à indeterminação dentro de um Claim.

### 4.3 Conformance Claim por Standard — reuso do Artifact de Standards §8.1

Ao concluir a avaliação de todos os NRs de um `(subject, standard, level)`, o Compliance Service **decide entre dois caminhos**, nunca ambos:

| Condição sobre os `ComplianceVerdict` do grupo | Ação |
|---|---|
| Todo NR `MUST`/`MUST_NOT` satisfeito, `indeterminate` vazio, ao menos um `SHOULD`/`SHOULD_NOT` não satisfeito | Emite `ConformanceClaim` (Standards §8.1) com `mode = PARTIAL`, `unsatisfied_should` enumerado (Standards ST8) |
| Todo NR `MUST`/`MUST_NOT` e `SHOULD`/`SHOULD_NOT` satisfeito, `indeterminate` vazio | Emite `ConformanceClaim` com `mode = STRICT` |
| Algum NR `MUST`/`MUST_NOT` não satisfeito, OU `indeterminate` não vazio | **MUST NOT** emitir `ConformanceClaim` — Standards §8.3 delega explicitamente este caso à "camada consumidora (Compliance, downstream)". O `ComplianceReport` (§5) permanece a fonte de verdade; a ausência de Claim **é**, por si, o sinal. |

`[ESCOLHA DE DESIGN]` Reusar `ConformanceClaim` como o Artifact emitido por Standard vinculado, em vez de o Compliance Report carregar apenas seus próprios `ComplianceVerdict` soltos. Alternativa descartada — e presente no rascunho original deste documento: tratar `ComplianceVerdict[]` como suficiente, sem nunca instanciar `ConformanceClaim`. Rejeitada porque Standards §8.4 já fecha explicitamente o forward-reference de Validation & Certification §5 ("L3 MUST exigir Strict Conformance... Partial Conformance MUST NOT satisfazer L3") **presumindo a existência de um produtor de `ConformanceClaim`** — sem este documento emiti-lo, aquele fechamento permaneceria vácuo na prática, apesar de formalmente completo no papel. Emitir o Claim aqui é a aplicação, não a redefinição, de Standards §8.1.

### 4.4 Binding Satisfaction — `conformance_mode` e o veredito do Binding

**Lacuna fechada nesta ratificação:** o rascunho original de Compliance foi escrito antes de `PolicyBinding.conformance_mode` (Policy §5.3.1) existir, e portanto nunca determinava se um `ConformanceClaim{mode: PARTIAL}` satisfaz ou não um `ResolvedBinding` específico do Effective Policy Set. Esta subseção fecha essa lacuna, sem introduzir nenhum construto novo além de um Value Object de resultado.

```
BindingSatisfaction {
  binding: ResolvedBinding                   [Policy §9 — carrega conformance_mode, enforcement_mode]
  claim_ref: ArtifactId?                      (ausente ⟺ Non-Conformance ou indeterminação — §4.3)
  satisfied: boolean
  reason: CLAIM_STRICT | CLAIM_PARTIAL_ACCEPTED | CLAIM_PARTIAL_REJECTED
        | NO_CLAIM_NON_CONFORMANT | NO_CLAIM_INDETERMINATE | WAIVED
  waiver_ref: DecisionRecordId?
}
```

**Regra (CM14):**

| `claim.mode` (se existir) | `binding.conformance_mode` | `satisfied` | `reason` |
|---|---|---|---|
| `STRICT` | qualquer | `true` | `CLAIM_STRICT` |
| `PARTIAL` | `PARTIAL_ACCEPTABLE` | `true` | `CLAIM_PARTIAL_ACCEPTED` |
| `PARTIAL` | `STRICT` | `false` (salvo waiver — abaixo) | `CLAIM_PARTIAL_REJECTED` |
| *(nenhum Claim — Non-Conformance)* | qualquer | `false` | `NO_CLAIM_NON_CONFORMANT` |
| *(nenhum Claim — indeterminação)* | qualquer | `false` | `NO_CLAIM_INDETERMINATE` |

Strict Conformance satisfaz qualquer Binding porque Strict **implica** Partial pela própria definição de Standards §8.2 (todo `MUST` e todo `SHOULD` satisfeitos é estritamente mais forte que apenas todo `MUST`). Esta implicação não é uma regra nova — é uma leitura direta das definições já fixadas em Standards §8.2, tornada explícita porque Compliance é o primeiro documento que precisa *comparar* os dois resultados, não apenas produzi-los.

**Waiver sobre `CLAIM_PARTIAL_REJECTED`:** um Binding `STRICT` cujo Claim seja `PARTIAL` **MAY** ser tratado como satisfeito (`reason = WAIVED`) quando existe Waiver ativo (Governance §15, §4.7) cobrindo especificamente a exigência de estritude daquele Binding — não os `SHOULD` individuais, que já são legitimamente dispensáveis sob Partial Conformance sem processo de exceção algum (Standards §8.2 já os declara "não bloqueantes" nesse modo). O que está sendo dispensado é a exigência do Binding, não o requisito do Standard — distinção preservada em `BindingSatisfaction.waiver_ref`, campo separado de `ComplianceVerdict.waiver_ref` (§4.2), embora ambos consumam o mesmo Governance §15 sem mecanismo paralelo.

`[ESCOLHA DE DESIGN]` Waiver de Binding como campo distinto de Waiver de NR, em vez de reusar `ComplianceVerdict.waiver_ref` para os dois casos. Alternativa rejeitada: exigir um Waiver por `SHOULD` individual não satisfeito sempre que o Binding for `STRICT`. Rejeitada porque produziria N processos de exceção (um por `SHOULD` pendente) para uma única decisão institucional real ("aceitamos Partial aqui"), inflando o Exception Process sem ganho de rastreabilidade — a rastreabilidade já existe em `unsatisfied_should` do próprio Claim (Standards ST8).

### 4.5 Static vs. Runtime Compliance

| Tipo | Sujeito | Momento | `applies_at` correspondente (Policy §8) |
|---|---|---|---|
| **Static** | Component (Coordinate@version) e sua Assembly | Admissão, mudança de norma, ciclo periódico | MANIFEST, COMPOSITION |
| **Runtime** | Execution concreta | Dispatch e/ou pós-conclusão | WORKFLOW, EXECUTION |

Runtime Compliance avalia contra o **Context Snapshot** da Execution avaliada (RFC-DM-001 C2), nunca contra o Context vivo — única forma de a avaliação ser reproduzível posteriormente (Domain Model §15).

Nota terminológica: `PolicyScope.applies_at` (Policy §8, quatro valores incluindo `WORKFLOW`) e `ComplianceTarget.applies_to` (Standards §4.5, quatro valores incluindo `ARTIFACT`) são enums **relacionados mas distintos** — o primeiro determina *quando* uma Policy se aplica, o segundo *que classe de sujeito* um NR individual mira. Policy PL13 já reconcilia os dois na validação (`INCOMPATIBLE_APPLICATION_PLANE`); este documento não introduz uma terceira noção de "plano", apenas consome ambas corretamente.

### 4.6 Compliance Drift

Drift é o delta entre dois Compliance Reports do mesmo sujeito em instantes distintos. Três causas, todas detectáveis mecanicamente:

| Causa | Origem | Detecção |
|---|---|---|
| **Subject drift** | Component mudou de versão | Comparação de `subject` entre Reports |
| **Normative drift** | Standard vinculado evoluiu (novo NR, força elevada) | Comparação da lineage do Standard (Standards §7.5) |
| **Applicability drift** | Effective Policy Set mudou (nova Policy, expiração, mudança de Context) | Comparação de `effective_policy_set_ref` |

Normative e Applicability drift são exatamente o cenário que Governance §13 mandata tratar ("inclusive quando esses Standards/Policies mudam depois que o componente já estava ativo"). Este documento fornece o mecanismo de detecção; **a resposta institucional (notificação, prazo, suspensão de descoberta) permanece integralmente definida por §13** e não é redefinida aqui.

### 4.7 Waiver e Risk Acceptance

Ambos são **especializações nominais do Exception Process** (Governance §15), não mecanismos novos. Herdam, sem alteração, todos os seus requisitos: motivo registrado, **prazo de validade obrigatório** (exceção sem prazo é proibida por §15), dono responsável, condição de encerramento, aprovação pela mesma autoridade que aprovaria a mudança formal equivalente, e visibilidade pública junto ao componente afetado.

| Forma | Semântica | Efeito |
|---|---|---|
| **Waiver (nível NR)** | Dispensa temporária de um `MUST` específico para um sujeito específico | `ComplianceVerdict.outcome` permanece `NON_CONFORMANT`, marcado com `waiver_ref` (§4.2) |
| **Waiver (nível Binding)** | Dispensa da exigência de estritude de um Binding `STRICT` quando o Claim é `PARTIAL` | `BindingSatisfaction.satisfied = true`, `reason = WAIVED` (§4.4) |
| **Risk Acceptance** | Aceitação formal do risco residual, sem promessa de remediação no prazo | Idem a qualquer das formas acima, com classificação de risco anexada (Governance §14) |

`[ESCOLHA DE DESIGN]` Waiver **MUST NOT** converter `ComplianceVerdict.outcome` em `CONFORMANT`, nem `BindingSatisfaction.reason` em `CLAIM_STRICT`/`CLAIM_PARTIAL_ACCEPTED`. Alternativa descartada: tratar waiver como conformidade concedida — rejeitada porque destruiria a distinção auditável entre "obedece" e "foi dispensado de obedecer", corrompendo permanentemente a série histórica de conformidade e violando Constitution (Auditabilidade: "deve ser sempre possível reconstruir por que algo foi feito"). Precedente: em auditoria de segurança, uma exceção aprovada nunca reclassifica o achado como inexistente — ela o marca como aceito.

### 4.8 Compliance Lifecycle

**Não existe.** Uma Compliance Assessment é uma `Execution` e usa exatamente o lifecycle de Domain Model §8. Um Compliance Report e um Conformance Claim são `Artifact` e usam exatamente `Generated → Verified → Retained | Superseded` (Domain Model §8). Nenhum estado novo é introduzido.

---

## 5. Modelo Operacional

**Serviço:** `Compliance Service` — substrato, mesma classe arquitetural do `Standard Resolution Service` (Standards §10) e do `Policy Evaluation Service` (Policy §10). Sem Lifecycle próprio, sem autoridade decisória, sem escrita em Component, Manifest, Registry ou status de Certificação.

```
assess(subject, kind: STATIC|RUNTIME, at: Timestamp, plane: ApplicationPlane) → ComplianceReport (Artifact)
  PRE:  subject resolve via Registry (Registry §6.1) a lifecycle_state ∈ {Active, Deprecated}
        E, se RUNTIME, subject referencia uma Execution com Context Snapshot existente
  POST: uma Execution de Assessment foi registrada (Initiated→Running→Completed|Failed)
        E um ComplianceReport imutável foi produzido
        E para cada (standard, level) do EPS, um ConformanceClaim foi emitido SE E SOMENTE SE
          a condição de §4.3 for satisfeita
        E toda Compliance Evidence produzida é imutável (Domain Model §13)
  INV:  o Service MUST NOT modificar o subject nem qualquer Component

compute_binding_satisfaction(binding: ResolvedBinding, claim: ConformanceClaim?) → BindingSatisfaction
  PRE:  binding pertence ao Effective Policy Set do assessment corrente
  POST: resultado determinístico conforme a tabela CM14 (§4.4)

detect_drift(subject, report_a, report_b) → ComplianceDrift
  PRE:  ambos Reports referenciam o mesmo subject Coordinate (versões podem diferir)
  POST: delta classificado por causa (§4.6), sem juízo de valor

evaluate_requirement(nr, subject, ctx_snapshot) → ComplianceVerdict
  PRE:  nr.evaluation.evidence_kind_required é conhecido                    [Standards §4.6]
  POST: verdict ∈ {CONFORMANT, NON_CONFORMANT, NOT_APPLICABLE, INDETERMINATE}
        E evidence_ref presente salvo NOT_APPLICABLE
```

**Invariantes institucionais:**
1. **Determinismo condicionado:** dado o mesmo `(subject, effective_policy_set, context_snapshot)`, `assess` **MUST** produzir os mesmos Verdicts, os mesmos Claims e as mesmas Binding Satisfactions — requisito herdado de Reproducibility (Validation & Certification §6).
2. **Não-modificação:** o Compliance Service **MUST NOT** possuir qualquer operação de escrita sobre Components, Manifests, Registry Entries ou status de Certificação.
3. **Não-decisão:** transições de Certificação decorrentes de não-conformidade **MUST** ser tomadas por Certifier/Steward sob Validation & Certification §5 e Governance §11/§13, consumindo o Report e os Claims como Evidence.

---

## 6. Diagramas

### 6.1 UML simplificado

```
┌──────────────────────┐        ┌──────────────────────┐
│ Compliance Assessment │───────►│ ComplianceReport      │ (Artifact)
│  ≡ Execution          │produces│  verdicts[]           │
│  Context{kind,subject,│        │  binding_satisfactions[]
│   eps_ref, ULID}      │        │  resolution_trace     │
│  captured_as ─────────┼──► Context Snapshot [RFC-DM-001 C2]
└──────────┬───────────┘        └─────────┬────────────┘
           │produces                       │1..*         │0..*
           ▼                                ▼             ▼
   ┌──────────────┐              ┌────────────────────┐  ┌──────────────────────┐
   │ Compliance    │◄─────────────┤ ComplianceVerdict   │  │ ConformanceClaim      │
   │ Evidence      │ evidence_ref │  nr_id, outcome     │  │ (Standards §8.1)      │
   │ ≡ Evidence    │              │  waiver_ref ────┐    │  │ mode: STRICT|PARTIAL  │
   └──────────────┘              └──────────────────┼───┘  └──────────┬────────────┘
                                                      │                 │ claim_ref
                                                      ▼                 ▼
                                              Decision Record   ┌────────────────────┐
                                              (Governance §15)  │ BindingSatisfaction │
                                                                 │  satisfied, reason  │
                                                                 │  waiver_ref ────────┼──► Decision Record
                                                                 └────────────────────┘     (Governance §15)
```

### 6.2 Sequência — assessment estático

```
Trigger(Governance §13 | periódico | Owner) -> ComplianceService : assess(subject, STATIC, at, MANIFEST)
ComplianceService -> Execution : Initiated
ComplianceService -> ContextSnapshot : capture              [RFC-DM-001 C2 — obrigatório]
ComplianceService -> Execution : → Running
ComplianceService -> PolicyEval  : resolve_effective_policy_set(subject, ctx, at, MANIFEST)   [Policy §10.1]
PolicyEval --> ComplianceService : EffectivePolicySet (Artifact)     [inclui bindings[].conformance_mode]
loop para cada ResolvedBinding
   ComplianceService -> StandardResolver : resolve_effective_requirements(std@v, level)  [Standards §10.1]
   StandardResolver --> ComplianceService : NormativeRequirement[]
   loop para cada NR
      ComplianceService -> ComplianceService : evaluate_requirement(nr, subject, snapshot)
      ComplianceService -> Evidence : produce (imutável)
      opt existe Waiver ativo para (subject, nr)
         ComplianceService -> Governance : lookup Exception (§15)
         ComplianceService -> Verdict : anexar waiver_ref (outcome permanece NON_CONFORMANT)
   ComplianceService -> ComplianceService : todo MUST ok E indeterminate=∅ ?
   alt sim
      ComplianceService -> ConformanceClaim : emitir (mode = STRICT|PARTIAL — §4.3)  [Standards §8.1]
   else não
      note: nenhum Claim emitido — Non-Conformance ou indeterminação (§4.3)
   ComplianceService -> ComplianceService : compute_binding_satisfaction(binding, claim?)  [§4.4]
ComplianceService -> ComplianceReport : produce (Artifact imutável)
ComplianceService -> Execution : → Completed
ComplianceService -> EventBus : ComplianceAssessmentCompleted
note: nenhuma escrita em Component, Registry ou Certification
```

### 6.3 Fluxo de drift e remediação

```
Standard v2 publicado ──► Normative Drift detectado
        │
        ▼
ComplianceService.assess(subjects vinculados) ──► Report{binding_satisfactions com satisfied=false}
        │
        ▼
Governance §13 : notifica Owner, define prazo proporcional ao risco (§14)
        │
        ├──► Owner remedia: nova versão do Component (Governance §7/§8) ──► reassess
        ├──► Owner solicita Waiver/Risk Acceptance — nível NR ou nível Binding (§4.7) ──► Decision Record, prazo obrigatório
        └──► Prazo expira sem ação ──► Governance §13: suspensão de descoberta ativa
                                        (decisão da Governance, não do Compliance Service)
```

### 6.4 Estados

Nenhum diagrama de estados próprio: Assessment usa o lifecycle de `Execution` (Domain Model §8); Report e Conformance Claim usam o de `Artifact` (Domain Model §8). Reproduzi-los aqui seria duplicação proibida.

---

## 7. Algoritmos

```
ALGORITMO Assess(subject, kind, at, plane):
  ctx = Context{ assessment_kind: kind, subject: subject,
                 assessment_id: new_ULID() }                        # Identity §4.2
  snapshot = capture_context_snapshot(ctx)                          # RFC-DM-001 C2 — obrigatório
  exec = Execution.Initiated(occurs_within=ctx, captured_as=snapshot)
  exec.transition(Running)

  eps = PolicyEvaluationService.resolve_effective_policy_set(subject, snapshot, at, plane)   # Policy §10.1
  verdicts = []
  binding_satisfactions = []

  FOR binding IN eps.bindings:                                                               # Policy §9
     nrs = StandardResolutionService.resolve_effective_requirements(
              binding.standard, binding.conformance_level)                                   # Standards §10.1
              # binding.standard MAY resolver a um Standard Package (standard_kind=PACKAGE);
              # resolve_effective_requirements já retorna o fecho de `includes` — nenhum caso especial (§12)
     group_verdicts = []
     FOR nr IN nrs:
        IF NOT target_matches(nr.target, subject, kind):                                     # Standards §11.3
           v = Verdict(nr, NOT_APPLICABLE)
        ELSE:
           ev = collect_evidence(nr.evaluation, subject, snapshot)
           IF ev is absent AND nr.evaluation.kind IN {ATTESTED, DYNAMIC}:
              v = Verdict(nr, INDETERMINATE)                                                 # §4.2
           ELSE:
              outcome = decide(nr, ev)                # CONFORMANT | NON_CONFORMANT
              waiver = Governance.lookup_active_exception(subject, nr.id, at)                 # §15
              v = Verdict(nr, outcome, evidence_ref=ev?.id, waiver_ref=waiver?.id)
        verdicts += v
        group_verdicts += v

     claim = NULL
     IF NOT AnyIndeterminate(group_verdicts) AND AllMustSatisfied(group_verdicts):            # §4.3
        mode = AnySHouldUnsatisfied(group_verdicts) ? PARTIAL : STRICT
        claim = Artifact(ConformanceClaim, {                                                  # Standards §8.1
           subject, standard: binding.standard, level: binding.conformance_level, mode,
           satisfied: [...], unsatisfied_should: [...], not_applicable: [...],
           indeterminate: [], evidence_refs: [...], evaluated_at: at, context_snapshot: snapshot.id
        })
     bs = ComplianceService.compute_binding_satisfaction(binding, claim)                      # §4.4, CM14
     binding_satisfactions += bs

  report = Artifact(ComplianceReport, {
     subject, eps_ref: eps.id, verdicts, binding_satisfactions,
     summary: aggregate(binding_satisfactions),
     resolution_trace: eps.resolution_trace     # Policy §9.2
  })
  exec.transition(Completed)
  RETURN report
  # INVARIANTE: nenhuma escrita em Component/Registry/Certification

ALGORITMO DetectDrift(report_a, report_b):
  drift = { subject: ∅, normative: ∅, applicability: ∅ }
  IF report_a.subject.version ≠ report_b.subject.version:
     drift.subject = diff(versions)
  IF standards_lineage(report_a) ≠ standards_lineage(report_b):
     drift.normative = diff(nr_sets)            # NRs adicionados, removidos, força elevada
  IF report_a.eps_ref ≠ report_b.eps_ref:
     drift.applicability = diff(policy_bindings)
  RETURN drift                                   # descritivo, sem juízo de valor

ALGORITMO ContinuousCompliance(trigger):
  # Reutiliza integralmente o gatilho já mandatado por Governance §13:
  # toda mudança em Standard/Policy dispara a lista de Components afetados.
  affected = Registry.list(bound_to=trigger.changed_component)     # Registry §5
  FOR subject IN affected:
     report = Assess(subject, STATIC, now(), MANIFEST)
     IF ANY bs IN report.binding_satisfactions WHERE bs.satisfied = FALSE:
        emit ComplianceViolationDetected(subject, report)
        # Cobre tanto Non-Conformance quanto CLAIM_PARTIAL_REJECTED sem waiver (§4.4) —
        # não apenas NON_CONFORMANT bruto, correção desta ratificação (ver nota de topo).
        # Notificação, prazo e suspensão são responsabilidade da Governance §13 —
        # o Compliance Service apenas emite o sinal.
```

---

## 8. Casos Extremos

| Caso | Tratamento |
|---|---|
| NR `ATTESTED` ou `DYNAMIC` sem Evidence | `INDETERMINATE` obrigatório — nunca presunção em qualquer direção (§4.2). |
| Standard vinculado foi `Archived` entre dois assessments | Verdict `INDETERMINATE` com causa registrada; escalado a Steward via Governance §13. Nunca `CONFORMANT` por ausência de norma — mesma regra de Standards §7.4. |
| Waiver expira durante um assessment em curso | Avaliação usa o estado em `at` do Context Snapshot — expiração posterior não altera o Report emitido (imutabilidade de Artifact, Domain Model §8). Próximo assessment refletirá. |
| Waiver sem prazo | Impossível: Governance §15 já proíbe exceção sem prazo. Nenhuma regra nova necessária. |
| Assessment falha por indisponibilidade do Standard Resolver | Execution transita a `Failed`; **MUST NOT** emitir Report parcial como se completo. Reutiliza Failure Policy de Execution §9. |
| Dois assessments concorrentes sobre o mesmo subject | Seguros por construção: `assessment_id` distintos, Context Snapshots independentes, Reports imutáveis — mesma garantia de Execution §9 para execuções concorrentes. |
| Effective Policy Set vazio | Report válido com zero verdicts e zero binding_satisfactions; conformidade trivialmente satisfeita. Não é erro (paridade com Policy §11.1, fase 4 sobre grupos vazios). |
| Subject em `Deprecated` | Assessment permitido (Governance §13 aplica-se a componentes ainda consumíveis); drift reportado normalmente. |
| `Binding.conformance_mode = STRICT`, Claim `PARTIAL`, sem Waiver | `BindingSatisfaction.satisfied = false`, `reason = CLAIM_PARTIAL_REJECTED` (§4.4, CM14) — **gap fechado nesta ratificação**; o rascunho original não distinguia este caso de conformidade plena. |
| Binding referencia um `Standard Package` (`standard_kind = PACKAGE`) | Nenhum tratamento especial: `resolve_effective_requirements` já retorna o fecho de `includes` (Standards §10.1); Compliance itera sobre o resultado sem saber, nem precisar saber, que a origem é um Package (§12). |
| Component com waiver permanente de facto (renovações sucessivas) | Detectável como padrão nas métricas (Governance §19 "exceções ativas vencidas sem resolução"); tratamento é institucional (Governance), não mecânico. Declarado explicitamente como risco residual. |
| Compliance Service tenta escrever em Component | Impossível por construção: o Service não expõe operação de escrita (§5, invariante 2). |

---

## 9. Performance

Static Compliance é cacheável por `(subject@version, effective_policy_set_id)` — ambos imutáveis, portanto o par determina o resultado, incluindo `binding_satisfactions`. Invalidação ocorre por evento de mudança de norma, não por tempo.

Runtime Compliance está no caminho quente (dispatch de Step — Execution §5). Mitigação normativa: Policies **SHOULD** preferir `applies_at` mais estático (Policy PL12), reservando avaliação em `EXECUTION` apenas para condições genuinamente dependentes de runtime. Avaliação de NRs independentes é paralelizável; `compute_binding_satisfaction` é O(1) por Binding após os Claims existirem.

`ContinuousCompliance` sobre mudança de Standard tem fan-out proporcional ao número de Components vinculados — potencialmente milhares. **SHOULD** ser executado de forma assíncrona e priorizada por risco (Governance §14), nunca sincronamente no caminho de publicação do Standard.

Particionamento e consistência: herdam integralmente as garantias de Execution §10 (forte para estado terminal de cada assessment; eventual com SLA para agregações) — nenhum modelo novo de consistência é introduzido.

---

## 10. Eventos

`ComplianceAssessmentStarted`, `ComplianceAssessmentCompleted`, `ComplianceAssessmentFailed`, `ComplianceViolationDetected`, `ComplianceDriftDetected(kind)`, `ConformanceClaimEmitted`, `BindingUnsatisfied(reason)`, `WaiverApplied`, `WaiverExpired`, `RiskAccepted`, `RemediationCompleted`, `IndeterminateVerdictRecorded`.

---

## 11. Regras Normativas (RFC 2119)

| # | Regra | Nível |
|---|---|---|
| CM1 | Compliance Service MUST NOT modificar Components, Manifests, Registry ou status de Certificação | MUST NOT |
| CM2 | Compliance Assessment MUST ser modelada como `Execution` — nenhum lifecycle novo | MUST |
| CM3 | Toda avaliação MUST usar Context Snapshot (RFC-DM-001 C2) | MUST |
| CM4 | Waiver MUST NOT converter `ComplianceVerdict.outcome` em `CONFORMANT` nem `BindingSatisfaction.reason` em resultado plenamente satisfeito sem `WAIVED` | MUST NOT |
| CM5 | Waiver e Risk Acceptance MUST seguir Governance §15 sem mecanismo paralelo, em qualquer granularidade (NR ou Binding) | MUST |
| CM6 | NR `ATTESTED` ou `DYNAMIC` sem Evidence MUST resultar em `INDETERMINATE` | MUST |
| CM7 | Compliance Report MUST ser imutável e carregar `resolution_trace` | MUST |
| CM8 | Compliance MUST NOT conceder, suspender ou revogar Certificação | MUST NOT |
| CM9 | Assessment com falha MUST NOT emitir Report parcial como completo | MUST NOT |
| CM10 | Compliance Report MUST agregar separadamente não-conformidades com e sem waiver, por NR e por Binding | MUST |
| CM11 | `ContinuousCompliance` SHOULD ser assíncrono e priorizado por risco | SHOULD |
| CM12 | Runtime Compliance MAY ser invocado por `GATE_AUTO` (Workflow §4) | MAY |
| CM13 | Static Compliance MAY ser cacheado por `(subject@version, eps_id)` | MAY |
| CM14 | `BindingSatisfaction` MUST ser computada pela tabela §4.4 — Strict Conformance sempre satisfaz; Partial Conformance satisfaz apenas Bindings `PARTIAL_ACCEPTABLE`, salvo Waiver de Binding | MUST |
| CM15 | `ConformanceClaim` MUST NOT ser emitido quando qualquer `MUST`/`MUST_NOT` do grupo estiver `NON_CONFORMANT` ou quando `indeterminate` for não vazio | MUST NOT |

---

## 12. Integrações

| Documento | Contrato de integração |
|---|---|
| **Constitution** | Confiança verificável materializada em `INDETERMINATE` (§4.2) e em `CLAIM_PARTIAL_REJECTED` sem gradação silenciosa (§4.4); auditabilidade preservada por waiver não reclassificar verdict nem satisfaction (§4.7). |
| **Kernel** | Nenhuma alteração de Contract; Compliance lê Manifests, nunca os escreve. |
| **Governance** | §13 (Compliance contínua) implementado, não redefinido; §15 (Exception) é o único mecanismo de waiver, em ambas as granularidades de §4.7; §14 (Risk) classifica risk acceptance; §12 (Audit) consome Reports e Claims como Evidence; §11 (Certification) recebe Claims como insumo direto de L3 sem que Compliance decida (§1). |
| **Domain Model v1.1.0** | Assessment = `Execution`; Evidence = `Evidence`; Report e Claim = `Artifact`; Waiver = `Decision`+`Decision Record`. Zero entidades, relações e estados novos. |
| **RFC-DM-001** | C2 (Context Snapshot) é precondição obrigatória de toda avaliação; C3 não é tocado; C1 respeitado. |
| **Identity & Namespace** | `assessment_id` é ULID do esquema existente (§4.2); referências a subject são Versioned Identifiers totalmente qualificados. |
| **Registry & Discovery** | `list(bound_to=...)` reutiliza o índice por Standard/Policy vinculado (Registry §5, §8); Compliance **MUST NOT** escrever no Registry. |
| **Validation & Certification** | Compliance Report e Conformance Claim são Evidence para decisões de Certificação (§5), incluindo suspensão. Este documento fornece a detecção e a emissão do Claim que L3 (Standards §8.4) já presumia; a transição continua exclusiva do Certifier. |
| **Composition** | Static Compliance avalia a Assembly resolvida (Composition §5) quando `applies_at = COMPOSITION`. |
| **Workflow** | `GATE_AUTO` (Workflow §4) **MAY** invocar `assess(RUNTIME)` e consumir o Report/Binding Satisfaction como Evidence de gate; a decisão de passar/bloquear é do Gate, não do Compliance Service. |
| **Execution** | Runtime Compliance avalia contra Context Snapshot; Policies `BLOCKING` (Policy §5.4) impedem transição a `Running` — decisão executada pelo Scheduler (Execution §5), com insumo do Compliance Service. |
| **Standards** | Consome `NormativeRequirement`, `EvaluationMethod` (§4.6) e `Standard Resolution Service` (§10.1) sem redefini-los; **emite** `ConformanceClaim` (§8.1) sob a regra de §4.3; Standard Package (§9) atravessado sem caso especial (§8, §12 desta linha). |
| **Policy** | Consome `Effective Policy Set` (§9), `Policy Evaluation Service` (§10.1) e `ResolvedBinding.conformance_mode` (§5.3.1) como entrada primária de §4.4 — a integração que fecha a lacuna desta ratificação. |
| **Template** | Nenhuma integração direta; Compliance não gera nem consome Templates. |
| **Skill** | Uma Skill **MAY** ser o `procedure_ref` (Standards §4.6) que implementa `evaluate_requirement` para um `EvaluationMethod.kind = DYNAMIC` — mesmo padrão de invocação de Skill §7, sem mecanismo novo. |
| **Observability** | `query_events()`/`trace()` (Observability §7) **MAY** ser usados por `DetectDrift` para correlacionar Reports históricos dentro da janela de retenção corrente — fecha parcialmente, sem substituir, o `[LACUNA proposital]` de armazenamento em escala (§3, §14). |
| **Agent** | `performed_by: Role` de uma Compliance Assessment **MAY** ser ocupado por um Agent (§4.1); AG4 (Agent §7, coautorização humana) aplica-se sem alteração quando o `risk_tier` da avaliação o exigir — mesma regra já usada por qualquer outro Role ocupado por Agent. |
| **Organization & Tenancy** | `Registry.list(bound_to=...)` já particiona por `org.<id>` (Organization & Tenancy §6.3, Registry §10); agregação de Compliance por Organization é uma consulta, não um mecanismo novo. |
| **Testing** | `TestRunReport`/`Evidence{TEST_RESULT}` (Testing §6, já antecipado em Testing §17 como dependência de Compliance) é a fonte de Evidence para `EvaluationMethod.kind = DYNAMIC` (§4.2, `collect_evidence`) — **forward-reference fechado nesta ratificação**, sem alteração a Testing Architecture. |
| **Packaging & Distribution** | Nenhuma integração direta; um Bundle (Packaging & Distribution §4) não é avaliado por Compliance — seus Components constituintes o são, individualmente, após importação e Admissão. |

---

## 13. Validação Institucional

| Documento base | Resultado | Evidência |
|---|---|---|
| Constitution | **PASS** | `INDETERMINATE` e `CLAIM_PARTIAL_REJECTED` honram Confiança verificável; waiver preserva Auditabilidade em ambas as granularidades |
| Kernel | **PASS** | Somente leitura de Manifests; nenhum Contract alterado |
| Governance | **PASS** | §11, §12, §13, §14, §15 reutilizados integralmente; nenhuma autoridade nova |
| Domain Model v1.1.0 | **PASS** | Assessment=Execution, Evidence=Evidence, Report/Claim=Artifact, Waiver=Decision — zero adições |
| RFC-DM-001 | **PASS** | C2 como precondição (CM3); C1 e C3 intocados |
| Identity & Namespace | **PASS** | ULID e Versioned Identifier reutilizados |
| Registry & Discovery | **PASS** | Somente leitura (CM1) |
| Validation & Certification | **PASS** | Fornece Evidence e Claims; nunca decide (CM8) — distinção preservada; fecha operacionalmente o forward-reference de L3 (Standards §8.4) |
| Composition | **PASS** | Avalia Assembly quando `applies_at=COMPOSITION` |
| Workflow | **PASS** | Consumido por Gate; não vira Gate (CM12) |
| Execution | **PASS** | Assessment é Execution; imutabilidade e concorrência herdadas |
| Standards v1.0.0 (ratificado) | **PASS** — revalidado contra a versão final, não o rascunho do Bloco 4 | `QualifiedRequirementIdentifier` (§5.1), `resolve_effective_requirements` (§10.1), `ConformanceClaim` (§8.1, agora emitido por este documento, §4.3), Standard Package (§9, atravessado sem caso especial) |
| Policy v1.0.0 (ratificado) | **PASS** — revalidado contra a versão final, não o rascunho do Bloco 4 | `resolve_effective_policy_set` com `plane` (§10.1), `ResolvedBinding.conformance_mode` (§5.3.1, consumido por §4.4 — lacuna fechada), `resolution_trace` (§9.2) |
| Template | **PASS** — validado nesta ratificação | Nenhuma superfície de contato; Compliance não gera Templates |
| Skill | **PASS** — validado nesta ratificação | `procedure_ref` de `EvaluationMethod` **MAY** ser Skill (§12), sem extensão de Skill Architecture |
| Observability | **PASS** — validado nesta ratificação | `query_events()`/`trace()` (§7) consumidos por `DetectDrift` sem alteração |
| Agent | **PASS** — validado nesta ratificação | `performed_by: Role` ocupável por Agent sob AG4 (§4.1), sem exceção nova |
| Organization & Tenancy | **PASS** — validado nesta ratificação | Agregação por Organization é consulta sobre partição de Registry já existente (§6.3) |
| Testing | **PASS** — validado nesta ratificação; forward-reference fechado | `TestRunReport`/`Evidence{TEST_RESULT}` como fonte de `DYNAMIC` (§12), antecipado por Testing §17 |
| Packaging & Distribution | **PASS** — validado nesta ratificação | Sem superfície de contato direta; Bundle não é sujeito de Compliance |
| **Exige RFC?** | **Não** | Vigésimo primeiro documento consecutivo sem necessidade de emenda ao Domain Model, Kernel ou Governance |

---

## 14. Dependências Futuras

**Fechadas nesta ratificação** (estavam listadas como abertas no rascunho do Bloco 4): Testing Architecture — `Evidence{TEST_RESULT}` para `EvaluationMethod.kind = DYNAMIC` (§12); Organization & Tenancy Architecture — agregação de Compliance por Organization (§12).

**Ainda aberta, sem mudança de status:** Observability & Provenance Storage Architecture (`[LACUNA proposital]` já declarada em Execution §14) armazenará séries históricas de Reports e Claims para análise de drift em escala arbitrária — Observability Architecture (ratificada) já fornece `query_events()`/`trace()` dentro da janela de retenção corrente (§3, §12), o que cobre o caso comum mas não substitui o armazenamento em escala; o contrato conceitual já fixado (`query by orchestration_id/coordinate/time_range`) permanece válido e não deve mudar quando aquele documento for escrito.

---

## 15. Critério de Aceitação

### ✔ Checklist Institucional

| Critério | Status |
|---|---|
| Compliance distinto de Certification, sem sobreposição de autoridade | ✔ §1 |
| Compliance Assessment = Execution, sem lifecycle novo | ✔ §4.1, §4.8 |
| Conformance Claim (Standards §8.1) emitido, não redefinido | ✔ §4.3, CM15 |
| `ResolvedBinding.conformance_mode` (Policy §5.3.1) determina satisfação do Binding | ✔ §4.4, CM14 |
| Waiver/Risk Acceptance reusam integralmente Governance §15, em duas granularidades | ✔ §4.7 |
| Zero entidade/relação/estado/autoridade nova | ✔ §4, §11 |
| UML, sequência, algoritmos, casos extremos, RFC2119 | ✔ §6-§11 |
| Validado contra os 20 documentos ratificados anteriores, incluindo os 7 posteriores ao rascunho original | ✔ §13 |
| Nenhuma RFC necessária | ✔ §13 |

### ✔ Confirmação Explícita

**Nenhum documento da base normativa foi alterado.** A única correção substantiva desta ratificação em relação ao rascunho do Bloco 4 — a introdução de `BindingSatisfaction` (§4.4) — não modifica Standards nem Policy; ela **consome** um campo (`conformance_mode`) que Policy já define desde sua própria ratificação v1.0.0, e que o rascunho original de Compliance simplesmente antecedia. `ConformanceClaim` é emitido, não redefinido. Compliance Architecture fecha o vigésimo primeiro documento da base normativa, e o último cuja ratificação permanecia pendente desde o Bloco 4.

---

*Fim do documento. Versão 1.0.0.*
