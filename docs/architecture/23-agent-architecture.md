# Agent Architecture
### Framework Eng — A Especialização Decisória do Operational Component

*Versão 1.0.0 · Base normativa (congelada): Constitution · Kernel · Governance · Domain Model v1.1.0 · RFC-DM-001 · Identity & Namespace · Registry & Discovery · Validation & Certification · Composition Architecture · Workflow Architecture · Execution Architecture · Standards Architecture · Policy Architecture · Template Architecture · Skill Architecture · RFC-COMP-001*

> **Tese central deste documento, provada seção a seção:** um `Agent` é, estrutural e operacionalmente, **exatamente** um `Component` (Kernel §1-§2) do tipo `Operational Component` (Domain Model §3) que ocupa uma `Role` (Domain Model §2 #12, Governance §2), recebe uma finalidade a cumprir, decompõe-na em unidades invocáveis já normatizadas (`Step`, Workflow §4), seleciona e invoca `Skill`s através do mecanismo já existente (`InvokeSkillStep`, Skill §9) e produz `Artifact` (Domain Model §2 #7). Este documento não define nenhum mecanismo novo — **integra**, exatamente como Skill Architecture já fez para a camada abaixo dela.

---

## 1. Posição Arquitetural

Um `Agent` é a especialização de **Operational Component** que representa a **unidade decisória** do Framework — o ponto em que a orquestração deixa de ser puramente declarativa (Workflow §4, um grafo de Phase/Step fixado antes da execução) e passa a envolver **seleção em tempo de invocação** de qual capacidade usar, sem no entanto ganhar qualquer autoridade, mecanismo ou caminho de execução que não exista já.

**Posição na cadeia de composição já estabelecida (estende, não substitui, o diagrama de Skill §1):**

```
Workflow  (orquestra, via Phase/Step — Workflow §4)
   │  resolve Providers via
   ▼
Composition Slot  (Composition §4)
   │  resolve, por Capability, a
   ▼
Agent  ◄── este documento             ou       Skill  (Skill Architecture)
   │  quando invocado, ocupa uma Role
   │  (Domain Model §12, Governance §2)
   │  e decompõe sua finalidade em Step[]
   │  (Workflow §4, reutilizado — ver §4)
   ▼
Step.slot  (Composition §4, mesmo Slot)
   │  resolve, por Capability, a
   ▼
Skill  (Skill Architecture)
   │  quando invocada, produz
   ▼
Execution → Artifact  (Domain Model §6-§7, Execution §5)
```

**Fronteira exata com os dois documentos vizinhos já ratificados:**

| Vizinho | Diferença estrutural |
|---|---|
| `Workflow` | Orquestra um grafo **declarado antes da execução** (Phase/Step, Workflow §4) — a sequência é fixa no Manifest. Um `Agent` decompõe sua finalidade **no momento em que é invocado**, mas a decomposição resultante é composta exatamente da mesma unidade que Workflow já usa (`Step`, ver §4) — a diferença é *quando* a sequência é decidida, nunca *do que* ela é feita |
| `Skill` | Unidade atômica, invocada, nunca orquestra. Um `Agent` nunca executa lógica de domínio diretamente — ele **sempre** delega a um `Skill` através de `InvokeSkillStep` (Skill §9), inalterado. Um `Agent` que processasse dados diretamente, sem invocar uma `Skill`, estaria violando esta fronteira |

**Regra de posicionamento central:** `Agent` não introduz um terceiro tipo de "motor de execução". Existem, no Framework, exatamente dois motores já ratificados — o de Composition (resolução estática de Slots, Composition §7) e o de Execution (Dispatch/Plan/Recover/Rollback, Execution §7). Um `Agent` é **cliente** de ambos, na mesma posição em que um `Workflow` já é — nunca um terceiro motor paralelo.

---

## 2. Objetivos

| # | Objetivo | Como este documento o realiza |
|---|---|---|
| O1 | Formalizar Agent como especialização de Operational Component, sem introduzir mecanismo novo | Prova exaustiva de reuso, §4 a §16 |
| O2 | Fechar o forward-reference de Skill Architecture §17 ("Agent ocupará Role... e orquestrará Skills sob autonomia de decisão") | §7, §8, §9 |
| O3 | Fechar o forward-reference de Policy Architecture §19 (`scope.roles` restringindo quais Roles um Agent pode ocupar) | §6.4 |
| O4 | Fechar o forward-reference deixado por RFC-COMP-001 §4 (`EnumerateSlots(Agent)` — "o que quer que Agent Architecture venha a declarar") | §4.2, §9 |
| O5 | Generalizar o achado H2 (separação de funções), hoje resolvido apenas para Certificação L4 (Validation & Certification §5, C3), para toda Decision que um Agent-Role possa tomar | §6.5 |
| O6 | Fechar o forward-reference de Validation & Certification §7 ("Agent: cenários comportamentais representativos; L4 exige avaliação humana") | §7.3 |
| O7 | Demonstrar que Registry, Composition, Execution, Workflow, Standards e Policy operam sobre Agent sem nenhum ramo condicional específico | §15 |

---

## 3. Escopo

### 3.1 Pertence

Estrutura do Manifest de um Agent; o mecanismo pelo qual um Agent obtém a lista de suas próprias unidades invocáveis (fechando `EnumerateSlots`, RFC-COMP-001); o fluxo de decisão ponta a ponta (receber finalidade → avaliar → selecionar Skill → invocar → avaliar resultado → continuar ou finalizar); especialização do critério de Certificação já anunciado para `component_type=Agent`; a regra geral de separação de funções para qualquer Role ocupada por um Agent.

### 3.2 Não pertence — com justificativa individual

| Excluído | Justificativa técnica |
|---|---|
| **O algoritmo interno de decisão** (como o Agent decide, dentre candidatos, qual invocar; como decompõe sua finalidade) | Opaco a este documento — exatamente a mesma fronteira que Skill §9 já traça para o "processamento efetivo" dentro de `Running` ("opaco a este documento — Execution §5, 'Running'"). O raciocínio de um Agent é sua lógica de negócio/IA própria, não normatizada aqui, do mesmo modo que o Framework nunca normatiza *como* uma Skill computa seu resultado |
| **Comunicação entre múltiplos Agents, protocolos, coordenação multi-agente** | `[LACUNA proposital]`, deferida a uma futura Multi-Agent Architecture. Nenhum mecanismo de comunicação é introduzido aqui — um Agent, neste documento, invoca Skills; não invoca outros Agents, nem troca mensagens com eles |
| **Memória e Conhecimento acumulado entre invocações** | `[LACUNA proposital]`, deferida a Memory/Knowledge Architecture (ainda não escritas). Cada invocação de um Agent é uma `Execution` isolada (Domain Model §8) — nenhum estado persistente entre invocações é introduzido |
| **Observabilidade de séries de invocações de Agent** | Já coberto pelo mesmo `[LACUNA proposital]` de Execution §14 (Observability & Provenance Storage) — Agent não define taxonomia de evento própria (§13) |
| **Algoritmo de planejamento (planning) ou de reasoning** | Fora de escopo por definição — é exatamente o "algoritmo interno de decisão" acima, apenas nomeado de outra forma. Nenhum algoritmo de planejamento é proposto, mandatado ou sequer sugerido aqui |
| **Novo mecanismo de descoberta, autorização, política ou versionamento** | Já resolvidos, integralmente, por Registry & Discovery, Governance, Policy e Identity & Namespace respectivamente — um Agent os consome com `component_type=Agent` como filtro, exatamente como Skill já faz (Skill §3.2) |

---

## 4. Modelo Conceitual

### 4.1 Prova de minimalidade — tabela de proveniência

**Este documento introduz zero entidades, zero Value Objects, zero relações, zero estados, zero algoritmos com corpo lógico próprio.** Toda linha abaixo é "Reutilizado", sem exceção — inclusive as duas linhas que poderiam parecer novas à primeira vista (`Goal`, `Action`), cuja resolução está detalhada em §4.2 e §4.3.

| Conceito usado por Agent | Definido em |
|---|---|
| `Component`, `Identity`, `Coordinate`, `Manifest`, `Contract` | Kernel §1-§2 |
| `Lifecycle` (Draft→Review→Approved→Active→Deprecated→Archived→Removed) | Kernel §3 |
| `Capability`, `Constraint` | Kernel §2.9, §2.10 |
| `Inputs`, `Outputs`, `Dependencies`, `Providers`, `Consumers`, `Compatibility`, `Metadata`, `Validation` | Kernel §2.4-§2.15 |
| Extension Model (conteúdo interno type-specific dentro do Contract) | Kernel §9 |
| `Operational Component` (categoria) | Domain Model §3 |
| `Execution`, `Artifact`, `Context`, `Evidence` | Domain Model §2; Execution Architecture |
| `Role`, `performed_by` (Execution→Role, N:1) — "ocupada por uma pessoa, time ou Agent" | Domain Model §2 #12, §5, §20; Governance §2 |
| `Decision`, autoridade declarada por Role | Domain Model §14; Governance §8 |
| `VersionedIdentifier`, Lineage, `supersedes` | Identity & Namespace §4, §7 |
| Registro, descoberta, `manifest_digest` | Registry & Discovery §3.1, §6; Validation & Certification §6 |
| Verificação estrutural, Certificação L0-L4, per-type specialization | Validation & Certification §4, §5, §7 |
| **`Step`** (reutilizado integralmente — ver §4.3) | Workflow Architecture §4 |
| `Slot`, `ResolveSlot`, `Assembly` | Composition Architecture §4, §7 |
| **`EnumerateSlots(component)`** (dispatch, sem corpo algorítmico) | RFC-COMP-001 §4 |
| Dispatch, Scheduler, Execution Plan | Execution Architecture §5, §7 |
| `Standard`, `NormativeRequirement`, `ComplianceTarget` | Standards Architecture §4 |
| `Policy`, `PolicyScope.roles`, `Effective Policy Set` | Policy Architecture §5.2, §9 |
| `Template`, `Variable`, `Placeholder`, `Expanded Template` | Template Architecture §4, §11 |
| `InvokeSkillStep` | Skill Architecture §9 |

### 4.2 A finalidade de um Agent ("Goal") — reutilização de `Context`, não entidade nova

`[ESCOLHA DE DESIGN]`

**Motivação:** decidir como representar a finalidade que um Agent recebe ao ser invocado, sem introduzir uma entidade ou Value Object novo.

**Alternativas rejeitadas:** (a) criar uma entidade `Goal` no Domain Model, exigindo RFC de emenda (Domain Model §18.1); (b) criar um Value Object `Goal` novo, paralelo, escopado ao Contract do Agent.

**Justificativa técnica:** Execution Architecture já resolveu, para o problema estruturalmente idêntico de correlacionar uma orquestração às suas Executions filhas (achado H6), o mesmo tipo de necessidade — **carregar informação semântica adicional como conteúdo de `Context`** (já genérico por definição, Domain Model §2 entidade #5), em vez de criar uma relação ou entidade nova (ver preâmbulo do bloco Composition/Workflow/Execution: *"Correlação... é carregada como conteúdo semântico dentro de Context... nunca como uma aresta nova."*). A finalidade de um Agent aplica-se exatamente ao mesmo padrão: **`Context.extra["goal"]` é a finalidade textual/estruturada que a Execution do Agent recebe**, com o critério de satisfação expresso como um `Constraint` (Kernel §2.10, já reutilizado por Template Architecture para restringir valores de `Variable` e por Workflow para `timeout`). Nenhuma entidade `Goal` existe; existe uma **convenção de conteúdo** sobre `Context`, precisamente como `orchestration_id`/`phase_id`/`step_id`/`attempt` já são.

**Precedente arquitetônico:** a mesma técnica — carregar semântica adicional em um campo genérico já existente, em vez de expandir o modelo — é a que W3C Trace Context usa para `tracestate` (conteúdo extensível dentro de um campo já genérico), citada explicitamente como precedente pelo preâmbulo do bloco Composition/Workflow/Execution.

### 4.3 As unidades de decomposição de um Agent ("Action") — reutilização de `Step`, não Value Object novo

`[ESCOLHA DE DESIGN]`

**Motivação:** decidir como um Agent decompõe sua finalidade em unidades invocáveis, sem introduzir um Value Object novo (o que o RFC-COMP-001 §4, ao citar "Action.slot" apenas como *exemplo ilustrativo* de uma futura possibilidade, deixou em aberto — não como mandato).

**Alternativas rejeitadas:** criar um Value Object `Action` novo, com campos próprios (`id`, `slot`, `kind`...), paralelo a `Step`.

**Justificativa técnica:** a estrutura de que um Agent precisa — uma unidade com identificador, um `Slot` a resolver (Composition §4), um tipo de operação (invocação, gate automático, gate de aprovação, compensação), uma política de falha e um `timeout` — é **estruturalmente idêntica** ao que `Step` (Workflow §4) já provê integralmente:

```
Step {
  id, slot: CompositionSlot, kind: INVOCATION | GATE_AUTO | GATE_APPROVAL | COMPENSATION,
  failure_policy: FailurePolicy, timeout: Constraint, compensated_by: StepRef?, params
}
```

Introduzir uma segunda estrutura, com os mesmos campos e o mesmo propósito, apenas para chamá-la de "Action" violaria diretamente a **Regra Imutável nº10 da Constitution** ("nenhum componente novo é aceito sem antes se verificar que algo equivalente já não existe — duplicação evitável é uma violação, não uma escolha neutra"). Este documento, portanto, **reutiliza `Step` tal qual**, hospedado agora em um campo aditivo do Manifest de um Agent (`actions: Step[]` — ver §5), em vez de exclusivamente dentro de uma `Phase` de Workflow.

**Consequência elegante, não coincidência:** um Agent, no momento em que age, está executando uma estrutura isomórfica a uma única `Phase` sem nome de um Workflow — a mesma gramática de `kind`/`failure_policy`/`compensated_by` que já rege gates, compensação e políticas de falha em Workflow aplica-se, sem nenhuma adaptação, à sequência de ações de um Agent.

**Precedente arquitetônico:** o mesmo padrão de "reaproveitar o VO já ratificado em um segundo host de Contract" que Kernel §9 (Extension Model) já sanciona para `templates[]` (hospedado tanto em Skill quanto, agora, potencialmente em Agent) — nenhuma extensão do mecanismo é necessária.

### 4.4 `EnumerateSlots(Agent)` — fechamento do forward-reference de RFC-COMP-001

Consequência direta de §4.3: `EnumerateSlots(component)`, quando `component.component_type = Agent`, é definida — pelo próprio Agent Architecture, exatamente como RFC-COMP-001 §4 antecipava ("a resposta pertence a cada tipo, não a Composition") — como:

```
EnumerateSlots(agent_manifest) = { step.slot : step ∈ agent_manifest.actions, step.slot ≠ null }
```

Idêntica, campo por campo, à definição já dada para Workflow em RFC-COMP-001 §4 (`{ step.slot : step ∈ all_steps(component.phases) }`), apenas trocando a fonte de `phases[].steps[]` para `actions[]` diretamente — porque um Agent, ao contrário de um Workflow, não possui `Phase` (não há fases nem gates de fluxo declarativo entre Agents; a sequência é decidida em tempo de invocação, §4.1). Nenhuma nova regra de dispatch é introduzida; apenas a instanciação, para `component_type=Agent`, que RFC-COMP-001 já previa como decisão a ser tomada "quando aquele documento for escrito" — este é aquele documento.

---

## 5. Manifest

| Campo do Component Contract (Kernel §2) | Uso por um Agent |
|---|---|
| `identity` | `component_type = Agent`; namespace/nome conforme convenção já fixada (Registry §5, `<ns>/agent.<papel>`) |
| `purpose` | Descrição do problema resolvido — sem alteração de semântica |
| `owner` | `Role` — Governance §2-§3, sem alteração |
| `inputs` | Schema declarado da finalidade recebida; **MAY** ser refinado por `INPUT Template`, exatamente como Skill §6.1 |
| `outputs` | Schema declarado do Artifact final agregado; **MAY** ser refinado por `OUTPUT Template`, exatamente como Skill §6.2 |
| `dependencies` / `providers` / `consumers` | Reutilizados sem alteração — um Agent **MAY** depender de Skills ou de outros Components, resolvidos por Composition |
| `capabilities` | Vocabulário de Capability exposto — usado por Registry §6.2 e Composition §6-§7 sem modificação |
| `constraints` | Kernel §2.10 — usado também como critério de satisfação da finalidade (§4.2) e dentro de `Variable.constraint` de Templates |
| `version` | SemVer — Kernel §2.11 |
| `lifecycle` | Kernel §3, sem exceção |
| `compatibility` | Kernel §2.13 |
| `metadata` | `standards_bound` (Kernel §2.14) — vínculo a Standards |
| `validation` | Critério de correção — Kernel §2.15 |
| `templates[]` | **Campo aditivo já normatizado por Template Architecture §4.2**, não introduzido aqui — um `PROMPT Template`, quando presente, serve de base para a instrução do Agent (fechando o forward-reference de Skill §17), da mesma forma que já serve de base para o processamento de uma Skill |
| `actions[]` | **Campo aditivo, habilitado por Kernel §9 (Extension Model), exatamente pelo mesmo mecanismo que autorizou `templates[]` e a "Orchestration Definition" de Workflow §4** — lista de `Step` (Workflow §4, reutilizado — §4.3), nunca um Value Object novo |

`[ESCOLHA DE DESIGN]`

**Motivação:** decidir se `actions[]` é um campo obrigatório de todo Agent.

**Alternativas rejeitadas:** exigir ao menos uma `Action` por Agent.

**Justificativa técnica:** exatamente o mesmo raciocínio de Skill §5 para `templates[]` — um Agent cuja finalidade seja satisfeita por uma única Skill conhecida antecipadamente **MAY** declarar `actions[]` com um único `Step`; nada nesta arquitetura força um mínimo maior que zero (um Agent sem `actions[]` teria `EnumerateSlots(agent) = ∅`, tratado como caso extremo válido — ver §11, CE1). Forçar um mínimo violaria Constitution (Simplicidade).

---

## 6. Contract

### 6.1 Como Input/Output Template refinam Inputs/Outputs de um Agent

Sem alteração de mecanismo: `INPUT Template` e `OUTPUT Template` (Template Architecture §4.2-§4.3) refinam `inputs`/`outputs` (Kernel §2.4-§2.5) exatamente como já fazem para uma Skill (Skill §6.1-§6.2) — Agent não introduz uma terceira semântica de refinamento.

### 6.2 Como Prompt Template participa da invocação

Um `PROMPT Template`, quando presente no Agent, é expandido (Template Architecture §11.3) entre `Initiated` e `Running` da Execution do próprio Agent — produzindo um `Expanded Template` que se torna a instrução inicial do processo de decisão (§3.2, opaco). Idêntico, mecanicamente, a Skill §6.3 — a única diferença é *o que* consome o resultado da expansão (o raciocínio opaco de um Agent, em vez do processamento opaco de uma Skill), nunca *como* a expansão ocorre.

### 6.3 Como `actions[]` participa da invocação

Cada `Step` de `actions[]` é candidato a ser selecionado (§9, `SelectSkill`) durante o ciclo de decisão do Agent. Nenhuma modificação de `Step` é necessária — `kind = INVOCATION` é resolvido via `ResolveSlot` + `InvokeSkillStep`, exatamente como dentro de uma Workflow Phase; `kind = GATE_APPROVAL` resolve-se contra um `Role` (podendo ser outro Agent ou um humano, ver §6.5); `kind = COMPENSATION` é dispatchado por `rollback()` (Execution §7), sem alteração alguma.

### 6.4 Como Policy restringe qual Role um Agent pode ocupar — fechamento do forward-reference de Policy §19

`PolicyScope.roles: [RoleClass]?` (Policy Architecture §5.2, já ratificado, inalterado) já é suficiente para restringir quais classes de Role um Agent está autorizado a ocupar — nenhuma extensão de Policy é necessária. Uma Policy com `scope.roles = [role.governance-area.code-quality.reviewer]` e `scope.component_types = [Agent]` já expressa, sem nenhuma mudança a Policy Architecture, "apenas Agents certificados podem ocupar este papel."

### 6.5 Separação de funções (H2) — generalização do caso já resolvido em Certificação

Validation & Certification §5 já estabelece, para o caso específico de Certificação L4: *"em L4, quando o Component sendo certificado é um Agent, o Certifier MUST ser um Role ocupado por humano — um Agent MUST NOT ser o único certificador L4 de outro Agent da mesma categoria operacional"* (C3). Governance §2 já estabelece, para qualquer Decision: *"ninguém pode ser simultaneamente Reviewer e Owner do mesmo componente na mesma decisão"* — regra que não distingue humano de Agent, porque Governance define Role por posição institucional, nunca por espécie do ocupante (Domain Model §20).

Este documento **generaliza a aplicação** dessas duas regras já ratificadas — sem alterar nenhuma delas — para qualquer Decision que um Agent-Role tome, não apenas Certificação: um Agent que ocupa um `Role` com autoridade de Decision (Domain Model §14) está sujeito, sem exceção, à mesma regra de não concentração de Governance §2, e — quando a Decision certifica ou aprova outro Component da mesma categoria operacional em L4 — à mesma exigência de coocupação humana de Validation & Certification §5 C3. Nenhuma autoridade nova é criada; nenhuma das duas regras-fonte é reescrita — apenas confirma-se, explicitamente, que "ninguém" em Governance §2 e "Certifier" em Validation & Certification §5 já significam, sem exceção, "humano ou Agent, sob a mesma regra".

---

## 7. Modelo Operacional

Toda operação sobre um Agent é a operação genérica já definida, filtrada por `component_type = Agent`. Nenhuma nova assinatura de operação é introduzida.

| Operação | Definida em | Especialização para Agent |
|---|---|---|
| Admissão / aprovação | Governance §7 | Nenhuma — processo idêntico a qualquer Component |
| Verificação estrutural | Kernel §8 | `inputs`/`outputs`/`templates[]`/`actions[]` validados por Kernel §8 + Template §9 + a mesma verificação de grafo já usada por Workflow (`ValidateWorkflowGraph`, Workflow §7, reaplicada sobre `actions[]` — ver §9.2) |
| Registro | Registry & Discovery §5 | `register(manifest, decision_record_ref)`, sem alteração |
| Descoberta | Registry & Discovery §6.2 | `search(capability)` — mesma operação já usada para Skill |
| Resolução de dependência/Provider | Composition §5-§7 | `EnumerateSlots` + `ResolveSlot` — Agent é candidato elegível como qualquer Component, e também consome Composition para os Slots de suas próprias `actions[]` |
| Certificação | Validation & Certification §5 | Ver §7.3 abaixo — fecha o forward-reference já existente |
| Dispatch/Execução | Execution §5 | `Dispatch(step)` — sem alteração; a invocação do Agent é, ela própria, uma Execution comum |
| Avaliação normativa | Standards §10; Policy §10 | `applies_to`/`applies_at = MANIFEST\|EXECUTION\|ARTIFACT`, sem novo valor de enum |

### 7.3 Fechamento do forward-reference de Certificação

Validation & Certification §7 já declarava, antes deste documento existir: *"Agent: Cenários comportamentais representativos; L4 exige avaliação humana — Comportamento sob ambiguidade + separação de funções (§5)."* Este documento fornece o mecanismo concreto, sem alterar aquele critério:

> Para um Agent, `Testing` (Validation & Certification §4) **MUST** consistir em uma ou mais `Execution`s do próprio Agent sob finalidades (`Goal`, §4.2) representativas de ambiguidade real — não apenas casos determinísticos — cujos `Artifact`s resultantes são avaliados contra `outputs` (refinado, quando presente, por `OUTPUT Template`) por um `Reviewer` humano (Governance §2). Cada Execution de teste produz `Evidence` via `Evaluation Method` do tipo `ATTESTED` (Standards §4.6) quando o critério exigir julgamento humano, ou `DYNAMIC` quando o critério for mecanicamente verificável (ex.: o Agent respeitou a fronteira §1, nunca processando dados sem invocar uma Skill). L4 **MUST**, adicionalmente, satisfazer §6.5 (separação de funções) — sem o que L4 **MUST NOT** ser concedido, mesma regra já estabelecida em Validation & Certification §5 C3.

---

## 8. Fluxo

```
1. Workflow declara Step com Composition Slot (capability=Y, min_certification_level=L2)  [Workflow §4]
2. Composition Resolver resolve Slot → Agent@version concreto                              [Composition §7]
3. Execution.Dispatch(step)                                                                 [Execution §5]
   a. Context{ orchestration_id, phase_id, step_id, attempt, goal: <finalidade> } montado    [§4.2]
   b. Context Snapshot capturado                                                             [RFC-DM-001 §3.2]
   c. Execution → Initiated → Running
4. SE Agent possui templates[] (PROMPT):
   a. Template.ResolveEffectiveTemplate / BindVariables / Expand                             [Template §11, §6.2]
5. EnumerateSlots(agent.manifest) → Step[] das próprias actions[]                            [§4.4, RFC-COMP-001]
6. Loop de decisão (opaco quanto ao "como", normatizado quanto ao "com o quê"):
   a. EvaluateGoal(context) → satisfeita? SIM → 7 ; NÃO → b                                  [§9]
   b. SelectSkill(actions_restantes, context) → próximo Step elegível                        [§9]
   c. Composition.ResolveSlot(step.slot, requester_ns)                                       [Composition §7]
   d. Skill.InvokeSkillStep(step, ctx, at) → Execution filha + Artifact                       [Skill §9]
      (orchestration_id da Execution filha = instance_id da Execution do próprio Agent — H6)
   e. Artefato agregado à lista de resultados; volta a (a)
7. FinishGoal(execution, artifacts) → Artifact final (Materialize, Kernel §2.5)               [§9]
8. Execution → Completed | Failed | Aborted                                                   [Domain Model §8]
```

Nenhum passo acima introduz operação nova — é composição sequencial de algoritmos já publicados, exatamente como Skill §8 já demonstrou para a camada abaixo.

---

## 9. Algoritmos

**Nenhum algoritmo novo é necessário.** Os quatro nomes pedidos são, cada um, orquestração pura de algoritmos já ratificados — prova de que Agent não exige lógica estrutural própria (a única lógica não normatizada é o "como decidir", deliberadamente opaco, §3.2).

```
ALGORITMO InvokeAgent(agent_ref, goal, ctx, at):
  slot_result ← Composition.ResolveSlot(step.slot, requester_ns)         # Composition §7 — Agent como Provider
  SE slot_result é SlotError: RETORNA Falha(slot_result)

  exec ← Execution.Dispatch(step, orchestration_id, attempt=0)           # Execution §7
  # exec já inclui: Context{..., goal} (§4.2), Context Snapshot, Initiated→Running

  SE Registry.resolve(agent_ref).manifest.templates ≠ ∅:
     eff_tpl ← Template.ResolveEffectiveTemplate(...)                     # Template §11.1 — igual a Skill §9
     expanded ← Template.Expand(...)                                      # Template §11.3

  actions ← EnumerateSlots(Registry.resolve(agent_ref).manifest)          # §4.4, RFC-COMP-001
  resultados ← []

  ENQUANTO ¬EvaluateGoal(exec.captured_as.captured_context):              # §9, abaixo
     step ← SelectSkill(actions, resultados, exec.captured_as)            # §9, abaixo
     SE step é null: exec.transition(Failed, "GOAL_UNREACHABLE"); RETORNA Falha
     (filho_exec, artifact) ← Skill.InvokeSkillStep(step, ...)             # Skill §9 — verbatim
     resultados.append(artifact)

  artifact_final ← FinishGoal(exec, resultados)                          # §9, abaixo
  RETORNA artifact_final


ALGORITMO EvaluateGoal(context):
  # mesma forma de EvaluateDecisionPoint (Workflow §7) — reaplicada, não reimplementada
  SE context.goal.success_criteria é PureExpression:
     RETORNA evaluate(context.goal.success_criteria, context)             # sem Execution nova
  SENÃO:
     RETORNA awaits a Execution do Step referenciado, então avalia         # idêntico a Workflow §7


ALGORITMO SelectSkill(actions, resultados_ate_agora, ctx_snapshot):
  # mesma forma de "ready_steps" (Execution §7 scheduler) — não um algoritmo de seleção novo:
  # percorre actions na ordem declarada, retorna o primeiro Step ainda não
  # resolvido cujas dependências (se declaradas via params/Context) já estão satisfeitas
  PARA CADA step EM actions:
     SE step JÁ RESOLVIDO EM resultados_ate_agora: CONTINUA
     RETORNA step
  RETORNA null   # nenhuma action elegível restante — ver CE1/CE2


ALGORITMO FinishGoal(execution, artifacts):
  artifact_final ← Materialize(artifacts CONFORME agent.manifest.outputs)  # Kernel §2.5 — igual a Skill §9
  execution.transition(Completed)                                          # Domain Model §8
  RETORNA artifact_final
```

Nenhum dos quatro algoritmos acima contém lógica de seleção, planejamento ou reasoning — cada um delega inteiramente a um algoritmo já ratificado (`ResolveSlot`, `Dispatch`, `InvokeSkillStep`, `EvaluateDecisionPoint`, `Materialize`) ou a uma travessia trivial de lista já usada em outro lugar (`ready_steps`).

### 9.1 Detecção de Breaking Change — reuso composto

```
ALGORITMO ClassifyAgentChange(prev, next):
  contract_class ← Kernel§2.13.ClassifyCompatibility(prev, next)       # já existente — inclui actions[]
  template_classes ← [ Template.ClassifyTemplateChange(prev, next, tid)
                        PARA CADA tid EM UnionDeTemplateIds(prev, next) ]
  RETORNA Max(contract_class, template_classes)    # o mais restritivo entre os dois domina
```

Idêntico, estrutural e literalmente, a `ClassifySkillChange` (Skill §9.1) — `actions[]`, por ser conteúdo de Extension Model dentro do Contract (§4.3), é coberto pela mesma classificação genérica de compatibilidade de Contract (Kernel §2.13), sem exigir um terceiro classificador dedicado a `Step[]`.

### 9.2 Validação estrutural de `actions[]` — reuso, não novo algoritmo

`validate_agent_definition(manifest)` **reutiliza integralmente** `ValidateWorkflowGraph` (Workflow §7) aplicado sobre `actions[]` tratado como uma única `Phase` implícita — mesma verificação de aciclicidade (Kernel §7), mesma regra de "toda `COMPENSATION` referenciada por exatamente um Step", mesmo requisito de `role_class` resolvível para `GATE_APPROVAL`. Nenhuma variante do algoritmo é escrita; é a mesma função, chamada com uma lista de `Step` em vez de uma lista de `Phase`.

---

## 10. Diagramas

### 10.1 UML — Agent como especialização

```
┌─────────────────────────┐
│ «abstract» Component      │   [Kernel §1-§2]
└─────────────┬────────────┘
               △
┌─────────────┴────────────┐
│ Operational Component      │   [Domain Model §3]
└─────────────┬────────────┘
               △
       ┌───────┴───────┐
       │     Agent      │   identity.component_type = Agent
       │                │   (nenhum atributo além do Contract padrão)
       └───┬───────┬───┘
           │0..*    │0..*
           ▼        ▼
    templates[]   actions[] : Step   [Workflow §4 — reutilizado, não redefinido]
    [Template §4]     │
                       ▼
                  Slot (Composition §4) ──resolve──► Skill | Agent
```

### 10.2 Sequência — invocação completa

```
Workflow(Step)   Composition      Registry     Execution    Template     Agent(runtime)    Skill(runtime)
     │                │              │             │            │             │                 │
     ├─ResolveSlot────►│              │             │            │             │                 │
     │                ├─search(cap)─►│              │            │             │                 │
     │◄─agent_ref──────┤              │             │            │             │                 │
     │                                              │            │             │                 │
     ├─Dispatch(step)──────────────────────────────►│            │             │                 │
     │                                    Context{goal}+Snapshot [RFC-DM-001 §3.2]                │
     │                                    Initiated→Running       │             │                 │
     │                                              │             │             │                 │
     │              opt templates[PROMPT] ≠ ∅        │            │             │                 │
     │                                              ├─Resolve/Bind/Expand──────►│                 │
     │                                              │◄──ExpandedTemplate────────┤                 │
     │                                              │                                              │
     │                                              ├──EnumerateSlots(agent)───────────────────────►│
     │                                              │◄──Step[] (actions[])──────────────────────────┤
     │                                              │                                              │
     │                loop EvaluateGoal = falso                                                    │
     │                                              ├──SelectSkill──────────────────────────────────►│
     │                                              │                    ├─ResolveSlot──────────────►│
     │                                              │                    ├─InvokeSkillStep───────────────────────────►│
     │                                              │                    │◄──Execution+Artifact──────────────────────┤
     │                                              │◄───────────────────┤                                          │
     │                loop EvaluateGoal = verdadeiro                                                                 │
     │                                              ├─FinishGoal / Materialize                                       │
     │                                              ├─Completed                                                      │
     │◄─artifact final────────────────────────────────┤                                                              │
```

### 10.3 Estados

Idêntico ao Kernel Lifecycle (Kernel §3), sem exceção — mesma disciplina já aplicada em Standards §11.4, Policy §12.4, Template §10.3, Skill §10.3. A invocação do Agent, por sua vez, usa exatamente o Lifecycle de `Execution` (Domain Model §8) — nenhum terceiro diagrama de estados é introduzido.

---

## 11. Casos Extremos

| # | Caso | Tratamento |
|---|---|---|
| CE1 | Goal impossível de satisfazer (nenhuma sequência de `actions[]` a atinge) | `EvaluateGoal` nunca retorna verdadeiro; `SelectSkill` eventualmente retorna `null` (todas as actions elegíveis já exauridas) → `Execution.transition(Failed, "GOAL_UNREACHABLE")` — mesmo padrão de falha nomeada já usado em Composition (`SlotError`) e Registry (`NotFound`), nenhum estado novo |
| CE2 | Nenhuma Skill encontrada para o Slot de uma `action` | `ResolveSlot` retorna `SlotError(UNSATISFIED)` (Composition §7, inalterado) — propagado como falha da Execution do Agent, nunca engolido silenciosamente |
| CE3 | Skill falha durante invocação | A Execution filha transita a `Failed` (Domain Model §8); o Agent reage conforme a `FailurePolicy` do `Step` correspondente (§4.3) — `ABORT` propaga falha ao Agent; `SKIP` continua para a próxima action elegível; `RETRY(n)` e `COMPENSATE` — ver CE4/CE9 |
| CE4 | Retry | **MUST** ser uma nova Execution — nunca reabertura da anterior (EX1, Execution §12; WF5, Workflow §12) — reutilizado sem exceção |
| CE5 | Abort | Execution transita a `Aborted` (Domain Model §8) — estado já existente, nenhuma adição |
| CE6 | Cancel (requisição externa de interrupção) | **Não existe um sexto estado "Cancelled".** Uma requisição de cancelamento honrada é registrada como a mesma transição para `Aborted` já usada para qualquer outra interrupção externa — Domain Model §8 não é estendido |
| CE7 | Role que o Agent tentaria ocupar não tem autorização (ex.: `GATE_APPROVAL` exigindo `role_class` que o Agent não satisfaz) | `Unauthorized` — mesma classe de erro já nomeada por Registry §13; resolução de `role_class` segue Governance §2/§8 sem exceção |
| CE8 | Policy nega a execução (`enforcement_mode = BLOCKING`) | Dispatch **MUST NOT** prosseguir (Policy §5.4, Execution §8) — mesmo mecanismo já previsto para qualquer Step de Workflow, sem tratamento condicional por Agent |
| CE9 | Standard obrigatório vinculado ao Agent | Avaliado em `applies_to = EXECUTION`/`MANIFEST` exatamente como para qualquer Component (Standards §4.5) — nenhum novo valor de enum |
| CE10 | Workflow que contém o Step do Agent é interrompido/abortado | A Execution do Agent, já em curso, permanece regida por sua própria imutabilidade (EX1) — a interrupção do Workflow não reabre nem modifica a Execution do Agent; propaga-se para frente, nunca para trás, mesma regra de Policy §14 F8/F9 |
| CE11 | Execution Failed | Estado terminal já existente (Domain Model §8) — tratado por `FailurePolicy` do Step que invocou o Agent, sem mecanismo novo |
| CE12 | "Execution Suspended" | **Não existe um estado de Execution chamado "Suspended".** O único "Suspended" ratificado pertence a **Certificação** (Validation & Certification §5: `Ln → Suspended(Ln) → restored`), não a Execution. Uma Certificação suspensa de uma Skill/Agent candidato **MAY** impedir uma *futura* resolução via `ResolveSlot` (se `min_certification_level` deixar de ser satisfeito) — mas **MUST NOT** afetar uma Execution já despachada (Policy §14 F8, imutabilidade de Execution já em curso) |
| CE13 | Assembly inválido (ex.: diamond dependency entre `actions[]`) | `CompositionInvalid` (Composition §9, CP6) — reportado, nunca resolvido silenciosamente; mesmo tratamento de qualquer Assembly |
| CE14 | Skill referenciada por uma `action` está `Deprecated` | Resolução **MUST** suceder com aviso (Registry §7.3); `SelectSkill` não rejeita — apenas o sistema de descoberta já sinaliza o drift (Registry §7.3, Governance §13), nenhum tratamento especial de Agent |

---

## 12. Performance

| Recurso | Regra de cache/complexidade | Origem |
|---|---|---|
| Resolução de `Agent@version` | Cache indefinido | Registry §8 |
| `EnumerateSlots(agent)` | Leitura de campo já resolvido — mesmo custo de ler `templates[]`; nenhuma política de cache nova além da já herdada do Manifest imutável (Kernel §8) | RFC-COMP-001 §4 |
| Resolução de Assembly contendo o Agent | Cache indefinido enquanto Slots não mudarem | Composition §10 |
| `ResolveEffectiveTemplate` / `Expand` | Cache indefinido por `(template_digest[, bindings_digest])` | Template §12 |
| Effective Policy Set aplicável | Cache com TTL/invalidação por evento, nunca indefinido | Policy §15.1 |
| Loop de decisão (`EvaluateGoal`/`SelectSkill`) | O(número de `actions[]`) por iteração — mesma ordem de grandeza já aceita para `ready_steps` (Execution §10) e `validate_workflow_definition` (Workflow §10) | Execution §10, Workflow §10 |

**Nenhuma política de cache nova.** A composição das políticas acima é suficiente porque cada camada já resolve seu próprio invariante de imutabilidade.

---

## 13. Eventos

**Agent não define nenhum tipo de evento próprio.** Tabela de eventos existentes aplicáveis, filtrados por `component_type = Agent`:

| Evento | Origem | Ocorre quando |
|---|---|---|
| `ComponentRegistered` / `VersionPublished` | Registry §11 | Admissão/nova versão de um Agent |
| `AssemblyResolved` / `SlotUnsatisfied` / `CompositionCycleDetected` | Composition §11 | Agent resolvido como Provider; ou uma de suas próprias `actions[]` falha a resolver |
| `StepDispatched` / `StepCompleted` / `StepFailed` | Execution §11 | Invocação do Agent dentro de um Workflow; e cada Execution filha que ele dispara |
| `TemplateExpanded` | Template §16 | Expansão de PROMPT/INPUT/OUTPUT Template do Agent |
| `EffectiveRequirementsResolved` | Standards §16 | Avaliação normativa sobre o Manifest do Agent |
| `EffectivePolicySetResolved` | Policy §16 | Avaliação de aplicabilidade sobre o Agent, inclusive `scope.roles` |

---

## 14. Regras Normativas (RFC 2119)

| # | Regra | Nível |
|---|---|---|
| AG1 | Agent MUST ser `identity.component_type = Agent`, um `Operational Component` (Domain Model §3) | MUST |
| AG2 | Agent MUST NOT introduzir campo de Manifest além dos quinze do Component Contract, `templates[]` e `actions[]` | MUST NOT |
| AG3 | Agent MUST NOT invocar uma Skill por caminho distinto de `InvokeSkillStep` (Skill §9) | MUST NOT |
| AG4 | Agent MUST NOT criar mecanismo paralelo de Registry, Composition, Execution ou Discovery | MUST NOT |
| AG5 | A invocação de um Agent MUST ser uma `Execution` comum (Domain Model §8), correlacionada a Executions filhas via `orchestration_id` (Execution §4, mesmo padrão H6) | MUST |
| AG6 | A finalidade recebida por um Agent (`Goal`) MUST ser carregada como conteúdo de `Context` (Domain Model §2 #5) — MUST NOT ser modelada como entidade ou Value Object novo | MUST / MUST NOT |
| AG7 | A decomposição de um Agent em unidades invocáveis MUST reutilizar `Step` (Workflow §4) tal qual — MUST NOT introduzir um tipo `Action` distinto | MUST / MUST NOT |
| AG8 | `EnumerateSlots(agent)` MUST ler exclusivamente `actions[].slot`, exatamente como RFC-COMP-001 §4 antecipou para este tipo | MUST |
| AG9 | Um Role ocupado por um Agent MUST estar sujeito à mesma regra de não concentração de Governance §2, e, em Decisions de Certificação L4 sobre a mesma categoria operacional, à mesma exigência de coocupação humana de Validation & Certification §5 C3 | MUST |
| AG10 | Retry, Abort e Cancel MUST reutilizar os estados já existentes de Execution (Domain Model §8) — MUST NOT introduzir "Suspended" ou "Cancelled" como estado de Execution | MUST / MUST NOT |
| AG11 | Agent MUST NOT contornar avaliação de Standard/Policy aplicável em `EXECUTION` (Standards §4.5; Policy §8) | MUST NOT |
| AG12 | O algoritmo interno de decisão de um Agent (como seleciona, decompõe ou raciocina) é opaco a este documento — este documento MUST NOT normatizá-lo, exatamente como Skill §9 não normatiza o processamento efetivo de uma Skill | MUST NOT |

---

## 15. Integrações

| Documento | Como Agent o consome — sem alteração |
|---|---|
| **Kernel** | Agent é Component pleno — §1-§15 aplicam-se sem exceção; §9 habilita `templates[]` e `actions[]` |
| **Governance** | Admissão, aprovação, deprecação — §7/§8/§16, sem processo paralelo; §2 (não concentração) generalizado por §6.5 deste documento |
| **Domain Model v1.1.0** | Agent = Operational Component (§3); `performed_by` (§5) resolve a um Agent sem alteração de cardinalidade |
| **RFC-DM-001** | Context Snapshot (§3.2) obrigatório antes de `Running`, inclusive para a Execution do próprio Agent |
| **Identity & Namespace** | Coordinate, Versioned Identifier — §2.1 já reservava a nota "identidade de Agent independe do modelo de IA subjacente" — reutilizada sem alteração |
| **Registry & Discovery** | Registro e descoberta por Capability — §5, §6.2, sem exceção |
| **Validation & Certification** | L0-L4 — §5; especialização de Agent em §7 fechada por este documento (§7.3); C3 generalizado por §6.5 |
| **Composition** | `ResolveSlot` trata Agent como candidato elegível igual a qualquer Component; `EnumerateSlots(Agent)` fecha o forward-reference de RFC-COMP-001 |
| **Workflow** | `Step` invoca Agent via Slot resolvido, exatamente como invocaria uma Skill; `Step` também é reutilizado *dentro* de Agent (§4.3) |
| **Execution** | Dispatch, Context Snapshot, Lifecycle — §5, sem alteração; correlação de Executions filhas via `orchestration_id` (H6) aplicada sem modificação |
| **Standards** | `ComplianceTarget.component_types` inclui `Agent` sem novo valor de enum |
| **Policy** | `scope.roles`/`scope.component_types = [Agent]` restringe aplicabilidade — §5.2, sem alteração |
| **Template Architecture** | `templates[]`, Variable, Placeholder, Expansion — §4, §11, sem alteração |
| **Skill Architecture** | `InvokeSkillStep` (§9) é o único caminho de invocação de Skill por um Agent |
| **RFC-COMP-001** | `EnumerateSlots(Agent)` instanciado neste documento, exatamente como aquela RFC antecipava |

---

## 16. Validação Institucional

| Documento base | Resultado |
|---|---|
| Constitution | **PASS** — Regra Imutável nº10 é a própria justificativa de reutilizar `Step` em vez de criar `Action` (§4.3) |
| Kernel | **PASS** — Agent é Component pleno; nenhum dos quinze campos alterado; `actions[]` habilitado por §9 exatamente como `templates[]` já era |
| Governance | **PASS** — §2 (não concentração) generalizado, não reescrito; nenhuma autoridade nova |
| Domain Model v1.1.0 | **PASS** — zero entidades/relações/estados; `Goal` é conteúdo de `Context`, não entidade |
| RFC-DM-001 | **PASS** — C2 (Context Snapshot) obrigatório, sem exceção |
| Identity & Namespace | **PASS** — §2.1 já antecipava Agent; nenhuma extensão de esquema |
| Registry & Discovery | **PASS** — §5/§6.2 reutilizados sem modificação |
| Validation & Certification | **PASS** — fecha forward-reference de §7 (§7.3); C3 generalizado (§6.5), não alterado |
| Composition | **PASS** — `ResolveSlot`/`Assembly` reutilizados; `EnumerateSlots(Agent)` instanciado sem tocar §7 |
| Workflow | **PASS** — `Step` reutilizado tal qual, tanto como consumidor (Agent como Provider de um Step) quanto como estrutura interna (`actions[]`) |
| Execution | **PASS** — Dispatch/Lifecycle/H6 reutilizados sem alteração |
| Standards | **PASS** — `component_types` inclui Agent sem novo enum |
| Policy | **PASS** — `scope.roles` fecha o forward-reference de §19 sem alteração de Policy |
| Template Architecture | **PASS** — `templates[]`, Expand, Bind reutilizados sem alteração |
| Skill Architecture | **PASS** — `InvokeSkillStep` é o único caminho de invocação; fronteira Agent/Skill (§1) respeitada |
| RFC-COMP-001 | **PASS** — `EnumerateSlots(Agent)` é exatamente a instanciação que aquela RFC previu, sem reabrir seu texto |
| **Exige RFC?** | **NÃO** |

**Prova formal de que Agent não adiciona:**

| Item vedado pelo mandato | Verificação |
|---|---|
| Nova entidade | Nenhuma — §4.1, tabela completa, toda linha "Reutilizado" |
| Novo Value Object | Nenhum — `Goal` é conteúdo de Context (§4.2); `Action` é `Step` reutilizado (§4.3) |
| Novo Lifecycle | Nenhum — Kernel §3 e Domain Model §8, sem exceção |
| Novo Registry | Nenhum — §15, Registry §5/§6.2 |
| Nova Execution / Dispatcher / Scheduler | Nenhum — Execution §5/§7, mesma Execution, mesmo Scheduler |
| Nova Composition | Nenhuma — Composition §7, `ResolveSlot` inalterado |
| Novo Workflow | Nenhum — Agent não substitui Workflow (§1) |
| Nova Policy / Standards / Validation | Nenhuma — §7.3, §6.4, §6.5 apenas instanciam critérios já anunciados |
| Novo Template / Artifact / Contract / Manifest | Nenhum — reutilizados tal qual, `actions[]` é campo aditivo, não um Manifest novo |
| Novo sistema de memória / conhecimento / multi-agent / comunicação / protocolo | Nenhum — explicitamente fora de escopo (§3.2) |
| Novo algoritmo de planejamento / reasoning | Nenhum — opaco a este documento (§3.2, AG12) |
| Novo tipo de decisão / mecanismo de descoberta / autorização / política / observabilidade | Nenhum — todos reutilizados sem exceção (§15) |

---

## 17. Dependências Futuras

| Consumidor | O que consome | Estado |
|---|---|---|
| **Multi-Agent Architecture** (futuro) | Agent como unidade individual já formalizada; este documento explicitamente não define comunicação entre Agents — pré-requisito estrutural sem bloqueio | Desbloqueado, não iniciado |
| **Memory Architecture** (futuro) | Nenhuma dependência estrutural — Agent não introduz estado persistente entre invocações | Isolado por design |
| **Knowledge Architecture** (futuro) | `Knowledge`/`Knowledge Asset` (RFC-DM-001 §3.1) já podem, em tese, ser produzidos como Artifact de uma Execution de Agent — nenhuma extensão necessária | Sem bloqueio |
| **Observability & Provenance Storage** | Séries de `StepDispatched`/`StepFailed` de Agents em escala | `[LACUNA proposital]` já declarada em Execution §14 |
| **Testing Architecture** | Formalização de geração de cenários comportamentais representativos para Evidence `ATTESTED`/`DYNAMIC` de Agent (§7.3) | `[LACUNA proposital]` |
| **Organization & Tenancy** | Agents escopados por `org.<id>` via Identity §8/§10, já suportado | Sem bloqueio |

---

## 18. Critério de Aceitação

### ✔ Checklist Institucional

| Critério do mandato | Status |
|---|---|
| Agent é Operational Component | ✔ §1, §4.1 |
| Ocupa Role, recebe Goal, decompõe em ações, seleciona Skill, invoca Skill, produz Artifact | ✔ §8, §9 |
| Reutiliza integralmente Kernel, Governance, Domain Model, Identity, Registry, Validation, Composition, Workflow, Execution, Standards, Policy, Template, Skill, RFC-COMP-001 | ✔ §4.1, §15, §16 |
| Zero entidades novas | ✔ §16 |
| Zero Value Objects novos (`Goal` = conteúdo de Context; `Action` = `Step` reutilizado) | ✔ §4.2, §4.3, §16 |
| Zero Lifecycle novo | ✔ §16 |
| Zero Registry novo | ✔ §16 |
| Zero Execution/Dispatcher/Scheduler novo | ✔ §16 |
| Zero Composition/Workflow/Policy/Standards/Validation/Template novos | ✔ §16 |
| Zero Discovery/Authority/Versionamento novos | ✔ §16 |
| Algoritmos (`InvokeAgent`, `SelectSkill`, `EvaluateGoal`, `FinishGoal`) são pura composição, sem lógica própria | ✔ §9 |
| Casos extremos exaustivos, incluindo os catorze pedidos | ✔ §11 |
| Nenhuma alteração silenciosa a documento anterior — qualquer necessidade de mudança seria RFC separada | ✔ §16 — nenhuma mudança encontrada; nenhuma RFC necessária |
| UML, sequência, algoritmos, casos extremos, RFC2119, performance, eventos | ✔ §9-§14 |

### ✔ Confirmação Explícita

**Nenhum documento da base normativa congelada foi alterado.** Agent Architecture, como Skill Architecture antes dela, é construída inteiramente por prova de reutilização — as duas únicas decisões que poderiam parecer introduzir algo novo (`Goal`, `Action`) foram resolvidas, em ambos os casos, como reaproveitamento explícito de um construto já ratificado (`Context` e `Step`, respectivamente), nunca como Value Object paralelo.

### ✔ Próximo Documento Desbloqueado

**Multi-Agent Architecture** pode agora ser escrita sem dependência pendente: Agent já define a unidade individual que uma futura orquestração multi-agente coordenaria, e a fronteira explícita deste documento (§3.2 — "Agent não invoca outros Agents, nem troca mensagens com eles") deixa claro, com precisão, exatamente onde a próxima camada começa.

---

*Fim do documento. Versão 1.0.0.*
