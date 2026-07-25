# Template Architecture
### Framework Eng — Documento 1 da Camada de Inteligência

*Versão 1.0.0 · Base normativa (congelada): Constitution · Kernel · Governance · Domain Model v1.1.0 · RFC-DM-001 · Identity & Namespace · Registry & Discovery · Validation & Certification · Composition · Workflow · Execution · Standards · Policy*

---

## 1. Posição Arquitetural

Um `Template` **não é um Component**. Não possui `Identity`, não possui `Coordinate`, não é registrado, não é descoberto, não tem Lifecycle próprio. Um Template é **conteúdo interno especializado do Contract** de um Component operacional (Skill, Agent ou Workflow) — habilitado pelo Kernel §9 (Extension Model), exatamente na mesma classe estrutural de `Phase`/`Step` (Workflow §4) e `NormativeRequirement` (Standards §4). Templates vivem no campo `templates[]` do Manifest de seu Component portador, ao lado (nunca em substituição) dos quinze campos universais do Component Contract.

### 1.1 Resolução da tensão terminológica com Domain Model §3

Domain Model §3 nomeia `Template` como categoria de *Structural Component*, na mesma linha em que nomeou `Standard` e `Policy` — ambos posteriormente realizados como Components plenos com Identity própria (Standards Architecture, Policy Architecture). O próprio Domain Model, contudo, já advertia explicitamente: *"Standard, Policy, Template (...) não são definidos neste documento como componentes concretos — eles aparecem aqui apenas como categorias (...) Sua definição normativa detalhada é papel do Standards Architecture e de documentos subsequentes."* Este documento é esse "documento subsequente", e exerce a prerrogativa já reservada por aquela nota para decidir, com fundamento técnico, como a categoria se realiza.

`[ESCOLHA DE DESIGN]` Template realiza-se como Value Object interno ao Contract, não como Component. Alternativa rejeitada: seguir o precedente de Standard/Policy e dar a Template Identity própria, Coordinate, registro no Registry. Rejeitada pelo **teste funcional de necessidade de identidade** já aplicado implicitamente em toda a base: um conceito merece Identity independente quando (a) é consumido por múltiplos Components não relacionados sob referência estável e versionada, e (b) sua evolução precisa ser rastreável independentemente de qualquer portador específico. `Standard` e `Policy` passam nesse teste — um único Standard é vinculado por centenas de Components através de Namespaces distintos. Um `Template`, por definição, **é sempre autorado para o processo generativo de um Component específico** (o prompt de um Skill, a estrutura de saída de um Agent) — não existe caso de uso institucional em que um Template precise ser descoberto por Capability independentemente de seu portador. Onde reuso entre Templates é necessário (composição, herança), este documento fornece um mecanismo de referência qualificada **sem** exigir Identity própria (§5) — o mesmo padrão já usado por `NormativeRequirement` (`RequirementIdentifier`, Standards §5) e por `Capability` (`#capability/<nome>`, Identity §2.2), ambos Value Objects endereçáveis sem serem Components. Precedente de indústria: no OpenAPI, um `schema` reutilizável vive em `components/schemas` e é referenciado por `$ref` — endereçável, versionado junto ao documento que o contém, mas nunca uma entidade registrada independentemente.

### 1.2 Fronteiras negativas (invioláveis)

| Fronteira | Regra |
|---|---|
| Template não tem Identity | **MUST NOT** ser resolvido pelo Registry; **MUST NOT** ter Coordinate própria |
| Template não define Lifecycle | Segue integralmente o Lifecycle do Manifest que o contém (Kernel §3) |
| Template não decide comportamento | Não é lógica de execução — é estrutura de conteúdo parametrizável, expandida deterministicamente antes de qualquer invocação generativa |
| Template não conhece aplicabilidade | Não sabe quando/para quem se aplica — isso é Policy, exatamente como Standard não conhece Context (Standards §1.1) |
| Template não avalia conformidade | Templates são **alvo** de avaliação (via `applies_to = MANIFEST`), nunca avaliadores |
| Expansão de Template não é o mesmo que Execution do Component portador | Expansão é função pura sobre conteúdo imutável; a Execution subsequente do Skill/Agent que consome o resultado expandido **pode** ser não determinística (ex.: inferência de LLM) — distinção formalizada em §7 |

---

## 2. Objetivos

| # | Objetivo | Motivação |
|---|---|---|
| O1 | Estruturar geração de conteúdo parametrizado (Prompt/Input/Output) de forma verificável | Sem estrutura formal, prompts e formatos de saída são texto livre não auditável, violando Constitution (Documentação como ativo) |
| O2 | Garantir determinismo da expansão, mesmo quando o consumo do resultado não é determinístico | Pré-requisito de Reproducibility (Validation & Certification §6) aplicado à camada de geração |
| O3 | Permitir reuso e composição de fragmentos de Template entre Components | Evitar duplicação de prompts/estruturas equivalentes em dezenas de Skills |
| O4 | Vincular evolução de Template ao versionamento já existente do Component portador | Nenhum esquema de versão paralelo — reuso de SemVer (Kernel §2.11) e Lineage (Identity §7) |
| O5 | Tornar Templates avaliáveis por Standards e restringíveis por Policies sem novo mecanismo | Reuso de `applies_to = MANIFEST` (Standards §4.5) e `scope` (Policy §5.2) |

---

## 3. Escopo

### 3.1 Pertence

Estrutura formal de Template (Prompt/Input/Output); Variable; Placeholder; Parameter Binding; Context Binding; algoritmo de expansão; validação estrutural; herança e composição entre Templates; classificação de mudança (breaking/non-breaking) vinculada ao versionamento do portador; serialização canônica e digest; integração com Manifest.

### 3.2 Não pertence — com justificativa

| Excluído | Justificativa |
|---|---|
| Lógica generativa em si (o que um LLM produz a partir do prompt expandido) | Pertence à Execution do Component portador (Execution §5). Template estrutura a entrada; não é a entrada consumida por um modelo específico nem controla seu comportamento interno |
| Identity, registro, descoberta de Template | Deliberadamente inexistente — §1.1. Templates são descobertos apenas como parte do Manifest de seu portador, via Registry & Discovery §3.1/§6.2 aplicado ao Component |
| Critério normativo sobre o que um Template deve conter | Standards Architecture. Um Standard pode exigir "todo Skill de categoria X declara um Output Template com campo `confidence_score`" — a exigência vive no Standard, nunca no Template |
| Aplicabilidade condicional de exigência sobre Templates | Policy Architecture, via `scope.capabilities`/`component_types` sobre o Component portador |
| Autoridade de aprovação de mudança em Template | Governance §7/§8, herdada integralmente do processo de admissão do Manifest que o contém — nenhum processo paralelo |
| Formato físico de serialização (bytes, encoding de arquivo) | `[LACUNA proposital]`, deferida a Packaging & Distribution Architecture, mesma lacuna já declarada em Standards §3.2 |

---

## 4. Modelo Conceitual

### 4.1 Tabela de proveniência conceitual

| Conceito | Natureza | Base / precedente |
|---|---|---|
| `Template` | **Value Object** interno ao Contract | Padrão de `Phase`/`Step` (Workflow §4), `NormativeRequirement` (Standards §4) |
| `TemplateIdentifier` / `QualifiedTemplateIdentifier` | **Value Object** — identificador local estável | Padrão de `RequirementIdentifier` (Standards §5.1) |
| `Variable` | **Value Object** interno ao Template | — |
| `Placeholder` | **Value Object** interno ao TemplateContent | — |
| `VariableBindingSet` | **Value Object**, produto do algoritmo de binding | — |
| **Expanded Template** | **Artifact** genérico | Mesmo padrão de `Assembly` (Composition §4), `Execution Plan` (Execution §4), `Effective Policy Set` (Policy §9) |
| `Constraint` | **Reutilizado** | Kernel §2.10, para regras de tipo/limite sobre Variable |
| `Capability` | **Reutilizado** | Kernel §2.9, para `binding_source = COMPOSITION_RESOLVED` |
| `Context` / `Context Snapshot` | **Reutilizado** | Domain Model §2 #5; RFC-DM-001 §3.2 — fonte de `binding_source = CONTEXT` |
| `Versioned Identifier` | **Reutilizado** | Identity §4.1, para referência qualificada entre Templates |
| Lifecycle | **Reutilizado sem alteração** | Kernel §3 |
| Detecção de ciclo | **Reutilizado (6ª aplicação)** | Kernel §7 |
| Registro e descoberta do portador | **Reutilizado** | Registry & Discovery §3.1, §6.2 |
| Manifest digest / Integrity | **Reutilizado, aplicado em granularidade fina** | Validation & Certification §6 |

**Nenhum construto exige RFC.** Todos satisfazem o critério formal de Value Object de Identity & Namespace §2.2.

### 4.2 Estrutura formal

```
Template {                                          [Value Object — campo templates[] do Manifest]
  local_id      : TemplateIdentifier                [§5]
  kind          : PROMPT | INPUT | OUTPUT            [§4.3]
  content       : TemplateContent                    (estrutura opaca a este documento —
                                                        texto, JSON schema, ou árvore —
                                                        contendo Placeholders inline)
  variables     : Variable[]
  extends       : QualifiedTemplateIdentifier?       [§6.1]
  includes      : QualifiedTemplateIdentifier[]?     [§6.2]
  deterministic_expansion : boolean                  (MUST ser true — §7)
}

Variable {
  name          : Identifier                         (único no escopo de expansão — §8)
  type          : PrimitiveType | CapabilitySignature | ContextFieldRef
  required      : boolean
  default_value : Literal?
  binding_source: PARAMETER | CONTEXT | COMPOSITION_RESOLVED | LITERAL     [§5.2]
  constraint    : Constraint?                        [Kernel §2.10 — reutilizado]
}

Placeholder {
  variable_ref  : Identifier                         (resolve contra Variable no escopo — §8)
  position      : Opaque                             (detalhe de TemplateContent)
  format_hint   : Text?
}
```

### 4.3 Três espécies de Template

| kind | Papel | Relação com o Component Contract |
|---|---|---|
| `PROMPT` | Conteúdo estruturado alimentado a um processo generativo (ex.: instrução de um Skill/Agent baseado em modelo) | Especializa o **como** interno, nunca os quinze campos universais (Kernel §9) |
| `INPUT` | Estrutura esperada de entrada, com defaults e bindings — refina, sem substituir, o campo `Inputs` do Component Contract (Kernel §2.4) | Camada de parametrização sobre `Inputs` |
| `OUTPUT` | Estrutura esperada do Artifact produzido — refina, sem substituir, o campo `Outputs` (Kernel §2.5) | Camada de parametrização sobre `Outputs` |

`[ESCOLHA DE DESIGN]` Três `kind` nomeados em vez de um único Template genérico com metadado livre. Alternativa rejeitada: `kind` como string livre. Rejeitada porque `Standards §4.5` (`ComplianceTarget.applies_to`) e `Policy §5.2` (`scope`) precisam de um vocabulário fechado e estável para permitir que Standards/Policies direcionem-se especificamente a "todo Output Template de Skills financeiros" — vocabulário aberto tornaria essa segmentação não verificável estruturalmente.

---

## 5. Template Identifier

### 5.1 Estrutura

```
TemplateIdentifier ::= <local-id>
QualifiedTemplateIdentifier ::= <owner-coordinate> "@" <version> "#template." <local-id>
```

Exatamente o mesmo padrão de `RequirementIdentifier` (Standards §5.1) e da qualificação de `Capability` (Identity §2.2, `#capability/<nome>`) — **nenhuma extensão do esquema de identidade é introduzida**. `<local-id>` **MUST** ser único dentro do `templates[]` do Manifest portador. Encoding herda integralmente Identity §4.4.

```
urn:framework-eng:core/skill.code-review@2.1.0#template.prompt.main
```

### 5.2 Fontes de Binding — como Templates recebem parâmetros e Context é injetado

| `binding_source` | Origem do valor | Momento de resolução |
|---|---|---|
| `PARAMETER` | Valor explícito fornecido pelo chamador (ex.: `Step.params` de um Workflow — Workflow §4) | Antes do dispatch |
| `CONTEXT` | Campo de `Context Snapshot` (RFC-DM-001 §3.2) — incluindo os campos de correlação já convencionados por Execution §4 (`orchestration_id`, `phase_id`) | Captura do Context Snapshot, no início da Execution |
| `COMPOSITION_RESOLVED` | Atributo do Coordinate resolvido pela `Assembly` (Composition §5) — ex.: versão exata do modelo subjacente | Resolução da Assembly, antes do dispatch |
| `LITERAL` | `default_value` declarado no próprio Template | Ausência de valor de qualquer outra fonte |

**Regra de precedência de binding (TP1):** quando múltiplas fontes poderiam satisfazer a mesma `Variable`, a ordem de precedência é `PARAMETER > CONTEXT > COMPOSITION_RESOLVED > LITERAL`, estrita e sem exceção. Um valor de fonte de maior precedência **MUST** sempre prevalecer sobre um de menor precedência.

`[ESCOLHA DE DESIGN]` Precedência fixa em vez de configurável por Template. Alternativa rejeitada: permitir que cada Variable declare sua própria ordem de precedência. Rejeitada porque introduziria uma segunda dimensão de configuração que precisaria ser validada individualmente por Variable, sem ganho de expressividade real — a ordem `PARAMETER > CONTEXT > COMPOSITION_RESOLVED > LITERAL` já captura a hierarquia natural de especificidade (uma decisão explícita do chamador sempre deve poder sobrepor um default institucional). Precedente: a mesma lógica de "mais específico vence" já aplicada em Policy §7.2 para resolução de conflito entre Policies.

---

## 6. Herança e Composição

Reutiliza, ao nível de Value Object, exatamente a mesma dualidade `extends`/`includes` já estabelecida para Standards (§6.1-6.2) — a mesma distinção lógica (substituibilidade vs. agregação), aplicada agora a fragmentos de Template em vez de conjuntos de NR.

### 6.1 `extends` — especialização com substituibilidade

Um Template derivado herda `variables[]` e `content` do base e **MAY** adicionar novas Variables e Placeholders. **MUST NOT** remover uma Variable herdada nem torná-la `required` quando o base a declarava opcional com default.

### 6.2 `includes` — composição sem substituibilidade

Incorpora, por referência qualificada, o `content` expandido de outro Template como sub-fragmento — analogia direta a `{% include %}` de sistemas de templating e à composição de módulos já citada em Composition §1. Variables do Template incluído são **qualificadas pela Identity do Template de origem** (mesma técnica de `includes` em Standards §6.2), prevenindo colisão de nome por construção — a menos que o Template composto declare um `alias` explícito para reexpor a Variable em seu próprio escopo.

### 6.3 Aciclicidade

O grafo `extends ∪ includes` **MUST** ser acíclico. **Reutiliza Kernel §7 — 6ª aplicação institucional**, após: dependências de Component, `derives_from` (RFC-DM-001), grafo de fases (Workflow), grafo de Composição (Composition), `extends/includes/replaces` de Standard, cadeia de `overrides` de Policy.

---

## 7. Determinismo e Reprodutibilidade

**Regra fundamental (TP2):** `expand(template, bindings)` **MUST** ser uma função pura — mesmo `template` (conteúdo imutável, parte de Manifest imutável, Kernel §8) e mesmo `VariableBindingSet` **MUST** produzir sempre o mesmo resultado, byte-idêntico.

Consequência direta: **nenhuma Variable pode ser resolvida por leitura de estado mutável no momento da expansão.** Um valor aparentemente "dinâmico" (timestamp corrente, um contador) **MUST** ser modelado como `binding_source = CONTEXT`, capturado **uma única vez** no `Context Snapshot` no início da Execution (RFC-DM-001 §3.2) — nunca lido novamente durante a expansão. Isso estende, para a camada de geração, a mesma garantia de reprodutibilidade que RFC-DM-001 já introduziu para auditoria: o "presente" de uma Execution é congelado no início, não recalculado a cada passo.

`[ESCOLHA DE DESIGN]` Expansão pura, separada da geração subsequente. Alternativa rejeitada: permitir que o próprio processo de expansão invoque um Component gerador (ex.: um Skill de sumarização usado para preencher um Placeholder), tornando a expansão potencialmente não determinística por herança. Rejeitada porque colapsaria a distinção essencial entre "montar a entrada" (mecânico, sempre verificável) e "processar a entrada" (pode ser generativo, sujeito às garantias de Reproducibility específicas de Validation & Certification §6, que já reconhece `deterministic = false` como caso legítimo para Standards — Standards §4.6). Se um Placeholder precisa do resultado de outro Component, esse Component **MUST** ser invocado em uma Execution própria e anterior, cujo Artifact resultante é então injetado como `PARAMETER` — nunca como um efeito colateral oculto dentro da expansão. Precedente: separação entre "template rendering" (Jinja2, Mustache — deliberadamente sem I/O) e "lógica de aplicação" em toda a tradição de sistemas de templating.

---

## 8. Prevenção de Ambiguidade

**Regra (TP3):** dentro do escopo de expansão de um Template — seu próprio `variables[]`, mais o fecho transitivo de `extends`, mais as Variables qualificadas de `includes` (ou explicitamente reexpostas por `alias`) — **MUST NOT** existir dois Variables de mesmo nome não qualificado.

Detectável estruturalmente na validação (§10, invariante K3), nunca em tempo de expansão — mesma disciplina de "falhar cedo" já estabelecida em Standards §12.1 (linha 6-8, colisão de RID) e Policy §11.4.

---

## 9. Modelo Operacional

**Serviço:** `Template Resolution Service` — substrato institucional, mesma classe de `Standard Resolution Service` (Standards §10) e `Policy Evaluation Service` (Policy §10). Não é Component, não tem Lifecycle, não escreve em lugar algum.

```
resolve_effective_template(template_ref: QualifiedTemplateIdentifier)
    → EffectiveTemplate | TemplateError
  PRE:  template_ref.owner resolve via Registry (Registry §6.1) a lifecycle_state ∈ {Active, Deprecated}
  POST: fecho transitivo de variables/content sobre extends ∪ includes,
        deduplicado, resolvido por não-enfraquecimento (§6.1)
  INV:  determinístico — mesma entrada produz sempre a mesma saída

bind_variables(effective_template, params, context_snapshot, assembly)
    → VariableBindingSet | BindingError
  PRE:  todo Variable required sem default tem fonte disponível conforme §5.2
  POST: um valor único por Variable, resolvido pela ordem de precedência TP1

expand(effective_template, bindings) → ExpandedTemplate (Artifact)
  PRE:  todo Placeholder resolve a um Variable com valor em bindings
  POST: Artifact imutável, byte-determinístico (TP2)

validate_template_definition(manifest) → ValidationResult
  PRE:  manifest contém templates[]
  POST: ver §10.1 (invariantes K1-K7)

classify_template_change(prev_manifest, next_manifest, local_id) → MAJOR | MINOR | PATCH | INVALID
  PRE:  ambos pertencem à mesma lineage de Manifest (RFC-DM-001 §3.6)
```

### 9.1 Invariantes verificados na validação

| # | Invariante |
|---|---|
| K1 | Todo `Placeholder.variable_ref` resolve a um `Variable` declarado no escopo (próprio, herdado ou incluído/aliased) |
| K2 | Todo `Variable` com `required = true` e sem `default_value` declara `binding_source` resolvível estruturalmente |
| K3 | Nenhuma colisão de nome não qualificado no escopo de expansão (§8) |
| K4 | Grafo `extends ∪ includes` acíclico (Kernel §7, 6ª aplicação) |
| K5 | `extends` não remove nem torna `required` uma Variable antes opcional |
| K6 | `includes` não modifica Variables do Template incluído |
| K7 | `deterministic_expansion = true` para todo Template — nenhuma exceção admitida (TP2) |

---

## 10. Diagramas

### 10.1 UML simplificado

```
┌─────────────────────────────┐
│ Manifest (do Component portador) │  [Kernel §9 — conteúdo interno type-specific]
│  templates[] ────────────────┼──┐
└──────────────────────────────┘  │
                                    │1..*
                                    ▼
                          ┌──────────────────────┐
                          │ Template  «VO»        │
                          │  local_id             │
                          │  kind: PROMPT|INPUT|  │
                          │        OUTPUT         │
                          │  deterministic:true   │
                          └──┬──────────┬─────────┘
                     extends │          │ includes
                             ▼          ▼
                  (QualifiedTemplateIdentifier — grafo acíclico, Kernel §7)
                             │
                    1..*     ▼
              ┌───────────────────┐        ┌────────────────────┐
              │ Variable «VO»      │◄───────┤ Placeholder «VO»    │
              │  binding_source ───┼──►     │  variable_ref       │
              │  constraint ───────┼──► Constraint [Kernel §2.10] │
              └───────────────────┘        └────────────────────┘
```

### 10.2 Sequência — expansão completa

```
Executor       TemplateResolver      Registry      StandardResolver     ExpandedTemplate(Artifact)
   │                  │                  │                │                     │
   ├─resolve_effective_template(ref)────►│                │                     │
   │                  ├─resolve(owner)──►│                │                     │
   │                  │◄─ResolvedIdentity┤                │                     │
   │                  ├─Kernel§7.CycleDetection (6ª aplicação)                  │
   │                  ├─merge extends/includes, não-enfraquecimento             │
   │◄─EffectiveTemplate│                                                        │
   │                  │                                                        │
   ├─bind_variables(params, ctx_snapshot, assembly) ─────────────────────────►  │
   │  (RFC-DM-001 §3.2: ctx_snapshot já capturado no Initiated da Execution)    │
   │◄─VariableBindingSet (ordem TP1: PARAMETER>CONTEXT>COMPOSITION>LITERAL)     │
   │                                                                            │
   ├─expand(effective_template, bindings) ────────────────────────────────────►│
   │◄─ExpandedTemplate (Artifact imutável, byte-determinístico — TP2) ─────────┤
   │
   │  [expansão termina aqui — a Execution do Skill/Agent que CONSOME o
   │   ExpandedTemplate é um passo subsequente, potencialmente não determinístico]
```

### 10.3 Estados

Template **não possui máquina de estados própria**. Segue o Lifecycle do Manifest que o contém (Kernel §3), projetado no Registry via Registry & Discovery §7.3 sobre o Component portador. Reproduzir isto seria duplicação — proibida pela Restrição Arquitetural 3 do mandato.

---

## 11. Algoritmos

### 11.1 Resolução de Template efetivo

```
ALGORITMO ResolveEffectiveTemplate(template_ref):
  ENTRADA: template_ref : QualifiedTemplateIdentifier
  SAÍDA:   EffectiveTemplate | TemplateError

  1  owner_entry ← Registry.resolve(template_ref.owner)          # Registry §6.1
  2  SE owner_entry.lifecycle_state ∉ {Active, Deprecated}:
  3     RETORNA TemplateError(OWNER_NOT_BINDABLE)
  4
  5  graph ← BuildReferenceGraph(template_ref, arestas = {extends, includes})
  6  SE Kernel§7.CycleDetection(graph) detecta ciclo:
  7     RETORNA TemplateError(CYCLIC_TEMPLATE_GRAPH)              # K4
  8
  9  vars ← OrderedMap()
 10  PARA CADA node EM TopologicalOrder(graph) invertida:
 11     PARA CADA v EM node.variables:
 12        qname ← SE EdgeKind(node) = INCLUDES: Qualify(v.name, node.owner) SENÃO v.name
 13        SE qname ∈ vars:
 14           SE EdgeKind(node) = INCLUDES: RETORNA TemplateError(ILLEGAL_MODIFY_IN_INCLUDES)   # K6
 15           SE v.required ∧ ¬vars[qname].required:
 16              RETORNA TemplateError(ILLEGAL_REQUIREMENT_STRENGTHENING)                        # K5
 17        vars[qname] ← v
 18
 19  ASSERT Unique(qname PARA qname EM vars)                       # K3
 20  RETORNA EffectiveTemplate(content = MergeContent(graph), variables = vars)
```

### 11.2 Binding de variáveis

```
ALGORITMO BindVariables(effective_template, params, ctx_snapshot, assembly):
  bindings ← Map()
  PARA CADA v EM effective_template.variables:
     valor ← ausente
     SE v.name ∈ params:                        valor ← params[v.name]          # PARAMETER
     SENÃO SE v.binding_source = CONTEXT:        valor ← ctx_snapshot[v.name]     # CONTEXT
     SENÃO SE v.binding_source = COMPOSITION_RESOLVED: valor ← assembly[v.name]   # COMPOSITION_RESOLVED
     SENÃO SE v.default_value ≠ null:            valor ← v.default_value          # LITERAL
     SE valor = ausente ∧ v.required:
        RETORNA BindingError(REQUIRED_VARIABLE_UNBOUND, v.name)                    # K2
     SE valor ≠ ausente:
        ASSERT Satisfies(valor, v.constraint)     # Kernel §2.10
        bindings[v.name] ← valor
  RETORNA VariableBindingSet(bindings)
```

### 11.3 Expansão

```
ALGORITMO Expand(effective_template, bindings):
  PARA CADA p EM effective_template.content.placeholders:
     ASSERT p.variable_ref ∈ bindings                              # K1
  resultado ← RenderMecanico(effective_template.content, bindings) # função pura — TP2
  RETORNA Artifact(ExpandedTemplate, {
     content: resultado,
     template_ref: effective_template.qualified_id,
     bindings_digest: Digest(bindings)          # §12
  })
  # TERMINAÇÃO: content é finito e imutável; nenhuma iteração não limitada
  # DETERMINISMO: RenderMecanico é substituição sintática pura, sem I/O (§7)
```

### 11.4 Classificação de mudança (breaking/non-breaking)

```
ALGORITMO ClassifyTemplateChange(prev, next, local_id):
  pv ← prev.templates[local_id] ; nv ← next.templates[local_id]
  SE pv = null: RETORNA MINOR                                 # novo Template no Manifest
  SE nv = null: RETORNA MAJOR                                 # Template removido

  PARA CADA v EM pv.variables:
     nv_v ← nv.variables[v.name]
     SE nv_v = null:                                    RETORNA MAJOR   # variável removida
     SE v.required = false ∧ nv_v.required = true:       RETORNA MAJOR   # exigência endurecida
     SE ¬TypeCompatible(nv_v.type, v.type):               RETORNA MAJOR   # tipo estreitado
  PARA CADA v EM nv.variables:
     SE v ∉ pv.variables ∧ v.required ∧ v.default_value = null:
                                                            RETORNA MAJOR   # nova exigência obrigatória sem default
     SE v ∉ pv.variables:                                  RETORNA MINOR   # nova variável opcional
  SE ContentChangedSemantically(pv.content, nv.content):    RETORNA MINOR   # conteúdo evolui, contrato estável
  RETORNA PATCH
```

**Uso normativo:** resultado **MUST** ser consistente com a classificação de versão já exigida para o Manifest inteiro pelo mecanismo geral de Breaking Change (Governance §10) — mesmo padrão de verificação já estabelecido por `ClassifyStandardChange` (Standards §12.2).

---

## 12. Serialização, Digest e Cache

**Serialização canônica** herda integralmente Identity & Namespace §4.4 (charset DNS-safe para identificadores; conteúdo estruturado serializado de forma determinística — mesma ordem de campos, sem espaço em branco não significativo) — nenhuma regra nova de encoding.

**`template_digest`:** hash sobre a serialização canônica de um `Template` — aplicação em granularidade fina do mesmo `manifest_digest` já definido em Validation & Certification §6 para Integrity. Como o Manifest portador é imutável uma vez `Active` (Kernel §8), `template_digest` é permanentemente estável para uma dada versão.

**Cache:** `expand()` é **integralmente cacheável com validade indefinida** pela chave `(template_digest, bindings_digest)` — prova de correção idêntica à já estabelecida em Standards §15.1: ambos os componentes da chave são, por construção, imutáveis (Manifest imutável; `Context Snapshot` imutável, RFC-DM-001 §3.2). Nenhuma política nova de cache é introduzida — mesma regra de Registry & Discovery §8 (cache indefinido para resolução de Versioned Identifier).

---

## 13. Integrações

| Documento base | Contrato de integração |
|---|---|
| **Constitution** | Determinismo obrigatório (TP2) realiza "Confiança verificável"; digest granular realiza "Auditabilidade" |
| **Kernel** | Template habilitado por §9 (Extension Model), mesma classe de `Phase`/`Step`; `Constraint` (§2.10) e `Capability` (§2.9) reutilizados; §7 reaplicado (6ª vez); §2.4/§2.5 (`Inputs`/`Outputs`) são refinados, nunca substituídos, por `INPUT`/`OUTPUT` Templates |
| **Governance** | Mudança em Template segue o processo de admissão/aprovação do Manifest portador (§7/§8), sem processo paralelo; Breaking Change (§10) consome `ClassifyTemplateChange` |
| **Domain Model v1.1.0** | Zero entidades, relações, estados novos. `Expanded Template` = `Artifact` genérico (§2 #7); produzido por uma `Execution` via `produces` já existente |
| **RFC-DM-001** | `Context Snapshot` (§3.2) é a única fonte válida de `binding_source = CONTEXT` — garante determinismo (§7); cardinalidade `Component 1:1..* Manifest` (§3.6) é a base da lineage que ancora `ClassifyTemplateChange` |
| **Identity & Namespace** | `QualifiedTemplateIdentifier` usa a forma canônica com fragmento `#template.` — mesmo padrão de `#capability/` (§2.2) e `#nr.` (Standards §5.1); nenhum esquema novo |
| **Registry & Discovery** | Templates **MUST NOT** ser registrados independentemente (§1.2); descoberta ocorre exclusivamente via o Component portador |
| **Validation & Certification** | `template_digest` especializa `manifest_digest` (§6); `deterministic_expansion` é pré-requisito estrutural para que o portador atinja L4 (Reproducibility) |
| **Composition** | `binding_source = COMPOSITION_RESOLVED` consome diretamente a `Assembly` (Composition §5) |
| **Workflow** | Um `Step` (Workflow §4) fornece `PARAMETER` bindings ao Template do Provider resolvido; `GATE_AUTO` **MAY** validar `ExpandedTemplate` como Evidence |
| **Execution** | `bind_variables`/`expand` ocorrem entre `Initiated` e `Running` da Execution que consome o Template, após a captura do `Context Snapshot` — nunca antes, nunca depois |
| **Standards** | `applies_to = MANIFEST` já cobre avaliação de Template como conteúdo do Manifest — nenhum novo valor de `ComplianceTarget.applies_to` é necessário |
| **Policy** | `scope.capabilities`/`component_types` sobre o Component portador restringe indiretamente quais Templates estão sob determinada exigência — nenhum mecanismo de escopo específico de Template é introduzido |

---

## 14. Casos Extremos

| # | Caso | Tratamento |
|---|---|---|
| G1 | Ciclo em `extends`/`includes` | `TemplateError(CYCLIC_TEMPLATE_GRAPH)` — Kernel §7, 6ª aplicação (K4) |
| G2 | `extends` que endurece exigência de Variable opcional | `TemplateError(ILLEGAL_REQUIREMENT_STRENGTHENING)` (K5) |
| G3 | `includes` que tenta modificar Variable incluída | `TemplateError(ILLEGAL_MODIFY_IN_INCLUDES)` (K6) |
| G4 | Colisão de nome de Variable não qualificado | Rejeitado na validação (K3, §8) |
| G5 | Variable `required` sem fonte de binding disponível em runtime | `BindingError(REQUIRED_VARIABLE_UNBOUND)` — a Execution **MUST NOT** prosseguir para `Running` sem binding completo (K2) |
| G6 | Placeholder referenciando Variable inexistente | Rejeitado na validação (K1) |
| G7 | Tentativa de Variable resolvida por leitura de estado mutável na expansão | Impossível por construção — `binding_source` é enum fechado (§5.2); qualquer valor "dinâmico" **MUST** passar por `CONTEXT`, capturado no Context Snapshot (TP2) |
| G8 | Template referenciando portador em `Archived`/`Removed` | Resolução retorna Tombstone (Registry §6.1); `TemplateError(OWNER_NOT_BINDABLE)` — mesma semântica de Standards §7.4/E9 |
| G9 | Template referenciando portador em `Deprecated` | Resolução sucede com aviso — mesma semântica de Standards E8 |
| G10 | `ClassifyTemplateChange` discorda da versão declarada no Manifest | Bloqueia saída de `Draft` — mesmo mecanismo de `I13` (Standards §10.3) aplicado à granularidade de Template |
| G11 | Duas Executions concorrentes expandindo o mesmo Template com bindings distintos | Seguro por construção — `expand()` é função pura sem estado compartilhado; cada `ExpandedTemplate` é Artifact independente e imutável |
| G12 | Template composto por `includes` profundamente encadeado | `[DÍVIDA TÉCNICA reconhecida]`, mesma classe de trade-off já assumida em Standards §15.3 para `extends` profundo — sem limite normativo de profundidade nesta versão |
| G13 | Policy `BLOCKING` restringe a Capability de um Skill cujo Template dependeria de `COMPOSITION_RESOLVED` sobre essa Capability | A resolução de Assembly falha antes de `bind_variables` ser alcançado (Composition §9, `SlotUnsatisfied`) — Template nunca chega a ser avaliado; comportamento em cascata correto, sem necessidade de tratamento especial aqui |

---

## 15. Performance

**Cache:** ver §12 — indefinido por `(template_digest, bindings_digest)`, mesma prova de correção de Standards §15.1.

**Complexidade:**

| Operação | Complexidade |
|---|---|
| `ResolveEffectiveTemplate` | O(V + E + R log R), mesma ordem de `ResolveEffectiveRequirements` (Standards §15.2) |
| `BindVariables` | O(Vars) |
| `Expand` | O(\|content\| + Placeholders) |
| `ClassifyTemplateChange` | O(Vars) |

**Trade-off explícito:** expansão ocorre no caminho quente de toda Execution que consome um Template (potencialmente o volume mais alto do Framework, per Domain Model §4.5). A garantia de cache indefinido (§12) é o que torna esse custo amortizável — a primeira expansão para um dado par `(template_digest, bindings_digest)` paga o custo total; toda repetição é leitura de cache. Nenhum mecanismo de escala adicional é necessário além do já normatizado.

---

## 16. Eventos

Telemetria de substrato — mesma classe de `Standard Event` (Standards §16) e `Policy Event` (Policy §16). Não são Event Entities do Domain Model.

| Evento | Emitido quando |
|---|---|
| `TemplateDefinitionValidated` | `validate_template_definition` retorna OK |
| `TemplateDefinitionRejected(invariant)` | Qualquer K1–K7 violado |
| `EffectiveTemplateResolved(qualified_id)` | Resolução bem-sucedida |
| `CyclicTemplateGraphDetected` | Violação de K4 |
| `RequiredVariableUnbound(qualified_id, variable)` | §11.2, binding falho |
| `TemplateExpanded(qualified_id, bindings_digest)` | Expansão bem-sucedida |
| `TemplateChangeClassified(local_id, class)` | `ClassifyTemplateChange` executado |
| `OwnerNotBindableReferenced(qualified_id)` | G8 |

---

## 17. Regras Normativas (RFC 2119)

| # | Regra | Nível |
|---|---|---|
| **TP1** | Precedência de binding MUST seguir `PARAMETER > CONTEXT > COMPOSITION_RESOLVED > LITERAL`, sem exceção | MUST |
| **TP2** | `expand()` MUST ser função pura; MUST NOT ler estado mutável durante a expansão | MUST / MUST NOT |
| **TP3** | Escopo de expansão MUST NOT conter dois Variables de mesmo nome não qualificado | MUST NOT |
| **TP4** | Template MUST NOT ter Identity, Coordinate ou registro independentes | MUST NOT |
| **TP5** | Referência entre Templates MUST usar Qualified Template Identifier, nunca nome livre | MUST |
| **TP6** | `extends` MUST NOT remover Variable herdada nem endurecer sua exigência | MUST NOT |
| **TP7** | `includes` MUST NOT modificar Variable do Template incluído | MUST NOT |
| **TP8** | Grafo `extends ∪ includes` MUST ser acíclico (Kernel §7) | MUST |
| **TP9** | Valor "dinâmico" de Variable MUST ser modelado via `binding_source = CONTEXT`, capturado no Context Snapshot | MUST |
| **TP10** | Todo Template MUST declarar `deterministic_expansion = true` | MUST |
| **TP11** | `ExpandedTemplate` MUST ser imutável | MUST |
| **TP12** | Classificação de mudança declarada MUST ser consistente com `ClassifyTemplateChange` | MUST |
| **TP13** | Expansão MAY ser cacheada indefinidamente por `(template_digest, bindings_digest)` | MAY |
| **TP14** | Variable `required` sem `default_value` MUST declarar `binding_source` estruturalmente resolvível | MUST |
| **TP15** | Template MUST NOT definir critério normativo nem condição de aplicabilidade | MUST NOT |

---

## 18. Validação Institucional

| Documento base | Resultado | Evidência |
|---|---|---|
| Constitution | **PASS** | TP2/TP10 realizam Confiança verificável; digest granular realiza Auditabilidade |
| Kernel | **PASS** | Habilitado por §9; §2.4/§2.5/§2.9/§2.10/§7 reutilizados sem modificação |
| Governance | **PASS** | Nenhuma autoridade nova; §7/§8/§10 delegados integralmente |
| Domain Model v1.1.0 | **PASS** | Zero entidades/relações/estados. Template = Value Object; ExpandedTemplate = Artifact genérico |
| RFC-DM-001 | **PASS** | Context Snapshot (§3.2) é fonte exclusiva de CONTEXT binding (TP9); §3.6 ancora lineage |
| Identity & Namespace | **PASS** | Qualified Template Identifier segue exatamente o padrão de fragmento já estabelecido (§2.2) |
| Registry & Discovery | **PASS** | TP4 garante ausência de registro paralelo |
| Validation & Certification | **PASS** | `template_digest` especializa `manifest_digest` (§6); determinismo é pré-requisito de L4 |
| Composition | **PASS** | `COMPOSITION_RESOLVED` consome Assembly (§5) sem alteração |
| Workflow | **PASS** | Step fornece PARAMETER bindings; GATE_AUTO pode consumir ExpandedTemplate como Evidence |
| Execution | **PASS** | Expansão ocorre entre Initiated e Running, após Context Snapshot |
| Standards | **PASS** | `applies_to = MANIFEST` cobre Template sem novo valor de enum |
| Policy | **PASS** | `scope` sobre o portador restringe indiretamente; nenhum mecanismo de escopo próprio |
| **Exige RFC?** | **NÃO** | — |

### 18.1 Checklist de Conformidade Institucional

| Restrição do mandato | Status |
|---|---|
| Zero entidades novas no Domain Model | ✔ |
| Zero relações novas | ✔ |
| Zero Lifecycle novo | ✔ (§10.3) |
| Nenhum documento anterior alterado | ✔ — confirmado item a item na tabela acima |
| Nenhuma RFC nova | ✔ |
| Template sem Identity própria, sem Component-hood | ✔ (§1.1, TP4) |
| Reutilização de Artifact/Context/Constraint/Capability/Versioned Identifier/Manifest/Contract | ✔ — todos citados nominalmente em §4.1 e §13 |
| Algoritmos determinísticos | ✔ — prova de pureza em §7, TP2 |
| Integração completa com Composition, Workflow, Execution, Standards, Policy | ✔ — §13, tabela completa |

---

## 19. Dependências Futuras

| Consumidor | O que consome | Estado |
|---|---|---|
| **Skill Architecture** (próximo documento) | `Template` como conteúdo do Manifest de um Skill; `INPUT`/`OUTPUT` Templates como refinamento de `Inputs`/`Outputs`; `template_digest` para Integrity de Skills | **Desbloqueado** |
| **Agent Architecture** | `PROMPT` Templates como estrutura de instrução; `COMPOSITION_RESOLVED` para vincular Template à versão exata do modelo subjacente resolvido pela Assembly | Desbloqueado, sem alteração deste documento |
| **Workflow Architecture** (já ratificado) | Nenhuma alteração — `Step.params` já era o mecanismo de `PARAMETER` binding; este documento apenas formaliza o lado receptor | Consumo retroativo sem impacto |
| **Testing Architecture** | Geração de casos de teste a partir de `Variable.type`/`constraint` declarados | `[LACUNA proposital]` |
| **Packaging & Distribution Architecture** | Serialização física e transporte de Templates como parte do Manifest empacotado | `[LACUNA proposital]` já declarada em Standards §3.2 |

---

# Critério de Aceitação

## ✔ Checklist Completo de Conformidade Institucional
Ver §18.1 — todas as oito verificações **PASS**.

## ✔ Evidência de Reutilização de Todos os Documentos-Base

| Documento | Conceito reutilizado neste documento |
|---|---|
| Constitution | Confiança verificável, Auditabilidade, fricção proporcional ao risco |
| Kernel | Extension Model (§9), `Constraint` (§2.10), `Capability` (§2.9), `Inputs`/`Outputs` (§2.4/§2.5), Cycle Detection (§7, 6ª aplicação), Lifecycle (§3) |
| Governance | Admissão/aprovação (§7/§8), Breaking Change (§10) |
| Domain Model v1.1.0 | `Artifact` genérico, `Execution.produces` |
| RFC-DM-001 | `Context Snapshot` (§3.2), cardinalidade de Manifest (§3.6) |
| Identity & Namespace | Padrão de qualificação por fragmento (§2.2), encoding (§4.4) |
| Registry & Discovery | Resolução do portador (§6.1) |
| Validation & Certification | `manifest_digest`/Integrity (§6), Reproducibility |
| Composition | `Assembly` (§5) como fonte de `COMPOSITION_RESOLVED` |
| Workflow | `Step.params` como fonte de `PARAMETER` |
| Execution | Sequência Initiated→Context Snapshot→Running (§5) |
| Standards | Padrão `RequirementIdentifier` (§5.1), `applies_to=MANIFEST` (§4.5) |
| Policy | Padrão `scope` sobre portador (§5.2) |

## ✔ Confirmação Explícita
**Nenhum documento da base normativa foi alterado.** Todo conceito introduzido é Value Object interno ao Contract (habilitado por Kernel §9, já vigente) ou `Artifact` genérico (já vigente em Domain Model §2). Nenhuma entidade, relação, estado ou autoridade nova foi criada.

## ✔ Dependências Desbloqueadas para Skill Architecture
Skill Architecture pode agora especificar, sem qualquer conceito pendente: como um Skill declara seus `INPUT`/`OUTPUT` Templates refinando `Inputs`/`Outputs` do Kernel Contract; como um `PROMPT` Template estrutura a instrução consumida por sua Execution; como `template_digest` participa da Integrity exigida por Certification L4; e como Standards/Policies já vigentes restringem Skills por `component_types`/`capabilities` sem exigir nenhum mecanismo novo. **Nenhuma dependência pendente permanece entre Template Architecture e Skill Architecture.**
