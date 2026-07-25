# Skill Architecture
### Framework Eng — A Especialização Atômica e Executável do Component

*Versão 1.0.0 · Base normativa (congelada): Constitution · Kernel · Governance · Domain Model v1.1.0 · RFC-DM-001 · Identity & Namespace · Registry & Discovery · Validation & Certification · Composition · Workflow · Execution · Standards · Policy · Template Architecture*

> **Tese central deste documento, provada seção a seção:** uma `Skill` é, estrutural e operacionalmente, **exatamente** um `Component` (Kernel §1-§2) do tipo `Operational Component` (Domain Model §3), sem qualquer campo, relação, estado, autoridade ou algoritmo além dos já normatizados nos treze documentos anteriores. Este documento não define — **integra**.

---

## 1. Posição Arquitetural

Uma `Skill` é a especialização de **Operational Component** que representa a **unidade executável atômica** do Framework — o nível mais granular em que um Contract (Kernel §2) se transforma em uma `Execution` (Domain Model §12) capaz de produzir `Artifact`.

**Posição na cadeia de composição já estabelecida:**

```
Workflow  (orquestra, via Phase/Step — Workflow §4)
   │  resolve Providers via
   ▼
Composition Slot  (Composition §4)
   │  resolve, por Capability, a
   ▼
Skill  (ou Agent — documento futuro)  ◄── este documento
   │  quando invocada, produz
   ▼
Execution → Artifact  (Domain Model §6-§7, Execution §5)
```

**Fronteira exata com os dois documentos vizinhos já ratificados:**

| Vizinho | Diferença estrutural |
|---|---|
| `Workflow` | Orquestra múltiplos Providers via grafo declarativo de Phase/Step (Workflow §4) — possui estrutura interna de orquestração. Uma Skill **MAY** ter Templates, mas **não** possui Phase/Step |
| `Agent` (futuro) | Ocupará Role (Governance §2) e orquestrará Skills sob autonomia de decisão — fora do escopo deste documento |

**Skill não introduz nenhum novo eixo do Domain Model.** Ela ocupa integralmente a categoria já nomeada em Domain Model §3 (`Operational Component`), com `identity.component_type = Skill` como único diferenciador — exatamente o mesmo mecanismo pelo qual Kernel §9 (Extension Model) já permitiu Workflow, Standard e Policy sem alterar o Kernel.

---

## 2. Objetivos

| # | Objetivo | Como este documento o realiza |
|---|---|---|
| O1 | Formalizar a menor unidade executável do Framework sem introduzir mecanismo novo | Prova exaustiva de reuso, §4 a §16 |
| O2 | Dar a Templates (Template Architecture) um portador concreto e nomeado | §6 |
| O3 | Fechar o forward-reference de Validation & Certification §7 ("Skill: casos de teste funcionais contra Contract declarado") | §7.3 |
| O4 | Demonstrar que Composition, Workflow, Execution, Standards, Policy e Registry operam sobre Skill sem qualquer ramo condicional específico | §15 |

---

## 3. Escopo

### 3.1 Pertence

Estrutura do Manifest de uma Skill; mapeamento de Input/Output/Prompt Template (Template Architecture) sobre `Inputs`/`Outputs` (Kernel §2.4-§2.5); fluxo de execução ponta a ponta de uma Skill invocada por Composition/Workflow/Execution; especialização do critério de Certificação já anunciado para `component_type=Skill`.

### 3.2 Não pertence — com justificativa

| Excluído | Justificativa |
|---|---|
| Orquestração de múltiplas Skills sob autonomia decisória | Agent Architecture (futuro) — Skill é invocada, não orquestra sob Role própria |
| Mecanismo de registro, descoberta, versionamento, certificação, composição, execução | Já integralmente definidos por Registry, Identity, Validation & Certification, Composition, Execution — Skill apenas os consome com `component_type=Skill` como filtro, nunca os redefine |
| Estrutura interna de Templates | Template Architecture — Skill apenas referencia `templates[]`, já especificado |
| Autoridade de aprovação | Governance §7/§8 — nenhuma autoridade nova |

---

## 4. Modelo Conceitual

### 4.1 Prova de minimalidade — tabela de proveniência

**Este documento introduz zero Value Objects, zero Artifacts, zero relações.** Toda linha abaixo é "Reutilizado", sem exceção.

| Conceito usado por Skill | Definido em |
|---|---|
| `Component`, `Identity`, `Coordinate`, `Manifest`, `Contract` | Kernel §1-§2 |
| `Lifecycle` (Draft→Review→Approved→Active→Deprecated→Archived→Removed) | Kernel §3 |
| `Capability`, `Constraint` | Kernel §2.9, §2.10 |
| `Inputs`, `Outputs`, `Dependencies`, `Providers`, `Consumers`, `Compatibility`, `Metadata`, `Validation` | Kernel §2.4-§2.15 |
| `Operational Component` (categoria) | Domain Model §3 |
| `Execution`, `Artifact`, `Evidence`, `Context`, `Context Snapshot` | Domain Model §2; RFC-DM-001 §3.2 |
| `VersionedIdentifier`, Lineage, `supersedes` | Identity & Namespace §4, §7 |
| Registro, descoberta, `manifest_digest` | Registry & Discovery §3.1, §6; Validation & Certification §6 |
| Verificação estrutural, Certificação L0–L4, per-type specialization | Validation & Certification §4, §5, §7 |
| Resolução de Provider, Assembly | Composition §5-§7 |
| `Step`, invocação por Workflow | Workflow §4 |
| Dispatch, Scheduler, Execution Plan | Execution §5 |
| `Standard`, `NormativeRequirement`, `ComplianceTarget` | Standards Architecture §4 |
| `Policy`, `PolicyScope`, `Effective Policy Set` | Policy Architecture §5, §9 |
| `Template`, `Variable`, `Placeholder`, `Expanded Template` | Template Architecture §4 |

`[ESCOLHA DE DESIGN]`

**Motivação:** decidir se Skill exige campos de Manifest próprios (ex.: `skill_category`, `runtime_hint`, `execution_mode`) além dos quinze campos do Component Contract e do `templates[]` já normatizado.

**Alternativas rejeitadas:** (a) introduzir campos específicos de Skill no Manifest; (b) criar um `component_type` refinado (`Skill.Generative`, `Skill.Deterministic`) para distinguir Skills baseadas em modelo generativo das puramente funcionais.

**Justificativa técnica:** Kernel §2.14 (`Metadata`) já é o campo genérico para categorização e tags sem exigir schema tipado — qualquer distinção de categoria de Skill é expressável ali sem novo campo. Kernel §9 (Extension Model) autoriza conteúdo interno type-specific apenas para a estrutura *como* (Phase/Step, Templates), nunca para novos campos de *interface* — introduzir `skill_category` como campo de primeira classe violaria essa fronteira e obrigaria Registry, Composition e Certification a conhecer um atributo que nenhum dos três precisa para operar corretamente (todos resolvem por `Capability`, não por categoria declarada).

**Precedentes arquitetônicos:** Kubernetes não distingue `Deployment` em subtipos por runtime interno — a variação vive em `spec.template.spec.containers[].image`, dado opaco ao scheduler. OpenAPI não tipifica `Operation` por "gerativo vs. determinístico" — a distinção é implementação, não contrato.

### 4.2 Nomenclatura descritiva não normativa

O termo **"Assinatura de Skill"** é usado neste documento como abreviação de leitura para a combinação de `Inputs` + `Outputs` + `Capabilities` de uma Skill — **não é um construto novo**, apenas um rótulo de conveniência sobre campos já existentes do Component Contract (Kernel §2.4, §2.5, §2.9). Nenhum algoritmo ou validação trata "Assinatura" como entidade separada.

---

## 5. Estrutura do Manifest

| Campo do Component Contract (Kernel §2) | Uso por uma Skill |
|---|---|
| `identity` | `component_type = Skill`; namespace/nome conforme convenção já fixada em Registry §5 (`<ns>/skill.<capacidade>`) |
| `purpose` | Descrição do problema resolvido — sem alteração de semântica |
| `owner` | `Role` — Governance §2-§3, sem alteração |
| `inputs` | Schema declarado; **MAY** ser refinado por `INPUT Template` (§6.1) |
| `outputs` | Schema declarado; **MAY** ser refinado por `OUTPUT Template` (§6.2) |
| `dependencies` / `providers` / `consumers` | Reutilizados sem alteração — uma Skill **MAY** depender de outras Skills, resolvidas por Composition (§9 abaixo) |
| `capabilities` | Vocabulário de Capability exposto — usado por Registry §6.2 e Composition §6-§7 sem modificação |
| `constraints` | Kernel §2.10 — usado também dentro de `Variable.constraint` de Templates (Template §4.2) |
| `version` | SemVer — Kernel §2.11 |
| `lifecycle` | Kernel §3, sem exceção |
| `compatibility` | Kernel §2.13 |
| `metadata` | `standards_bound` (Kernel §2.14) — vínculo a Standards |
| `validation` | Critério de correção — Kernel §2.15 |
| `templates[]` | **Campo adicional já normatizado por Template Architecture §4.2**, não introduzido aqui |

`[ESCOLHA DE DESIGN]`

**Motivação:** decidir se `templates[]` é obrigatório em toda Skill.

**Alternativas rejeitadas:** exigir ao menos um Template por Skill, forçando toda Skill a ser parametrizável.

**Justificativa técnica:** Template Architecture §3.2 não torna `templates[]` obrigatório — uma Skill puramente funcional e determinística (ex.: validação de checksum) não precisa de Prompt/Input/Output Template algum; seus `Inputs`/`Outputs` do Kernel Contract já bastam. Forçar Templates universalmente violaria Constitution (Simplicidade: "a solução mais simples que resolve o problema real é sempre preferível").

**Precedentes arquitetônicos:** em OpenAPI, um `Schema` não exige `example`/`default` — são opcionais, adicionados apenas quando agregam valor.

---

## 6. Contrato da Skill

### 6.1 Como Input Template refina Inputs

O campo `inputs` do Component Contract (Kernel §2.4) declara **o quê** é esperado — forma e tipo. Um `INPUT Template` (Template Architecture §4.3), quando presente, **refina** esse campo adicionando: `Variable` nomeada por campo de entrada, `default_value`, `binding_source`, e `Constraint` (Kernel §2.10) por variável. **Refina, nunca substitui** — a validação estrutural de `inputs` (Kernel §8) continua sendo a autoridade sobre a forma; o Template acrescenta a mecânica de *como um valor concreto é vinculado* a essa forma.

### 6.2 Como Output Template refina Outputs

Simetricamente, um `OUTPUT Template` refina `outputs` (Kernel §2.5) declarando a estrutura do `Artifact` produzido, com `Placeholder`s preenchidos a partir do resultado da Execution. O `Artifact` final **MUST** ser conformante à forma declarada em `outputs` — o Template não relaxa essa exigência, apenas parametriza como o conteúdo é montado dentro dela.

### 6.3 Como Prompt Template participa da execução

Um `PROMPT Template`, quando presente, é expandido (Template Architecture §11.3) **entre `Initiated` e `Running`** da Execution da Skill, produzindo um `Expanded Template` (`Artifact` genérico) que se torna a entrada do processamento efetivo realizado durante `Running`. A expansão em si é determinística (Template §7, TP2); o processamento que a consome durante `Running` **MAY** ser não determinístico (ex.: inferência de modelo generativo) — distinção já formalizada e não reaberta aqui.

### 6.4 Como Capabilities são declaradas

Sem alteração: `capabilities[]` (Kernel §2.9) — usado por Registry §6.2 (`search(capability)`) e por `ResolveSlot` (Composition §7) exatamente como para qualquer Component.

### 6.5 Como Constraints são utilizadas

Sem alteração: `constraints[]` no nível do Contract (Kernel §2.10) restringe condições gerais de uso da Skill; `Variable.constraint` (Template §4.2) restringe valores individuais de parâmetro — mesmo construto, dois pontos de uso já normatizados.

---

## 7. Modelo Operacional

Toda operação sobre uma Skill é a operação genérica já definida, filtrada por `component_type = Skill`. Nenhuma nova assinatura de operação é introduzida.

| Operação | Definida em | Especialização para Skill |
|---|---|---|
| Admissão / aprovação | Governance §7 | Nenhuma — processo idêntico a qualquer Component |
| Verificação estrutural | Kernel §8 | `inputs`/`outputs`/`templates[]` validados por Kernel §8 + Template §9 (`validate_template_definition`) |
| Registro | Registry & Discovery §5 | `register(manifest, decision_record_ref)`, sem alteração |
| Descoberta | Registry & Discovery §6.2 | `search(capability)` — mesma operação já exemplificada em Registry §6.2 com `core/skill.static-analysis.sql-injection-scan` |
| Resolução de dependência/Provider | Composition §5-§7 | `ResolveSlot` — Skill é candidato elegível como qualquer Component |
| Certificação | Validation & Certification §5 | Ver §7.3 abaixo — fecha o forward-reference já existente |
| Dispatch/Execução | Execution §5 | `Dispatch(step)` — sem alteração |
| Avaliação normativa | Standards §10; Policy §10 | `applies_to`/`applies_at = MANIFEST\|EXECUTION\|ARTIFACT`, sem novo valor de enum |

### 7.3 Fechamento do forward-reference de Certificação

Validation & Certification §7 já declarava, antes deste documento existir: *"Skill: Casos de teste funcionais contra Contract declarado — Corretude de I/O."* Este documento fornece o mecanismo concreto, sem alterar aquele critério:

> Para uma Skill, `Testing` (Validation & Certification §4) **MUST** consistir em uma ou mais `Execution`s da própria Skill sob `Input` variados, cujos `Artifact`s resultantes são comparados contra `outputs` (refinado, quando presente, por `OUTPUT Template`). Cada Execution de teste produz `Evidence` (Domain Model §13) via `Evaluation Method` do tipo `DYNAMIC` (Standards §4.6). Reprodutibilidade (L4, Validation & Certification §6) exige que `deterministic_expansion = true` (Template §7, TP2/TP10) para todo Template envolvido — sem isso, a Evidence de teste não é reprodutível e L4 **MUST NOT** ser concedido (mesma regra já estabelecida em Standards §14/E19).

---

## 8. Fluxo de Execução

```
1. Workflow declara Step com Composition Slot (capability=X, min_certification_level=L2)     [Workflow §4]
2. Composition Resolver resolve Slot → Skill@version concreta                                  [Composition §7]
3. Execution.Dispatch(step)                                                                     [Execution §5]
   a. Context{ orchestration_id, phase_id, step_id, attempt } montado
   b. Context Snapshot capturado                                                                [RFC-DM-001 §3.2]
   c. Execution → Initiated → Running
4. SE Skill possui templates[]:
   a. Template.ResolveEffectiveTemplate(qualified_id)                                           [Template §11.1]
   b. Template.BindVariables(params=Step.params, ctx_snapshot, assembly)                         [Template §11.2]
   c. Template.Expand(...) → ExpandedTemplate (Artifact)                                         [Template §11.3]
5. Processamento efetivo da Skill consome (Inputs refinados | ExpandedTemplate)
6. Skill produz Artifact conforme outputs (refinado por OUTPUT Template, se presente)             [Kernel §2.5]
7. Execution → Completed | Failed | Aborted                                                       [Domain Model §8]
```

Nenhum passo acima introduz operação nova — é composição sequencial de algoritmos já publicados.

---

## 9. Algoritmos

**Nenhum algoritmo novo é necessário.** O fluxo de §8 é formalizado abaixo como **orquestração pura** de chamadas a algoritmos já definidos — prova de que Skill não exige lógica própria.

```
ALGORITMO InvokeSkillStep(step, ctx, at):
  slot_result ← Composition.ResolveSlot(step.slot, requester_ns)          # Composition §7
  SE slot_result é SlotError: RETORNA Falha(slot_result)

  skill_ref ← slot_result                                                   # VersionedIdentifier
  exec ← Execution.Dispatch(step, orchestration_id, attempt=0)              # Execution §7
  # exec já inclui: Context{...}, captura de Context Snapshot, Initiated→Running

  SE Registry.resolve(skill_ref).manifest.templates ≠ ∅:
     eff_tpl ← Template.ResolveEffectiveTemplate(skill_ref#template.<kind>)  # Template §11.1
     bindings ← Template.BindVariables(eff_tpl, step.params,
                                        exec.context_snapshot, slot_result.assembly)  # Template §11.2
     expanded ← Template.Expand(eff_tpl, bindings)                          # Template §11.3
     # expanded torna-se insumo do processamento de exec

  resultado ← ProcessamentoEfetivoDaSkill(exec, expanded?)   # opaco a este documento — Execution §5, "Running"
  artifact ← Materialize(resultado CONFORME skill_ref.manifest.outputs)     # Kernel §2.5
  exec.transition(Completed)                                                # Domain Model §8
  RETORNA artifact
```

### 9.1 Detecção de Breaking Change — reuso composto

```
ALGORITMO ClassifySkillChange(prev, next):
  contract_class ← Kernel§2.13.ClassifyCompatibility(prev, next)      # já existente — Kernel/Identity §7
  template_classes ← [ Template.ClassifyTemplateChange(prev, next, tid)   # Template §11.4
                        PARA CADA tid EM UnionDeTemplateIds(prev, next) ]
  RETORNA Max(contract_class, template_classes)   # o mais restritivo entre os dois domina
```

`[ESCOLHA DE DESIGN]`

**Motivação:** decidir se Skill precisa de um algoritmo próprio de classificação de mudança (`ClassifySkillChange` como lógica original) ou se é composição das duas já existentes.

**Alternativas rejeitadas:** replicar a lógica de `ClassifyTemplateChange` (Template §11.4) diretamente dentro de um algoritmo específico de Skill, adaptando-a a particularidades supostas de Skill.

**Justificativa técnica:** não existe nenhuma particularidade de Skill que a lógica genérica de compatibilidade de Contract (Kernel §2.13) e de Template (Template §11.4) já não cubram — uma mudança de `inputs`/`outputs` é compatibilidade de Contract; uma mudança de `Variable`/`Placeholder` é compatibilidade de Template. `Max()` sobre os dois resultados (usando a mesma ordem MAJOR > MINOR > PATCH já definida em Standards §7.1) é suficiente e não introduz nova regra de classificação.

**Precedentes arquitetônicos:** a mesma técnica de composição de classificadores já foi usada, sem alarde, ao longo de toda a base — `ClassifyStandardChange` (Standards §12.2) e `ClassifyTemplateChange` (Template §11.4) são estruturalmente isomórficos por design, precisamente para permitir esse tipo de composição sem duplicação.

---

## 10. Diagramas

### 10.1 UML — Skill como especialização

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
       │     Skill      │   identity.component_type = Skill
       │                │   (nenhum atributo além do Contract padrão)
       └───────┬───────┘
                │0..*
                ▼
         templates[] : Template   [Template Architecture §4 — reutilizado, não redefinido]
```

### 10.2 Sequência — invocação completa

```
Workflow(Step)   Composition      Registry     Execution        Template          Skill(runtime)
     │                │              │             │                │                  │
     ├─ResolveSlot────►│              │             │                │                  │
     │                ├─search(cap)─►│              │                │                  │
     │                │◄─candidates──┤              │                │                  │
     │◄─skill_ref──────┤              │             │                │                  │
     │                                              │                │                  │
     ├─Dispatch(step)──────────────────────────────►│                │                  │
     │                                    Context+Snapshot [RFC-DM-001 §3.2]             │
     │                                    Initiated→Running           │                  │
     │                                              │                │                  │
     │              opt templates[] ≠ ∅              │                │                  │
     │                                              ├─ResolveEffectiveTemplate──────────►│
     │                                              │◄────────────────────────────────────┤
     │                                              ├─BindVariables──────────────────────►│
     │                                              │◄────────────────────────────────────┤
     │                                              ├─Expand──────────────────────────────►│
     │                                              │◄─ExpandedTemplate(Artifact)──────────┤
     │                                              │                                       │
     │                                              ├─────────────────processamento───────►│
     │                                              │◄─resultado────────────────────────────┤
     │                                              ├─Materialize(outputs)                  │
     │                                              ├─Completed                             │
     │◄─artifact────────────────────────────────────┤                                       │
```

### 10.3 Estados

Idêntico ao Kernel Lifecycle (Kernel §3), sem exceção — reprodução proibida por ser duplicação (mesma disciplina já aplicada em todos os documentos anteriores, Standards §11.4, Policy §12.4, Template §10.3).

---

## 11. Casos Extremos

| # | Caso | Tratamento |
|---|---|---|
| S1 | Skill sem `templates[]` | Válido — `inputs`/`outputs` do Kernel Contract bastam (§5, ESCOLHA DE DESIGN) |
| S2 | Skill apenas com `OUTPUT Template`, `inputs` fixo | Válido — refinamento é independente por lado (§6.1/§6.2) |
| S3 | Skill referenciada por Coordinate sem versão em um Slot | Rejeitado pela própria Composition §7 (`ResolveSlot` exige `version_range`, nunca Coordinate nu) — nenhum tratamento especial de Skill necessário |
| S4 | Dependência circular entre Skills via `depends_on` | `Kernel§7.CycleDetection` — mesma aplicação já usada para qualquer Component |
| S5 | Certificação da Skill degrada (`Suspended`) durante uma Execution de Workflow em curso | Resolução de Assembly já ocorreu no dispatch; Execution em curso não é afetada — mesma regra de imutabilidade já aplicada em Policy §14/F8 |
| S6 | `PROMPT Template` com Variable `required` sem binding disponível | `BindingError(REQUIRED_VARIABLE_UNBOUND)` — Execution **MUST NOT** avançar a `Running` (Template §14/G5), propagado sem alteração |
| S7 | Skill declarada como Provider de si mesma (auto-dependência) | Rejeitado por `Kernel§7.CycleDetection` — caso trivial do mesmo mecanismo |
| S8 | Artifact produzido não conforma a `outputs` mesmo após expansão de `OUTPUT Template` | Execution **MUST** transitar a `Failed` — violação de Contract, tratada por Execution §9 (Failure Policy), sem regra nova |

---

## 12. Performance

| Recurso | Regra de cache/complexidade | Origem |
|---|---|---|
| Resolução de `Skill@version` | Cache indefinido | Registry §8 |
| Resolução de Assembly contendo a Skill | Cache indefinido enquanto Slots não mudarem | Composition §10 |
| `ResolveEffectiveTemplate` | Cache indefinido por `(template_digest)` | Template §12 |
| `Expand` | Cache indefinido por `(template_digest, bindings_digest)` | Template §12 |
| Effective Policy Set aplicável | Cache com TTL/invalidação por evento, nunca indefinido | Policy §15.1 |

**Nenhuma política de cache nova.** A composição das políticas acima é suficiente porque cada camada já resolve seu próprio invariante de imutabilidade (Manifest imutável — Kernel §8; Context Snapshot imutável — RFC-DM-001 §3.2).

---

## 13. Eventos

**Skill não define nenhum tipo de evento próprio.** Tabela de eventos existentes aplicáveis, filtrados por `component_type = Skill`:

| Evento | Origem | Ocorre quando |
|---|---|---|
| `ComponentRegistered` | Registry §11 | Admissão de uma nova Skill |
| `VersionPublished` | Registry §11 | Nova versão da Skill |
| `AssemblyResolved` | Composition §11 | Skill resolvida como Provider |
| `StepDispatched` / `StepCompleted` / `StepFailed` | Execution §11 | Invocação da Skill dentro de um Workflow |
| `TemplateExpanded` | Template §16 | Expansão de Prompt/Input/Output Template da Skill |
| `EffectiveRequirementsResolved` | Standards §16 | Avaliação normativa sobre o Manifest da Skill |
| `EffectivePolicySetResolved` | Policy §16 | Avaliação de aplicabilidade sobre a Skill |

---

## 14. Regras Normativas (RFC 2119)

| # | Regra | Nível |
|---|---|---|
| SK1 | Skill MUST ser `identity.component_type = Skill`, um `Operational Component` (Domain Model §3) | MUST |
| SK2 | Skill MUST NOT introduzir campo de Manifest além dos quinze do Component Contract e de `templates[]` | MUST NOT |
| SK3 | Skill MUST possuir Identity, Coordinate, Manifest e Lifecycle idênticos a qualquer Component | MUST |
| SK4 | `INPUT`/`OUTPUT Template`, quando presentes, MUST refinar — nunca substituir — `inputs`/`outputs` | MUST |
| SK5 | Skill MAY não declarar nenhum Template | MAY |
| SK6 | Certificação de Skill MUST usar `Evaluation Method = DYNAMIC` com Evidence de Execution real | MUST |
| SK7 | L4 de uma Skill com Template MUST exigir `deterministic_expansion = true` em todo Template envolvido | MUST |
| SK8 | Skill MUST NOT ser registrada, descoberta, versionada, certificada, composta ou executada por mecanismo distinto dos já definidos | MUST NOT |
| SK9 | Artifact produzido MUST conformar a `outputs`, refinado ou não por Template | MUST |
| SK10 | Classificação de Breaking Change de Skill MUST ser o máximo entre a classificação de Contract e a de cada Template | MUST |

---

## 15. Integrações

| Documento | Como Skill o consome — sem alteração |
|---|---|
| **Kernel** | Skill é Component pleno — §1-§15 aplicam-se sem exceção; §9 habilita `templates[]` |
| **Governance** | Admissão, aprovação, deprecação — §7/§8/§16, sem processo paralelo |
| **Domain Model v1.1.0** | Skill = Operational Component (§3); Execution/Artifact/Evidence sem alteração |
| **RFC-DM-001** | Context Snapshot (§3.2) obrigatório antes de `Running` |
| **Identity & Namespace** | Coordinate, Versioned Identifier, Lineage — §4, §7, sem exceção |
| **Registry & Discovery** | Registro e descoberta por Capability — §5, §6.2, exemplo já dado com Skill em §6.2 |
| **Validation & Certification** | L0-L4 — §5; especialização de Skill em §7 fechada por este documento (§7.3) |
| **Composition** | `ResolveSlot` trata Skill como candidato elegível igual a qualquer Component — §5-§7 |
| **Workflow** | `Step` invoca Skill via Slot resolvido — §4, sem tratamento condicional por tipo |
| **Execution** | Dispatch, Context Snapshot, Lifecycle — §5, sem alteração |
| **Standards** | `ComplianceTarget.component_types` inclui `Skill` sem novo valor de enum — §4.5 |
| **Policy** | `scope.component_types = [Skill]` restringe aplicabilidade — §5.2 |
| **Template Architecture** | `templates[]`, Variable, Placeholder, Expansion — §4, §7, §11 |

---

## 16. Validação Institucional

| Documento base | Resultado |
|---|---|
| Constitution | **PASS** |
| Kernel | **PASS** |
| Governance | **PASS** |
| Domain Model v1.1.0 | **PASS** — zero entidades/relações/estados |
| RFC-DM-001 | **PASS** |
| Identity & Namespace | **PASS** |
| Registry & Discovery | **PASS** |
| Validation & Certification | **PASS** — fecha forward-reference de §7 |
| Composition | **PASS** |
| Workflow | **PASS** |
| Execution | **PASS** |
| Standards | **PASS** |
| Policy | **PASS** |
| Template Architecture | **PASS** |
| **Exige RFC?** | **NÃO** |

**Prova formal de que Skill não adiciona:**

| Item vedado pelo mandato | Verificação |
|---|---|
| Nova entidade | Nenhuma — §4.1, tabela completa de proveniência, toda linha "Reutilizado" |
| Novo estado | Nenhum — §10.3, Lifecycle idêntico ao Kernel |
| Novo lifecycle | Nenhum |
| Novo Registry | Nenhum — §15, Registry §5/§6.2 reutilizados sem modificação |
| Novo sistema de versionamento | Nenhum — Identity §7 reutilizado |
| Nova Authority | Nenhuma — Governance §7/§8 |
| Novo mecanismo de Discovery | Nenhum — Registry §6.2 |
| Novo mecanismo de Policy | Nenhum — Policy §5.2/§10 |
| Novo mecanismo de Standards | Nenhum — Standards §4.5/§10 |
| Novo mecanismo de Validation | Nenhum — Validation & Certification §4/§5; §7.3 apenas fecha lacuna já anunciada |
| Novo mecanismo de Composition | Nenhum — Composition §5-§7 |
| Novo mecanismo de Execution | Nenhum — Execution §5, §7 |

---

## 17. Dependências Futuras

| Consumidor | O que consome | Estado |
|---|---|---|
| **Agent Architecture** (próximo) | Skill como unidade invocável sob orquestração de Role; `PROMPT Template` como base para instrução de Agent; achado H2 (separação de funções) a fechar no caso geral | **Desbloqueado** |
| **Organization & Tenancy** | Skills escopadas por `org.<id>` via Identity §8/§10, já suportado | Sem bloqueio |
| **Observability & Provenance Storage** | Séries de `StepCompleted`/`StepFailed` de Skills em escala | `[LACUNA proposital]` já declarada em Execution §14 |
| **Testing Architecture** | Formalização de geração de casos de teste a partir de `Variable.constraint` (Template) para Evidence `DYNAMIC` de Skill (§7.3) | `[LACUNA proposital]` |

---

## 18. Critério de Aceitação

### ✔ Checklist Institucional

| Critério do mandato | Status |
|---|---|
| Skill é Component | ✔ §1, §4 |
| Possui Identity, Coordinate, Manifest, Lifecycle do Kernel | ✔ §5 |
| Pode possuir Templates | ✔ §5, §6 |
| Pode declarar Capabilities e Constraints | ✔ §6.4, §6.5 |
| Produz Artifacts | ✔ §6.2, §8 |
| É Executável, Registrável, Descobrível | ✔ §7, §8, §15 |
| Zero entidades/relações/lifecycle/Registry/versionamento/Authority/Discovery/Policy/Standards/Validation/Composition/Execution novos | ✔ §16, prova item a item |
| Nenhuma RFC necessária | ✔ §16 |
| UML, sequência, algoritmos, casos extremos, RFC2119, complexidade, cache, digest, breaking change | ✔ §9-§14 |

### ✔ Evidência de Reutilização de Todos os Documentos

Constitution (princípios), Kernel (§1-§15), Governance (§7-§8, §16), Domain Model v1.1.0 (§3, §8, §12-13), RFC-DM-001 (§3.2), Identity & Namespace (§4, §7), Registry & Discovery (§5, §6.2, §8), Validation & Certification (§4-§7), Composition (§5-§7, §10), Workflow (§4), Execution (§5, §7), Standards (§4.5, §10), Policy (§5.2, §10), Template Architecture (§4, §7, §11, §12) — **todos citados nominalmente e aplicados sem modificação** ao longo deste documento.

### ✔ Confirmação Explícita

**Nenhum documento da base normativa foi alterado.** Skill Architecture é, por construção e por prova exaustiva, o documento de menor superfície de mudança institucional desta série — não introduz um único Value Object, Artifact, relação, estado ou algoritmo que não existisse antes de sua redação.

### ✔ Próximo Documento Desbloqueado

**Agent Architecture** pode agora ser escrito sem qualquer dependência pendente: Skill já define a unidade invocável que um Agent orquestrará sob Role, e Policy §6/§19 já reserva `scope.roles` como o mecanismo que restringirá quais Roles um Agent pode ocupar — pré-requisito estrutural para fechar o achado H2 no caso geral.
