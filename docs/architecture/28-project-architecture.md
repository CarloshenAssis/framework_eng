# Project Architecture
### Framework Eng — O Contêiner Institucional que Preenche o Último Slot de Namespace Reservado

*Versão 1.0.0 · Base normativa (congelada): Constitution · Kernel · Governance · Domain Model v1.1.0 · RFC-DM-001 · Identity & Namespace · Registry & Discovery · Validation & Certification · Composition Architecture · Workflow Architecture · Execution Architecture · Standards Architecture · Policy Architecture · Template Architecture · Skill Architecture · Observability Architecture · Organization & Tenancy Architecture · Packaging & Distribution Architecture · Compliance Architecture v1.1.0 · RFC-COMP-001 · Agent Architecture (23) · Testing Architecture (24) · Quality Gate Architecture (25) · Security Architecture (26) · Development Lifecycle Architecture (27)*

> **Tese central deste documento, provada seção a seção:** um `Project` é a especialização de **Structural Component** (mesma categoria de `Standard`, `Policy` e `Organization`) cuja `Identity` coincide com o **último segmento de Namespace ainda não preenchido** entre os quatro já reservados por Identity & Namespace §3.1 — `domain.<bounded-context>`. Organization Architecture (Documento 18) já preencheu `org.<id>`; este documento preenche `domain.<bounded-context>`, com o **mesmo raciocínio, palavra por palavra**. Um Project não executa nada, não certifica nada, não versiona nada por conta própria — ele é a fronteira de Namespace sob a qual Components, Workflows, Agents, Skills, Standards, Policies, Testing Assets, Security Assets, RFCs, Decision Records, Artifacts e Documentação **já produzidos por mecanismos existentes** são organizados, descobertos e agregados.

---

## 1. Posição Arquitetural

### 1.1 O slot que faltava

Identity & Namespace §3.1 reserva quatro segmentos de Namespace, na ordem: `core`, `org.<organization-id>`, `domain.<bounded-context>` *(opcional, dentro de um org ou de core)*, `env.<environment>` *(opcional)*. Três desses quatro já foram preenchidos por documentos anteriores:

| Segmento | Preenchido por | Como |
|---|---|---|
| `core` | Identity & Namespace, desde a origem | Raiz de escrita restrita ao Framework Council |
| `org.<id>` | **Organization & Tenancy Architecture** (Documento 18) | `Organization` = Structural Component cujo Coordinate **é** `org.<id>` |
| `env.<environment>` | Identity & Namespace + Organization §3.2 (referenciado, não expandido) | Partição de identidade para sandbox/produção |
| `domain.<bounded-context>` | **Este documento** | `Project` = Structural Component cujo Coordinate **é** `<parent>/domain.<id>` |

`Project` é, portanto, exatamente o que `Organization` já foi para `org.<id>`: o preenchimento, por reutilização estrita do mesmo padrão de design, do único segmento de Namespace que ainda não tinha um Component formal.

### 1.2 Relação hierárquica com Organization

```
core/                                     [raiz compartilhada — Framework Council]
 └── domain.<project-id>/                 [Project dentro de core — projeto do próprio núcleo do Framework]

org.<organization-id>/                    [Organization — Documento 18]
 └── domain.<project-id>/                 [Project dentro de uma Organization — caso mais comum]
      ├── skill.<nome>                     [Components filhos do Project]
      ├── agent.<papel>
      ├── workflow.<nome>
      └── standard.<área>.<nome>
```

Uma Organization **MAY** conter zero ou mais Projects; um Project **MUST** ter exatamente um segmento-pai (`core` ou uma `org.<id>` específica — nunca ambíguo, mesma regra de unicidade de Coordinate já normatizada). Nenhuma relação nova: `domain.<bounded-context>` já era, desde Identity §3.1, um segmento **filho** de `org` ou de `core` — este documento não altera essa hierarquia, apenas a preenche.

### 1.3 Posição na cadeia recursiva de nomeação (recapitulação)

```
Workflow (genérico) ⊂ Quality Gate (18 Gates) ⊂ Security (21 controles) ⊂ Development Lifecycle (19 fases)
                                                                                      │
                    todos os quatro operam SOBRE Components — mas nenhum deles
                    definia onde esses Components vivem organizacionalmente
                                                                                      ▼
                                                                          Project Architecture ◄── este documento
                                                          (a fronteira de Namespace + a organização de
                                                           tudo que os quatro documentos acima produzem)
```

### 1.4 Fronteiras negativas (invioláveis)

| Fronteira | Regra |
|---|---|
| Project não cria novo Runtime | Toda execução dentro de um Project **MUST** usar exatamente Execution Architecture §5/§7 (Dispatch/Plan/Recover/Rollback) — nenhum motor próprio |
| Project não cria novo Lifecycle | O `Project` (como Component) segue Kernel §3 sem exceção; os Components que ele organiza também |
| Project não cria novo Registry | Descoberta e resolução continuam sendo Registry & Discovery §5-§6, particionado por Namespace (Registry §10) — Project é apenas mais um nível dessa mesma partição |
| Project não cria novo mecanismo de Versionamento | SemVer (Kernel §2.11), Lineage (Identity §7) — sem alteração; o próprio Project, como Component, versiona-se do mesmo jeito |
| Project não substitui Organization | Organization é a fronteira de isolamento *físico*/tenant (Identity §10); Project é a fronteira de organização *lógica* de um corpo de trabalho dentro dessa fronteira — nunca a mesma coisa, nunca uma redefinindo a outra |

---

## 2. Objetivos

| # | Objetivo | Mecanismo |
|---|---|---|
| O1 | Preencher o slot `domain.<bounded-context>` reservado por Identity §3.1, com o mesmo padrão de design de Organization (Documento 18) | §1, §4 |
| O2 | Demonstrar Module, Feature, Epic, Milestone, Roadmap, RFC, Decision Record, Artifact, Documentação — todos como projeções organizacionais, nunca entidades novas | §6-§15 |
| O3 | Definir a estrutura oficial de diretórios do Framework Eng | §6 |
| O4 | Mapear Release para `Bundle` (Packaging & Distribution, Documento 20) sem redefini-lo | §9 |
| O5 | Provar que Project não introduz Runtime, Lifecycle, Registry, Versionamento, Composition, Execution, Policy, Standards ou Workflow novos | §26 |
| O6 | Dar ao Framework Eng uma estrutura oficial de organização de repositórios (**Objetivo Prático**) | §6, §28 |

---

## 3. Escopo

### 3.1 Pertence

Estrutura do Manifest de Project; a organização lógica de Module/Feature/Epic/Milestone/Roadmap; como RFCs, Decision Records, Artifacts e Documentação se agregam por Namespace de Project; a estrutura oficial de diretórios; o mapeamento de Release para Bundle.

### 3.2 Não pertence — com justificativa individual

| Excluído | Justificativa técnica |
|---|---|
| Ferramenta de gestão de projeto (Jira, Linear, GitHub Projects) | Este documento nomeia conceitos institucionais, nunca um produto — mesma fronteira já traçada por Testing §3.2 (nenhum framework de teste específico) |
| Metodologia (Scrum, Kanban) | Já explicitamente fora de escopo de Development Lifecycle Architecture §3.2 — Project herda a mesma exclusão |
| Billing, quotas, orçamento de projeto | `[LACUNA proposital]`, já deferida por Organization §3.2 (`Resource & Quota Architecture`, futura) — Project não a reabre |
| Novo mecanismo de isolamento físico | Já integralmente definido — Identity §10, Registry §10, Organization §1.2; Project apenas consome, um nível mais fundo |

---

## 4. Modelo Conceitual

### 4.1 Prova de minimalidade — tabela de proveniência

**Este documento introduz zero entidades, zero Value Objects, zero algoritmos com corpo lógico próprio, zero estado novo.**

| Conceito usado por Project | Natureza | Já definido em |
|---|---|---|
| `Component`, `Structural Component` | **Reutilizado** | Kernel §1-§2; Domain Model §3 |
| Manifest de 15 campos | **Reutilizado, sem campo novo** | Kernel §2 |
| Coordinate = segmento `domain.<bounded-context>` | **Reutilizado, mesmo token, mesmo padrão de Organization §1.2** | Identity §3.1; Organization §1.2 |
| `Owner`, `Steward` | **Reutilizado** | Kernel §2.3; Governance §3-§4 |
| `metadata` (categorização — base de Module) | **Reutilizado, uso semântico estendido** | Kernel §2.14 |
| `Metric` (base de status agregado de Feature/Epic) | **Reutilizado — mesma técnica de Testing §4.3 (Coverage)** | Domain Model §2 #14; RFC-DM-001 C4 |
| `Decision`/`Decision Record` (base de Milestone) | **Reutilizado** | Domain Model §14 |
| `Knowledge Asset` / `codifies` (base de Roadmap) | **Reutilizado** | RFC-DM-001 §3.1 (C1) |
| `Bundle` (base de Release) | **Reutilizado, sem alteração** | Packaging & Distribution §4.2 |
| RFC Process | **Reutilizado, sem alteração** | Governance §9 |
| `Artifact` genérico | **Reutilizado** | Domain Model §2 #7 |
| Isolamento e particionamento por Namespace | **Reutilizado, um nível mais fundo que Organization** | Identity §10; Registry §10 |
| Reserva permanente de nome (tombstone) | **Reutilizado** | Identity §3.2 |
| `resolve_assembly`/`EnumerateSlots` (fecho de dependências, base de Release) | **Reutilizado** | Composition §5; RFC-COMP-001 §4 |
| As dezenove fases do Development Lifecycle | **Reutilizado, sem redefinição — Project é o contêiner sob o qual elas ocorrem** | Development Lifecycle Architecture §6 |
| Catálogo de 18 Gates / 21 controles de segurança | **Reutilizado — Testing Assets/Security Assets são apenas os `test_suite[]`/bindings já dentro dos Components do Project** | Quality Gate §4.3; Security §4.5 |

**Nenhuma linha introduz entidade, relação ou estado novo.**

### 4.2 Estrutura formal

```
Project (Structural Component) {
  identity          : "<core|org.<id>>/domain." + <project-id>   [Identity §3.1 — MESMO padrão de Organization §1.2]
  version           : SemVer                                     [Kernel §2.11 — governa a própria política do Project]
  lifecycle_state   : KernelLifecycleState                        [Kernel §3 — sem alteração]
  owner             : Role                                         [Kernel §2.3 — Steward de Projeto — §6.1]

  capabilities      : [Capability]?                                (ex.: "project.hosts-regulated-workload" —
                                                                       mesma técnica de reuso já usada por
                                                                       Organization §4.2)
  constraints       : [Constraint]?                                 (ex.: limite de dependência cross-project)
  metadata          : Metadata                                      [Kernel §2.14 — nome legível, Module tags,
                                                                       vínculo a Organization-pai]
}
```

Nenhum campo além dos já definidos por Kernel §2 — **idêntico, campo a campo, à estrutura de `Organization`** (Organization §4.2), porque o mesmo teste que justificou Organization como Component (não Value Object) se aplica aqui sem alteração: Project é referenciado por múltiplos Components não relacionados (todo Component filho o referencia via prefixo de Namespace) e sua evolução (mudança de Owner, de política de risco) precisa de trilha própria — os dois critérios de Organization §1.1.

### 4.3 Por que Project não é um segundo Lifecycle nem um segundo Registry

Mesma prova que Development Lifecycle Architecture já fez para si mesma (Documento 27, §4.3), aplicada aqui: o **Project como Component** segue exatamente os sete estados de Kernel §3; os **Components dentro do Project** seguem, cada um, exatamente os mesmos sete estados, de forma independente. Não existe um "estado do projeto" agregado que seja um oitavo valor de enum — qualquer noção de "quão pronto está o Project" é uma **projeção computada** (§8, Feature/Epic status), nunca um campo persistido.

---

## 5. Estrutura do Manifest de Projeto

Idêntica à de Organization (Organization §5), com a mesma disciplina de "uso semântico, não estrutural" para os campos que carregam significado adicional:

| Campo do Component Contract (Kernel §2) | Uso por um Project |
|---|---|
| `identity` | `component_type = Project`; Coordinate = `<parent>/domain.<project-id>` |
| `owner` | Steward de Projeto — mesma autoridade de Governance §3-§4, escopada ao Namespace do Project |
| `capabilities` | Tags de classificação de risco/domínio (ex.: `project.regulated`), mesmo padrão de Organization §4.2 |
| `constraints` | Restrição de dependência cross-project, mesma técnica de Organization §6.3 (Standard + Policy) |
| `dependencies`/`providers` | Um Project **MAY** declarar `depends_on` outro Project (Kernel §2.6) quando seus Components compartilham Providers — reutilizado sem extensão |
| `metadata` | `module_registry` (ver §7) — lista de valores de tag `module` reconhecidos, puramente descritiva; `organization_ref` (o Organization-pai, quando aplicável) |
| Demais campos | Idênticos a Organization — §5 daquele documento |

`[ESCOLHA DE DESIGN]`

**Motivação:** decidir se `metadata.module_registry` deveria ser um campo estrutural novo (`modules: [ModuleDefinition]`).

**Alternativa rejeitada:** um Value Object `Module` com Identity, Lifecycle ou schema próprio.

**Justificativa técnica:** exatamente o mesmo raciocínio já usado por Agent §5.1 (`Capability` como elegibilidade de Role, em vez de um campo novo) — `metadata` (Kernel §2.14) já é o campo genérico para categorização sem exigir schema tipado. `module_registry` é uma lista de strings puramente descritiva (documentação de quais valores de tag são esperados), nunca uma entidade validada ou versionada por si própria.

---

## 6. Organização Lógica do Projeto — Estrutura Oficial de Diretórios

Este documento define, oficialmente, a seguinte estrutura de diretórios para qualquer Project construído sobre o Framework Eng:

```
/architecture   Os documentos institucionais ratificados que este Project herda/estende
                (mesmo padrão já usado por este próprio repositório em docs/architecture/)
/components     Manifests de Component (Kernel §6) — Standard, Policy, Skill, Agent, Workflow,
                Organization, Project — organizados por Namespace (Identity §8)
/skills         Projeção lógica de /components filtrada por component_type=Skill
/agents         Projeção lógica de /components filtrada por component_type=Agent
/templates      Components cujo propósito primário é hospedar templates[] (Template §4.2)
                reutilizáveis via extends/includes (Template §6.1-§6.2) por outros Components —
                Template em si nunca vive fora do Manifest que o declara (Template §1.1)
/workflows      Projeção lógica de /components filtrada por component_type=Workflow
/standards      Projeção lógica de /components filtrada por component_type=Standard
/policies       Projeção lógica de /components filtrada por component_type=Policy
/runtime        A implementação executável (Registry/Composition/Workflow/Execution/Template/
                Skill Runtime) — mesmo papel que runtime/ já cumpre neste próprio repositório
/testing        test_suite[] compartilhados entre Components, quando extraídos por conveniência —
                cada TestCase individual, no entanto, vive dentro do Manifest que certifica
                (Testing Architecture §5)
/security       Standards/Policies de domínio de segurança (Security Architecture §4.5) — mesma
                projeção lógica de /standards e /policies, filtrada por domínio de conteúdo
/records        Decision Records — Certification, RoleAssignment/Membership, Compliance,
                Knowledge (Domain Model §14) — nunca Manifests definicionais
/rfc            RFCs em andamento e resolvidos (Governance §9) cujo escopo afeta este Project
/docs           Documentação — ver §15
/examples       Conteúdo ilustrativo (mesmo papel que os "Reference Cycles" já cumprem
                neste repositório) — nunca Runtime real
/scripts        Automação operacional (fora da altitude conceitual do Framework — mesma
                fronteira já traçada por Development Lifecycle §3.2 para CI/CD)
/tools          Idem — ferramentas de suporte, fora de escopo normativo
```

**Regra central (PJ1, §24):** `/skills`, `/agents`, `/workflows`, `/standards`, `/policies`, `/security` **são projeções lógicas** — um mesmo Manifest físico **MAY** viver fisicamente sob `/components/<namespace>/` (convenção já usada por este próprio repositório, com `component_type` codificado no nome do arquivo: `skill.<nome>.yaml`, `standard.<área>.<nome>.yaml`) **ou** ser fisicamente replicado/simbolizado sob o diretório de tipo correspondente. Este documento **não** mandata uma única codificação física — mesma fronteira já traçada por Standards §3.2 e fechada, para o formato de serialização em si (não para o layout de diretórios), por Packaging & Distribution §5.

**Divergência conhecida, disclosed:** este próprio repositório (`framework_eng`) usa, desde os Reference Cycles, a convenção `components/<namespace>/<tipo>.<nome>.yaml` — sem os diretórios físicos separados `/skills`, `/agents`, etc. que este documento agora oficializa como estrutura recomendada para **novos** Projects. Reorganizar este repositório para a nova convenção física é trabalho futuro, explicitamente **não realizado por este documento** — mesma disciplina de disclosure já usada na deprecação dos Documentos 17/19 (ver `docs/CHECKPOINT.md` §8).

---

## 7. Estrutura de Módulos

`Module` **não é uma entidade** — é o valor de uma tag em `metadata.module` (Kernel §2.14), aplicada a qualquer Component dentro do Namespace de um Project, servindo puramente como dimensão de filtro/agrupamento para descoberta (Registry §6.2, `search` por `tags/Metadata`, já normatizado desde Kernel §5).

```
EnumerateModules(project_ref) ≡ { c.metadata.module | c ∈ Registry.list(namespace=project_ref.coordinate) }
                                  DISTINCT, excluindo null
```

Nenhum novo mecanismo de descoberta — `Registry.list(namespace, filter)` (Registry & Discovery §5) já suporta filtro por Metadata desde sua especificação original. Um Module **MAY**, opcionalmente, corresponder a um subdiretório físico sob `/components/<namespace>/<module>/` — convenção de organização física, não regra institucional.

---

## 8. Organização de Features (e Epics)

`[ESCOLHA DE DESIGN]`

**Motivação:** decidir como representar Feature e Epic — unidades de trabalho maiores que um Component individual, sem introduzir uma entidade de "unidade de trabalho" nova.

**Alternativas rejeitadas:** uma entidade `Feature`/`Epic` com Lifecycle próprio, tracking de progresso mutável.

**Justificativa técnica:** exatamente a mesma técnica já usada por Testing Architecture para `Coverage` (§4.3 daquele documento) — Feature e Epic são **tags de agrupamento** (`metadata.feature`/`metadata.epic`, Kernel §2.14) aplicadas a um ou mais Components, e seu "status de conclusão" é um **`Metric`** (Domain Model §2 #14) computado, nunca um campo mutável:

```
ComputeFeatureStatus(feature_tag) ≡ Metric{
  target: feature_tag (escopo lógico, não um Component único),
  value:  |{ c ∈ tagged(feature_tag) : c.lifecycle_state = Active }| / |tagged(feature_tag)|
}
```

`Epic` é a mesma técnica em granularidade maior — uma tag `metadata.epic` que tipicamente agrupa múltiplas `metadata.feature` distintas. **Nenhuma hierarquia nova é declarada estruturalmente** — a relação Epic⊃Feature é, ela própria, apenas uma convenção de nomenclatura de tags (ex.: `epic.billing.invoicing` / `feature.billing.invoicing.pdf-export`), resolvida por prefixo de string, nunca por uma relação tipada do Domain Model.

---

## 9. Organização de Releases

`Release` **é**, sem qualquer extensão, um `Bundle` (Packaging & Distribution Architecture §4.2) cujo `primary_subject` é o próprio `Project` (ou um Component-âncora dentro dele) e cujo fecho de dependências (`include_dependency_closure=true`) captura todos os Components do Project que compõem aquela versão distribuída:

```
CreateRelease(project_ref, version_tag) ≡
   ExportBundle(project_ref, include_closure=true, include_cert_evidence=true)   [Packaging & Distribution §9]
```

Nenhum novo mecanismo de empacotamento, versionamento ou integridade — `bundle_format_version`, `manifest_digest`, `verify_bundle`/`import_bundle` (Packaging & Distribution §4-§9) aplicam-se sem exceção. A única especialização é de **escopo**: um Release de Project é um Bundle cujo `subject` é o Coordinate do Project inteiro, em vez de um único Component isolado — Composition §5 (`resolve_assembly`) já resolve corretamente esse fecho maior, sem alteração de algoritmo.

---

## 10. Organização de Milestones

`Milestone` **é** uma `Decision` (Domain Model §14) — um compromisso formal, autorizado por um `Role` com autoridade declarada (o Owner/Steward do Project, Governance §8), que produz um `Decision Record` imutável:

```
Milestone ⊂ Decision {
  subtype        : MILESTONE_COMMITMENT
  project_ref    : VersionedIdentifier
  target_state   : Text                    (descrição do que constitui "alcançado" — ex.: "Epic X em Active")
  target_date    : Timestamp?
  authorized_by  : Role
}
```

Nenhuma estrutura além da já existente — mesmo padrão de família nomeada de Decision já usado por `CertificationGrant` (Validation & Certification §3) e generalizado por Organization Architecture para outros propósitos (§4.1 daquele documento: *"mesmo padrão... aplicado a nova família"*). Um Milestone **MUST** ser verificável objetivamente contra `target_state` (mesma exigência de Kernel §2.15, `validation`) — nunca uma aspiração vaga sem critério checável.

---

## 11. Organização de Roadmaps

`Roadmap` **é** um `Knowledge Asset` (RFC-DM-001 §3.1, C1 — especificamente um `Knowledge Base Entry`) que `codifies` (mesma relação já definida por C1) a sequência ordenada de `Milestone`s (§10) já declarados para um Project:

```
Roadmap (Knowledge Asset) --codifies--> { Milestone_1, Milestone_2, ... }   [RFC-DM-001 §3.1]
```

**Justificativa técnica:** um Roadmap não declara nenhum compromisso novo — ele **cura e ordena** compromissos (`Milestone`/`Decision`) que já existem, exatamente o papel que `codifies` já foi desenhado para cumprir (*"Knowledge Asset é a forma curada, governada, citável"* de entendimento/decisão já existente, RFC-DM-001 §3.1). Um Roadmap é, portanto, sempre uma **projeção documental** sobre Decision Records já registrados — nunca uma fonte independente de compromisso institucional. Isso resolve, sem mecanismo novo, a aparente tensão entre "Roadmap é sobre o futuro" e "Knowledge é descritiva do passado" (Domain Model §11): o Roadmap descreve compromissos **já tomados** (Milestones já autorizados), apenas ordenados para leitura prospectiva — nunca compromissos ainda não decididos.

---

## 12. Organização de RFCs

Nenhum mecanismo novo. Todo RFC cujo escopo afete um ou mais Components do Namespace de um Project segue integralmente Governance §9 (Draft → Discussão → Revisão → Decisão → Registro permanente). "Organizar RFCs por Project" é, tecnicamente, apenas a consulta:

```
ProjectRFCs(project_ref) ≡ { rfc ∈ Governance.RFCs : rfc.affected_components ∩ Registry.list(namespace=project_ref.coordinate) ≠ ∅ }
```

Fisicamente, `/rfc` (§6) armazena o texto desses RFCs — mesma convenção editorial já usada por este próprio repositório para `RFC-DM-001` e `RFC-COMP-001` (arquivos em `docs/architecture/`, citados por Coordinate lógico, nunca por um esquema de armazenamento novo).

---

## 13. Organização de Decision Records

Nenhum mecanismo novo. Todo `Decision Record` (Domain Model §14) referenciando um Component sob o Namespace de um Project é, por definição, um Decision Record "do Project" — mesma relação `references` (Domain Model §5) já tipada, apenas filtrada por prefixo de Namespace:

```
ProjectDecisionRecords(project_ref) ≡ { dr ∈ AllDecisionRecords : ∃ c ∈ dr.references : Namespace(c) ⊆ project_ref.coordinate }
```

Fisicamente, vivem em `/records` (§6) — mesma convenção já usada por `records/certification/`, `records/role-assignment/`, `records/compliance/` neste próprio repositório.

---

## 14. Organização de Artifacts

Nenhum mecanismo novo. `Artifact` (Domain Model §2 #7) é sempre produzido por uma `Execution` de um Component — "Artifacts do Project" é a mesma consulta de filtro por Namespace, aplicada a `produced_by_execution.performed_on` em vez de a `references`:

```
ProjectArtifacts(project_ref) ≡ { a ∈ AllArtifacts : Namespace(a.produced_by_execution.subject) ⊆ project_ref.coordinate }
```

Nenhum diretório físico dedicado é necessário além do que já existe para Evidence/Certification (`/records`) — Artifacts efêmeros (Assembly, Execution Plan, ExpandedTemplate) nunca são persistidos como arquivo, mesma disciplina já aplicada em todo o corpus (Composition §5, Execution §4, Template §11.3).

---

## 15. Organização de Documentação

`[ESCOLHA DE DESIGN]`

**Motivação:** decidir se Documentação (READMEs, guias, texto institucional) é um `Artifact` (Domain Model §2 #7) ou uma categoria à parte.

**Alternativa rejeitada:** modelar toda Documentação como `Artifact` de uma Execution.

**Justificativa técnica:** Domain Model §2 #7 define Artifact como *"resultado tangível e persistente produzido por uma Execution ou por uma Decision"* — texto institucional **hand-authored** (como os próprios vinte e oito documentos de arquitetura, ou um README de projeto) nunca foi produzido por uma Execution, exatamente como a própria Constitution não é Artifact de nenhuma Execution. Documentação hand-authored, portanto, **não é modelada como Artifact** — é conteúdo institucional textual puro, organizado por Namespace/diretório (`/docs`, `/architecture`), fora da cadeia de proveniência de Execução. Documentação **gerada** (ex.: docs de API produzidos automaticamente por uma Skill) **é** um `Artifact` comum, sem exceção — a mesma distinção Draft/Active de Kernel §3 não se aplica à prosa institucional em si.

Isso não introduz uma categoria nova do Domain Model — apenas reconhece, explicitamente, que nem todo conteúdo de um repositório precisa ser reduzido a uma das catorze entidades fundamentais (Domain Model §19.2 já previa isso: conceitos que não se encaixam não *precisam* de expansão do modelo se já são adequadamente descritos como *ausência* de proveniência de Execução, não como um conceito novo a ser modelado).

---

## 16. Fluxo Operacional

```
1.  Organization (opcional) já existe — org.acme                                        [Organization §7]
2.  CreateProject("billing", parent=org.acme) → Project Component em Draft→...→Active     [Governance §7, §9]
3.  Component filhos admitidos sob org.acme/domain.billing/... — Development Lifecycle    [Documento 27, fases 1-14]
    percorrido por Component, não pelo Project como um todo
4.  Tags de Module/Feature/Epic aplicadas via metadata durante Requirements/Architecture   [§7, §8]
5.  Milestones declarados como Decision, conforme necessário                              [§10]
6.  Roadmap publicado/atualizado como Knowledge Asset codificando Milestones vigentes      [§11]
7.  RFCs, quando necessários, seguem Governance §9 — filtrados por Namespace do Project    [§12]
8.  Ao atingir um conjunto coerente de Components Active: CreateRelease(project, "v1.2.0") [§9]
    → ExportBundle com fecho de dependências e Evidence de Certificação
9.  Monitoring/Maintenance/Evolution (Development Lifecycle, fases 15-17) ocorrem por
    Component, agregados por consulta ao Namespace do Project quando necessário
10. Eventualmente: Component individual entra em Deprecation/Archive (fases 18-19);
    o Project como Component só entra em Deprecation/Archive quando TODOS os seus
    Components filhos já o fizeram (mesma regra de Kernel §3 sobre Consumers ativos,
    aplicada recursivamente)
```

---

## 17. Algoritmos

**Nenhum algoritmo novo com lógica de decisão própria.**

```
ALGORITMO CreateProject(project_id, parent_namespace, manifest, requested_by):
  1  coordinate ← parent_namespace + "/domain." + project_id
  2  ASSERT project_id ∉ {core, org, system, registry, urn}          # Identity §8, mesma regra de Organization
  3  entry ← Registry.resolve(coordinate)
  4  SE entry ≠ NotFound ∧ entry.lifecycle_state ≠ Removed:
  5     RETORNA AdmissionError(NAMESPACE_ALREADY_CLAIMED)             # mesma regra de Organization §9
  6  decision ← Governance.Admit(coordinate, manifest, requested_by)   # Governance §7 — sem exceção
  7  Registry.register(manifest, decision.produces(DecisionRecord))    # Registry §5
  8  RETORNA decision.decision_record

ALGORITMO EnumerateModules(project_ref):
  RETORNA DISTINCT { c.metadata.module PARA c EM Registry.list(namespace=project_ref.coordinate) }
                    SE c.metadata.module ≠ null                       # §7 — leitura pura, Registry §5

ALGORITMO ComputeFeatureStatus(feature_tag, project_ref):
  membros ← { c PARA c EM Registry.list(namespace=project_ref.coordinate)
              SE c.metadata.feature = feature_tag }
  RETORNA Metric{ target: feature_tag,                                 # Domain Model §2 #14
                  value: |{ c EM membros : c.lifecycle_state = Active }| / |membros| }

ALGORITMO CreateRelease(project_ref, version_tag):
  RETORNA ExportBundle(project_ref, include_closure=true,               # Packaging & Distribution §9 — verbatim
                        include_cert_evidence=true)

ALGORITMO PublishRoadmap(project_ref, milestone_refs):
  ordenados ← SortBy(milestone_refs, m: m.target_date)
  RETORNA KnowledgeAsset.codifies(ordenados)                            # RFC-DM-001 §3.1 — verbatim
```

**Terminação/determinismo:** `CreateProject` reutiliza `Governance.Admit` (já terminante, Governance §7); `EnumerateModules`/`ComputeFeatureStatus` são leituras puras sobre conjuntos finitos já indexados (Registry §5); `CreateRelease` delega inteiramente a `ExportBundle`, já provado puro e determinístico (Packaging & Distribution PK6).

---

## 18. Diagramas UML

### 18.1 Project como Structural Component, coincidente com segmento de Namespace

```
┌─────────────────────────┐
│ «abstract» Component      │
└─────────────┬────────────┘
               △
┌─────────────┴────────────┐
│ Structural Component       │   [Domain Model §3 — mesma categoria de Standard, Policy, Organization]
└─────────────┬────────────┘
               △
       ┌───────┴───────┐
       │    Project     │   identity = "<core|org.<id>>/domain.<project-id>"
       └───────┬───────┘
                │ owner
                ▼
             Role  [Governance §3-§4 — Steward de Projeto]

     ┌──────────────────────────────────────────┐
     │  Namespace ".../domain.<project-id>/"       │  ◄── mesmo token, isolamento por
     │   ├── skill.<nome>                           │      Identity §10 / Registry §10,
     │   ├── agent.<papel>                            │     sem mecanismo adicional
     │   ├── workflow.<nome>                            │
     │   └── standard.<área>.<nome>                       │
     └──────────────────────────────────────────┘
```

### 18.2 Organização lógica — projeções, nunca entidades

```
Project
  │
  ├─ metadata.module=X ──────► "Module X"        (tag, §7)
  ├─ metadata.feature=Y ─────► "Feature Y" ──Metric──► status  (§8)
  ├─ metadata.epic=Z ────────► "Epic Z" (mesma técnica, granularidade maior)
  │
  ├─ Decision(subtype=MILESTONE_COMMITMENT) ──► "Milestone"      (§10)
  │        │ codifies (ordenado)
  │        ▼
  │   Knowledge Asset ──────────────────────► "Roadmap"          (§11)
  │
  ├─ Bundle(subject=project, closure=true) ──► "Release"          (§9)
  │
  └─ filtros de Namespace sobre:
       RFC (Governance §9), Decision Record (Domain Model §14),
       Artifact (Domain Model §2 #7)                              (§12-§14)
```

---

## 19. Diagramas de Sequência

### 19.1 Criação de Project e primeiro Release

```
Requester      Governance        Registry        Composition        Packaging
    │              │                │                 │                 │
    ├─CreateProject("billing", org.acme)──────────────►│                 │
    │              ├─Admit (Review→Approved→Active)     │                 │        [Governance §7]
    │              ├─Registry.register ─────────────────►│                 │
    │◄─DecisionRecord│                                    │                 │
    │                                                                       │
    │  [Components filhos admitidos ao longo do Development Lifecycle]     │
    │                                                                       │
    ├─CreateRelease(org.acme/domain.billing, "v1.0.0")───────────────────►│
    │              │                │  resolve_assembly (fecho)            │
    │              │                │◄───────────────────┤                 │
    │              │                │                     ├─ExportBundle──►│
    │◄─Bundle{v1.0.0}────────────────────────────────────────────────────┤
```

### 19.2 Consulta de status agregado (Feature)

```
Owner          ProjectQuerySvc      Registry
   │                  │                │
   ├─ComputeFeatureStatus("pdf-export", project_ref)─►│
   │                  ├─list(namespace, filter=metadata.feature)─►│
   │                  │◄─Components[]───────────────────┤
   │◄─Metric{value: 0.75}│
```

---

## 20. Estados

**Nenhum estado novo.** Prova exaustiva:

| Camada | Estados usados | Origem |
|---|---|---|
| Project (como Component) | `Draft, Review, Approved, Active, Deprecated, Archived, Removed` | Kernel §3 |
| Components filhos | Idem, cada um independentemente | Kernel §3 |
| Milestone (⊂ Decision) | `Proposed, Authorized, Recorded` | Domain Model §8, §14 |
| Release (= Bundle) | Nenhum — Bundle não tem Lifecycle (Packaging & Distribution §10.3) | Packaging & Distribution §10.3 |
| Feature/Epic/Module | Nenhum — são tags + projeções computadas, nunca persistem estado próprio | §7, §8 |

---

## 21. Casos Extremos

| # | Caso | Tratamento |
|---|---|---|
| PJ-E1 | `project_id` colide com token reservado ou tombstone existente | `AdmissionError` — mesma regra de Organization O1/O2 (§9 daquele documento), aplicada ao segmento `domain.*` |
| PJ-E2 | Project sem nenhuma Organization-pai (diretamente sob `core/`) | Válido — Identity §3.1 já permite `domain.<bounded-context>` "dentro de um org **ou de core**" |
| PJ-E3 | Dois Components de Projects distintos declaram o mesmo valor de `metadata.feature` | Sem conflito — a tag não é globalmente única (mesma disciplina de tags/Metadata, Kernel §2.14); `ComputeFeatureStatus` é sempre escopado a um `project_ref` |
| PJ-E4 | `ComputeFeatureStatus` chamado sobre uma tag sem nenhum Component ainda | Divisão por zero evitada por definição — `membros = ∅` retorna `Metric{value: undefined}`, tratado como "nenhum dado ainda", mesma disciplina de Observability B8/Packaging P8 (série/conjunto vazio é resultado válido) |
| PJ-E5 | Milestone com `target_date` já passada e `target_state` não alcançado | Não é erro estrutural — o Milestone permanece `Recorded` (imutável, Domain Model §14); a inconsistência é sinalizada por Governance §13 (Compliance), nunca corrigida retroativamente no próprio registro |
| PJ-E6 | Roadmap referencia um Milestone posteriormente revogado/superado | `codifies` aponta a uma versão específica do Decision Record (Domain Model §14, `supersedes`) — Roadmap **MUST** ser republicado (nova versão do Knowledge Asset) para refletir a superação; a versão antiga do Roadmap permanece válida como histórico |
| PJ-E7 | Release (Bundle) solicitado com Components filhos ainda em `Draft`/`Review` | `ExportBundle` já exige `lifecycle_state ∈ {Active, Deprecated}` (Packaging & Distribution §7, PRE) — Components não-Active são excluídos do fecho, nunca incluídos parcialmente prontos |
| PJ-E8 | Project decomissionado com Components filhos ainda `Active` | **MUST NOT** ser permitido — mesma regra de Kernel §3 sobre Consumers ativos, aplicada recursivamente (todo Component filho é, estruturalmente, um "Consumer" do Namespace do Project) |
| PJ-E9 | Dois Projects, mesma Organization-pai, dependência cross-project | Mesmo tratamento de dependência cross-organização (Organization §6.3) — Standard + Policy, `applies_at=COMPOSITION`, nenhum mecanismo novo, apenas escopado um nível mais fundo |

---

## 22. Performance

| Recurso | Regra de cache/complexidade | Origem |
|---|---|---|
| Resolução de `Project@version` | Cache indefinido — mesmo regime de qualquer Component | Registry §8 |
| `EnumerateModules`/`ComputeFeatureStatus` | O(Components sob o Namespace) — mesma ordem de `Registry.list`, já aceita | Registry §5, §10 |
| `CreateRelease` | Herda integralmente a complexidade de `ExportBundle` (O(V+E) sobre o fecho) | Packaging & Distribution §12 |
| Particionamento | Namespace do Project **é** mais um nível do particionamento já natural por primeiro segmento (Registry §10) — nenhum eixo de escala adicional | Registry §10 |

**Nenhuma política de cache nova.**

---

## 23. Eventos

**Nenhum evento novo.**

| Evento | Origem | Ocorre quando |
|---|---|---|
| `ComponentRegistered`/`VersionPublished` | Registry §11 | Criação do Project; admissão de Components filhos |
| `MilestoneRecorded` | Mesma classe de `CertificationGrant` (Governance §18, Decision Record) | Milestone (§10) autorizado |
| `BundleExported` | Packaging & Distribution §13 | `CreateRelease` (§9) |
| `KnowledgeAssetPublished` | Mesma classe já usada para Knowledge Asset (RFC-DM-001) | `PublishRoadmap` (§11) |
| `ComponentDeprecated`/`ComponentArchived` | Registry §11 | Deprecation/Archive do Project ou de um Component filho |

---

## 24. Regras Normativas (RFC 2119)

| # | Regra | Nível |
|---|---|---|
| PJ1 | `/skills`, `/agents`, `/workflows`, `/standards`, `/policies`, `/security` MUST ser tratados como projeções lógicas sobre `/components` — MUST NOT exigir uma única codificação física | MUST / MUST NOT |
| PJ2 | Project MUST ser um Structural Component cujo Coordinate coincide com um segmento `domain.<bounded-context>` já reservado por Identity §3.1 | MUST |
| PJ3 | Project MUST NOT introduzir campo de Manifest além dos já normatizados por Kernel §2 | MUST NOT |
| PJ4 | Module/Feature/Epic MUST ser representados como tags de `metadata` (Kernel §2.14) — MUST NOT ser entidades com Lifecycle próprio | MUST / MUST NOT |
| PJ5 | Milestone MUST ser modelado como `Decision` (família nomeada) — MUST NOT introduzir um mecanismo de compromisso paralelo | MUST / MUST NOT |
| PJ6 | Roadmap MUST `codifies` apenas Milestones já registrados como Decision Record — MUST NOT declarar compromisso institucional por si próprio | MUST / MUST NOT |
| PJ7 | Release MUST ser um `Bundle` (Packaging & Distribution §4.2) — MUST NOT introduzir mecanismo de empacotamento paralelo | MUST / MUST NOT |
| PJ8 | Documentação hand-authored MUST NOT ser modelada como `Artifact` — apenas Documentação gerada por Execution MUST sê-lo | MUST NOT / MUST |
| PJ9 | Decomissionamento de um Project MUST NOT ocorrer enquanto existir Component filho `Active` | MUST NOT |
| PJ10 | Este documento MUST NOT introduzir novo Runtime, Registry, Lifecycle, Versionamento, Composition, Execution, Policy, Standards ou Workflow | MUST NOT |
| PJ11 | Dependência cross-project MUST seguir exatamente o mecanismo já fechado por Organization §6.3 (Standard + Policy), escopado um nível mais fundo | MUST |

---

## 25. Integrações

| Documento | Como Project o consome — sem alteração |
|---|---|
| **Constitution** | Regra Imutável nº10 (não duplicar) fundamenta a decisão de reutilizar Organization §1.1 integralmente |
| **Kernel** | Component pleno; §2.6 (`dependencies`) usado para Project→Project |
| **Governance** | §7 (Admission), §9 (RFC), §13 (Compliance) — reutilizados sem exceção |
| **Domain Model v1.1.0** | `Decision`/`Decision Record` (Milestone), `Metric` (Feature/Epic status), `Artifact` (Documentação gerada) |
| **RFC-DM-001** | `Knowledge Asset`/`codifies` (C1) é o mecanismo inteiro de Roadmap |
| **Identity & Namespace** | Preenche exatamente o quarto e último slot reservado (§3.1) |
| **Registry & Discovery** | `list`/`search`/`register` reutilizados sem extensão; particionamento (§10) ganha mais um nível |
| **Validation & Certification** | Certificação de Components filhos é herdada como Evidence advisória em Releases (via Packaging §6.2) |
| **Composition** | `resolve_assembly` usado pelo fecho de dependências de Release |
| **Workflow** | Development Lifecycle (que Project contém) já é instância de Workflow — nenhuma extensão |
| **Execution** | Nenhuma alteração — toda Execution dentro de um Project é uma Execution comum |
| **Standards / Policy** | Restrição cross-project (§21, PJ-E9) reutiliza exatamente Organization §6.3 |
| **Template Architecture** | `/templates` (§6) hospeda Components cujo propósito primário é servir Templates reutilizáveis |
| **Skill / Agent Architecture (23)** | `/skills`/`/agents` são projeções lógicas sobre os mesmos Components já definidos por esses documentos |
| **Observability Architecture** | `trace`/`provenance`/`query_events` já operam por Namespace — Project não exige extensão |
| **Organization & Tenancy** | Precedente direto e integral — §1.2, §4.2, §5 deste documento espelham Organization §1.2, §4.2, §5 |
| **Packaging & Distribution** | `Bundle` é, literalmente, `Release` (§9) |
| **Compliance Architecture** | Maintenance (Development Lifecycle, fase 16) aplicada por Component, agregável por Namespace de Project |
| **RFC-COMP-001** | `EnumerateSlots` consumido indiretamente via Composition |
| **Agent Architecture (23)** | Implementation de Components do Project pode ser realizada por Agent |
| **Testing Architecture (24)** | `/testing` é projeção sobre `test_suite[]` já dentro de cada Manifest |
| **Quality Gate Architecture (25)** | Cada Component do Project percorre o mesmo catálogo de 18 Gates, sem exceção |
| **Security Architecture (26)** | `/security` é projeção sobre os mesmos Standards/Policies de domínio de segurança já catalogados |
| **Development Lifecycle Architecture (27)** | Project é o contêiner de Namespace sob o qual as dezenove fases ocorrem, por Component — nenhuma fase nova, nenhuma redefinição |

---

## 26. Validação Institucional

| Documento base | Resultado |
|---|---|
| Constitution | **PASS** — Regra Imutável nº10 fundamenta reuso integral de Organization |
| Kernel | **PASS** — Component pleno, zero campo novo |
| Governance | **PASS** — Admission/RFC/Compliance reutilizados sem exceção |
| Domain Model v1.1.0 | **PASS** — zero entidades/relações/estados |
| RFC-DM-001 | **PASS** — `Knowledge Asset`/`codifies` reutilizado para Roadmap |
| Identity & Namespace | **PASS** — preenche exatamente o slot `domain.<bounded-context>` já reservado |
| Registry & Discovery | **PASS** — `list`/`search`/`register` sem extensão |
| Validation & Certification | **PASS** — Certificação herdada como Evidence em Release, sem redefinição |
| Composition | **PASS** — `resolve_assembly` reutilizado |
| Workflow | **PASS** — Development Lifecycle (que Project contém) já é Workflow |
| Execution | **PASS** — sem alteração |
| Standards / Policy | **PASS** — restrição cross-project reutiliza Organization §6.3 |
| Template Architecture | **PASS** — `/templates` como projeção, sem alteração |
| Skill / Agent Architecture (23) | **PASS** — `/skills`/`/agents` como projeções |
| Observability Architecture | **PASS** — sem extensão |
| Organization & Tenancy | **PASS** — precedente direto, espelhado sem contradição |
| Packaging & Distribution | **PASS** — `Bundle` = `Release`, sem redefinição |
| Compliance Architecture | **PASS** — agregação por Namespace, sem novo mecanismo |
| RFC-COMP-001 | **PASS** — `EnumerateSlots` consumido sem reabertura |
| Testing Architecture (24) | **PASS** — `/testing` como projeção |
| Quality Gate Architecture (25) | **PASS** — catálogo reutilizado por Component |
| Security Architecture (26) | **PASS** — `/security` como projeção |
| Development Lifecycle Architecture (27) | **PASS** — Project é o contêiner, não uma redefinição das dezenove fases |
| **Exige RFC?** | **NÃO** |

**Prova formal de que Project não adiciona:**

| Item vedado pelo mandato | Verificação |
|---|---|
| Novo Runtime | Nenhum — Dispatch/Plan/Recover/Rollback reutilizados (§16, §17) |
| Novo Lifecycle | Nenhum — Kernel §3, sem exceção (§4.3, §20) |
| Novo Registry | Nenhum — Registry & Discovery §5-§6, particionamento estendido em um nível (§4.1, §22) |
| Novo mecanismo de Versionamento | Nenhum — SemVer/Lineage reutilizados (§4.1) |
| Novo mecanismo de Composition/Execution/Policy/Standards/Workflow | Nenhum — §25, §26 |

---

## 27. Dependências Futuras

| Consumidor | O que consome | Estado |
|---|---|---|
| **Resource & Quota Architecture** (futuro, já deferida por Organization §17) | Coordinate de Project como segunda unidade de medição de consumo, abaixo de Organization | `[LACUNA proposital]`, explicitamente deferida |
| **Multi-Agent Architecture** (futuro) | Múltiplos Agents coordenados dentro do Namespace de um Project | Sem bloqueio |
| **Marketplace** (futuro) | `Release` (Bundle de Project) como unidade de listagem/distribuição entre organizações | Sem bloqueio |
| **CI/CD** (futuro, operacional) | Estrutura oficial de diretórios (§6) como convenção de entrada para pipelines automatizados | Desbloqueado — Objetivo Prático |

---

## 28. Critério de Aceitação

### ✔ Checklist Institucional

| Critério do mandato | Status |
|---|---|
| Project preenche o slot `domain.<bounded-context>` (Identity §3.1) | ✔ §1, §4 |
| Module, Feature, Epic, Milestone, Roadmap, RFC, Decision Record, Artifact, Documentação — projeções, nunca entidades | ✔ §7-§15 |
| Component, Workflow, Agent, Skill, Standards, Policies, Testing Assets, Security Assets organizados sem mecanismo novo | ✔ §6, §25 |
| Estrutura oficial de diretórios definida, com todos os dezessete solicitados | ✔ §6 |
| Zero Runtime/Lifecycle/Registry/Versionamento/Composition/Execution/Policy/Standards/Workflow novo | ✔ §26 |
| UML, sequência, algoritmos, casos extremos, RFC2119, performance, eventos | ✔ §17-§24 |
| Tabela de proveniência completa | ✔ §4.1 |
| Integração documento a documento (vinte e sete anteriores) | ✔ §25 |
| Nenhuma alteração a documento anterior — RFC separada se necessário | ✔ §26 — nenhuma mudança encontrada; nenhuma RFC necessária |

### ✔ Objetivo Prático Realizado

O Framework Eng possui, a partir deste documento, uma estrutura oficial de organização de repositórios — dezessete diretórios nomeados, cada um mapeado explicitamente a um mecanismo institucional já ratificado, prontos para orientar tanto ferramentas de CI/CD quanto Agentes de IA que precisem localizar onde um tipo de conteúdo institucional vive dentro de um Project real.

### ✔ Confirmação Explícita

**Nenhum dos vinte e sete documentos anteriores foi alterado.** `Project` espelha `Organization` (Documento 18) campo a campo, decisão a decisão — o mesmo teste que justificou Organization como Component justifica Project; a mesma disciplina de "projeção computada, nunca entidade nova" que Testing já usou para Coverage é reaplicada a Feature/Epic; a mesma família nomeada de Decision já usada por Certification é reaplicada a Milestone; `Bundle` já existente torna-se `Release` sem nenhuma extensão. **O último segmento de Namespace reservado por Identity & Namespace §3.1 está, agora, preenchido — fechando um compromisso aberto desde o sexto documento desta série.**

---

*Fim do documento. Versão 1.0.0.*
