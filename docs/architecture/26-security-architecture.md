# Security Architecture
### Framework Eng — A Especialização de Segurança sobre a Base Já Ratificada

*Versão 1.0.0 · Base normativa (congelada): Constitution · Kernel · Governance · Domain Model v1.1.0 · RFC-DM-001 · Identity & Namespace · Registry & Discovery · Validation & Certification · Composition Architecture · Workflow Architecture · Execution Architecture · Standards Architecture · Policy Architecture · Template Architecture · Skill Architecture · Agent Architecture · Testing Architecture · Quality Gate Architecture · RFC-COMP-001*

> **Tese central deste documento, provada seção a seção:** `Security` não é um mecanismo — é um **domínio de conteúdo** expresso inteiramente por `Standard` (o quê), `Policy` (quando/para quem), `Skill`/`Agent` (quem verifica), `Testing` (como se produz Evidence) e `Quality Gate` (quando isso bloqueia progresso). Este documento não define nenhuma quinta camada acima dessas cinco — **nomeia** vinte e um controles de segurança já exaustivamente expressáveis por elas, e mostra, com proveniência exata, como cada um se resolve sem exceção.

---

## 1. Posição Arquitetural

Este documento ocupa uma posição dupla, ambas de puro consumo:

```
Standards Architecture (Documento 12)          Policy Architecture (Documento 13)
   │  fornece a gramática de NormativeRequirement    │  fornece scope/enforcement_mode
   ▼                                                  ▼
        Security Architecture  ◄── este documento (nomeia conteúdo, não mecanismo)
   │                                                  │
   ▼                                                  ▼
Testing Architecture (Documento 24)          Quality Gate Architecture (Documento 25)
   fornece TestKind/Evidence                    fornece a sequência de Steps que bloqueia
```

**Regra de posicionamento central:** assim como Quality Gate Architecture (Documento 25) é uma camada de nomeação sobre Workflow (*"Quality Gate é apenas um Workflow especializado"*), Security Architecture é uma camada de nomeação sobre Standards + Policy + Testing + Quality Gate — **um nível acima**, na mesma disciplina recursiva. Nenhum documento nesta cadeia introduz mecanismo abaixo do que o documento anterior já définia; cada um apenas **cataloga uma convenção de uso**.

Esta arquitetura já é demonstrável com dado real do próprio repositório: `core/skill.static-analysis.code-review` (Reference Cycle 1, já certificado e executado pelo Runtime — ver `RUNTIME.md`) já detecta segredos em texto plano (`sk-live-`/`sk_live_`); `core/skill.security.dependency-audit` já classifica `event-stream@3.3.6` como crítico. Security Architecture não inventa esses controles — **nomeia institucionalmente o que já roda**.

---

## 2. Objetivos

| # | Objetivo | Como este documento o realiza |
|---|---|---|
| O1 | Provar que Security é especialização de Standards/Policy/Testing/Quality Gate, nunca mecanismo novo | §4 |
| O2 | Catalogar os vinte e um controles obrigatórios, cada um como uso nomeado de um construto já existente | §4.5 |
| O3 | Demonstrar que `Secrets Scan`, `Security Scan`, `Dependency Audit`, `Regression`, `Publication` são instâncias já cobertas pelo catálogo de dezoito Gates do Documento 25, sem alterá-lo | §8.2 |
| O4 | Provar formalmente que nenhum novo Runtime, Registry, Lifecycle ou Scheduler é necessário | §16 |
| O5 | Formalizar como um projeto construído sobre o Framework Eng impede código inseguro de alcançar produção (**Objetivo Prático**) | §8, §18 |

---

## 3. Escopo

### 3.1 Pertence

Como requisitos de segurança são declarados (Standard), avaliados (Policy + Testing), como produzem Evidence (Testing §9), como influenciam Certification (Validation & Certification §5, L3), como bloqueiam Publication (Quality Gate §9, `BlockPublication`), como interagem com Policy (`enforcement_mode`, `scope`).

### 3.2 Não pertence — com justificativa individual

| Excluído | Justificativa técnica |
|---|---|
| **Firewall, VPN, IAM específico, segurança de nuvem (AWS/Azure/GCP/Kubernetes)** | Infraestrutura de execução, não modelo institucional — mesma fronteira que Standards §3.2 traça para "formato físico de serialização" |
| **Criptografia proprietária, protocolos próprios** | Este documento não inventa primitiva criptográfica ou protocolo — reutiliza `Integrity` (manifest_digest, Validation & Certification §6) já normatizado |
| **Ferramentas específicas** | Nenhuma tecnologia é mandatada — mesma disciplina de Testing §3.2 (nenhum framework de teste específico) |
| **Autenticação técnica (verificação de credencial)** | Explicitamente fora de escopo desde Identity & Namespace §1: *"Este documento não trata de autenticação, autorização ou controle de acesso... competência futura de uma camada de Permission/RBAC ainda não especificada."* Este documento **não fecha** essa lacuna — apenas formaliza a Autorização institucional já existente (Governance §2/§8), distinta de Autenticação técnica (ver §4.5, linha `Authentication`) |

---

## 4. Modelo Conceitual

### 4.1 Prova de minimalidade — tabela de proveniência

**Este documento introduz zero entidades, zero Value Objects, zero algoritmos com corpo lógico próprio.**

| Conceito pedido | Resolução | Provado em |
|---|---|---|
| **Security Requirement** | **É** `NormativeRequirement` (Standards §4.3) — um NR cujo `target`/`rationale` versa sobre um domínio de segurança; nenhum campo além dos já definidos | §4.2 |
| **Security Control** | **É** `PolicyBinding` (Policy §5.3) — vincula o Security Requirement acima a um `enforcement_mode` e a um escopo | §4.3 |
| **Security Finding** | **É** um item estruturado dentro de `Artifact.content` (Domain Model §2 #7) — a mesma forma já usada por `core/skill.static-analysis.code-review` (`findings[]`) e `core/skill.security.dependency-audit` (`vulnerabilities[]`) | §4.4 |
| **Security Evidence** | **É** `Evidence` (Domain Model §13), produzida por `CollectEvidence` (Testing §9) — referencia a Execution que produziu os Findings, nunca os duplica | §4.4 |

| Conceito usado por Security | Definido em |
|---|---|
| `NormativeRequirement`, `ComplianceTarget`, `EvaluationMethod`, `EvidenceRequirement`, `precedence_level=GLOBAL` | Standards Architecture §4 |
| `PolicyBinding`, `PolicyScope`, `PolicyCondition`, `enforcement_mode`, `overrides` | Policy Architecture §5 |
| `TestCase`, `TestKind=SECURITY`, `ExecuteTestSuite`, `ExecuteTestCase`, `EvaluateResult`, `CollectEvidence` | Testing Architecture §4, §9 |
| Catálogo de dezoito Gates (`Security Scan`, `Dependency Audit`, `Regression Test`, `Publication`) | Quality Gate Architecture §4.3 |
| `Execution`, `Artifact`, `Evidence`, `Context Snapshot` | Domain Model §2, §8, §13; RFC-DM-001 §3.2 |
| `Decision`, `Decision Record`, `Role`, autoridade (Governance §2/§8) | Domain Model §14; Governance §2, §8 |
| Rastreabilidade obrigatória de toda Output Entity | Domain Model §15 |
| `manifest_digest`, Integrity | Validation & Certification §6 |
| Reserva permanente de nome (dependency confusion) | Identity & Namespace §3.2 |
| `Exception Process` | Governance §15 |
| `InvokeSkillStep`, `InvokeAgent` | Skill Architecture §9; Agent Architecture §9 |
| `EnumerateSlots` | RFC-COMP-001 §4 |

### 4.2 Security Requirement = NormativeRequirement

`[ESCOLHA DE DESIGN]`

**Motivação:** decidir como um requisito de segurança é expresso institucionalmente.

**Alternativa rejeitada:** um construto `SecurityRequirement` próprio, com força normativa e semântica distintas de `NormativeRequirement`.

**Justificativa técnica:** `NormativeRequirement` (Standards §4.3) já é genérico o suficiente — `rid`, `normative_keyword` (RFC 2119), `target`, `evaluation` — para expressar qualquer regra de segurança sem adaptação. Um Standard de segurança (ex.: `core/standard.security.secrets-management`) **é** um `Standard` comum, cujo único traço distintivo é o domínio do conteúdo de seus NRs — exatamente como Standards §1.1 já proíbe um Standard de "conhecer contexto", nenhum Standard de segurança pode, tampouco, introduzir um segundo tipo de requisito. A maioria dos Standards de segurança **SHOULD** declarar `precedence_level = GLOBAL` (Constitution, hierarquia de precedência) — o que já implica, sem nenhuma regra nova, `retention = PERMANENT` para toda `EvidenceRequirement` (Standards ST9).

### 4.3 Security Control = PolicyBinding

`[ESCOLHA DE DESIGN]`

**Motivação:** decidir como um requisito de segurança se torna exigível.

**Justificativa técnica:** exatamente o mesmo mecanismo de qualquer `PolicyBinding` (Policy §5.3) — vincula um Security Requirement (§4.2) a um `conformance_level`, com `conformance_mode = STRICT` obrigatório quando o Standard for `GLOBAL` (Policy §5.3.1, PL15, já mandatório, sem exceção para segurança). A maioria dos Security Controls **SHOULD** declarar `enforcement_mode = BLOCKING` — mas isso é uma recomendação de uso, não uma regra nova; `ADVISORY`/`AUDIT_ONLY` continuam válidos para ambientes de experimentação (mesma justificativa de Policy §5.4).

### 4.4 Security Finding e Security Evidence

`[ESCOLHA DE DESIGN]`

**Motivação:** decidir como o resultado observável de uma verificação de segurança é representado.

**Justificativa técnica:** um "achado" de segurança **não é uma Evidence** — é o conteúdo bruto que uma Skill/Agent de segurança produz como `Artifact` de sua própria `Execution` (Domain Model §2 #7). Isto já está em produção institucional: `core/skill.static-analysis.code-review` produz `Artifact.content.findings[]` com `{ file, line, severity, category, description, suggestion }`; `core/skill.security.dependency-audit` produz `Artifact.content.vulnerabilities[]` com `{ package, version, severity }`. Nenhuma estrutura nova é necessária — este documento apenas nomeia esse item de conteúdo já existente como **Security Finding**.

**Security Evidence**, por sua vez, **é** `Evidence` (Domain Model §13) — o mesmo que `CollectEvidence` (Testing §9) já produz para qualquer `TestCase`, com `result = FAIL` sempre que ao menos um Security Finding tiver severidade bloqueante (§9, `EvaluateSecurity`). A Evidence referencia a Execution que produziu os Findings (`subject_execution`) — nunca os copia para dentro de si, preservando a regra de proveniência única (Domain Model §15).

### 4.5 Catálogo institucional dos vinte e um controles

Cada linha é uma **especialização nomeada** de um construto já existente — nunca mecanismo novo.

| # | Controle | Realização institucional | Provido por |
|---|---|---|---|
| 1 | Secrets Management | Standard (`core/standard.security.secrets-management`) + Skill detectora (já existente, `core/skill.static-analysis.code-review`) | Standards §4; conteúdo já em produção |
| 2 | Dependency Audit | `TestKind = SECURITY`/capability `security.dependency-audit` — mesma Skill já existente | Testing §4.5; Quality Gate §4.3 (Gate 13) |
| 3 | SAST (Static Application Security Testing) | `EvaluationMethod.kind = STATIC` ou `DYNAMIC` via Skill de análise estática, `ComplianceTarget.applies_to = ARTIFACT` | Standards §4.6; Quality Gate §4.3 (Gate 4, Static Analysis) |
| 4 | DAST (Dynamic Security Testing) | `TestKind = SECURITY`, `EvaluationMethod.kind = DYNAMIC`, `ComplianceTarget.applies_to = EXECUTION` (sujeito vivo, não apenas Artifact) | Testing §4.5; Standards §4.6 |
| 5 | Input Validation | `inputs` (Kernel §2.4) + `Variable.constraint` (Template §4.2) + Validação Estrutural (Kernel §8) | Kernel §2.4, §8; Template §4.2 |
| 6 | Output Validation | `outputs` (Kernel §2.5) + SK9 (Skill §14, "Artifact produzido MUST conformar a outputs") | Kernel §2.5; Skill §14 |
| 7 | Authentication | **Fora de escopo, explicitamente** (Identity & Namespace §1) — não fechado aqui, não inventado aqui | Identity & Namespace §1 |
| 8 | Authorization | Autoridade de `Role` (Governance §2, §8, "Quem Pode Alterar o Quê") + `PolicyScope.roles` (Policy §5.2) | Governance §2, §8; Policy §5.2 |
| 9 | Least Privilege | `PolicyScope.roles`/`capabilities` restrito ao mínimo necessário — convenção de configuração, não mecanismo | Policy §5.2 |
| 10 | RBAC | `Role` (Governance §2) + `PolicyScope.roles` — já é, literalmente, Role-Based Access Control | Governance §2; Policy §5.2 |
| 11 | Rate Limiting | `PolicyCondition` (Predicate<Context>, Policy §5.2) avaliando um `Metric` (Domain Model §2 #14) de frequência de Execution, com `enforcement_mode = BLOCKING` | Policy §5.2, §5.4; Domain Model §2 #14 |
| 12 | Sensitive Data | Standard de classificação de dado + Skill de varredura — mesmo padrão de Secrets Management (#1) | Standards §4; Testing §4.5 |
| 13 | PII | Idem #12, `ComplianceTarget.applies_to = ARTIFACT` | Standards §4.5 |
| 14 | LGPD | Standard (o requisito legal) + Policy (`scope.namespaces` restrito às organizações sob jurisdição) — mesma separação Standard/Policy já estabelecida | Standards §1.1; Policy §5.2 |
| 15 | Logging Seguro | NR exigindo que `Context Snapshot`/`Artifact` **MUST NOT** conter Security Finding de categoria `secret`/`PII` sem redação | RFC-DM-001 §3.2; Standards §4.3 |
| 16 | Audit Trail | Integralmente já existente — Domain Model §15 (rastreabilidade obrigatória) + Governance §12 (Audit) | Domain Model §15; Governance §12 |
| 17 | Integrity | Já nomeado e definido — Validation & Certification §1, §6 (`manifest_digest`, mismatch invalida) | Validation & Certification §1, §6 |
| 18 | Supply Chain | Reserva permanente de nome, justificada explicitamente contra *dependency confusion* | Identity & Namespace §3.2 |
| 19 | Configuration Review | Gate `Documentation Review` (Quality Gate §4.3, Gate 16) aplicado a `constraints`/`compatibility`/`metadata` em vez de `purpose`/`validation` | Quality Gate §4.3 |
| 20 | Security Regression | Gate `Regression Test` (Quality Gate §4.3, Gate 11), `standard_ref` a um Standard de segurança | Testing §4.5; Quality Gate §4.3 |
| 21 | Threat Review | Gate de aprovação (Quality Gate §4.3, Gates 1-3), `role_class` orientado a segurança, `EvaluationMethod.kind = ATTESTED` | Quality Gate §4.3; Standards §4.6 |

---

## 5. Manifest

**Nenhum campo novo.** Todo controle do catálogo (§4.5) é expressável por campos já existentes:

| Necessidade | Já resolvido por |
|---|---|
| Quais Standards de segurança um Component deve satisfazer | `metadata.standards_bound` (Kernel §2.14) |
| Sob quais condições um controle é `BLOCKING` | Effective Policy Set (Policy §9) |
| Quais `TestCase` de segurança um Component possui | `test_suite[]` (Testing §5) |

`[ESCOLHA DE DESIGN]` Não introduzir `metadata.security_profile` ou campo equivalente — mesma justificativa de Quality Gate §5: duplicaria o que `standards_bound` + Policy já respondem deterministicamente.

---

## 6. Contract

Nenhuma refinação de `inputs`/`outputs` além da já existente. O "contrato" de um controle de segurança é inteiramente o `NormativeRequirement`/`PolicyBinding` que o declara (§4.2-§4.3) mais o `TestCase`/`Step` que o executa (Testing §4.4, Quality Gate §4.2) — nenhuma terceira camada de contrato.

---

## 7. Modelo Operacional

| Operação | Definida em | Especialização para Security |
|---|---|---|
| Declaração de requisito | Standards §4 | NR com domínio de segurança, tipicamente `precedence_level = GLOBAL` |
| Aplicabilidade | Policy §5-§8 | `PolicyBinding` com `enforcement_mode` tipicamente `BLOCKING` |
| Execução da verificação | Testing §9 (`ExecuteTestCase`) | `TestKind = SECURITY`, ou Gate automatizado (Quality Gate §9) |
| Certificação | Validation & Certification §5, L3 | *"L3 MUST exigir Strict Conformance a todo Standard vinculado"* (Standards §8.4) — um Standard de segurança não certificado impede L3 sem exceção |
| Bloqueio de Publication | Quality Gate §9 (`ApprovePublication`) | Ver §9 abaixo, `BlockPublication` |

---

## 8. Fluxo

### 8.1 Fluxo de uma verificação de segurança individual

```
1. Standard de segurança declarado (ex.: core/standard.security.secrets-management)      [Standards §4]
2. Policy vincula o Standard, enforcement_mode=BLOCKING, scope.namespaces=[...]           [Policy §5]
3. TestCase(kind=SECURITY, standard_ref=<NR do Standard>) declarado em test_suite[]        [Testing §4.4]
4. ExecuteTestCase → InvokeSkillStep(core/skill.static-analysis.code-review, ...)          [Testing §9; Skill §9]
5. Artifact.content.findings[] produzido (Security Finding)                                [§4.4]
6. EvaluateSecurity(artifact) → PASS | FAIL                                                 [§9]
7. CollectEvidence → Security Evidence (Evidence, result=FAIL se houver Finding bloqueante) [§9; Testing §9]
8. Evidence alimenta: (a) Conformance Claim (Standards §8.1); (b) Score de Certificação (Validation & Certification §6)
```

### 8.2 Integração explícita com Quality Gate (Documento 25) — reuso, não alteração

Os cinco Gates pedidos já existem, sem modificação, no catálogo de dezoito Gates do Documento 25:

| Gate pedido | Linha do catálogo (Quality Gate §4.3) | Como Security o especializa |
|---|---|---|
| **Secrets Scan** | Gate 12, `Security Scan` (`GATE_AUTO`, `TestKind=SECURITY`) | `standard_ref` aponta ao Standard de Secrets Management (§4.5, #1) — mesma linha do catálogo, `standard_ref` distinto |
| **Security Scan** | Gate 12, `Security Scan` — tal qual, sem especialização adicional | `standard_ref` a qualquer Standard de segurança geral |
| **Dependency Audit** | Gate 13, `Dependency Audit` (`GATE_AUTO`, capability `security.dependency-audit`) | Já é a Skill de segurança real (`core/skill.security.dependency-audit`) — nenhuma mudança |
| **Regression** | Gate 11, `Regression Test` | `standard_ref` a um Standard de segurança — mesma linha, `TestKind=REGRESSION`, disparada por `ClassifyXChange=MAJOR` |
| **Publication** | Gate 18, `Publication` (`INVOCATION`, capability `registry.publish_version`) | Gateada por `ApprovePublication`/`BlockPublication` (§9) — mesmo Gate, precondição de segurança adicionada via `enforcement_mode=BLOCKING`, não via novo Gate |

**Nenhuma linha do catálogo de Quality Gate Architecture é alterada, adicionada ou removida.** Security Architecture apenas preenche `standard_ref`/`capability` com conteúdo de domínio de segurança — exatamente a mesma relação que "Formatting" tem com "Lint" no próprio catálogo do Documento 25 (mesma linha, Standard distinto).

---

## 9. Algoritmos

**Nenhum algoritmo novo com lógica de decisão própria.** Os cinco nomes pedidos são composição pura sobre Testing e Quality Gate.

```
ALGORITMO ExecuteSecurityReview(component_ref, test_case, requester_ns):
  # é ExecuteGate (Quality Gate §9) para o Gate que realiza o controle de segurança pedido (§8.2)
  RETORNA ExecuteGate(step_do_gate_de_seguranca, ctx)                          # Quality Gate §9 — verbatim


ALGORITMO EvaluateSecurity(artifact):
  findings ← artifact.content.get("findings", []) ∪ artifact.content.get("vulnerabilities", [])  # §4.4
  bloqueantes ← [f PARA f EM findings SE f.severity ∈ {"blocker", "critical"}]
  RETORNA (bloqueantes = ∅) ? PASS : FAIL                                       # mesma forma de EvaluateResult, Testing §9


ALGORITMO CollectSecurityEvidence(test_case, execution, resultado):
  RETORNA CollectEvidence(test_case, execution, resultado)                     # Testing §9 — verbatim,
                                                                                 # evidence_kind já cobre
                                                                                 # TEST_RESULT/ANALYSIS_OUTPUT


ALGORITMO ApproveSecurityGate(gate_evidence):
  RETORNA EvaluateGate(gate_evidence)                                          # Quality Gate §9 — verbatim


ALGORITMO BlockPublication(component_ref, security_evidences):
  criticos ← [e PARA e EM security_evidences
              SE e.policy.enforcement_mode = BLOCKING E e.result = "FAIL"]
  SE criticos ≠ ∅:
     RETORNA RejectGate(...)                                                   # Quality Gate §9 — verbatim,
                                                                                 # nunca chega a Publication (Gate 18)
  RETORNA ApprovePublication(component_ref, security_evidences)                # Quality Gate §9 — verbatim
```

Todos os cinco delegam integralmente a `ExecuteGate`/`EvaluateGate`/`EvaluateResult`/`CollectEvidence`/`ApprovePublication`/`RejectGate` (Testing §9, Quality Gate §9) — nenhuma nova assinatura de dispatch, nenhuma nova regra de decisão.

---

## 10. Diagramas

### 10.1 UML — Security como conteúdo, não mecanismo

```
┌─────────────────────────┐        ┌──────────────────────┐
│ Standard (domínio: sec.)  │──────►│ NormativeRequirement    │  [Standards §4]
└─────────────────────────┘        └──────────┬───────────┘
                                                │ vinculado por
                                                ▼
                                     ┌──────────────────────┐
                                     │ PolicyBinding          │  [Policy §5.3]
                                     │  enforcement_mode      │
                                     └──────────┬───────────┘
                                                │ avaliado via
                                                ▼
┌────────────┐   produces  ┌────────────────────┐   contém    ┌──────────────────┐
│ Execution   │────────────►│ Artifact             │────────────►│ Security Finding   │  [Domain Model §7]
│ (Skill/Agent│             │ (findings/           │             │  «item, não Entity»│
│  de segurança)│           │  vulnerabilities)    │             └──────────────────┘
└──────┬─────┘             └────────────────────┘
       │ referenciado por
       ▼
┌─────────────┐
│  Evidence     │  (Security Evidence)   [Domain Model §13]
│  result=PASS|FAIL│
└──────┬──────┘
       │ alimenta
       ▼
┌──────────────────────────┐        ┌────────────────────┐
│ Conformance Claim           │──────►│ Certification (L3+)  │  [Standards §8.1; Validation & Certification §5]
└──────────────────────────┘        └────────────────────┘
       │
       ▼
┌──────────────────────────┐
│ Quality Gate (Documento 25) │──BlockPublication──► Publication (Gate 18)
└──────────────────────────┘
```

### 10.2 Sequência — segredo encontrado bloqueia Publication

```
Workflow(Quality Gate)   Composition   Skill(code-review)   Testing        Standards/Policy    Registry
        │                    │              │                  │                 │               │
        ├─Step(Secrets Scan)►│              │                  │                 │               │
        │                    ├─ResolveSlot──►│                  │                 │               │
        │                    │◄─candidate───┤                  │                 │               │
        ├─ExecuteSecurityReview──────────────►│                  │                 │               │
        │                                    ├─InvokeSkillStep──►│                 │               │
        │                                    │◄─Artifact{findings:[{severity:"blocker",category:"secret"}]}
        │                                    ├─EvaluateSecurity → FAIL             │               │
        │                                    ├─CollectSecurityEvidence─────────────►│ (Evidence FAIL)│
        ├─ApproveSecurityGate = BLOCK                                              │               │
        ├─RejectGate → FailurePolicy(ABORT)                                        │               │
        │                                                                          │               │
        │   [Publication NUNCA é alcançada — Gate 18 nunca despachado]             │               │
        │                                                                          │               │
        │   [se o Finding for posteriormente avaliado como falso positivo]         │               │
        │                                                                          Governance §15   │
        │                                                                          (Exception Process,│
        │                                                                           prazo, dono, registro)│
```

### 10.3 Estados

Nenhum diagrama de estados novo. Mesma disciplina de Quality Gate §10.3, Testing §10.3, Agent §10.3, Skill §10.3.

---

## 11. Casos Extremos

| # | Caso | Tratamento |
|---|---|---|
| CE1 | Segredo encontrado | Finding `category=secret`, `severity=blocker` (mesma detecção já em produção em `code-review`) → `EvaluateSecurity=FAIL` → `BlockPublication` (§9) |
| CE2 | Dependência crítica | Finding `severity=critical` (mesmo padrão de `dependency-audit`, `event-stream@3.3.6`) → idem CE1 |
| CE3 | Policy negando execução | `enforcement_mode=BLOCKING`, `applies_at=EXECUTION/WORKFLOW` (Policy §5.4, §8) — mesmo tratamento de Testing CE6/Quality Gate CE6, sem exceção para segurança |
| CE4 | Credencial inválida | A verificação técnica de credencial permanece fora de escopo (§3.2, CE do controle #7) — a **consequência institucional** de uma falha desse tipo (quando reportada por um mecanismo externo) é `Unauthorized` (Registry §13, classe de erro já existente) |
| CE5 | RBAC insuficiente | `Role` sem autoridade declarada para a Decision pretendida (Governance §8) → `Unauthorized`, mesma classe |
| CE6 | PII detectado | Finding `category=pii` → idem CE1 |
| CE7 | LGPD violada | Non-Conformance (Standards §8.2) ao Standard de LGPD vinculado → Conformance Claim `NON_CONFORMANCE` → Gate `BLOCK` |
| CE8 | Security Scan falhou | Mesmo tratamento de Quality Gate CE10, sem exceção |
| CE9 | Falso positivo | **MUST** ser tratado exclusivamente via Exception Process (Governance §15: motivo, prazo, dono, condição de encerramento) — **MUST NOT** ser suprimido silenciosamente (SEC6, §14) |
| CE10 | Evidence conflitante | Regra de Integrity (Validation & Certification §6) — `manifest_digest` divergente invalida Evidence associada, nunca reconciliada silenciosamente |
| CE11 | Execution interrompida | Transita a `Aborted` (Domain Model §8) — mesma regra de qualquer interrupção |
| CE12 | Retry | Sempre nova Execution (EX1, Execution §12; WF5, Workflow §12) — nunca reabertura |
| CE13 | Publication bloqueada | `BlockPublication` (§9) impede o dispatch de Gate 18 — Publication nunca ocorre enquanto houver Security Evidence `FAIL` sob `enforcement_mode=BLOCKING` |

---

## 12. Performance

| Recurso | Regra de cache/complexidade | Origem |
|---|---|---|
| Resolução de Standard/Policy de segurança | Cache indefinido para Standard (Standards §15.1); TTL/invalidação por evento para Policy (Policy §15.1) | Standards §15.1; Policy §15.1 |
| Security Evidence reutilizada por Certificação | Reuso sem recoleta enquanto `manifest_digest` não mudar (mesma regra de Quality Gate §9.1) | Testing §12; Quality Gate §12 |
| Execução de `TestKind=SECURITY` | O(número de TestCase de segurança) — mesma ordem de Testing §12 | Testing §12 |

**Nenhuma política de cache nova.**

---

## 13. Eventos

**Nenhum evento novo.** Tabela de eventos já existentes:

| Evento | Origem |
|---|---|
| `StepDispatched`/`StepCompleted`/`StepFailed`, `GateEvaluated`/`GatePassed`/`GateBlocked` | Execution §11; Workflow §11 |
| Eventos de `ExecuteTestCase`/`ExecuteTestSuite` | Testing §13 |
| `EffectiveRequirementsResolved`, `PartialConformanceClaimed`, `IllegalGlobalOverrideAttempted` | Standards §16 |
| `EffectivePolicySetResolved`, `PolicyConflictResolved` | Policy §16 |
| `ComponentRegistered`/`VersionPublished` (Publication) | Registry §11 |

---

## 14. Regras Normativas (RFC 2119)

| # | Regra | Nível |
|---|---|---|
| SEC1 | Secrets MUST NOT existir em texto plano em Artifact ou Context Snapshot — Finding `category=secret` com `severity=blocker` MUST bloquear Publication | MUST |
| SEC2 | Dependências com Finding `severity=critical` MUST bloquear Publication | MUST |
| SEC3 | Toda Skill/Agent com `standards_bound` a um Standard de segurança SHOULD possuir Threat Review antes de Certificação L3 | SHOULD |
| SEC4 | Toda alteração classificada MAJOR (qualquer `ClassifyXChange`) em um Component com Standard de segurança vinculado MUST executar Security Regression antes de Publication | MUST |
| SEC5 | Security Evidence MUST ser preservada com `retention=PERMANENT` quando o Standard vinculado for `precedence_level=GLOBAL` (Standards ST9, reutilizado) | MUST |
| SEC6 | Um Finding avaliado como falso positivo MUST ser tratado exclusivamente via Exception Process (Governance §15) — MUST NOT ser suprimido silenciosamente | MUST / MUST NOT |
| SEC7 | Nenhuma Policy MUST suprimir, por `overrides`, um `PolicyBinding` cujo Standard de segurança seja `precedence_level=GLOBAL` (PL4, reutilizado sem exceção) | MUST NOT |
| SEC8 | Este documento MUST NOT introduzir mecanismo de autenticação técnica — permanece fora de escopo (Identity & Namespace §1) | MUST NOT |
| SEC9 | RBAC MUST ser expresso exclusivamente via `Role` (Governance §2) + `PolicyScope.roles` (Policy §5.2) — MUST NOT introduzir sistema de permissão paralelo | MUST / MUST NOT |
| SEC10 | Rate Limiting MUST ser expresso como `PolicyCondition` sobre um `Metric` já existente — MUST NOT introduzir mecanismo de contagem/agendamento novo | MUST / MUST NOT |
| SEC11 | Proteção de Supply Chain (dependency confusion) MUST reutilizar a reserva permanente de nome já normatizada (Identity & Namespace §3.2) — MUST NOT introduzir segundo mecanismo | MUST / MUST NOT |
| SEC12 | Toda Execution de um controle de segurança MUST produzir Evidence, mesmo quando o resultado é `FAIL` — MUST NOT omitir silenciosamente uma falha | MUST / MUST NOT |
| SEC13 | Este documento MUST NOT mandatar tecnologia, protocolo ou ferramenta de segurança específica | MUST NOT |
| SEC14 | Audit Trail de segurança MUST reutilizar integralmente a rastreabilidade já obrigatória (Domain Model §15) — MUST NOT introduzir mecanismo de log paralelo | MUST / MUST NOT |
| SEC15 | Toda Skill SHOULD possuir Security Review antes de ser exposta como Provider elegível em ambiente de produção | SHOULD |

---

## 15. Integrações

| Documento | Como Security o consome — sem alteração |
|---|---|
| **Constitution** | Regra Imutável nº2 (*"Nenhum Agente pode ignorar um Standard ou Policy que se aplique a ele"*) é o mandato direto para todo controle deste catálogo |
| **Kernel** | `inputs`/`outputs`/Validação Estrutural reutilizados para Input/Output Validation (#5-#6) |
| **Governance** | Autoridade (§2, §8), Exception Process (§15, CE9), Audit (§12) reutilizados sem alteração |
| **Domain Model v1.1.0** | `Evidence`, `Artifact`, rastreabilidade (§15) reutilizados sem alteração |
| **RFC-DM-001** | Context Snapshot obrigatório em toda Execution de controle de segurança |
| **Identity & Namespace** | §1 (fora de escopo de AuthN, honrado); §3.2 (dependency confusion, base de Supply Chain) |
| **Registry & Discovery** | Publication (Gate 18) inalterada; `resolve()` usado por `ExecuteSecurityReview` |
| **Validation & Certification** | L3 (§8.4, Strict Conformance) é o gate de Certificação para todo Standard de segurança |
| **Composition** | `ResolveSlot` resolve o Provider de cada controle automatizado |
| **Workflow** | Gates de segurança são `Step(GATE_AUTO\|GATE_APPROVAL)`, sem extensão |
| **Execution** | `Dispatch` único caminho real |
| **Standards** | Fonte exclusiva de todo Security Requirement (§4.2) |
| **Policy** | Fonte exclusiva de todo Security Control (§4.3) |
| **Template Architecture** | Não referenciada diretamente além do já reutilizado por Skill |
| **Skill Architecture** | `InvokeSkillStep` é o caminho de execução de Skills de segurança (`code-review`, `dependency-audit`) |
| **Agent Architecture** | `InvokeAgent` disponível para controles que exijam decisão (ex.: Threat Review orquestrado por um Agent) |
| **Testing Architecture** | `TestKind=SECURITY`, `ExecuteTestSuite`/`ExecuteTestCase`/`EvaluateResult`/`CollectEvidence` reutilizados tal qual |
| **Quality Gate Architecture** | Cinco Gates pedidos são linhas já existentes do catálogo de dezoito (§8.2) — zero alteração |
| **RFC-COMP-001** | `EnumerateSlots` consumido indiretamente via Composition |

---

## 16. Validação Institucional

| Documento base | Resultado |
|---|---|
| Constitution | **PASS** — Regra Imutável nº2 é o mandato direto |
| Kernel | **PASS** — Inputs/Outputs/Validação Estrutural reutilizados |
| Governance | **PASS** — Autoridade, Exception Process, Audit intocados |
| Domain Model v1.1.0 | **PASS** — zero entidades novas; Finding é conteúdo de Artifact, não Entity |
| RFC-DM-001 | **PASS** — Context Snapshot obrigatório, sem exceção |
| Identity & Namespace | **PASS** — §1 honrado (AuthN fora de escopo); §3.2 reutilizado para Supply Chain |
| Registry & Discovery | **PASS** — Publication inalterada |
| Validation & Certification | **PASS** — L3/Strict Conformance reutilizado sem redefinição |
| Composition | **PASS** — `ResolveSlot` reutilizado |
| Workflow | **PASS** — `GATE_AUTO`/`GATE_APPROVAL` reutilizados, nenhum `StepKind` novo |
| Execution | **PASS** — `Dispatch` único caminho real |
| Standards | **PASS** — fonte exclusiva de Security Requirement, nunca redefinida |
| Policy | **PASS** — fonte exclusiva de Security Control, nunca redefinida |
| Template Architecture | **PASS** — não tocada |
| Skill Architecture | **PASS** — `InvokeSkillStep` reutilizado |
| Agent Architecture | **PASS** — `InvokeAgent` reutilizado |
| Testing Architecture | **PASS** — `TestKind=SECURITY` e algoritmos reutilizados tal qual |
| Quality Gate Architecture | **PASS** — catálogo de dezoito Gates reutilizado sem alteração, adição ou remoção de linha (§8.2) |
| RFC-COMP-001 | **PASS** — `EnumerateSlots` consumido sem reabertura |
| **Exige RFC?** | **NÃO** |

**Prova formal de que Security não adiciona:**

| Item vedado pelo mandato | Verificação |
|---|---|
| Runtime novo | Nenhum — `ExecuteGate`/`ExecuteTestCase`/`InvokeSkillStep`/`InvokeAgent` reutilizados (§9) |
| Registry novo | Nenhum — Registry & Discovery §5, inalterado |
| Lifecycle novo | Nenhum — Kernel §3, Domain Model §8, sem exceção |
| Scheduler novo | Nenhum — Execution §7, inalterado |
| Mecanismo paralelo (Firewall/VPN/IAM/criptografia/protocolo) | Nenhum — explicitamente fora de escopo (§3.2) |

---

## 17. Dependências Futuras

| Consumidor | O que consome | Estado |
|---|---|---|
| **Observability** | Séries históricas de Security Evidence/Findings em escala | `[LACUNA proposital]` já declarada em Execution §14 |
| **CI/CD** | A sequência de §8.1/§8.2 já é diretamente traduzível para pipeline executável | Desbloqueado |
| **Deployment** | Publication (Gate 18) gateada por segurança já é o ponto de transição que um pipeline de deployment consome | Sem bloqueio |
| **Marketplace** | Certificação L3+ com Security Evidence já fornece o sinal de confiança necessário para listagem | Sem bloqueio |

---

## 18. Critério de Aceitação

### ✔ Checklist Institucional

| Critério do mandato | Status |
|---|---|
| Security é especialização de Standards/Policy/Testing/Validation/Certification/Quality Gate/Execution/Skill/Agent | ✔ §1, §4 |
| Vinte e um controles modelados como uso de construtos já existentes | ✔ §4.5 |
| Integração explícita com Quality Gate (5 Gates pedidos) demonstrada sem alteração ao Documento 25 | ✔ §8.2 |
| Algoritmos (`EvaluateSecurity`, `ExecuteSecurityReview`, `CollectSecurityEvidence`, `ApproveSecurityGate`, `BlockPublication`) são pura composição | ✔ §9 |
| Casos extremos exaustivos, incluindo os treze pedidos | ✔ §11 |
| RFC2119 completo | ✔ §14 |
| Performance/Eventos sem novidade | ✔ §12, §13 |
| Integração completa com Testing, Quality Gate, Validation, Certification, Standards, Policy, Execution, Workflow, Skill, Agent | ✔ §15 |
| UML e diagramas de sequência | ✔ §10 |
| Prova de reutilização e tabela de proveniência completa | ✔ §4.1 |
| Validação institucional | ✔ §16 |
| Nenhuma alteração a documento anterior — RFC separada se necessário | ✔ §16 — nenhuma mudança encontrada; nenhuma RFC necessária |

### ✔ Objetivo Prático Realizado

A cadeia causal completa, sem nenhum elo hipotético, é: um Standard de segurança (§4.2) é vinculado por uma Policy `BLOCKING` (§4.3); uma Skill como `core/skill.static-analysis.code-review` ou `core/skill.security.dependency-audit` — já existentes e já executadas por este Runtime — produz Findings (§4.4) dentro de um `TestCase(kind=SECURITY)` (Testing §4.4); `EvaluateSecurity` (§9) classifica qualquer Finding bloqueante como `FAIL`; a Security Evidence resultante (§4.4) é consumida tanto pelo Gate correspondente do catálogo de Quality Gate (§8.2) quanto pela escalada de Certificação L3 (Standards §8.4, "L3 MUST exigir Strict Conformance"); `BlockPublication` (§9) impede, mecanicamente, que o Gate 18 (Publication, Quality Gate §4.3) seja alcançado enquanto essa falha existir. **Nenhum código inseguro alcança `Active` sem que essa cadeia inteira — construída inteiramente de mecanismos já ratificados antes deste documento — tenha sido percorrida e satisfeita.**

### ✔ Confirmação Explícita

**Nenhum documento da base normativa congelada foi alterado**, incluindo o catálogo de dezoito Gates do Documento 25, que permanece byte-a-byte idêntico — Security Architecture apenas preenche `standard_ref`/`capability` de linhas já existentes com conteúdo de domínio de segurança.

---

*Fim do documento. Versão 1.0.0.*
