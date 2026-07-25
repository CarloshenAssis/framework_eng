# Organization & Tenancy Architecture
### Framework Eng — A Fronteira Institucional de Isolamento Multi-Organização

*Versão 1.0.0 · Base normativa (congelada): Constitution · Kernel · Governance · Domain Model v1.1.0 · RFC-DM-001 · Identity & Namespace · Registry & Discovery · Validation & Certification · Composition · Workflow · Execution · Standards · Policy · Template Architecture · Skill Architecture · Observability Architecture · Agent Architecture*

> **Tese central, provada seção a seção:** `Organization` fecha um slot **já reservado, nunca implementado**, em quatro documentos anteriores — Identity & Namespace §8/§10 (o segmento `org.<id>` e a garantia de isolamento), Identity & Namespace §2.1 (Organization listada como "forward-compatible... reserva o espaço estrutural sem especificar o modelo interno"), Policy §5.2 (`OrganizationRef` como "slot reservado") e Composition §14 (restrição de dependência cross-org, "hoje não bloqueante"). Este documento preenche esse slot **integralmente por reutilização**: `Organization` é um `Structural Component` — a mesma categoria de `Standard` e `Policy` — e "Membership" é uma consulta sobre `RoleAssignment`, mecanismo já formalizado por Agent Architecture §4.2.

---

## 1. Posição Arquitetural

Uma `Organization` é a especialização de **Structural Component** (Domain Model §3, mesma categoria de `Standard`/`Policy`) cuja `Identity` **coincide** com a raiz de um segmento de Namespace (`org.<id>`, Identity §8). Essa coincidência deliberada é o que torna Organization, ao mesmo tempo, (a) um Component versionado, governado e descoberto como qualquer outro, e (b) a fronteira física de isolamento já garantida por Identity §10 e Registry §10 — sem exigir dois mecanismos paralelos.

### 1.1 Por que Organization é um Component (e não um Value Object, como Template)

`[ESCOLHA DE DESIGN]`

**Motivação:** aplicar o mesmo teste funcional já usado para decidir que `Template` **não** deveria ter Identity própria (Template §1.1) — e verificar se Organization passa nesse teste em sentido oposto.

**Alternativas rejeitadas:** modelar Organization como Value Object escopado a algo (ex.: um campo dentro de Identity & Namespace), sem Identity, Lifecycle ou Manifest próprios.

**Justificativa técnica:** o teste já estabelecido é: *"um conceito merece Identity independente quando (a) é consumido por múltiplos Components não relacionados sob referência estável e versionada, e (b) sua evolução precisa ser rastreável independentemente de qualquer portador específico."* Organization passa nas duas condições, ao contrário de Template: (a) `Policy.scope.organizations` (Policy §5.2) já referencia Organizations a partir de Policies que **não pertencem** a essa Organization; Registry particiona por ela (Registry §10); dezenas de Components referenciam `org.<id>` como prefixo de Namespace — consumo amplo e externo, exatamente o padrão que justificou Component-hood para Standard/Policy. (b) Fatos de governança de uma Organization (quem é seu Steward, se está ativa/suspensa) evoluem no tempo e precisam de trilha de auditoria própria — não fazem sentido "dentro" do Manifest de outro Component.

**Precedentes arquitetônicos:** a mesma decisão já foi tomada, com o mesmo raciocínio, para Standard e Policy — nenhum precedente novo é necessário além do já estabelecido internamente por este próprio Framework.

### 1.2 Coincidência entre Identity de Organization e raiz de Namespace

`[ESCOLHA DE DESIGN]`

**Motivação:** decidir se `Organization` deveria ter um Coordinate próprio, distinto do token de Namespace `org.<id>` já reservado por Identity §8.

**Alternativas rejeitadas:** Coordinate de Organization em um Namespace separado (ex.: `system/organization.<id>`), com um campo `namespace_root` apontando para `org.<id>`.

**Justificativa técnica:** introduzir dois identificadores para o mesmo conceito (um para o Component, outro para o Namespace que ele governa) reproduziria exatamente a classe de ambiguidade que RFC-DM-001 eliminou nos achados C1/H1 — duas referências para uma única realidade institucional, com risco de divergirem. Fazer o Coordinate da Organization **ser** `org.<id>` elimina essa possibilidade por construção: arquivar o Component Organization e arquivar o Namespace que ele governa tornam-se, estruturalmente, o mesmo evento (§7.3).

**Precedentes arquitetônicos:** em Kubernetes, um `Namespace` é, ele mesmo, um objeto de primeira classe com seu próprio ciclo de vida (`kubectl get namespace`) — não existe um objeto separado "dono" de um Namespace distinto do próprio Namespace. A mesma unificação é aplicada aqui.

### 1.3 Fronteiras negativas (invioláveis)

| Fronteira | Regra |
|---|---|
| Organization não introduz novo mecanismo de isolamento | Isolamento **MUST** continuar sendo o particionamento físico por Namespace já normatizado (Identity §10, Registry §10) |
| Organization não define novo mecanismo de autoridade | Admissão, Ownership, Stewardship — Governance §7/§8, sem exceção |
| Organization não define billing, quotas ou consumo de recurso | `[LACUNA proposital]`, deferida — §3.2 |
| Organization não substitui Policy | `Policy.scope.organizations` continua sendo o mecanismo de aplicabilidade normativa por tenant; Organization apenas fornece o `VersionedIdentifier` que esse campo referencia |
| Organization não cria novo Lifecycle | Kernel §3, sem exceção — idêntico a qualquer Component |

---

## 2. Objetivos

| # | Objetivo | Mecanismo |
|---|---|---|
| O1 | Preencher o slot `Organization` reservado por Identity §2.1/§8/§10 | §1.2, §5 |
| O2 | Fechar `OrganizationRef` (Policy §5.2) como referência concreta e resolúvel | §5.1 |
| O3 | Definir "Membership" sem entidade nova | §6.1 — reuso de `RoleAssignment` (Agent §4.2) |
| O4 | Fechar a restrição de dependência cross-org anunciada por Composition §14 | §6.3 |
| O5 | Provar que isolamento multi-tenant não exige mecanismo além do já existente | §16 |

---

## 3. Escopo

### 3.1 Pertence

Estrutura do Manifest de uma Organization; ciclo de vida de criação/suspensão/decomissionamento; autoridade administrativa (Steward do Namespace); Membership como consulta derivada; restrição de dependência cross-organização via Standard+Policy; resolução de `OrganizationRef`.

### 3.2 Não pertence — com justificativa

| Excluído | Justificativa |
|---|---|
| Billing, quotas, consumo de recurso computacional | `[LACUNA proposital]` — já explicitamente deferida por Identity §10 e Policy §3.2; requer um documento próprio (`Resource & Quota Architecture`, futuro), pois envolve conceitos (medição de consumo, tarifação) que nenhum documento até aqui precisou tratar |
| Autenticação de membros | Fora de escopo desde Identity §1 — "não é autenticação/autorização" |
| Formato de onboarding comercial (contratos, SLAs) | Fora do domínio técnico do Framework |
| Mecanismo de isolamento físico | Já integralmente definido — Identity §10, Registry §10; este documento apenas o **consome**, não o redefine |

---

## 4. Modelo Conceitual

### 4.1 Tabela de proveniência — prova de minimalidade

| Conceito usado por Organization | Natureza | Já definido em |
|---|---|---|
| `Component`, `Structural Component` | **Reutilizado** | Kernel §1-§2; Domain Model §3 |
| Manifest de 15 campos | **Reutilizado, sem campo novo** | Kernel §2 |
| Coordinate = raiz de Namespace `org.<id>` | **Reutilizado, mesmo token** | Identity §8 |
| `Owner`, `Steward` | **Reutilizado** | Kernel §2.3; Governance §3-§4 |
| `RoleAssignment` (⊂ Decision) | **Reutilizado, generalizado além de Agent** | Agent Architecture §4.2 (já definido genericamente: *"occupant: VersionedIdentifier (Agent, ou referência a pessoa/time)"*) |
| Isolamento por Namespace | **Reutilizado, sem extensão** | Identity §10; Registry §10 |
| `Policy.scope.organizations` / `OrganizationRef` | **Reutilizado — este documento fecha o tipo referenciado** | Policy §5.2 |
| `Constraint` | **Reutilizado**, para restrição de dependência cross-org | Kernel §2.10 |
| `Standard.ComplianceTarget.applies_to = COMPOSITION` | **Reutilizado**, para NR que restringe Namespace de Providers | Standards §4.5 |
| Tombstone permanente de nome | **Reutilizado** | Identity §3.2 |
| Lifecycle | **Reutilizado, sem alteração** | Kernel §3 |
| `provenance()` / `query_events()` | **Reutilizado, para auditoria de Membership** | Observability §7.1, §9.2 |

**Nenhuma linha introduz entidade, relação ou estado novo.**

### 4.2 Estrutura formal

```
Organization (Structural Component) {
  identity          : "org." + <organization-id>       [Identity §8 — MESMO token do Namespace]
  version           : SemVer                            [Kernel §2.11 — governa a própria política institucional da org]
  lifecycle_state   : KernelLifecycleState               [Kernel §3 — sem alteração]
  owner             : Role                               [Kernel §2.3 — Steward administrativo — §6.1]

  capabilities      : [Capability]?                       (ex.: "org.hosts-regulated-workload" —
                                                             tag útil para Policy targeting, opcional)
  constraints       : [Constraint]?                        [§6.3 — restrição de dependência cross-org]
  metadata          : Metadata                             [Kernel §2.14 — nome legível, contato, categoria]
}
```

Nenhum campo além dos já definidos por Kernel §2. `capabilities`/`constraints` recebem **uso semântico**, não estrutural — mesmo padrão de reuso já aplicado a `Capability` em Agent §5.1.

---

## 5. Estrutura do Manifest e Referência

### 5.1 `OrganizationRef` — fechamento formal

`OrganizationRef` (Policy §5.2) **é**, sem qualquer extensão, um `VersionedIdentifier` (Identity §4.1) cujo Coordinate resolve, via Registry, a um Component com `component_type = Organization`:

```
OrganizationRef ≡ VersionedIdentifier   onde Registry.resolve(ref).component_type = Organization
```

Nenhum novo tipo de referência é introduzido — `Policy.scope.organizations` (Policy §5.2) passa a resolver, a partir de agora, contra Organizations reais no Registry, exatamente como `scope.capabilities` já resolvia contra `Capability` declarada em qualquer Component.

### 5.2 Convenção de nomenclatura

Reutiliza literalmente Identity & Namespace §5 e §8 — nenhuma convenção nova: `org.<organization-id>` é, simultaneamente, o Coordinate do Component Organization e a raiz do Namespace sob a qual todos os Components daquela organização vivem.

---

## 6. Membership, Autoridade e Isolamento Cross-Org

### 6.1 Autoridade administrativa = Ownership/Stewardship já existente

O `owner` declarado no Manifest de uma Organization **é** o Steward administrativo do Namespace `org.<id>` inteiro — a mesma autoridade que Governance §7/§8 já concede a qualquer Owner/Steward, apenas escopada ao Namespace da Organização em vez de a um domínio de Standards/Policies. **Nenhuma classe de autoridade nova é introduzida.**

### 6.2 Membership como projeção sobre `RoleAssignment`

`[ESCOLHA DE DESIGN]`

**Motivação:** decidir como representar "quem pertence a uma Organization" — a tentação natural seria uma lista `members: [PersonRef]` no Manifest.

**Alternativas rejeitadas:** campo `members[]` no Manifest da Organization, mutável diretamente.

**Justificativa técnica:** Agent Architecture §4.2 já resolveu exatamente este problema — "quem ocupa que autoridade, durante que intervalo, quem autorizou" — via `RoleAssignment`, uma família nomeada de `Decision`, deliberadamente **não** generalizada apenas a Agents (a definição original já incluía *"occupant: VersionedIdentifier (Agent, ou referência a pessoa/time)"*). "Ser membro de uma Organization" é o caso particular em que o `role_class` de um `RoleAssignment` está escopado ao Namespace `org.<id>` — não é um fato novo, é uma **consulta filtrada** sobre fatos já registrados.

```
ResolveMembers(org_ref, at) ≡ { r.occupant | r ∈ RoleAssignments vigentes em `at`
                                              ∧ r.role_class.namespace_scope ⊆ org_ref.namespace }
```

**Justificativa formal:** um campo `members[]` mutável exigiria reabrir o Manifest a cada mudança de composição — violando a imutabilidade de Manifest por versão (Kernel §8) ou forçando uma nova versão da Organization a cada admissão/saída de membro, o que é claramente incorreto (Membership não é uma propriedade *definicional* da Organization, é um fato *temporal*, exatamente a categoria de coisa que `Decision`/`Decision Record` já foi desenhada para capturar, Domain Model §14).

**Precedentes arquitetônicos:** o mesmo padrão — associação de identidade a um grupo modelada como evento de decisão, não como lista mutável — já foi usado para RoleAssignment em geral e é o padrão canônico de sistemas RBAC baseados em auditoria de eventos.

### 6.3 Restrição de dependência cross-organização — fechamento de Composition §14

Composition §14 declarou explicitamente: *"Policy Architecture (futuro) poderá restringir quais Namespaces são elegíveis em resolução cross-org — hoje não bloqueante."* Esta seção fecha esse compromisso, **sem introduzir mecanismo novo**, combinando dois já existentes:

1. Um `Standard` **MAY** declarar um `NormativeRequirement` com `ComplianceTarget.applies_to = COMPOSITION` cujo critério restringe o conjunto de Namespaces elegíveis como origem de um Provider resolvido (Standards §4.5, §4.6 — `EvaluationMethod` do tipo `STATIC`, avaliando o `Namespace` do candidato resolvido pela `Assembly`).
2. Uma `Policy` com `scope.organizations = [org_ref]`, `scope.applies_at = COMPOSITION`, `enforcement_mode = BLOCKING` vincula esse Standard à Organização específica que deseja a restrição (Policy §5.2, §8).

```
ex.: Standard "core/standard.isolation.no-external-dependencies" declara:
   NR: MUST — todo Provider resolvido para um Slot de Composition MUST pertencer
       ao Namespace `core/` ou ao próprio Namespace do requisitante
   target.applies_to = COMPOSITION

Policy "org.acme/policy.isolation.strict" vincula esse Standard,
   scope.organizations=[org.acme], enforcement_mode=BLOCKING
```

**Nenhum campo novo em Organization, Standard, Policy ou Composition é necessário** — a combinação já existente resolve integralmente o caso de uso.

---

## 7. Modelo Operacional

**Serviço:** nenhum serviço de substrato novo. Criação/suspensão/decomissionamento de uma Organization seguem **exatamente** o Admission Process e o Deprecation/Breaking Change process já normatizados por Governance §7/§10/§16, sem exceção — a única especialização é que a "Component" sendo admitida reserva, ao mesmo tempo, um segmento de Namespace (Identity §3.2, regra de reserva permanente já existente).

```
create_organization(candidate_id, manifest, requested_by) → DecisionRecord | AdmissionError
  PRE:  candidate_id ∉ tokens reservados (core, org, system, registry, urn — Identity §8)
        E "org." + candidate_id ∉ Namespace já reivindicado (Identity §3.2 — inclusive tombstones)
  POST: segue Governance §7 (Admission) sem exceção — Review, checagem de duplicação
        (Registry §5, "search" por Coordinate, trivial aqui pois Coordinate é único por construção),
        Approve, Active — Organization torna-se Component Active e raiz de Namespace simultaneamente

suspend_organization(org_ref, decision_record_ref) → void
  # transição Active → Deprecated, Governance §16, sem exceção

decommission_organization(org_ref, decision_record_ref) → void
  # transição → Archived → tombstone permanente do Namespace inteiro (Identity §3.2, estendido
  # à subárvore por consequência estrutural: nenhum novo Component pode ser admitido sob um
  # Namespace cuja raiz está Archived — mesma regra já aplicada individualmente a cada Coordinate)
```

---

## 8. Fluxo de Criação e Isolamento

```
1. Time requisita criação de Organization "acme-corp"                        [Governance §7]
2. Registry.search("org.acme-corp")                                          [Registry §5, dedup trivial]
3. Admission: Review → Approved → Active                                     [Governance §7]
4. Namespace "org.acme-corp/" reservado, raiz = Organization Component        [Identity §8, §3.2]
5. Steward (owner) da Organization aprova Admission de Components filhos      [§6.1]
6. Cada Component filho referencia "org.acme-corp/..." — isolado por
   construção de qualquer outro Namespace (Identity §10)                      [reutilizado, sem alteração]
7. Membership consultada sob demanda via RoleAssignment filtrado              [§6.2]
8. Dependências cross-Namespace, se restringidas, seguem Standard+Policy       [§6.3]
```

---

## 9. Algoritmos

```
ALGORITMO CreateOrganization(candidate_id, manifest, requested_by):
  1  ASSERT candidate_id ∉ {core, org, system, registry, urn}         # Identity §8, reservado
  2  coordinate ← "org." + candidate_id
  3  entry ← Registry.resolve(coordinate)
  4  SE entry ≠ NotFound ∧ entry.lifecycle_state ≠ Removed:
  5     RETORNA AdmissionError(NAMESPACE_ALREADY_CLAIMED)
  6  SE entry.lifecycle_state = Removed (tombstone):
  7     RETORNA AdmissionError(TOMBSTONE_RECYCLE_FORBIDDEN)             # Identity §3.2
  8  # segue Governance §7 sem exceção — dedup, Review, Approve
  9  decision ← Governance.Admit(coordinate, manifest, requested_by)
 10  Registry.register(manifest, decision.produces(DecisionRecord))     # Registry §5
 11  RETORNA decision.decision_record

ALGORITMO ResolveMembers(org_ref, at):
  ns ← org_ref.coordinate                                               # ex.: "org.acme-corp"
  assignments ← Governance.query(subtype ∈ {ROLE_ASSIGNMENT_GRANT, ROLE_ASSIGNMENT_REVOCATION})
  escopados ← Filter(a: NamespaceScope(a.role_class) ⊆ ns)
  vigentes ← Filter(a: a.effective_from ≤ at ∧ (a.expires_at=null ∨ at<a.expires_at)
                     ∧ ¬RevogadoAntesDe(a, at))                          # mesma lógica de Agent §9
  RETORNA { a.occupant PARA a EM vigentes }

ALGORITMO ValidateCrossOrgSlotResolution(candidate, requester_org_ref):
  SE Namespace(candidate) = "core" ∨ Namespace(candidate) ⊆ requester_org_ref.coordinate:
     RETORNA OK                                    # sempre permitido — núcleo compartilhado + próprio
  eps ← PolicyEval.resolve_effective_policy_set(requester_org_ref, ctx, now(), plane=COMPOSITION)  # Policy §11.1
  SE ∃ binding EM eps.bindings COM binding.standard exige isolamento E enforcement_mode=BLOCKING:
     nrs ← StandardResolver.resolve_effective_requirements(binding.standard, binding.conformance_level)  # Standards §12.1
     SE ¬Satisfies(candidate.namespace, nrs):
        RETORNA CompositionError(CROSS_ORG_DEPENDENCY_BLOCKED)           # §6.3
  RETORNA OK
```

**Terminação/determinismo:** `CreateOrganization` reutiliza `Governance.Admit` (já provado terminante e determinístico em Governance §7); `ResolveMembers` reutiliza exatamente `ResolveCurrentOccupant` (Agent §9), generalizado; `ValidateCrossOrgSlotResolution` reutiliza `ResolveEffectivePolicySet` (Policy §11.1) e `ResolveEffectiveRequirements` (Standards §12.1) sem modificação.

---

## 10. Diagramas

### 10.1 UML — Organization como Structural Component, coincidente com raiz de Namespace

```
┌─────────────────────────┐
│ «abstract» Component      │
└─────────────┬────────────┘
               △
┌─────────────┴────────────┐
│ Structural Component       │   [Domain Model §3 — mesma categoria de Standard, Policy]
└─────────────┬────────────┘
               △
       ┌───────┴───────┐
       │  Organization   │   identity = "org.<id>"  ══ raiz do Namespace (Identity §8)
       └───────┬───────┘
                │ owner
                ▼
             Role  [Governance §3-§4 — Steward administrativo do Namespace inteiro]

     ┌──────────────────────────────────────────┐
     │  Namespace "org.<id>/"                     │  ◄── mesmo token, isolamento por
     │   ├── domain.<bounded-context>/              │      Identity §10 / Registry §10,
     │   ├── env.<environment>/                      │      sem mecanismo adicional
     │   └── <component-name>                         │
     └──────────────────────────────────────────┘
```

### 10.2 Sequência — criação e consulta de membership

```
Requester      Governance        Registry        Identity(regras)
    │              │                │                  │
    ├─create_organization("acme-corp")────────────────►│
    │              │                │       valida token não-reservado, sem colisão
    │              │◄───────────────┤                  │
    │              ├─Admit (Review→Approved→Active)     │        [Governance §7 — sem exceção]
    │              ├─Registry.register ─────────────────►│
    │◄─DecisionRecord│                                   │
    │                                                    │
    │  [tempo depois]                                    │
    ├─ResolveMembers(org.acme-corp, now())───────────────►│
    │              ├─query RoleAssignment escopados a ns  │        [Agent §4.2, generalizado]
    │◄─{occupants}──┤                                     │
```

### 10.3 Estados

Idêntico ao Kernel Lifecycle (§3), sem exceção. **Nenhum estado novo.**

---

## 11. Casos Extremos

| # | Caso | Tratamento |
|---|---|---|
| O1 | `candidate_id` colide com token reservado (`core`, `system`...) | `AdmissionError(NAMESPACE_ALREADY_CLAIMED)` — mesma regra de Identity §8 |
| O2 | Recriação de Organization sob nome anteriormente decomissionado | `AdmissionError(TOMBSTONE_RECYCLE_FORBIDDEN)` — mesma regra de Identity §3.2, agora aplicada à raiz inteira de um Namespace |
| O3 | RoleAssignment escopado a `org.acme/domain.billing` — pertence à Organization "acme" ou ao domínio "billing"? | Ambos, sem conflito — `NamespaceScope ⊆ org.acme` inclui todos os descendentes; `ResolveMembers` retorna o occupant como membro de "acme" independentemente da profundidade do escopo declarado |
| O4 | Organization suspensa (`Deprecated`) tenta admitir novo Component filho | Permitido com aviso — mesma semântica já aplicada a qualquer Component `Deprecated` referenciado (Standards §7.4, Skill §11); Governance §13 monitora e pode escalar |
| O5 | Organization `Archived` — Component filho tenta resolver Assembly contra ela | Retorna Tombstone (Registry §6.1) — mesma regra já aplicada a qualquer Coordinate arquivado |
| O6 | Dois requesters tentam criar a mesma `candidate_id` concorrentemente | Serializado pela mesma disciplina de Governance §7 (uma aprovação por vez sobre o mesmo Coordinate) — nenhuma regra nova |
| O7 | Policy de isolamento (`enforcement_mode=BLOCKING`) criada **depois** de dependências cross-org já existirem | Dependências já resolvidas em `Assembly`s anteriores permanecem válidas (imutabilidade, Composition §5); apenas novas resoluções são bloqueadas — mesma regra de não-retroatividade já aplicada em Policy §14/F8 |
| O8 | Organization sem nenhum Component filho (namespace vazio) | Válido — mesma disciplina de "Standard sem nenhum NR" (Standards §14/E12): estruturalmente correto, apenas sem efeito prático ainda |

---

## 12. Performance

Idêntico ao regime já estabelecido para qualquer Component (Registry §8: cache indefinido de resolução por Versioned Identifier). `ResolveMembers` segue a mesma distinção já usada por Policy §15.1: cacheável indefinidamente para `at` no passado (Decision Records imutáveis); não cacheável indefinidamente para `at = now()`.

Particionamento: a Organization **é** a própria fronteira de particionamento já usada por Registry §10 e Observability §6.1 — este documento não introduz nenhum eixo de escala adicional; apenas nomeia formalmente o que já era, implicitamente, o eixo mais usado de todos.

---

## 13. Eventos

Nenhum tipo de evento além da reaplicação nominal já usada por Registry/Governance:

| Evento | Ocorre quando |
|---|---|
| `OrganizationCreated` | `CreateOrganization` bem-sucedido — mesma classe de `ComponentRegistered` (Registry §11) |
| `OrganizationSuspended` | Transição `Active → Deprecated` |
| `OrganizationDecommissioned` | Transição `→ Archived` |
| `CrossOrgDependencyBlocked` | `ValidateCrossOrgSlotResolution` retorna `CompositionError` |

---

## 14. Regras Normativas (RFC 2119)

| # | Regra | Nível |
|---|---|---|
| OR1 | Organization MUST ser um Structural Component, com Coordinate idêntico à raiz do Namespace que governa | MUST |
| OR2 | `candidate_id` MUST NOT colidir com token reservado nem com tombstone existente | MUST NOT |
| OR3 | Membership MUST ser derivado de `RoleAssignment`, MUST NOT ser campo mutável de Manifest | MUST / MUST NOT |
| OR4 | Autoridade administrativa de uma Organization MUST reutilizar Ownership/Stewardship de Governance §3-§4, sem classe de autoridade nova | MUST |
| OR5 | Restrição de dependência cross-org MUST ser expressa via Standard+Policy, nunca via campo específico de Organization | MUST |
| OR6 | Decomissionamento MUST tornar toda a subárvore de Namespace permanentemente reservada (Identity §3.2), nunca reciclável | MUST |
| OR7 | Organization MUST NOT introduzir campo de Manifest além dos já normatizados por Kernel §2 | MUST NOT |
| OR8 | Dependência já resolvida em Assembly existente MUST NOT ser invalidada retroativamente por Policy de isolamento criada posteriormente | MUST NOT |

---

## 15. Integrações

| Documento | Como Organization o consome — sem alteração |
|---|---|
| **Kernel** | Component pleno; nenhum campo novo |
| **Governance** | Admission/Deprecation/Ownership/Stewardship — §7, §8, §16, sem exceção |
| **Domain Model v1.1.0** | Organization = Structural Component; Membership = `Decision`/`Decision Record` |
| **Identity & Namespace** | Preenche exatamente o slot de §2.1, §8, §10 — nenhuma regra de isolamento nova |
| **Registry & Discovery** | Registro/descoberta idênticos a qualquer Component; particionamento por Organization já era o eixo natural de §10 |
| **Policy** | `OrganizationRef` (§5.2) resolvido; `scope.organizations` agora aponta a Organizations reais |
| **Standards** | NR com `applies_to=COMPOSITION` é o mecanismo de restrição cross-org (§6.3) |
| **Composition** | Fecha §14 — restrição cross-org sem campo novo em Composition |
| **Agent Architecture** | `RoleAssignment` generalizado além de Agent para Membership (§6.2) |
| **Observability** | `provenance()`/`query_events()` auditam Membership histórica sem mecanismo novo |

---

## 16. Validação Institucional

| Documento base | Resultado |
|---|---|
| Constitution | **PASS** |
| Kernel | **PASS** — Component pleno, zero campo novo |
| Governance | **PASS** — nenhuma autoridade nova |
| Domain Model v1.1.0 | **PASS** — zero entidades/relações/estados |
| RFC-DM-001 | **PASS** |
| Identity & Namespace | **PASS** — preenche exatamente o slot já reservado |
| Registry & Discovery | **PASS** |
| Validation & Certification | **PASS** |
| Composition | **PASS** — fecha §14 |
| Workflow / Execution | **PASS** |
| Standards / Policy | **PASS** — `OrganizationRef` fechado; restrição cross-org via combinação já existente |
| Template / Skill | **PASS** |
| Observability | **PASS** |
| Agent Architecture | **PASS** — `RoleAssignment` reutilizado exatamente como generalizado desde sua origem |
| **Exige RFC?** | **NÃO** |

---

## 17. Dependências Futuras

| Consumidor | O que consome | Estado |
|---|---|---|
| **Resource & Quota Architecture** (futuro) | Coordinate de Organization como unidade de medição de consumo | `[LACUNA proposital]`, explicitamente deferida — §3.2 |
| **Testing Architecture** | Ambientes de teste isolados por `org.<id>/env.<environment>` (Identity §3.1, já reservado) | Sem bloqueio |
| **Packaging & Distribution Architecture** | Distribuição de Standards/Templates entre Organizations distintas via `core/` compartilhado | Sem bloqueio |

---

## 18. Critério de Aceitação

### ✔ Checklist Institucional

| Critério | Status |
|---|---|
| Organization preenche o slot de Identity §2.1/§8/§10 | ✔ §1, §5 |
| `OrganizationRef` (Policy §5.2) fechado | ✔ §5.1 |
| Membership sem entidade nova | ✔ §6.2 |
| Restrição cross-org (Composition §14) fechada | ✔ §6.3 |
| Zero entidade/relação/estado/mecanismo de isolamento novo | ✔ §16 |
| UML, sequência, algoritmos, casos extremos, RFC2119 | ✔ §9-§14 |
| Nenhuma RFC necessária | ✔ §16 |

### ✔ Confirmação Explícita

Nenhum documento da base normativa foi alterado. Organization é um `Structural Component` cujo Coordinate coincide com a raiz de Namespace já reservada; Membership é uma projeção de `RoleAssignment` já formalizado por Agent Architecture; isolamento reutiliza integralmente Identity §10 e Registry §10; restrição cross-org combina Standard e Policy já existentes. **Quatro forward-references de quatro documentos distintos (Identity, Policy, Composition, e implicitamente Registry) fecham-se neste único documento, sem exigir nenhuma alteração retroativa.**
