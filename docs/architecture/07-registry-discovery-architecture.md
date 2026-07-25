# FASE 3 — Registry & Discovery Architecture
### Framework Eng — A Autoridade Institucional de Resolução

*Versão 1.0.0 · Base: Domain Model v1.1.0, RFC-DM-001, Identity & Namespace Architecture v1.0.0*

---

## 1. Posição Arquitetural

O Registry **não é um banco de dados de componentes**. É o serviço institucional que **implementa operacionalmente** o mecanismo de Descoberta já mandatado por Kernel Architecture §5 e o contrato conceitual já reservado por Identity & Namespace Architecture §9 (`resolve` / `list` / `lineage`).

Distinção arquitetural que governa todo este documento: o **Domain Model é a camada semântica** (o que as coisas *são*); o **Registry é a camada de serviço/infraestrutura** (como se *encontra* e se *resolve* o que existe). Um `Component` não passa a existir porque foi registrado — ele existe porque uma `Decision` de Admission (Governance Architecture §7) o promoveu a `Active` (Kernel §3). **O Registry nunca decide; ele reflete.** Essa fronteira é a regra mais importante deste documento e é reforçada em cada seção abaixo.

`[ESCOLHA DE DESIGN]`: o Registry **não é ele próprio um `Component`** governado pelo Kernel Lifecycle — é parte do substrato institucional, no mesmo plano que o motor de validação do Kernel. Isso evita regressão infinita ("quem registra o Registry?") pelo mesmo motivo que o API server do Kubernetes não é, ele mesmo, um objeto `etcd` comum.

---

## 2. Objetivos e Motivação

**Objetivos:** (a) resolução determinística de qualquer `Identifier` (Identity Architecture §4) ao seu `Component`/`Manifest` canônico; (b) descoberta multi-dimensional (por Namespace, Capability, Classification, Lifecycle) sem depender de navegação manual; (c) autoridade única de Lineage, aliases e redirects; (d) superfície de leitura para status de Certificação (Fase 4).

**Motivação:** Kernel §5 já declara que "um componente que não pode ser descoberto é, para efeitos práticos, equivalente a um componente que não existe." Sem uma arquitetura formal de serviço, essa garantia permanece uma intenção em prosa. Este documento a torna operável.

---

## 3. Escopo

### 3.1 O que o Registry indexa
`Component` e suas subcategorias (`Standard`, `Policy`, `Template`, `Skill`, `Agent`, `Workflow`, `Knowledge Asset`) — entidades **definicionais, versionadas, de baixa cardinalidade relativa e alta taxa de reuso**.

### 3.2 O que o Registry explicitamente NÃO indexa
`Execution`, `Artifact`, `Evidence`, `Knowledge` (instâncias), `Decision Record` (instâncias) — entidades de **escala de log/evento** (milhões, per Domain Model §9 "transitórias/persistentes de alto volume"). Estas exigem características de armazenamento (append-heavy, particionado por tempo) incompatíveis com um índice de descoberta otimizado para leitura de baixa cardinalidade.

`[ESCOLHA DE DESIGN]`, justificada por precedente direto: nem o Docker Hub nem o npm Registry indexam "cada execução de `npm install`" junto com os pacotes — apenas os pacotes (definições). O componente equivalente a "execuções" pertence a um futuro armazém de proveniência (**Execution Ledger**, fora de escopo — ver §"Pontos que ainda exigem documentos específicos" ao final).

**Consequência normativa:** referências a `Execution`/`Artifact`/`Knowledge`/`Decision Record` individuais **MUST** usar o `Instance Identifier` (Identity §4.2) diretamente — nunca passam por resolução via Registry.

---

## 4. Modelo Conceitual e Entidades

Construtos **internos de serviço** — não são novas entidades do Domain Model, não requerem RFC de emenda:

| Construto | Definição | Cardinalidade com Component |
|---|---|---|
| **Registry Entry** | O registro indexado para uma `Coordinate`: estado de Lifecycle (projetado do Kernel, nunca mutado independentemente), Lineage completa, aliases, redirects, tags de Classification, referência de status de Certificação (read-through, Fase 4). | 1:1 com `Coordinate` |
| **Alias Table** | Mapa `(namespace, alias) → Coordinate`, escopado por Namespace (Identity §6.1). | N:1 (vários aliases → um Coordinate) |
| **Redirect Chain** | Aresta `redirects_to` entre Coordinates (Identity §6.4-6.6), com profundidade máxima de 5 saltos. | 1:0..1 por Coordinate |
| **Lineage Index** | Projeção ordenada de `Component "1"—"1..*" Manifest` (RFC-DM-001 §3.6). | 1:N |
| **Registry Event** | Registro imutável de mudança de estado no Registry — análogo operacional aos `Event` objects do Kubernetes: informativo/telemetria, **não** um Domain Model Event Entity. | 1:N por Coordinate |
| **Cache Entry** | Projeção derivada, efêmera, de qualquer construto acima — nunca fonte de verdade. | N/A |

---

## 5. Serviços Internos e APIs Conceituais

| Serviço | Responsabilidade | Quem pode invocar operações de escrita |
|---|---|---|
| **Resolution Service** | Implementa `resolve()` (Identity §6.7). | Leitura: qualquer Role/Component. Escrita: nenhuma (é puramente derivado). |
| **Discovery Service** | Implementa `list()`/`search()` multi-dimensional. | Leitura: qualquer. |
| **Lineage Service** | Implementa `lineage()` e resolução de faixas SemVer. | Leitura: qualquer. |
| **Registration Service** | Cria/atualiza Registry Entry. | **Exclusivamente** invocado pelo Governance Admission/Deprecation Process mediante `Decision Record` válido — nunca por um Owner diretamente. |
| **Event Service** | Emite Registry Events. | Sistema (automático, em toda mutação). |
| **Integrity Service** | Valida referências, detecta ciclos, sinaliza órfãos. | Sistema (automático + sob demanda de Auditoria). |

**APIs conceituais (pré/pós-condições, no estilo do Component Contract do Kernel):**

```
register(manifest, decision_record_ref) → RegistryEntry
  PRE:  decision_record_ref referencia uma Decision de Admission válida (Governance §7)
        E manifest passou em Validação Estrutural (Kernel §8)
  POST: RegistryEntry criado com lifecycle_state = Active
        E Registry Event ComponentRegistered emitido

publish_version(coordinate, manifest, decision_record_ref) → RegistryEntry
  PRE:  coordinate já existe E manifest.version > max(Lineage.versions)
  POST: Lineage estendida (imutável) E "current" recalculado

resolve(reference: Coordinate | VersionedIdentifier | Alias) → ResolvedIdentity | Error
deprecate(coordinate, version, redirect_to?, decision_record_ref) → void
  PRE:  decision_record_ref referencia Decision de Deprecation (Governance §7)
archive(coordinate, version, decision_record_ref) → void
create_alias(namespace, alias, coordinate) → void
  PRE:  alias não coincide com nenhum token reservado (Identity §8)
list(namespace, filters) → Coordinate[]
search(capability | classification | text) → Coordinate[]
lineage(coordinate) → Manifest[]
compatible_versions(coordinate, range: SemVerRange) → Manifest[]
subscribe(filter) → EventStream
```

---

## 6. Algoritmos de Resolução

### 6.1 `resolve()` — algoritmo canônico (formaliza Identity §6.7)

```
1. SE referência já é uma Versioned Identifier totalmente qualificada:
     → verificar existência direta no Lineage Index → retornar (caminho rápido, cacheável)
2. SE referência é uma Coordinate sem versão:
     → resolver "current" (maior versão em lifecycle_state = Active na Lineage)
3. SE referência é um Alias:
     → consultar Alias Table escopada ao Namespace corrente
     → SE não encontrado no namespace corrente, NÃO buscar em outros namespaces (Identity §6.2: sem lookup global implícito)
4. Seguir Redirect Chain até estabilizar:
     → SE profundidade > 5: retornar Error(RedirectLoopExceeded)
     → cada salto é acumulado em resolution_path (retornado ao chamador — nunca oculto, Domain Model §15)
5. SE Coordinate final está em lifecycle_state = Removed:
     → retornar Tombstone{ redirect_to?, removed_at, reason_ref }
6. Retornar ResolvedIdentity{ canonical_urn, lifecycle_state, resolution_path, certification_status }
```

### 6.2 Descoberta por capacidade (Kernel §5 operacionalizado)

```
search(capability="static-analysis.sql-injection") →
  1. Consultar Capability Index (secundário, ver §8)
  2. Filtrar por lifecycle_state ∈ {Active} (default; caller MAY incluir Deprecated explicitamente)
  3. Ordenar por: certification_level DESC, então version DESC
  4. Retornar Coordinate[] + metadados suficientes para decisão sem 2ª consulta
```

Esta é a operação que a Governance Admission Process (Governance §7) **MUST** invocar antes de aprovar qualquer componente novo — é o mecanismo concreto por trás do "gate de deduplicação" já mandatado.

---

## 7. Fluxos e Diagramas

### 7.1 Fluxo de Registro (sequência)

```
Owner -> Governance : submit(Manifest)  [Draft]
Governance -> Registry : search(purpose, capability)   -- dedup gate, Governance §7
Registry --> Governance : candidates[]
Governance -> Governance : Review, Decision (Approve)   [Approved]
Governance -> Registry : register(manifest, decision_record_ref)
Registry -> Registry : create RegistryEntry, update indices, update Lineage
Registry -> EventBus : emit ComponentRegistered
Registry --> Governance : RegistryEntry{state=Active}
```

### 7.2 Fluxo de Depreciação/Redirect

```
Steward -> Governance : initiate Deprecation Decision (Breaking Change, Governance §10)
Governance -> Registry : deprecate(coordinate, version, redirect_to, decision_record_ref)
Registry -> Registry : lifecycle_state → Deprecated, criar Redirect edge
Registry -> EventBus : emit ComponentDeprecated
[janela de transição decorre — Governance §10]
Governance -> Registry : archive(coordinate, version, decision_record_ref)
Registry -> Registry : lifecycle_state → Archived, nome permanentemente reservado (Identity §3.2)
```

### 7.3 Diagrama de Estados — Registry Entry

`[ESCOLHA DE DESIGN]`: o estado de um Registry Entry **é uma projeção 1:1 do Kernel Lifecycle (Kernel §3)** — nunca uma máquina de estados independente. Isso evita exatamente o tipo de duplicação de modelo de estado que a revisão institucional já penalizou noutro contexto (H3).

```
(Kernel Lifecycle)         (Registry Entry — espelho, somente leitura de origem)
Draft/Review/Approved  ──►  [não indexado — invisível à Discovery]
Active                 ──►  Indexed, discoverable
Deprecated             ──►  Indexed, discoverable com aviso, redirect visível
Archived                ──►  Indexed apenas como Tombstone
Removed                 ──►  Tombstone permanente, nome reservado para sempre
```

### 7.4 Diagrama UML — entidades internas

```
┌───────────────┐        ┌───────────────┐
│ RegistryEntry │1──────*│ Manifest (ref) │  (Lineage Index)
└───────┬───────┘        └───────────────┘
        │1
        │
        │0..*         ┌────────────┐
        ├────────────►│ Alias      │
        │             └────────────┘
        │0..1         ┌────────────┐
        ├────────────►│ Redirect   │
        │             └────────────┘
        │0..*         ┌────────────┐
        └────────────►│ RegistryEvent│
                       └────────────┘
```

---

## 8. Armazenamento, Índices e Cache

**Modelo de dados conceitual (não físico):** chave primária = URN canônico (Identity §4.3). Índices secundários **MUST** existir para: Namespace, Capability, `component_type` (Classification), `lifecycle_state`, Owner (Role).

**Cache — regra normativa central:**
- Resolução de uma **Versioned Identifier** específica **MAY** ser cacheada **indefinidamente** sem invalidação por conteúdo — Manifests são imutáveis uma vez `Active` (Kernel §8). Invalidação só ocorre por mudança de *metadado* (ex.: transição para `Deprecated`), nunca por mudança de conteúdo.
- Resolução de uma **Coordinate sem versão** ("current") ou de um **Alias** **MUST NOT** ser cacheada além de um TTL curto ou invalidação orientada a evento — ambos podem mudar a cada `publish_version`.

---

## 9. Consistência e Integridade

**Garantia formal de consistência:** o Registry oferece **consistência forte** para resolução de Versioned Identifier (nunca duas respostas diferentes para a mesma pergunta exata) e **consistência eventual, com SLA declarado**, para índices secundários de Discovery (busca por capability pode ficar segundos atrasada após um `register`). `[ESCOLHA DE DESIGN]`, justificada pelo mesmo padrão usado por registries de contêiner (resolução de digest é forte; busca é eventual) — correção é inegociável onde há risco de execução incorreta; frescor é negociável onde o pior caso é "não apareceu ainda na busca".

**Integridade:**
- Toda escrita em `depends_on`/`provides_for` **MUST** passar pela verificação de ciclos já definida em Kernel §7 — reaplicada, não reimplementada.
- Órfãos (Owner inexistente, Governance §6) **MUST** ser **detectados** pelo Integrity Service e **sinalizados** à Governance — o Registry nunca decide o destino de um órfão, apenas o denuncia (mesma fronteira de responsabilidade do §1).

---

## 10. Escalabilidade e Performance

Particionamento natural pelo primeiro segmento de Namespace (`core`, `org.<id>`) — alinhado à árvore da Identity Architecture §8, permitindo sharding sem reprojetar o esquema de identidade. Caminho de leitura (Discovery/Resolution) é assumido ordens de magnitude mais frequente que o de escrita (Registration) — típico de qualquer registry de definições — e o índice é desenhado read-optimized por consequência direta da imutabilidade de versão (§8).

---

## 11. Eventos e Auditoria

**Taxonomia de Registry Event:** `ComponentRegistered`, `VersionPublished`, `ComponentDeprecated`, `ComponentArchived`, `AliasCreated`, `RedirectCreated`, `IntegrityViolationDetected`.

Toda mutação autorizada pela Governance **MUST** referenciar o `Decision Record` que a autorizou (Domain Model `references`) — o Registry Event é o rastro operacional; o Decision Record permanece a fonte de verdade institucional (Domain Model §14). `IntegrityViolationDetected` é a única categoria de evento que o Registry **MAY** emitir sem uma Decision precedente, por ser puramente descritiva de um estado encontrado, não uma mutação autorizada.

---

## 12. Integrações

| Camada | Contrato de integração |
|---|---|
| **Kernel** | Registry implementa operacionalmente o mecanismo de Discovery do Kernel §5; usa o cycle-detection de Kernel §7 sem modificação. |
| **Governance** | Toda escrita passa por Decision Record prévio; Registration Service nunca aceita chamada de um Owner sem `decision_record_ref` válido. |
| **Domain Model** | Escopo estritamente limitado a `Component` (§3); nenhuma entidade de instância (Execution/Artifact/Knowledge/Decision Record) é indexada aqui. |
| **Namespace** | Toda operação é namespace-aware; resolução nunca cruza namespace implicitamente (Identity §6.2, §10). |
| **Certification (Fase 4)** | `RegistryEntry.certification_status` é um **read-through** projetado sobre a última `Decision Record` da família Certification não superada (ver Fase 4 §4) — Registry não possui nem decide esse dado. |
| **Validation (Fase 4)** | Idem — Registry apenas surfaces o resultado; não executa validação. |

---

## 13. Casos Extremos, Erros e Recuperação

| Caso | Tratamento |
|---|---|
| Publicação simultânea de duas versões concorrentes | Lineage Index **MUST** serializar por `decision_record_ref` — a Decision de Admission já é serializada pela Governance (uma aprovação por vez sobre o mesmo Coordinate); Registry rejeita a segunda escrita com `Error(ConcurrentModification)` se ambas chegarem sem ordenação causal clara. |
| Ciclo de redirect | `Error(RedirectLoopExceeded)` após 5 saltos (§6.1) — nunca resolve parcialmente. |
| Alias colidindo com token reservado | Rejeitado na criação (`create_alias` precondition, §5). |
| Namespace removido com filhos ativos | **MUST NOT** ser permitido — Namespace só pode ser arquivado quando sua subárvore inteira estiver `Archived`/`Removed` (regra de integridade referencial descendente). |
| Índice secundário divergente do primário (após falha parcial) | Integrity Service reconstrói o índice secundário a partir do primário (fonte de verdade única) — nunca o inverso. |

**Taxonomia de erro:** `NotFound`, `Ambiguous` (alias resolve a mais de um candidato — não deveria ocorrer dado §3.2 da Identity Architecture, mas tratado defensivamente), `RedirectLoopExceeded`, `IntegrityViolation`, `Unauthorized` (escrita sem `decision_record_ref`).

---

## 14. Tabelas Normativas (consolidado MUST/SHOULD/MAY)

| # | Regra | Nível |
|---|---|---|
| R1 | Registration Service MUST rejeitar escrita sem Decision Record de Governance válido | MUST |
| R2 | Resolução de Versioned Identifier MUST ser fortemente consistente | MUST |
| R3 | Resolução de Alias/Coordinate-sem-versão MAY ser eventualmente consistente | MAY |
| R4 | Toda mutação MUST emitir um Registry Event | MUST |
| R5 | Nome de Component removido MUST NUNCA ser reatribuído | MUST NOT (reuse) |
| R6 | Cadeia de redirect MUST ter profundidade máxima de 5 | MUST |
| R7 | Registry SHOULD cachear indefinidamente resoluções de versão exata | SHOULD |
| R8 | Registry MUST NOT indexar entidades de instância (Execution/Artifact/Knowledge/Decision Record) | MUST NOT |
| R9 | Integrity Service MUST reutilizar o algoritmo de detecção de ciclos do Kernel §7 | MUST |

---

## 15. Validação Institucional Final

| Verificação cruzada | Resultado |
|---|---|
| Consistente com Kernel §5 (Discovery) | **PASS** — operacionaliza sem contradizer |
| Consistente com Governance §7 (Admission) | **PASS** — Registry é consumidor, nunca substitui a decisão |
| Consistente com Domain Model v1.1.0 | **PASS** — nenhuma entidade nova introduzida no Domain Model |
| Consistente com Identity Architecture §9 | **PASS** — cumpre exatamente o contrato conceitual reservado (`resolve`/`list`/`lineage`) |
| Exige RFC de emenda? | **Não** |
