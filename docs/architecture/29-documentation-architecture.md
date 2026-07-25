# Documentation Architecture
### Framework Eng — A Organização Institucional de Tudo o que é Prosa

*Versão 1.0.0 · Base normativa (congelada): Constitution · Kernel · Governance · Domain Model v1.1.0 · RFC-DM-001 · Identity & Namespace · Registry & Discovery · Validation & Certification · Composition Architecture · Workflow Architecture · Execution Architecture · Standards Architecture · Policy Architecture · Template Architecture · Skill Architecture · Observability Architecture · Organization & Tenancy Architecture · Packaging & Distribution Architecture · Compliance Architecture v1.1.0 · RFC-COMP-001 · Agent Architecture (23) · Testing Architecture (24) · Quality Gate Architecture (25) · Security Architecture (26) · Development Lifecycle Architecture (27) · Project Architecture (28)*

> **Tese central deste documento, provada seção a seção:** documentação não é uma categoria institucional nova — é a organização de conteúdo que já se divide, sem exceção, em três classes já existentes: (a) conteúdo que já vive **dentro** do Manifest de um Component (Standards, Policies, Specifications de Contract — nunca um documento à parte); (b) conteúdo **gerado** por uma Execution (Artifact, Domain Model §2 #7 — API docs derivadas, relatórios); (c) prosa **hand-authored**, livre de Execution, organizada por diretório de Project (Project Architecture §6, §15 — exatamente a mesma categoria que os vinte e oito documentos de arquitetura já ratificados, incluindo este, sempre ocuparam). Este documento não cria uma quarta classe. Ele nomeia dezessete tipos documentais pedidos, prova que cada um cai em uma das três classes acima, e formaliza o fluxo (criação→revisão→aprovação→publicação→atualização→depreciação→arquivamento) reutilizando, sem exceção, Governance, Workflow, Registry e Development Lifecycle já ratificados.

---

## 1. Posição Arquitetural

### 1.1 Documentação não é um quarto tipo de entidade — é uma classificação sobre as três já existentes

```
                    ┌─────────────────────────────────────────┐
                    │         "Documento" (uso comum)            │
                    └──────────────────┬──────────────────────┘
                                        │ classifica-se sempre em uma de três classes já existentes
           ┌────────────────────────────┼────────────────────────────┐
           ▼                            ▼                             ▼
┌─────────────────────┐   ┌─────────────────────────┐   ┌──────────────────────────┐
│ (a) Campo de Manifest │   │ (b) Artifact              │   │ (c) Prosa hand-authored    │
│  de um Component        │   │  (Domain Model §2 #7)     │   │  (Project Architecture     │
│  já existente            │   │  produzido por Execution  │   │   §15 — NÃO é Artifact)     │
│  (Standards §4.3,        │   │                            │   │                            │
│   Policy §5, Kernel §2)  │   │                            │   │                            │
└─────────────────────┘   └─────────────────────────┘   └──────────────────────────┘
```

**Nenhuma quarta classe é introduzida.** Este documento nomeia, cataloga e organiza — nunca cria mecanismo.

### 1.2 Posição na cadeia recursiva de nomeação (recapitulação)

```
Workflow ⊂ Quality Gate ⊂ Security ⊂ Development Lifecycle ⊂ Project
                                                                  │
                          Project já resolveu §15 (Documentação hand-authored
                          ≠ Artifact) e §6 (/docs, /architecture como diretórios)
                                                                  ▼
                                                      Documentation Architecture ◄── este documento
                                       (aprofunda §15/§6 de Project em dezessete tipos nomeados
                                        e um fluxo documental completo, sem reabrir nenhum dos dois)
```

### 1.3 Fronteiras negativas (invioláveis)

| Fronteira | Regra |
|---|---|
| Documentation não cria novo Registry | Apenas Components (Registry & Discovery §3.1) são indexados pelo Registry; documentação hand-authored **MUST NOT** ser indexada por um segundo mecanismo de descoberta |
| Documentation não cria novo Versionamento | Quando um documento precisa de versão, reutiliza SemVer (Kernel §2.11) exatamente como qualquer Component — nunca um esquema de versão de documento à parte |
| Documentation não cria novo Workflow | O fluxo documental (§8) é uma instância nomeada de `Phase`/`Step` (Workflow §4) — mesma disciplina já usada por Quality Gate, Security e Development Lifecycle |
| Documentation não cria novo Lifecycle | Documentos que precisam de estado seguem exatamente Kernel §3 (quando anexados a um Component) ou o padrão já **exercido**, não inventado, de emenda/depreciação de documento de arquitetura (§12) |
| Documentation reutiliza integralmente Project Architecture | `/docs`, `/architecture` (Project §6) permanecem os únicos diretórios físicos relevantes — nenhum diretório novo é proposto aqui |

---

## 2. Objetivos

| # | Objetivo | Mecanismo |
|---|---|---|
| O1 | Classificar os dezessete tipos documentais pedidos em uma das três classes de §1.1 | §5 |
| O2 | Justificar por que "ADR" não é introduzido como convenção distinta | §5.1 |
| O3 | Formalizar o fluxo documental de sete passos, reutilizando Governance/Workflow/Registry/Development Lifecycle | §8 |
| O4 | Definir as dez relações pedidas (Project, Registry, Decision Record, RFC, Standards, Policies, Runtime, Testing, Security, Development Lifecycle) | §17 |
| O5 | Provar que Documentation não introduz Registry, Versionamento, Workflow ou Lifecycle novos | §18 |
| O6 | Dar ao Framework Eng um modelo oficial de documentação para qualquer Project (**Objetivo Prático**) | §20 |

---

## 3. Escopo

### 3.1 Pertence

Classificação dos dezessete tipos documentais; a relação de cada um com Manifest/Artifact/prosa; o fluxo documental de sete passos; as dez relações pedidas; o estado análogo (não idêntico) de um documento de arquitetura, já exercido três vezes neste próprio repositório.

### 3.2 Não pertence — com justificativa individual

| Excluído | Justificativa técnica |
|---|---|
| Ferramenta de geração de documentação (Sphinx, MkDocs, Docusaurus) | Mesma fronteira já traçada por Testing §3.2 e Development Lifecycle §3.2 — nenhuma tecnologia específica é mandatada |
| Detecção mecânica de *drift* de prosa (documentação desatualizada em relação ao Runtime) | `[LACUNA proposital]`, disclosed em §13, CE-D9 — Standards/Policy só avaliam Components com Contract declarado (Standards §4.5); prosa hand-authored não tem `ComplianceTarget` possível sem inventar um mecanismo de Standards novo, expressamente proibido pelo mandato |
| Formato de marcação (Markdown vs. outro) | Detalhe de implementação abaixo da altitude conceitual de toda a série — mesma abstenção já praticada por Identity §4.4 quanto a encoding físico |
| Tradução/internacionalização de documentação | Fora do domínio técnico do Framework — nenhum documento anterior tratou disso |

---

## 4. Modelo Conceitual

### 4.1 Prova de minimalidade — tabela de proveniência

**Este documento introduz zero entidades, zero Value Objects, zero algoritmos com corpo lógico próprio, zero estado novo.**

| Conceito usado por Documentation | Natureza | Já definido em |
|---|---|---|
| `Manifest` (`purpose`, `statement`/`rationale`) | **Reutilizado** — é a documentação de um Component | Kernel §2.2; Standards §4.3 |
| `Artifact` genérico (documentação gerada) | **Reutilizado** | Domain Model §2 #7 |
| Prosa hand-authored ≠ Artifact | **Reutilizado, decisão já tomada** | Project Architecture §15 |
| `/docs`, `/architecture` (diretórios) | **Reutilizado, sem diretório novo** | Project Architecture §6 |
| RFC Process (cinco etapas) | **Reutilizado** | Governance §9 |
| Admission Process (Review/Approval) | **Reutilizado** | Governance §7 |
| `Decision`, `Decision Record` | **Reutilizado** | Domain Model §14 |
| `Knowledge Asset` / `codifies` (base de CHANGELOG, ROADMAP, RELEASE NOTES) | **Reutilizado** | RFC-DM-001 §3.1 (C1) |
| `Bundle` (base de RELEASE NOTES) | **Reutilizado** | Packaging & Distribution §4.2; Project §9 |
| `ClassifyStandardChange`/`ClassifyTemplateChange`/`ClassifySkillChange`/`ClassifyAgentChange` | **Reutilizado — base de CHANGELOG** | Standards §12.2; Template §11.4; Skill §9.1; Agent §9.1 |
| Lineage (Identity §7) | **Reutilizado — base de CHANGELOG** | Identity & Namespace §7 |
| Breaking Change Process (base de MIGRATION GUIDE) | **Reutilizado** | Governance §10 |
| Milestone (⊂ Decision) | **Reutilizado — base de ROADMAP** | Project Architecture §10 |
| `Phase`/`Step` (base do fluxo documental) | **Reutilizado** | Workflow §4 |
| As dezenove fases do Development Lifecycle | **Reutilizado, sem redefinição** | Development Lifecycle Architecture §6 |
| Reserva permanente de nome / não-edição retroativa | **Reutilizado — base de Arquivamento** | Identity §3.2; Governance §18 |
| `[ESCOLHA DE DESIGN]` (convenção narrativa já usada em 28 documentos) | **Reutilizado — metade da função de "ADR"** | Convenção editorial já estabelecida por esta própria série |

**Nenhuma linha introduz entidade, relação ou estado novo.**

### 4.2 Por que este documento não é, ele próprio, uma exceção à sua própria tese

Este documento — como os vinte e oito anteriores — é prosa hand-authored, vivendo em `/architecture` (Project §6), classificado como "Architecture Document" (§5). Ele não escapa da própria taxonomia que define; é uma instância dela, exatamente como Kernel §0 já observa sobre si mesmo em relação ao Component Contract que define (*"o Kernel não cria nada... torna possível"*).

---

## 5. Classificação dos Documentos

Cada um dos dezessete tipos pedidos, classificado por: (a) pertence a um Component já existente, ou é livre-standing; (b) é gerado (Artifact) ou hand-authored; (c) exige aprovação formal de Governance; (d) mecanismo que já o realiza integralmente.

| # | Tipo | (a) Vínculo | (b) Natureza | (c) Aprovação formal | (d) Mecanismo já existente |
|---|---|---|---|---|---|
| 1 | **Constitution** | Livre-standing (acima do Kernel) | Hand-authored | Sim — Framework Council, unanimidade/supermaioria (Governance §8) | Constitution §9 (processo de emenda próprio) |
| 2 | **Architecture Documents** | Livre-standing | Hand-authored | Sim — Framework Council ou RFC (Governance §8-§9) | Padrão já **exercido** três vezes nesta série: RFC-DM-001, Compliance v1.1.0, depreciação dos Documentos 17/19 |
| 3 | **RFC** | Livre-standing até ratificação | Hand-authored | Sim — Governance §9, processo completo | Governance §9 |
| 4 | **Decision Record** | **Não é documentação — é entidade** (Domain Model §14) | N/A | Herdada da própria Decision | Domain Model §14; Governance §18 |
| 5 | **ADR** | **Não introduzido como convenção distinta** — ver §5.1 | — | — | `Decision Record` (evento) + `[ESCOLHA DE DESIGN]` (narrativa) |
| 6 | **Standards** | Component-attached (dentro do Manifest) | Hand-authored, campo `statement`/`rationale` | Aprovação do Standard como Component (Governance §7) | Standards §4.3 |
| 7 | **Policies** | Component-attached | Hand-authored, campo análogo | Idem Standards | Policy §5 |
| 8 | **Specifications** | Component-attached (Contract) ou livre-standing (pré-Component) | Hand-authored | Quando vira Contract, Admission normal | Kernel §2; Development Lifecycle fase 2 (Requirements) |
| 9 | **Runtime Documentation** | Livre-standing | Hand-authored (ex.: `RUNTIME.md`, já existente neste repositório) | Não formalmente | Project §6 (`/runtime`, `/docs`) |
| 10 | **API Documentation** | Livre-standing ou gerado | Ambos — gerado quando derivado de `inputs`/`outputs`; hand-authored quando narrativo | Não formalmente | Kernel §2.4-§2.5; Project §15 |
| 11 | **Project Documentation** | Livre-standing | Hand-authored | Não formalmente | Project §6, §15 |
| 12 | **User Documentation** | Livre-standing | Hand-authored (ou gerado) | Não formalmente | Project §6 |
| 13 | **CHANGELOG** | Livre-standing, **projeção** sobre dados já existentes | Knowledge Asset que `codifies` Decision Records de versão + resultado de `ClassifyXChange` | Não — é projeção | RFC-DM-001 C1; Identity §7 (Lineage) |
| 14 | **ROADMAP** | Livre-standing, **projeção** | Knowledge Asset que `codifies` Milestones | Já definido | Project Architecture §11 |
| 15 | **CHECKPOINT** | Livre-standing | Hand-authored, republicado periodicamente | Não formalmente | Project Documentation, instância recorrente (§6.3) |
| 16 | **RELEASE NOTES** | Livre-standing, **projeção** sobre um Release | Knowledge Asset que `codifies` o Bundle + Decision Records/Milestones associados | Não — é projeção | Project §9 (Release = Bundle) |
| 17 | **MIGRATION GUIDE** | Livre-standing, obrigatório sob Breaking Change | Hand-authored | Sim — parte do próprio processo de Breaking Change | Governance §10 |
| 18 | **README** | Livre-standing | Hand-authored | Não formalmente | Project §6 |

### 5.1 Por que "ADR" não é introduzido como convenção distinta

`[ESCOLHA DE DESIGN]`

**Motivação:** o mandato exige justificar explicitamente a ausência de ADR (Architecture Decision Record, formato Nygard: Title/Status/Context/Decision/Consequences) como convenção própria.

**Alternativa rejeitada:** introduzir um tipo de documento `ADR` — um arquivo por decisão arquitetural, com seu próprio ciclo de vida e numeração.

**Justificativa técnica:** a função de um ADR já é cumprida, integralmente, pela **combinação** de dois mecanismos já existentes e usados de forma consistente em todos os vinte e oito documentos anteriores:

1. **O evento institucional** (o quê foi decidido, por quem, quando, com que autoridade) — já é, palavra por palavra, a definição de `Decision`/`Decision Record` (Domain Model §14; Governance §18: *"contexto, alternativas consideradas, decisão tomada, autoridade responsável, data"* — a definição de Decision Record já é, literalmente, a definição de um ADR).
2. **A narrativa de justificativa** (por que essa alternativa e não outra) — já é, palavra por palavra, o papel do bloco `[ESCOLHA DE DESIGN]` (**Motivação** ~ Context; **Alternativas rejeitadas** ~ Consequences consideradas; **Justificativa técnica** ~ Decision rationale; **Precedentes arquitetônicos** — sem equivalente direto em ADR tradicional, um extra já praticado aqui) — usado consistentemente desde o Documento 6 (Identity & Namespace) até este.

Introduzir "ADR" como terceiro mecanismo reproduziria exatamente a classe de erro que a **Regra Imutável nº10 da Constitution** proíbe (*"nenhum componente novo é aceito sem antes se verificar que algo equivalente já não existe"*) — dois lugares (Decision Record + `[ESCOLHA DE DESIGN]`) já respondem, juntos e sem lacuna, a toda pergunta que um ADR responderia sozinho.

**Precedente arquitetônico:** a mesma disciplina de "não duplicar o que já existe" já rejeitou, explicitamente, introduzir `AutonomyLevel` (Agent, doc 17 — hoje deprecated) por já existir a escada L0-L4, e rejeitou introduzir `TestResult` por já existir `Evidence`.

---

## 6. Estrutura Oficial da Documentação

Reutiliza integralmente a estrutura de diretórios já oficializada por Project Architecture §6 — nenhum diretório novo:

| Tipo documental | Diretório (Project §6) |
|---|---|
| Constitution, Architecture Documents, RFC (após ratificação) | `/architecture` |
| RFC (durante discussão), Decision Record (registro textual, não o evento em si) | `/rfc`, `/records` |
| Standards, Policies (Manifest completo) | `/standards`, `/policies` (projeções de `/components`) |
| Specifications (pré-Component) | `/docs` |
| Runtime Documentation | `/runtime` (código) + `/docs` (narrativa, ex.: `RUNTIME.md`) |
| API Documentation | `/docs` (hand-authored) ou Artifact gerado, sem diretório fixo (produto de Execution) |
| Project Documentation, User Documentation, CHECKPOINT, README | `/docs` |
| CHANGELOG, ROADMAP, RELEASE NOTES | `/docs` (Knowledge Assets publicados como texto) |
| MIGRATION GUIDE | `/docs`, referenciado pelo Decision Record do Breaking Change correspondente |

### 6.1 Regra de organização física (DOC1, §16)

Nenhum destes é um diretório novo — todos já existiam em Project Architecture §6. Este documento apenas atribui, a cada um dos dezessete tipos, um diretório já oficializado.

### 6.2 README como entrada

`README.md` na raiz de `/` (implícito em Project §6, não listado separadamente porque é a própria porta de entrada) é a instância "raiz" de Project Documentation — mesmo papel que já cumpre, hoje, neste próprio repositório (`README.md`, `components/README.md`, `records/README.md`).

### 6.3 CHECKPOINT como instância recorrente de Project Documentation

`CHECKPOINT` não introduz mecanismo de republicação — é Project Documentation comum (§5, linha 15), republicada por convenção sempre que o estado agregado do Project muda de forma que a versão anterior deixe de refletir a realidade. Mesmo papel já cumprido, concretamente, por `docs/CHECKPOINT.md` neste próprio repositório ao longo de toda esta sessão.

---

## 7. Organização dos Registros

`/records` (Project §6) organiza exclusivamente **eventos institucionais já registrados** (Decision Record, Domain Model §14) — nunca prosa livre. A relação com Documentation é estritamente de **referência, nunca de duplicação**:

```
CHANGELOG (Knowledge Asset, /docs) ──narra, sem duplicar──► Decision Record (/records)
RELEASE NOTES (Knowledge Asset, /docs) ──narra, sem duplicar──► Decision Record + Milestone (/records)
MIGRATION GUIDE (/docs) ──referencia──► Decision Record do Breaking Change (/records)
```

**Regra (DOC7, §16):** nenhuma prosa em `/docs` **MUST** duplicar o conteúdo de um Decision Record em `/records` — apenas referenciá-lo por seu identificador (Identity §4.2, ULID). Um Decision Record é a fonte de verdade institucional (Domain Model §14, imutável); a prosa em `/docs` é uma narrativa de leitura humana **sobre** ele, nunca uma segunda cópia que possa divergir.

---

## 8. Fluxo Documental

Sete passos pedidos, cada um mapeado a uma fase já existente do Development Lifecycle (Documento 27) ou a um processo já existente de Governance — nenhuma fase nova.

| Passo | Realização institucional | Reutiliza |
|---|---|---|
| 1. Criação | Prosa rascunhada — para Architecture Documents, equivalente a Ideation/Requirements (Development Lifecycle fases 1-2); para os demais, ato de autoria livre sob `/docs` | Development Lifecycle §6 (fases 1-2) |
| 2. Revisão | `Step(GATE_APPROVAL, role_class=Reviewer)` — mesma Review de Governance §7 passos 3-4; para Architecture Documents, discussão aberta de RFC (Governance §9, etapa 2) | Development Lifecycle fase 12 (Review); Governance §7, §9 |
| 3. Aprovação | Decisão da autoridade correspondente à camada (Governance §8 — Framework Council para Kernel/Constitution; Domain Steward para os demais) | Governance §8; Development Lifecycle fase 12-13 |
| 4. Publicação | Commit à `/architecture`/`/docs` do Project (mesma prática já exercida, sessão inteira, neste repositório: escrever → commit → push → merge); quando o documento é campo de um Component, `register()`/`publish_version()` | Development Lifecycle fase 14; Registry & Discovery §5 |
| 5. Atualização | MINOR (aditiva, ex.: Compliance v1.1.0) ou nova ratificação (MAJOR, ex.: uma nova era constitucional, Constitution §9) — nunca edição silenciosa | Development Lifecycle fase 17 (Evolution); Constitution §9 |
| 6. Depreciação | Notice explícito + redirect ao sucessor, texto original preservado — **mesmo padrão já exercido nesta sessão** para os Documentos 17 e 19 | Development Lifecycle fase 18; Kernel §3 (Deprecated, por analogia) |
| 7. Arquivamento | Retenção permanente, nunca deletado — mesma disciplina de Governance §18 (*"Decision Records são permanentes e nunca editados retroativamente"*) e Identity §3.2 (tombstone) | Development Lifecycle fase 19; Identity §3.2 |

**Prova de que o passo 6 não é hipotético:** este próprio documento é escrito na mesma sessão em que os passos 1-7 foram literalmente executados sobre os Documentos 17 e 19 (deprecados) e sobre Compliance Architecture (atualizado para v1.1.0) — o fluxo descrito aqui não é uma proposta teórica, é a **nomeação formal** de um processo já em uso.

---

## 9. Algoritmos

**Nenhum algoritmo novo com lógica de decisão própria.**

```
ALGORITMO PublishDocument(doc_kind, content, project_ref, requested_by):
  classificacao ← Lookup(doc_kind, TabelaClassificação)              # §5 — tabela estática, não lógica nova
  CASO classificacao.natureza:
     "Component-attached" → RETORNA "documentação já embutida no Manifest — nada a publicar à parte"
     "Artifact gerado"    → RETORNA Execution.Dispatch(...)           # Execution §7 — Artifact comum
     "hand-authored"      → SE classificacao.aprovacao_formal:
                                RETORNA Governance.Admit(...)          # Governance §7/§9, conforme camada
                             SENÃO:
                                RETORNA CommitToProjectDocs(project_ref, content)  # Project §6, sem aprovação formal


ALGORITMO GenerateChangelog(project_ref, from_version, to_version):
  versoes ← Identity.Lineage(project_ref, from_version, to_version)    # Identity §7
  entradas ← []
  PARA CADA (v_prev, v_next) EM Pairwise(versoes):
     classe ← Max(ClassifyStandardChange | ClassifyTemplateChange |
                   ClassifySkillChange | ClassifyAgentChange)(v_prev, v_next)  # já existente, por tipo
     dr ← Governance.query(subtype=VERSION_PUBLISHED, version=v_next)   # Decision Record já existente
     entradas += (v_next, classe, dr)
  RETORNA KnowledgeAsset.codifies(entradas)                             # RFC-DM-001 §3.1 — verbatim


ALGORITMO GenerateReleaseNotes(release_ref):
  bundle ← release_ref                                                 # Project §9 — Release = Bundle
  milestones ← Project.ResolveMilestonesFor(bundle.primary_subject, bundle.exported_at)  # Project §10
  RETORNA KnowledgeAsset.codifies(bundle.manifests, milestones)         # RFC-DM-001 §3.1 — verbatim


ALGORITMO DeprecateDocument(doc_ref, successor_ref, reason):
  # mesmo procedimento manual já exercido nesta sessão para os Documentos 17/19 —
  # nomeado aqui, não inventado
  notice ← FormatDeprecationNotice(successor_ref, reason)               # prosa, sem lógica institucional
  PrependToDocument(doc_ref, notice)                                    # texto original preservado abaixo
  RETORNA notice
```

**Terminação/determinismo:** `PublishDocument` é um dispatch trivial sobre uma tabela finita (§5); `GenerateChangelog`/`GenerateReleaseNotes` reutilizam algoritmos já provados terminantes (`Lineage`, os quatro `ClassifyXChange`, `codifies`); `DeprecateDocument` é puramente uma formatação de texto seguida de uma operação de escrita já corriqueira (edição de arquivo), sem decisão institucional própria — a decisão de depreciar já foi tomada antes de chamar este algoritmo.

---

## 10. Diagramas UML

### 10.1 As três classes, nunca uma quarta

```
┌─────────────────────────────────────────────────────────┐
│                  "Tipo documental" (dezessete pedidos)      │
└──────────────────────────┬────────────────────────────────┘
                            │ classifica-se em exatamente uma de três:
        ┌────────────────────┼────────────────────┐
        ▼                    ▼                     ▼
┌───────────────┐  ┌──────────────────┐  ┌────────────────────┐
│ Manifest field  │  │ Artifact           │  │ Prosa hand-authored │
│ «Standards,     │  │ «API docs geradas, │  │ «Constitution,       │
│  Policies»      │  │  relatórios»       │  │  Architecture Docs,   │
│ Kernel §2;      │  │  Domain Model §2#7 │  │  RFC, Runtime Doc,    │
│ Standards §4.3  │  │                    │  │  README, CHANGELOG*  │
└───────────────┘  └──────────────────┘  │  (*Knowledge Asset)   │
                                          └────────────────────┘
```

### 10.2 CHANGELOG/ROADMAP/RELEASE NOTES — mesma técnica, três instâncias

```
Decision Record(s) / Milestone(s) / Bundle       [já existentes, Domain Model §14, Project §10, §9]
        │                    │              │
        │ codifies           │ codifies     │ codifies
        ▼                    ▼              ▼
   CHANGELOG            ROADMAP        RELEASE NOTES
   (Knowledge Asset — RFC-DM-001 §3.1, mesma relação, três nomes de leitura humana)
```

---

## 11. Diagramas de Sequência

### 11.1 Fluxo documental completo — Architecture Document

```
Author        Governance        Registry/Repo        Project(/architecture)
   │              │                   │                       │
   ├─Criação (Draft de RFC ou rascunho)──────────────────────►│                [passo 1]
   ├─Revisão──────►│ Discussão aberta (Governance §9)          │                [passo 2]
   ├─Aprovação────►│ Framework Council / Steward (§8)           │                [passo 3]
   │              ├─Decision + Decision Record                 │
   ├─Publicação────────────────────────────────────────────────►│ commit/push/merge  [passo 4]
   │                                                            │
   │  [tempo depois, mudança necessária]                       │
   ├─Atualização (MINOR aditiva OU nova ratificação)───────────►│                [passo 5]
   │                                                            │
   │  [documento superado por outro]                           │
   ├─Depreciação (notice + redirect, texto preservado)──────────►│                [passo 6]
   │                                                            │
   │  [nunca deletado]                                          │
   └─Arquivamento (retenção permanente)──────────────────────────►│               [passo 7]
```

### 11.2 CHANGELOG sob demanda

```
Owner          DocumentationSvc     Identity(Lineage)     Standards/Template/Skill/Agent    Governance
   │                  │                    │                          │                        │
   ├─GenerateChangelog(project, v1, v2)───►│                          │                        │
   │                  ├─Lineage(v1,v2)─────►│                          │                        │
   │                  │◄─versões────────────┤                          │                        │
   │                  ├─ClassifyXChange (por tipo)──────────────────►│                        │
   │                  │◄─classe─────────────────────────────────────┤                        │
   │                  ├─query(VERSION_PUBLISHED)──────────────────────────────────────────────►│
   │                  │◄─Decision Record[]──────────────────────────────────────────────────────┤
   │◄─KnowledgeAsset (CHANGELOG)│
```

---

## 12. Estados

**Nenhum estado novo.** Dois regimes já existentes, nunca um terceiro:

| Camada | Estados usados | Origem |
|---|---|---|
| Documentação Component-attached (Standards, Policies) | Idêntico ao Kernel §3 do próprio Component (Draft→...→Removed) | Kernel §3 |
| Documentação hand-authored anexada a um Component (nenhuma, por definição — vive dentro do Manifest) | N/A | — |
| Architecture Documents (Constitution, Kernel, este e os demais) | **Não têm `lifecycle_state` como campo** (não são Components — Kernel §0, evita circularidade) — seguem um padrão **análogo, já exercido três vezes**: `Proposed (RFC) → Ratified → Active (consumido por documentos subsequentes) → Amended (MINOR, in-place, ex.: Compliance v1.1.0) → Superseded/Deprecated (notice + redirect, ex.: Documentos 17/19)` | Constitution §9; Governance §9; exercício real nesta sessão |
| CHANGELOG/ROADMAP/RELEASE NOTES | Nenhum — são Knowledge Assets, seguem `Proposed → Validated → Established → Superseded` (Domain Model §8) sem exceção | Domain Model §8 |

**Nota crítica (evita confusão terminológica):** o "estado" de um Architecture Document **não é** uma instância do Kernel Lifecycle — é uma analogia deliberada e explicitamente nomeada como tal, nunca uma alegação de que Constitution/Kernel sejam Components. Confundir os dois reproduziria exatamente a circularidade que Kernel §0 evita (*"o Kernel não tem opinião sobre si mesmo... define a forma que os outros devem ter"*).

---

## 13. Casos Extremos

| # | Caso | Tratamento |
|---|---|---|
| CE-D1 | Dois Architecture Documents se contradizem | Governança §17 (Conflict Resolution) — hierarquia da Constitution (§6) decide; **precedente real**: nenhuma contradição sobrevivente foi encontrada em vinte e oito documentos (Runtime Gap Analysis, `docs/runtime-gap-analysis.md`) |
| CE-D2 | RFC nunca ratificado (fica `Proposed` indefinidamente) | Mesma ambiguidade já aceita por Governance §9 e por Development Lifecycle CE12 — este documento não a resolve nem a agrava |
| CE-D3 | CHANGELOG solicitado para um intervalo de versões sem nenhum Decision Record de `VERSION_PUBLISHED` | `GenerateChangelog` retorna Knowledge Asset vazio — mesma disciplina de "conjunto vazio é resultado válido" (Observability B8; Packaging P8) |
| CE-D4 | RELEASE NOTES para um Release sem nenhum Milestone associado | Válido — `ResolveMilestonesFor` retorna conjunto vazio; RELEASE NOTES descreve apenas o conteúdo do Bundle |
| CE-D5 | MIGRATION GUIDE ausente para uma Breaking Change já classificada `MAJOR` | **MUST** bloquear Publication (Development Lifecycle fase 14) — Governance §10 já exige *"comunicação formal a todos os Consumers"* antes da mudança valer; ausência de Migration Guide é ausência dessa comunicação |
| CE-D6 | README ausente em um Project | Não é erro — apenas `SHOULD` (§16, DOC9), mesma severidade branda já aplicada a "Component sem test_suite" (Testing §11, CE8) |
| CE-D7 | Documentação anexada a um Component que entra em `Archived` | Preservada integralmente (mesma regra de Kernel §3 sobre histórico) — nunca removida junto com o Component |
| CE-D8 | Dois documentos hand-authored (ex.: dois READMEs) descrevendo o mesmo Component de forma divergente | Sinal de drift — detectável apenas por revisão humana (Governance §12, Audit); **não** existe mecanismo automático, mesma limitação disclosed em §3.2 |
| CE-D9 | Documentação hand-authored descrevendo comportamento que o Runtime real não tem mais (drift prosa-vs-código) | `[LACUNA proposital]`, explicitamente disclosed — nenhum `ComplianceTarget` (Standards §4.5) pode ser declarado sobre prosa livre sem introduzir um mecanismo de Standards novo, proibido pelo mandato. Mitigação disponível hoje: Governance §12 (Audit humana), nunca automática |
| CE-D10 | Amendment de um Architecture Document que, na prática, é MAJOR (quebra citação de documento subsequente) | **MUST** seguir nova ratificação completa (Constitution §9, "nova era"), nunca tratado como MINOR — mesma disciplina de Standards §7.1 aplicada, por analogia honesta, a prosa institucional |

---

## 14. Performance

| Recurso | Regra de cache/complexidade | Origem |
|---|---|---|
| `GenerateChangelog`/`GenerateReleaseNotes` | Cacheável indefinidamente para um par `(from_version, to_version)` já fechado — Decision Records e Manifests envolvidos são imutáveis | Registry §8; Packaging §12 |
| `PublishDocument` (Component-attached) | Nenhum custo além do já existente para publicar o próprio Component | Registry §8 |
| Documentação hand-authored | Nenhuma política de cache aplicável — é leitura de arquivo comum, fora da altitude de qualquer Registry | — |

**Nenhuma política de cache nova.**

---

## 15. Eventos

**Nenhum evento novo.**

| Evento | Origem | Ocorre quando |
|---|---|---|
| `ComponentRegistered`/`VersionPublished` | Registry §11 | Publicação de documentação Component-attached |
| `DecisionRecorded` (mesma classe de eventos de Decision) | Domain Model §14; Governance §18 | Aprovação de RFC/Architecture Document |
| `KnowledgeAssetPublished` | RFC-DM-001; já reutilizado por Project §23 | CHANGELOG/ROADMAP/RELEASE NOTES gerados |
| `ComponentDeprecated` (aplicado por analogia a Architecture Documents) | Registry §11 | Depreciação (passo 6) |

---

## 16. Regras Normativas (RFC 2119)

| # | Regra | Nível |
|---|---|---|
| DOC1 | Documentação MUST viver exclusivamente nos diretórios já oficializados por Project Architecture §6 — MUST NOT introduzir diretório novo | MUST / MUST NOT |
| DOC2 | Documentação Component-attached (Standards, Policies, Specifications-como-Contract) MUST viver dentro do próprio Manifest — MUST NOT ser duplicada como arquivo à parte | MUST / MUST NOT |
| DOC3 | "ADR" MUST NOT ser introduzido como convenção distinta — a função MUST continuar sendo cumprida pela combinação Decision Record + `[ESCOLHA DE DESIGN]` | MUST NOT / MUST |
| DOC4 | CHANGELOG, ROADMAP e RELEASE NOTES MUST ser modelados como Knowledge Asset (`codifies`) — MUST NOT introduzir uma quarta especialização de Artifact | MUST / MUST NOT |
| DOC5 | Nenhuma prosa em `/docs` MUST duplicar o conteúdo de um Decision Record em `/records` — MUST apenas referenciá-lo por identificador | MUST NOT / MUST |
| DOC6 | MIGRATION GUIDE MUST existir antes de Publication para qualquer mudança classificada MAJOR por `ClassifyXChange` | MUST |
| DOC7 | Depreciação de um Architecture Document MUST preservar o texto original íntegro, com notice explícito e redirect — MUST NOT editar ou remover silenciosamente | MUST / MUST NOT |
| DOC8 | Arquivamento MUST ser permanente — MUST NOT permitir reciclagem de nome/Coordinate (Identity §3.2) | MUST / MUST NOT |
| DOC9 | Todo Project SHOULD possuir README — ausência MUST NOT bloquear nenhuma fase do Development Lifecycle | SHOULD / MUST NOT |
| DOC10 | Uma emenda a Architecture Document que quebra citação de documento subsequente MUST seguir nova ratificação (nunca MINOR) | MUST |
| DOC11 | Este documento MUST NOT introduzir Registry, Versionamento, Workflow, Lifecycle, Composition, Execution, Policy ou Standards novo | MUST NOT |

---

## 17. Integrações

Cobrindo explicitamente as dez relações pedidas:

| Relação pedida | Como se define — sem alteração ao documento-alvo |
|---|---|
| **Documentação ↔ Project** | `/docs`/`/architecture` são diretórios já oficializados por Project Architecture §6; nenhuma extensão |
| **Documentação ↔ Registry** | Apenas documentação Component-attached é indexada (via o próprio Component); prosa hand-authored **nunca** é Registry-resolvable — Registry & Discovery §3.1/§3.2 já excluem exatamente essa classe |
| **Documentação ↔ Decision Record** | Referência, nunca duplicação (§7, DOC5) — Decision Record é a fonte de verdade (Domain Model §14) |
| **Documentação ↔ RFC** | RFC é, ele próprio, um tipo documental (§5, linha 3) — segue Governance §9 integralmente |
| **Documentação ↔ Standards** | A documentação de um Standard **é** seu próprio `statement`/`rationale` (Standards §4.3) — nenhum documento externo necessário |
| **Documentação ↔ Policies** | Idem, Policy §5 |
| **Documentação ↔ Runtime** | Runtime Documentation é hand-authored, vive em `/docs` referenciando `/runtime` — mesmo papel que `RUNTIME.md` já cumpre neste repositório |
| **Documentação ↔ Testing** | Documentação de um `TestCase` individual já vive nos próprios campos de `test_suite[]` (Testing §4.4) — um "Guia de Testes" é Project Documentation comum, separado |
| **Documentação ↔ Security** | Mesmo padrão de Testing — controles de segurança já se autodocumentam via Standard/Policy (Security §4.5); um "Guia de Segurança" é Project Documentation |
| **Documentação ↔ Development Lifecycle** | Cada tipo documental é produzido em uma fase específica (§8) — Specifications na fase 2 (Requirements), Architecture Documents na fase 4 (Architecture), MIGRATION GUIDE quando a fase 17 (Evolution) classifica MAJOR, RELEASE NOTES/CHANGELOG na fase 14 (Publication) |

| Documento | Integração adicional |
|---|---|
| **Constitution** | Regra Imutável nº10 fundamenta DOC3 (não duplicar ADR) |
| **Kernel** | §0 fundamenta a nota crítica de §12 (Architecture Documents não são Components) |
| **Governance** | §7-§9-§10-§18 realizam integralmente o fluxo documental (§8) |
| **Domain Model v1.1.0** | `Decision`/`Decision Record`/`Artifact`/`Knowledge Asset` reutilizados sem exceção |
| **RFC-DM-001** | `codifies` é o mecanismo inteiro de CHANGELOG/ROADMAP/RELEASE NOTES |
| **Identity & Namespace** | Lineage (§7) base de CHANGELOG; tombstone (§3.2) base de Arquivamento |
| **Registry & Discovery** | Confirma, por exclusão, que prosa livre nunca é indexada |
| **Validation & Certification** | Nenhuma alteração — Documentation não certifica prosa |
| **Composition / Execution** | Nenhuma alteração direta |
| **Standards / Policy** | `statement`/`rationale` já são a documentação do próprio Component |
| **Template Architecture** | Nenhuma alteração |
| **Skill / Agent Architecture (23)** | `ClassifySkillChange`/`ClassifyAgentChange` reutilizados por CHANGELOG |
| **Observability Architecture** | Nenhuma alteração |
| **Organization & Tenancy** | Nenhuma alteração |
| **Packaging & Distribution** | `Bundle` é a base de RELEASE NOTES |
| **Compliance Architecture** | Precedente real de "Atualização" (v1.1.0, MINOR aditiva) |
| **RFC-COMP-001** | Nenhuma alteração |
| **Testing Architecture (24)** | `test_suite[]` já autodocumentado |
| **Quality Gate Architecture (25)** | Nenhuma alteração direta |
| **Security Architecture (26)** | Standards/Policies de segurança já autodocumentados |
| **Development Lifecycle Architecture (27)** | Mapeamento completo do fluxo documental às dezenove fases (§8) |
| **Project Architecture (28)** | Precedente direto e integral — §6/§15 daquele documento são a base inteira deste |

---

## 18. Validação Institucional

| Documento base | Resultado |
|---|---|
| Constitution | **PASS** — Regra Imutável nº10 fundamenta DOC3 |
| Kernel | **PASS** — §0 fundamenta a distinção Architecture Document ≠ Component |
| Governance | **PASS** — §7, §9, §10, §18 reutilizados sem redefinição |
| Domain Model v1.1.0 | **PASS** — zero entidades/relações/estados |
| RFC-DM-001 | **PASS** — `codifies` reutilizado três vezes (CHANGELOG/ROADMAP/RELEASE NOTES) |
| Identity & Namespace | **PASS** — Lineage/tombstone reutilizados |
| Registry & Discovery | **PASS** — confirma escopo de indexação, sem extensão |
| Validation & Certification | **PASS** — sem alteração |
| Composition / Execution | **PASS** — sem alteração |
| Standards / Policy | **PASS** — `statement`/`rationale` reutilizados como autodocumentação |
| Template Architecture | **PASS** |
| Skill / Agent Architecture (23) | **PASS** — classificadores de mudança reutilizados |
| Observability Architecture | **PASS** |
| Organization & Tenancy | **PASS** |
| Packaging & Distribution | **PASS** — `Bundle` reutilizado para RELEASE NOTES |
| Compliance Architecture | **PASS** — precedente real de Atualização |
| RFC-COMP-001 | **PASS** |
| Testing Architecture (24) | **PASS** |
| Quality Gate Architecture (25) | **PASS** |
| Security Architecture (26) | **PASS** |
| Development Lifecycle Architecture (27) | **PASS** — fluxo documental mapeado às fases já existentes |
| Project Architecture (28) | **PASS** — §6/§15 daquele documento reutilizados integralmente, sem reabertura |
| **Exige RFC?** | **NÃO** |

**Prova formal de que Documentation não adiciona:**

| Item vedado pelo mandato | Verificação |
|---|---|
| Novo Registry | Nenhum — §17, prosa hand-authored explicitamente nunca indexada |
| Novo sistema de Versionamento | Nenhum — SemVer (Kernel §2.11) reutilizado quando aplicável |
| Novo Workflow | Nenhum — fluxo documental é `Phase`/`Step` (§8), sem StepKind novo |
| Novo Lifecycle | Nenhum — Kernel §3 para Component-attached; padrão análogo já exercido (não inventado) para Architecture Documents (§12) |
| Novo mecanismo de Composition/Execution/Policy/Standards | Nenhum — §17, §18 |

---

## 19. Dependências Futuras

| Consumidor | O que consome | Estado |
|---|---|---|
| **CI/CD** (futuro, operacional) | O fluxo documental (§8) é diretamente traduzível para gates automatizados de publicação de documentação | Desbloqueado |
| **Observability — implementação em Runtime** | Séries históricas de `KnowledgeAssetPublished`/depreciações de documento | Sem bloqueio adicional |
| **Multi-Agent Architecture** (futuro) | Um Agent MAY gerar CHANGELOG/RELEASE NOTES automaticamente via os algoritmos de §9, sem esperar autoria humana | Sem bloqueio |
| **Mecanismo de detecção de drift de prosa** (nenhum documento futuro ainda o reserva) | `[LACUNA proposital]` genuína, disclosed em CE-D9 — nenhum forward-reference é criado aqui, porque nenhum mecanismo de Standards sobre prosa livre é sequer contemplado sem violar o mandato desta série | Deliberadamente não reservada |

---

## 20. Critério de Aceitação

### ✔ Checklist Institucional

| Critério do mandato | Status |
|---|---|
| Dezessete tipos documentais classificados, cada um como Asset ou projeção | ✔ §5 |
| Justificativa explícita da ausência de ADR como convenção distinta | ✔ §5.1 |
| Estrutura oficial da documentação, reutilizando Project Architecture | ✔ §6 |
| Organização dos registros, sem duplicação com `/records` | ✔ §7 |
| Fluxo documental de sete passos, reutilizando Governance/Workflow/Registry/Development Lifecycle | ✔ §8 |
| Dez relações pedidas (Project, Registry, Decision Record, RFC, Standards, Policies, Runtime, Testing, Security, Development Lifecycle) | ✔ §17 |
| Zero Registry/Versionamento/Workflow/Lifecycle/Composition/Execution/Policy/Standards novo | ✔ §18 |
| UML, sequência, algoritmos, casos extremos, RFC2119, performance, eventos | ✔ §9-§16 |
| Tabela de proveniência completa | ✔ §4.1 |
| Integração documento a documento (vinte e oito anteriores) | ✔ §17 |
| Nenhuma alteração a documento anterior — RFC separada se necessário | ✔ §18 — nenhuma mudança encontrada; nenhuma RFC necessária |

### ✔ Objetivo Prático Realizado

O Framework Eng possui, a partir deste documento, um modelo oficial de documentação para qualquer Project construído sobre ele: dezessete tipos documentais nomeados, cada um rastreável a uma de três classes já existentes (campo de Manifest, Artifact gerado, ou prosa hand-authored organizada por Project), um fluxo de sete passos já exercido de verdade nesta mesma sessão (não apenas teorizado), e dez relações explícitas com o restante do corpus.

### ✔ Confirmação Explícita

**Nenhum dos vinte e oito documentos anteriores foi alterado.** A prova mais forte deste documento não é apenas lógica — é **empírica**: o fluxo de sete passos que ele formaliza já foi executado, dentro desta mesma sessão, três vezes (RFC-DM-001, Compliance v1.1.0, depreciação dos Documentos 17/19), antes mesmo deste documento existir para nomeá-lo. Documentation Architecture não propõe um processo — **reconhece e nomeia um que já estava em uso**.

---

*Fim do documento. Versão 1.0.0.*
