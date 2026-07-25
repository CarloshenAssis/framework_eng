# DOCUMENTO 2 — Policy Architecture

### Framework Eng — O Mecanismo Institucional de Vinculação Normativa

*Versão 1.0.0 · Base normativa: Constitution · Kernel · Governance · Domain Model v1.1.0 · RFC-DM-001 · Identity & Namespace · Registry & Discovery · Validation & Certification · Composition · Workflow · Execution · **Standards Architecture (Documento 1 deste bloco)***

---

## 1. Posição Arquitetural

Uma `Policy` é uma especialização de **Structural Component** — categoria já nomeada em Domain Model §3. Policy Architecture especifica **o mecanismo pelo qual um Standard, em um Conformance Level determinado, torna-se exigível para um conjunto de sujeitos, sob condições e durante um período**.

**Responsabilidade institucional exclusiva:** ser a única fonte de aplicabilidade normativa do Framework. Nenhuma outra camada decide *quando* uma regra vale.

### 1.1 A assimetria fundamental

```
Standard  →  contém requisitos, ignora contexto        (Documento 1)
Policy    →  escolhe Standards, ignora requisitos      (este documento)
```

Esta assimetria é **estrutural e mecanicamente verificada**, não convencionada:
- Standard é impedido de conhecer contexto por ST1 + invariante I2 (Documento 1 §10.3).
- Policy é impedida de conter critério por PL1 + invariante J2 (§10.3 deste documento).

Nenhum dos dois pode invadir o território do outro sem que a validação falhe.

### 1.2 Fronteiras negativas (invioláveis)

| Fronteira | Regra | Detentor da responsabilidade |
|---|---|---|
| Policy não define critério | **MUST NOT** conter Normative Requirement inline | Standards Architecture |
| Policy não conhece implementação | **MUST NOT** referenciar Coordinate de Skill/Agent/Workflow concreto | Composition (resolução por Capability) |
| Policy não avalia | **MUST NOT** emitir veredito de conformidade | Compliance (downstream) |
| Policy não bloqueia diretamente | Declara `enforcement_mode`; a aplicação é executada por Gate, Admission ou Scheduler | Workflow §4; Governance §7; Execution §5 |
| Policy não cria autoridade | Aprovação por Governance Area Steward, sem exceção | Governance §8 |
| Policy não trata exceções | Waiver e Risk Acceptance são Exception Process | Governance §15 |
| Policy não tem lifecycle próprio | Kernel Lifecycle integral; vigência é **atributo**, não estado | Kernel §3 |

### 1.3 Posição na hierarquia constitucional

A Constitution posiciona Policies no **nível 5** da hierarquia de decisões, imediatamente abaixo de Standards (nível 4). Este documento opera estritamente dentro dessa subordinação: uma Policy **MUST NOT** contradizer um Standard, e **MUST NOT** suprimir um vínculo a Standard de `precedence_level = GLOBAL` (§7.3, PL4) — aplicação operacional literal da regra constitucional "o nível mais específico vence, exceto quando conflita com nível 1".

---

## 2. Objetivos e Motivação

### 2.1 Problema resolvido

Kernel §2.14 provê `standards_bound` — enumeração explícita de Standards no Manifest de cada Component. Esse mecanismo é correto, permanece válido, e **não é depreciado por este documento**. Mas é insuficiente sozinho, por quatro razões estruturais:

1. **Não escala** — exigir que cada um de milhares de Components enumere dezenas de Standards produz duplicação massiva e divergência inevitável.
2. **Não é condicional** — `standards_bound` é estático; não expressa "aplica-se apenas se a organização for do tipo X" ou "apenas em execuções de produção".
3. **Não permite mudança normativa centralizada** — elevar uma exigência institucional exigiria editar N Manifests, cada um sob seu próprio processo de Governance §7, com N janelas de aprovação independentes.
4. **Não expressa herança** — não há como declarar "tudo abaixo deste Namespace herda esta exigência".

### 2.2 Objetivos

| # | Objetivo | Mecanismo |
|---|---|---|
| O1 | Aplicabilidade declarativa e condicional | `PolicyScope` + `PolicyCondition` (§5) |
| O2 | Herança normativa ao longo da árvore de Namespaces | §7.1, ancorado em Identity & Namespace §8 |
| O3 | Resolução de conflito determinística e total | Algoritmo formal §11.1, com prova de determinismo e terminação |
| O4 | Vigência temporal sem estado novo | `effective_from`/`expires_at` como atributos (§5.5) |
| O5 | Coexistência não conflitante com `standards_bound` | Regra de união com prevalência do mais alto (§7.5) |
| O6 | Rigor proporcional ao risco | `enforcement_mode` de três valores (§5.4) |
| O7 | Aplicabilidade em todas as camadas operacionais | `applies_at` cobrindo Manifest/Composition/Workflow/Execution (§8) |

---

## 3. Escopo

### 3.1 Pertence a esta arquitetura

Estrutura formal de uma Policy; Policy Binding; Policy Scope; Policy Condition; Applicability; Enforcement Mode; Priority; Override; Conflict Resolution; Effective Policy Set e seu algoritmo de geração; Policy Evaluation; herança ao longo de Namespaces; validade temporal; políticas condicionais; e as classes nomeadas de Policy (Organization, Namespace, Execution, Workflow, Composition) como **padrões de uso**, não como subtipos.

### 3.2 Não pertence — com justificativa individual

| Excluído | Justificativa técnica |
|---|---|
| **Critério normativo** | Standards Architecture (Documento 1). Permitir critério inline criaria dois lugares onde norma pode residir — exatamente a duplicidade conceitual que RFC-DM-001 eliminou no achado C1 (colisão `Knowledge`). |
| **Avaliação de conformidade real** | Compliance (downstream). Policy declara exigência; verificar é ato independente, e Governance §12 exige independência entre quem estabelece e quem verifica. |
| **Autoridade de aprovação** | Governance §8 já a define (Governance Area Steward). Redefini-la seria duplicação de Governance — proibida pela Restrição 4 do mandato. |
| **Exceções, waivers, risk acceptance** | Governance §15 (Exception Process) já define mecanismo completo: motivo, prazo obrigatório, dono, condição de encerramento, autoridade equivalente, visibilidade pública. Uma exceção é evento sobre uma *avaliação*, não sobre a *declaração* de aplicabilidade — portanto pertence a Compliance, consumindo §15, não a Policy. |
| **Enforcement em runtime** | Policy declara `enforcement_mode`; a execução do bloqueio é de Workflow §4 (`GATE_AUTO`), Governance §7 (Admission) ou Execution §5 (dispatch). Policy nunca executa nada. |
| **Autenticação e autorização** | Explicitamente fora de escopo desde Identity & Namespace §1. `RoleClass` em Scope é critério de aplicabilidade, não controle de acesso. |
| **Modelo interno de Organization** | `[LACUNA proposital]` — Organization & Tenancy Architecture. Este documento consome o slot `org.<id>` já reservado por Identity & Namespace §8/§10, sem presumir estrutura interna. |

---

## 4. Modelo Conceitual

### 4.1 Tabela de proveniência conceitual

| Conceito | Natureza | Base / precedente estrutural |
|---|---|---|
| `Policy` | **Especializado** — Structural Component | Domain Model §3 |
| **Policy Binding** | **Value Object** interno ao Contract | Mandato §7; padrão de `Composition Slot` (Composition §4) |
| **Policy Scope** | **Value Object** interno ao Contract | — |
| **Policy Condition** | **Value Object** — `Predicate<Context>` | Mesmo padrão de `Slot.condition` (Composition §4) e `Phase.entry_predicate` (Workflow §4) |
| **Enforcement Mode** | **Value Object** enumerado | — |
| **Effective Policy Set** | **Artifact** genérico | Mandato §8; padrão de `Assembly` (Composition §4), `Execution Plan` (Execution §4), `Conformance Claim` (Doc 1 §8.1) |
| **Resolution Trace** | **Value Object** interno ao Artifact | `resolution_path` de Registry §6.1; cadeia de redirect de Identity §6.6 |
| Precedência e arbitragem | **Reutilizado** | Constitution (hierarquia); Governance §17 |
| `Capability` | **Reutilizado** | Kernel §2.9 |
| `RoleClass` | **Reutilizado** | Governance §2 |
| Namespace e ancestralidade | **Reutilizado** | Identity & Namespace §3, §8 |
| `Context` / Context Snapshot | **Reutilizado** | Domain Model §2 #5; RFC-DM-001 §3.2 |
| Identidade, versão, lineage | **Reutilizado** | Identity & Namespace §4, §5, §7 |
| Lifecycle | **Reutilizado sem alteração** | Kernel §3 |
| Detecção de ciclo | **Reutilizado (5ª aplicação)** | Kernel §7 |
| Registro e descoberta | **Reutilizado** | Registry & Discovery §3.1, §5 |

**Nenhum construto exige RFC.**

### 4.2 Por que Policy não pode conter critério

`PolicyBinding` referencia um Standard por `VersionedIdentifier`; **MUST NOT** conter `NormativeRequirement` inline. Verificado pelo invariante J2 (§10.3).

`[ESCOLHA DE DESIGN]` Proibição absoluta de critério inline, sem exceção para regras triviais. Alternativa rejeitada: permitir "inline requirements" para regras de uma linha, evitando o custo de criar um Standard mínimo. Rejeitada por três motivos: (a) produziria dois locais onde norma reside, tornando indecidível para Compliance qual consultar e reintroduzindo a duplicidade conceitual do achado C1; (b) regras "triviais" evoluem — uma vez inline, sua evolução escaparia ao versionamento e à lineage de Standards, perdendo `RequirementIdentifier` estável e tornando Evidence histórica ininterpretável (Doc 1 §5.2); (c) o custo real é baixo — um Standard com um único NR é estruturalmente válido (Doc 1 ST25, E12). Precedente: no Kubernetes, `ValidatingAdmissionPolicy` (a expressão de validação) e `ValidatingAdmissionPolicyBinding` (onde e a quem se aplica) são objetos rigorosamente distintos, e o binding jamais contém a expressão.

### 4.3 Por que Policy não pode referenciar implementação

`PolicyScope` referencia `CapabilitySignature`, `ComponentType`, `RoleClass`, `NamespacePattern`, `OrganizationRef` — **nunca** um Coordinate concreto de Skill, Agent ou Workflow (PL3, invariante J3).

`[ESCOLHA DE DESIGN]` Alternativa rejeitada: permitir Policy dirigida a um Component específico ("este Agent deve cumprir este Standard"). Rejeitada porque quebraria a substituibilidade garantida por Composition §4/§7, onde Providers são resolvidos por Capability e podem ser substituídos por equivalentes superiores sem reescrita do consumidor. Uma Policy acoplada a Coordinate concreto tornaria a substituição de um Provider uma quebra silenciosa de cobertura normativa — o novo Provider não herdaria a exigência. Vinculação a Component específico permanece plenamente disponível pelo mecanismo correto: `standards_bound` no próprio Manifest (Kernel §2.14), que é local, explícito e visível a quem lê o Component.

---

## 5. Estrutura Formal

### 5.1 Policy

```
Policy (Structural Component) {
  identity          : Coordinate                     [Identity §4.1]
  version           : SemVer                         [Kernel §2.11]
  lifecycle_state   : KernelLifecycleState           [Kernel §3 — nunca estendido]
  owner             : Role                           [Kernel §2.3]

  priority          : Integer                        [§7.2]
  scope             : PolicyScope                    [§5.2]
  condition         : PolicyCondition?               (ausente ⟹ incondicional no scope)
  bindings          : PolicyBinding[]                (≥ 1 — J1)
  enforcement_mode  : BLOCKING | ADVISORY | AUDIT_ONLY        [§5.4]

  effective_from    : Timestamp                      [§5.5]
  expires_at        : Timestamp?                     [§5.5]

  overrides         : [VersionedIdentifier]?         [§7.3]
}
```

### 5.2 Policy Scope — dimensões de aplicabilidade

```
PolicyScope {
  namespaces      : [NamespacePattern]               [Identity §3, §8 — obrigatório, ≥1]
  organizations   : [OrganizationRef]?               [Identity §8 — slot reservado]
  component_types : [ComponentType]?                 (ausente ⟹ todos)
  capabilities    : [CapabilitySignature]?           [Kernel §2.9]
  roles           : [RoleClass]?                     [Governance §2]
  applies_at      : MANIFEST | COMPOSITION | WORKFLOW | EXECUTION      [§8]
}
```

**Semântica de combinação (PL14):** as dimensões combinam-se por **conjunção** (AND). Um sujeito está no escopo se e somente se satisfaz **todas** as dimensões declaradas. Dimensões omitidas são universalmente satisfeitas.

`[ESCOLHA DE DESIGN]` Conjunção entre dimensões, disjunção dentro de cada dimensão. Alternativa rejeitada: permitir expressões booleanas arbitrárias entre dimensões (`namespaces = X OR capabilities = Y`). Rejeitada porque tornaria a análise estática de sobreposição entre Policies indecidível na prática, impedindo a detecção de conflito em tempo de validação e empurrando toda a detecção para runtime — resultado inaceitável dado que PL4 (proibição de override de GLOBAL) **MUST** ser verificada na validação, não em runtime. Precedente: label selectors do Kubernetes usam a mesma semântica AND-entre-chaves / OR-dentro-de-valores, pela mesma razão de decidibilidade.

### 5.3 Policy Binding

```
PolicyBinding {
  standard          : VersionedIdentifier            [Doc 1 — MUST ser versionado, PL2]
  conformance_level : LevelName                      [Doc 1 §4.4]
  profile           : ProfileName?                   [Doc 1]
  conformance_mode  : STRICT | PARTIAL_ACCEPTABLE    [§5.3.1]
}
```

#### 5.3.1 `conformance_mode`

Determina se Partial Conformance (Doc 1 §8.2) satisfaz este Binding:

| Valor | Semântica |
|---|---|
| `STRICT` | Apenas Strict Conformance satisfaz. **MUST** ser o valor de todo Binding cujo Standard tenha `precedence_level = GLOBAL` (PL15) |
| `PARTIAL_ACCEPTABLE` | Partial Conformance satisfaz o Binding; `SHOULD` não satisfeitos são reportados, não bloqueantes |

**Interação com Certification:** independentemente de `conformance_mode`, Certification L3 exige Strict Conformance (Doc 1 ST19). Um Binding `PARTIAL_ACCEPTABLE` permite que um Component opere conforme à Policy sem atingir L3 — separação deliberada entre *operar sob a norma* e *ser certificado quanto a ela*.

### 5.4 Enforcement Mode

| Modo | Semântica | Consumidor executor |
|---|---|---|
| `BLOCKING` | Não conformidade impede a transição (Admission, Gate, dispatch) | Governance §7; Workflow §4; Execution §5 |
| `ADVISORY` | Não conformidade é sinalizada; nada é impedido | Compliance (downstream) |
| `AUDIT_ONLY` | Não conformidade é apenas registrada como Evidence | Governance §12 (Audit) |

`[ESCOLHA DE DESIGN]` Três modos em vez de enforcement uniforme. Alternativa rejeitada: toda Policy é bloqueante, e "recomendações" seriam expressas apenas por `SHOULD` no Standard. Rejeitada porque confundiria duas dimensões ortogonais e ambas necessárias: a **força normativa do requisito** (`MUST` vs `SHOULD`, propriedade do Standard) e a **consequência institucional do descumprimento** (bloquear vs. registrar, propriedade do contexto). Um mesmo `MUST` pode legitimamente ser bloqueante em produção e apenas auditado em ambiente de experimentação — sem `enforcement_mode`, isso exigiria dois Standards distintos, duplicando norma. Fundamento constitucional direto: **fricção proporcional ao risco**, o mesmo princípio que já produziu janelas de validade variáveis em Validation & Certification §5 e quórum variável em Governance §14.

### 5.5 Validade temporal

`effective_from` e `expires_at` são **atributos**, nunca estados (PL10).

Uma Policy em lifecycle `Active` mas fora da janela de vigência simplesmente **não integra** o Effective Policy Set. Modelar vigência como estado de lifecycle duplicaria o Kernel Lifecycle — proibido pela Restrição Arquitetural 3.

`[ESCOLHA DE DESIGN]` Vigência como atributo. Alternativa rejeitada: estados `Scheduled` / `Expired` no lifecycle da Policy. Rejeitada por dois motivos: (a) violaria a Restrição 3 e a regra já estabelecida em Registry §7.3 de que o estado de Registry Entry é projeção 1:1 do Kernel Lifecycle, "nunca uma máquina de estados independente"; (b) exigiria um processo ativo que transicionasse Policies no tempo, criando um componente de infraestrutura com autoridade de mutação sobre Components — precisamente o que Registry §1 proíbe ao estabelecer que o substrato "nunca decide; apenas reflete". Como atributo, a vigência é avaliada por consulta pura, sem mutação e sem processo de background.

---

## 6. Classes Nomeadas de Policy

As cinco classes exigidas pelo mandato **não são subtipos**. São **padrões de uso** distinguidos exclusivamente pela combinação de `scope` e `applies_at`. Nenhum `component_type` novo é introduzido; todas são `Policy`.

| Classe | Caracterização estrutural | `applies_at` típico | Consumidor executor |
|---|---|---|---|
| **Namespace Policy** | `scope.namespaces` é a única dimensão restritiva | MANIFEST | Governance §7 (Admission) |
| **Organization Policy** | `scope.organizations` presente; tipicamente ancorada em `org.<id>` | MANIFEST, COMPOSITION | Governance §7; Composition §5 |
| **Composition Policy** | `applies_at = COMPOSITION`; frequentemente com `capabilities` | COMPOSITION | Composition Resolver §5 |
| **Workflow Policy** | `applies_at = WORKFLOW`; `component_types = [Workflow]` ou `roles` para gates | WORKFLOW | Workflow §4 (`GATE_AUTO`) |
| **Execution Policy** | `applies_at = EXECUTION`; condição frequentemente dependente de runtime | EXECUTION | Execution §5 (dispatch) |

`[ESCOLHA DE DESIGN]` Classes como padrões de uso, não como subtipos. Alternativa rejeitada: `policy_kind` enumerado, ou `component_type` distinto por classe. Rejeitada porque exigiria que Registry, Governance, Composition, Workflow e Execution passassem a conhecer cinco tipos onde o mecanismo de resolução é idêntico — inflação de tipos sem ganho de expressividade. O mesmo raciocínio que levou Composition §4 a modelar cardinalidade de Slot como atributo (`EXACTLY_ONE`/`ONE_OF_MANY`/`ALL_OF_MANY`) em vez de três tipos de Slot. `applies_at` já carrega toda a informação que os consumidores precisam para filtrar.

---

## 7. Herança, Prioridade, Override e Coexistência

### 7.1 Herança por ancestralidade de Namespace

Policies são herdadas **descendentemente** na árvore de Namespaces de Identity & Namespace §8: uma Policy declarada em `core/` aplica-se a todos os Namespaces descendentes, salvo override válido (§7.3).

```
core/                                    ← Policy P1 (GLOBAL binding)
 └── org.acme-corp/                       ← Policy P2 (herda P1; MUST NOT suprimir binding GLOBAL)
      └── domain.billing/                  ← Policy P3 (herda P1, P2)
           └── env.production/              ← Policy P4 (herda P1, P2, P3)
```

A ancestralidade é sempre um **caminho da raiz até a folha**, nunca a árvore inteira — propriedade que mantém o conjunto candidato pequeno independentemente do tamanho total do ecossistema (§12.2).

### 7.2 Especificidade e prioridade

Dois critérios ordenados, aplicados nesta sequência estrita:

1. **Especificidade de Namespace** — profundidade na árvore. Mais profundo prevalece.
2. **`priority` explícito** — maior valor prevalece, **apenas** como desempate dentro do mesmo nível de especificidade.

`[ESCOLHA DE DESIGN]` Especificidade domina prioridade. Alternativa rejeitada: `priority` como critério primário, permitindo que uma Policy de `core/` com prioridade alta sobrepuje uma Policy local. Rejeitada porque inverteria a semântica de herança estabelecida — se `core/` pudesse sempre vencer por prioridade, a delegação a Governance Areas (Governance §4, Stewardship por domínio) tornar-se-ia nominal. A proteção do que é genuinamente institucional já existe e é mais forte que prioridade: PL4 (proibição absoluta de override de GLOBAL), que não depende de números.

### 7.3 Override e o limite constitucional

Uma Policy **MAY** declarar `overrides: [VersionedIdentifier]` suprimindo outras Policies.

**Limite absoluto (PL4):** override **MUST NOT** suprimir qualquer `PolicyBinding` cujo Standard tenha `precedence_level = GLOBAL`. Tentativa é rejeitada **na validação**, não em runtime.

Esta é a aplicação operacional literal da regra constitucional "o nível mais específico vence, exceto quando conflita com nível 1 (não negociável)". Nenhuma reinterpretação é introduzida.

A cadeia de `overrides` **MUST** ser acíclica — **reutiliza Kernel §7**, quinta aplicação institucional.

### 7.4 Resolução de conflito — a regra da união restritiva

Quando duas ou mais Policies aplicáveis empatam em especificidade e prioridade, e vinculam o mesmo Standard em Conformance Levels distintos, o resultado **MUST** ser a **união restritiva**: o nível mais alto prevalece; se os níveis forem incomparáveis (§7.4.1), a união dos requisitos de ambos prevalece.

`[ESCOLHA DE DESIGN]` União restritiva em vez de "última vence", "primeira vence", ou erro de resolução. Alternativas rejeitadas:
- *Erro em empate* — rejeitada porque empates são configuração legítima e comum (duas Policies independentes exigindo o mesmo Standard por razões distintas). Tornar isso um erro produziria fragilidade operacional sem ganho de segurança.
- *Última/primeira vence* — rejeitada porque dependeria de ordem de descoberta ou de timestamp, ambos não determinísticos sob particionamento do Registry (Registry §9, consistência eventual para índices secundários), violando o requisito de reprodutibilidade.
- *Menos restritivo vence* — rejeitada por inverter o incentivo institucional.

A escolha pela união restritiva realiza o princípio de que, sob ambiguidade genuína, o sistema **MUST** falhar em direção a mais rigor. Precedente: semântica *deny-overrides* de XACML; regra constitucional em que o nível não negociável sempre vence.

#### 7.4.1 Níveis incomparáveis

Conformance Levels formam uma **ordem parcial** via `inherits_from` (Doc 1 §4.4), não uma ordem total. Dois níveis em ramos distintos de herança são **incomparáveis** — não existe "mais alto" entre eles.

**Regra (PL16):** quando os níveis empatados são incomparáveis, o Effective Policy Set **MUST** conter ambos os Bindings, e a conformidade exigida é a **união dos requisitos** de ambos os níveis.

**Fundamento formal:** o conjunto de requisitos ordenado por inclusão forma um reticulado; a união é o supremo (*least upper bound*) nesse reticulado, existente mesmo quando os níveis nomeados são incomparáveis na ordem parcial de `inherits_from`. Isso torna a operação **total** — sempre definida, para qualquer par de Bindings.

Este é o caso extremo que garante que o algoritmo de §11.1 é uma função total, não parcial. Sem esta regra, existiria uma classe de configurações válidas para as quais a resolução seria indefinida.

### 7.5 Coexistência com `standards_bound`

`standards_bound` (Kernel §2.14) permanece plenamente válido e **MUST NOT** ser depreciado por este documento — depreciá-lo seria alteração de documento congelado.

**Regra de composição (PL5):**

> O conjunto normativo efetivo de um Component é a **união** de (a) seus `standards_bound` explícitos e (b) os `PolicyBinding` derivados do Effective Policy Set aplicável. Havendo o mesmo Standard em ambos com Conformance Levels distintos, aplica-se a mesma regra de união restritiva de §7.4, incluindo o tratamento de incomparabilidade de §7.4.1.

`[ESCOLHA DE DESIGN]` União com prevalência do mais alto. Alternativas rejeitadas:
- *Policy sobrepõe `standards_bound`* — permitiria que uma Policy relaxasse uma exigência que o autor do Component assumiu deliberadamente, subvertendo a intenção local sem visibilidade.
- *`standards_bound` sobrepõe Policy* — permitiria que qualquer Component se eximisse de exigência institucional pela simples omissão, destruindo a utilidade de Policy.

A união preserva ambas as intenções e é a única opção que não permite que nenhum dos dois mecanismos enfraqueça o outro. Consistente com §7.4.

---

## 8. Applicability — os quatro planos

`applies_at` determina **em que momento e contra que sujeito** os Bindings são avaliados.

| Plano | Sujeito avaliado | Momento | Executor | Custo |
|---|---|---|---|---|
| `MANIFEST` | Manifest de um Component | Admission; mudança normativa | Governance §7 | Uma vez por versão; cache indefinido |
| `COMPOSITION` | `Assembly` resolvida | Resolução de Assembly | Composition Resolver §5 | Uma vez por Assembly; cacheável |
| `WORKFLOW` | Definição de Workflow / avaliação de Gate | `validate_workflow_definition`; `GATE_AUTO` | Workflow §4 | Uma vez por versão; por gate |
| `EXECUTION` | Execution concreta | Dispatch de Step | Execution §5 | Por Execution — caminho quente |

**Regra de economia (PL12):** uma Policy **SHOULD** declarar o `applies_at` mais estático que sua semântica permita. Justificativa: avaliação em `EXECUTION` incide no caminho quente de dispatch (Execution §5), com custo proporcional ao volume de Executions — que Domain Model §4.5 antecipa como a classe de entidade mais numerosa do Framework. Reservar `EXECUTION` a condições genuinamente dependentes de runtime é a diferença entre custo O(versões) e custo O(execuções).

**Regra de compatibilidade (PL13):** `scope.applies_at` **MUST** ser compatível com o `ComplianceTarget.applies_to` dos NRs dos Standards vinculados (Doc 1 §4.5). Vincular, em `applies_at = MANIFEST`, um Standard cujos requisitos são todos `applies_to = EXECUTION` produz um Binding vacuamente satisfeito — detectado na validação como `INCOMPATIBLE_APPLICATION_PLANE` (invariante J7).

---

## 9. Effective Policy Set

O **Effective Policy Set (EPS)** é um `Artifact` genérico (Domain Model §2 #7) — mandato §8. Mesmo padrão de `Assembly` (Composition §4), `Execution Plan` (Execution §4) e `Conformance Claim` (Doc 1 §8.1). **Não é entidade nova.**

```
EffectivePolicySet (Artifact) {
  subject               : VersionedIdentifier | ExecutionInstanceId
  evaluated_at          : Timestamp
  context_snapshot_ref  : ContextSnapshotId?     [RFC-DM-001 §3.2 — obrigatório se applies_at=EXECUTION]
  applies_at            : ApplicationPlane

  bindings              : ResolvedBinding[]
  resolution_trace      : ResolutionTrace        [§9.2 — obrigatório, PL8]
}

ResolvedBinding {
  standard          : VersionedIdentifier
  conformance_level : LevelName
  conformance_mode  : STRICT | PARTIAL_ACCEPTABLE
  enforcement_mode  : BLOCKING | ADVISORY | AUDIT_ONLY
  origin            : POLICY(VersionedIdentifier) | STANDARDS_BOUND
  precedence_level  : GLOBAL | DOMAIN | STACK | PROJECT
}
```

### 9.1 Imutabilidade

Um EPS publicado **MUST** ser imutável. Alterar qualquer resolução exige gerar um novo EPS — nunca mutação in-place.

Isto espelha exatamente a invariante já estabelecida em Composition §5 para `Assembly` ("uma Assembly publicada MUST ser imutável; mudar qualquer resolução exige uma nova Assembly") e a imutabilidade de Manifest de Kernel §8. Nenhuma regra nova de imutabilidade é introduzida — é a aplicação da regra existente a mais um Artifact.

### 9.2 Resolution Trace

```
ResolutionTrace {
  candidates_considered : [VersionedIdentifier]
  filtered_out          : [(VersionedIdentifier, FilterReason)]
  suppressed_by_override: [(VersionedIdentifier, VersionedIdentifier)]
  conflicts_resolved    : [(StandardRef, [LevelName], ResolutionStrategy)]
  standards_bound_merged: [(StandardRef, LevelName, MergeOutcome)]
}
```

O EPS **MUST** carregar o trace completo (PL8).

Isto **não é mecanismo novo** — é a aplicação, ao domínio normativo, do princípio já normatizado em três pontos independentes da base: Identity & Namespace §6.6 (cadeia de redirecionamento nunca oculta ao chamador), Registry & Discovery §6.1 (`resolution_path` retornado em toda resolução) e Composition §7 (desempate determinístico registrado para auditabilidade). Consistência de princípio, não invenção.

---

## 10. Modelo Operacional

**Serviço:** `Policy Evaluation Service` — substrato institucional. Mesma classe arquitetural de `Composition Resolver` (Composition §5), `Scheduler` (Execution §5) e `Standard Resolution Service` (Doc 1 §10). **Não é Component**, não possui Lifecycle, não possui autoridade decisória, **não escreve em lugar algum**.

### 10.1 Operações

```
resolve_effective_policy_set(subject, context, at, plane) → EffectivePolicySet | PolicyError
  PRE:  subject descreve um Component (Coordinate@version) ou uma Execution
        E se plane = EXECUTION, context é um Context Snapshot [RFC-DM-001 §3.2], não Context vivo
  POST: EPS imutável, determinístico, com resolution_trace completo
  INV:  determinismo total — mesma tupla (subject, context, at, plane) ⟹ mesmo EPS
        (requisito herdado de Validation & Certification §6, Reproducibility)

validate_policy_definition(manifest) → ValidationResult
  PRE:  manifest.component_type = Policy
  POST: ver §10.3

analyze_policy_overlap(policy_a, policy_b) → OverlapReport
  POST: relatório estático de sobreposição de escopo, para detecção
        de conflito em Admission (Governance §7) — descritivo, não decisório
```

### 10.2 Invariante de admissão

`validate_policy_definition` **MUST** ser satisfeito antes de uma Policy sair de `Draft`. **Reutiliza integralmente** o gate de Verification de Validation & Certification §4 e o critério de Conformance para `component_type = Policy` já anunciado em Validation & Certification §7 ("Revisão de completude e ausência de conflito de precedência"). Este documento fornece o conteúdo verificável daquele critério, sem redefinir o gate.

### 10.3 Invariantes verificados

| # | Invariante | Origem |
|---|---|---|
| J1 | `bindings` não vazio | §5.1 |
| J2 | Nenhum critério normativo inline em qualquer campo | PL1, §4.2 |
| J3 | Nenhuma referência a Coordinate de implementação concreta | PL3, §4.3 |
| J4 | Todo `binding.standard` resolve a Standard em `Active` ou `Deprecated` | Registry §6.1 |
| J5 | Todo `binding.conformance_level` existe no Standard referenciado | Doc 1 §4.4 |
| J6 | Todo `binding.standard` usa Versioned Identifier | PL2 |
| J7 | `scope.applies_at` compatível com `ComplianceTarget.applies_to` dos NRs vinculados | PL13, §8 |
| J8 | `condition` é predicado puro e determinístico | PL6 |
| J9 | Nenhum `overrides` suprime Binding de Standard `GLOBAL` | PL4, §7.3 |
| J10 | Cadeia de `overrides` acíclica | PL9 (Kernel §7, 5ª aplicação) |
| J11 | `effective_from < expires_at` quando ambos presentes | §5.5 |
| J12 | `scope.namespaces` não vazio | §5.2 |
| J13 | Binding de Standard `GLOBAL` tem `conformance_mode = STRICT` | PL15, §5.3.1 |
| J14 | `scope.namespaces` não referencia `core/` se o autor não for Framework Council | Identity §8; Governance §8 |
| J15 | Nenhum `overrides` referencia Policy em Namespace não ancestral nem descendente | §7.3 |

---

## 11. Algoritmos

### 11.1 Geração do Effective Policy Set

```
ALGORITMO ResolveEffectivePolicySet(subject, ctx, at, plane):
  ENTRADA: subject : VersionedIdentifier | ExecutionInstanceId
           ctx     : Context | ContextSnapshot
           at      : Timestamp
           plane   : ApplicationPlane
  SAÍDA:   EffectivePolicySet (Artifact) | PolicyError
  INVARIANTES: determinístico · total · terminante · imutável na saída

  ── FASE 0 — precondições ────────────────────────────────────────────────
  1  SE plane = EXECUTION ∧ ctx NÃO É ContextSnapshot:
  2     RETORNA PolicyError(LIVE_CONTEXT_FORBIDDEN_AT_EXECUTION)     # PL7

  ── FASE 1 — candidatos por ancestralidade ───────────────────────────────
  3  ancestry ← NamespaceAncestry(subject.namespace)      # raiz → folha, Identity §8
  4  candidates ← Registry.list(component_type = Policy, namespaces = ancestry)
  5  trace.candidates_considered ← candidates

  ── FASE 2 — filtros sucessivos, cada rejeição registrada ────────────────
  6  candidates ← Filter(p: p.lifecycle_state = Active)              → LIFECYCLE
  7  candidates ← Filter(p: p.effective_from ≤ at
  8                        ∧ (p.expires_at = null ∨ at < p.expires_at))  → TEMPORAL
  9  candidates ← Filter(p: p.scope.applies_at = plane)              → PLANE
 10  candidates ← Filter(p: ScopeMatches(p.scope, subject, ctx))      → SCOPE
 11  candidates ← Filter(p: p.condition = null
 12                        ∨ Evaluate(p.condition, ctx) = TRUE)       → CONDITION
 13  # cada elemento removido é registrado em trace.filtered_out com o motivo

  ── FASE 3 — cadeia de override ──────────────────────────────────────────
 14  SE Kernel§7.CycleDetection(OverrideGraph(candidates)) detecta ciclo:
 15     RETORNA PolicyError(CYCLIC_OVERRIDE_CHAIN)                    # J10
 16  suppressed ← ∅
 17  PARA CADA p EM candidates ONDE p.overrides ≠ ∅:
 18     PARA CADA alvo EM p.overrides:
 19        SE ∃ b EM alvo.bindings COM b.standard.precedence_level = GLOBAL:
 20           RETORNA PolicyError(ILLEGAL_OVERRIDE_OF_GLOBAL, p, alvo)   # PL4 — falha, não ignora
 21        suppressed ← suppressed ∪ {alvo}
 22        trace.suppressed_by_override ← trace.suppressed_by_override ∪ {(p, alvo)}
 23  candidates ← candidates \ suppressed

  ── FASE 4 — resolução de conflito por Standard ──────────────────────────
 24  grupos ← GroupByStandardCoordinate(Flatten(candidates.bindings))
 25  resolvidos ← ∅
 26  PARA CADA (std_coord, grupo) EM SortedByCoordinate(grupos):
 27     resolvidos ← resolvidos ∪ ResolveConflict(std_coord, grupo, trace)

  ── FASE 5 — merge com standards_bound ───────────────────────────────────
 28  SE subject é Component:
 29     PARA CADA sb EM subject.manifest.standards_bound:            # Kernel §2.14
 30        SE ∃ r EM resolvidos COM r.standard.coordinate = sb.coordinate:
 31           r.conformance_level ← JoinLevels(r.conformance_level, sb.level)   # §7.4.1
 32           trace.standards_bound_merged += (sb, r.conformance_level, MERGED)
 33        SENÃO:
 34           resolvidos ← resolvidos ∪ { ResolvedBinding(sb, origin = STANDARDS_BOUND) }
 35           trace.standards_bound_merged += (sb, sb.level, ADDED)

  ── FASE 6 — materialização imutável ─────────────────────────────────────
 36  RETORNA Artifact(EffectivePolicySet, {
 37     subject, evaluated_at = at, plane,
 38     context_snapshot_ref = (plane = EXECUTION ? ctx.id : null),
 39     bindings = SortedByCoordinate(resolvidos),        # ordenação ⟹ saída estável
 40     resolution_trace = trace
 41  })
```

**Terminação:** Fase 1 retorna conjunto finito (ancestralidade é caminho finito). Fases 2 e 4-5 são iterações sobre conjuntos finitos. Fase 3 termina porque o grafo de override é acíclico (linhas 14-15).

**Determinismo:** garantido por (a) `SortedByCoordinate` nas linhas 26 e 39, (b) `ResolveConflict` ser total e determinístico (§11.2), (c) `Evaluate(condition)` ser puro e determinístico por J8, (d) avaliação contra Context Snapshot imutável quando `plane = EXECUTION`.

**Totalidade:** garantida por `JoinLevels` (§11.3) ser total, incluindo o caso de níveis incomparáveis.

### 11.2 Resolução formal de conflito

```
ALGORITMO ResolveConflict(std_coord, grupo, trace):
  ENTRADA: std_coord : Coordinate
           grupo     : [(Policy, PolicyBinding)]
  SAÍDA:   ResolvedBinding
  PROPRIEDADES: total · determinístico · monotônico no rigor

  ── critério 1: especificidade de Namespace ──────────────────────────────
  1  max_spec ← Max(NamespaceDepth(p.namespace) PARA (p, _) EM grupo)
  2  nivel1 ← { (p,b) EM grupo : NamespaceDepth(p.namespace) = max_spec }
  3  SE |nivel1| = 1:
  4     trace.conflicts_resolved += (std_coord, Levels(grupo), BY_SPECIFICITY)
  5     RETORNA Materialize(Único(nivel1))

  ── critério 2: priority explícito ───────────────────────────────────────
  6  max_prio ← Max(p.priority PARA (p, _) EM nivel1)
  7  nivel2 ← { (p,b) EM nivel1 : p.priority = max_prio }
  8  SE |nivel2| = 1:
  9     trace.conflicts_resolved += (std_coord, Levels(nivel1), BY_PRIORITY)
 10     RETORNA Materialize(Único(nivel2))

  ── critério 3: união restritiva (§7.4) ──────────────────────────────────
 11  # empate genuíno: aplica-se o supremo no reticulado de requisitos
 12  nivel_final ← Fold(JoinLevels, Levels(nivel2))
 13  modo_final  ← SE ∃ (_,b) EM nivel2 COM b.conformance_mode = STRICT
 14                ENTÃO STRICT SENÃO PARTIAL_ACCEPTABLE      # mais restritivo vence
 15  enforce_final ← MaxByRestrictiveness(EnforcementModes(nivel2))
 16                   # BLOCKING > ADVISORY > AUDIT_ONLY
 17  trace.conflicts_resolved += (std_coord, Levels(nivel2), BY_RESTRICTIVE_UNION)
 18  RETORNA ResolvedBinding(std_coord, nivel_final, modo_final, enforce_final,
 19                          origin = POLICY(Todos(nivel2)))
```

**Propriedade de monotonicidade no rigor:** em nenhum ramo do algoritmo o resultado é menos restritivo que qualquer um dos Bindings de entrada. Nas linhas 13-16, `conformance_mode` e `enforcement_mode` são resolvidos sempre pelo mais restritivo. Esta propriedade é o que garante formalmente que **nenhuma configuração de Policies pode enfraquecer, por acidente de resolução, uma exigência declarada** — realização direta do princípio de §7.4.

### 11.3 Join de Conformance Levels

```
ALGORITMO JoinLevels(L1, L2):
  ENTRADA: L1, L2 : LevelName do mesmo Standard
  SAÍDA:   LevelName | SyntheticLevel
  PROPRIEDADE: função total (definida para todo par, inclusive incomparáveis)

  1  SE L1 = L2: RETORNA L1
  2
  3  # ordem parcial induzida por inherits_from (Doc 1 §4.4, monotônico)
  4  SE Ancestor(L1, L2): RETORNA L2         # L2 é mais alto — herda e amplia L1
  5  SE Ancestor(L2, L1): RETORNA L1
  6
  7  # incomparáveis: ramos distintos da hierarquia de herança — §7.4.1
  8  # supremo no reticulado de conjuntos de requisitos ordenado por inclusão
  9  RETORNA SyntheticLevel(requires = Requires(L1) ∪ Requires(L2),
 10                          derived_from = [L1, L2])
```

**Nota estrutural:** `SyntheticLevel` **não é** um Conformance Level adicionado ao Standard — o Standard permanece imutável (Kernel §8, Doc 1). É um Value Object efêmero, interno ao EPS, expressando "o conjunto de requisitos exigido é a união destes dois níveis". Sua materialização vive exclusivamente dentro do Artifact EPS, é imutável junto com ele, e nunca é escrita de volta em nenhum Component.

### 11.4 Validação de definição

```
ALGORITMO ValidatePolicyDefinition(manifest):
  1  ASSERT |manifest.bindings| ≥ 1                                        → J1
  2  ASSERT |manifest.scope.namespaces| ≥ 1                                → J12
  3  ASSERT NenhumCriterioNormativoInline(manifest)                        → J2, PL1
  4  ASSERT NenhumaReferenciaAImplementacaoConcreta(manifest.scope)        → J3, PL3
  5
  6  PARA CADA b EM manifest.bindings:
  7     ASSERT IsVersionedIdentifier(b.standard)                           → J6, PL2
  8     std ← Registry.resolve(b.standard)                                 # Registry §6.1
  9     ASSERT std.lifecycle_state ∈ {Active, Deprecated}                  → J4
 10     ASSERT b.conformance_level ∈ std.conformance_levels                → J5
 11     SE std.precedence_level = GLOBAL:
 12        ASSERT b.conformance_mode = STRICT                              → J13, PL15
 13     nrs ← StandardResolver.resolve_effective_requirements(b.standard, b.conformance_level)
 14     ASSERT ∃ nr EM nrs COM nr.target.applies_to compatível
 15            COM manifest.scope.applies_at                                → J7, PL13
 16
 17  SE manifest.condition ≠ null:
 18     ASSERT IsPureDeterministic(manifest.condition)                     → J8, PL6
 19
 20  ASSERT Kernel§7.CycleDetection(OverrideChain(manifest)) sem ciclo      → J10
 21  PARA CADA alvo EM manifest.overrides:
 22     t ← Registry.resolve(alvo)
 23     ASSERT ∄ b EM t.bindings COM b.standard.precedence_level = GLOBAL   → J9, PL4
 24     ASSERT IsAncestorOrDescendant(t.namespace, manifest.namespace)      → J15
 25
 26  SE manifest.effective_from ∧ manifest.expires_at ambos presentes:
 27     ASSERT manifest.effective_from < manifest.expires_at                → J11
 28
 29  SE manifest.scope.namespaces intersecta core/:
 30     ASSERT Author ∈ FrameworkCouncil                                    → J14
 31
 32  RETORNA OK | ValidationError(invariante, detalhe)
```

---

## 12. Diagramas

### 12.1 UML simplificado

```
┌────────────────────────────────────────┐
│ Policy                                  │  «Structural Component» — Domain Model §3
│  priority : Integer                     │
│  enforcement_mode : BLOCKING|ADVISORY|  │
│                     AUDIT_ONLY          │
│  effective_from / expires_at  (atributos, nunca estados — PL10)
│  overrides[] ──────────────────────────┼──► VersionedIdentifier
└──┬──────────────┬───────────────┬──────┘      (grafo acíclico — Kernel §7)
   │1             │0..1            │1..*
   ▼              ▼                ▼
┌─────────────┐ ┌──────────────┐ ┌──────────────────────────┐
│PolicyScope  │ │PolicyCondition│ │ PolicyBinding             │
│ «VO»        │ │ «VO»          │ │ «VO»                      │
│ namespaces[]│ │ Predicate     │ │  standard ────────────────┼──► Standard  [Doc 1]
│ orgs[]      │ │ <Context>     │ │    (VersionedIdentifier)  │    ↑ referência apenas
│ types[]     │ │ puro e        │ │  conformance_level ───────┼──► ConformanceLevel
│ capabilities┼─►determinístico │ │  profile?                 │    NUNCA critério inline
│ roles[]     │ │ (J8)          │ │  conformance_mode         │    (PL1, J2)
│ applies_at  │ └──────────────┘ └──────────────────────────┘
└─────────────┘
      │ combinação AND entre dimensões, OR dentro de cada (PL14)
      ▼
 ┌──────────────────────────────────────────────┐
 │ EffectivePolicySet   «Artifact» genérico      │
 │  bindings : ResolvedBinding[]                 │
 │  resolution_trace  (obrigatório — PL8)        │
 │  context_snapshot_ref  [RFC-DM-001 §3.2]      │
 │  imutável (§9.1, espelha Assembly/Composition §5)
 └──────────────────────────────────────────────┘
```

### 12.2 Sequência — resolução completa

```
Consumer      PolicyEval        Registry      StandardResolver     EPS(Artifact)
   │              │                 │                │                   │
   ├─resolve_eps─►│                 │                │                   │
   │ (subj,ctx,   │                 │                │                   │
   │  at,plane)   │                 │                │                   │
   │              │                                                       │
   │        alt plane=EXECUTION ∧ ctx não é Snapshot                      │
   │◄─PolicyError(LIVE_CONTEXT_FORBIDDEN)  [PL7]                          │
   │              │                 │                │                   │
   │              ├─list(Policy,────►│                │                   │
   │              │  ancestry)      │                │                   │
   │              │◄─candidates[]───┤                │                   │
   │              │                                                       │
   │              ├─filtros: lifecycle → temporal → plane → scope → cond  │
   │              │  (cada rejeição registrada em trace.filtered_out)     │
   │              │                                                       │
   │              ├─Kernel§7.CycleDetection(override graph)  [5ª aplicação]
   │              │                                                       │
   │        loop cadeia de override                                       │
   │              ├─alvo tem binding GLOBAL?                              │
   │◄─PolicyError(ILLEGAL_OVERRIDE_OF_GLOBAL)  [PL4 — falha na validação] │
   │              │                                                       │
   │        loop por Standard agrupado                                    │
   │              ├─ResolveConflict: especificidade → priority → união    │
   │              ├──────────────────────────────────►│ (JoinLevels)      │
   │              │◄─nivel resolvido, incl. incomparáveis (§7.4.1)────────┤
   │              │                                                       │
   │              ├─merge com standards_bound (§7.5, união restritiva)    │
   │              ├─materializar imutável, ordenado ────────────────────►│
   │◄─EffectivePolicySet ─────────────────────────────────────────────────┤
```

### 12.3 Herança e override na árvore de Namespaces

```
core/                          P1 { binding: std.security@2 (GLOBAL), BLOCKING }
  │                                 ↓ herdada por todos os descendentes
  ├─ org.acme-corp/             P2 { binding: std.api@1, ADVISORY, priority: 10 }
  │    │                             ↓
  │    ├─ domain.billing/        P3 { binding: std.api@1 nível EXTENDED, priority: 5 }
  │    │    │                          overrides: [P2]  ✔ legal (std.api não é GLOBAL)
  │    │    │                          overrides: [P1]  ✘ REJEITADO — PL4
  │    │    │
  │    │    └─ env.production/   P4 { binding: std.perf@1, applies_at: EXECUTION }
  │    │
  │    └─ domain.identity/       (herda P1, P2 — sem Policy local)
  │
  └─ org.globex/                 (herda apenas P1 — isolada de P2 por Identity §10)

EPS resolvido para: org.acme-corp/domain.billing/env.production/<component>
  ├─ std.security@2  EXTENDED?  ← de P1 (GLOBAL, jamais suprimível, STRICT obrigatório)
  ├─ std.api@1 EXTENDED         ← de P3 (mais específico que P2; P2 suprimida)
  ├─ std.perf@1                  ← de P4 (applies_at = EXECUTION)
  └─ + standards_bound do próprio Component (união restritiva — §7.5)
```

### 12.4 Estados

Policy **não possui máquina de estados própria** — Kernel Lifecycle exclusivamente, projetado no Registry conforme Registry §7.3. Vigência temporal é dimensão **ortogonal** ao lifecycle:

```
                    │ at < effective_from │ vigente │ at ≥ expires_at
────────────────────┼─────────────────────┼─────────┼─────────────────
lifecycle = Active  │ não integra EPS      │ INTEGRA │ não integra EPS
lifecycle ≠ Active  │ não integra EPS      │ não int.│ não integra EPS
```

Reproduzir isto como máquina de estados própria duplicaria o Kernel Lifecycle — proibido pela Restrição Arquitetural 3.

---

## 13. Integrações

| Documento base | Contrato de integração | Direção |
|---|---|---|
| **Constitution** | Hierarquia de precedência aplicada literalmente em PL4 (GLOBAL inviolável); fricção proporcional ao risco materializada em `enforcement_mode` (§5.4); Transparência realizada por `resolution_trace` obrigatório (PL8) | Consumo de princípio |
| **Kernel** | Policy é Component pleno; `standards_bound` (§2.14) preservado e integrado por união (§7.5), jamais substituído ou depreciado; `CapabilitySignature` (§2.9) em Scope; Cycle Detection (§7) reaplicado — 5ª aplicação institucional; Lifecycle (§3) intocado | Reuso puro |
| **Governance** | Aprovação por Governance Area Steward (§8) sem alteração; conflitos irresolvíveis por §11.2 escalam a §17; exceções permanecem exclusivamente em §15, consumidas por Compliance, jamais redefinidas aqui; Admission (§7) consome Policies `applies_at = MANIFEST`; Audit (§12) consome EPS e traces | Delegação total |
| **Domain Model v1.1.0** | Zero entidades, relações e estados novos. Policy = Structural Component (§3); Scope/Condition/Binding/EnforcementMode = Value Objects; EPS = `Artifact` genérico (§2 #7); Condition = predicado sobre `Context` já genérico (§2 #5) | Conformidade estrita |
| **RFC-DM-001** | PL7 exige Context Snapshot (§3.2, achado C2) para avaliação em `EXECUTION` — sem isso, a avaliação não seria reproduzível posteriormente, violando Domain Model §15; C1, C3, C4 não tocados | Consumo de correções |
| **Identity & Namespace** | Árvore de Namespaces (§8) é o eixo de herança e de especificidade; `OrganizationRef` usa o slot reservado (§10); isolamento cross-org de §10 garante que Policies de `org.globex` jamais alcancem `org.acme-corp`; convenção `<ns>/policy.<área>.<nome>` (§5); `resolution_trace` segue o princípio de §6.6 | Reuso integral |
| **Registry & Discovery** | `list(component_type=Policy, namespaces=ancestry)` (§5) é a operação primária; `resolve()` (§6.1) para Standards vinculados; nenhum índice novo além dos normatizados em §8; Policy **MUST NOT** escrever no Registry | Consumidor puro |
| **Validation & Certification** | §4 (gate de Verification) e §7 (critério para `component_type=Policy`) reutilizados sem redefinição; L3 avalia conformidade ao conjunto normativo efetivo, que passa a ser EPS ∪ `standards_bound` — extensão do **insumo**, sem alteração do **mecanismo** de certificação; §5 (níveis) e §6 (Reproducibility) intocados | Bidirecional, sem alteração |
| **Composition** | `applies_at = COMPOSITION` restringe candidatos elegíveis na resolução de Slot; `Slot.condition` já usa o mesmo padrão `Predicate<Context>` (§4), portanto nenhum mecanismo novo de predicado é introduzido; desbloqueia a dependência declarada em Composition §14 sem alterá-la | Desbloqueio |
| **Workflow** | `applies_at = WORKFLOW` é avaliado por `GATE_AUTO` (§4); o Gate consome o resultado e decide passar/bloquear conforme sua `FailurePolicy` — Policy fornece insumo, jamais vira Gate | Unidirecional |
| **Execution** | `applies_at = EXECUTION` avaliado no dispatch (§5) contra Context Snapshot; `BLOCKING` impede transição a `Running`, decisão executada pelo Scheduler; imutabilidade de Execution (Domain Model §8, EX1) garante que expiração posterior de Policy não altera Execution em curso (E8) | Unidirecional |
| **Standards (Documento 1)** | Consome `VersionedIdentifier`, `ConformanceLevel`, `precedence_level`, ordem parcial de `inherits_from` (§4.4) para `JoinLevels`, e a distinção Strict/Partial (§8.2) para `conformance_mode`. Standard **MUST NOT** conhecer Policy — relação estritamente unidirecional | Consumidor |
| **Compliance (downstream)** | Consome EPS como entrada primária; produz Evidence e Reports; consome Governance §15 para waivers. Não altera este documento | Consumidor futuro |

---

## 14. Casos Extremos

| # | Caso | Tratamento normativo |
|---|---|---|
| F1 | Duas Policies, mesma especificidade e prioridade, níveis distintos do mesmo Standard | União restritiva — nível mais alto (§11.2 linha 12). Determinístico, jamais erro |
| F2 | Níveis empatados **incomparáveis** (ramos distintos de `inherits_from`) | `SyntheticLevel` com união dos requisitos (§7.4.1, §11.3 linha 9). Garante totalidade do algoritmo |
| F3 | Override sobre Binding de Standard `GLOBAL` | `PolicyError(ILLEGAL_OVERRIDE_OF_GLOBAL)` na **validação**, nunca em runtime (PL4, J9) |
| F4 | Cadeia de `overrides` cíclica | Kernel §7, 5ª aplicação; rejeitado na validação (J10) |
| F5 | Override apontando para Policy em Namespace não relacionado (nem ancestral nem descendente) | Rejeitado (J15). Justificativa: override entre ramos não relacionados violaria o isolamento de Identity §10 e tornaria a resolução dependente de Policies fora da ancestralidade — quebrando a garantia de custo O(profundidade) de §15.2 |
| F6 | Policy referencia Standard em `Deprecated` | Permitido com aviso (paridade com Doc 1 E8 e Registry §7.3); sinalizado como drift para Compliance |
| F7 | Policy referencia Standard em `Archived`/`Removed` | Validação falha (J4); Policy `Active` que caia nessa condição é detectada por Compliance contínua (Governance §13) e escalada ao Steward |
| F8 | Policy expira durante uma Execution longa | Avaliação ocorre **uma vez**, no dispatch, contra o Context Snapshot. Expiração posterior **MUST NOT** alterar a Execution em curso. Coerente com imutabilidade de Execution (Domain Model §8) e com EX1 (Execution §12) |
| F9 | Policy ativada durante uma Execution longa | Simétrico a F8: não afeta Executions já despachadas. Aplica-se a partir do próximo dispatch |
| F10 | `Condition` não determinística ou com efeito colateral | Rejeitada na validação (J8, PL6). Sem isso, reprodutibilidade de avaliação (Validation & Certification §6) seria impossível |
| F11 | Nenhuma Policy aplicável ao sujeito | EPS válido contendo apenas `standards_bound` (§7.5). Conjunto vazio é resultado legítimo, **não** erro |
| F12 | Policy sem `condition` | Incondicional dentro do `scope` (PL17). Comportamento normal, não caso de erro |
| F13 | Policy tenta escopo sobre `core/` sem ser Framework Council | Rejeitada (J14). Escrita em `core/` é exclusiva do Council (Identity §8; Governance §8) |
| F14 | Policy de `org.globex` tentando alcançar `org.acme-corp` | Estruturalmente impossível: a Fase 1 do algoritmo consulta apenas a **ancestralidade** do sujeito; `org.globex` nunca é ancestral de `org.acme-corp`. Isolamento garantido por construção, não por verificação |
| F15 | `applies_at` incompatível com `ComplianceTarget.applies_to` dos NRs vinculados | `INCOMPATIBLE_APPLICATION_PLANE` na validação (J7, PL13). Evita Bindings vacuamente satisfeitos |
| F16 | Binding de Standard `GLOBAL` com `conformance_mode = PARTIAL_ACCEPTABLE` | Rejeitado (J13, PL15). Norma não negociável não admite conformidade parcial |
| F17 | Policy com `effective_from ≥ expires_at` | Rejeitada (J11). Janela vazia é erro de definição, não configuração válida |
| F18 | Dois EPS concorrentes para o mesmo sujeito em instantes distintos | Seguros por construção: cada EPS é Artifact imutável com `evaluated_at` próprio. Mesma garantia de concorrência de Execution §9 |
| F19 | Standard vinculado torna-se `Archived` **entre** a geração do EPS e seu consumo | EPS permanece válido (imutável, §9.1); a avaliação subsequente contra Standard arquivado falha por Doc 1 ST20. Detectado como drift por Compliance |
| F20 | `priority` idêntico e especificidade idêntica em ramos de Namespace diferentes | Impossível: especificidade é profundidade na **mesma** ancestralidade (caminho único raiz→folha); duas Policies na ancestralidade de um mesmo sujeito estão necessariamente em profundidades comparáveis. Empate real só ocorre no mesmo Namespace, resolvido por F1 |
| F21 | Policy vinculando Standard cujos `conformance_levels` foram removidos em MAJOR posterior | Impossível de afetar EPS existente: Binding usa `VersionedIdentifier` (PL2), e Manifests são imutáveis (Kernel §8). Adotar a nova MAJOR exige nova versão da Policy — decisão explícita, jamais silenciosa |
| F22 | Fan-out muito grande: mudança em Standard `core/` vinculado por centenas de Policies | Não é erro; é questão de escala. Tratamento: reavaliação **SHOULD** ser assíncrona e priorizada por risco (Governance §14) — mesma disciplina que Governance §13 já mandata para Compliance contínua |

---

## 15. Performance

### 15.1 Cache — e por que difere de Standards

| Objeto | Cacheável indefinidamente? | Razão |
|---|---|---|
| `resolve_effective_requirements` (Doc 1) | **Sim** | Depende apenas de Manifests imutáveis (Kernel §8) |
| `resolve_effective_policy_set` | **Não** (PL11) | Depende de `at` (tempo), de transições de lifecycle, e de `Context` |

**Chave de cache:** `(subject, plane, context_digest, at_bucket)`.

**Invalidação (SHOULD ser orientada a evento):** `PolicyActivated`, `PolicyExpired`, `PolicyDeprecated`, `PolicyPublished` no Namespace ancestral.

Esta distinção — cache indefinido para resolução de identidade versionada, TTL curto ou invalidação por evento para resolução dependente de tempo/contexto — é **exatamente** a mesma já normatizada em Registry & Discovery §8 entre Versioned Identifier (indefinido) e Coordinate/Alias (TTL curto). Nenhuma política nova de cache é introduzida.

### 15.2 Complexidade

| Operação | Complexidade | Comentário |
|---|---|---|
| `ResolveEffectivePolicySet` | O(D · P · B · log B) | D = profundidade do Namespace (tipicamente ≤ 5), P = Policies por nível, B = bindings por Policy |
| `ResolveConflict` | O(G log G) | G = Bindings do mesmo Standard |
| `JoinLevels` | O(R) | R = requisitos nos níveis; O(1) no caso comparável |
| `ValidatePolicyDefinition` | O(B · R) | Inclui resolução de requisitos para verificar J7 |

**Propriedade de escala fundamental:** a ancestralidade é sempre um **caminho da raiz até a folha**, nunca a árvore inteira. O conjunto candidato é O(profundidade), não O(total de Policies no ecossistema). Isso significa que adicionar milhares de Policies em `org.globex` **não** afeta a latência de resolução para sujeitos em `org.acme-corp` — propriedade herdada diretamente do particionamento por Namespace de Registry §10 e do isolamento de Identity §10.

### 15.3 Trade-offs explícitos

**Trade-off 1 — Latência no caminho quente.** Avaliar Policy a cada dispatch de Step (Execution §5) adiciona latência proporcional ao volume de Executions. Mitigação normativa: PL12 (`SHOULD` preferir `applies_at` mais estático). Uma Policy avaliada em `MANIFEST` custa O(versões); a mesma em `EXECUTION` custa O(execuções) — diferença de várias ordens de magnitude na escala que Domain Model §4.5 antecipa. Não eliminado, apenas governado por recomendação normativa e mensurável.

**Trade-off 2 — Ausência de materialização antecipada.** Alternativa rejeitada: pré-computar e armazenar o EPS de cada Component no momento da publicação. Rejeitada porque o EPS depende de `at` e de `Context`, ambos variáveis após a publicação — um EPS materializado tornar-se-ia obsoleto silenciosamente a cada Policy que ativasse ou expirasse, produzindo a pior falha possível nesta camada: aplicação de norma desatualizada sem sinal. O custo de recomputar é aceito deliberadamente em troca de correção temporal garantida.

**Trade-off 3 — Trace completo sempre.** `resolution_trace` obrigatório (PL8) aumenta o tamanho de cada EPS. Alternativa rejeitada: trace opcional, ativado apenas em modo debug. Rejeitada porque auditoria (Governance §12) é retrospectiva por natureza — um trace que precisa ser ativado antes do fato é inútil quando a pergunta surge depois. Mesma razão pela qual Registry §6.1 retorna `resolution_path` sempre, e Identity §6.6 proíbe ocultar a cadeia de redirecionamento.

---

## 16. Eventos

Taxonomia operacional — mesma classe de `Registry Event` (Registry §11), `Composition Event` (Composition §11) e `Standard Event` (Doc 1 §16). Telemetria de substrato; **não** são Event Entities do Domain Model; **não** exigem Decision Record.

| Evento | Emitido quando |
|---|---|
| `PolicyDefinitionValidated` | `ValidatePolicyDefinition` retorna OK |
| `PolicyDefinitionRejected(invariant, detail)` | Qualquer invariante J1–J15 violado |
| `EffectivePolicySetResolved(subject, plane, binding_count)` | EPS gerado com sucesso |
| `PolicyConflictResolved(standard, strategy)` | `ResolveConflict` aplica BY_SPECIFICITY / BY_PRIORITY / BY_RESTRICTIVE_UNION |
| `IncomparableLevelsJoined(standard, [levels])` | `JoinLevels` produz `SyntheticLevel` (F2) |
| `IllegalGlobalOverrideAttempted(policy, target)` | Violação de PL4 |
| `CyclicOverrideChainDetected` | Violação de J10 |
| `PolicyActivated(policy@v)` | Transição a `Active` ou início de vigência |
| `PolicyExpired(policy@v)` | `expires_at` atingido |
| `DeprecatedStandardBound(policy@v, standard@v)` | Binding a Standard em `Deprecated` (F6) |
| `ArchivedStandardBoundDetected(policy@v, standard@v)` | Binding a Standard arquivado detectado pós-ativação (F7) |
| `IncompatibleApplicationPlane(policy@v, standard@v)` | Violação de J7 |
| `StandardsBoundMerged(subject, standard, outcome)` | Fase 5 do algoritmo (§11.1 linhas 28-35) |
| `LiveContextRejectedAtExecution(subject)` | Violação de PL7 |

---

## 17. Regras Normativas (RFC 2119)

| # | Regra | Nível |
|---|---|---|
| **PL1** | Policy MUST NOT conter critério normativo inline sob nenhuma forma | MUST NOT |
| **PL2** | Policy MUST referenciar Standard por Versioned Identifier, nunca por Coordinate sem versão | MUST |
| **PL3** | Policy MUST NOT referenciar Coordinate de implementação concreta (Skill, Agent, Workflow específico) | MUST NOT |
| **PL4** | Override MUST NOT suprimir Binding cujo Standard tenha `precedence_level = GLOBAL`; a violação MUST ser rejeitada na validação, não em runtime | MUST NOT |
| **PL5** | Conjunto normativo efetivo MUST ser a união de `standards_bound` e EPS, com prevalência do nível mais alto | MUST |
| **PL6** | `PolicyCondition` MUST ser predicado puro e determinístico | MUST |
| **PL7** | Avaliação em `applies_at = EXECUTION` MUST usar Context Snapshot (RFC-DM-001 §3.2), nunca Context vivo | MUST |
| **PL8** | Effective Policy Set MUST carregar `resolution_trace` completo | MUST |
| **PL9** | Cadeia de `overrides` MUST ser acíclica, verificada por Kernel §7 | MUST |
| **PL10** | Vigência temporal MUST ser atributo; MUST NOT ser modelada como estado de lifecycle | MUST / MUST NOT |
| **PL11** | Effective Policy Set MUST NOT ser cacheado indefinidamente | MUST NOT |
| **PL12** | Policy SHOULD declarar o `applies_at` mais estático que sua semântica permita | SHOULD |
| **PL13** | `scope.applies_at` MUST ser compatível com `ComplianceTarget.applies_to` dos NRs vinculados | MUST |
| **PL14** | Dimensões de `PolicyScope` MUST combinar-se por conjunção; valores dentro de cada dimensão por disjunção | MUST |
| **PL15** | Binding a Standard `GLOBAL` MUST declarar `conformance_mode = STRICT` | MUST |
| **PL16** | Conflito entre Conformance Levels incomparáveis MUST resolver pela união dos requisitos | MUST |
| **PL17** | Policy MAY omitir `condition`, tornando-se incondicional dentro do `scope` | MAY |
| **PL18** | Effective Policy Set MUST ser imutável após publicação | MUST |
| **PL19** | Policy MUST NOT ser registrada ou descoberta por serviço distinto do Registry existente | MUST NOT |
| **PL20** | Policy MUST NOT emitir veredito de conformidade nem modificar qualquer Component | MUST NOT |
| **PL21** | Policy MUST NOT declarar autoridade de aprovação; Governance §8 aplica-se integralmente | MUST NOT |
| **PL22** | Policy MUST NOT definir mecanismo de exceção; Governance §15 é o único mecanismo | MUST NOT |
| **PL23** | Resolução de conflito MUST ser determinística e total para toda configuração válida | MUST |
| **PL24** | Reavaliação em massa por mudança normativa SHOULD ser assíncrona e priorizada por risco | SHOULD |
| **PL25** | Policy MAY declarar `overrides` apenas sobre Policies em Namespace ancestral ou descendente | MAY |
| **PL26** | Resolução de conflito MUST NOT produzir resultado menos restritivo que qualquer Binding de entrada | MUST NOT |

---

## 18. Validação Institucional

| Documento base | Resultado | Evidência de conformidade |
|---|---|---|
| **Constitution** | **PASS** | PL4 realiza literalmente a regra de precedência não negociável; `enforcement_mode` realiza fricção proporcional ao risco; PL8 realiza Transparência; PL26 realiza o viés institucional pelo rigor |
| **Kernel Architecture** | **PASS** | Policy é Component pleno; `standards_bound` (§2.14) preservado e integrado, jamais depreciado; §2.9 e §7 reutilizados; §3 (Lifecycle) intocado |
| **Governance Architecture** | **PASS** | §7, §8, §12, §13, §15, §17 delegados integralmente; PL21 e PL22 garantem ausência de autoridade ou mecanismo paralelo |
| **Domain Model v1.1.0** | **PASS** | Zero entidades, zero relações, zero estados novos. Verificado item a item em §4.1 |
| **RFC-DM-001** | **PASS** | C2 (Context Snapshot) obrigatório em `applies_at = EXECUTION` (PL7); C1, C3, C4 não tocados |
| **Identity & Namespace** | **PASS** | §3, §5, §8 (ancestralidade), §10 (isolamento cross-org, garantido por construção em F14) reutilizados; §6.6 é o precedente de PL8 |
| **Registry & Discovery** | **PASS** | PL19 garante ausência de registry paralelo; §5, §6.1, §7.3, §8, §10 reutilizados; PL20 garante somente-leitura |
| **Validation & Certification** | **PASS** | §4 e §7 reutilizados sem redefinição; §5 (L3) recebe insumo estendido sem alteração de mecanismo; §6 (Reproducibility) é fundamento de PL6 e PL7 |
| **Composition Architecture** | **PASS** | Desbloqueia §14 sem alterá-lo; `Slot.condition` de §4 é o precedente estrutural de `PolicyCondition`; `Assembly` de §5 é o precedente de imutabilidade de EPS (PL18) |
| **Workflow Architecture** | **PASS** | `GATE_AUTO` (§4) consome EPS; Policy não vira Gate; padrão de Value Object de §4 replicado |
| **Execution Architecture** | **PASS** | Dispatch (§5) consome EPS contra Context Snapshot; EX1 (imutabilidade de Execution) preservada em F8/F9 |
| **Standards Architecture (Doc 1)** | **PASS** | Consome `VersionedIdentifier`, `ConformanceLevel`, `precedence_level`, ordem parcial de `inherits_from`, distinção Strict/Partial. Relação estritamente unidirecional — Standard não conhece Policy |
| **Restrições 1–10 do mandato** | **PASS** | (1) zero entidades ✔ (2) zero relações ✔ (3) zero lifecycle ✔ (4) tudo reutiliza Execution/Artifact/Decision/Evidence/Context/Role/Capability/Constraint/VersionedIdentifier/Registry/Certification/Governance ✔ (5) Policy é Component ✔ (6) n/a a este documento ✔ (7) Policy Binding é Value Object ✔ (8) EPS é Artifact genérico ✔ (9) nenhuma RFC ✔ (10) tudo por reutilização ✔ |
| **Exige RFC?** | **NÃO** | — |

---

## 19. Dependências Futuras

| Consumidor | O que consome | Estado |
|---|---|---|
| **Compliance Architecture** | EPS como entrada primária; `enforcement_mode` para classificar severidade; `resolution_trace` para auditoria | Downstream, não bloqueante |
| **Organization & Tenancy Architecture** | Preencherá `OrganizationRef` (hoje slot reservado de Identity §10); Policy já o referencia estruturalmente | Aditivo, sem bloqueio |
| **Composition Architecture §14** | Critério normativo em `Composition Slot` — **agora plenamente desbloqueado**: Doc 1 fornece o critério, este documento fornece a aplicabilidade | Fechado |
| **Agent Architecture** | `scope.roles` para restringir quais Roles um Agent pode ocupar — mecanismo relevante para o achado H2 (separação de funções), hoje resolvido apenas para Certificação L4 | Extensão natural, sem alteração deste documento |
| **Skill / Template Architecture** | `scope.component_types` e `scope.capabilities` específicos | Aditivo |
| **Observability & Provenance Storage** | Séries históricas de EPS e traces para análise de deriva de aplicabilidade | `[LACUNA proposital]` já declarada em Execution §14 |
| **Testing Architecture** | Avaliação de Policies em ambientes de teste via segmento `env.<environment>` (Identity §3.1, §8) | Aditivo |
