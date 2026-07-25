# RFC-COMP-001 — Component Assembly Contract

### Framework Eng — Fechamento da Lacuna de `resolve_assembly(component_coordinate)`

**Status:** Proposed — redigida para ratificação pelo Framework Council per Governance Architecture §8-9 (esta RFC não se autorratifica; é o artefato submetido àquele processo).
**Target document:** Composition Architecture v1.0.0
**Resulting version:** Composition Architecture v1.1.0 (minor — puramente aditiva, ver §6-§7)
**Origem do achado:** Runtime Gap Analysis v1.0 (`docs/runtime-gap-analysis.md`, §3.1 e §7), produzida após implementação completa e execução real do Runtime contra dado institucional certificado.

> Todo o corpus normativo anterior — Constitution, Kernel, Governance, Domain Model v1.1.0, RFC-DM-001, Identity & Namespace, Registry & Discovery, Validation & Certification, Composition Architecture, Workflow Architecture, Execution Architecture, Standards Architecture, Policy Architecture, Template Architecture e Skill Architecture — é tratado aqui como **congelado**. Nenhuma linha de nenhum desses documentos é alterada por esta RFC. O que se corrige é uma lacuna de especificação em Composition Architecture, fechada de forma estritamente aditiva.

---

## 1. Motivação

Composition Architecture §5 contrata:

```
resolve_assembly(component_coordinate) → Assembly | CompositionError
  PRE:  component_coordinate está em lifecycle_state ∈ {Approved, Active}
  POST: Assembly é um Artifact imutável, produzido por uma Execution do Resolver,
        referenciando exatamente um Coordinate resolvido por Slot (ou erro nomeado)
```

Esta é uma operação de topo — resolve **todos** os Slots de um Component, não um único Slot isolado (essa segunda operação já está inteiramente especificada em §7, `ALGORITMO ResolveSlot(slot, requester_ns)`). Sem `resolve_assembly` implementável, um Component genérico nunca pode ter sua Assembly completa resolvida de uma só vez — apenas Slot a Slot, manualmente, por quem já sabe de antemão quais Slots existem.

O Runtime Gap Analysis (produzido após a implementação e execução real do Runtime contra o Manifest certificado `core/skill.static-analysis.code-review@1.0.0`) confirmou isso na prática: `resolve_assembly` nunca foi implementado como função autônoma — apenas `resolve_slot`, chamado sempre com um único Slot já fornecido externamente por um `Step` de Workflow. Nenhum caminho de código jamais perguntou "quais são os Slots deste Component?" de forma genérica, porque não há onde essa pergunta seria respondida para um Component qualquer.

---

## 2. Problema

`Slot` (Composition §4) é um Value Object bem definido — estrutura, campos, semântica de cada um, tudo especificado sem ambiguidade. O problema não é a definição de `Slot`. O problema é **onde `Slot[]` vive** quando o dono é um Component genérico, não um Workflow.

Hoje, apenas um lugar do corpus normativo declara, concretamente, onde um `Slot` mora:

> Workflow Architecture §4: `Step { id, slot: CompositionSlot, kind, failure_policy, timeout, compensated_by }`

Nenhum outro documento — nem Kernel §2 (os quinze campos do Component Contract), nem Composition §4 (a própria definição de `Slot`) — declara um campo, seção ou convenção pela qual um Component **arbitrário** (não um Workflow) exponha os Slots que ele próprio precisa resolver.

Consequência direta: `resolve_assembly(component_coordinate)`, tal como contratado, tem uma PRE e uma POST bem definidas, mas **nenhuma fonte declarada de onde ler seu próprio insumo** (os Slots do Component referenciado por `component_coordinate`) quando esse Component não é um Workflow.

---

## 3. Prova da Inconsistência

Prova por ausência, verificada exaustivamente contra os quinze documentos congelados:

| Documento | O que declara sobre `Slot[]` de um Component genérico | Resultado |
|---|---|---|
| Kernel Architecture §2 | Quinze campos do Component Contract — nenhum chamado `slots` ou equivalente | Ausente |
| Kernel Architecture §9 | Extension Model: autoriza conteúdo interno *type-specific* dentro do Contract (o "como"), sem enumerar quais tipos existirão — mecanismo, não instância | Habilita, não declara |
| Composition Architecture §4 | Define a estrutura de `Slot` — nunca declara onde um Component guarda a *lista* de seus próprios Slots | Ausente |
| Composition Architecture §5 | Contrata `resolve_assembly(component_coordinate)` — PRE/POST não mencionam a fonte de `Slot[]` | Lacuna confirmada |
| Composition Architecture §7 | `ALGORITMO ResolveSlot(slot, requester_ns)` — recebe um **único** `slot` já dado; não itera sobre uma coleção de Slots de um Component | Não cobre o caso de topo |
| Workflow Architecture §4 | `Step.slot` — único lugar do corpus com um Slot concretamente ancorado a uma estrutura declarada | Único caso resolvido, e só para Workflow |
| Skill Architecture §4.1 | Tabela de proveniência: Skill **consome** `Slot`/`Assembly` (Composition §5-§7) como candidato elegível, mas **nunca declara Slots de si própria** — Skill é o alvo de uma resolução, não a origem de uma | Confirma que nem todo tipo tem Slots próprios |

**Conclusão da prova:** a lacuna é real, verificável e não decorre de leitura incompleta — é uma ausência objetiva, confirmada por execução real do Runtime (nenhuma chamada a `resolve_assembly` foi jamais possível de forma genérica).

---

## 4. Solução Mínima

Introduz-se **um único mecanismo de dispatch**, sem conteúdo algorítmico próprio: `EnumerateSlots(component)`.

```
EnumerateSlots(component: ResolvedManifest) → Slot[]
```

**Isto não é um novo algoritmo.** É um nome dado a uma leitura de campo já autorizada pelo Kernel §9 Extension Model — exatamente o mesmo tipo de operação que já existe, sem nome próprio, em todo o corpus: ler `manifest.templates[]` (Template Architecture §4.2) não é tratado como um algoritmo; ler `Phase.steps[].slot` também não deveria ser. `EnumerateSlots` apenas **nomeia** essa leitura para que Composition §5 tenha, formalmente, algo a chamar.

**Regra central (a única regra nova desta RFC):**

> `EnumerateSlots(component)` é definida **pelo próprio tipo especializado do Component**, nunca por Composition Architecture. Composition invoca `EnumerateSlots` como uma capacidade opaca do tipo, exatamente como já invoca `search()` do Registry sem conhecer o índice interno do Registry (Composition §8, "Registry: fonte exclusiva de candidatos").

Instanciações concretas — **nenhuma delas exige mudança em documento algum**, porque cada uma é apenas a leitura de uma estrutura que já existe:

| Tipo de Component | `EnumerateSlots(component)` lê | Documento que já declara essa estrutura |
|---|---|---|
| `Workflow` | `{ step.slot : step ∈ all_steps(component.phases), step.slot ≠ null }` | Workflow Architecture §4 (`Step.slot`) — **já existe, nenhuma mudança** |
| `Skill` | `∅` (conjunto vazio) — Skill nunca declarou estrutura interna portadora de Slot (§4.1, tabela de proveniência) | Skill Architecture — **já existe, nenhuma mudança** |
| `Standard`, `Policy`, `Template` | `∅` — nenhum destes documentos declara Slot interno | Cada respectivo documento — **nenhuma mudança** |
| `Agent` (documento futuro) | O que quer que Agent Architecture venha a declarar (ex.: `Action.slot`, por analogia direta a `Step.slot`) | A ser definido **por aquele documento, quando escrito** — não por esta RFC |

O caso "tipo futuro ainda não escrito" não é uma lacuna desta RFC: é exatamente o mesmo padrão de extensibilidade que já rege todo o Kernel §9 — o Kernel nunca precisou saber, com antecedência, quais tipos de Component existiriam em cinco anos, porque valida *forma*, não uma lista fechada de tipos. `EnumerateSlots` aplica esse mesmo princípio a um caso concreto: Composition nunca precisa saber quais tipos declaram Slot, porque a resposta pertence a cada tipo, não a Composition.

---

## 5. Integração com Composition

`resolve_assembly(component_coordinate)` passa a ter uma definição operacional completa, sem alterar sua PRE/POST já ratificada:

```
resolve_assembly(component_coordinate) → Assembly | CompositionError
  1. resolved ← Registry.resolve(component_coordinate)          # Registry §6.1 — inalterado
  2. slots ← EnumerateSlots(resolved.manifest)                  # NOVO — dispatch por component_type
  3. PARA CADA slot EM slots:
       resultado[slot] ← ResolveSlot(slot, requester_ns)        # Composition §7 — inalterado, verbatim
  4. RETORNA Assembly(resolved_slots = resultado)                # Assembly (§4) — inalterado
```

Nenhuma linha de `ResolveSlot` (§7) muda. Nenhum campo de `Assembly` (§4) muda. O único elemento novo é o passo 2, que é uma leitura, não uma decisão — `EnumerateSlots` nunca filtra, nunca seleciona, nunca resolve versão ou certificação; apenas devolve a lista de Slots que já existia, declarada em outro lugar.

`[ESCOLHA DE DESIGN]` `EnumerateSlots` como dispatch opaco por `component_type`, em vez de Composition Architecture enumerar, ela própria, "se Workflow então X, se Agent então Y". Alternativa rejeitada: um `if/else` dentro de Composition Architecture testando o tipo do Component. Rejeitada porque violaria a fronteira que a própria Composition §1 já estabelece — *"Composition nunca conhece a estrutura interna"* dos tipos que orquestra — e obrigaria Composition Architecture a ser reaberta toda vez que um novo tipo especializado (Agent, e outros ainda não escritos) precisasse declarar seus próprios Slots. O padrão correto, já usado em todo o corpus para esse exato problema, é o mesmo de Kernel §9: quem sabe *o quê* (o tipo especializado) responde a operação; quem sabe *que a operação existe* (Composition) apenas a invoca.

---

## 6. Compatibilidade Retroativa

**Alegação formal: esta RFC não introduz nenhuma mudança quebra-compatibilidade.**

- O Runtime Gap Analysis confirma que `resolve_assembly(component_coordinate)` nunca foi invocado como operação autônoma por nenhum código existente — não há Consumer algum dependendo do comportamento atual (ausência de implementação), porque não havia comportamento algum a que se apegar.
- Nenhuma `Assembly`, `Slot` ou resolução já produzida por `ResolveSlot` (§7) é afetada — o algoritmo de resolução por Slot individual é reutilizado sem qualquer alteração de assinatura, ordem ou semântica.
- Para `Workflow`, `EnumerateSlots` apenas nomeia uma leitura sobre um campo (`Step.slot`) que já existe e já é populado exatamente da mesma forma antes e depois desta RFC.
- Para qualquer outro tipo já ratificado (Skill, Standard, Policy, Template), `EnumerateSlots` retorna o conjunto vazio — o mesmo resultado que a ausência total de mecanismo já produzia implicitamente (nenhum desses tipos jamais teve Slots próprios resolvidos).

Migração, portanto, é vácua — mesmo padrão formal já usado em RFC-DM-001 §6: "porque [o alvo] tem zero instâncias/consumidores dependentes do comportamento anterior, a migração consiste inteiramente em fechamento de especificação, sem qualquer backfill de dado ou código".

---

## 7. Nenhuma Mudança em Documentos Anteriores

Verificação item a item, documento por documento:

| Documento | Mudança exigida | Motivo |
|---|---|---|
| Constitution | Nenhuma | Nenhum princípio, valor ou regra imutável é tocado |
| Kernel Architecture | Nenhuma | Nenhum campo é adicionado ao Component Contract (§2); Extension Model (§9) já autorizava exatamente este uso sem precisar prever `Slot` |
| Governance Architecture | Nenhuma | Nenhuma autoridade, papel ou processo novo |
| Domain Model v1.1.0 | Nenhuma | Zero entidades, zero relações, zero estados |
| RFC-DM-001 | Nenhuma | Não referenciada por este achado |
| Identity & Namespace | Nenhuma | Nenhum esquema de identidade novo — `EnumerateSlots` não introduz identidade própria (é dispatch, não Entity) |
| Registry & Discovery | Nenhuma | `Registry.resolve()` é reutilizado sem alteração (passo 1, §5 acima) |
| Validation & Certification | Nenhuma | Não referenciada por este achado |
| **Composition Architecture** | **Aditiva — ver §6** | Único documento que recebe o fechamento, de forma estritamente aditiva |
| **Workflow Architecture** | **Nenhuma** | `Step.slot` permanece exatamente como já era; `EnumerateSlots` apenas *lê* esse campo, não o redefine, não o move, não lhe acrescenta nada |
| Execution Architecture | Nenhuma | Não referenciada por este achado |
| Standards Architecture | Nenhuma | Não referenciada por este achado |
| Policy Architecture | Nenhuma | Não referenciada por este achado |
| Template Architecture | Nenhuma | Não referenciada por este achado |
| **Skill Architecture** | **Nenhuma** | Skill continua sem Slots próprios — `EnumerateSlots(Skill) = ∅` é o comportamento implícito já vigente, apenas agora nomeado |

**Confirmação explícita, no mesmo formato usado por RFC-DM-001 §8 e por toda "Validação Institucional" do corpus:** catorze dos quinze documentos permanecem byte-a-byte idênticos. Apenas Composition Architecture recebe uma seção aditiva.

---

## 8. Algoritmo Reutilizado

Nenhum algoritmo novo é introduzido por esta RFC. Prova exaustiva:

| Elemento usado | Onde já existia | Papel nesta RFC |
|---|---|---|
| `Registry.resolve()` | Registry & Discovery §6.1 | Passo 1 de `resolve_assembly` — inalterado |
| `ALGORITMO ResolveSlot(slot, requester_ns)` | Composition Architecture §7 | Passo 3 de `resolve_assembly` — inalterado, chamado uma vez por Slot enumerado |
| `Assembly` (estrutura) | Composition Architecture §4 | Estrutura de retorno — inalterada |
| Kernel §9 Extension Model | Kernel Architecture §9 | Mecanismo que já autoriza conteúdo interno type-specific — `EnumerateSlots` é sua aplicação, não sua extensão |
| Leitura de campo já declarado (`Step.slot`) | Workflow Architecture §4 | Fonte concreta de dados para `EnumerateSlots(Workflow)` |
| Padrão "tipo sem estrutura → conjunto/lista vazia, não erro" | Skill Architecture §5, S1 (`templates[]` vazio é válido) | Precedente direto para `EnumerateSlots(tipo-sem-Slots) = ∅` |

`EnumerateSlots` em si **não tem corpo algorítmico**: não itera, não filtra, não decide, não ramifica com lógica de negócio. É uma assinatura de dispatch — o mesmo papel que `manifest.templates` (um acesso de campo, nunca chamado de "algoritmo" em Template Architecture) já cumpre há quinze documentos.

---

## 9. Casos Extremos

| # | Caso | Tratamento |
|---|---|---|
| CE1 | Component de um tipo sem nenhuma estrutura Slot-portadora (Skill, Standard, Policy, Template) | `EnumerateSlots(component) = ∅`; `resolve_assembly` retorna uma `Assembly` com `resolved_slots = {}` — **não é erro**, mesmo padrão de Skill §11 S1 |
| CE2 | Workflow sem nenhum Step contendo `slot` (todos `GATE_APPROVAL`/`COMPENSATION` sem capability a resolver) | `EnumerateSlots(workflow) = ∅` — idem CE1 |
| CE3 | `component_coordinate` resolve a um tipo ainda não escrito em nenhum documento ratificado | `EnumerateSlots` é indefinida até que o documento daquele tipo a declare — **mesmo comportamento que já vale hoje para qualquer operação sobre um tipo inexistente**; esta RFC não piora nem resolve esse caso, apenas não o esconde |
| CE4 | Dois Steps do mesmo Workflow com Slots que requerem o mesmo `required_capability` | `EnumerateSlots` retorna ambos como entradas distintas da lista — a agregação/deduplicação, se necessária, permanece responsabilidade de `resolve_assembly`'s passo 3, exatamente como já seria com Slots fornecidos manualmente hoje; esta RFC não introduz nem remove essa responsabilidade |
| CE5 | `component_coordinate` em lifecycle_state fora de `{Approved, Active}` | Já coberto pela PRE existente de `resolve_assembly` (§5, inalterada) — `EnumerateSlots` nunca é chamada, pois a PRE falha antes |

---

## 10. Regras Normativas (RFC 2119)

| # | Regra | Nível |
|---|---|---|
| CA1 | `EnumerateSlots(component)` MUST ser uma função pura sobre o Manifest já resolvido do Component — MUST NOT depender de `Context` ou de qualquer estado externo | MUST / MUST NOT |
| CA2 | `EnumerateSlots` MUST NOT ser implementada dentro de Composition Architecture — sua definição concreta pertence exclusivamente ao documento do tipo especializado (Workflow hoje; qualquer tipo futuro, quando escrito) | MUST NOT |
| CA3 | Um tipo de Component sem estrutura interna portadora de Slot MUST produzir `EnumerateSlots(component) = ∅`; isto MUST NOT ser tratado como erro por `resolve_assembly` | MUST / MUST NOT |
| CA4 | `resolve_assembly(component_coordinate)` MUST invocar `EnumerateSlots` exactly uma vez por resolução, sobre o Manifest já resolvido — MUST NOT derivar Slots de nenhuma outra fonte | MUST / MUST NOT |
| CA5 | `ALGORITMO ResolveSlot` (Composition §7) MUST permanecer inalterado — `EnumerateSlots` MUST apenas alimentá-lo, nunca substituí-lo ou reimplementá-lo | MUST |
| CA6 | Esta RFC MUST NOT ser lida como autorização para um décimo-sexto campo no Component Contract (Kernel §2) — a fonte de `EnumerateSlots` MUST sempre ser conteúdo interno já autorizado sob Kernel §9 Extension Model | MUST NOT |

---

## 11. Prova Institucional

| Verificação cruzada | Resultado | Evidência |
|---|---|---|
| Nenhuma entidade nova | **PASS** | `EnumerateSlots` não é uma Entity — não tem identidade, não é persistida, não aparece no Domain Model §2 |
| Nenhum Value Object novo | **PASS** | `EnumerateSlots` é uma função de dispatch, não uma estrutura de dados; `Slot` (o VO já existente) não é alterado |
| Nenhum algoritmo novo | **PASS** | Prova exaustiva em §8 — toda peça é reutilizada; `EnumerateSlots` não tem corpo algorítmico próprio |
| Nenhum estado novo | **PASS** | Nenhum Lifecycle, nenhuma máquina de estados, nenhuma transição introduzida |
| Registry inalterado | **PASS** | `Registry.resolve()` chamado exatamente como já era (§5, passo 1) |
| Identity inalterado | **PASS** | Nenhum esquema de identificador tocado |
| Component Contract inalterado | **PASS** | Kernel §2 permanece com exatamente quinze campos — ver CA6 |
| Workflow inalterado | **PASS** | `Step.slot` lido, nunca modificado, movido ou estendido |
| Skill inalterado | **PASS** | `EnumerateSlots(Skill) = ∅` é leitura do que já era verdade, não uma mudança de comportamento |
| Composition — mudança | **Aditiva, ver §6** | Único documento tocado, e apenas por adição |
| Consistente com Kernel §9 (Extension Model) | **PASS** | `EnumerateSlots` é aplicação direta do princípio já existente — dispatch por tipo, sem enumeração fechada |
| Runtime implementado continua válido | **PASS** | Nenhuma chamada existente do Runtime a `resolve_slot`, `Assembly`, `Registry.resolve` muda de assinatura ou comportamento; o Runtime pode, opcionalmente, passar a expor `resolve_assembly` chamando `EnumerateSlots` sem tocar em nenhum módulo já escrito além de acrescentar essa nova função |
| `resolve_assembly` torna-se implementável | **PASS** | §5 apresenta a definição operacional completa, ausente antes desta RFC |
| Exige RFC de emenda a outro documento? | **Não** | — |

---

## 12. Critério de Aceitação

| Critério do mandato | Status |
|---|---|
| RFC extremamente pequena (~4-8 páginas) | ✔ — 12 seções, sem prosa redundante, cada uma respondendo exatamente ao que foi pedido |
| Não modifica nenhum documento anterior | ✔ §7 — verificação item a item, catorze de quinze documentos sem nenhuma alteração |
| Nenhuma nova entidade | ✔ §11 |
| Nenhum novo Value Object | ✔ §11 |
| Nenhum novo algoritmo | ✔ §8, §11 |
| Nenhum novo estado | ✔ §11 |
| Registry inalterado | ✔ §7, §11 |
| Identity inalterado | ✔ §7, §11 |
| Component Contract inalterado | ✔ §7, §11, CA6 |
| Workflow inalterado | ✔ §7, §11 |
| Skill inalterado | ✔ §7, §11 |
| Apenas fecha a lacuna de Composition | ✔ Composition Architecture é o único documento com mudança (aditiva) |
| `resolve_assembly` obtém Slots da estrutura interna do próprio tipo especializado | ✔ §4 — tabela de instanciações por tipo |
| Composition nunca conhece a estrutura interna dos tipos | ✔ §5 — `EnumerateSlots` é dispatch opaco, justificado contra a alternativa rejeitada |
| `EnumerateSlots` não é um novo algoritmo, é abstração equivalente ao Extension Model | ✔ §4, §8 |

---

## Fechamento

Esta RFC elimina o único achado estrutural encontrado durante a implementação completa e execução real do Runtime (Runtime Gap Analysis v1.0, §3.1 e §7): a impossibilidade de implementar `resolve_assembly(component_coordinate)` como operação autônoma, por ausência de uma fonte declarada para os Slots de um Component genérico. Nenhuma funcionalidade nova surge — `resolve_assembly` já estava contratado desde Composition Architecture v1.0.0; esta RFC apenas nomeia, de forma aditiva e não invasiva, o mecanismo de onde ele lê seu próprio insumo. Nenhum comportamento novo surge — para todo tipo já ratificado, `EnumerateSlots` produz exatamente o resultado que o silêncio normativo anterior já implicava (Workflow: os Slots que `Step.slot` já continha; qualquer outro tipo hoje existente: o conjunto vazio, porque nenhum deles jamais declarou Slots próprios). O que muda é, exclusivamente, que uma operação antes contratada e inexequível passa a ser, agora, formalmente completa.

*Fim do documento. RFC-COMP-001, v1.0.0 — Proposed.*
