# BLOCO 3 — Composition · Workflow · Execution Architecture
### Framework Eng — Resolução Definitiva do Achado H6

*Base normativa (imutável): Constitution · Kernel · Governance · Domain Model v1.1.0 · RFC-DM-001 · Identity & Namespace · Registry & Discovery · Validation & Certification*

**Decisão arquitetural que atravessa os três documentos**, declarada uma única vez aqui para não ser repetida três vezes:

> `[ESCOLHA DE DESIGN — a mais importante deste bloco]` H6 é resolvido **sem nenhuma nova entidade e sem nenhuma nova relação no Domain Model**. Correlação entre uma orquestração e suas Executions filhas é carregada como **conteúdo semântico dentro de `Context`** (já genérico por definição — Domain Model §2, entidade #5), nunca como uma aresta `composed_of` nova. Precedente direto: **W3C Trace Context / OpenTelemetry Semantic Conventions** definem `trace_id`/`parent_span_id` como *atributos padronizados de conteúdo*, não como alteração ao modelo de dados de `Span`/`Resource`. Alternativa descartada: introduzir `Execution.composed_of → Execution` como relação nova no Domain Model — rejeitada porque exigiria RFC-DM-002 para resolver algo que a genericidade já-existente de `Context` resolve sem tocar em nenhum documento ratificado. Estrutura de Phase/Step/Gate/Branch é modelada como **Value Object escopado ao Contract** do Component tipo Workflow — mesmo padrão já estabelecido para `Capability` (Identity & Namespace §2.2) — habilitado por Kernel §9 (Extension Model: o Contract declara o *quê*, nunca o *como*; Phase/Step é o *como* interno de um Workflow, exatamente como um prompt é o *como* interno de um Skill).

---
---

# DOCUMENTO 1 — Composition Architecture

## 1. Posição Arquitetural

Composition Architecture **estende operacionalmente Kernel §10** (que já distingue `Dependency` de `Provider` em prosa) para um mecanismo de resolução completo. Sua responsabilidade institucional: **decidir, de forma determinística e auditável, quais Components concretos satisfazem os requisitos declarados de outro Component.** Ela não executa nada (isso é Execution Architecture) e não declara estrutura temporal/orquestração (isso é Workflow Architecture) — ela resolve **grafos estáticos de composição**, ponto.

**Fronteira:** Composition termina no momento em que produz uma `Assembly` resolvida. Não decide *quando* nem *em que ordem* os Providers resolvidos são invocados.

## 2. Objetivos e Motivação

Resolver, de forma central e reutilizável por Workflow/Execution/Certification, o problema já antecipado por Kernel §10 mas nunca operacionalizado: como um `Component` que declara "preciso de uma Capability X" (não um Coordinate fixo) obtém, de forma reprodutível, um Provider concreto — incluindo entre organizações, entre versões incompatíveis, e com Providers opcionais/condicionais.

## 3. Escopo

**Pertence:** resolução de `depends_on`/`provides_for` abstratos (por Capability) a Coordinates concretos; Assembly; composição hierárquica; composição cross-namespace; contratos de slot de composição.

**NÃO pertence (com justificativa):**
- *Ordem temporal de invocação* — pertence a Workflow Architecture, porque composição é sobre "o quê", não "quando".
- *Execução física dos Providers resolvidos* — pertence a Execution Architecture; Composition nunca invoca nada, apenas resolve referências.
- *Critério normativo de qual Standard/Policy um Provider deve obedecer* — pertence a Standards/Policy Architecture (futuro); Composition apenas consulta o nível de Certificação já emitido (Fase 4), não o calcula.

## 4. Modelo Conceitual

| Conceito | Natureza | Base |
|---|---|---|
| `depends_on` | **Reutilizado** | Domain Model §5 / Kernel §2.6 |
| `provides_for` | **Reutilizado** | Domain Model §5 / Kernel §2.8 |
| **Composition Slot** | **Novo construto interno** (Value Object, escopado ao Contract de quem o declara — sem identidade própria, sem RFC) | Análogo a `Capability` (Identity §2.2) |
| **Assembly** | **Novo construto interno**, modelado como `Artifact` genérico (Domain Model §2, entidade #7) — nenhuma especialização nova | Produzido por uma `Execution` do Resolver |
| Resolução cross-namespace | **Reutilizado** | Identity & Namespace §10 |
| Nível mínimo de Certificação como critério | **Reutilizado** | Validation & Certification §5 |
| Busca por Capability | **Reutilizado** | Registry & Discovery §6.2 |
| Detecção de ciclo | **Reutilizado (3ª aplicação do mesmo mecanismo)** | Kernel §7 → já reaplicado em RFC-DM-001 §3.3 (`derives_from`) e Validation & Certification §7 (grafo de Workflow) |

**Composition Slot — estrutura formal:**
```
Slot {
  required_capability: CapabilitySignature   (Kernel §2.9)
  version_range: SemVerRange                  (Kernel §2.13)
  min_certification_level: L0..L4             (Validation & Certification §5)
  cardinality: EXACTLY_ONE | ONE_OF_MANY | ALL_OF_MANY
  optional: boolean
  condition: Predicate<Context>? (para composição condicional)
  pinned_coordinate: VersionedIdentifier?      (override explícito — ignora resolução por Capability)
}
```

## 5. Modelo Operacional

**Serviço:** `Composition Resolver` (substrato, não-Component, mesma classe arquitetural do Registry — Fase 3 §1).

```
resolve_assembly(component_coordinate) → Assembly | CompositionError
  PRE:  component_coordinate está em lifecycle_state ∈ {Approved, Active}
  POST: Assembly é um Artifact imutável, produzido por uma Execution do Resolver,
        referenciando exatamente um Coordinate resolvido por Slot (ou erro nomeado)

resolve_slot(slot: Slot, requester_namespace) → VersionedIdentifier | SlotError
  PRE:  slot.required_capability é bem formado
  POST: resultado satisfaz slot.version_range E certification_level ≥ slot.min_certification_level
        E, se cross-namespace, referência é totalmente qualificada (Identity §4.5)
```

**Invariante central:** uma `Assembly` publicada **MUST** ser imutável — mudar qualquer resolução exige uma nova Assembly (nunca mutação in-place), espelhando a imutabilidade de Manifest (Kernel §8).

## 6. Diagramas

### 6.1 Composição hierárquica (UML simplificado)
```
Workflow ──provides_for──► Agent ──provides_for──► Skill ──depends_on──► Skill
   │                          │
   └── Slot(cap=X) ───────────┘   (resolvido via Composition Resolver, não por posse)
```

### 6.2 Fluxo de resolução
```
Owner -> Resolver : resolve_assembly(coordinate)
Resolver -> Kernel Manifest : ler Slots declarados
loop para cada Slot:
  Resolver -> Registry : search(capability, version_range)
  Registry --> Resolver : candidates[]
  Resolver -> Validation&Certification : filter(candidates, min_level)
  Resolver -> Resolver : aplicar policy de seleção (maior certificação > maior versão > pin explícito)
  alt nenhum candidato:
    Resolver --> Owner : SlotError(unsatisfied) [a menos que slot.optional]
Resolver -> Resolver : verificar ciclo no grafo composto (Kernel §7)
Resolver -> Resolver : produce Assembly (Artifact)
Resolver --> Owner : Assembly
```

## 7. Algoritmos

```
ALGORITMO ResolveSlot(slot, requester_ns):
  candidates = Registry.search(slot.required_capability)
  candidates = filter(c in candidates: c.version in slot.version_range)
  candidates = filter(c in candidates: Certification.level(c) >= slot.min_certification_level)
  IF slot.pinned_coordinate present:
     candidates = [slot.pinned_coordinate] ∩ candidates   # pin nunca ignora critérios mínimos
  IF empty(candidates):
     RETURN slot.optional ? SKIPPED : SlotError(UNSATISFIED)
  IF cross_namespace(candidates[0], requester_ns):
     assert fully_qualified_reference()                    # Identity §10
  RETURN select_best(candidates)   # highest certification, then highest semver

ALGORITMO DetectCompositionCycle(assembly_graph):
  REUSA Kernel§7.CycleDetection(assembly_graph)             # nenhuma reimplementação
```

## 8. Integrações

| Documento | Contrato |
|---|---|
| Constitution | Reuso máximo (princípio "menos é mais"); nenhuma entidade nova. |
| Kernel §7, §9, §10 | Extensão direta, sem contradição. |
| Governance | Resolução de Assembly **não é** uma Decision — é um cálculo determinístico; só a Admission do Component *composto* passa por Governance. |
| Domain Model | Assembly = `Artifact` genérico; nenhuma entidade nova. |
| Identity & Namespace | Toda referência resolvida é uma Versioned Identifier totalmente qualificada (§4.5). |
| Registry | Fonte exclusiva de candidatos (`search`/`list`). |
| Validation & Certification | Fonte exclusiva do critério `min_certification_level`. |

## 9. Casos Extremos

| Caso | Tratamento |
|---|---|
| Diamond dependency (dois Slots exigem versões incompatíveis do mesmo Coordinate) | `CompositionInvalid` — **MUST NOT** resolver silenciosamente; erro nomeado com os dois Slots conflitantes. |
| Provider resolvido depois torna-se `Archived` | Detectado via Tombstone do Registry (Fase 3 §6.1); Assembly antiga permanece válida (imutável) até nova resolução ser solicitada. |
| Slot opcional sem candidato | `SKIPPED`, não é erro. |
| Composição cross-org sem qualificação explícita | Rejeitada estruturalmente — Identity §10 já proíbe resolução implícita cross-namespace. |
| Múltiplos candidatos empatados em certificação e versão | Desempate determinístico por ordem lexicográfica de Coordinate (nunca aleatório — auditabilidade). |

## 10. Performance

Resolução é **cacheável por Assembly completa** enquanto nenhum Slot envolvido mudar de versão/certificação (mesma lógica de cache do Registry, Fase 3 §8). Paralelizável por Slot (Slots independentes resolvem concorrentemente). Particionamento herda o particionamento por Namespace do Registry (Fase 3 §10) — nenhum mecanismo novo de escalabilidade é necessário.

## 11. Eventos

`AssemblyResolved`, `AssemblyResolutionFailed`, `SlotUnsatisfied`, `CompositionCycleDetected`, `CompositionInvalid` — telemetria operacional (mesma classe de `Registry Event`, não Domain Model Event).

## 12. Regras Normativas

| # | Regra | Nível |
|---|---|---|
| CP1 | Assembly MUST ser imutável uma vez produzida | MUST |
| CP2 | Resolução MUST NOT cruzar Namespace implicitamente | MUST NOT |
| CP3 | Pin explícito MUST ainda satisfazer version_range e min_certification_level | MUST |
| CP4 | Grafo de composição MUST ser acíclico (Kernel §7) | MUST |
| CP5 | Slot opcional não resolvido MUST NOT bloquear a Assembly | MUST NOT (block) |
| CP6 | Diamond dependency incompatível MUST ser reportado, nunca resolvido silenciosamente | MUST |

## 13. Validação Institucional

| Documento base | Resultado |
|---|---|
| Kernel §10 | **PASS** — estende, não contradiz |
| Domain Model v1.1.0 | **PASS** — zero entidades novas |
| Registry / Certification | **PASS** — consumidor puro |
| Exige RFC? | **Não** |

## 14. Dependências Futuras
Workflow Architecture consome `Slot`/`Assembly` diretamente (Documento 2, §4). Policy Architecture (futuro) poderá restringir quais Namespaces são elegíveis em resolução cross-org — hoje não bloqueante.
