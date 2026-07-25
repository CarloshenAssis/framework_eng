# FASE 2 — Identity & Namespace Architecture

### Framework Eng — Identidade Institucional Permanente

*Versão 1.0.0 — assumes RFC-DM-001 (above) ratified; Domain Model references below are to v1.1.0*

> Este documento não trata de autenticação, autorização ou controle de acesso — isso é competência futura de uma camada de Permission/RBAC ainda não especificada. Este documento trata de uma questão anterior e mais fundamental: **o que faz duas referências apontarem, sem ambiguidade, para a mesma coisa — hoje, e daqui a dez anos.**

---

## 1. Objetivo

Definir o esquema pelo qual **toda** entidade institucionalmente relevante do Framework recebe um identificador permanente, globalmente único, legível por humanos e por máquinas, estável através de renomeações, reorganizações, mudanças de propriedade e décadas de operação — independentemente de onde a entidade esteja fisicamente armazenada ou de qual organização a criou.

Sem este documento, `Registry` (Kernel Architecture §5), `Certification`, `Audit` (Governance Architecture §11-12) e a resolução de `derives_from`/`codifies`/`measures` (RFC-DM-001 acima) não têm uma noção estável do que estão, de fato, referenciando.

---

## 2. Escopo

### 2.1 Entidades com identidade institucional (Entity, no sentido DDD — identidade própria, independente de atributos)

| Entidade | Tem identidade própria? | Observação |
|---|---|---|
| `Component` | **Sim** | Identidade permanente por versão-independente (coordinate) — ver §7. |
| `Manifest` | **Sim** | Identidade derivada de `Component` + versão específica; imutável. |
| `Execution` | **Sim** | Instância única, nunca reaberta. |
| `Artifact` (e especializações: `Evidence`, `Decision Record`, `Context Snapshot`) | **Sim** | Cada instância recebe identificador próprio. |
| `Knowledge` | **Sim** | Necessário para que `derives_from`/`codifies` (RFC-DM-001) sejam referenciáveis de forma estável. |
| `Decision Record` | **Sim** | Ver Artifact acima (é uma especialização). |
| `Metric` | **Sim**, como *definição*; observações individuais da série temporal são Value Objects endereçados por `(metric_id, timestamp)`, sem ID próprio. |
| `Role` | **Sim** — e criticamente, a identidade do **cargo** (ex.: "Governance Area Steward de Security") é distinta da identidade de quem o ocupa; sucessão de ownership (Governance Architecture §5) depende exatamente dessa separação. |
| `Agent` | **Sim** — subtipo de `Component` (Operational), herda o esquema de identidade de Component. Nota importante: a identidade institucional de um Agent **é independente da versão do modelo subjacente que o executa** — um Agent mantém sua Identity mesmo que o modelo de IA por trás dele mude de versão; o modelo é um detalhe de implementação do Agent, não parte de sua identidade. |
| `Context Snapshot` | **Sim** (introduzido pela RFC-DM-001 acima) — precisa de identidade permanente exatamente porque sua razão de existir é ser referenciável indefinidamente. |
| `Registry` | **Sim**, forward-compatible — este documento não implementa Registry, mas garante que o esquema de identidade que ele vai indexar já é estável (§9). |
| `Organization` | **Sim**, forward-compatible — mesma lógica; este documento reserva o espaço estrutural (§8, §10) sem especificar o modelo interno de Organization, que é escopo de um documento futuro dedicado. |

### 2.2 Entidades sem identidade institucional própria (Value Object, no sentido DDD — definidas por atributos, endereçadas apenas via seu portador)

| Entidade | Por que não |
|---|---|
| `Contract` | Escopado 1:1 a um `Manifest` — não tem ciclo de vida próprio fora dele. |
| `Capability` | Escopada a um `Contract` — endereçada como `<component-coordinate>@<version>#capability/<nome>`, nunca isoladamente. |
| `Context` (a versão viva, não o Snapshot) | Transitória por definição (Domain Model §9) — correlacionada por um ID de correlação de curta duração, não por identidade institucional permanente. |
| `Relationship` (instâncias de `depends_on`, `provides_for` etc.) | Determinada de forma única pela tupla `(origem, destino, tipo, versão)` — não precisa de UUID próprio. |

Esta distinção Entity/Value Object (DDD) é o critério de admissão para "precisa de identificador institucional" usado em todo este documento — evita o erro comum de dar identidade global a tudo, o que infla o Registry sem necessidade.

---

## 3. Namespace Model

Um **Namespace** é uma partição hierárquica, nomeada, que garante que dois `Component`s (ou qualquer entidade com identidade) com o mesmo nome local, criados por organizações ou domínios diferentes, nunca colidem.

### 3.1 Estrutura hierárquica

```
<namespace> ::= <root-segment> ("/" <segment>)*
```

Segmentos válidos, da raiz para as folhas:

1. **Root reservado `core`** — o núcleo reutilizável do Framework (Constitution, camada "núcleo" vs. "Domain" específico de organização). Escrita restrita à autoridade do Framework Council (Governance Architecture §8).
2. **`org.<organization-id>`** — um segmento por Organização (Organization formalizada em documento futuro; este documento apenas reserva e garante o slot — ver §10).
3. **`domain.<bounded-context>`** *(opcional, dentro de um `org` ou de `core`)* — o sentido DDD de `Domain`, agora unívoco após RFC-DM-001 §3.5 (ex.: `org.acme/domain.billing`).
4. **`env.<environment>`** *(opcional, folha adicional para organizações que precisam separar, por exemplo, componentes em sandbox de componentes certificados para produção — é uma partição de identidade, não uma preocupação de infraestrutura de deployment)*.

**Decisão de design explícita:** o tipo de componente (`Standard`, `Skill`, `Agent`...) **NÃO** faz parte do caminho do Namespace — é um atributo de classificação ortogonal (Kernel Architecture §2.14, Metadata), não uma partição de identidade. `[ESCOLHA DE DESIGN]`, justificada por paralelo direto com Kubernetes: `Namespace` e `Kind` são ortogonais na API Machinery (um `Namespace` pode conter Pods, Services e ConfigMaps ao mesmo tempo); misturar as duas dimensões aqui produziria o mesmo anti-padrão que a Kubernetes API deliberadamente evita.

### 3.2 Isolamento e prevenção de colisão

- Dentro de um mesmo Namespace, o nome local de um `Component` **MUST** ser único entre todas as versões, incluindo as de componentes `Deprecated` ou `Archived`.
- Um nome local, uma vez usado por qualquer Component que tenha alcançado `Active` (Kernel Architecture §3), **MUST NOT** ser reatribuído a um Component diferente — mesmo após `Removed`. O nome é reservado permanentemente (tombstone), nunca reciclado. `[ESCOLHA DE DESIGN]`, justificada por paralelo com a prática de PyPI/npm de proibir reuso de nomes de pacote removidos, evitando *dependency confusion* e falsificação de identidade histórica.
- Entre Namespaces diferentes, **não há nenhuma restrição de colisão** — `org.acme/billing.invoice-validator` e `org.globex/billing.invoice-validator` são identidades completamente distintas e válidas simultaneamente. Isso é a garantia central de isolamento multi-tenant (§10).

---

## 4. Identifier Specification

### 4.1 Duas formas de identidade, deliberadamente distintas

1. **Coordinate Identifier** (identidade definicional, independente de versão): identifica *o que é este Component*, não *qual versão*.
   ```
   <namespace>/<local-name>
   ex.: core/quality.code-reviewer
        org.acme-corp/domain.billing/invoice-validator
   ```
2. **Versioned Identifier** (identidade + uma versão específica):
   ```
   <namespace>/<local-name>@<semver>
   ex.: core/quality.code-reviewer@2.3.0
   ```

Esta separação existe porque **Identity é permanente e Version não é** (Kernel Architecture §2.1 vs §2.11) — colapsar as duas em um único token reintroduziria exatamente a ambiguidade que a correção H3 da RFC-DM-001 acabou de eliminar na cardinalidade Component:Manifest.

### 4.2 Instance Identifier (para entidades-evento: Execution, Artifact, Knowledge, Decision Record, Context Snapshot)

Entidades de instância única (não definicional) recebem um identificador de instância **ULID** (Universally Unique Lexicographically sortable IDentifier) em vez de inteiro sequencial.

**Justificativa técnica:**
- **Sem coordenação central** — Agents e Executions distribuídos em múltiplas organizações podem gerar identificadores válidos offline, sem consultar um serviço central. Um inteiro auto-incremento exigiria exatamente esse ponto único de coordenação, inviável em escala multi-organização.
- **Ordenável por tempo** — ULIDs preservam ordem cronológica na própria string, o que é diretamente útil para reconstruir a sequência de Executions em uma auditoria (Domain Model §15) sem depender de um campo de timestamp separado sujeito a divergência de relógio.
- **Colisão desprezível em escala global** — mesmo com milhões de Executions/dia distribuídas entre centenas de organizações, a probabilidade de colisão é criptograficamente irrelevante.

Esta é a mesma justificativa que levou sistemas distribuídos maduros e Event Sourcing a abandonar chaves sequenciais em favor de UUID/ULID — não é uma escolha nova, é a aplicação de uma prática já validada.

### 4.3 Forma canônica completa (URN)

```
urn:framework-eng:<coordinate>[@<version>][:<entity-type>:<instance-id>]
```

Exemplos:
```
urn:framework-eng:core/quality.code-reviewer@2.3.0
urn:framework-eng:core/quality.code-reviewer@2.3.0:execution:01JB3XQZ8K7VG3T9YHDW2QATZR
urn:framework-eng:org.acme-corp/domain.billing/invoice-validator@1.4.1:knowledge:01JB3Y1H9M2R5S8VQKX3ZC7NWT
```

**Nota sobre registro do NID:** `framework-eng` é um Namespace Identifier de URN de uso interno/institucional. Registro formal junto ao IANA só é necessário se identificadores precisarem resolver fora do próprio ecossistema do Framework — não é um requisito deste documento, apenas uma extensão possível e não bloqueante.

### 4.4 Regras de encoding

- Segmentos de namespace e nome local **MUST** usar apenas `[a-z0-9]`, `-` e `.` como separador de sub-segmento — o mesmo conjunto de caracteres de rótulos DNS válidos (RFC 1123), a mesma convenção que Kubernetes usa para `metadata.name`. Justificativa: um identificador válido é, sem escaping, também um caminho de arquivo, um segmento de URL e um rótulo de subdomínio válidos — elimina uma classe inteira de bugs de escaping em ferramentas futuras.
- Versão **MUST** seguir SemVer 2.0.0 estrito (já mandatado por Kernel Architecture §2.11).
- Instance ID **MUST** ser um ULID de 26 caracteres, Crockford Base32.

### 4.5 Representação canônica

A forma **totalmente qualificada** (namespace + nome + versão + tipo + instância, quando aplicável) é a **única forma válida para armazenamento, referência entre Components e serialização em Manifests**. Formas curtas (aliases, nomes sem namespace) são permitidas **apenas** como conveniência de exibição/entrada humana e **MUST** ser resolvidas à forma canônica antes de qualquer persistência (ver §6).

---

## 5. Naming Convention

| Tipo | Convenção | Exemplo |
|---|---|---|
| Component (geral) | `<namespace>/<categoria>.<nome-descritivo>` | `core/quality.code-reviewer` |
| Standard | `<namespace>/standard.<área>.<nome>` | `core/standard.security.input-validation` |
| Policy | `<namespace>/policy.<área>.<nome>` | `org.acme/policy.data-residency.eu-only` |
| Template | `<namespace>/template.<artifact-type>` | `core/template.adr` |
| Skill | `<namespace>/skill.<capacidade>` | `core/skill.static-analysis.sql-injection-scan` |
| Agent | `<namespace>/agent.<papel>` | `core/agent.code-reviewer` |
| Metric (definição) | `<namespace>/metric.<domínio>.<nome>` | `core/metric.governance.admission-time` |
| Artifact (instância) | `<component-coordinate>@<version>:artifact:<ulid>` | ver §4.3 |
| Execution (instância) | `<component-coordinate>@<version>:execution:<ulid>` | ver §4.3 |
| Knowledge (instância) | `<component-coordinate>@<version>:knowledge:<ulid>` | ver §4.3 |
| Decision Record (instância) | `<namespace>:decision-record:<ulid>` (não escopado a um único Component — pode referenciar N) | — |
| Namespace | `<segmento>[.<segmento>]*` (minúsculo, DNS-safe) | `org.acme-corp.domain.billing` |
| Organization | `org.<organization-id>` (reservado; ver §10) | `org.acme-corp` |

---

## 6. Resolution Rules

1. **Aliases.** Um Namespace **MAY** registrar apelidos curtos para uso humano (ex.: `code-reviewer` → `core/quality.code-reviewer`). Aliases **MUST** ser escopados ao Namespace em que são declarados — nunca globais — para não recriar o problema de colisão que o esquema inteiro existe para evitar.
2. **Lookup.** Toda resolução **MUST** partir de um Namespace explícito ou de uma cadeia de resolução de alias declarada — não existe busca "por nome nu" em escopo global. Isso é uma decisão deliberada: buscas sem escopo são exatamente o que produz ambiguidade em sistemas com milhares de componentes.
3. **"latest".** É um alias especial, resolvido como a versão de maior precedência SemVer entre as que estão em Lifecycle `Active` — nunca inclui `Draft`, `Deprecated` ou posteriores.
4. **Renomeações.** A Identity (nome local dentro do namespace) de um Component em `Active` **MUST NOT** ser mutada in-place — isso violaria Kernel Architecture §2.1 (Identity é permanente). Uma "renomeação" é modelada como: (a) criação de uma nova coordinate, (b) o Component antigo migra para `Deprecated` com uma relação `redirects_to` apontando à nova coordinate, (c) o nome antigo entra no regime de reserva permanente do §3.2.
5. **Componentes descontinuados.** Resolver a coordinate de um Component `Removed` **MUST** retornar um registro tombstone (não um erro silencioso) — contendo, quando existir, o `redirects_to` para o substituto.
6. **Redirecionamentos.** `redirects_to` é seguido automaticamente pela resolução, mas o resultado **MUST** expor a cadeia de redirecionamento completa ao chamador (nunca ocultada) — consistente com o princípio de rastreabilidade do Domain Model §15. Profundidade de redirecionamento **MUST** ter um limite máximo (ex.: 5 saltos) para impedir ciclos de redirecionamento.
7. **Resolução canônica (algoritmo).** input humano/alias → verificar tabela de alias do Namespace corrente → verificar cadeia de `redirects_to` até estabilizar ou atingir o limite → retornar URN canônico completo + o caminho de resolução percorrido (para auditoria).

---

## 7. Version-aware Identity

| Conceito | Definição | Onde vive |
|---|---|---|
| **Identity** | O par `(namespace, local-name)` — permanente, independente de versão. | Coordinate Identifier (§4.1) |
| **Version** | Um rótulo SemVer atribuído a um `Manifest` específico. | Atributo do Manifest (Kernel §2.11) |
| **Lineage** | A sequência ordenada e imutável de todas as versões já publicadas para uma Identity, do primeiro Manifest ao mais recente. | Derivado da relação `Component "1"—"1..*" Manifest` (corrigida pela RFC-DM-001 §3.6) |
| **`supersedes`** | Aresta explícita entre duas versões consecutivas na Lineage — generalizado nesta arquitetura para além do uso original em `Decision Record` (RFC-DM-001), agora aplicável a qualquer par de versões de Component. | Relação Manifest → Manifest |
| **Compatibility** | Faixa SemVer que um Consumer declara aceitar de uma Identity — validada contra a Lineage, nunca contra uma versão isolada. | Kernel Architecture §2.13 |

**Regra de consistência com RFC-DM-001 §3.3:** a Lineage, assim como o grafo `derives_from`, **MUST** ser temporalmente monotônica e acíclica — mesma classe de regra, dois grafos diferentes, um único mecanismo de validação (Kernel §7) reaplicado.

---

## 8. Namespace Hierarchy

```
urn:framework-eng:
│
├── core/                                  [somente-escrita: Framework Council]
│   ├── quality/
│   ├── delivery/
│   ├── architecture/
│   ├── security/
│   └── ...
│
├── org.<organization-id>/                 [um por Organization — ver §10]
│   ├── domain.<bounded-context>/          [opcional — sentido DDD, pós H1]
│   │   └── <component-name>
│   ├── env.<environment>/                 [opcional — partição de identidade, não de infraestrutura]
│   └── <component-name>                   [componentes sem domain explícito]
│
└── reserved/                              [palavras reservadas — não reivindicáveis como organization-id]
    ├── core
    ├── org
    ├── system
    ├── registry
    └── urn
```

**Regra de reserva:** os tokens `core`, `org`, `system`, `registry`, `urn`, `reserved` **MUST NOT** ser aceitos como `<organization-id>` — previne que uma organização reivindique um segmento que colidiria com a estrutura institucional do próprio Framework.

---

## 9. Registry Integration

Este documento **não implementa** Registry (Kernel Architecture §5 o descreve operacionalmente; uma futura Registry Architecture o formalizará como entidade — achado H4 da revisão institucional). O que este documento garante é o **contrato conceitual estável** sobre o qual Registry será construído, sem antecipar sua implementação:

- `resolve(identifier: Coordinate | VersionedIdentifier | Alias) → EntityDescriptor` — toda resolução passa pelas regras do §6.
- `list(namespace: Namespace, filter?: Classification) → Coordinate[]` — descoberta é sempre escopada a um Namespace (ou explicitamente à raiz, para uma busca institucional completa).
- `lineage(coordinate: Coordinate) → Manifest[]` — expõe a Lineage completa (§7) de uma Identity.

Registry, quando especificado, **MUST** indexar exclusivamente por estes identificadores canônicos — nunca por caminho de arquivo, nome de exibição, ou qualquer identificador não regido por este documento.

---

## 10. Multi-tenancy Readiness

- O limite de Namespace (`org.<organization-id>`) **é**, por construção, o limite de isolamento de identidade entre organizações — dois Namespaces distintos nunca colidem, por definição do próprio esquema (§3.2).
- Referências **cross-namespace** (uma organização consumindo um Component `core` ou de outra organização) **MUST** usar a forma totalmente qualificada (§4.5) — não existe resolução implícita entre Namespaces de organizações diferentes. Isso fecha, no nível de identidade, a lacuna de relacionamento `imports`/`exports` identificada na revisão institucional anterior: um `depends_on` (Domain Model §5) cruzando fronteira de Namespace **é**, estruturalmente, um import — sem precisar de um relacionamento novo, apenas de uma referência corretamente qualificada.
- **Fora de escopo aqui, deliberadamente:** billing, membership, quotas e o modelo de dados completo de `Organization` — apenas o *slot* de Namespace e a garantia de isolamento de identidade são entregues por este documento; o restante é uma futura Organization & Tenancy Architecture (roadmap). `[LACUNA reconhecida e delimitada — não é decisão de design escondida]`.

---

## 11. Future Compatibility

| Documento futuro | Como este esquema já o suporta, sem modificação |
|---|---|
| **Registry Architecture** | Contrato conceitual já definido (§9); Registry apenas implementa `resolve`/`list`/`lineage` sobre o esquema existente. |
| **Discovery Architecture** | `list(namespace, filter)` já dá a base de busca por Namespace/Classification (Kernel §5). |
| **Validation Architecture** | Todo resultado de validação é um `Artifact`, logo já herda identidade institucional (§2.1) automaticamente. |
| **Certification Architecture** | Certificação referencia uma `Versioned Identifier` específica — nunca uma Coordinate sem versão — garantindo que a certificação nunca "escorregue" silenciosamente para uma versão não avaliada. |
| **Organization & Tenancy Architecture** | O slot `org.<organization-id>` (§8) e a garantia de isolamento (§10) já estão reservados; esse documento futuro preenche o *modelo interno*, não a identidade. |
| **Composition & Orchestration Architecture** | `composed_of` (relação ainda a ser formalizada) referenciará Executions por seu Instance Identifier (§4.2) — já suficiente, nenhuma extensão de identidade necessária. |
| **Workflow Architecture** | Fases/Gates (conceitos ainda a formalizar) serão Value Objects escopados a um Workflow Execution — não precisam de identidade própria além do padrão já definido em §2.2. |
| **Agent Architecture** | A separação Agent-identity vs. modelo-subjacente (§2.1) já está estabelecida — Agent Architecture não precisa reabrir essa questão. |
| **Observability Architecture** | `Metric` já tem identidade de definição própria (§2.1); observações de série temporal já seguem o padrão Value Object `(metric_id, timestamp)` (§2.1). |
| **Packaging & Distribution Architecture** | A forma canônica totalmente qualificada (§4.5) é exatamente o que um pacote distribuído precisa carregar como manifesto de dependência — nenhuma tradução adicional necessária. |
| **Testing Architecture** | Ambientes de teste usam o segmento `env.<environment>` (§3.1, §8) já reservado no esquema. |

---

## 12. Final Validation

| Verificação | Resultado | Evidência |
|---|---|---|
| Unicidade | **PASS** | Chave composta `(namespace, local-name, version)` garante unicidade; instâncias usam ULID com colisão desprezível (§4.2). |
| Colisões | **PASS** | Isolamento por Namespace (§3.2, §10); nomes reservados protegidos (§8). |
| Namespaces | **PASS** | Hierarquia completa definida (§8), com tokens reservados e regra de reserva permanente de nomes descontinuados. |
| Versionamento | **PASS** | Coordinate vs. Versioned Identifier explicitamente separados (§4.1); Lineage formalizada (§7), consistente com a correção de cardinalidade da RFC-DM-001 §3.6. |
| Migração | **PASS (vácua)** | Zero identificadores pré-existentes no Framework — nenhuma migração de dados é necessária; o esquema nasce já correto. |
| Referências | **PASS** | Toda entidade referenciável tem forma canônica definida (§4.3); nenhuma referência solta (o defeito C4 da RFC-DM-001 é resolvido de ponta a ponta aqui, com `Namespace` agora formalizado). |
| Retrocompatibilidade | **PASS** | Este documento não altera nenhum identificador previamente definido — é estritamente aditivo sobre a RFC-DM-001. |
| Consistência terminológica | **PASS** | `Domain` usado exclusivamente no sentido DDD (§3.1, pós-H1); nenhuma nova colisão de nome introduzida — verificado contra o glossário do Domain Model v1.1.0. |
