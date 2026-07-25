# Packaging & Distribution Architecture
### Framework Eng — Serialização, Integridade em Trânsito e Portabilidade Institucional

*Versão 1.0.0 · Base normativa (congelada): Constitution · Kernel · Governance · Domain Model v1.1.0 · RFC-DM-001 · Identity & Namespace · Registry & Discovery · Validation & Certification · Composition · Workflow · Execution · Standards · Policy · Template Architecture · Skill Architecture · Observability Architecture · Agent Architecture · Organization & Tenancy · Testing Architecture*

> **Tese central, provada seção a seção:** este documento fecha as últimas quatro `[LACUNA proposital]` declaradas pela série — serialização física (Standards §3.2, Template §3.2), formato de exportação de métricas (Observability §17), e distribuição de Templates entre organizações (Skill §17). O objeto central, `Bundle`, **não é uma entidade do Domain Model** — é uma **codificação física, portátil e verificável** de dados que já possuem Identity, Lifecycle e digest (Validation & Certification §6). Empacotar não cria; **transporta com prova**.

---

## 1. Posição Arquitetural

### 1.1 Desambiguação terminológica obrigatória

`[ESCOLHA DE DESIGN]`

**Motivação:** Standards Architecture §9 já usa o termo *"Standard Package"* (`standard_kind = PACKAGE`) para um Standard agregador via `includes`. Este documento precisa de um termo para "a unidade física transportável de um Component" — usar "Package" aqui colidiria exatamente com o termo já reservado.

**Alternativas rejeitadas:** reutilizar "Package" também para a unidade de distribuição, confiando no contexto para desambiguar.

**Justificativa técnica:** RFC-DM-001 eliminou, nos achados C1/H1, precisamente esta classe de erro — um termo com dois significados no mesmo corpo normativo. Um `Standard Package` é um **Component normativo** (agrega `NormativeRequirement`s por `includes`); a unidade que este documento define é uma **codificação de transporte** de qualquer Manifest, sem conteúdo normativo próprio. São conceitos de naturezas diferentes que, por acidente de linguagem, poderiam compartilhar um nome.

**Decisão:** o termo técnico deste documento é **`Bundle`** (Distribution Bundle), nunca "Package", em nenhuma seção, tabela ou algoritmo abaixo.

### 1.2 O que é um Bundle

Um `Bundle` **não é uma entidade do Domain Model**. É a **serialização canônica e verificável** de um ou mais `Manifest`s já existentes, imutáveis e identificados (Kernel §8; Identity §4.1), acompanhada de seu `manifest_digest` (Validation & Certification §6) — suficiente para transportar um Component (ou o fecho de suas dependências) para fora da Registry institucional e reintroduzi-lo, com integridade verificável, em qualquer outro ponto — incluindo um deployment físico distinto do Framework.

```
Manifest (já imutável, já com Identity)
   │  serialização canônica  [Identity §4.4 — reutilizada, sem novo encoding]
   ▼
Bundle{ manifests[], manifest_digest[], format_version }
   │  transporte (rede, mídia física, air-gap)
   ▼
verify_bundle() — recomputa digest, compara            [Validation & Certification §6]
   │
   ▼
import_bundle() — Governance §7 Admission, sem atalho    [nenhuma autoridade nova]
```

### 1.3 Fronteiras negativas (invioláveis)

| Fronteira | Regra |
|---|---|
| Bundle não é entidade | Não possui Identity, Lifecycle ou Registro próprios — é encoding de algo que já os possui |
| Bundle não confere Certificação | Evidência de Certificação carregada em um Bundle é **advisória**, nunca automaticamente reestabelecida no deployment receptor (§6) |
| Bundle não contorna Admissão | `import_bundle` **MUST** passar por Governance §7, exatamente como qualquer Component recém-autorado |
| Bundle não introduz novo esquema de identidade | Identity de todo conteúdo é a `VersionedIdentifier` já existente (Identity §4.1) — nunca um "Bundle ID" paralelo |
| Bundle não altera imutabilidade | Um Bundle nunca modifica o Manifest que empacota — apenas o transporta |

---

## 2. Objetivos

| # | Objetivo | Fecha |
|---|---|---|
| O1 | Definir a codificação física de Manifest, Templates, Test Suite, NRs — sem inventar novo formato lógico | Standards §3.2, Template §3.2 |
| O2 | Definir verificação de integridade em trânsito | Validation & Certification §6, aplicado fora da Registry |
| O3 | Definir exportação/importação respeitando Governance e isolamento por Organization | Organization §6.3 |
| O4 | Definir formato de exportação de séries de `Metric` | Observability §17 |
| O5 | Definir portabilidade de Templates entre organizações | Skill §17 |

---

## 3. Escopo

### 3.1 Pertence

Estrutura de `Bundle`; serialização canônica de Manifest e conteúdo interno type-specific; verificação de digest; exportação com/sem fecho de dependências; importação via Admissão; confiança em evidência de Certificação cross-deployment; serialização de `MetricSeries`.

### 3.2 Não pertence — com justificativa

| Excluído | Justificativa |
|---|---|
| Protocolo de rede/transporte físico (HTTP, filesystem, mídia) | Fora da altitude arquitetural de todo o Framework — nenhum documento anterior especificou protocolo de rede; este não seria o primeiro a fazê-lo |
| Autenticação/autorização de quem pode exportar/importar | Fora de escopo desde Identity §1; a autoridade de **admitir** o conteúdo importado continua sendo Governance §7, já suficiente |
| Compressão, formato binário específico | Detalhe de implementação abaixo da altitude conceitual já mantida em toda a série (ex.: Identity §4.4 já se absteve de mandar um encoding físico específico além do charset) |
| Federação entre múltiplas instâncias de Registry | Fora de escopo — Registry & Discovery §1 já estabeleceu Registry como autoridade lógica única; Bundle resolve exatamente o caso em que **não** há uma Registry compartilhada (transporte para fora do Framework, ou entre deployments totalmente separados) |

---

## 4. Modelo Conceitual

### 4.1 Tabela de proveniência — prova de minimalidade

| Conceito usado por Packaging | Natureza | Já definido em |
|---|---|---|
| `Manifest`, imutabilidade por versão | **Reutilizado, sem alteração** | Kernel §8 |
| `manifest_digest` | **Reutilizado — já existia para Integrity** | Validation & Certification §6 |
| Serialização canônica (charset, ordem determinística) | **Reutilizado, sem novo encoding** | Identity & Namespace §4.4 |
| `VersionedIdentifier` | **Reutilizado — identidade do conteúdo do Bundle** | Identity §4.1 |
| Admissão (Governance §7) | **Reutilizado — único caminho de importação** | Governance §7 |
| `Assembly` (fecho de dependências) | **Reutilizado, para exportação com closure** | Composition §5 |
| `Decision Record` (evidência de Certificação) | **Reutilizado, transportado como conteúdo advisório** | Domain Model §14 |
| Isolamento por Namespace | **Reutilizado, sem extensão** | Identity §10; Organization §6.3 |
| `Metric` | **Reutilizado — fonte de `MetricSeries`** | Domain Model §2 #14 |
| SemVer | **Reutilizado — disciplina aplicada ao formato do Bundle (§4.3)** | Kernel §2.11 |
| Detecção de ciclo | **Reutilizado — grafo de fecho já garantido acíclico por Composition §7** | Kernel §7 |

**Nenhuma linha introduz entidade, relação ou estado novo.**

### 4.2 Estrutura formal

```
Bundle {                                             [codificação física — NÃO é entidade do Domain Model]
  bundle_format_version : SemVer                      [§4.3]
  primary_subject        : VersionedIdentifier
  manifests               : [ (VersionedIdentifier, SerializedManifest, Digest) ]
                                                        (1 elemento se standalone; N se fecho de dependências)
  certification_evidence  : [DecisionRecordRef]?        (opcional — §6, sempre advisória)
  exported_at              : Timestamp
  exported_by               : Role
}
```

### 4.3 `bundle_format_version` — versionamento do encoding, não do conteúdo

`[ESCOLHA DE DESIGN]`

**Motivação:** decidir se a codificação física do Bundle precisa de seu próprio esquema de versão, distinto da versão de cada Manifest que ele carrega.

**Alternativas rejeitadas:** usar a versão do `primary_subject` como versão implícita do formato do Bundle inteiro.

**Justificativa técnica:** a codificação (como bytes representam um Manifest) e o conteúdo (o que aquele Manifest significa) evoluem em ritmos independentes — o Kernel pode, em tese, evoluir seu esquema de Manifest (via RFC futura) sem que nenhum Standard/Skill/Agent individual mude de versão. Confundir os dois faria a interpretação de um Bundle antigo depender de inferência sobre o conteúdo, em vez de uma verificação direta de compatibilidade de formato — reproduzindo a ambiguidade já eliminada por RFC-DM-001 §3.3 entre `Coordinate` e `Version`.

**Justificativa formal:** `bundle_format_version` reutiliza a **disciplina** SemVer (Kernel §2.11) — MAJOR quando a estrutura de serialização muda de forma incompatível (um leitor antigo não consegue mais decodificar), MINOR quando novos campos opcionais são adicionados (retrocompatível), PATCH para correção sem mudança estrutural. **Nenhum sistema de versionamento novo** — mesma semântica, aplicada a um sujeito diferente (o encoding, não o Component).

**Precedente arquitetônico:** a distinção entre versão de protocolo/formato e versão de conteúdo é padrão em qualquer sistema de serialização durável (ex.: versão de schema do Protocol Buffers é independente da versão semântica da API que o usa).

---

## 5. Estrutura do Bundle

Reutiliza integralmente a serialização canônica já definida:

- **Charset e encoding**: Identity & Namespace §4.4 — nenhuma extensão.
- **Ordem determinística de campos**: mesma regra já aplicada para digest de Template (Template §12) e de Manifest (Validation & Certification §6) — necessária para que `manifest_digest` seja reproduzível.
- **Conteúdo interno type-specific incluído**: `templates[]` (Template §4.2), `test_suite[]` (Testing §5.2), `requirements[]` (Standards §4.2), `bindings[]`/`scope` (Policy §5.1-§5.3), `phases[]` (Workflow §4) — cada um serializado exatamente conforme seu próprio documento de origem já especifica; Packaging não redefine nenhum desses formatos, apenas os concatena canonicamente.

**Regra de determinismo (PK6):** `export_bundle(subject, options)` **MUST** ser uma função pura — mesmo `subject` (Manifest imutável) e mesmas `options` **MUST** produzir Bundle byte-idêntico, sempre. Mesma prova de correção já usada para `Expand()` (Template §7, TP2).

---

## 6. Integridade e Confiança entre Deployments

### 6.1 Verificação de digest

Reutiliza `manifest_digest` (Validation & Certification §6) sem alteração: `verify_bundle` recomputa o digest sobre a serialização canônica de cada Manifest contido e compara ao digest declarado. Qualquer divergência **MUST** rejeitar o Bundle inteiro — nunca aceitar parcialmente.

### 6.2 Evidência de Certificação é advisória, nunca vinculante

`[ESCOLHA DE DESIGN]`

**Motivação:** decidir se `Decision Record`s de Certificação carregados em um Bundle deveriam re-estabelecer automaticamente aquele nível de Certificação no deployment receptor.

**Alternativas rejeitadas:** aceitar Certificação carregada em Bundle como válida por transitividade de confiança entre deployments.

**Justificativa técnica:** Governance §4/§8 estabelece autoridade de Certificação como **local a um deployment** — um Certifier em um deployment não tem, por definição, autoridade delegada em outro (Governance nunca definiu confiança federada entre instâncias distintas de Governança). Aceitar automaticamente quebraria exatamente a garantia de Governance §12 (Auditoria) de que "quem audita não pode ter aprovado ou sido Owner do que audita" — aqui generalizada: nenhuma autoridade de um deployment estranho pode substituir a autoridade local.

**Regra (PK4):** `certification_evidence` de um Bundle **MUST** ser tratada como `Evidence` (Domain Model §13) de suporte — **MAY** acelerar re-certificação local (ex.: pular diretamente a fase de Testing se o `TestRunReport` original acompanhar o Bundle, Testing §5.2), mas **MUST NOT** conceder Certificação sem passar pela `Decision` local de um Certifier do deployment receptor.

**Precedente arquitetônico:** exatamente a mesma cautela de sistemas de assinatura de pacotes que aceitam a assinatura como prova de proveniência, mas exigem que a política local (não a de origem) decida se aquela proveniência é suficiente para confiança operacional.

### 6.3 Isolamento por Namespace na importação

`import_bundle` **MUST** respeitar exatamente a mesma regra de qualificação cross-namespace já normatizada por Identity §10 e operacionalizada por Organization §6.3: um Bundle contendo Components de `org.acme/` só pode ser importado sob `org.acme/` (ou sob uma Organization diferente, mediante nova Admissão que reserve um Coordinate distinto — nunca uma reatribuição implícita de Namespace). **Nenhum mecanismo de isolamento novo.**

---

## 7. Modelo Operacional

**Serviço:** nenhum substrato novo. `export_bundle`/`verify_bundle`/`import_bundle` são operações de leitura/serialização sobre dados já geridos pelo Registry (Registry §5-§6) e Governance (§7), mais uma função pura de encoding.

```
export_bundle(subject: VersionedIdentifier, include_dependency_closure: boolean,
               include_certification_evidence: boolean) → Bundle
  PRE:  subject resolve via Registry a lifecycle_state ∈ {Active, Deprecated}
  POST: Bundle imutável, determinístico (PK6)

verify_bundle(bundle) → VerificationResult
  POST: PASS se todo digest confere; FAIL explícito caso contrário — nunca aceitação parcial

import_bundle(bundle, target_namespace) → DecisionRecord | AdmissionError
  PRE:  verify_bundle(bundle) = PASS
  POST: cada Manifest do bundle segue Governance §7 (Admission) integralmente — sem atalho

export_metrics_series(metric_ref, time_range) → MetricSeries
  # fecha Observability §17 — ver §9.4
```

---

## 8. Fluxo de Exportação/Importação

```
1. export_bundle(skill@2.1.0, include_dependency_closure=true, include_certification_evidence=true)
   a. Composition.resolve_assembly(skill@2.1.0) → fecho de dependências                    [Composition §5]
   b. PARA CADA Manifest no fecho: serializar canonicamente, computar digest                [Identity §4.4]
   c. SE include_certification_evidence: anexar Decision Records de CertificationGrant vigentes
   d. Materializar Bundle{ manifests[], certification_evidence?, format_version }

2. Transporte (fora de escopo — §3.2)

3. verify_bundle(bundle) no deployment receptor
   a. Recomputar digest de cada manifest, comparar

4. import_bundle(bundle, target_namespace="org.acme")
   a. PARA CADA (coordinate, manifest, digest) no bundle:
      i.   Governance.Admit(coordinate, manifest, requested_by)                              [Governance §7]
      ii.  Registry.register(...)                                                             [Registry §5]
   b. certification_evidence anexada como Evidence de suporte, MUST NOT conceder nível automaticamente  [PK4]
```

---

## 9. Algoritmos

```
ALGORITMO ExportBundle(subject, include_closure, include_cert_evidence):
  manifests ← [ (subject, Serialize(Registry.resolve(subject).manifest)) ]
  SE include_closure:
     assembly ← Composition.resolve_assembly(subject)                     # Composition §5 — já acíclico
     PARA CADA dep EM assembly.resolved_dependencies:
        manifests += (dep, Serialize(Registry.resolve(dep).manifest))
  digests ← [ (coord, ComputeDigest(ser)) PARA (coord, ser) EM manifests ]
  cert_evidence ← SE include_cert_evidence:
                     Governance.query(subtype=CERTIFICATION_GRANT, subject=subject, superseded=false)
                   SENÃO: null
  RETORNA Bundle{ bundle_format_version: CURRENT, primary_subject: subject,
                  manifests: Zip(manifests, digests), certification_evidence: cert_evidence,
                  exported_at: now(), exported_by: CurrentRole() }
  # TERMINAÇÃO: fecho de dependências já garantido finito e acíclico por Composition §7

ALGORITMO VerifyBundle(bundle):
  SE bundle.bundle_format_version.major > CURRENT.major:
     RETORNA VerificationResult(FAIL, UNSUPPORTED_FORMAT_VERSION)          # falha explícita, nunca melhor esforço
  PARA CADA (coord, ser, digest_declarado) EM bundle.manifests:
     digest_recomputado ← ComputeDigest(ser)
     SE digest_recomputado ≠ digest_declarado:
        RETORNA VerificationResult(FAIL, DIGEST_MISMATCH, coord)           # rejeita o Bundle inteiro
  RETORNA VerificationResult(PASS)

ALGORITMO ImportBundle(bundle, target_namespace):
  ASSERT VerifyBundle(bundle) = PASS                                        # PK2
  resultados ← []
  PARA CADA (coord, ser, _) EM bundle.manifests:
     ASSERT NamespaceOf(coord) ⊆ target_namespace ∨ NamespaceOf(coord) = "core"   # §6.3, Identity §10
     manifest ← Deserialize(ser)
     dependencias_faltantes ← [ d PARA d EM manifest.dependencies SE Registry.resolve(d) = NotFound ]
     SE dependencias_faltantes ≠ ∅:
        RETORNA AdmissionError(MISSING_DEPENDENCIES, dependencias_faltantes)  # nunca admissão parcial
     decision ← Governance.Admit(coord, manifest, requested_by=CurrentRole())  # §7 — sem atalho
     Registry.register(manifest, decision.decision_record)
     resultados += decision.decision_record
  SE bundle.certification_evidence ≠ null:
     PARA CADA dr EM bundle.certification_evidence:
        AnexarComoEvidence(dr, subject=coord)                                # PK4 — nunca concede nível
  RETORNA resultados

ALGORITMO ExportMetricsSeries(metric_ref, time_range):
  observacoes ← Observability.query(metric=metric_ref, range=time_range)      # Observability §7.1
  RETORNA MetricSeries{
     metric_ref, points: SortBy(observacoes, timestamp),
     serialization: SerializeCanonically(observacoes)                        # Identity §4.4 — sem novo encoding
  }
```

---

## 10. Diagramas

### 10.1 UML — Bundle como codificação, não entidade

```
┌──────────────┐  serializa  ┌─────────────────────────┐
│ Manifest      ├────────────►│ SerializedManifest        │  (dado opaco, canônico)
│ (imutável,    │             └───────────┬──────────────┘
│  já com       │                          │ digest
│  Identity)    │                          ▼
└──────────────┘             ┌─────────────────────────┐
                              │ Digest                    │   [Validation & Certification §6]
                              └─────────────────────────┘
        ┆ agregação física — NÃO é relação do Domain Model
        ▼
┌──────────────────────────────────────────┐
│ Bundle                                     │  «codificação, não entidade»
│  manifests[] : [(VersionedIdentifier,       │
│                  SerializedManifest, Digest)]│
│  certification_evidence[]? ────────────────┼──► Decision Record  [advisória — PK4]
└──────────────────────────────────────────┘
```

### 10.2 Sequência — exportação e reimportação

```
Owner        PackagingSvc      Composition      Registry        Governance(destino)
   │              │                 │               │                    │
   ├─export_bundle(subject, closure=true)─────────►│                    │
   │              ├─resolve_assembly ──────────────►│                    │
   │              │◄─fecho──────────────────────────┤                    │
   │              ├─Serialize + Digest cada Manifest │                    │
   │◄─Bundle───────┤                                                       │
   │                                                                       │
   │  [transporte — fora de escopo]                                       │
   │                                                                       │
   ├─verify_bundle(bundle)──────────────────────────────────────────────►│
   │◄─PASS/FAIL──────────────────────────────────────────────────────────┤
   │                                                                       │
   ├─import_bundle(bundle, "org.acme")──────────────────────────────────►│
   │              │                                  ├─Admit (§7, sem atalho)
   │◄─DecisionRecord[]────────────────────────────────────────────────────┤
```

### 10.3 Estados

Nenhum — Bundle não tem Lifecycle. Cada Manifest importado assume o Kernel Lifecycle já existente, a partir de `Draft` (Governance §7), exatamente como qualquer Component recém-autorado.

---

## 11. Casos Extremos

| # | Caso | Tratamento |
|---|---|---|
| P1 | Digest não confere (adulteração ou corrupção em trânsito) | `VerificationResult(FAIL, DIGEST_MISMATCH)` — Bundle inteiro rejeitado, nunca aceitação parcial |
| P2 | `bundle_format_version` mais nova que o suportado pelo receptor | `FAIL(UNSUPPORTED_FORMAT_VERSION)` — nunca melhor esforço de leitura parcial |
| P3 | Dependência do fecho ausente no deployment receptor | `AdmissionError(MISSING_DEPENDENCIES, [...])` — listadas explicitamente, mesma disciplina de `SlotUnsatisfied` (Composition §9) |
| P4 | `certification_evidence` de um deployment não confiável | Tratada apenas como `Evidence` de suporte — **MUST NOT** conceder nível (PK4) |
| P5 | Reimportação do mesmo Bundle (idempotência) | `Governance.Admit` já detecta duplicação via `search` (Registry §5) — comportamento idêntico ao de qualquer Admissão redundante, nenhuma regra nova |
| P6 | Bundle contendo Component cujo Namespace não pertence ao `target_namespace` nem a `core/` | Rejeitado — mesma regra de Identity §10, sem exceção |
| P7 | Fecho de dependências excede limite prático de tamanho | `[DÍVIDA TÉCNICA reconhecida]`, mesma classe já assumida para profundidade de `extends` (Standards §15.3) — sem limite normativo nesta versão |
| P8 | `MetricSeries` para `time_range` sem observações | Série vazia é resultado válido, mesma disciplina de Observability §11/B8 |

---

## 12. Performance

| Operação | Cache/Complexidade |
|---|---|
| `export_bundle` (sem closure) | O(1) — Manifest já imutável e serializável de forma cacheável indefinidamente |
| `export_bundle` (com closure) | O(V+E) sobre o grafo de Assembly, já garantido finito/acíclico por Composition §7 |
| `verify_bundle` | O(N) sobre número de Manifests contidos — recomputação de digest é a única operação não trivial |
| `import_bundle` | Dominada pelo custo de `Governance.Admit`, já normatizado (Governance §7) |

**Cache:** um Bundle exportado para `(subject@version, options)` é cacheável indefinidamente — mesma prova de determinismo de PK6 e mesma disciplina de cache-por-imutabilidade já usada em Registry §8, Standards §15.1, Template §12, Skill §12.

---

## 13. Eventos

| Evento | Ocorre quando |
|---|---|
| `BundleExported(subject, format_version, manifest_count)` | `ExportBundle` concluído |
| `BundleVerificationFailed(reason)` | P1 ou P2 |
| `BundleImported(target_namespace, admitted_count)` | `ImportBundle` concluído com sucesso |
| `BundleImportBlocked(missing_dependencies)` | P3 |
| `CertificationEvidenceAttachedAdvisory(subject)` | PK4 |
| `MetricsSeriesExported(metric_ref, range)` | `ExportMetricsSeries` |

Mesma classe operacional já usada em toda a série — não são Domain Model Event Entities.

---

## 14. Regras Normativas (RFC 2119)

| # | Regra | Nível |
|---|---|---|
| PK1 | O termo "Package" MUST NOT ser reutilizado para a unidade de distribuição — o termo técnico MUST ser "Bundle" | MUST NOT / MUST |
| PK2 | `import_bundle` MUST verificar digest de todo Manifest contido antes de qualquer Admissão | MUST |
| PK3 | `import_bundle` MUST rotear cada Manifest por Governance §7 — MUST NOT contornar Admissão | MUST / MUST NOT |
| PK4 | Evidência de Certificação carregada em Bundle MUST NOT conceder nível automaticamente — apenas Evidence de suporte | MUST NOT |
| PK5 | `bundle_format_version` MUST seguir disciplina SemVer; mudança incompatível MUST exigir nova major version do formato | MUST |
| PK6 | `export_bundle` MUST ser função pura e determinística de `(subject, options)` | MUST |
| PK7 | Importação MUST NOT alterar a `VersionedIdentifier` de nenhum conteúdo do Bundle | MUST NOT |
| PK8 | `MetricSeries` MUST usar a serialização canônica já definida por Identity §4.4, sem novo encoding | MUST |
| PK9 | Bundle contendo Component fora do `target_namespace` e fora de `core/` MUST ser rejeitado | MUST |
| PK10 | Verificação de digest com falha MUST rejeitar o Bundle inteiro, nunca parcialmente | MUST |

---

## 15. Integrações

| Documento | Como Packaging o consome — sem alteração |
|---|---|
| **Kernel** | Imutabilidade de Manifest (§8) é a base da determinística de `export_bundle` |
| **Governance** | Único caminho de importação — §7, sem atalho (PK3) |
| **Domain Model v1.1.0** | Nenhuma entidade nova; `Decision Record` transportado como Evidence |
| **Identity & Namespace** | Serialização canônica (§4.4) reutilizada sem extensão; isolamento por Namespace (§10) na importação |
| **Registry & Discovery** | `resolve()`/`register()` reutilizados sem modificação |
| **Validation & Certification** | `manifest_digest` (§6) é o mecanismo de integridade inteiro deste documento |
| **Composition** | `resolve_assembly` (§5) usado para fecho de dependências na exportação |
| **Standards** | Desambiguação explícita de "Standard Package" (§9) — nenhuma colisão terminológica |
| **Observability** | Fecha §17 — `export_metrics_series` dá forma física ao contrato conceitual já declarado |
| **Skill / Template / Agent** | Fecha Skill §17 — Templates/Skills/Agents tornam-se portáveis entre organizações via Bundle |
| **Organization & Tenancy** | Isolamento cross-org na importação reutiliza exatamente §6.3 |
| **Testing Architecture** | `TestRunReport` **MAY** acompanhar um Bundle como Evidence de suporte para acelerar re-certificação local (§6.2) |

---

## 16. Validação Institucional

| Documento base | Resultado |
|---|---|
| Constitution | **PASS** — PK4/PK3 realizam Auditabilidade e Responsabilidade; nenhuma confiança cega entre deployments |
| Kernel | **PASS** |
| Governance | **PASS** — único caminho de Admissão preservado |
| Domain Model v1.1.0 | **PASS** — zero entidades/relações/estados |
| RFC-DM-001 | **PASS** |
| Identity & Namespace | **PASS** — encoding e isolamento reutilizados sem extensão |
| Registry & Discovery | **PASS** |
| Validation & Certification | **PASS** — `manifest_digest` é o mecanismo central, intocado |
| Composition | **PASS** |
| Workflow / Execution | **PASS** |
| Standards | **PASS** — desambiguação explícita de terminologia, §9 intocado |
| Policy | **PASS** |
| Template Architecture | **PASS** — fecha §3.2 |
| Skill Architecture | **PASS** — fecha §17 |
| Observability Architecture | **PASS** — fecha §17 |
| Agent Architecture | **PASS** |
| Organization & Tenancy | **PASS** — isolamento reutilizado |
| Testing Architecture | **PASS** — `TestRunReport` reutilizável como Evidence |
| **Exige RFC?** | **NÃO** |

---

## 17. Dependências Futuras

| Consumidor | O que consome | Estado |
|---|---|---|
| **Fase de conteúdo** (Standards/Skills/Templates/Agents/Workflows reais) | `Bundle` como unidade de distribuição de biblioteca institucional entre organizações | Desbloqueado |
| **Resource & Quota Architecture** (futuro, já deferida por Organization §17) | Medição de consumo de exportação/importação, se necessário | Sem bloqueio — fora de escopo aqui, deliberadamente |

---

## 18. Critério de Aceitação

### ✔ Checklist Institucional

| Critério | Status |
|---|---|
| Serialização física fechada (Standards §3.2, Template §3.2) | ✔ §5 |
| Integridade em trânsito | ✔ §6.1, PK2/PK10 |
| Exportação de métricas (Observability §17) | ✔ §9.4, PK8 |
| Distribuição de Templates entre organizações (Skill §17) | ✔ §1.2, §8 |
| Desambiguação de "Package" vs. "Standard Package" | ✔ §1.1, PK1 |
| Zero entidade/relação/estado/autoridade nova | ✔ §16 |
| UML, sequência, algoritmos, casos extremos, RFC2119 | ✔ §9-§14 |
| Nenhuma RFC necessária | ✔ §16 |

### ✔ Confirmação Explícita

Nenhum documento da base normativa foi alterado. `Bundle` é uma codificação física de dados já imutáveis e identificados, nunca uma entidade; integridade reutiliza `manifest_digest` já existente; importação nunca contorna Admissão; evidência de Certificação nunca cruza fronteira de autoridade automaticamente. **Quatro `[LACUNA proposital]` de quatro documentos distintos (Standards, Template, Observability, Skill) fecham-se aqui, sem alteração retroativa a nenhum deles.**
