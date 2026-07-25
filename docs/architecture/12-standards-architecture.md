> **Nota de versionamento editorial:** os documentos abaixo são as versões ratificáveis v1.0.0 de Standards Architecture e Policy Architecture. Eles **substituem integralmente** os rascunhos de mesmo nome produzidos no Bloco 4 (Documentos 1 e 2 daquele bloco), incorporando os construtos adicionais exigidos por este mandato — Requirement Identifier formal, Evidence Requirement, Partial/Strict Conformance, Backward/Forward Compatibility, Replacement, Lineage, Standard Packages, e as classes nomeadas de Policy — além dos dois algoritmos formais exigidos. Nenhum documento da base normativa é alterado. Compliance Architecture permanece **consumidor downstream**, não base normativa deste bloco.

---
---

# DOCUMENTO 1 — Standards Architecture

### Framework Eng — O Corpo Normativo Reutilizável

*Versão 1.0.0 · Base normativa: Constitution · Kernel · Governance · Domain Model v1.1.0 · RFC-DM-001 · Identity & Namespace · Registry & Discovery · Validation & Certification · Composition · Workflow · Execution*

---

## 1. Posição Arquitetural

Um `Standard` é uma especialização de **Structural Component** — categoria já nomeada em Domain Model §3 e jamais redefinida aqui. Standards Architecture especifica **a gramática interna pela qual um Standard expressa o significado de conformidade**, e nada além disso.

**Responsabilidade institucional exclusiva:** ser a única fonte de definição normativa do Framework. Nenhuma outra camada — Policy, Compliance, Certification, Workflow, Composition — define critério. Todas o consomem por referência versionada.

### 1.1 Fronteiras negativas (invioláveis)

| Fronteira | Regra | Documento que detém a responsabilidade |
|---|---|---|
| Standard não conhece contexto | Um Standard **MUST NOT** expressar aplicabilidade contextual (organização, namespace, role, ambiente, condição temporal) | Policy Architecture (Documento 2) |
| Standard não avalia | Um Standard **MUST NOT** conter lógica de veredito ou julgamento sobre um sujeito concreto | Compliance Architecture (downstream) |
| Standard não bloqueia | Um Standard **MUST NOT** declarar consequência de não conformidade | Policy (`enforcement_mode`) e Workflow §4 (`GATE_AUTO`) |
| Standard não se registra | Um Standard **MUST NOT** ser publicado em serviço distinto do Registry existente | Registry & Discovery §3.1 |
| Standard não define seu próprio ciclo de vida | Kernel Lifecycle aplica-se integralmente e sem exceção | Kernel §3 |

### 1.2 Relação com forward-references já existentes

Dois pontos da base normativa apontavam para uma especificação inexistente. Este documento os fecha **sem alterá-los**:

- **Kernel §2.14** prevê `standards_bound` no Manifest de qualquer Component — uma lista de identificadores cuja estrutura-alvo nunca fora definida. Este documento define o alvo.
- **Validation & Certification §5** define o nível **L3 — Standards Certified** como "Conformance a todo Standard/Policy vinculado", exigindo `Conformance Evidence por Standard`, sem que existisse gramática de conformance verificável. Este documento fornece essa gramática, e §8.4 estabelece a regra exata de suficiência para L3.

`[ESCOLHA DE DESIGN]` Fechar forward-references por **especificação aditiva downstream**, em vez de emendar os documentos que os contêm. Alternativa rejeitada: RFC de emenda a Kernel §2.14 e Validation & Certification §5 para embutir a gramática lá. Rejeitada por três motivos: (a) violaria a imutabilidade declarada da base normativa; (b) inflaria o Kernel com detalhe de domínio normativo, contrariando Kernel §0 ("o Kernel tem opinião sobre uma coisa só: a forma que qualquer coisa precisa ter"); (c) o padrão de fechar forward-reference por documento downstream já é precedente estabelecido — Workflow Architecture §8 fechou exatamente assim o critério de Conformance para `component_type = Workflow` anunciado em Validation & Certification §7.

---

## 2. Objetivo e Motivação

### 2.1 Problema resolvido

Antes deste documento, conformidade normativa no Framework era verificável apenas por julgamento textual: um Reviewer lia um Standard escrito em prosa e formava uma opinião. Isso produz três falhas estruturais, todas explicitamente condenadas pela base normativa:

1. **Não reprodutibilidade** — Validation & Certification §6 exige `reproducible: true` como condição para L4. Julgamento textual não é reproduzível por construção.
2. **Não rastreabilidade granular** — Domain Model §15 exige que toda Evidence responda "contra qual versão de qual Component". Sem identificadores estáveis por requisito, Evidence só pode apontar para o Standard inteiro, tornando impossível reconstruir *qual regra específica* foi verificada.
3. **Engenharia como arte individual** — Constitution §Modelo de Engenharia rejeita explicitamente o modelo em que "qualidade depende do talento de quem executa naquele momento".

### 2.2 Objetivos

| # | Objetivo | Mecanismo |
|---|---|---|
| O1 | Conformidade verificável, não opinável | Normative Requirement estruturado com Evaluation Method e Evidence Requirement (§4) |
| O2 | Reuso entre organizações sem modificação | Ausência estrutural de contexto (§1.1, ST1) |
| O3 | Reuso entre Standards sem duplicação de requisito | `extends` / `includes` com semânticas distintas (§6) |
| O4 | Evolução normativa sem invalidar histórico | Requirement Identifier estável + lineage + semântica SemVer própria (§5, §7) |
| O5 | Graduação de exigência | Conformance Level monotônico + Strict/Partial Conformance (§4.4, §8) |
| O6 | Distribuição de baselines curados | Standard Package como Standard puramente agregador (§9) |

---

## 3. Escopo

### 3.1 Pertence a esta arquitetura

Estrutura formal de um Standard; Normative Requirement como unidade atômica; Requirement Identifier e sua estabilidade; Compliance Target; Conformance Level; Evaluation Method; Evidence Requirement; herança e composição entre Standards; conformidade estrita e parcial; compatibilidade retroativa e prospectiva; evolução, deprecação, substituição e lineage; Standards cross-namespace; Standard Packages.

### 3.2 Não pertence — com justificativa individual

| Excluído | Justificativa técnica |
|---|---|
| **Aplicabilidade (quando/para quem)** | Pertence a Policy (Documento 2). Embutir aplicabilidade destruiria O2: um Standard com condições organizacionais embutidas só serve à organização que as escreveu, impossibilitando o modelo `core/` compartilhado garantido por Identity & Namespace §8/§10. Precedente: ISO define controles; o escopo de certificação é declarado pela organização, não pela norma. |
| **Avaliação de conformidade real** | Pertence a Compliance (downstream). Colapsar norma e verificação eliminaria a independência do avaliador exigida por Governance §12 ("quem audita não pode ter aprovado ou sido Owner do que audita"). |
| **Registro e descoberta** | Já resolvido. Registry & Discovery §3.1 indexa `Standard` explicitamente. Um "Standard Registry" dedicado violaria a proibição de duplicar responsabilidades do Registry e criaria duas fontes de verdade sobre existência de Component. |
| **Arbitragem entre Standards conflitantes de mesma precedência** | Já resolvido por Governance §17 (Conflict Resolution) e pela hierarquia da Constitution. Este documento garante que a contradição seja *estruturalmente detectável* (§10), não que seja resolvida automaticamente. |
| **Autoridade de aprovação** | Já resolvido por Governance §8: Standards são aprovados por Governance Area Steward. Definir autoridade nova seria duplicação de Governance. |
| **Consequência de não conformidade** | Pertence a Policy (`enforcement_mode`) e a Governance §13. Um Standard que declarasse "bloquear se violado" estaria decidindo aplicabilidade — violação de §1.1. |
| **Formato físico de serialização** | `[LACUNA proposital]` deferida a Packaging & Distribution Architecture. Este documento especifica estrutura lógica; a serialização canônica herda as regras de encoding já fixadas em Identity & Namespace §4.4. |

---

## 4. Modelo Conceitual

### 4.1 Tabela de proveniência conceitual

Conformidade com a Restrição Arquitetural 1-8 do mandato: nenhuma linha abaixo introduz entidade, relação ou lifecycle.

| Conceito | Natureza | Base / precedente estrutural |
|---|---|---|
| `Standard` | **Especializado** — Structural Component | Domain Model §3 |
| **Normative Requirement (NR)** | **Value Object** interno ao Contract | Padrão de `Capability` (Identity §2.2), `Phase`/`Step` (Workflow §4), `Composition Slot` (Composition §4) |
| **Requirement Identifier** | **Value Object** — identificador local estável | Análogo à qualificação de `Capability` em Identity §2.2 |
| **Compliance Target** | **Value Object** interno ao NR | — |
| **Conformance Level** | **Value Object** interno ao Contract | Conformance classes do W3C |
| **Evaluation Method** | **Value Object** interno ao NR | — |
| **Evidence Requirement** | **Value Object** interno ao Evaluation Method | Especializa a exigência de `Evidence` (Domain Model §13) sem criar subtipo |
| **Conformance Claim** | **Artifact** genérico | Mesmo padrão de `Assembly` (Composition §4), `Execution Plan` (Execution §4) |
| **Standard Package** | **Standard** com perfil estrutural restrito (§9) | Nenhum construto novo |
| `Constraint` | **Reutilizado** | Kernel §2.10 |
| `Capability` | **Reutilizado** | Kernel §2.9 |
| Precedence level | **Reutilizado** | Constitution (hierarquia de 4 níveis) |
| Identidade, versão, lineage, `supersedes` | **Reutilizado** | Identity & Namespace §4, §5, §7 |
| Lifecycle | **Reutilizado sem alteração** | Kernel §3 |
| Detecção de ciclo | **Reutilizado (4ª aplicação)** | Kernel §7 |
| Registro e descoberta | **Reutilizado** | Registry & Discovery §3.1, §6.2 |
| Certificação do próprio Standard | **Reutilizado** | Validation & Certification §7, linha Standard/Policy |

**Nenhum construto exige RFC.** Todos satisfazem o critério formal de Value Object de Identity & Namespace §2.2 — definidos por atributos, sem identidade institucional própria, endereçados exclusivamente através de seu portador — ou são `Artifact` genérico já existente.

### 4.2 Estrutura formal do Standard

```
Standard (Structural Component) {
  identity          : Coordinate                    [Identity §4.1 — reutilizado]
  version           : SemVer                        [Kernel §2.11 — semântica especializada em §7]
  lifecycle_state   : KernelLifecycleState          [Kernel §3 — reutilizado, nunca estendido]
  owner             : Role                          [Kernel §2.3 — reutilizado]

  precedence_level  : GLOBAL | DOMAIN | STACK | PROJECT      [Constitution — reutilizado]
  standard_kind     : NORMATIVE | PACKAGE                     [§9]

  extends           : [VersionedIdentifier]?                  [§6.1]
  includes          : [VersionedIdentifier]?                  [§6.2]
  replaces          : VersionedIdentifier?                    [§7.4]

  requirements      : NormativeRequirement[]                  (vazio obrigatório se PACKAGE — §9)
  conformance_levels: ConformanceLevel[]
  retired_rids      : [RequirementIdentifier]                 (tombstones — §5.3)
}
```

### 4.3 Normative Requirement

```
NormativeRequirement {
  rid               : RequirementIdentifier         [§5]
  normative_keyword : MUST | MUST_NOT | SHOULD | SHOULD_NOT | MAY     [RFC 2119]
  statement         : NormativeText                 (prosa normativa, human-authoritative)
  rationale         : Text?                         (não normativo; existe para auditoria)
  target            : ComplianceTarget              [§4.5]
  evaluation        : EvaluationMethod              [§4.6]
  constraint        : Constraint?                   [Kernel §2.10 — reutilizado]
  supersedes        : RequirementIdentifier?        (dentro da própria lineage — §5.4)
  introduced_in     : SemVer                        (versão do Standard em que surgiu — §7.5)
}
```

**Regra de dualidade prosa/estrutura:** `statement` é a fonte normativa autoritativa para leitura humana; `evaluation` é a fonte autoritativa para verificação mecânica. Quando divergem, `statement` prevalece para fins de interpretação institucional, e a divergência **MUST** ser tratada como defeito do Standard, corrigível apenas por nova versão. Justificativa: subordinar a prosa ao mecanismo transformaria limitações do avaliador em relaxamento silencioso da norma — inaceitável sob Constitution (Confiança verificável).

### 4.4 Conformance Level

```
ConformanceLevel {
  name          : LevelName                (ex.: BASE, EXTENDED, STRICT — nomes livres)
  requires      : [RequirementIdentifier]
  inherits_from : LevelName?               (monotonicidade obrigatória)
  description   : Text
}
```

**Regra de monotonicidade (ST5):** se `L2.inherits_from = L1`, então `requires(L2) ⊇ requires(L1)`. Um nível superior **MUST NOT** relaxar, remover ou enfraquecer qualquer requisito de um nível inferior.

`[ESCOLHA DE DESIGN]` Monotonicidade obrigatória em vez de níveis arbitrariamente compostos. Alternativa rejeitada: permitir níveis independentes com conjuntos disjuntos de requisitos (modelo "flavors"). Rejeitada porque a ordenação por conformidade é consumida diretamente por Composition §7 (`select_best`: maior certificação primeiro) e por Policy (§4.4 do Documento 2, união restritiva escolhendo "nível mais alto"). Sem monotonicidade, "nível mais alto" não seria uma relação de ordem e ambos os algoritmos perderiam fundamento semântico. Precedente: conformance classes cumulativas do W3C e níveis de conformidade OpenAPI. Níveis genuinamente disjuntos são expressáveis por **Profiles via `includes`** (§6.2) sem quebrar a ordem.

### 4.5 Compliance Target

```
ComplianceTarget {
  component_types    : [ComponentType] | ANY
  capability_filter  : CapabilitySignature?         [Kernel §2.9 — reutilizado]
  applies_to         : MANIFEST | COMPOSITION | EXECUTION | ARTIFACT
}
```

`ComplianceTarget` declara a **classe estrutural** de sujeito. **MUST NOT** referenciar Namespace, Organization, Role, ambiente, ou qualquer predicado sobre `Context` (ST1). Esta restrição é mecanicamente verificável na validação (§5 do Modelo Operacional), o que torna a fronteira Standard/Policy uma propriedade checada, não uma convenção documentada.

`[ESCOLHA DE DESIGN]` Proibir Namespace em `ComplianceTarget`. Alternativa rejeitada: permitir `namespace_filter`, o que pareceria conveniente para Standards de escopo organizacional. Rejeitada porque criaria **dois mecanismos concorrentes de escopo** — `Target` em Standard e `Scope` em Policy — reintroduzindo exatamente a classe de duplicidade conceitual que RFC-DM-001 eliminou nos achados C1 e H1, e tornando indecidível qual mecanismo governa em caso de divergência. Precedente: no Kubernetes, `CustomResourceDefinition` (o que é válido) não carrega selectors de namespace; isso é responsabilidade de binding separado.

### 4.6 Evaluation Method e Evidence Requirement

Dois conceitos deliberadamente separados: `EvaluationMethod` responde **como se verifica**; `EvidenceRequirement` responde **o que deve existir e persistir como prova**.

```
EvaluationMethod {
  kind          : STATIC | DYNAMIC | ATTESTED
  procedure_ref : CapabilitySignature?      (capacidade requerida do avaliador — Kernel §2.9)
  deterministic : boolean
  evidence      : EvidenceRequirement
}

EvidenceRequirement {
  evidence_kind      : STRUCTURAL | TEST_RESULT | ANALYSIS_OUTPUT | ATTESTATION | EXECUTION_TRACE
  producer_role_class: RoleClass?           (Governance §2 — quem tem autoridade para produzir)
  reproducible       : boolean              [Validation & Certification §6 — reutilizado]
  freshness_window   : Duration?            (validade máxima da Evidence antes de exigir recoleta)
  retention          : PERMANENT | BOUNDED(Duration)
  minimum_artifacts  : Integer              (default 1)
}
```

**Semântica de `kind`:**

| kind | Verificação | Evidence típica | Consequência de ausência |
|---|---|---|---|
| `STATIC` | Inspeção do Manifest/Assembly sem execução | STRUCTURAL | Verdict determinável sem Evidence externa |
| `DYNAMIC` | Requer Execution real do sujeito | TEST_RESULT, EXECUTION_TRACE | Verdict **MUST** ser indeterminado (§8.3) |
| `ATTESTED` | Requer afirmação humana ou de Role autorizado | ATTESTATION | Verdict **MUST** ser indeterminado (§8.3) |

**Regra de retenção (ST9):** `retention = PERMANENT` **MUST** ser declarado para todo NR cujo Standard tenha `precedence_level = GLOBAL`. Justificativa: Evidence de conformidade a norma não negociável integra o registro institucional permanente exigido por Constitution (Auditabilidade) e por Domain Model §9 (entidades de Governança nunca são verdadeiramente transitórias).

**Regra de determinismo:** `deterministic = false` **MUST** implicar `evidence.reproducible = false`. A combinação `deterministic = false` com `reproducible = true` é contraditória e **MUST** ser rejeitada na validação.

---

## 5. Requirement Identifier

### 5.1 Estrutura

```
RequirementIdentifier ::= <local-rid>
QualifiedRequirementIdentifier ::= <standard-coordinate> "#" <local-rid>
```

- `<local-rid>` **MUST** ser único dentro do Standard, ao longo de **toda a sua lineage** (não apenas dentro de uma versão).
- Encoding herda integralmente as regras de Identity & Namespace §4.4: `[a-z0-9]`, `-`, `.` como separadores. Nenhum esquema novo de encoding é introduzido.
- Referências externas (por Policy, Compliance, Evidence, Certification) **MUST** usar a forma qualificada, e **MUST** incluir a versão do Standard quando a semântica temporal importar:

```
urn:framework-eng:core/standard.security.input-validation@2.1.0#nr.sql-injection.parameterized-queries
```

Esta forma é uma aplicação direta da forma canônica de Identity & Namespace §4.3, com o fragmento `#` cumprindo, para NRs, o mesmo papel que `#capability/<nome>` já cumpre para Capabilities (Identity §2.2). **Nenhuma extensão do esquema de identidade é necessária.**

### 5.2 Estabilidade semântica (ST6)

Dentro de uma mesma **major version** de um Standard, um `rid` **MUST NOT**:
- ser removido do Standard;
- ter seu `statement` alterado de forma semanticamente significativa;
- ter sua `normative_keyword` enfraquecida;
- ter seu `target` ampliado ou reduzido de forma que altere quais sujeitos são avaliados.

Alterações permitidas sem novo `rid`: correção tipográfica, esclarecimento de `rationale`, adição de `procedure_ref` mais preciso que não altera o critério.

**Justificativa formal:** Compliance Evidence e Certification L3 (Validation & Certification §5) referenciam NRs individualmente. Domain Model §13 estabelece que Evidence é imutável e que Evidence editada "deixa de ser Evidence". Se um `rid` pudesse mudar de significado sob o mesmo identificador, toda Evidence histórica que o referencia tornar-se-ia ininterpretável — uma corrupção retroativa do registro institucional, violando simultaneamente Domain Model §15 (rastreabilidade) e Constitution (Auditabilidade).

### 5.3 Tombstones de Requirement Identifier

Quando um NR é removido em uma major version, seu `rid` **MUST** ser registrado em `retired_rids` e **MUST NOT** ser reatribuído a um requisito diferente em nenhuma versão futura.

`[ESCOLHA DE DESIGN]` Reserva permanente de `rid`. Alternativa rejeitada: permitir reuso de identificadores após remoção, economizando espaço de nomes. Rejeitada por analogia direta e deliberada com a regra de reserva permanente de nomes de Component já estabelecida em Identity & Namespace §3.2 (tombstone, nunca reciclagem), motivada lá pela prevenção de *dependency confusion*. O risco aqui é isomórfico e mais grave: um `rid` reciclado faria Evidence histórica apontar, silenciosamente, para uma norma que nunca foi avaliada.

### 5.4 Supersessão intra-lineage

Quando a semântica de um requisito precisa mudar, o Standard **MUST** introduzir um novo `rid` com `supersedes` apontando ao anterior, e **MUST** aposentar o anterior conforme §5.3. Isso torna a evolução normativa um grafo explícito e navegável — a mesma disciplina que RFC-DM-001 §3.1 aplicou a `Decision Record` e que Identity & Namespace §7 aplicou a versões de Component.

O grafo de `supersedes` entre RIDs **MUST** ser acíclico. **Reutiliza Kernel §7** — nenhuma implementação nova.

---

## 6. Herança e Composição

Duas relações estruturais com semânticas **deliberadamente distintas**. Ambas expressas por `VersionedIdentifier` (nunca Coordinate sem versão — ST3), garantindo que a composição normativa seja reprodutível ao longo do tempo.

### 6.1 `extends` — especialização com substituibilidade

O Standard derivado herda todos os NRs do base e **MAY**:
- adicionar novos NRs;
- **elevar** a força normativa de um NR herdado (`MAY` → `SHOULD` → `MUST`).

E **MUST NOT**:
- remover NR herdado;
- enfraquecer força normativa;
- restringir `target` de NR herdado de modo a excluir sujeitos antes cobertos.

**Propriedade garantida (substituibilidade normativa):** conformidade a `S_derivado@vX` no nível `L` **implica** conformidade a `S_base@vY` no nível correspondente. Esta implicação é a razão de existir de `extends`, e é consumida por Policy quando avalia se um Binding já está satisfeito por um Binding mais forte.

### 6.2 `includes` — agregação sem substituibilidade

Incorpora por referência o conjunto de NRs de outro Standard, preservando os `rid` originais **qualificados pela Identity do Standard de origem**. O Standard agregador **MUST NOT** modificar, sobrescrever ou reinterpretar NRs incluídos.

Colisão de `rid` entre Standards incluídos é **impossível por construção**, pois a qualificação usa a Identity do Standard de origem, garantidamente única por Identity & Namespace §3.2.

`[ESCOLHA DE DESIGN]` Distinguir `extends` de `includes` em vez de um mecanismo único de "reuso". Alternativa rejeitada: uma única relação `imports` cobrindo ambos os casos. Rejeitada porque `extends` cria uma relação de implicação lógica entre conformidades (substituibilidade), enquanto `includes` cria apenas agregação sem implicação. Colapsá-las tornaria indecidível, para Policy e Compliance, se conformidade a A implica conformidade a B — uma pergunta que ambos precisam responder deterministicamente. Precedente: distinção entre herança nominal (subtipagem, com substituibilidade) e `allOf` (composição estrutural, sem subtipagem) em JSON Schema e OpenAPI.

### 6.3 Aciclicidade

O grafo dirigido formado pela união de `extends`, `includes` e `replaces` **MUST** ser acíclico.

**Reutiliza Kernel §7 (Cycle Detection)** — esta é a **quarta aplicação institucional** do mesmo mecanismo, após: `dependencies` de Component (Kernel §7 original), `derives_from` de Knowledge (RFC-DM-001 §3.3), grafo de fases de Workflow (Workflow §7) e grafo de Composition (Composition §7). Nenhuma reimplementação, nenhuma variante.

---

## 7. Evolução, Compatibilidade, Deprecação e Substituição

### 7.1 Semântica SemVer especializada para Standards

Kernel §2.11 já mandata SemVer 2.0.0 estrito para todo Component. Standards exigem uma **interpretação especializada** de o que constitui breaking change, porque o "consumidor" de um Standard não é um chamador de API, mas um **conjunto de Components previamente conformes**.

| Mudança | Impacto sobre conformidade preexistente | Versão exigida |
|---|---|---|
| Adicionar NR com `MUST` / `MUST_NOT` a um Conformance Level existente | Component antes conforme **pode** tornar-se não conforme | **MAJOR** |
| Elevar força normativa de NR existente (`SHOULD` → `MUST`) | Idem | **MAJOR** |
| Remover NR de um Conformance Level | Conformidade preexistente permanece válida, mas claims perdem interpretação | **MAJOR** |
| Ampliar `ComplianceTarget` de um NR (mais sujeitos cobertos) | Componentes antes fora de escopo passam a ser avaliados | **MAJOR** |
| Adicionar NR com `SHOULD` / `SHOULD_NOT` / `MAY` | Conformidade Strict preexistente pode degradar a Partial (§8) | **MINOR** |
| Adicionar novo Conformance Level | Nenhum impacto sobre níveis existentes | **MINOR** |
| Adicionar NR a um nível novo apenas | Nenhum impacto | **MINOR** |
| Tornar `EvidenceRequirement` mais rigoroso (freshness menor, retention maior) | Evidence preexistente pode expirar | **MAJOR** |
| Tornar `EvidenceRequirement` menos rigoroso | Nenhum impacto negativo | **MINOR** |
| Correção tipográfica, `rationale`, `description` | Nenhum | **PATCH** |

`[ESCOLHA DE DESIGN]` Classificar "adicionar `SHOULD`" como MINOR e não MAJOR. Alternativa rejeitada: tratar qualquer adição de requisito como MAJOR, por máxima cautela. Rejeitada porque `SHOULD` não invalida conformidade — degrada Strict para Partial (§8.2), que é um resultado **declarável e auditável**, não uma falha. Tratar toda adição como MAJOR tornaria a evolução normativa proibitivamente cara, empurrando autores a nunca adicionarem recomendações — resultado pior para a qualidade institucional. A degradação Strict→Partial é visível no Conformance Claim, portanto não é silenciosa.

### 7.2 Backward Compatibility (retrocompatibilidade)

**Definição normativa:** uma versão `S@vN` é *backward compatible* com `S@vM` (`M < N`, mesma major) se e somente se **todo Component conformante a `S@vM` no nível `L` permanece conformante a `S@vN` no nível `L`**, sem qualquer alteração no Component.

Garantia estrutural: a tabela §7.1 é construída de modo que **toda mudança MINOR ou PATCH seja backward compatible por construção**, e apenas mudanças MAJOR possam quebrá-la. Um Standard cuja mudança MINOR quebre conformidade preexistente é um **defeito de versionamento**, detectável pelo algoritmo `ClassifyStandardChange` (§9 do Modelo Operacional) e **MUST** bloquear a saída de `Draft`.

### 7.3 Forward Compatibility (compatibilidade prospectiva)

**Definição normativa:** um avaliador construído para `S@vN` é *forward compatible* se consegue interpretar corretamente um Conformance Claim emitido contra `S@vM` (`M < N`).

Três garantias estruturais tornam isso possível, todas já estabelecidas:
1. **Estabilidade de `rid`** (§5.2) — um `rid` significa a mesma coisa em toda a major version.
2. **Tombstones** (§5.3) — um `rid` desconhecido pelo avaliador nunca é um `rid` reciclado com outro significado; é inequivocamente um requisito aposentado ou de versão posterior.
3. **`introduced_in`** — permite ao avaliador determinar se a ausência de um `rid` em um Claim antigo é omissão indevida ou consequência legítima de o requisito não existir àquela época.

**Regra de tolerância (ST12):** um avaliador que encontre um `rid` desconhecido em um Claim **MUST** registrar `INDETERMINATE` para aquele requisito e **MUST NOT** ignorá-lo silenciosamente nem tratá-lo como conforme.

`[ESCOLHA DE DESIGN]` `INDETERMINATE` em vez de ignorar `rid` desconhecido. Alternativa rejeitada: ignorar requisitos não reconhecidos (modelo "must-ignore" de extensibilidade, comum em protocolos web). Rejeitada porque o must-ignore é apropriado quando o desconhecido é *opcional por definição*; aqui, um `rid` desconhecido pode ser um `MUST` de versão posterior, e ignorá-lo produziria falsa afirmação de conformidade — violação direta de Constitution (Confiança verificável: "confiança não é concedida por reputação, é concedida por conformidade demonstrada").

### 7.4 Deprecação e Substituição

Ambas reutilizam integralmente mecanismos existentes; **nenhum estado novo é introduzido**.

| Ato | Mecanismo | Documento base |
|---|---|---|
| Deprecação | Transição de Lifecycle para `Deprecated` | Kernel §3; Governance §16 |
| Visibilidade da deprecação | Registry mantém descobrível com aviso | Registry & Discovery §7.3 |
| Substituição | Campo `replaces: VersionedIdentifier` no Standard sucessor | Análogo a `redirects_to` de Identity §6.4 |
| Redirecionamento de resolução | Resolução expõe a cadeia completa, nunca a oculta | Identity §6.6; Registry §6.1 |
| Lineage | Sequência imutável de Manifests | Identity & Namespace §7; RFC-DM-001 §3.6 (`Component 1:1..* Manifest`) |

**Regra de continuidade normativa (ST10):** um Standard que declara `replaces` **SHOULD** preservar os `rid` do Standard substituído para todo requisito cuja semântica permaneça inalterada. Justificativa: preservar `rid` através de substituição permite que Evidence histórica continue interpretável mesmo após troca de Standard, estendendo a garantia de §5.2 para além da fronteira de identidade — sem o que uma substituição funcionaria como reset do histórico de conformidade.

**Regra de referência a Standard não-`Active`:**
- Referência a `Deprecated` — **MUST** resolver com aviso; avaliação prossegue. O aviso é sinal de drift para Compliance (downstream).
- Referência a `Archived` ou `Removed` — resolução retorna Tombstone (Registry §6.1); avaliação **MUST** falhar explicitamente com causa registrada. **MUST NOT** produzir veredito de conformidade.

`[ESCOLHA DE DESIGN]` Falha explícita em vez de conformidade trivial quando a norma desapareceu. Alternativa rejeitada: tratar ausência de norma como "nada a verificar, logo conforme". Rejeitada porque produziria o resultado perverso de um Component tornar-se automaticamente conforme ao ter sua norma arquivada — invertendo o incentivo institucional e violando Governance §13 (que exige resposta ativa a mudanças normativas, não absolvição automática).

### 7.5 Lineage normativa

A lineage de um Standard é a projeção `Component "1" —— "1..*" Manifest` corrigida por RFC-DM-001 §3.6, exposta pelo serviço `lineage()` já contratado em Identity & Namespace §9 e implementado em Registry & Discovery §5. **Nenhum serviço novo é introduzido.**

Sobre essa lineage, este documento define uma projeção derivada adicional, computada sob demanda e nunca armazenada redundantemente:

```
requirement_lineage(qualified_rid) → [ (SemVer, NormativeRequirement) ]
```

Retorna a evolução de um requisito específico ao longo das versões do Standard, incluindo elos de `supersedes`. É o que permite responder, em auditoria: *"o que exatamente este requisito exigia no momento em que esta Evidence foi produzida?"* — pergunta que Domain Model §15 torna obrigatória e que, sem esta projeção, exigiria reconstrução manual.

---

## 8. Conformidade: Estrita, Parcial e Não Conformidade

### 8.1 Conformance Claim

Um **Conformance Claim** é um `Artifact` genérico (Domain Model §2, entidade #7) — mesmo padrão de `Assembly` (Composition §4), `Execution Plan` (Execution §4) e `Effective Policy Set` (Documento 2). **Não é entidade nova.**

```
ConformanceClaim (Artifact) {
  subject          : VersionedIdentifier        (o Component avaliado)
  standard         : VersionedIdentifier
  level            : LevelName
  mode             : STRICT | PARTIAL
  satisfied        : [QualifiedRequirementIdentifier]
  unsatisfied_should: [QualifiedRequirementIdentifier]     (vazio se STRICT)
  not_applicable   : [QualifiedRequirementIdentifier]
  indeterminate    : [QualifiedRequirementIdentifier]      (MUST ser vazio para claim válido — §8.3)
  evidence_refs    : [EvidenceId]
  evaluated_at     : Timestamp
  context_snapshot : ContextSnapshotId          [RFC-DM-001 §3.2 — obrigatório]
}
```

### 8.2 Definições normativas dos três resultados

| Resultado | Condição necessária e suficiente |
|---|---|
| **Strict Conformance** | Todo NR de `requires(level)` com keyword `MUST` ou `MUST_NOT` está satisfeito **E** todo NR com `SHOULD`/`SHOULD_NOT` está satisfeito **E** `indeterminate` é vazio |
| **Partial Conformance** | Todo NR com `MUST`/`MUST_NOT` está satisfeito **E** ao menos um `SHOULD`/`SHOULD_NOT` não está satisfeito **E** `indeterminate` é vazio |
| **Non-Conformance** | Ao menos um NR com `MUST` ou `MUST_NOT` não está satisfeito |

**Regra fundamental (ST7):** Partial Conformance **MUST NOT** ser declarada quando qualquer `MUST` falha. Falha de `MUST` é Non-Conformance, sem gradação.

`[ESCOLHA DE DESIGN]` Partial Conformance restrita a `SHOULD` não satisfeitos, jamais a `MUST` parcialmente satisfeitos. Alternativa rejeitada: permitir "conformidade parcial" como percentual de requisitos satisfeitos, incluindo `MUST` (modelo de score). Rejeitada por dois motivos convergentes: (a) violaria a regra já estabelecida em Validation & Certification §5 de que "avanço de nível MUST satisfazer mínimo por dimensão, nunca média ponderada" — permitir 90% dos `MUST` seria exatamente a compensação por média que aquele documento proíbe; (b) destruiria o significado de `MUST` em RFC 2119, cuja definição é categórica e não gradual. Precedente: conformidade W3C e ISO são binárias quanto a requisitos obrigatórios; graduação existe apenas entre níveis/perfis, nunca dentro de um requisito obrigatório.

**Regra de justificação (ST8):** um Claim `PARTIAL` **MUST** enumerar explicitamente cada `SHOULD` não satisfeito em `unsatisfied_should`. Um Claim que declare `PARTIAL` sem enumerar é inválido. Justificativa: sem enumeração, "parcial" seria opaco e não auditável, contrariando Constitution (Transparência) e impedindo Compliance de detectar drift em recomendações.

### 8.3 Indeterminação

`indeterminate` **MUST** estar vazio para que um Conformance Claim seja válido. Um requisito indeterminado (Evidence ausente para `DYNAMIC`/`ATTESTED`, ou `rid` desconhecido por §7.3) **MUST NOT** ser silenciosamente classificado como satisfeito nem como violado.

Consequência operacional: um avaliador que encontre indeterminação **MUST NOT** emitir Conformance Claim; **MUST** emitir um resultado de avaliação incompleta, tratado pela camada consumidora (Compliance, downstream) conforme suas próprias regras. Isso preserva a integridade do Claim como afirmação institucional: um Claim existente é sempre uma afirmação completa.

### 8.4 Integração com Certification L3 — fechamento do forward-reference

Validation & Certification §5 define L3 como "Conformance a todo Standard/Policy vinculado", exigindo "Conformance Evidence por Standard". Este documento estabelece a regra exata de suficiência, **sem alterar aquele documento**:

> **L3 MUST exigir Strict Conformance** a todo Standard vinculado, no Conformance Level exigido pelo vínculo. Partial Conformance **MUST NOT** satisfazer L3.

`[ESCOLHA DE DESIGN]` Exigir Strict para L3. Alternativa rejeitada: aceitar Partial Conformance para L3 quando todos os `MUST` estão satisfeitos. Rejeitada porque L3 é explicitamente nomeado "Standards Certified" e antecede L4 ("Institutionally Certified") na escala de Validation & Certification §5; aceitar recomendações sistematicamente ignoradas em um nível chamado "Standards Certified" esvaziaria a distinção entre `MUST` e `SHOULD` na prática certificatória. Partial Conformance permanece plenamente útil: é resultado válido e declarável para contextos de `enforcement_mode = ADVISORY` (Documento 2 §4.3) e para níveis L1/L2.

---

## 9. Standard Packages

Um **Standard Package** é um `Standard` com `standard_kind = PACKAGE`, sujeito a restrições estruturais adicionais:

- `requirements` **MUST** ser vazio — um Package não define norma própria.
- `includes` **MUST** conter ao menos uma referência.
- `extends` **MUST** ser vazio — Packages agregam, não especializam.
- `conformance_levels` **MAY** definir níveis que agrupam requisitos dos Standards incluídos, permitindo baselines curados (ex.: um nível `BASELINE_2027` reunindo requisitos de segurança, dados e API).

**Propósito institucional:** fornecer uma **Coordinate estável e versionada** para um conjunto curado de Standards, de modo que Policies possam vincular-se a um único identificador em vez de enumerar dezenas de Standards individuais — e de modo que a evolução coordenada desse conjunto seja versionável como unidade.

`[ESCOLHA DE DESIGN]` Package como perfil restrito de Standard, não como novo `component_type`. Alternativas rejeitadas: (a) criar `component_type = StandardPackage` — rejeitada por violar a Restrição Arquitetural 1 e por exigir que Registry, Certification, Policy e Compliance passassem a conhecer um tipo adicional, quando nenhum deles precisa distinguir; (b) modelar Package como um Profile transversal — rejeitada porque Profile não tem Coordinate própria nem lineage própria, e é precisamente a estabilidade de Coordinate e a versionabilidade independente que justificam a existência do Package. Precedente: OCI image spec e distribuições Linux versionam *conjuntos curados* sob identidade própria, distinta da identidade dos componentes que agregam.

**Regra de propagação de compatibilidade (ST13):** a versão de um Package **MUST** ser MAJOR sempre que qualquer Standard incluído for atualizado para uma versão MAJOR. Justificativa: um Package cuja MINOR incorpore MAJOR de um incluído violaria a garantia de backward compatibility de §7.2 para seus próprios consumidores, transformando o Package em vetor de quebra silenciosa.

---

## 10. Modelo Operacional

**Serviço:** `Standard Resolution Service` — substrato institucional, mesma classe arquitetural do `Composition Resolver` (Composition §5) e do `Policy Evaluation Service` (Documento 2 §5). **Não é um Component**, não possui Lifecycle, não possui autoridade decisória, e não escreve em lugar algum.

### 10.1 Operações

```
resolve_effective_requirements(standard: VersionedIdentifier, level: LevelName)
    → NormativeRequirement[] | StandardError
  PRE:  standard resolve via Registry (Registry §6.1) a lifecycle_state ∈ {Active, Deprecated}
        E level ∈ standard.conformance_levels
  POST: retorna o fecho transitivo de NRs sobre extends ∪ includes,
        deduplicado por QualifiedRequirementIdentifier,
        com força normativa resolvida pela regra de não-enfraquecimento (§6.1),
        restrito a requires(level) expandido por inherits_from
  INV:  determinismo total — mesma entrada produz sempre a mesma saída,
        requisito herdado de Validation & Certification §6 (Reproducibility)

validate_standard_definition(manifest) → ValidationResult
  PRE:  manifest.component_type = Standard
  POST: ver §10.3 (lista completa de invariantes verificados)

classify_standard_change(prev: Manifest, next: Manifest) → MAJOR | MINOR | PATCH | INVALID
  PRE:  prev e next pertencem à mesma lineage (mesma Coordinate)
  POST: classificação conforme tabela §7.1; INVALID quando a mudança
        viola estabilidade de rid (§5.2) ou reciclagem de tombstone (§5.3)

requirement_lineage(qualified_rid) → [(SemVer, NormativeRequirement)]
  POST: projeção derivada sobre a lineage do Registry; nunca armazenada
```

### 10.2 Invariante institucional de admissão

`validate_standard_definition` **MUST** ser satisfeito antes de um Standard sair de `Draft`. Isto **reutiliza integralmente** o gate de Verification já definido em Validation & Certification §4 e o critério de Conformance para `component_type = Standard` já anunciado em Validation & Certification §7 ("Revisão de completude e ausência de conflito de precedência"). Este documento **fornece o conteúdo verificável daquele critério, sem redefinir o gate**.

### 10.3 Invariantes verificados na validação

| # | Invariante | Origem |
|---|---|---|
| I1 | Grafo `extends ∪ includes ∪ replaces` acíclico | Kernel §7 (4ª aplicação) |
| I2 | Nenhum `ComplianceTarget` referencia Namespace/Organization/Role/Context | ST1, §4.5 |
| I3 | Todo Conformance Level é monotônico sobre `inherits_from` | ST5, §4.4 |
| I4 | Todo `rid` é único dentro do Standard e não colide com `retired_rids` | §5.1, §5.3 |
| I5 | Todo NR declara `EvaluationMethod` com `EvidenceRequirement` completo | ST4, §4.6 |
| I6 | `deterministic = false` ⟹ `reproducible = false` | §4.6 |
| I7 | `precedence_level = GLOBAL` ⟹ toda `retention = PERMANENT` | ST9, §4.6 |
| I8 | `extends` não enfraquece nem remove NR herdado | §6.1 |
| I9 | `includes` não modifica NR incorporado | §6.2 |
| I10 | Grafo de `supersedes` entre RIDs acíclico | §5.4 (Kernel §7) |
| I11 | Se `standard_kind = PACKAGE`: `requirements` vazio, `extends` vazio, `includes` não vazio | §9 |
| I12 | Todo `RequirementIdentifier` referenciado em `conformance_levels` existe em `requirements` ou no fecho de `includes`/`extends` | §4.4 |
| I13 | Classificação de versão consistente com `classify_standard_change` | ST11, §7.1 |

---

## 11. Diagramas

### 11.1 UML simplificado — estrutura interna

```
┌────────────────────────────────────┐
│ Standard                            │  «Structural Component» — Domain Model §3
│  precedence_level                   │
│  standard_kind: NORMATIVE|PACKAGE   │
│  retired_rids[]                     │
└──┬──────────┬──────────┬───────────┘
   │0..*      │0..*      │0..1
   │extends   │includes  │replaces
   ▼          ▼          ▼
 (VersionedIdentifier — grafo acíclico, Kernel §7)
   │
   │1..*                              │0..*
   ▼                                   ▼
┌──────────────────────────┐   ┌────────────────────────┐
│ NormativeRequirement      │   │ ConformanceLevel        │
│  «Value Object»           │   │  «Value Object»         │
│  rid ─────────────────────┼──►│  requires[rid]          │
│  normative_keyword        │   │  inherits_from ─────────┼─┐
│  statement / rationale    │   └────────────────────────┘ │
│  supersedes ──► rid       │            ▲                  │ monotônico (§4.4)
│  introduced_in            │            └──────────────────┘
│                            │
│  target ──────────────────┼──► ComplianceTarget «VO»
│                            │      component_types[], capability_filter,
│                            │      applies_to  (livre de Context — ST1)
│                            │
│  constraint ──────────────┼──► Constraint  [Kernel §2.10 — reutilizado]
│                            │
│  evaluation ──────────────┼──► EvaluationMethod «VO»
└──────────────────────────┘         kind: STATIC|DYNAMIC|ATTESTED
                                       deterministic
                                       procedure_ref ──► CapabilitySignature [Kernel §2.9]
                                       evidence ──► EvidenceRequirement «VO»
                                                      evidence_kind, producer_role_class,
                                                      reproducible, freshness_window,
                                                      retention, minimum_artifacts
```

### 11.2 Sequência — resolução de requisitos efetivos

```
Consumer            StandardResolver          Registry
   │                       │                      │
   ├─resolve_effective_────►│                      │
   │  requirements(s@v,L)  ├──resolve(s@v)────────►│      [Registry §6.1]
   │                       │◄─ResolvedIdentity─────┤
   │                       │                      │
   │              alt lifecycle_state ∉ {Active, Deprecated}
   │◄─StandardError(NOT_APPLICABLE)                │
   │                       │                      │
   │              loop fecho transitivo (extends ∪ includes)
   │                       ├──resolve(base@v)─────►│
   │                       │◄──────────────────────┤
   │                       ├─Kernel§7.CycleDetection
   │                       │  (4ª aplicação — sem reimplementação)
   │                       │
   │                       ├─merge NRs por QualifiedRID
   │                       ├─resolver força normativa (§6.1: nunca enfraquecer)
   │                       ├─expandir level via inherits_from (§4.4, monotônico)
   │                       ├─validar I12 (todo rid de requires existe)
   │◄─NormativeRequirement[]│   (determinístico — mesma entrada, mesma saída)
```

### 11.3 Sequência — emissão de Conformance Claim

```
Evaluator          StandardResolver      EvidenceStore        Claim (Artifact)
    │                     │                    │                     │
    ├─resolve_effective──►│                    │                     │
    │◄──NR[]──────────────┤                    │                     │
    │                                          │                     │
    │  loop para cada NR                       │                     │
    ├─ target_matches(nr.target, subject)? ────┼─ não ──► not_applicable[] += rid
    ├─ collect_evidence(nr.evaluation) ───────►│                     │
    │◄─ Evidence | ausente ────────────────────┤                     │
    │                                                                 │
    │  alt Evidence ausente E kind ∈ {DYNAMIC, ATTESTED}              │
    ├──► indeterminate[] += rid  ──► MUST NOT emitir Claim (§8.3)     │
    │                                                                 │
    │  alt keyword ∈ {MUST, MUST_NOT} E não satisfeito                │
    ├──► resultado = NON_CONFORMANCE (sem gradação — ST7)             │
    │                                                                 │
    │  alt todos MUST ok E algum SHOULD não satisfeito                │
    ├──► mode = PARTIAL, unsatisfied_should[] enumerado (ST8) ───────►│
    │                                                                 │
    │  alt todos MUST e SHOULD ok                                     │
    ├──► mode = STRICT ──────────────────────────────────────────────►│
    │                                                                 │
    │  context_snapshot obrigatório [RFC-DM-001 §3.2] ───────────────►│
```

### 11.4 Estados

Um Standard **não possui máquina de estados própria**. Seu ciclo de vida é exatamente o Kernel Lifecycle, projetado no Registry conforme Registry & Discovery §7.3:

```
Kernel Lifecycle              Registry projection            Efeito normativo
──────────────────────────────────────────────────────────────────────────────────
Draft / Review / Approved  →  não indexado                →  não vinculável por Policy
Active                     →  indexado, descobrível        →  plenamente vinculável
Deprecated                 →  indexado com aviso           →  vinculável; sinal de drift
Archived                   →  Tombstone                    →  avaliação MUST falhar (§7.4)
Removed                    →  Tombstone permanente         →  avaliação MUST falhar (§7.4)
```

Reproduzir este diagrama como máquina própria seria duplicação do Kernel Lifecycle — proibido pela Restrição Arquitetural 3.

---

## 12. Algoritmos

### 12.1 Resolução de requisitos efetivos

```
ALGORITMO ResolveEffectiveRequirements(standard_ref, level):
  ENTRADA: standard_ref : VersionedIdentifier, level : LevelName
  SAÍDA:   NormativeRequirement[] | StandardError
  INVARIANTE: determinístico e total sobre entradas válidas

  1  entry ← Registry.resolve(standard_ref)                      # Registry §6.1
  2  SE entry.lifecycle_state ∉ {Active, Deprecated}:
  3     RETORNA StandardError(STANDARD_NOT_BINDABLE, entry.lifecycle_state)
  4
  5  graph ← BuildReferenceGraph(standard_ref, arestas = {extends, includes})
  6  SE Kernel§7.CycleDetection(graph) detecta ciclo:
  7     RETORNA StandardError(CYCLIC_STANDARD_GRAPH)
  8
  9  # ordenação determinística: bases resolvidas antes de derivados
 10  ordem ← TopologicalOrder(graph) invertida
 11  nrs ← OrderedMap()          # ordenação por QualifiedRID garante saída estável
 12
 13  PARA CADA node EM ordem:
 14     PARA CADA nr EM node.requirements:
 15        qrid ← Qualify(nr.rid, node.identity)
 16        SE qrid ∈ nrs:
 17           SE EdgeKind(node) = INCLUDES:
 18              RETORNA StandardError(ILLEGAL_OVERRIDE_IN_INCLUDES, qrid)
 19           SE Strength(nr.normative_keyword) < Strength(nrs[qrid].normative_keyword):
 20              RETORNA StandardError(NORMATIVE_WEAKENING, qrid)
 21           SE TargetNarrows(nr.target, nrs[qrid].target):
 22              RETORNA StandardError(ILLEGAL_TARGET_NARROWING, qrid)
 23        nrs[qrid] ← nr
 24
 25  level_rids ← ExpandLevel(level, standard_ref)     # aplica inherits_from transitivamente
 26  SE ¬Monotonic(level_rids):
 27     RETORNA StandardError(NON_MONOTONIC_LEVEL, level)
 28
 29  PARA CADA rid EM level_rids:
 30     SE rid ∉ nrs:
 31        RETORNA StandardError(DANGLING_REQUIREMENT_REFERENCE, rid)     # I12
 32
 33  RETORNA [ nrs[rid] PARA rid EM SortedByQRID(level_rids) ]

FUNÇÃO Strength(keyword):
  MUST      → 4
  MUST_NOT  → 4
  SHOULD    → 2
  SHOULD_NOT→ 2
  MAY       → 1

FUNÇÃO ExpandLevel(level, std):
  acc ← ∅ ; cur ← level
  ENQUANTO cur ≠ null:
     acc ← acc ∪ requires(cur)
     cur ← cur.inherits_from
  RETORNA acc
```

**Terminação:** garantida — o grafo é acíclico (linhas 6-7) e a cadeia `inherits_from` é finita e acíclica por I3.
**Determinismo:** garantido — `TopologicalOrder` sobre grafo acíclico com desempate lexicográfico por Coordinate, e `SortedByQRID` na saída.

### 12.2 Classificação de mudança de versão

```
ALGORITMO ClassifyStandardChange(prev, next):
  ENTRADA: prev, next : Manifest da mesma lineage
  SAÍDA:   MAJOR | MINOR | PATCH | INVALID

  1  # verificação de integridade antes de classificar
  2  PARA CADA rid EM next.retired_rids:
  3     SE rid ∈ RIDs(next.requirements):
  4        RETORNA INVALID(TOMBSTONE_RECYCLED, rid)              # §5.3
  5
  6  SE MajorOf(prev.version) = MajorOf(next.version):
  7     PARA CADA rid EM RIDs(prev.requirements):
  8        SE rid ∉ RIDs(next.requirements) ∧ rid ∉ next.retired_rids:
  9           RETORNA INVALID(RID_SILENTLY_DROPPED, rid)          # §5.2
 10        SE SemanticallyChanged(prev[rid].statement, next[rid].statement):
 11           RETORNA INVALID(RID_SEMANTIC_MUTATION, rid)         # §5.2
 12
 13  # classificação conforme tabela §7.1
 14  PARA CADA rid EM RIDs(next.requirements):
 15     SE rid ∉ RIDs(prev.requirements):
 16        SE Strength(next[rid].keyword) = 4:      RETORNA MAJOR   # novo MUST
 17     SENÃO:
 18        SE Strength(next[rid].keyword) > Strength(prev[rid].keyword):  RETORNA MAJOR
 19        SE TargetWidens(next[rid].target, prev[rid].target):           RETORNA MAJOR
 20        SE EvidenceStricter(next[rid].evaluation.evidence,
 21                            prev[rid].evaluation.evidence):            RETORNA MAJOR
 22
 23  PARA CADA rid EM prev.retired_rids_delta(next):    RETORNA MAJOR     # remoção de NR
 24
 25  SE ∃ rid novo com Strength ∈ {1,2}:                RETORNA MINOR
 26  SE ∃ ConformanceLevel novo:                        RETORNA MINOR
 27  SE EvidenceLooser(next, prev):                     RETORNA MINOR
 28
 29  RETORNA PATCH
```

**Uso normativo:** o resultado deste algoritmo **MUST** ser consistente com a versão declarada no Manifest (I13). Divergência bloqueia a saída de `Draft`. Isto torna a garantia de backward compatibility de §7.2 **verificada, não prometida**.

### 12.3 Validação de definição

```
ALGORITMO ValidateStandardDefinition(manifest):
  1  Kernel§7.CycleDetection(extends ∪ includes ∪ replaces)      → I1
  2  Kernel§7.CycleDetection(supersedes entre RIDs)               → I10
  3
  4  PARA CADA nr EM manifest.requirements:
  5     ASSERT nr.target NÃO referencia Namespace|Organization|Role|Context   → I2, ST1
  6     ASSERT nr.evaluation.evidence está completamente declarado             → I5
  7     ASSERT ¬(nr.evaluation.deterministic = false ∧ evidence.reproducible)  → I6
  8     SE manifest.precedence_level = GLOBAL:
  9        ASSERT nr.evaluation.evidence.retention = PERMANENT                 → I7
 10     ASSERT Unique(nr.rid) ∧ nr.rid ∉ manifest.retired_rids                 → I4
 11
 12  PARA CADA lvl EM manifest.conformance_levels:
 13     ASSERT requires(lvl) ⊇ requires(lvl.inherits_from)                     → I3
 14     PARA CADA rid EM requires(lvl):
 15        ASSERT rid ∈ RIDs(manifest) ∪ RIDs(fecho de includes/extends)       → I12
 16
 17  SE manifest.standard_kind = PACKAGE:
 18     ASSERT manifest.requirements = ∅
 19     ASSERT manifest.extends = ∅
 20     ASSERT manifest.includes ≠ ∅                                            → I11
 21
 22  PARA CADA base EM manifest.extends:
 23     ASSERT ¬Weakens(manifest, base) ∧ ¬Removes(manifest, base)             → I8
 24  PARA CADA inc EM manifest.includes:
 25     ASSERT ¬Modifies(manifest, inc)                                         → I9
 26
 27  SE ∃ prev na lineage:
 28     ASSERT ClassifyStandardChange(prev, manifest) consistente com version   → I13
 29
 30  RETORNA OK | ValidationError(invariante violado, detalhe)
```

---

## 13. Integrações

| Documento base | Contrato de integração | Direção |
|---|---|---|
| **Constitution** | `precedence_level` reutiliza literalmente a hierarquia de 4 níveis; NRs estruturados realizam o princípio "documentação executável"; Confiança verificável realizada por `INDETERMINATE` obrigatório (§8.3) e por proibição de must-ignore (§7.3) | Consumo de princípio |
| **Kernel** | Standard é Component pleno — §2.1 a §2.15 aplicam-se sem exceção; `Constraint` (§2.10) e `CapabilitySignature` (§2.9) reutilizados; Cycle Detection (§7) reaplicado 4×; Extension Model (§9) é o que autoriza `requirements[]` como conteúdo interno do Contract, exatamente como autorizou `Phase`/`Step` em Workflow §4 | Reuso puro |
| **Governance** | Admissão, aprovação, deprecação e substituição seguem §7/§8/§16 sem alteração — aprovação por Governance Area Steward; conflito entre Standards de mesma precedência resolve-se por §17, jamais por lógica interna deste documento; auditoria (§12) consome Conformance Claims como Evidence | Delegação total de autoridade |
| **Domain Model v1.1.0** | Zero entidades, relações e estados novos. Standard = Structural Component (§3); NR/Target/Level/EvaluationMethod/EvidenceRequirement = Value Objects; Conformance Claim = `Artifact` genérico (§2 #7); Evidence exigida é `Evidence` existente (§2 #8, §13) sem subtipo novo | Conformidade estrita |
| **RFC-DM-001** | `context_snapshot` obrigatório em todo Conformance Claim (§3.2, achado C2); vocabulário corrigido respeitado — `Knowledge Asset` jamais confundido com `Knowledge`; cardinalidade `Component 1:1..* Manifest` (§3.6) é a base formal da lineage (§7.5) | Consumo de correções |
| **Identity & Namespace** | Convenção `<ns>/standard.<área>.<nome>` (§5); `QualifiedRequirementIdentifier` usa a forma canônica URN com fragmento `#` (§4.3), mesmo padrão já usado para Capability (§2.2); lineage e `supersedes` (§7); tombstone de `rid` (§5.3) é isomórfico à reserva permanente de nome (§3.2); referências cross-namespace totalmente qualificadas (§10) | Reuso integral do esquema |
| **Registry & Discovery** | Único mecanismo de registro e descoberta (ST2). `resolve()` (§6.1), `list(component_type=Standard)` (§5), `lineage()` (§5) reutilizados sem extensão. Tombstone (§6.1) governa referência a Standard removido. Nenhum índice novo além dos já normatizados em §8 | Consumidor puro |
| **Validation & Certification** | Fecha o forward-reference de L3 (§8.4) sem redefinir o mecanismo de certificação; `EvidenceRequirement.reproducible` reutiliza literalmente o requisito de Reproducibility (§6); a regra "mínimo por dimensão, nunca média" (§5) é o fundamento de ST7 (Partial Conformance nunca cobre `MUST`); Standards são eles próprios certificáveis conforme §7 | Bidirecional, sem alteração |
| **Composition** | `ComplianceTarget.applies_to = COMPOSITION` permite NRs avaliáveis sobre uma `Assembly` resolvida (§5). A dependência declarada em Composition §14 ("critério normativo em Slot além de `min_certification_level`") fica estruturalmente desbloqueada; sua ativação requer Policy (Documento 2), não este documento | Desbloqueio, sem alteração |
| **Workflow** | `applies_to = WORKFLOW` — NRs sobre definição de Workflow são avaliáveis; `GATE_AUTO` (§4) **MAY** consumir Conformance Claims como Evidence de gate. Standard nunca vira Gate | Unidirecional |
| **Execution** | `applies_to = EXECUTION` — NRs avaliáveis contra uma Execution concreta; avaliação usa Context Snapshot (Execution §5), nunca Context vivo, garantindo reprodutibilidade posterior | Unidirecional |
| **Policy (Documento 2)** | Policy referencia Standards por `VersionedIdentifier` + `ConformanceLevel`; Standard **MUST NOT** conhecer Policy — relação estritamente unidirecional | Consumido por |
| **Compliance (downstream)** | Consome `NormativeRequirement[]` e `EvidenceRequirement`; emite Conformance Claims. Não altera este documento | Consumidor futuro |

---

## 14. Casos Extremos

| # | Caso | Tratamento normativo |
|---|---|---|
| E1 | Ciclo em `extends`/`includes`/`replaces` | `StandardError(CYCLIC_STANDARD_GRAPH)`; **MUST NOT** sair de `Draft` (I1) |
| E2 | `extends` que enfraquece força normativa | `StandardError(NORMATIVE_WEAKENING)`; rejeitado na validação (I8) |
| E3 | `includes` que tenta sobrescrever NR | `StandardError(ILLEGAL_OVERRIDE_IN_INCLUDES)` (I9) |
| E4 | Colisão de `rid` entre Standards incluídos | Impossível por construção — qualificação pela Identity de origem, única por Identity §3.2 |
| E5 | `rid` reciclado após aposentadoria | `INVALID(TOMBSTONE_RECYCLED)` em `ClassifyStandardChange` (§5.3, §12.2 linha 4) |
| E6 | `rid` removido silenciosamente dentro da mesma major | `INVALID(RID_SILENTLY_DROPPED)` (§12.2 linha 9) |
| E7 | Mutação semântica de `statement` sob mesmo `rid` na mesma major | `INVALID(RID_SEMANTIC_MUTATION)` (§12.2 linha 11) |
| E8 | Standard referenciado em `Deprecated` | Resolução **MUST** suceder com aviso; avaliação prossegue; aviso é sinal de drift para Compliance (§7.4) |
| E9 | Standard referenciado em `Archived`/`Removed` | Tombstone (Registry §6.1); avaliação **MUST** falhar explicitamente; **MUST NOT** produzir conformidade trivial (§7.4) |
| E10 | Dois Standards de mesmo `precedence_level` com NRs contraditórios | **Deliberadamente fora de escopo** — arbitragem é Governance §17. Este documento garante *detectabilidade* (NRs estruturados e comparáveis por `target` + `constraint`), não resolução automática |
| E11 | Conformance Level referencia `rid` inexistente | `StandardError(DANGLING_REQUIREMENT_REFERENCE)` (I12) |
| E12 | Standard sem nenhum NR e `standard_kind = NORMATIVE` | Estruturalmente válido, normativamente vazio — trivialmente satisfeito por qualquer sujeito. **Não é erro**: permite Standards-placeholder durante composição incremental sob Governance §7 |
| E13 | Package com `requirements` não vazio | Rejeitado (I11, §9) |
| E14 | Package cuja MINOR incorpora MAJOR de Standard incluído | Rejeitado por ST13 — quebraria backward compatibility para consumidores do Package (§9) |
| E15 | NR `DYNAMIC` sem Evidence disponível na avaliação | `INDETERMINATE`; Conformance Claim **MUST NOT** ser emitido (§8.3) |
| E16 | Claim declara `PARTIAL` sem enumerar `unsatisfied_should` | Claim inválido (ST8, §8.2) |
| E17 | Claim declara `PARTIAL` com `MUST` violado | Claim inválido — é Non-Conformance sem gradação (ST7, §8.2) |
| E18 | Avaliador encontra `rid` desconhecido em Claim antigo | `INDETERMINATE`; **MUST NOT** ignorar nem presumir conformidade (ST12, §7.3) |
| E19 | `deterministic = false` com `reproducible = true` | Rejeitado na validação — contradição estrutural (I6) |
| E20 | Standard `GLOBAL` com `retention = BOUNDED` | Rejeitado (I7, ST9) — Evidence de norma não negociável integra o registro permanente |
| E21 | Substituição (`replaces`) que não preserva `rid` de requisitos inalterados | Permitido, porém desaconselhado (ST10, `SHOULD`); consequência é perda de interpretabilidade de Evidence histórica através da fronteira de substituição, sinalizada como drift |
| E22 | Lineage com salto de MAJOR sem migração declarada | Detectado por `ClassifyStandardChange`; Governance §10 (Breaking Change) exige RFC e janela de transição — mecanismo já existente, não redefinido aqui |

---

## 15. Performance

### 15.1 Cache

`resolve_effective_requirements(standard@version, level)` é **integralmente cacheável com validade indefinida**.

**Prova de correção do cache:** o resultado depende exclusivamente de (a) o Manifest de `standard@version` e (b) os Manifests do fecho transitivo de `extends`/`includes`, todos referenciados por `VersionedIdentifier` (ST3). Kernel §8 estabelece que Manifests são imutáveis uma vez `Active`. Logo, o resultado é imutável. Invalidação é necessária **apenas** por mudança de metadado de lifecycle (`Active → Deprecated`), que afeta o aviso mas não o conteúdo dos requisitos.

Esta é exatamente a mesma regra de cache já normatizada em Registry & Discovery §8 para resolução de Versioned Identifier — **nenhuma política nova de cache é introduzida**.

### 15.2 Complexidade

| Operação | Complexidade | Comentário |
|---|---|---|
| `ResolveEffectiveRequirements` | O(V + E + R log R) | V,E = nós e arestas do grafo `extends`/`includes`; R = NRs no fecho. Ordenação para determinismo |
| `ValidateStandardDefinition` | O(V + E + R + L) | L = níveis de conformance |
| `ClassifyStandardChange` | O(R) | Comparação linear entre duas versões |
| `requirement_lineage` | O(N) | N = versões na lineage; consulta ao Registry §5 |

Mesma ordem já aceita para validação de Workflow (Workflow §10) e resolução de Composition (Composition §10).

### 15.3 Particionamento e trade-offs

Particionamento herda integralmente o particionamento por Namespace do Registry (Registry §10). Nenhum mecanismo novo.

**Trade-off explícito assumido:** Standards profundamente encadeados (`extends` de `extends` de `extends`) tornam a primeira resolução custosa. Alternativa rejeitada: materializar o fecho no próprio Manifest no momento da publicação ("flattening"). Rejeitada porque destruiria a rastreabilidade da origem de cada NR — perder-se-ia a informação de *qual* Standard base introduziu cada requisito, que é precisamente o que `QualifiedRequirementIdentifier` existe para preservar e que auditoria (Governance §12) precisa. A imutabilidade por versão torna o cache trivialmente correto, transferindo todo o custo para o primeiro acesso.

**Trade-off de profundidade:** não há limite normativo de profundidade de `extends`. `[DÍVIDA TÉCNICA reconhecida]` — cadeias patologicamente profundas degradam a primeira resolução e a legibilidade humana. Mitigação disponível hoje: Governance §7 (Admission) pode rejeitar por critério de qualidade. Um limite normativo poderá ser introduzido aditivamente por versão futura deste documento sem quebrar Standards existentes.

---

## 16. Eventos

Taxonomia operacional. Mesma classe de `Registry Event` (Registry §11) e de `Composition Event` (Composition §11): telemetria de substrato, **não** Event Entities do Domain Model, **não** exigindo Decision Record.

| Evento | Emitido quando |
|---|---|
| `StandardDefinitionValidated` | `ValidateStandardDefinition` retorna OK |
| `StandardDefinitionRejected(invariant, detail)` | Qualquer invariante I1–I13 violado |
| `EffectiveRequirementsResolved(standard@v, level, count)` | Resolução bem-sucedida |
| `NormativeWeakeningDetected(qrid)` | Violação de §6.1 |
| `CyclicStandardGraphDetected` | Violação de I1 ou I10 |
| `TombstoneRecycleAttempted(rid)` | Violação de §5.3 |
| `RequirementSemanticMutationDetected(rid)` | Violação de §5.2 |
| `VersionClassificationMismatch(declared, computed)` | Violação de I13 |
| `DeprecatedStandardReferenced(standard@v)` | Referência a Standard em `Deprecated` (E8) |
| `ArchivedStandardReferenced(standard@v)` | Referência a Standard em `Archived`/`Removed` (E9) |
| `PartialConformanceClaimed(subject, standard@v, level)` | Claim emitido com `mode = PARTIAL` |
| `IndeterminateRequirementEncountered(qrid)` | §8.3 ou §7.3 |
| `StandardPackagePublished(package@v, includes_count)` | Publicação de Package (§9) |

---

## 17. Regras Normativas (RFC 2119)

| # | Regra | Nível |
|---|---|---|
| **ST1** | `ComplianceTarget` MUST NOT referenciar Namespace, Organization, Role, ambiente ou qualquer predicado sobre Context | MUST NOT |
| **ST2** | Standard MUST NOT ser registrado ou descoberto por serviço distinto do Registry existente | MUST NOT |
| **ST3** | Referência a Standard (em `extends`, `includes`, `replaces`, ou por Policy) MUST usar Versioned Identifier, nunca Coordinate sem versão | MUST |
| **ST4** | Todo Normative Requirement MUST declarar `EvaluationMethod` contendo `EvidenceRequirement` completo | MUST |
| **ST5** | Conformance Levels MUST ser monotônicos sobre `inherits_from` | MUST |
| **ST6** | `RequirementIdentifier` MUST ser semanticamente estável dentro de uma major version | MUST |
| **ST7** | Partial Conformance MUST NOT ser declarada quando qualquer `MUST`/`MUST_NOT` falha | MUST NOT |
| **ST8** | Claim `PARTIAL` MUST enumerar explicitamente cada `SHOULD`/`SHOULD_NOT` não satisfeito | MUST |
| **ST9** | Standard com `precedence_level = GLOBAL` MUST declarar `retention = PERMANENT` em todo `EvidenceRequirement` | MUST |
| **ST10** | Standard que declara `replaces` SHOULD preservar os `rid` de requisitos semanticamente inalterados | SHOULD |
| **ST11** | Versão declarada MUST ser consistente com `ClassifyStandardChange` | MUST |
| **ST12** | Avaliador que encontre `rid` desconhecido MUST registrar `INDETERMINATE`; MUST NOT ignorar nem presumir conformidade | MUST / MUST NOT |
| **ST13** | Versão de Standard Package MUST ser MAJOR quando qualquer Standard incluído for atualizado para MAJOR | MUST |
| **ST14** | `rid` aposentado MUST NOT ser reatribuído a requisito diferente em nenhuma versão futura | MUST NOT |
| **ST15** | Grafo `extends ∪ includes ∪ replaces` MUST ser acíclico, verificado por Kernel §7 | MUST |
| **ST16** | Grafo de `supersedes` entre RIDs MUST ser acíclico | MUST |
| **ST17** | Conformance Claim MUST referenciar Context Snapshot (RFC-DM-001 §3.2) | MUST |
| **ST18** | Conformance Claim com `indeterminate` não vazio MUST NOT ser emitido | MUST NOT |
| **ST19** | Certification L3 MUST exigir Strict Conformance; Partial Conformance MUST NOT satisfazer L3 | MUST / MUST NOT |
| **ST20** | Avaliação contra Standard em `Archived`/`Removed` MUST falhar explicitamente; MUST NOT produzir conformidade trivial | MUST / MUST NOT |
| **ST21** | Standard MUST NOT declarar consequência de não conformidade | MUST NOT |
| **ST22** | `deterministic = false` MUST implicar `reproducible = false` | MUST |
| **ST23** | Standard SHOULD declarar `precedence_level` explicitamente; omissão assume PROJECT (mais restrito) | SHOULD |
| **ST24** | Resolução de requisitos efetivos MAY ser cacheada indefinidamente por `(standard@version, level)` | MAY |
| **ST25** | Standard MAY definir zero requisitos (placeholder normativo válido) | MAY |
| **ST26** | Conformance Level MAY ser definido sem `inherits_from` (nível raiz independente) | MAY |

---

## 18. Validação Institucional

| Documento base | Resultado | Evidência de conformidade |
|---|---|---|
| **Constitution** | **PASS** | `precedence_level` reutiliza hierarquia existente; NRs estruturados realizam "documentação executável"; `INDETERMINATE` obrigatório realiza "Confiança verificável"; ST8 realiza "Transparência" |
| **Kernel Architecture** | **PASS** | Standard é Component pleno; §2.9, §2.10, §7, §8, §9 reutilizados sem modificação; nenhum campo do Component Contract alterado |
| **Governance Architecture** | **PASS** | §7 (Admission), §8 (autoridade), §10 (Breaking Change), §12 (Audit), §16 (Deprecation), §17 (Conflict) delegados integralmente; nenhuma autoridade nova criada |
| **Domain Model v1.1.0** | **PASS** | Zero entidades, zero relações, zero estados novos. Verificado item a item na tabela §4.1 |
| **RFC-DM-001** | **PASS** | C2 (Context Snapshot) obrigatório em Claims (ST17); C1 respeitado; C3 não tocado; C4 não tocado; §3.6 (cardinalidade) é base da lineage |
| **Identity & Namespace** | **PASS** | §2.2 (Value Object), §3.2 (tombstone, isomórfico a §5.3), §4.1, §4.3, §4.4, §5, §7, §9, §10 reutilizados |
| **Registry & Discovery** | **PASS** | ST2 garante ausência de registry paralelo; §5, §6.1, §7.3, §8, §11 reutilizados |
| **Validation & Certification** | **PASS** | §4 (gate de Verification) e §7 (critério para `component_type=Standard`) reutilizados; §5 (L3) fechado por §8.4 sem alteração; §6 (Reproducibility) reutilizado literalmente |
| **Composition Architecture** | **PASS** | Desbloqueia §14 sem alterá-lo; `applies_to = COMPOSITION` avalia Assembly de §5 |
| **Workflow Architecture** | **PASS** | Padrão de Value Object de §4 replicado; `GATE_AUTO` consome Claims sem que Standard vire Gate |
| **Execution Architecture** | **PASS** | Context Snapshot de §5 usado para reprodutibilidade; nenhum acoplamento reverso |
| **Restrições 1–10 do mandato** | **PASS** | (1) zero entidades ✔ (2) zero relações ✔ (3) zero lifecycle ✔ (4) tudo reutiliza Execution/Artifact/Decision/Evidence/Context/Role/Capability/Constraint/VersionedIdentifier/Registry/Certification/Governance ✔ (5) Standard é Component ✔ (6) NR é Value Object ✔ (7) n/a a este documento ✔ (8) Conformance Claim é Artifact genérico ✔ (9) nenhuma RFC ✔ (10) tudo por reutilização ✔ |
| **Exige RFC?** | **NÃO** | — |

---

## 19. Dependências Futuras

| Consumidor | O que consome | Estado |
|---|---|---|
| **Policy Architecture** (Documento 2) | `VersionedIdentifier` + `ConformanceLevel` em `PolicyBinding`; `precedence_level` para a regra de override GLOBAL | Fechado neste bloco |
| **Compliance Architecture** | `NormativeRequirement[]`, `EvaluationMethod`, `EvidenceRequirement`, Conformance Claim | Downstream, não bloqueante |
| **Composition Architecture §14** | Critério normativo em `Composition Slot` além de `min_certification_level` | Desbloqueado estruturalmente; ativação requer Policy |
| **Skill / Agent / Template Architecture** | `ComplianceTarget.component_types` específicos; NRs por tipo | Aditivo, não bloqueante |
| **Organization & Tenancy Architecture** | Nada de Standard (Standard não conhece Organization por ST1); consome via Policy | Isolado por design |
| **Testing Architecture** | Formalização de como Evidence é produzida para `EvaluationMethod.kind = DYNAMIC` | `[LACUNA proposital]` |
| **Packaging & Distribution Architecture** | Serialização canônica de Standards e Packages; `manifest_digest` para Integrity | `[LACUNA proposital]` já declarada em §3.2 |
| **Observability & Provenance Storage** | Séries históricas de Conformance Claims para análise de drift normativo | `[LACUNA proposital]` já declarada em Execution §14 |
