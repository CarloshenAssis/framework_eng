# Observability Architecture
### Framework Eng — A Camada Institucional de Correlação, Consulta e Prova

*Versão 1.0.0 · Base normativa (congelada): Constitution · Kernel · Governance · Domain Model v1.1.0 · RFC-DM-001 · Identity & Namespace · Registry & Discovery · Validation & Certification · Composition · Workflow · Execution · Standards · Policy · Template Architecture · Skill Architecture*

> **Tese central, provada seção a seção:** Observability não executa nada, não decide nada, não cria nada além de **projeções de leitura, transitórias e não persistidas**, sobre dados que já são produzidos, versionados, validados e retidos pelos catorze documentos anteriores. Este documento **fecha, literalmente, os `[LACUNA proposital]` já pré-comprometidos** por Execution §14 (contrato conceitual `query by orchestration_id/coordinate/time_range`), Composition §14, Standards §19 e Policy §19 — sem alterar uma linha de nenhum deles.

---

## 1. Posição Arquitetural

Observability é o **serviço de substrato somente-leitura** que opera sobre a totalidade dos registros já institucionalmente permanentes (`Execution`, `Artifact`, `Evidence`, `Decision`, `Decision Record`, `Context Snapshot`) e sobre o fluxo de telemetria operacional já nomeado por sete documentos anteriores (`Registry Event`, `Composition Event`, `Workflow Event`, `Execution Event`, `Standard Event`, `Policy Event`, `Template Event`, `Skill Event`), tornando ambos **correlacionáveis, consultáveis e reconstruíveis** sem jamais escrevê-los.

### 1.1 Fechamento formal de forward-references já existentes

| Documento | Compromisso já assumido | Como este documento o honra |
|---|---|---|
| Execution §4, §14 | "Provenance Service — contrato conceitual definido aqui; armazenamento físico deferido... `query by orchestration_id/coordinate/time_range`... não deve mudar quando aquele documento for escrito" | O `Provenance Service` é **o mesmo serviço**, agora fisicamente especificado (§6-§7), com o **exato** conjunto de eixos de consulta prometido — nenhum eixo adicional, nenhuma renomeação |
| Composition §14 | "armazenamento físico e escala do Provenance Service" | Idem — Composition apenas referenciava a mesma lacuna |
| Standards §19 | "Séries históricas de Conformance Claims para análise de drift normativo" | `query_events`/`provenance()` sobre `Conformance Claim` (Artifact já existente), sem novo mecanismo |
| Policy §19 | "Séries históricas de EPS e traces para análise de deriva de aplicabilidade" | Idem, mesma consulta genérica aplicada a `Effective Policy Set` |
| Domain Model §15 | As "cinco perguntas obrigatórias de rastreabilidade" — nunca antes formalizadas como algoritmo | `BuildProvenanceChain` (§9.2) é a especificação executável dessa exigência, catorze documentos depois |

### 1.2 O que Observability estruturalmente NÃO é

`[ESCOLHA DE DESIGN]`

**Motivação:** decidir se o substrato de Observability deveria ser modelado como uma extensão do Registry (dado que ambos "indexam" coisas) ou como um serviço arquiteturalmente distinto.

**Alternativas rejeitadas:** (a) estender Registry & Discovery para também indexar instâncias de Execution; (b) introduzir um "Provenance Registry" paralelo ao Registry existente.

**Justificativa técnica:** Registry & Discovery §3.2 já declara, explicitamente e por decisão deliberada daquele documento, que `Execution`/`Artifact`/`Knowledge`/`Decision Record` **MUST NOT** ser indexados pelo Registry — a justificativa lá dada é que Registry serve descoberta de **definições** de baixa cardinalidade (Components), enquanto instâncias são **escala de log** (potencialmente milhões, Domain Model §4.5). Um "Provenance Registry" duplicaria a responsabilidade de resolução de identidade que já pertence exclusivamente ao Registry (Registry §1: autoridade única). Observability, portanto, não é um Registry de segunda espécie — é um substrato de **consulta sobre instâncias já persistidas por outros mecanismos**, nunca um índice de **definições**.

**Precedentes arquitetônicos:** exatamente a mesma separação entre `kube-apiserver`/`etcd` (registro de definições, Registry-equivalente) e backends de observabilidade (Prometheus, backends de tracing compatíveis com OpenTelemetry) no ecossistema Kubernetes — arquiteturalmente distintos por desenho, nunca fundidos, mesmo operando sobre o mesmo cluster.

### 1.3 Fronteiras negativas (invioláveis)

| Fronteira | Regra |
|---|---|
| Observability não executa | **MUST NOT** possuir nenhuma operação de escrita sobre Component, Execution, Manifest, Registry, Certificação ou Policy |
| Observability não decide | **MUST NOT** ter autoridade de Governance; consultas informam Auditoria (Governance §12), nunca a substituem |
| Observability não versiona | **MUST NOT** introduzir esquema de versão próprio — toda versão consultada é `VersionedIdentifier` já existente (Identity §4.1) |
| Observability não descobre Components | **MUST NOT** duplicar `search(capability)` (Registry §6.2) — seu eixo de consulta é instância, não definição |
| Observability não estende Lifecycle | **MUST NOT** introduzir estado — todo estado consultado é o Kernel Lifecycle (§3) ou o Lifecycle de Execution (Domain Model §8), inalterados |

---

## 2. Objetivos

| # | Objetivo | Mecanismo |
|---|---|---|
| O1 | Correlacionar Workflow → Step → Execution → Artifact → Evidence de forma determinística | `BuildTrace` (§9.1) sobre a convenção de correlação já normatizada (Execution §4) |
| O2 | Responder, algoritmicamente, as cinco perguntas obrigatórias de Domain Model §15 | `BuildProvenanceChain` (§9.2) |
| O3 | Cumprir literalmente o contrato `query by orchestration_id/coordinate/time_range` pré-comprometido | `ProvenanceService.query` (§7) |
| O4 | Permitir reconstrução fiel de uma orquestração passada sem re-executar nada | `Replay` (§9.3), respeitando EX1 (Execution §12) |
| O5 | Fornecer superfície de debug sobre uma Execution individual | `Debug` (§9.4) |
| O6 | Definir retenção sem inventar vocabulário — reusar `EvidenceRequirement.retention` já existente | §6.3 |
| O7 | Provar formalmente ausência de qualquer novo mecanismo institucional | §16, prova exaustiva |

---

## 3. Escopo

### 3.1 Pertence

Modelo de consulta (Trace, Span, Execution Timeline, Provenance Chain); correlação Workflow→Step→Execution→Artifact→Evidence; retenção de telemetria operacional (distinta da retenção institucional já mandatada por Domain Model §9); Replay; Debug institucional; exportação de séries de `Metric`; integração de Observability com Standards/Policy como *alvo* de requisitos normativos de retenção.

### 3.2 Não pertence — com justificativa

| Excluído | Justificativa |
|---|---|
| Autoridade de auditoria (o que um achado significa institucionalmente) | Governance §12 — Observability fornece a consulta; Governance mantém a autoridade de interpretação e ação |
| Avaliação de conformidade contínua | `Compliance Architecture` — **não integra a base normativa congelada deste documento** (permanece consumidor downstream, não ratificado); Observability apenas fornece o substrato de consulta que tal camada, quando ratificada, consumirá |
| Re-execução de qualquer Execution | Execution Architecture — `Replay` (§9.3) é leitura pura; **MUST NOT** disparar nova Execution, sob pena de violar EX1 (Execution §12) |
| Formato físico de exportação de métricas (wire format, protocolo) | `[LACUNA proposital]`, deferida a Packaging & Distribution — mesma classe de lacuna já assumida em Standards §3.2, Template §3.2 |
| Controle de acesso a consultas de Observability | Fora de escopo desde Identity §1 ("não é autenticação/autorização"); a **partição** de dados por Namespace (§6.1) é estrutural, não é controle de acesso |

---

## 4. Modelo Conceitual

### 4.1 Tabela de proveniência — prova de zero criação de entidade

| Conceito consultado/produzido por Observability | Natureza | Já definido em |
|---|---|---|
| `Execution`, Lifecycle (`Initiated→Running→Completed\|Failed\|Aborted`) | **Reutilizado, sem alteração** | Domain Model §8; Execution §5 |
| `Artifact`, `Evidence`, `Decision Record`, `Context Snapshot` | **Reutilizado, sem alteração** | Domain Model §2, §13; RFC-DM-001 §3.2 |
| `Decision`, `Role` | **Reutilizado** | Domain Model §14; Governance §2 |
| Convenção `orchestration_id`/`phase_id`/`step_id`/`attempt` | **Reutilizado** | Execution Architecture §4 (convenção semântica sobre `Context`, precedente OpenTelemetry já citado naquele documento) |
| `Metric` | **Reutilizado** | Domain Model §2, entidade #14 |
| `Registry Event`, `Composition Event`, `Workflow Event`, `Execution Event`, `Standard Event`, `Policy Event`, `Template Event`, `Skill Event` | **Reutilizado** — cada taxonomia já definida por seu documento de origem, cada um explicitamente descrito como "telemetria operacional, não Domain Model Event Entity" | Registry §11; Composition §11; Workflow §11; Execution §11; Standards §16; Policy §16; Template §16; Skill §13 |
| `EvidenceRequirement.retention: PERMANENT \| BOUNDED(Duration)` | **Reutilizado**, aplicado a nova categoria de dado | Standards §4.6 |
| `VersionedIdentifier`, `Coordinate`, Namespace | **Reutilizado** | Identity & Namespace §4, §3, §8 |
| Regras de partição/consistência (forte para identidade versionada; eventual para índice secundário) | **Reutilizado, mesma regra reaplicada** | Registry §9; Policy §15.1 |
| **Trace** | **Value Object efêmero — projeção de consulta, não persistido** | Novo *nome*, zero conteúdo novo — ver §4.2 |
| **Span** | **Value Object efêmero — projeção de uma Execution** | Idem |
| **Execution Timeline** | **Value Object efêmero — reordenação de Trace** | Idem |
| **Provenance Chain** | **Value Object efêmero — grafo de leitura sobre relações já existentes** | Idem |
| **Query Model** (operações) | **Serviço de substrato, mesma classe de `Composition Resolver`/`Scheduler`/`Standard Resolution Service`/`Policy Evaluation Service`** | Nenhum novo padrão arquitetural — reaplica exatamente a mesma classe de substrato já usada quatro vezes |

**Nenhuma linha da tabela introduz Component, Artifact, relação, estado ou Lifecycle.** As quatro únicas linhas "novas" são **nomes dados a projeções de leitura** — nunca gravadas, nunca versionadas, nunca dotadas de Identity.

### 4.2 Por que Trace/Span/Timeline/Provenance Chain não são Artifacts

`[ESCOLHA DE DESIGN]`

**Motivação:** todo documento anterior que precisou de um resultado estruturado (Assembly, Execution Plan, Effective Policy Set, Conformance Claim, Expanded Template) o modelou como `Artifact` genérico. Era necessário decidir se Trace/Span/Timeline/Provenance Chain deveriam seguir o mesmo padrão.

**Alternativas rejeitadas:** modelar `Trace` como `Artifact` produzido por uma "Execution de consulta", pelo mesmo padrão dos documentos anteriores.

**Justificativa técnica:** um `Artifact`, por definição (Domain Model §2, entidade #7), é *"qualquer resultado tangível e persistente produzido por uma Execution ou Decision"* — persistência é parte constitutiva da definição. Assembly/Execution Plan/EPS/Conformance Claim/Expanded Template são todos produzidos **uma vez** e **consumidos por múltiplas leituras subsequentes** — persistência agrega valor real (evita recomputação, sustenta auditoria). Um `Trace`, ao contrário, é **puramente derivado**, recomputável a qualquer momento a partir dos mesmos dados-fonte imutáveis, sem nenhuma perda de informação se nunca for persistido — sua existência é inteiramente uma função dos dados-fonte já persistidos. Persisti-lo criaria uma **cópia derivada redundante**, sujeita a divergir da fonte (um problema clássico de cache invalidado incorretamente), violando exatamente o motivo pelo qual o mandato deste documento proíbe novos Artifacts.

**Precedentes arquitetônicos:** um *trace* em OpenTelemetry não é uma entidade de armazenamento própria — é a **agregação de Spans já emitidos**, reconstruída por consulta ao backend; o backend armazena Spans (aqui, já cobertos por `Execution`+`Context Snapshot`+`Artifact`), nunca "Traces" como registro primário.

---

## 5. Estrutura

### 5.1 Span — a projeção de uma Execution

```
Span {                                              [Value Object — nunca persistido, sempre recomputado]
  execution_id      : InstanceIdentifier             [Identity §4.2 — ULID já existente]
  component_ref     : VersionedIdentifier
  orchestration_id  : InstanceIdentifier?             [Execution §4 — convenção de Context]
  phase_id, step_id : Identifier?
  attempt           : Integer
  state             : Initiated | Running | Completed | Failed | Aborted    [Domain Model §8 — inalterado]
  performed_by      : Role
  context_snapshot_ref : ArtifactId                    [RFC-DM-001 §3.2]
  produced_artifacts   : [ArtifactId]
  evidence_refs        : [EvidenceId]
  started_at, ended_at : Timestamp?
}
```

### 5.2 Trace — o conjunto de Spans de uma orquestração

```
Trace {
  orchestration_id : InstanceIdentifier
  spans            : Span[]                          (ordenados por phase_sequence/step_id/started_at)
  complete         : boolean                          (true sse todo Span está em estado terminal)
}
```

### 5.3 Execution Timeline — reordenação estrita por tempo

```
ExecutionTimeline {
  orchestration_id : InstanceIdentifier
  events           : [ (Timestamp, Span, TransitionKind) ]      (Initiated|Running|Completed|Failed|Aborted)
}
```

`ExecutionTimeline` **difere** de `Trace` apenas na chave de ordenação (tempo estrito vs. topologia de Phase/Step) — mesmo conjunto de dados-fonte, duas projeções.

### 5.4 Provenance Chain — resposta às cinco perguntas de Domain Model §15

```
ProvenanceChain {
  subject       : ArtifactId | ExecutionId
  origin        : ExecutionId | DecisionId            (pergunta 1: "de onde veio?")
  context       : ArtifactId (Context Snapshot)         (pergunta 2: "sob qual Context?")
  responsible   : Role                                 (pergunta 3: "quem foi responsável?")
  against       : VersionedIdentifier                   (pergunta 4: "contra qual versão?")
  affects       : [VersionedIdentifier | DecisionRecordId]   (pergunta 5: "o que afeta/referencia?")
  complete      : boolean                              (MUST ser true para a cadeia ser válida — §9.2)
}
```

### 5.5 Debug View e Replay View

```
DebugView { span: Span, evidence: Evidence[], bindings: VariableBindingSet?, failure_detail: FailureDetail? }
ReplayView { trace: Trace, provenance_chains: ProvenanceChain[], faithful_reconstruction: boolean }
```

Nenhuma das cinco estruturas acima possui `Identity`, é registrada, é versionada ou é retida além da duração da consulta que a produziu.

---

## 6. Modelo de Dados

### 6.1 Particionamento

O `Provenance Service` (Execution §4, agora especificado fisicamente) particiona por `orchestration_id` como chave primária de afinidade — **exatamente** a afinidade natural já apontada por Execution §10 ("todas as Executions de uma mesma orquestração tendem a ser consultadas juntas"). Índices secundários:

| Índice | Eixo | Cumpre o eixo pré-comprometido |
|---|---|---|
| Por `orchestration_id` | Trace/Timeline completos | `orchestration_id` (Execution §14) |
| Por `component_ref` (Coordinate@version) | "todas as Executions da Skill X" | `coordinate` (Execution §14) |
| Por intervalo de `started_at`/`ended_at` | Consultas temporais, auditoria por período | `time_range` (Execution §14) |
| Por `Namespace` (herdado de `component_ref`) | Particionamento físico, isolamento estrutural | Identity §10 |

**Nenhum eixo além dos três explicitamente prometidos em Execution §14 é introduzido.** O quarto índice (Namespace) não é um eixo de consulta institucional novo — é herança direta do particionamento já normatizado em Registry §10 e Identity §10, aplicado aqui por razões de isolamento físico, não de funcionalidade nova.

### 6.2 Consistência

Reaplica, sem modificação, a mesma dualidade já estabelecida três vezes (Registry §9, Standards §15.1, Policy §15.1):

| Consulta | Consistência |
|---|---|
| `span(execution_id)` sobre Execution em estado terminal | **Forte** — dado imutável (Domain Model §8) |
| `span(execution_id)` sobre Execution em `Running` | Reflete o estado mais recente conhecido; não há garantia de linearização com o Scheduler (Execution §5), mesma classe de eventual consistency já aceita em Execution §10 |
| `trace(orchestration_id)` incompleto | **MUST** declarar `complete = false` explicitamente — nunca apresentar um Trace parcial como se fosse total |
| `query_events(filter, time_range)` | Eventual, com SLA declarado — mesma regra de Registry §9 para índices secundários |

### 6.3 Retenção — reuso literal do vocabulário de Standards

`[ESCOLHA DE DESIGN]`

**Motivação:** decidir se Observability precisa de um vocabulário próprio de política de retenção.

**Alternativas rejeitadas:** definir `RetentionPolicy` como enumeração nova, específica de Observability (ex.: `HOT/WARM/COLD/EXPIRED` com semântica própria não relacionada a nenhum documento anterior).

**Justificativa técnica:** Standards Architecture §4.6 já define `EvidenceRequirement.retention: PERMANENT | BOUNDED(Duration)` — vocabulário suficiente e já normativamente vinculante para toda `Evidence` do Framework. Reaproveitá-lo aqui, aplicando-o à categoria adicional de **telemetria operacional** (Events), evita introduzir um segundo vocabulário de retenção concorrente — que produziria exatamente a ambiguidade terminológica que RFC-DM-001 já eliminou nos achados C1/H1.

**Justificativa formal — dois regimes, um vocabulário:**

| Categoria de dado | Regra de retenção | Fundamento |
|---|---|---|
| `Execution`, `Artifact`, `Evidence`, `Decision`, `Decision Record`, `Context Snapshot` | **MUST** ser `PERMANENT` | Domain Model §9 — entidades de Governança/Execução com relevância de Governança **nunca** são verdadeiramente transitórias; Observability **MUST NOT** encurtar essa garantia |
| `Registry/Composition/Workflow/Execution/Standard/Policy/Template/Skill Event` (telemetria operacional) | `BOUNDED(Duration)` por padrão institucional; `PERMANENT` **SHOULD** ser aplicado quando um NR de Standard com `applies_to = EXECUTION` explicitamente o exigir (Standards §4.6, `EvidenceRequirement.retention`) | Nenhuma garantia de permanência foi assumida por nenhum documento de origem desses Events — retenção limitada é o padrão seguro, elevável por norma explícita |

**Precedentes arquitetônicos:** a mesma distinção entre "registro de auditoria permanente" e "log operacional de curta retenção" existe em toda infraestrutura observável madura (ex.: AWS CloudTrail vs. logs de aplicação de curta duração) — aqui formalizada com o vocabulário já ratificado, não um novo.

---

## 7. Modelo Operacional

**Serviço:** `Observability Query Service`, operando sobre o `Provenance Service` (já nomeado por Execution §4) e o `Event Log` (armazenamento do fluxo de telemetria, §6.3). Mesma classe de substrato institucional de `Composition Resolver`, `Scheduler`, `Standard Resolution Service`, `Policy Evaluation Service`. **Não é Component. Não possui Lifecycle. Não escreve em lugar algum além do próprio Event Log operacional (nunca em Component, Manifest, Registry, ou dado institucional permanente).**

### 7.1 Superfície de operações — prova de "somente leitura"

```
trace(orchestration_id)                    → Trace
span(execution_id)                          → Span
timeline(orchestration_id)                  → ExecutionTimeline
provenance(subject: ArtifactId|ExecutionId) → ProvenanceChain
debug(execution_id)                         → DebugView
replay(orchestration_id)                    → ReplayView
query_events(filter, time_range)            → Event[]
export_metrics(metric_ref, time_range)      → MetricSeries[]
```

**Nenhuma operação de escrita existe na superfície.** Todas as oito operações têm assinatura `(...) → dado`, nunca `(...) → void` com efeito colateral sobre estado institucional — prova formal de que Observability é *cross-cutting* sem afetar comportamento funcional (mandato do documento).

### 7.2 Pré-condição estrutural já garantida por Execution — nenhum gate novo

`[ESCOLHA DE DESIGN]`

**Motivação:** decidir se Observability precisa de um mecanismo próprio para *garantir* que dados observáveis sejam capturados (ex.: um "gate de observabilidade" análogo ao `GATE_AUTO` de Workflow).

**Alternativas rejeitadas:** introduzir uma precondição nova bloqueando transição de Execution até que dados de observabilidade estejam completos.

**Justificativa técnica:** essa garantia **já existe**, sem qualquer ação deste documento — Execution §12, regra **EX2**: *"Running MUST ter Context Snapshot precedente"*. Captura de dado observável não é opcional nem precisa ser mandatada aqui porque já é, desde RFC-DM-001 §3.2, uma precondição estrutural inegociável de toda Execution. Introduzir um gate próprio duplicaria uma garantia já absoluta.

**Precedentes arquitetônicos:** OpenTelemetry não "ativa" instrumentação via política externa quando a instrumentação já está embutida no runtime por construção — a mesma lógica aqui: observabilidade é subproduto estrutural da Execution, não um recurso opcional configurável.

---

## 8. Fluxo de Observabilidade

```
1. Workflow(Step) dispara Execution                                              [Execution §7 — InvokeSkillStep]
2. Execution captura Context Snapshot (orchestration_id/phase_id/step_id/attempt) [RFC-DM-001 §3.2; Execution §4]
3. Execution produz Artifact(s), eventualmente Evidence                          [Domain Model §7]
4. (paralelo, sem alterar 1-3) Cada camada emite seu Event já normatizado:
   Registry/Composition/Workflow/Execution/Standard/Policy/Template/Skill Event  [documentos de origem]
5. Event Log absorve o Event (retenção conforme §6.3)
6. Provenance Service indexa Execution/Artifact/Evidence por orchestration_id/coordinate/time (§6.1)
7. Sob demanda, Observability Query Service:
   a. trace()/timeline() reconstrói a orquestração                              [§9.1]
   b. provenance() responde às 5 perguntas do Domain Model §15                  [§9.2]
   c. replay() reconstrói fielmente, sem re-executar                            [§9.3]
   d. debug() expõe uma Execution individual                                    [§9.4]
```

Os passos 1-4 **são exatamente** os já normatizados pelos documentos de origem — nenhum passo é alterado, adicionado ou removido por este documento. Os passos 5-7 são a **contribuição exclusiva** de Observability Architecture: leitura pura.

---

## 9. Algoritmos

### 9.1 Construção de Trace

```
ALGORITMO BuildTrace(orchestration_id):
  ENTRADA: orchestration_id : InstanceIdentifier
  SAÍDA:   Trace

  1  spans_raw ← ProvenanceService.query(filter = {context.orchestration_id = orchestration_id})
  2  spans ← [ Span(e) PARA e EM spans_raw ]           # projeção 1:1 de cada Execution encontrada
  3  ordenados ← SortBy(spans, chave = (phase_sequence, step_id, started_at))
  4  completo ← Todos(s EM ordenados : s.state ∈ {Completed, Failed, Aborted})
  5  RETORNA Trace{ orchestration_id, spans: ordenados, complete: completo }

  # TERMINAÇÃO: query() retorna conjunto finito (Execution é evento único — Domain Model §8)
  # DETERMINISMO: ordenação total sobre chave estável; sem I/O não determinístico
```

### 9.2 Construção de Provenance Chain — a formalização de Domain Model §15

```
ALGORITMO BuildProvenanceChain(subject):
  ENTRADA: subject : ArtifactId | ExecutionId
  SAÍDA:   ProvenanceChain
  INVARIANTE: MUST responder as cinco perguntas obrigatórias (Domain Model §15) ou falhar explicitamente

  1  raiz ← Resolve(subject)
  2  SE raiz é Artifact:
  3     origin ← WalkBack(raiz, relação = produces⁻¹)              # de onde veio
  4  SENÃO:
  5     origin ← raiz                                                # já é a Execution
  6  context ← WalkBack(origin, relação = captured_as)                # sob qual Context (Snapshot)
  7  responsible ← WalkBack(origin, relação = performed_by)            # quem foi responsável
  8  against ← WalkBack(origin, relação = declares/describes)          # contra qual versão
  9  affects ← WalkForward(raiz, relações = {derives_from⁻¹, informs, references⁻¹})   # o que afeta
 10
 11  SE ALGUM(origin, context, responsible, against) = ausente:
 12     RETORNA ProvenanceError(INCOMPLETE_CHAIN, subject)
 13     # Domain Model §15: entidade sem essas respostas é, por definição, inválida —
 14     # este algoritmo NÃO inventa dado ausente; ele expõe a lacuna
 15
 16  RETORNA ProvenanceChain{ subject, origin, context, responsible, against, affects,
                              complete: true }
```

**Prova de terminação:** cada `WalkBack`/`WalkForward` percorre relações já garantidas acíclicas ou de cardinalidade finita fixa (`produces`, `captured_as`, `performed_by`, `declares` são todas N:1 ou 1:1 — Domain Model §7); `WalkForward` sobre `derives_from` é finito porque RFC-DM-001 §3.3 já garante o grafo acíclico e temporalmente monotônico.

### 9.3 Replay — reconstrução fiel, nunca re-execução

```
ALGORITMO Replay(orchestration_id):
  ENTRADA: orchestration_id : InstanceIdentifier
  SAÍDA:   ReplayView
  INVARIANTE: MUST NOT criar nenhuma nova Execution (EX1, Execution §12)

  1  trace ← BuildTrace(orchestration_id)
  2  chains ← [ BuildProvenanceChain(s.execution_id) PARA s EM trace.spans ]
  3  PARA CADA span EM trace.spans:
  4     # Reconstrução usa exclusivamente dados JÁ PERSISTIDOS e imutáveis —
  5     # nunca recomputa Expand() do zero; usa o Artifact ExpandedTemplate já produzido
  6     SE span possui template_ref:
  7        span.expanded_ref ← Provenance.produces(span.execution_id, kind = ExpandedTemplate)
  8        ASSERT span.expanded_ref ≠ ausente     # já produzido — Template §11.3
  9  RETORNA ReplayView{ trace, provenance_chains: chains, faithful_reconstruction: true }
```

`[ESCOLHA DE DESIGN]`

**Motivação:** decidir o significado exato de "Replay" — reconstrução de leitura vs. re-execução.

**Alternativas rejeitadas:** interpretar "Replay" no sentido de Event Sourcing clássico — reprocessar eventos para reconstituir estado *recomputando* efeitos (o que, aqui, significaria potencialmente re-invocar `Expand()` ou até reexecutar Steps).

**Justificativa técnica:** Execution §12 (regra **EX1**) proíbe categoricamente reabrir ou recriar uma `Execution` — "falha gera nova Execution ou compensação, nunca reabertura". Um "Replay" que recomputasse qualquer coisa arriscaria (a) produzir um resultado diferente caso o ambiente de execução tenha mudado desde então (quebrando a garantia de que o histórico é imutável), e (b) confundir-se com uma nova tentativa institucional (retry), que já tem semântica própria e distinta (Domain Model §8). Por isso `Replay` aqui **MUST** usar exclusivamente Artifacts já produzidos e persistidos (linha 7-8 do algoritmo) — nunca recalcular.

**Precedentes arquitetônicos:** "replay" de um trace distribuído em sistemas de observabilidade maduros (Jaeger, Zipkin) sempre significa *visualização* do que aconteceu, nunca reexecução do sistema monitorado — a mesma convenção semântica é adotada aqui.

### 9.4 Debug

```
ALGORITMO Debug(execution_id):
  span ← ProvenanceService.span(execution_id)
  evidence ← Provenance.query(filter = {substantiates = execution_id})
  bindings ← SE span.template_ref: Provenance.produces(execution_id, kind = VariableBindingSet_ref)
  falha ← SE span.state = Failed: BuildFailureDetail(span) SENÃO null
  RETORNA DebugView{ span, evidence, bindings, failure_detail: falha }
```

### 9.5 Consulta de eventos

```
ALGORITMO QueryEvents(filter, time_range):
  PRE:  time_range ⊆ janela de retenção vigente para a categoria de Event filtrada (§6.3)
  SE time_range excede a retenção configurada:
     RETORNA EventQueryError(RETENTION_WINDOW_EXCEEDED, filter.category)
  RETORNA EventLog.scan(índice = (component_type, event_type, timestamp), filter, time_range)
```

---

## 10. Diagramas

### 10.1 UML — projeções sobre dados já existentes (nenhuma aresta sólida nova)

```
┌─────────────┐  produces   ┌──────────┐ captured_as ┌──────────────────┐
│  Execution   ├────────────►│ Artifact │◄────────────┤ Context Snapshot  │  [Domain Model §7, §13;
│  (Domain     │             │  ├Evidence│             │  [RFC-DM-001 §3.2] │   RFC-DM-001 §3.2 —
│   Model §8)  │ performed_by│  ├Decision │             └──────────────────┘   todas relações JÁ
└──────┬──────┘◄────────────┤   Record  │                                     existentes]
       │                     │  └Expanded │
       │                     │    Template│
       │                     └──────────┘
       │
       ┆ projeção somente-leitura (nunca persistida)
       ▼
┌─────────────┐   1..*   ┌──────────┐
│    Span      │◄─────────┤   Trace   │  «Value Object efêmero»
│  «VO»        │          │  «VO»     │
└─────────────┘          └──────────┘
       ┆ projeção
       ▼
┌──────────────────┐
│ ProvenanceChain    │  «VO» — responde Domain Model §15
└──────────────────┘
```

### 10.2 Sequência — correlação Workflow → Step → Execution → Artifact → Evidence

```
Auditor        ObservabilityQuery      ProvenanceService        (dados já persistidos)
   │                   │                       │
   ├─trace(orch_id)────►│                       │
   │                   ├─query(orch_id)────────►│
   │                   │                       ├─ lê Executions com Context.orchestration_id=X
   │                   │                       ├─ cada Execution → produces → Artifact
   │                   │                       ├─ cada Artifact → (subtipo) Evidence
   │                   │◄─spans_raw─────────────┤
   │                   ├─SortBy(phase,step,time)
   │◄─Trace(spans[])────┤
   │                                            │
   ├─provenance(artifact_id)───────────────────►│
   │                                            ├─ WalkBack: produces⁻¹, captured_as, performed_by, declares
   │                                            ├─ WalkForward: derives_from⁻¹, informs, references⁻¹
   │◄─ProvenanceChain (5 perguntas respondidas)──┤
   │
   │  nota: nenhuma escrita ocorreu; Workflow, Step, Execution, Artifact e Evidence
   │        são exatamente os já definidos por Workflow §4, Execution §4-§5, Domain Model §7/§13
```

### 10.3 Estados

Observability **não possui máquina de estados**. `Span.state` é a projeção literal do Lifecycle de `Execution` (Domain Model §8) — nenhuma extensão, nenhum novo valor.

---

## 11. Casos Extremos

| # | Caso | Tratamento |
|---|---|---|
| B1 | Consulta de `trace()` sobre orquestração ainda em `Running` | Retorna `Trace{complete: false}` explicitamente — **MUST NOT** apresentar como completo |
| B2 | Duas Steps paralelas emitindo Events concorrentemente | Seguro por construção — cada Execution/Evidence é imutável e independente (mesmo argumento de Execution §9) |
| B3 | Consulta de `provenance()` sobre Artifact cujo Component de origem foi `Removed` | **MUST** ainda resolver — Evidence/Decision Record são permanentes por Domain Model §9, independentemente do Component ainda estar `Active` no Registry; resolução usa a Lineage histórica (Identity §7), não apenas o índice `Active` |
| B4 | `replay()` de orquestração cujo Template mudaria de expansão se recomputado hoje | Impossível de ocorrer incorretamente — `Replay` **MUST** usar o `ExpandedTemplate` já persistido (§9.3, linhas 6-8), nunca recomputar `Expand()` |
| B5 | `query_events()` com `time_range` além da janela de retenção configurada | `EventQueryError(RETENTION_WINDOW_EXCEEDED)` — falha explícita, nunca resultado vazio silencioso |
| B6 | `ProvenanceChain` incompleta (uma das cinco perguntas não respondível) | `ProvenanceError(INCOMPLETE_CHAIN)` — a entidade subjacente é, por definição de Domain Model §15, inválida; Observability expõe isso, não o mascara |
| B7 | Consulta cruzando fronteira de Namespace (ex.: `time_range` sobre `component_ref` de organização distinta) | Particionamento físico por Namespace (§6.1) já isola os dados estruturalmente — mesma garantia de Identity §10, sem necessidade de lógica adicional aqui |
| B8 | `export_metrics()` para um `Metric` sem observações no `time_range` solicitado | `MetricSeries` vazia é resultado válido, não erro (mesma disciplina de "conjunto vazio é resultado legítimo" já usada em Policy §14/F11 e Standards §14/E12) |
| B9 | Orquestração com milhões de Spans (Workflow de altíssimo fan-out) | `trace()` **SHOULD** paginar; complexidade permanece O(S log S) — ver §12 |

---

## 12. Performance

### 12.1 Cache

| Consulta | Cacheável indefinidamente? | Fundamento |
|---|---|---|
| `span()`/`trace()`/`provenance()` sobre orquestração `complete = true` | **Sim** | Toda entrada é imutável em estado terminal (Domain Model §8) — mesma prova de correção já usada em Registry §8, Standards §15.1, Template §12 |
| `span()`/`trace()` sobre orquestração ainda `Running` | **Não** — TTL curto ou invalidação por `StepCompleted`/`StepFailed` (Execution §11) | Estado ainda mutável |
| `export_metrics()` para janela temporal já fechada | **Sim**, indefinidamente | Série histórica imutável uma vez a janela encerrada |
| `query_events()` | **Não**, ou TTL curto | Dependente de `time_range` corrente e de retenção não permanente (§6.3) |

**Nenhuma política de cache nova** — pura reaplicação da regra já estabelecida três vezes: imutabilidade da fonte ⟹ cache indefinido correto.

### 12.2 Complexidade

| Operação | Complexidade | Comentário |
|---|---|---|
| `BuildTrace` | O(S log S) | S = Spans da orquestração; mesma ordem de grandeza de `ResolveEffectiveRequirements` (Standards §15.2) |
| `BuildProvenanceChain` | O(1) amortizado por salto, grafo de grau fixo (5 perguntas) | Bounded por construção — Domain Model §15 fixa exatamente 5 relações a percorrer |
| `Replay` | O(S log S + S) | Trace + reconstrução por Span |
| `QueryEvents` | O(log N + K) | N = eventos indexados na janela; K = resultado retornado, via índice `(component_type, event_type, timestamp)` |

### 12.3 Trade-off explícito

**Trade-off — granularidade de retenção operacional.** Manter telemetria de altíssimo volume (`Skill Event`, `Execution Event`) em retenção `PERMANENT` por padrão inviabilizaria custo de armazenamento na escala projetada por Domain Model §4.5 (milhões de Executions). A regra de §6.3 (BOUNDED por padrão, elevável por Standard explícito) é o trade-off deliberado entre custo e auditabilidade — coerente com o princípio constitucional de **fricção proporcional ao risco**: apenas o que é normativamente exigido paga o custo de permanência.

---

## 13. Eventos

**Observability não define nenhum novo tipo de evento de domínio.** Os únicos eventos que este documento introduz são de natureza puramente operacional do próprio serviço de consulta — nunca eventos institucionais:

| Evento (operacional do Query Service) | Emitido quando |
|---|---|
| `TraceBuilt(orchestration_id, span_count)` | `BuildTrace` concluída |
| `ProvenanceChainIncomplete(subject)` | §9.2, linha 11-12 |
| `ReplayCompleted(orchestration_id)` | `Replay` concluído |
| `RetentionWindowExceeded(category, requested_range)` | B5 |
| `MetricsExported(metric_ref, range)` | `export_metrics` concluída |

Todo evento institucional consultado (`ComponentRegistered`, `StepCompleted`, `PolicyActivated`, etc.) já é definido, nominalmente, pelos documentos de origem citados em §4.1 — nenhum é redefinido aqui.

---

## 14. Regras Normativas (RFC 2119)

| # | Regra | Nível |
|---|---|---|
| OB1 | Observability Query Service MUST NOT expor nenhuma operação de escrita sobre Component, Manifest, Registry, Certificação ou Policy | MUST NOT |
| OB2 | `Trace`, `Span`, `Execution Timeline`, `Provenance Chain`, `Debug View`, `Replay View` MUST NOT ser persistidos como Artifact ou qualquer entidade do Domain Model | MUST NOT |
| OB3 | `Replay` MUST NOT criar nova Execution nem reabrir Execution existente (EX1) | MUST NOT |
| OB4 | `Replay` MUST usar Artifacts já persistidos (ex.: `ExpandedTemplate`), nunca recomputar funções puras já executadas | MUST |
| OB5 | `Trace` incompleto MUST declarar `complete = false` explicitamente | MUST |
| OB6 | `ProvenanceChain` incompleta (falha em responder qualquer das 5 perguntas de Domain Model §15) MUST resultar em erro explícito, nunca em cadeia parcial silenciosa | MUST |
| OB7 | Retenção de `Execution`/`Artifact`/`Evidence`/`Decision`/`Decision Record`/`Context Snapshot` MUST ser `PERMANENT` | MUST |
| OB8 | Retenção de telemetria operacional (Events) MUST ser `BOUNDED` por padrão, elevável a `PERMANENT` apenas por NR de Standard explícito | MUST |
| OB9 | Vocabulário de retenção MUST reusar `EvidenceRequirement.retention` (Standards §4.6), sem novo enum | MUST |
| OB10 | Particionamento MUST usar exatamente os três eixos pré-comprometidos por Execution §14: `orchestration_id`, `coordinate`, `time_range` | MUST |
| OB11 | Consulta além da janela de retenção configurada MUST falhar explicitamente | MUST |
| OB12 | Query Model MAY cachear indefinidamente resultados sobre dados em estado terminal | MAY |
| OB13 | Query Model MUST NOT cachear indefinidamente resultados sobre dados ainda mutáveis (`Running`) | MUST NOT |

---

## 15. Integrações

| Documento | Contrato de integração |
|---|---|
| **Constitution** | OB2/OB3 realizam Auditabilidade sem comprometer Reversibilidade; fricção proporcional ao risco realizada em §12.3 |
| **Kernel** | Nenhuma alteração — Lifecycle (§3) e Component Contract permanecem intocados; Observability apenas lê |
| **Governance** | Fornece o substrato de consulta que Governance §12 (Audit) usa; autoridade de interpretação permanece exclusivamente lá |
| **Domain Model v1.1.0** | Domain Model §15 (rastreabilidade) é formalizado algoritmicamente por §9.2 — nenhuma entidade nova |
| **RFC-DM-001** | Context Snapshot (§3.2) é a fonte primária de correlação; EX2 (via Execution §12) já garante captura, sem gate novo (§7.2) |
| **Identity & Namespace** | Particionamento por Namespace (§10) herdado; `VersionedIdentifier`/ULID (§4) usados sem extensão |
| **Registry & Discovery** | Distinção explícita de responsabilidade (§1.2) — Registry indexa definições, Observability consulta instâncias, nunca convergem em um mecanismo só |
| **Validation & Certification** | Fornece a base de Evidence e Reproducibility já usada por `provenance()`/`debug()`; nenhuma alteração ao pipeline de certificação |
| **Composition** | Fecha o `[LACUNA proposital]` de Composition §14 |
| **Workflow** | Correlação Step→Execution consumida diretamente por `BuildTrace` |
| **Execution** | Fecha literalmente o contrato conceitual pré-comprometido de Execution §4/§14 |
| **Standards** | `EvidenceRequirement.retention` reutilizado para governar telemetria (§6.3); NRs `applies_to=EXECUTION` podem exigir retenção elevada |
| **Policy** | `scope.applies_at=EXECUTION` + `enforcement_mode` podem vincular Standards de retenção a Namespaces/Organizações específicas, sem novo mecanismo de Policy |
| **Template Architecture** | `ExpandedTemplate` (Artifact já existente) é a fonte usada por `Replay` (§9.3) sem recomputação |
| **Skill Architecture** | Fecha o `[LACUNA proposital]` de Skill §17 (séries de `StepCompleted`/`StepFailed` em escala) |

---

## 16. Validação Institucional

| Documento base | Resultado |
|---|---|
| Constitution | **PASS** |
| Kernel | **PASS** |
| Governance | **PASS** |
| Domain Model v1.1.0 | **PASS** — zero entidades/relações/estados novos |
| RFC-DM-001 | **PASS** |
| Identity & Namespace | **PASS** |
| Registry & Discovery | **PASS** — distinção de responsabilidade formalmente demonstrada (§1.2) |
| Validation & Certification | **PASS** |
| Composition | **PASS** — fecha §14 |
| Workflow | **PASS** |
| Execution | **PASS** — fecha §4/§14, contrato honrado literalmente |
| Standards | **PASS** — fecha §19; retenção reusa §4.6 sem novo vocabulário |
| Policy | **PASS** — fecha §19 |
| Template Architecture | **PASS** |
| Skill Architecture | **PASS** — fecha §17 |
| **Exige RFC?** | **NÃO** |

### Prova formal — item a item do mandato

| Vedação do mandato | Verificação |
|---|---|
| Não cria novos Components | Nenhum `component_type` introduzido — §4.1 |
| Não cria novos Artifacts | Prova explícita em §4.2 — Trace/Span/Timeline/Provenance Chain são Value Objects efêmeros, nunca `Artifact` |
| Não cria novos Lifecycles | §10.3 — `Span.state` é projeção literal de Domain Model §8 |
| Não cria novos estados | Idem |
| Não cria novo Registry | §1.2 — separação formal demonstrada, com precedente de indústria |
| Não cria novo mecanismo de Versionamento | Nenhuma operação de versão — toda referência é `VersionedIdentifier` já existente |
| Não cria novo mecanismo de Discovery | §1.2 — distinção explícita entre "descoberta de definição" (Registry) e "consulta de instância" (Observability) |
| Não cria novo mecanismo de Execution | §7.1 — superfície 100% leitura, zero operação de escrita/dispatch |
| Não cria novo mecanismo de Policy | Reusa `scope`/`applies_at`/`enforcement_mode` sem extensão |
| Não cria novo mecanismo de Standards | Reusa `EvidenceRequirement.retention` sem novo enum (OB9) |

---

## 17. Dependências Futuras

| Consumidor | O que consome | Estado |
|---|---|---|
| **Testing Architecture** (próximo documento) | `provenance()`/`debug()` para rastrear resultado de suites de teste até a Skill/Template original; `query_events()` para análise de regressão histórica; `Trace` como base de cobertura de execução | **Desbloqueado** |
| **Compliance Architecture** (downstream, não ratificada) | Substrato de consulta completo para Compliance Report/Drift, quando ratificada | Sem bloqueio — contrato já suficiente |
| **Packaging & Distribution Architecture** | Formato físico de exportação de métricas (`export_metrics`) | `[LACUNA proposital]` |
| **Organization & Tenancy Architecture** | Particionamento por Namespace (§6.1) já preparado para o slot `org.<id>` reservado (Identity §8/§10) | Sem bloqueio |

---

## 18. Critério de Aceitação

### ✔ Checklist Institucional

| Critério do mandato | Status |
|---|---|
| Não cria novos Components / Artifacts / Lifecycles / estados / Registry / Versionamento / Discovery / Execution / Policy / Standards | ✔ — prova item a item em §16 |
| Reutiliza exclusivamente Execution, Workflow, Skill, Template, Registry, Validation, Domain Model, RFC-DM-001, Standards, Policy | ✔ — §4.1, §15 |
| Trace, Span, Timeline, Provenance Chain formalizados | ✔ — §5, §9.1-§9.2 |
| Correlação Workflow→Step→Execution→Artifact→Evidence | ✔ — §8, §10.2 |
| Auditoria, Replay, Debug, Event Correlation, Query Model | ✔ — §9.3, §9.4, §9.5, §7.1 |
| Retenção de logs, políticas de armazenamento, exportação de métricas | ✔ — §6.1, §6.3, §7.1 |
| Integração completa com Standards e Policy | ✔ — §15, retenção normativa via §4.6 |
| UML, sequência, algoritmos, casos extremos, RFC2119, complexidade, cache | ✔ — §9-§14 |
| Prova de camada transversal sem alterar comportamento funcional | ✔ — §7.1 (zero operação de escrita), §7.2 (nenhum gate novo) |

### ✔ Prova Formal de que Nenhuma RFC Adicional é Necessária

Todo construto introduzido por este documento (`Trace`, `Span`, `Execution Timeline`, `Provenance Chain`, `Debug View`, `Replay View`, `Observability Query Service`) satisfaz uma de duas condições: (a) é uma **projeção de leitura efêmera** sobre dados já persistidos por documentos anteriores, sem Identity, sem persistência, sem Lifecycle — portanto fora do domínio que exigiria emenda ao Domain Model; ou (b) é um **serviço de substrato** da mesma classe arquitetural já usada quatro vezes (Composition Resolver, Scheduler, Standard Resolution Service, Policy Evaluation Service) — nenhuma classe arquitetural nova. Nenhuma linha deste documento contradiz, estreita ou amplia qualquer regra, entidade, relação ou estado dos catorze documentos-base.

### ✔ Próximo Documento Desbloqueado

**Testing Architecture** está desbloqueada sem qualquer dependência pendente: a formalização de geração de casos de teste, execução de suites, cobertura e regressão poderá consumir diretamente `Evaluation Method = DYNAMIC` (Standards §4.6, já usado por Skill §7.3 para certificação funcional), `Evidence` (Domain Model §13) como resultado de cada caso, e — a contribuição específica que só este documento tornava possível — `trace()`/`debug()`/`query_events()` do Observability Query Service para rastrear, correlacionar e analisar regressão sobre séries históricas de Execution já produzidas por Skills e Workflows. **Nenhuma dependência pendente permanece entre Observability Architecture e Testing Architecture.**
