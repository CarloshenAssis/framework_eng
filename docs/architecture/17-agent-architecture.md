# Agent Architecture
### Framework Eng — A Especialização com Autoridade Decisória do Component

*Versão 1.0.0 · Base normativa (congelada): Constitution · Kernel · Governance · Domain Model v1.1.0 · RFC-DM-001 · Identity & Namespace · Registry & Discovery · Validation & Certification · Composition · Workflow · Execution · Standards · Policy · Template Architecture · Skill Architecture · Observability Architecture*

> **Tese central, provada seção a seção:** um `Agent` é, estruturalmente, **exatamente** um `Component` do tipo `Operational Component` — a mesma base de Skill. A diferença entre os dois não está na estrutura, está no **uso de um mecanismo já existente e até aqui subutilizado**: `Role` (Governance §2) pode ser *"ocupada por pessoa, time ou Agent"* — frase que consta, textualmente, no glossário do Domain Model desde sua primeira versão. Este documento não inventa autoridade decisória; ele **formaliza** uma frase que já estava lá, sem alterar nenhum documento anterior.

---

## 1. Posição Arquitetural

**Skill faz. Agent decide.** Formalmente: uma `Skill`, quando invocada, produz um `Artifact` dentro dos limites do seu `Contract` — nunca detém autoridade (Governance §2-§8) sobre o que acontece a seguir. Um `Agent`, quando invocado, **pode ocupar um `Role`** e, ao ocupá-lo, **pode autorizar `Decision`s** (Domain Model §14) — o mesmo mecanismo já usado por Reviewers, Stewards e Certifiers humanos, sem nenhuma extensão.

### 1.1 A diferença estrutural exata (e nada além dela)

| Dimensão | Skill | Agent |
|---|---|---|
| Categoria (Domain Model §3) | Operational Component | Operational Component — **idêntica** |
| Manifest (Kernel §2) | 15 campos + `templates[]` | 15 campos + `templates[]` — **idêntico** |
| Produz | `Artifact` via `Execution` | `Artifact` via `Execution` — **idêntico** |
| Autoridade | Nenhuma | **Pode** ocupar `Role` e autorizar `Decision` |
| Orquestração de outros Components | Nenhuma exigida (mas permitida via `depends_on`/`provides_for`, Kernel §10) | Resolve Providers **dinamicamente**, em tempo de Execution, em vez de seguir um grafo estático de Phase/Step |

**Nenhuma linha da tabela introduz um campo, entidade ou relação nova.** A distinção inteira se resume a **uma relação já anunciada** (`Role` ocupada por `Agent`) que este documento formaliza pela primeira vez.

### 1.2 Por que Agent não usa Phase/Step (Workflow §4)

`[ESCOLHA DE DESIGN]`

**Motivação:** decidir se a orquestração de Skills por um Agent deveria reutilizar a Orchestration Definition (Phase/Step/Gate/Branch) já especificada por Workflow Architecture §4.

**Alternativas rejeitadas:** modelar Agent como um Workflow cujo grafo de Phases é "dinâmico" ou "auto-modificável".

**Justificativa técnica:** Workflow §4 exige que o grafo de Phases seja **estático, validável e acíclico antes da execução** (`validate_workflow_definition`, Workflow §5) — essa é precisamente a propriedade que torna um Workflow certificável em L2/L3 (Validation & Certification §7: *"grafo de fases acíclico e bem formado"*) e auditável antes do primeiro uso. Um Agent, por definição, decide sua próxima ação **durante** a `Execution`, com base em raciocínio sobre `Inputs`/`Context` — não existe grafo para validar antecipadamente sem eliminar exatamente a propriedade que justifica a existência de um Agent (se a sequência fosse previsível, um Workflow já resolveria o problema, e um Agent seria redundante). Forçar Agent a declarar um grafo estático seria uma contradição de propósito, não uma reutilização.

**Precedentes arquitetônicos:** a mesma distinção existe em sistemas de orquestração maduros — um DAG do Airflow/Argo (estático, validado antes da execução) resolve o caso "sequência conhecida"; um *agente* de ferramentas (tool-calling loop) resolve o caso "sequência decidida em tempo real" — as duas abordagens coexistem porque resolvem problemas estruturalmente diferentes, nunca uma substitui a outra.

### 1.3 Fronteiras negativas (invioláveis)

| Fronteira | Regra |
|---|---|
| Agent não é uma nova categoria de autoridade | Toda `Decision` que um Agent autoriza usa exatamente a mesma autoridade já delegada a um `RoleClass` por Governance §8 — nunca uma autoridade paralela |
| Agent não cria novo Lifecycle | Kernel §3, sem exceção — idêntico a Skill |
| Agent não cria novo mecanismo de Composition | `ResolveSlot` (Composition §7) trata Agent como candidato elegível igual a Skill |
| Agent não decide fora do escopo do Role que ocupa | Uma `Decision` autorizada por um Agent **MUST** estar dentro da autoridade já delegada àquele `RoleClass` (Governance §8) — Agent não expande autoridade, apenas a exerce quando ocupa o Role |
| Agent não substitui Governance | A concessão de autoridade a um `RoleClass` continua sendo decisão de Governance (§4, §8); este documento formaliza apenas *quem pode ocupar* o Role, nunca *o que o Role pode fazer* |

---

## 2. Objetivos

| # | Objetivo | Mecanismo |
|---|---|---|
| O1 | Formalizar "Role ocupada por Agent" — frase já presente no Domain Model desde sua origem, nunca operacionalizada | `RoleAssignment` como família nomeada de Decision (§5.2) |
| O2 | Fechar o achado H2 no caso geral (separação de funções quando o ocupante de um Role é um Agent) | §7 — regra de coautorização humana por `RoleClass` |
| O3 | Definir orquestração dinâmica de Skills sem replicar Phase/Step de Workflow | §6, §8 |
| O4 | Reutilizar integralmente a escada L0–L4 de Certificação como gradiente de autonomia, sem inventar "Trust Level" | §6.3 |
| O5 | Provar que zero entidade, relação, estado ou autoridade nova foi introduzida | §16 |

---

## 3. Escopo

### 3.1 Pertence

Estrutura do Manifest de um Agent; formalização de `RoleAssignment` (ocupação de Role por Agent); regra de separação de funções generalizada (fecha H2); resolução dinâmica de Providers durante `Running`; distinção entre saída ordinária de Execution (Artifact) e saída com efeito institucional (Decision); uso de Certificação como gradiente de autonomia.

### 3.2 Não pertence — com justificativa

| Excluído | Justificativa |
|---|---|
| O que um `RoleClass` pode decidir | Governance §8 ("Quem Pode Alterar o Quê") — imutável; Agent Architecture não redefine autoridade, apenas quem pode exercê-la |
| Estrutura de Templates/Prompt do Agent | Template Architecture — reutilizada integralmente, sem extensão |
| Certificação de um Agent | Validation & Certification §5, §7 — já nomeia Agent explicitamente ("cenários comportamentais representativos; L4 exige avaliação humana"); este documento consome, não redefine |
| Orquestração estática auditável | Workflow Architecture — permanece o mecanismo correto quando a sequência é conhecida a priori; Agent não a substitui |
| Modelo interno de "raciocínio" do Agent (arquitetura do modelo subjacente) | Opaco ao Framework, mesma fronteira já estabelecida para o "processamento efetivo" de uma Skill (Skill §6.3) — Kernel §9: Contract declara o quê, nunca o como |

---

## 4. Modelo Conceitual

### 4.1 Tabela de proveniência — prova de minimalidade

| Conceito usado por Agent | Natureza | Já definido em |
|---|---|---|
| `Component`, `Operational Component` | **Reutilizado** | Kernel §1-§2; Domain Model §3 |
| Manifest de 15 campos + `templates[]` | **Reutilizado, sem campo novo** | Kernel §2; Template Architecture §4.2 |
| `Role`, `RoleClass` | **Reutilizado** | Governance §2, §4 |
| "Role ocupada por... Agent" | **Reutilizado — já enunciado, nunca operacionalizado** | Domain Model §20 (glossário) |
| `Decision`, `Decision Record` | **Reutilizado** | Domain Model §14, RFC-DM-001 §3.4 |
| Padrão de família nomeada de Decision (`CertificationGrant`, `CertificationRevocation`...) | **Reutilizado, mesmo padrão aplicado a nova família** | Validation & Certification §3 (decisão de reuso já documentada lá) |
| `Capability` | **Reutilizado, com uso semântico estendido (§5.1)** | Kernel §2.9 |
| Certificação L0–L4 | **Reutilizado como gradiente de autonomia, sem novo eixo** | Validation & Certification §5, §7 |
| `Composition Slot`, `ResolveSlot` | **Reutilizado, invocado dinamicamente em vez de estaticamente** | Composition §4, §7 |
| `Execution`, correlação via `Context` (`orchestration_id`) | **Reutilizado, sem plano estático prévio** | Domain Model §8; Execution §4 |
| `Context Snapshot` | **Reutilizado** | RFC-DM-001 §3.2 |
| `Provenance Chain` (pergunta 3: "quem foi responsável?") | **Reutilizado como mecanismo de resolução de ocupante** | Observability §5.4, §9.2 |
| `Policy.scope.roles` | **Reutilizado, agora ativado** | Policy §5.2, §19 (dependência já declarada) |
| `Governance §14` (Risk Management, rigor proporcional) | **Reutilizado como fundamento da regra de coautorização** | Governance §14 |

**Nenhuma linha introduz entidade, relação, estado ou campo de Manifest novo.**

### 4.2 `RoleAssignment` — a formalização central

`[ESCOLHA DE DESIGN]`

**Motivação:** decidir como registrar, de forma auditável e versionável, que um Agent específico (Coordinate@version) ocupa um Role específico durante um intervalo de tempo — dado que nem Domain Model nem Governance jamais formalizaram essa relação como campo ou tabela própria.

**Alternativas rejeitadas:** (a) introduzir uma relação `occupies: Agent → Role` no Domain Model, exigindo RFC de emenda; (b) introduzir uma entidade `RoleOccupancy` própria, com Lifecycle dedicado.

**Justificativa técnica:** exatamente o mesmo problema — "como registrar um fato institucional, temporal, revogável, com autoridade que o concede" — já foi resolvido, sem nova entidade, pelo padrão de família nomeada de Decision usado em Validation & Certification §3 para Certificação (`CertificationGrant`/`Renewal`/`Suspension`/`Revocation`) e no rascunho de Compliance (não ratificado, mas cuja decisão de design permanece válida como precedente) para Waiver. `RoleAssignment` segue o mesmo padrão: é uma `Decision`, autorizada por quem já detém autoridade de Governance sobre aquele `RoleClass` (Governance §4, Stewardship), que produz um `Decision Record` imutável — sem exigir nenhuma alteração ao Domain Model.

**Justificativa formal:** a pergunta "quem ocupava o Role X no momento T" é respondida por: *a `RoleAssignment`-família de Decision Record mais recente, não superada, referenciando (Role=X) com `effective_from ≤ T`* — mesma lógica de resolução já usada por Policy §7.4 (união restritiva por precedência temporal) e por Observability §9.2 (Provenance Chain, pergunta 3, "quem foi responsável").

**Precedentes arquitetônicos:** a mesma técnica — modelar atribuição de papel como um evento de decisão registrado, nunca como um campo mutável de estado — é usada em sistemas de RBAC maduros baseados em *event sourcing*, onde "role binding" é um evento append-only, nunca um campo editável.

```
RoleAssignment ⊂ Decision {
  subtype        : ROLE_ASSIGNMENT_GRANT | ROLE_ASSIGNMENT_REVOCATION
  role_class     : RoleClass                          [Governance §2]
  occupant       : VersionedIdentifier                (Agent, ou referência a pessoa/time — Governance §3)
  effective_from : Timestamp
  expires_at     : Timestamp?
  authorized_by  : Role                                [Governance §4 — Steward do RoleClass]
  co_authorized_by : Role?                              [§7 — coautorização humana quando exigida]
}
```

Produz `Decision Record` (Domain Model §14) — **nenhuma estrutura além da já existente**.

---

## 5. Estrutura do Manifest

| Campo do Component Contract (Kernel §2) | Uso por um Agent |
|---|---|
| `identity` | `component_type = Agent`; convenção `<ns>/agent.<papel>` (já prevista em Registry §5) |
| `capabilities` | Inclui, além das capacidades funcionais, **capacidades de elegibilidade de Role** — §5.1 |
| `templates[]` | `PROMPT Template` estrutura o raciocínio decisório do Agent — reutilizado sem extensão (Template §4.3) |
| `constraints` | Limita explicitamente o escopo de autonomia — ex.: teto de risco autorizável sem coautorização humana |
| `validation` | Critério de correção — Kernel §2.15, reutilizado |
| Demais campos | Idênticos a Skill — §5 daquele documento, sem alteração |

### 5.1 Capability como elegibilidade de Role

`[ESCOLHA DE DESIGN]`

**Motivação:** decidir onde declarar quais `RoleClass` um Agent está apto a ocupar — exigiria, à primeira vista, um campo novo (`eligible_roles[]`).

**Alternativas rejeitadas:** introduzir `eligible_roles: [RoleClass]` como décimo sexto campo do Component Contract.

**Justificativa técnica:** Kernel §2.9 já define `Capability` como *"o vocabulário de ações ou resultados que o componente oferece ao restante do sistema"* — ocupar um `RoleClass` **é** uma ação que o Agent oferece ao sistema, exatamente na mesma categoria semântica de qualquer outra Capability. Declarar `capability: role-eligibility.reviewer` é reuso direto do campo já existente, descoberto pelo mesmo `search(capability)` (Registry §6.2) que já resolve qualquer outra Capability — sem exigir alteração ao Kernel nem a Registry.

**Precedentes arquitetônicos:** a mesma técnica de expressar "elegibilidade para um papel" como uma capacidade descoberta (não como um campo de schema dedicado) é usada em sistemas de *capability-based security* (ex.: modelos de permissão do E, Cap'n Proto) — a posse de uma capability é, ela própria, a prova de elegibilidade, sem registro paralelo.

**Regra de consistência (AG1):** um `RoleAssignment` **MUST NOT** ser concedido a um Agent que não declare a `Capability` de elegibilidade correspondente ao `RoleClass` — verificado na autorização da Decision, reutilizando `Kernel§2.9` sem extensão.

---

## 6. Contrato do Agent — Elegibilidade, Certificação e Autonomia

### 6.1 Gradiente de autonomia = escada de Certificação já existente

`[ESCOLHA DE DESIGN]`

**Motivação:** decidir como graduar "quanto um Agent pode decidir sozinho" — a tentação natural é introduzir um eixo próprio (`AutonomyLevel: Assisted | Supervised | Autonomous`).

**Alternativas rejeitadas:** introduzir `AutonomyLevel` como novo Value Object paralelo à Certificação.

**Justificativa técnica:** Validation & Certification §5 já define exatamente o gradiente necessário — L0 (Unverified) a L4 (Institutionally Certified, exige Certifier humano e Reproducibility) — e §7 já nomeia Agent explicitamente: *"L4 exige avaliação humana"*. Introduzir um segundo eixo de gradiente duplicaria semântica já certificada, produzindo exatamente a ambiguidade terminológica que RFC-DM-001 eliminou nos achados C1/H1 (dois lugares medindo "o quanto confiar", potencialmente divergentes).

**Regra de vinculação (AG2):** a elegibilidade de um Agent para ocupar um `RoleClass` de risco `R` **MUST** exigir Certificação de nível mínimo proporcional a `R`, seguindo a mesma tabela de rigor proporcional já estabelecida por Governance §14 (Risk Management) — **nenhuma tabela nova é introduzida**; a already-existing tabela de Governance §14 é referenciada por `RoleClass.risk_tier`, atributo já implícito em Governance §2.

### 6.2 Distinção entre saída ordinária e saída com efeito institucional

Toda `Execution` de um Agent produz `Artifact` (Domain Model §7) — isso é **sempre** verdadeiro, sem exceção, exatamente como para Skill. A diferença surge apenas quando o conteúdo dessa saída constitui uma ação que Governance já classifica como `Decision` (Governance §8 — Admission, Certification, Conflict Resolution, etc.):

```
SE resultado_da_execução ∈ {ações já classificadas como Decision por Governance §8}
   E Agent ocupa Role com autoridade sobre essa classe de Decision (RoleAssignment vigente)
ENTÃO
   resultado ⟹ Decision, produz Decision Record (Domain Model §14)
SENÃO
   resultado ⟹ Artifact ordinário (mesma semântica de Skill §6.2)
```

**Regra (AG3):** um Agent **MUST NOT** produzir `Decision Record` fora de uma `RoleAssignment` vigente no momento da `Execution` (verificável via Context Snapshot, RFC-DM-001 §3.2) — a ausência de `RoleAssignment` válido reduz o resultado a `Artifact` ordinário, **nunca** a uma Decision institucional, mesmo que o conteúdo textual pareça uma decisão.

### 6.3 Resolução dinâmica de Providers

Um Agent **MAY** resolver `Composition Slot`s (Composition §7) **durante** sua própria `Execution` (entre `Initiated` e `Completed`), invocando Skills como Providers — cada invocação produz uma `Execution` filha correlacionada pelo mesmo `orchestration_id` (Execution §4), exatamente como um Step de Workflow, **sem** exigir um `Execution Plan` (Execution §4) prévio, porque não há grafo estático a planejar (§1.2).

---

## 7. Fluxo de Decisão — fechamento do achado H2

**Regra de separação de funções generalizada (AG4):**

> Uma `RoleAssignment` para `RoleClass` com `risk_tier ≥ MÉDIO` **MUST** ser autorizada por um `Role` ocupado por humano (`authorized_by`), e toda `Decision` autorizada por um Agent ocupando esse `RoleClass` **MUST** ser coautorizada (`co_authorized_by`) por um `Role` ocupado por humano quando a Decision afeta um Component da **mesma categoria operacional** do Agent decisor (ex.: um Agent-Reviewer avaliando outro Agent).

Isso generaliza, sem introduzir mecanismo novo, a regra já estabelecida em Validation & Certification §5 apenas para L4 de Agent (*"um Agent MUST NOT ser o único certificador L4 de outro Agent da mesma categoria"*) — aplicando o mesmo princípio a **qualquer** Decision, não apenas Certificação, fechando o achado H2 no caso geral conforme prometido em Skill §17 e Policy §19.

**Regra de não-autoaprovação (AG5, reforço explícito):** um Agent **MUST NOT** ocupar simultaneamente Role de Owner e Role de Reviewer/Certifier/Steward sobre o mesmo Component — mesma regra já enunciada em Governance §2 ("ninguém pode ser simultaneamente Reviewer e Owner do mesmo componente"), agora explicitamente estendida a ocupantes do tipo Agent, fechando a lacuna que a revisão institucional original apontou (a regra bloqueava apenas o mesmo Component, não a mesma categoria — AG4 cobre exatamente essa extensão).

---

## 8. Fluxo de Execução Completo

```
1. Governance identifica necessidade de Role X (ex.: Reviewer de um novo Skill)              [Governance §7]
2. Registry.search(capability="role-eligibility.reviewer", min_certification_level=L2)        [Registry §6.2]
3. Candidatos filtrados por RoleAssignment ausente/expirada e por AG2 (Certificação mínima)
4. RoleAssignment(GRANT) autorizada por Steward — coautorização humana se risk_tier≥MÉDIO      [§6.1, AG4]
   → Decision Record produzido                                                                  [Domain Model §14]
5. Agent invocado: Execution.Dispatch — Context{orchestration_id, ...}, Context Snapshot        [Execution §5]
6. Durante Running: Agent MAY resolver Slots dinamicamente, invocando Skills                    [§6.3]
   cada invocação → Execution filha correlacionada pelo mesmo orchestration_id
7. Agent produz resultado:
   a. SE constitui ação classificada por Governance §8 E RoleAssignment vigente:
      → Decision + coautorização se AG4 exigir → Decision Record                                [§6.2, AG3]
   b. SENÃO: Artifact ordinário                                                                  [§6.2]
8. Execution → Completed                                                                          [Domain Model §8]
```

Nenhum passo introduz operação de escrita nova — `RoleAssignment` reutiliza Decision/Decision Record; resolução de Slot reutiliza Composition; dispatch reutiliza Execution; correlação reutiliza a convenção de Context já normatizada.

---

## 9. Algoritmos

```
ALGORITMO GrantRoleAssignment(agent_ref, role_class, requested_by):
  ENTRADA: agent_ref : VersionedIdentifier, role_class : RoleClass
  SAÍDA:   DecisionRecord | AuthorizationError

  1  manifest ← Registry.resolve(agent_ref)
  2  SE "role-eligibility." + role_class.name ∉ manifest.capabilities:
  3     RETORNA AuthorizationError(NOT_ELIGIBLE)                                      # AG1
  4  cert ← Certification.current_level(agent_ref)
  5  SE cert < MinimumLevelFor(role_class.risk_tier):                                  # AG2
  6     RETORNA AuthorizationError(INSUFFICIENT_CERTIFICATION)
  7  SE role_class.risk_tier ≥ MEDIO ∧ ¬IsHuman(requested_by):
  8     RETORNA AuthorizationError(HUMAN_AUTHORIZATION_REQUIRED)                       # AG4
  9  ASSERT NOT (agent_ref já ocupa Owner sobre Component-alvo E role_class ∈ {Reviewer,Certifier,Steward})  # AG5
 10  decision ← Decision(subtype=ROLE_ASSIGNMENT_GRANT, occupant=agent_ref,
                          role_class, authorized_by=requested_by,
                          effective_from=now())
 11  RETORNA decision.produces(DecisionRecord)                                          # Domain Model §14

ALGORITMO ResolveCurrentOccupant(role_class, at: Timestamp):
  # responde "quem ocupava este Role no instante T" — reusa Observability, pergunta 3 (§9.2 daquele doc)
  grants ← Governance.query(subtype ∈ {ROLE_ASSIGNMENT_GRANT, ROLE_ASSIGNMENT_REVOCATION},
                             role_class = role_class)
  vigentes ← Filter(g: g.effective_from ≤ at ∧ (g.expires_at = null ∨ at < g.expires_at)
                     ∧ ¬Superseded(g, REVOCATION válida antes de `at`))
  RETORNA MaisRecente(vigentes).occupant | ausente

ALGORITMO ClassifyAgentOutput(execution, result):
  role ← ResolveCurrentOccupant(execution.role_class_declarado, at=execution.context_snapshot.timestamp)
  SE role = ausente:
     RETORNA Artifact(result)                                                            # AG3
  SE ¬IsGovernanceClassifiedAction(result, Governance§8):
     RETORNA Artifact(result)
  SE RequiresCoAuthorization(role.role_class) ∧ ¬execution.co_authorized_by:              # AG4
     RETORNA PendingCoAuthorization(result)
  RETORNA Decision(result, authorized_by=role).produces(DecisionRecord)
```

**Terminação e determinismo:** `ResolveCurrentOccupant` opera sobre um conjunto finito de Decision Records (append-only, imutáveis — Domain Model §14) ordenado por timestamp — mesma prova de terminação já usada em Policy §11.1 (Effective Policy Set) e Standards §12.1.

---

## 10. Diagramas

### 10.1 UML — Agent como especialização, RoleAssignment como Decision

```
┌─────────────────────────┐
│ «abstract» Component      │
└─────────────┬────────────┘
               △
┌─────────────┴────────────┐
│ Operational Component      │
└─────────────┬────────────┘
               △
       ┌───────┴───────┐
       │     Agent      │   identity.component_type = Agent
       │                │   capabilities[] inclui "role-eligibility.*"
       └───────┬───────┘
                │0..*
                ▼
         templates[] : Template   [reutilizado, Template §4]

┌──────────┐  authorizes  ┌────────────────────────┐  produces  ┌───────────────┐
│  Role     │◄─────────────┤ RoleAssignment ⊂ Decision│───────────►│ Decision Record│
│  (Gov §2) │              │  occupant → Agent@version│           │  (imutável)     │
└──────────┘              └────────────────────────┘           └───────────────┘
```

### 10.2 Sequência — concessão e exercício de autoridade

```
Governance      RoleAssignmentSvc     Registry      Certification      Agent(runtime)
    │                  │                 │                │                  │
    ├─GrantRoleAssignment(agent,role)───►│                │                  │
    │                  ├─resolve(agent)─►│                │                  │
    │                  │◄─manifest───────┤                │                  │
    │                  ├─current_level──────────────────►│                  │
    │                  │◄─cert_level──────────────────────┤                  │
    │                  ├─checa AG1,AG2,AG4,AG5             │                  │
    │◄─DecisionRecord───┤ (RoleAssignment GRANT)           │                  │
    │                                                                         │
    │  [tempo depois — Agent invocado dentro do escopo do Role]              │
    ├─Dispatch(agent, ctx)──────────────────────────────────────────────────►│
    │                                                        Context Snapshot│
    │                                              (opt) resolve Slots, invoca Skills
    │                                                        (Execution filha, orchestration_id)
    │◄─resultado ──────────────────────────────────────────────────────────┤
    ├─ClassifyAgentOutput(resultado)
    │   alt ação classificada por Governance §8 E RoleAssignment vigente
    │      ├─checa AG4 (coautorização) ──► Decision + Decision Record
    │   alt caso contrário
    │      └─Artifact ordinário
```

### 10.3 Estados

Idêntico ao Kernel Lifecycle (§3) — sem exceção. `RoleAssignment`, como toda `Decision`, segue o ciclo já definido em Domain Model §8 (`Proposed → Authorized → Recorded`, imutável, superável apenas por novo registro). **Nenhum estado novo.**

---

## 11. Casos Extremos

| # | Caso | Tratamento |
|---|---|---|
| E1 | Agent sem `Capability` de elegibilidade tenta ocupar Role | `AuthorizationError(NOT_ELIGIBLE)` (AG1) |
| E2 | Agent certificado abaixo do mínimo exigido pelo `risk_tier` do Role | `AuthorizationError(INSUFFICIENT_CERTIFICATION)` (AG2) |
| E3 | Tentativa de RoleAssignment de risco médio/alto autorizada apenas por outro Agent | `AuthorizationError(HUMAN_AUTHORIZATION_REQUIRED)` (AG4) |
| E4 | Agent-Owner tenta ocupar Reviewer sobre o mesmo Component | Rejeitado (AG5, extensão de Governance §2) |
| E5 | Agent produz saída textual que "parece" uma decisão sem RoleAssignment vigente | Classificado como `Artifact` ordinário, nunca `Decision` (AG3) — nenhum efeito institucional |
| E6 | Dois Agents resolvem Slots concorrentemente dentro da mesma orquestração | Seguro por construção — cada Execution filha é independente e imutável (mesmo argumento de Execution §9, Skill §11/S4-S7) |
| E7 | RoleAssignment expira durante uma Execution longa do Agent | Avaliada uma vez, no dispatch, contra Context Snapshot — expiração posterior não afeta a Execution em curso (mesma regra de Policy §14/F8, Skill §11/S5) |
| E8 | Agent tenta invocar a si mesmo recursivamente sem limite | Kernel §7 (Cycle Detection) aplica-se ao grafo de `depends_on`/`provides_for` declarado no Manifest; invocação dinâmica recursiva não declarada é limitada por `Constraint` (Kernel §2.10) de profundidade máxima, declarado no Manifest do Agent — nenhum mecanismo novo, apenas uso do já existente |
| E9 | RoleAssignment revogada enquanto uma Decision do Agent está sendo processada | `ResolveCurrentOccupant` é avaliado no momento exato da Decision (Context Snapshot); revogação posterior não retroage sobre Decision Records já produzidos (imutabilidade, Domain Model §14) |
| E10 | Agent certificado L4 mas sem `co_authorized_by` disponível no momento (nenhum humano acessível) | Decision permanece `PendingCoAuthorization` — Execution **MUST NOT** forçar Decision sem coautorização; comportamento correto é bloqueio, não bypass |

---

## 12. Performance

Idêntico a Skill §12 — resolução de Manifest, Assembly e Templates seguem exatamente o mesmo regime de cache (Registry §8, Composition §10, Template §12). Adicionalmente:

| Consulta | Cache |
|---|---|
| `ResolveCurrentOccupant(role_class, at)` | Cacheável indefinidamente para `at` no passado (Decision Records imutáveis); **não** cacheável para `at = now()` sem invalidação por evento (`RoleAssignmentGranted`/`Revoked`) |

Nenhuma política de cache nova além da reaplicação da regra já usada por Policy §15.1 (identidade versionada vs. dependente de tempo).

---

## 13. Eventos

Nenhum tipo de evento novo além da extensão nominal da família já usada por Certification/Waiver:

| Evento | Ocorre quando |
|---|---|
| `RoleAssignmentGranted` | AG-fluxo §9, `GrantRoleAssignment` bem-sucedido |
| `RoleAssignmentRevoked` | Revogação processada |
| `RoleAssignmentRejected(reason)` | Qualquer AG1/AG2/AG4/AG5 violado |
| `AgentDecisionProduced` | `ClassifyAgentOutput` produz `Decision Record` |
| `AgentOutputClassifiedAsArtifact` | `ClassifyAgentOutput` produz `Artifact` ordinário (AG3) |
| `PendingCoAuthorizationRaised` | E10 |

Todos os demais eventos aplicáveis a um Agent (registro, dispatch, certificação) são exatamente os já listados em Skill §13, filtrados por `component_type = Agent`.

---

## 14. Regras Normativas (RFC 2119)

| # | Regra | Nível |
|---|---|---|
| AG1 | Agent MUST declarar `Capability` de elegibilidade correspondente antes de receber `RoleAssignment` | MUST |
| AG2 | `RoleAssignment` MUST exigir Certificação mínima proporcional a `RoleClass.risk_tier` | MUST |
| AG3 | Saída de Agent MUST NOT ser classificada como `Decision` sem `RoleAssignment` vigente no Context Snapshot | MUST NOT |
| AG4 | `RoleAssignment`/`Decision` de risco médio/alto MUST exigir autorização/coautorização por Role ocupado por humano | MUST |
| AG5 | Agent MUST NOT ocupar simultaneamente Owner e Reviewer/Certifier/Steward sobre o mesmo Component | MUST NOT |
| AG6 | Agent MUST NOT declarar Phase/Step estático (Workflow §4) — orquestração é sempre dinâmica, por Slot | MUST NOT |
| AG7 | Revogação de `RoleAssignment` MUST NOT retroagir sobre Decision Records já produzidos | MUST NOT |
| AG8 | `ResolveCurrentOccupant` MUST ser determinístico para qualquer `at` no passado | MUST |
| AG9 | Agent MAY resolver Composition Slots dinamicamente durante `Running`, sem Execution Plan prévio | MAY |
| AG10 | Agent MUST NOT introduzir campo de Manifest além dos já normatizados por Kernel e Template Architecture | MUST NOT |

---

## 15. Integrações

| Documento | Como Agent o consome — sem alteração |
|---|---|
| **Kernel** | Component pleno; `Capability` (§2.9) reutilizada com uso semântico estendido (§5.1); `Constraint` (§2.10) limita autonomia |
| **Governance** | §2-§4 (Role, RoleClass, Stewardship), §8 (autoridade), §14 (Risk, fundamento de AG2/AG4) — nenhuma autoridade nova, apenas novo ocupante possível |
| **Domain Model v1.1.0** | Formaliza "Role ocupada por Agent" (glossário §20), já anunciado; `RoleAssignment` reusa `Decision`/`Decision Record` (§14) |
| **RFC-DM-001** | Context Snapshot (§3.2) é o instante de avaliação de `ResolveCurrentOccupant` (AG3, AG7) |
| **Identity & Namespace** | Coordinate, Versioned Identifier — sem exceção |
| **Registry & Discovery** | `search(capability="role-eligibility.*")` (§6.2) descobre candidatos, sem novo mecanismo |
| **Validation & Certification** | §5/§7 já nomeavam Agent e a exigência de Certifier humano em L4 — AG4 generaliza essa regra a qualquer Decision, não apenas Certificação |
| **Composition** | `ResolveSlot` invocado dinamicamente (§6.3), sem alteração ao algoritmo |
| **Workflow** | Um Agent **MAY** ser invocado como Provider de um Step (Workflow §4) — do ponto de vista do Workflow, indistinguível de uma Skill |
| **Execution** | Correlação via `orchestration_id`, dispatch — reutilizados sem Execution Plan prévio (AG9) |
| **Standards / Policy** | `Policy.scope.roles` (Policy §5.2, dependência já declarada em §19) é o mecanismo que agora restringe quais Namespaces/Organizações permitem Agent ocupar determinado `RoleClass` |
| **Template Architecture** | `PROMPT Template` estrutura o raciocínio decisório — reutilizado sem extensão |
| **Skill Architecture** | Agent invoca Skills como Providers exatamente como um Workflow o faria — nenhuma diferença de tratamento |
| **Observability Architecture** | `provenance()` (pergunta 3, "quem foi responsável") é o mecanismo de auditoria de qual Agent ocupava um Role em qualquer instante passado |

---

## 16. Validação Institucional

| Documento base | Resultado |
|---|---|
| Constitution | **PASS** — AG4/AG5 realizam "Confiança verificável" e "Responsabilidade"; nenhuma autoridade concedida sem verificação |
| Kernel | **PASS** — Component pleno; §2.9 reutilizado com extensão semântica legítima, não estrutural |
| Governance | **PASS** — §2 (não-autoaprovação) estendido a Agent (AG5) sem alterar o texto original; §8 intocado |
| Domain Model v1.1.0 | **PASS** — zero entidades/relações/estados; `RoleAssignment` = `Decision` |
| RFC-DM-001 | **PASS** — Context Snapshot como instante de avaliação (AG3, AG7, AG8) |
| Identity & Namespace | **PASS** |
| Registry & Discovery | **PASS** |
| Validation & Certification | **PASS** — generaliza regra já anunciada para L4/Agent, não a contradiz |
| Composition | **PASS** — Agent é candidato elegível, sem tratamento condicional |
| Workflow | **PASS** — Agent MAY ser Provider de Step, tratado uniformemente |
| Execution | **PASS** — dispatch/correlação sem Execution Plan (AG9), consistente com o modelo genérico |
| Standards | **PASS** |
| Policy | **PASS** — ativa `scope.roles`, já reservado |
| Template Architecture | **PASS** |
| Skill Architecture | **PASS** — mesma base estrutural |
| Observability Architecture | **PASS** — `provenance()` usado sem extensão |
| **Exige RFC?** | **NÃO** |

**Prova de fechamento do achado H2:** a regra AG4 generaliza, sem introduzir mecanismo novo, a exigência de coautorização humana de Validation & Certification §5 (antes restrita a L4) para **qualquer** `Decision` autorizada por um Agent em `RoleClass` de risco médio/alto — e AG5 estende a regra de não-autoaprovação de Governance §2 (antes implícita para "o mesmo Component") para "a mesma categoria operacional". **H2 está fechado no caso geral.**

---

## 17. Dependências Futuras

| Consumidor | O que consome | Estado |
|---|---|---|
| **Organization & Tenancy Architecture** | `Policy.scope.roles` combinado com `scope.organizations` para restringir Agent por tenant | Desbloqueado |
| **Testing Architecture** | Avaliação comportamental de Agent (Validation & Certification §7 — "cenários representativos") usando `query_events`/`trace()` (Observability) para regressão | Desbloqueado |
| **Packaging & Distribution Architecture** | Distribuição de `PROMPT Template` de Agents entre organizações | Sem bloqueio adicional |

---

## 18. Critério de Aceitação

### ✔ Checklist Institucional

| Critério | Status |
|---|---|
| Agent é Component, Operational Component | ✔ §1, §4 |
| Zero entidade/relação/estado/campo de Manifest novo | ✔ §4.1, AG10, §16 |
| "Role ocupada por Agent" formalizada sem alteração ao Domain Model | ✔ §4.2 |
| H2 fechado no caso geral | ✔ §7, §16 |
| Orquestração dinâmica sem duplicar Workflow | ✔ §1.2, AG6, AG9 |
| Gradiente de autonomia reusa Certificação, sem eixo novo | ✔ §6.1 |
| UML, sequência, algoritmos, casos extremos, RFC2119 | ✔ §9-§14 |
| Nenhuma RFC necessária | ✔ §16 |

### ✔ Confirmação Explícita

Nenhum documento da base normativa foi alterado. `RoleAssignment` é uma família nomeada de `Decision` (mesmo padrão de `CertificationGrant`); a elegibilidade de Role é uma `Capability` (mesmo campo, uso estendido); a coautorização humana generaliza uma regra já existente. **Agent Architecture fecha a infraestrutura institucional do Framework.**
