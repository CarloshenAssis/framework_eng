# DOMAIN MODEL ARCHITECTURE
### Framework Eng — O Meta-Modelo Semântico do Sistema

*Versão 1.0.0 — Especificação Institucional*

> A Constitution define por que o Framework existe. O Kernel define a forma que tudo deve ter. A Governance define quem decide e como. Este documento define **o vocabulário — as entidades, relações e regras semânticas que tornam possível descrever qualquer coisa dentro do Framework sem ambiguidade**. Nenhum Standard, Skill, Agent, Workflow ou Template pode ser descrito de forma válida usando um conceito que não esteja definido aqui.

---

# 1. Papel do Domain Model

O Kernel Architecture definiu a *forma estrutural* de um Componente (Component Contract, Manifest, Lifecycle). O que faltava — e é o objeto deste documento — é o **vocabulário semântico** que dá sentido a essa forma: o que é, afinal, um Artefato? O que distingue Conhecimento de Evidência? O que diferencia uma Execução de uma Decisão? O Kernel diz "todo componente tem Outputs" — o Domain Model diz **o que uma Output pode, de fato, ser**.

Sem este documento, cada Standard futuro reinventaria seu próprio vocabulário — um definiria "evidência" de um jeito, outro de outro, e a interoperabilidade prometida pelo Kernel (Seção 11 daquele documento) quebraria silenciosamente na semântica, mesmo respeitando a forma.

O Domain Model é, portanto, **a ontologia do Framework**: o conjunto fechado e formal de tipos de entidade e relações entre elas, do qual todo conceito futuro deve derivar por especialização — nunca por invenção paralela.

---

# 2. Entidades Fundamentais do Framework

O universo do Framework é composto por **catorze entidades fundamentais**, organizadas em cinco classificações (Seção 4). Cada uma é definida de forma exaustiva — nenhuma entidade futura pode ser introduzida fora desta lista sem passar pelo processo formal de evolução do modelo (Seção 18).

| # | Entidade | Definição essencial |
|---|---|---|
| 1 | **Component** | Qualquer unidade reconhecida pelo Kernel, com Contract, Identity e Lifecycle próprios. |
| 2 | **Manifest** | A representação declarativa formal de um Component. |
| 3 | **Contract** | O conjunto de compromissos (entrada, saída, capacidades, restrições) que um Component declara. |
| 4 | **Capability** | Uma unidade nomeada de "o que pode ser feito", oferecida por um Component. |
| 5 | **Context** | O estado relevante — de projeto, domínio ou sessão — que condiciona como um Component se comporta em uma Execution específica. |
| 6 | **Execution** | Uma instância concreta e única de um Component sendo aplicado em um momento específico. |
| 7 | **Artifact** | Qualquer resultado tangível e persistente produzido por uma Execution ou por uma Decision. |
| 8 | **Evidence** | Um Artifact cuja função específica é comprovar que um resultado declarado de fato ocorreu. |
| 9 | **Knowledge** | Entendimento acumulado, validado e reutilizável, derivado de Execution, Research ou Decision. |
| 10 | **Decision** | Uma escolha formal, tomada por um Role sob autoridade de Governance, que altera o estado de um ou mais Components. |
| 11 | **Decision Record** | O Artifact permanente que documenta uma Decision. |
| 12 | **Role** | Uma posição de responsabilidade (Owner, Steward, Reviewer etc.) definida pela Governance, ocupada por uma pessoa, time ou Agent. |
| 13 | **Relationship** | Uma conexão declarada e tipada entre dois Components (Dependency, Provider, Consumer — ver Seção 5). |
| 14 | **Metric** | Uma medida quantificável e recorrente sobre o estado de um Component, um domínio, ou do Framework como um todo. |

---

# 3. Hierarquia Completa das Entidades

A hierarquia não é uma árvore de pastas — é uma hierarquia de **generalização/especialização** (o que, em um meta-modelo, se chama de `is-a`).

```
ENTITY (raiz abstrata — tudo no Framework é uma Entity)
│
├── Component                          [abstrato — ver Kernel Architecture]
│   ├── Structural Component
│   │   ├── Standard
│   │   ├── Policy
│   │   └── Template
│   ├── Operational Component
│   │   ├── Skill
│   │   ├── Agent
│   │   └── Workflow
│   └── Knowledge Component
│       ├── Research
│       ├── Playbook
│       └── Knowledge Base Entry
│
├── Descriptive Entity
│   ├── Manifest
│   ├── Contract
│   └── Capability
│
├── Situational Entity
│   └── Context
│
├── Event Entity
│   ├── Execution
│   └── Decision
│
├── Output Entity
│   ├── Artifact
│   │   └── Evidence            [especialização de Artifact]
│   ├── Decision Record         [especialização de Artifact]
│   └── Knowledge               [pode ser produzido como Output de Execution/Decision]
│
├── Institutional Entity
│   ├── Role
│   └── Relationship
│
└── Observational Entity
    └── Metric
```

**Nota de leitura:** `Standard`, `Policy`, `Template`, `Skill`, `Agent` e `Workflow` **não são definidos neste documento como componentes concretos** — eles aparecem aqui apenas como *categorias* dentro da hierarquia do Domain Model, herdando de `Component`. Sua definição normativa detalhada é papel do Standards Architecture e de documentos subsequentes. Isso respeita a restrição deste documento (não criar Standards/Policies/Templates/Agents/Skills/Workflows) enquanto ainda permite que o modelo seja completo.

---

# 4. Classificação das Entidades

Toda entidade do Framework pertence a exatamente uma das cinco classificações abaixo — a classificação determina suas regras gerais de persistência, mutabilidade e governança.

### 4.1 Estruturais
Definem forma e regras normativas. Ex.: `Standard`, `Policy`, `Template`, `Contract`, `Manifest`. Mudam raramente; toda mudança é um evento de Governance formal.

### 4.2 Operacionais
Executam trabalho. Ex.: `Skill`, `Agent`, `Workflow`. Mudam com frequência moderada; versionadas continuamente.

### 4.3 Conhecimento
Acumulam entendimento reutilizável. Ex.: `Knowledge`, `Research`, `Playbook`. Crescem por adição; raramente são "corrigidas" — mais frequentemente são superadas por uma entrada nova que referencia a anterior.

### 4.4 Governança
Regulam o sistema. Ex.: `Role`, `Decision`, `Decision Record`, `Relationship` (quando expressa política de dependência formal). Sua integridade é a mais protegida — nenhuma entidade de Governança é editável retroativamente (apenas superada por um novo registro).

### 4.5 Execução
Representam o acontecimento real no tempo. Ex.: `Execution`, `Artifact`, `Evidence`, `Metric`. São, por natureza, as mais transitórias e as mais numerosas — o volume do Framework em 5 anos será dominado por entidades desta classe.

---

# 5. Relacionamentos entre Entidades

Todo relacionamento entre entidades é **tipado e nomeado** — não existe relação genérica e implícita no Domain Model.

| Relacionamento | De | Para | Natureza |
|---|---|---|---|
| **describes** | Manifest | Component | 1:1 — todo Component tem exatamente um Manifest vigente por versão |
| **declares** | Component | Contract | 1:1 |
| **exposes** | Contract | Capability | 1:N |
| **depends_on** | Component | Component | N:N (ver Kernel, `dependencies`) |
| **provides_for** | Component | Component | N:N (relação de composição/orquestração — ver Kernel, `providers`) |
| **consumes** | Component | Component | N:N — inverso derivado de `depends_on`, mantido pelo sistema |
| **occurs_within** | Execution | Context | N:1 — toda Execution acontece dentro de exatamente um Context |
| **produces** | Execution | Artifact | 1:N |
| **produces** | Decision | Decision Record | 1:1 |
| **substantiates** | Evidence | Execution | N:1 — toda Evidence comprova exatamente uma Execution |
| **derives_from** | Knowledge | Execution \| Decision \| Research | N:N |
| **informs** | Knowledge | Decision | N:N — conhecimento acumulado pode subsidiar decisões futuras |
| **performed_by** | Execution | Role | N:1 |
| **authorizes** | Role | Decision | 1:N |
| **references** | Decision Record | Component | N:N — toda decisão referencia os componentes afetados |
| **measures** | Metric | Component \| Domain \| Framework | N:1 |
| **supersedes** | Decision Record | Decision Record | 1:1 (opcional) — uma nova decisão pode substituir formalmente uma anterior |

---

# 6. Regras de Dependência entre Entidades

1. **Nenhuma entidade de Execução existe sem Context declarado.** Uma Execution sem Context é semanticamente inválida — não pode ser interpretada nem auditada.
2. **Nenhum Artifact existe sem uma Execution ou Decision que o originou.** Artifacts não nascem espontaneamente — todo Artifact tem proveniência rastreável.
3. **Toda Evidence pressupõe a existência prévia da Execution que ela comprova.** Evidence nunca precede seu objeto.
4. **Toda Decision pressupõe um Role com autoridade declarada (Governance Architecture) para tomá-la.** Uma Decision sem Role autorizado é inválida por definição, independente do conteúdo.
5. **Knowledge pode depender de múltiplas fontes (Execution, Decision, Research), mas nunca de outra Knowledge sem Relationship explícita `derives_from`.** Conhecimento não se propaga por herança implícita.
6. **Component nunca depende diretamente de Execution, Artifact ou Decision.** Um Component é atemporal por natureza (definição estrutural); ele pode ser *informado por* Knowledge, mas sua definição não pode depender de um evento específico no tempo — isso quebraria reprodutibilidade.

---

# 7. Cardinalidade

| Relação | Cardinalidade |
|---|---|
| Component : Manifest (por versão) | 1:1 |
| Component : Contract | 1:1 |
| Contract : Capability | 1:N |
| Component : Component (`depends_on`) | N:N |
| Component : Component (`provides_for`) | N:N |
| Execution : Context | N:1 |
| Execution : Artifact | 1:N |
| Execution : Evidence | 1:N |
| Execution : Role (performer) | N:1 |
| Decision : Decision Record | 1:1 |
| Decision : Role (autoridade) | N:1 |
| Decision Record : Component (afetados) | N:N |
| Knowledge : fontes (`derives_from`) | N:N |
| Metric : alvo medido | N:1 |
| Role : Decision | 1:N |

---

# 8. Ciclo de Vida de Cada Entidade

| Entidade | Ciclo de vida |
|---|---|
| **Component** | `Draft → Review → Approved → Active → Deprecated → Archived → Removed` (definido integralmente no Kernel Architecture, Seção 3). |
| **Manifest** | Nasce junto com cada versão do Component; imutável após publicação (`Active`); uma nova versão gera um novo Manifest, nunca edita o anterior. |
| **Contract** | Vinculado 1:1 ao Manifest — mesmo regime de imutabilidade por versão. |
| **Execution** | `Initiated → Running → Completed | Failed | Aborted`. Estado terminal é permanente — uma Execution nunca é reaberta; uma nova tentativa é uma nova Execution. |
| **Artifact** | `Generated → Verified → Retained | Superseded`. Um Artifact pode ser superado por uma versão mais nova sem deixar de existir historicamente. |
| **Evidence** | `Captured → Validated → Retained`. Evidence nunca é editada após captura — apenas invalidada formalmente se a Execution associada for considerada inválida. |
| **Knowledge** | `Proposed → Validated → Established → Superseded`. Conhecimento estabelecido não é apagado quando superado — permanece rastreável como histórico. |
| **Decision** | `Proposed → Authorized → Recorded`. Estado terminal único — uma Decision não é "desfeita", apenas superada por uma nova Decision (com novo Decision Record que referencia a anterior). |
| **Decision Record** | `Created → Immutable`. Nunca editado; correção gera novo registro com `supersedes`. |
| **Role** | `Assigned → Active → Transferred | Vacated` (ver Governance Architecture, Ownership/Sucessão). |
| **Metric** | Contínua — não tem estado terminal enquanto o que ela mede permanecer relevante; é recalculada em cada ciclo de observação. |

---

# 9. Entidades Persistentes vs. Transitórias

| Persistentes (permanecem indefinidamente, mesmo após relevância operacional cessar) | Transitórias (existem por uma janela de tempo funcional) |
|---|---|
| Component (histórico completo até `Removed`, e mesmo após, como registro mínimo) | Context (válido apenas durante a Execution que o usa) |
| Manifest / Contract (imutáveis por versão) | Execution (evento único, não reaberto) |
| Decision Record | — |
| Knowledge (mesmo superado, mantido como histórico) | — |
| Evidence | — |
| Metric (série histórica) | Métrica *instantânea* (o valor pontual é transitório; a série histórica é persistente) |

**Regra geral:** nenhuma entidade de Governança ou Conhecimento é verdadeiramente transitória — mesmo entidades "encerradas" (Decision Record superado, Knowledge substituída) permanecem no sistema como histórico auditável. Apenas `Context` é genuinamente efêmero por natureza — ele é, por definição, específico de um momento e não tem valor fora dele.

---

# 10. Fluxo de Geração de Artefatos

```
Component (Active)
      │
      │ é invocado dentro de
      ▼
   Context  ─────────────────────► condiciona
      │
      ▼
  Execution  ── performed_by ──► Role
      │
      ├──► produces ──► Artifact ──► (opcionalmente) torna-se input de nova Execution
      │
      ├──► produces ──► Evidence ──► substantiates a própria Execution
      │
      └──► pode gerar ──► Knowledge (quando o resultado é validado como reutilizável)
                              │
                              └──► informs ──► Decision futura
```

Todo Artifact tem uma cadeia de proveniência reconstruível: de qual Execution veio, sob qual Context, executado por qual Role, usando qual versão de qual Component. Um Artifact sem essa cadeia completa é, por definição, inválido dentro do Domain Model — não é auditável e portanto não pode ser tratado como confiável.

---

# 11. Modelo de Conhecimento

**Knowledge** é a entidade que representa entendimento validado e reutilizável — distinta de um Artifact comum por ter passado por um processo de validação que a torna apta a **informar decisões futuras**, não apenas registrar um resultado passado.

Fontes de Knowledge (relação `derives_from`):
- **Execution** — padrões observados repetidamente através de múltiplas execuções.
- **Research** — investigação estruturada conduzida deliberadamente para reduzir incerteza.
- **Decision** — o raciocínio e o contexto por trás de uma escolha institucional, capturado para reuso.

Knowledge nunca é criada diretamente — ela é sempre **derivada** de algo que já aconteceu (Execution) ou foi deliberadamente investigado (Research) ou decidido (Decision). Isso a distingue de Standards e Policies (Componentes Estruturais), que são normativos *para o futuro*; Knowledge é descritiva *do que se aprendeu*.

Knowledge segue seu próprio ciclo de vida (Seção 8) independente do ciclo de vida do Component que a originou — uma Skill pode ser `Removed` e a Knowledge derivada de suas execuções permanece `Established`, pois seu valor histórico independe da existência continuada da fonte.

---

# 12. Modelo de Execução

**Execution** é o único ponto do Domain Model em que o sistema deixa de ser puramente declarativo. Toda Execution é:

- **Única** — identificada de forma não ambígua (nunca duas Execuções são "a mesma").
- **Contextualizada** — ocorre sempre `occurs_within` um Context específico.
- **Atribuída** — sempre `performed_by` um Role identificável (humano, Agent, ou combinação orquestrada).
- **Rastreável até o Component e a versão exata** que a originou — nunca até um Component genérico sem versão.
- **Produtora de saída verificável** — toda Execution que termina em `Completed` produz ao menos um Artifact ou Evidence; uma Execution que não produz nada verificável é, por definição, inconclusiva e não pode ser tratada como sucesso.

Execution é o evento a partir do qual todas as outras entidades de Output (Artifact, Evidence, potencialmente Knowledge) se originam — é o "verbo" central do Domain Model, enquanto Component é o "substantivo".

---

# 13. Modelo de Evidências

**Evidence** é uma especialização de Artifact com uma função exclusiva: **comprovar** que uma Execution produziu o resultado que declarou produzir.

Propriedades exclusivas de Evidence (que a distinguem de um Artifact comum):
- Vínculo obrigatório e único (`substantiates`) a exatamente uma Execution.
- Imutabilidade absoluta após captura — Evidence editada deixa de ser Evidence (perde sua função probatória) e deve ser tratada como inválida.
- Papel central em Certification e Audit (Governance Architecture) — nenhuma Certification é concedida, e nenhuma Audit é considerada completa, sem Evidence associada às afirmações verificadas.

Nem todo Artifact é Evidence (um relatório gerado pode ser apenas um resultado de trabalho), mas toda Evidence é um Artifact (herda proveniência, imutabilidade de forma, e rastreabilidade).

---

# 14. Modelo de Decisões

**Decision** é o evento formal pelo qual um Role autorizado altera o estado de um ou mais Components (aprovação, rejeição, mudança de Lifecycle, resolução de conflito, concessão de exceção — ver Governance Architecture).

Toda Decision:
- É tomada por um **Role com autoridade declarada** para aquele tipo específico de decisão (Governance Architecture, Seção 8, "Quem Pode Alterar o Quê").
- Produz exatamente um **Decision Record**, de forma inseparável — não existe Decision sem seu registro correspondente.
- Pode **referenciar Knowledge** que a informou, tornando explícito o raciocínio, não apenas o resultado.
- É **imutável uma vez registrada** — uma mudança de entendimento não edita a Decision original, gera uma nova Decision cujo Decision Record usa `supersedes` para apontar à anterior.

Este modelo garante que a história institucional do Framework (por que cada coisa é como é) seja, ela própria, uma entidade de primeira classe — nunca uma consequência acidental de outros processos.

---

# 15. Modelo de Rastreabilidade entre Entidades

Toda entidade de Output (Artifact, Evidence, Decision Record, Knowledge) deve poder responder, sem exceção, às seguintes perguntas de rastreabilidade:

1. **De onde veio?** (Execution ou Decision de origem)
2. **Sob qual Context?**
3. **Quem foi responsável?** (Role)
4. **Contra qual versão de qual Component?**
5. **O que ela afeta ou referencia?** (Components, outras entidades)

A cadeia de rastreabilidade nunca pode ter um elo quebrado — se qualquer uma dessas cinco perguntas não puder ser respondida para uma entidade, essa entidade é, por definição do Domain Model, **inválida** e não pode ser tratada como confiável para fins de Governance, Certification ou Audit (Governance Architecture).

Esse é o mecanismo semântico que torna Auditoria e Certificação possíveis em escala: elas não dependem de reconstrução manual de histórico — dependem de a rastreabilidade já estar embutida na própria existência de cada entidade.

---

# 16. Diagrama UML Textual Completo

```
┌─────────────────────────────────────────────────────────────────────┐
│ «abstract» Entity                                                     │
└─────────────────────────────────────────────────────────────────────┘
              △
              │
   ┌──────────┼───────────────────────────────────────────────────┐
   │          │                    │                    │          │
┌──┴───┐ ┌────┴─────┐      ┌───────┴──────┐    ┌────────┴───┐ ┌───┴────┐
│Component│ │Descriptive│      │  Situational  │    │    Event    │ │Output  │
│«abstract»│ │  Entity   │      │    Entity     │    │   Entity    │ │Entity  │
└──┬───┘ └────┬─────┘      └───────┬──────┘    └────────┬───┘ └───┬────┘
   │          │                    │                    │          │
   │     ┌────┴────┐               │            ┌───────┴──┐   ┌───┴────────┐
   │     │Manifest │            ┌──┴──┐         │Execution │   │  Artifact   │
   │     │Contract │            │Context│        │Decision  │   │  «─────┐   │
   │     │Capability│            └─────┘         └──────────┘   │  Evidence  │
   │     └─────────┘                                            │(specializes │
   │                                                             │  Artifact)  │
   │                                                             │Decision     │
   │                                                             │ Record      │
   │                                                             │(specializes │
   │                                                             │  Artifact)  │
   │                                                             │Knowledge    │
   │                                                             └────────────┘
   │
   ├── Structural Component  ──► {Standard, Policy, Template}  *categorias, não instâncias*
   ├── Operational Component ──► {Skill, Agent, Workflow}      *categorias, não instâncias*
   └── Knowledge Component   ──► {Research, Playbook, KB Entry} *categorias, não instâncias*

┌─────────────────────────────────────────────────────────────────────┐
│ «institutional» Role  ──authorizes──► Decision                       │
│ «institutional» Relationship  (depends_on | provides_for | consumes) │
│ «observational» Metric  ──measures──► (Component | Domain | Framework)│
└─────────────────────────────────────────────────────────────────────┘
```

**Notas de leitura UML:**
- `△` indica generalização (is-a).
- `Evidence` e `Decision Record` são especializações formais de `Artifact` — herdam proveniência, imutabilidade e regras de rastreabilidade, adicionando restrições próprias (Seções 13 e 14).
- `Component` permanece `«abstract»` neste documento — suas subclasses concretas (Standard, Agent etc.) são apenas nomeadas como categorias; sua especificação normativa completa é diferida aos documentos subsequentes (Standards Architecture e além), conforme a restrição deste documento.

---

# 17. Diagrama de Relacionamentos

```
   Manifest ──describes──► Component ◄──depends_on──► Component
                               │  ▲                        │
                          declares  provides_for/consumes  │
                               │  │                        │
                               ▼  │                        │
                           Contract                        │
                               │                            │
                            exposes                         │
                               ▼                            │
                          Capability                        │
                                                             │
   Component ◄──occurs against / is used within──── Execution
                                                       │  │  │
                                        performed_by ──┘  │  └── occurs_within ──► Context
                                                           │
                                                     produces
                                                     ┌─────┴─────┐
                                                     ▼           ▼
                                                 Artifact     Evidence
                                                     │      (substantiates
                                                derives_from   Execution)
                                                     │
                                                     ▼
                                                 Knowledge ──informs──► Decision
                                                                            │
                                                                       produces
                                                                            ▼
                                                                    Decision Record
                                                                            │
                                                                       references
                                                                            ▼
                                                                       Component

   Role ──authorizes──► Decision
   Role ──performed_by (inverso)──► Execution

   Metric ──measures──► Component | Domain | Framework  (observação contínua, fora do fluxo de produção)
```

---

# 18. Regras de Evolução do Modelo

1. **Nenhuma entidade nova é adicionada à lista fundamental (Seção 2) sem RFC formal** aprovado pelo Framework Council (Governance Architecture, Seção 9) — o Domain Model tem a mesma proteção estrutural do Kernel, por ser igualmente fundacional.
2. **Especialização é sempre preferível a criação de nova entidade raiz.** Um novo conceito que se comporta como um Artifact deve ser modelado como especialização de Artifact (como Evidence e Decision Record o são), nunca como uma entidade paralela desconectada da hierarquia.
3. **Nenhuma mudança no Domain Model pode invalidar retroativamente entidades já existentes.** Evolução é aditiva ou de especialização — nunca uma reforma que torne inválido o que já foi registrado sob a versão anterior do modelo.
4. **Toda mudança no Domain Model gera um Decision Record próprio**, seguindo o mesmo mecanismo de Governança usado para qualquer outra decisão estrutural.
5. **O Domain Model é versionado independentemente do Kernel e da Constitution**, mas mudanças nele têm, por natureza, impacto potencial em ambos — por isso sua autoridade de aprovação é a mesma do Kernel (Framework Council).

---

# 19. Princípios de Consistência Semântica

1. **Um mesmo termo nunca significa duas coisas diferentes em domínios diferentes do Framework.** Se dois domínios precisam de conceitos parecidos mas distintos, eles devem ser modelados como entidades ou especializações distintas, nunca reaproveitar o mesmo nome com semântica divergente.
2. **Toda entidade concreta futura deve ser redutível a uma das catorze entidades fundamentais por especialização.** Se um conceito novo não se encaixa em nenhuma delas, isso é sinal de que o Domain Model está incompleto — e deve ser resolvido por evolução formal (Seção 18), nunca por uso informal fora do modelo.
3. **Relações não declaradas não existem.** Assim como no Kernel um Component não pode depender implicitamente de outro, nenhuma entidade do Domain Model pode se relacionar com outra fora dos Relationships tipados definidos na Seção 5.
4. **Rastreabilidade não é opcional para nenhuma entidade de Output.** Consistência semântica pressupõe que toda afirmação do sistema ("isto foi decidido", "isto foi comprovado", "isto foi aprendido") possa ser reconstruída até sua origem (Seção 15).
5. **Nomenclatura é estável.** Uma vez que um termo é definido no Glossário (Seção 20), seu significado não muda entre versões do Domain Model sem processo formal de evolução — times e Agents constroem entendimento cumulativo sobre um vocabulário estável, não sobre um alvo em movimento.

---

# 20. Glossário Inicial das Entidades

| Termo | Definição formal |
|---|---|
| **Entity** | A raiz abstrata de tudo que existe no universo semântico do Framework. |
| **Component** | Entidade reconhecida pelo Kernel, com Contract, Identity e Lifecycle próprios (definição completa: Kernel Architecture). |
| **Manifest** | A representação declarativa e imutável (por versão) de um Component. |
| **Contract** | O conjunto de compromissos de entrada, saída, capacidades e restrições que um Component declara. |
| **Capability** | Uma unidade nomeada e descoberta de "o que pode ser feito" por um Component. |
| **Context** | O estado situacional — de projeto, domínio ou sessão — que condiciona uma Execution específica; entidade transitória por natureza. |
| **Execution** | Um evento único e não reaberto de aplicação concreta de um Component, sempre atribuído a um Role e ocorrido dentro de um Context. |
| **Artifact** | Qualquer resultado tangível e persistente produzido por uma Execution ou Decision, com proveniência sempre rastreável. |
| **Evidence** | Especialização de Artifact cuja função exclusiva é comprovar o resultado declarado de uma Execution específica; imutável após captura. |
| **Knowledge** | Entendimento validado e reutilizável, derivado de Execution, Research ou Decision, apto a informar Decisions futuras. |
| **Decision** | Escolha formal tomada por um Role com autoridade declarada, que altera o estado de um ou mais Components. |
| **Decision Record** | Especialização de Artifact que documenta permanentemente uma Decision; imutável, superável apenas por um novo registro. |
| **Role** | Posição de responsabilidade institucional (Owner, Steward, Reviewer, Auditor, Certifier — Governance Architecture), ocupada por pessoa, time ou Agent. |
| **Relationship** | Conexão tipada e declarada entre dois Components (`depends_on`, `provides_for`, `consumes`). |
| **Metric** | Medida quantificável e recorrente sobre o estado de um Component, domínio ou do Framework como um todo. |
| **Research** | Categoria de Knowledge Component — investigação estruturada e deliberada conduzida para reduzir incerteza antes de uma Decision. |
| **Playbook** | Categoria de Knowledge Component — guia de resposta estruturada para uma classe recorrente de situação, derivado de Knowledge acumulada. |
| **Standard / Policy / Template / Skill / Agent / Workflow** | Categorias de Component (Structural, Operational) referenciadas por nome neste modelo, cuja especificação normativa detalhada é objeto de documentos subsequentes — não definidas em profundidade aqui. |

---

## Fechamento

O Domain Model não introduz nenhum processo novo, nenhuma regra de aprovação, nenhuma forma de manifesto — todos esses já existem no Kernel e na Governance. O que ele introduz é a **garantia de que, quando o Framework tiver centenas de Agents, milhares de Skills e dezenas de Workflows, todos eles estarão falando exatamente a mesma língua semântica** — o mesmo entendimento do que é uma Execution, uma Evidence, uma Decision, um Contexto — porque essa língua foi fixada aqui, antes de qualquer um deles existir.

É esse vocabulário compartilhado, mais do que qualquer processo de governança, que torna possível a um Agent de IA criado no ano 5 do Framework interpretar corretamente um Decision Record registrado no ano 1 — a semântica não deriva, porque ela nunca foi implícita.
