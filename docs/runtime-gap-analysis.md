# Runtime Gap Analysis v1.0
### Framework Eng — Prova de Consistência Institucional entre Documentação e Runtime

*Autor: papel de Arquiteto-Chefe, sessão de revisão pós-implementação · Base analisada: `docs/architecture/01` a `15` (Constitution → Skill Architecture) + RFC-DM-001, comparados linha a linha contra `runtime/` (29 arquivos, ~2.230 linhas, commit `a88b5f5`).*

> Este relatório não implementa nada. Não reescreve nenhum documento institucional. Onde a implementação exigiu uma decisão e a documentação não a define, isso está classificado explicitamente (Editorial / Ambiguidade / Inconsistência / Conceito ausente / RFC necessária) — nunca silenciosamente resolvido nem inflado em problema maior do que é.

---

## 0. Método

Para cada um dos 15 documentos: (a) extraí toda regra normativa (MUST/SHOULD/MAY, algoritmos ALGORITMO, invariantes numerados); (b) localizei a linha exata do runtime que a implementa, ou registrei a ausência; (c) toda divergência encontrada foi checada contra o próprio texto do documento antes de ser listada, para não inventar exigência que o documento não faz.

---

## 1. Cobertura por Documento

| # | Documento | Implementado | Parcial | Não implementado |
|---|---|---|---|---|
| 01 | Constitution | Princípios refletidos em design (reuso, simplicidade, transparência) | — | N/A — Constitution não é mecanismo, é critério |
| 02 | Kernel | Component Contract (15 campos, `contracts/component.py`); Lifecycle + transições (`is_valid_transition`); Manifest uniforme; detecção de ciclo (`contracts/graph.py`) | Discovery (só por Capability, não por `component_type`/tags/Identity+filtros combinados); Validação Estrutural (não checa existência/lifecycle de Dependencies referenciadas) | Ciclo de dependências do próprio grafo `Component.dependencies` (o caso original de §7, antes de Review→Approved); `consumers` (§2.7) nunca populado pelo sistema |
| 03 | Governance | `decision_record_ref` exigido como precondição opaca de `register()` (R1) | — | Tudo o mais — Roles, Decision, Decision Record reais, Admission workflow, RFC process, Audit, Exception, Technical Debt, Conflict Resolution — **por exclusão explícita da tarefa** |
| 04 | Domain Model | Component, Manifest, Execution, Artifact, Evidence, Context, Capability | Role (apenas `str`, não Entity com identidade própria — Identity §2.1 já define Role como tendo identidade); Decision/Decision Record (apenas `str` opaco) | Knowledge, Decision (como entidade real), Metric, Relationship como entidade tipada persistida |
| 05 | RFC-DM-001 | C2 Context Snapshot (`capture_context_snapshot`, obrigatório antes de `Running`); H3 cardinalidade `Component 1:1..*` (`RegistryEntry.lineage` + `current_active()`) | — | C1 (`Knowledge Asset`), C3 (`derives_from` Knowledge→Knowledge), C4 (`measures`/Namespace) — N/A, Knowledge/Metric fora de escopo |
| 06 | Identity & Namespace | `Coordinate`/`VersionedIdentifier` com regex §4.4; `new_instance_identifier()` ULID Crockford Base32; `urn()`; qualificação de Template (`qualified_template_id`) | Redirect chain (segue, mas nada popula `redirect_to`); Tombstone (retorna, mas não impede reatribuição de nome — §3.2) | Alias Table / `create_alias` / resolução por alias (§6 passo 3); "latest" como alias especial; hierarquia `core/`, `org.<id>`, `domain.*`, `env.*`; tokens reservados (§8) |
| 07 | Registry & Discovery | `resolve()` §6.1 (exceto alias); `search()` §6.2 exato; `lineage()`; `register()` com R1 | `publish_version` (não valida `version > max(Lineage)`) | `deprecate()`, `archive()`, `create_alias()`; Registry Events; Integrity Service; Cache |
| 08 | Validation & Certification | Leitura de nível com regra de Integrity (§6: digest mismatch → L0) | — | Pipeline completo (Evidence, scoring multi-dimensão, Certifier humano p/ L4, Suspended/Revoked/Expired, herança PATCH) — **deliberadamente mínimo, já declarado em RUNTIME.md** |
| 09 | Composition | `Slot` (§4, campo a campo); `ResolveSlot` (§7, verbatim); `select_best` com desempate lexicográfico (§9); `detect_composition_cycle` (delega a `graph.py`) | `Assembly` mutável (sem `frozen=True`) apesar de CP1 exigir imutabilidade; diamond dependency (CP6) não verificado entre Slots de uma mesma Assembly | `resolve_assembly(component_coordinate)` como operação de topo — nunca implementada como tal (ver §3.1 abaixo, achado central) |
| 10 | Workflow | `Phase`/`Step`/`FailurePolicy` (§4 + `params`); `validate_workflow_definition` (WF1, WF4, GATE_APPROVAL, WF6); `evaluate_decision_point` (com escopo reduzido já autodeclarado) | `run_workflow` executa apenas INVOCATION e apenas em cadeia linear (`current.next[0]`) | Execução de Branch/Join real (múltiplos `next`); Retry automático; disparo automático de Compensation em falha (`rollback()` existe isolado, nunca chamado por `run_workflow`); Timeout (`timeout_seconds` declarado, nunca checado) |
| 11 | Execution | `Execution`/`Context`/`ContextSnapshot`/`Artifact`/`Evidence`; `Dispatch` (EX2 por construção); `Plan`/`ready_steps` (EX3, paralelismo lógico); `Recover` (EX4) | — | `track_state`/Provenance Service (já declarado `[LACUNA proposital]` no próprio documento); revalidação contra Registry no momento do dispatch; Timeout |
| 12 | Standards | — | — | **100% não implementado** — por exclusão explícita da tarefa |
| 13 | Policy | — | — | **100% não implementado** — por exclusão explícita da tarefa |
| 14 | Template | `ResolveEffectiveTemplate`, `BindVariables`, `Expand`, `ClassifyTemplateChange` (todos §11, verbatim, citados linha a linha) | Cache por `(template_digest, bindings_digest)` — dígeste calculado, cache não implementado (MAY, não MUST); `alias` de reexposição em `includes` (§6.2) não implementado | — |
| 15 | Skill | `InvokeSkillStep` (§9, elaborado para o fluxo de dois momentos PROMPT/OUTPUT) | — | `ClassifySkillChange` (§9.1) — **algoritmo do próprio documento, ausente por completo**; `Kernel§2.13.ClassifyCompatibility` (do qual §9.1 depende) também nunca implementado |

---

## 2. Divergências (documentação → implementação)

Mesmo pequenas, listadas com localização exata:

1. **`ComponentType` como Enum fechado** (`contracts/component.py:56-66`, 5 valores) — Kernel §9 (Extension Model) declara que a extensibilidade vem de validar *forma*, nunca de uma lista fechada de tipos. Pragmatismo aceitável para uma demonstração com 5 tipos conhecidos, mas é, tecnicamente, o oposto do princípio declarado.
2. **`Assembly` mutável** (`composition/resolver.py:65-72`, dataclass simples com `dict` mutável) — Composition §5 CP1: *"uma Assembly publicada MUST ser imutável."* Nenhum `frozen=True`, nenhuma cópia defensiva.
3. **`semver_tuple` duplicado** — `contracts/identity.py:72-74` (método de `VersionedIdentifier`) e `composition/resolver.py:60-62` (`_semver_tuple`, função livre sobre string crua) implementam exatamente a mesma lógica de parsing duas vezes (ver §4).
4. **Certificação modelada como dataclass própria, não como Decision/Decision Record** — Validation & Certification §3 declara explicitamente essa decisão de reuso como *"a decisão arquitetural mais importante deste documento."* `validation/certification.py:34-42` implementa `CertificationGrant` como um dataclass paralelo, não como uma especialização do padrão Decision/Decision Record — forçado pela ausência de Governance no escopo, mas é uma divergência real do desenho ratificado, não apenas uma omissão de escopo.
5. **`decision_record_ref` e `performed_by`/Role como `str` opacos** — Domain Model define Decision Record e Role como entidades com identidade, proveniência e ciclo de vida próprios (Identity §2.1 para Role). O runtime os trata como strings não validadas em toda parte (`registry.py:148`, `execution/model.py:144`, `execution/scheduler.py:78`).
6. **`Qualified Requirement Identifier`** (`contracts/identity.py:113-117`) implementado mas nunca exercitado — Standards não existe no runtime, então essa função é código morto, mantido apenas "por completude" (comentário do próprio arquivo).

---

## 3. Lacunas Institucionais

### 3.1 Composition Architecture — o achado mais relevante deste relatório

**Classificação: Ambiguidade, no limiar de RFC necessária.**

Composition §5 contrata `resolve_assembly(component_coordinate) → Assembly | CompositionError`, com PRE `component_coordinate está em lifecycle_state ∈ {Approved, Active}`. Mas **nenhum documento ratificado** — nem Kernel §2 (os 15 campos do Contract), nem Composition §4 (a estrutura de `Slot`) — declara **em qual campo do Manifest de um Component genérico vivem os `Slot[]` que esse Component declara**. `Slot` só tem um lar concreto e nomeado em **Workflow §4**, como `Step.slot`.

Isso significa que `resolve_assembly(component_coordinate)`, como literalmente contratado em Composition §5, **não é implementável como operação autônoma sobre um Component qualquer** — só é implementável quando os Slots já chegam de fora, mediados por um Workflow Step. O runtime confirma isso na prática: `resolve_assembly` nunca foi implementado como função de topo; `skill/runtime.py:89` monta uma `Assembly` ad hoc de um único slot, sempre a partir do `Slot` de um `Step` de Workflow — nunca a partir de "os slots do próprio Component".

Não é um conceito inexistente (Slot é perfeitamente definido); é a **ausência de um campo declarado** que torne `resolve_assembly` executável fora do contexto de um Workflow. Três resoluções possíveis, nenhuma delas implementada aqui por não ser tarefa desta análise decidir:
- (a) emendar Composition Architecture para declarar que `resolve_assembly` é sempre mediado por um chamador que já possui a lista de Slots (Workflow Step, ou futuramente Agent) — nunca uma operação verdadeiramente standalone; ou
- (b) adicionar um campo aditivo ao Manifest (via Kernel §9 Extension Model, análogo a `templates[]`) nomeando os Slots que um Component declara para si mesmo; ou
- (c) deixar explícito que `resolve_assembly(component_coordinate)` é hoje uma assinatura aspiracional, não implementável literalmente, até que (a) ou (b) sejam decididos.

**Candidato único a RFC formal — ver §7.**

### 3.2 `Step.params` — Workflow §4 vs. Template §5.2 / Skill §9

**Classificação: Inconsistência (cross-documento).** Já identificada e registrada durante a construção do Runtime (`workflow/model.py:4-13`, `RUNTIME.md` §5.1). Template Architecture §5.2 e Skill Architecture §9 referenciam `Step.params` por nome; o struct de `Step` em Workflow §4 não o lista. Repetido aqui por completude do relatório — **candidato a emenda de uma linha**, não a RFC formal (mesmo padrão editorial não-estrutural já usado em RFC-DM-001 §3.5 para o rename de `Domain Steward`).

### 3.3 "Consumers Index" — Kernel §2.7 vs. Registry & Discovery §4

**Classificação: Conceito ausente (implícito, nunca nomeado).** Kernel §2.7 atribui a manutenção de `consumers` (o inverso de `dependencies`) "ao sistema, não ao próprio componente" — mas Registry & Discovery §4 (a tabela de construtos internos: Registry Entry, Alias Table, Redirect Chain, Lineage Index, Registry Event, Cache Entry) nunca nomeia um construto equivalente a um "Consumer/Dependent Index". Diferente do achado 3.1, isto **não é impossível de implementar** — `register()` já tem toda informação necessária (`manifest.dependencies`) para popular o índice inverso sem exigir nenhum conceito novo. Por isso **não** entra na lista de RFCs (§7): é lacuna de nomeação em Registry & Discovery §4, resolúvel por uma emenda aditiva menor (nomear o construto) e por uma linha de implementação no Runtime, nunca por RFC.

### 3.4 Decisões de implementação inevitáveis (Editorial — não lacunas normativas)

Sem exigir mudança em documento algum, porque nenhum documento arbitra uma escolha concreta aqui: algoritmo de hash (`SHA-256`, `registry.py:90-117`), gramática de `version_range` (`*`, `X.Y.Z`, `>=`, `^`, `composition/resolver.py:17-23`), técnica concreta de detecção de ciclo (DFS + pilha de recursão, `contracts/graph.py`). Todos já documentados como tal no próprio código-fonte.

---

## 4. Duplicações

Duas duplicações mecânicas reais, ambas pequenas e ambas com proposta de reuso concreta:

1. **Parsing de SemVer duplicado.** `contracts/identity.py:72-74` (`VersionedIdentifier.semver_tuple()`) e `composition/resolver.py:60-62` (`_semver_tuple`) implementam a mesma lógica (`split(".")` → `tuple[int,int,int]`) de forma independente. **Proposta:** `version_in_range()` (`composition/resolver.py:49-57`) deveria chamar `VersionedIdentifier(Coordinate("x","x"), version).semver_tuple()` ou, mais simplesmente, `contracts/identity.py` deveria expor `parse_semver(version: str) -> tuple[int,int,int]` como função livre, reutilizada pelos dois pontos.

2. **Padrão de digest canônico triplicado.** `manifest_digest()` (`registry/registry.py:90-117`), `template_digest()` (`template/engine.py:188-203`) e `digest_of_bindings()` (`template/engine.py:206-208`) implementam, três vezes, exatamente o mesmo padrão: `dict canônico → json.dumps(sort_keys=True, separators=(",",":")) → sha256 → prefixo "sha256:"`. **Proposta concreta:** extrair `runtime/contracts/digest.py` com uma única `canonical_digest(data: dict) -> str`, usada pelos três pontos — exatamente o mesmo padrão de refatoração já aplicado nesta sessão para a detecção de ciclo (`contracts/graph.py`), só que ainda não replicado aqui.

**Achado positivo, para contraste:** a detecção de ciclo está corretamente deduplicada — um único `detect_cycle()`/`topological_sort()` em `contracts/graph.py`, reutilizado por `composition/resolver.py`, `template/engine.py`, `execution/scheduler.py` e `workflow/engine.py`. É a prova de que o padrão de reuso funciona quando aplicado — só não foi aplicado de forma consistente a digest/semver.

---

## 5. Complexidade (à luz da Constitution)

- **Acoplamento:** a disciplina "nenhum módulo importa para cima" (contracts → registry → validation → composition → template → execution → skill → workflow) se mantém — verificado import por import. `skill/runtime.py` e `workflow/engine.py` são os módulos com mais dependências (9 e 6 imports, respectivamente) — mas isso **reflete fielmente**, não viola, o desenho documentado: Skill Architecture §9 e Workflow's próprio `run_workflow` são, por definição institucional, orquestração pura de tudo abaixo ("nenhum algoritmo novo é necessário"). Alto fan-in aqui é design correto, não acoplamento acidental.
- **Coesão:** alta — cada módulo faz exatamente uma coisa (registry resolve/registra, template resolve/liga/expande). O único ajuste de coesão que já ocorreu nesta sessão (mover `extract_placeholder_names`/`render_mechanico` de privado para público em `template/model.py`, em vez de `template/engine.py` acessar `_PLACEHOLDER_RE` de outro módulo) foi corretamente resolvido antes deste relatório.
- **Reutilização:** inconsistente — excelente para detecção de ciclo (4 reaplicações reais, ver §4), ausente para digest/semver (2 duplicações reais, ver §4). Constitution Valor 5 ("resolver o mesmo problema duas vezes é falha do sistema, não escolha neutra") pede que as duas sejam corrigidas com a mesma disciplina já aplicada ao grafo.
- **Simplicidade:** o runtime erra, quando erra, para o lado de **sub-implementar**, nunca de over-engineering — não há abstração especulativa, não há Certification pipeline completo construído "para o futuro". O risco real não é complexidade excessiva; é um punhado de comportamentos declarados mas inertes (Retry, Compensation, Timeout, Branch/Join) que a Constitution (Valor 4, "nenhuma entrega é aceitável apenas por estar pronta") pediria para ligar ou remover explicitamente, não deixar como código morto silencioso.
- **Dependências:** `Manifest.dependencies` (Kernel §2.6) é declarado e usado pelo `loader.py`, mas nunca resolvido/validado como grafo geral de dependências (distinto da resolução por Capability da Composition) — path genuinamente não percorrido pelo runtime.

---

## 6. Teste da Tese

**A tese institucional do Framework continua válida: SIM.**

Evidência: as 15 seções de "Validação Institucional" dos próprios documentos (uma por documento, PASS em todas, nenhuma exigindo RFC) se sustentaram sob teste real — o Runtime executou, com dado institucional real e já certificado (`core/skill.static-analysis.code-review@1.0.0`), a cadeia completa Registry→Certification→Discovery→Composition→Execution→Template→Artifact→Evidence, em duas rodadas completas, mais 5 verificações de caminho negativo, sem exigir nenhum conceito que não estivesse já em algum dos 15 documentos.

**Onde a tese mostra tensão real (não ruptura):**
1. Composition §5's `resolve_assembly(component_coordinate)` é a única lacuna de especificação genuína encontrada — uma operação contratada cujo insumo (Slots de um Component genérico) não tem lar declarado em nenhum documento (§3.1). Isto é uma tensão de especificação, não uma contradição entre documentos — nenhum dos 15 documentos se contradiz entre si; um deles subespecifica uma operação própria.
2. Um pequeno conjunto de comportamentos que a própria Workflow/Execution Architecture já define algoritmicamente (Retry, Compensation, Branch/Join, Timeout) existe no Runtime como função isolada, mas não está fiada ao orquestrador principal (`run_workflow`) — é uma lacuna de completude de implementação, não de tese: os algoritmos que faltam ligar já existem, ratificados, prontos para compor.

Nenhum dos dois pontos invalida a tese central — "o comportamento pode ser derivado inteiramente da documentação, sem invenção" continua comprovado; o que falta é terminar de compor o que já está escrito, mais uma única cláusula de especificação a fechar em Composition.

---

## 7. Lista de RFCs Necessárias

**Apenas uma.** Por disciplina explícita do pedido ("não criar RFC por melhoria estética, somente quando houver impossibilidade de implementação"), tudo o que é meramente "faltando implementar" (Standards/Policy runtime, wiring de Retry/Compensation/Branch, Consumer Index) foi mantido em Cobertura/Lacunas Institucionais §3.3, não promovido a RFC.

| # | Documento alvo | Escopo da mudança | Por que é RFC e não apenas "implementar" |
|---|---|---|---|
| 1 | **Composition Architecture** (docs/architecture/09) | Declarar, aditivamente, onde vivem os `Slot[]` de um Component genérico (Kernel §9 Extension Model, análogo a `templates[]`) **ou** restringir explicitamente `resolve_assembly` a ser sempre mediado por um chamador (Workflow Step hoje; potencialmente Agent no futuro) que já possui a lista de Slots | Sem essa decisão, `resolve_assembly(component_coordinate)` como contratado em §5 é **literalmente não implementável** de forma standalone — não é falta de código, é falta de especificação de onde o código leria os Slots. Agent Architecture (próximo documento, per Skill §17) provavelmente tropeçaria na mesma pergunta ao decidir como um Agent resolve suas próprias capacidades — resolver agora evita retrabalho quando Agent Architecture for escrita |

---

## 8. Roadmap Recalculado

Ordem que minimiza retrabalho, derivada diretamente dos achados acima — não de preferência genérica:

1. **RFC Composition Architecture (achado §7)** — barato, pequeno, aditivo. Resolver antes de Agent Architecture evitar que o mesmo buraco de especificação seja reaberto (e precise de uma segunda rodada de reconciliação) quando Agent precisar resolver suas próprias capacidades.
2. **Runtime: ligar Standards + Policy** (documentos já ratificados, zero documento novo necessário) — fecha o único buraco de correção *carregando peso real* encontrado neste relatório: `CertificationStore.grant()` hoje concede L3/L4 sem checar Conformance nenhuma (Standards §8.4 exige Strict Conformance para L3; sem Standards/Policy no runtime, isso é inexequível). Prioridade alta porque é uma lacuna de correção, não apenas de cobertura.
3. **Runtime: ligar o que já existe mas está inerte** — `rollback()` disparado por falha de Step (Compensation), execução real de Branch/Join (`Phase.next` com múltiplos alvos), Retry por `FailurePolicy`, Timeout por `Step.timeout_seconds`. Nenhum algoritmo novo — tudo já implementado isoladamente (§1); falta compor.
4. **Agent Architecture** (novo documento) — só depois de (1)-(3): construir Agent sobre um substrato de Composition/Workflow ainda com a lacuna de Slot-declarativo aberta e um motor de Workflow ainda linear duplicaria retrabalho quando Agent precisar de orquestração real e resolução de capacidade própria.
5. **Testing Architecture** (novo documento) — citada como `[LACUNA proposital]` em Standards §19, Skill §17 e Template §19; fecha a peça que falta para uma Certification real (não apenas a leitura mínima atual) produzir Evidence de verdade em vez de ser assertada pela demonstração.
6. **Observability Architecture — implementação em Runtime** (documento 16 já ratificado) — só passa a valer a pena depois de (3)-(4): sem branching/retry/multi-agent real acontecendo, a Timeline intrínseca atual já cobre o que há para observar; Observability ganha sentido quando há órbita de execução mais rica para consultar.
7. **Tudo o mais** (Memory, Knowledge, Multi-Agent formal, Security, SDK, Marketplace, Organization & Tenancy) — nenhuma pressão de forward-reference encontrada nesta análise; adiável sem custo identificado.

---

## Fechamento

Catorze dos quinze documentos analisados não precisam de nenhuma mudança — o corpus normativo é, na prática observada por esta análise, tão consistente quanto suas próprias seções de "Validação Institucional" já afirmavam. O único ponto genuíno de subespecificação (Composition §5) é pequeno, aditivo, e não contradiz nada já escrito. O restante das lacunas encontradas é, sem exceção, superfície de implementação ainda não construída sobre uma base documental que já a permite — exatamente a distinção que este relatório foi encarregado de preservar.
