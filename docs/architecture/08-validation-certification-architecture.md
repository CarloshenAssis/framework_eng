# FASE 4 — Validation & Certification Architecture
### Framework Eng — Da Existência à Confiança Institucional

*Versão 1.0.0 · Base: Constitution, Kernel, Governance, Domain Model v1.1.0, RFC-DM-001, Identity & Namespace, Registry & Discovery*

---

## 1. Posição Arquitetural e Separação de Responsabilidades

Dez termos, dez responsabilidades **não sobrepostas**:

| Termo | Pergunta que responde | Natureza | Definido aqui ou reutilizado? |
|---|---|---|---|
| **Verification** | "O Manifest está bem formado, per o Kernel?" | Automatizada, estrutural | Reutiliza Kernel §8 "Validação Estrutural" |
| **Testing** | "O que acontece quando eu executo isto?" | Atividade que produz Evidence | Novo (mecanismo, não julgamento) |
| **Validation** | "O componente faz o que declara, incluindo modos de falha?" | Julgamento sobre Evidence de Testing + Verification | Reutiliza Kernel §8 "Validação de Conformidade", ampliado |
| **Conformance** | "Está alinhado a um Standard/Policy nomeado, especificamente?" | Subconjunto normativo da Validation | Novo, escopo estreito |
| **Compliance** | "Ainda está alinhado, agora, de forma contínua?" | Monitoramento contínuo, não pontual | Reutiliza Governance §13 integralmente |
| **Approval** | "Pode existir/tornar-se Active?" | Decisão de admissão (gate único) | Reutiliza Governance §7 |
| **Certification** | "Está formalmente atestado como confiável, num nível declarado, até quando?" | Status registrado, expirável, revogável | Novo — arquitetura central deste documento |
| **Governance** | "Quem tinha autoridade para decidir isto?" | Autoridade | Reutiliza Governance Architecture integralmente |
| **Integrity** | "Isto é exatamente o que foi certificado, sem adulteração?" | Propriedade técnica (hash/digest) | Novo, escopo estreito |
| **Reproducibility** | "Se eu repetir a validação, chego ao mesmo resultado?" | Meta-critério sobre a própria Evidence | Novo, requisito para Evidence, não gate separado |

**Regra central de não-sobreposição:** `Approval` e `Certification` são **eventos independentes** — um Component pode estar `Active` (Approved) e nunca ter sido `Certified`; pode perder Certificação sem deixar de estar `Active`. Confundir os dois é o erro mais comum em pipelines de qualidade reais e é explicitamente proibido aqui.

---

## 2. Objetivos e Motivação

Definir como um componente `Active` mas não comprovado passa a ser **institucionalmente confiável**, com evidência, nível, prazo e reversibilidade — sem introduzir uma segunda máquina de estados paralela ao Kernel Lifecycle, e sem exigir emenda ao Domain Model.

---

## 3. Escopo e Modelo Conceitual — a Decisão de Reuso Central

`[ESCOLHA DE DESIGN — decisão arquitetural mais importante deste documento]`: **nenhuma entidade nova é introduzida no Domain Model.** Certificação é modelada inteiramente sobre primitivas já existentes:

- **Validation Result = `Evidence`** (Domain Model, especialização de `Artifact`). Satisfaz exatamente a definição existente ("Artifact cuja função exclusiva é comprovar que uma Execution produziu o resultado declarado") — testar um componente é uma `Execution`; seu resultado é `Evidence`. Nenhuma nova especialização de Artifact é necessária.
- **Certificate = um padrão estruturado de `Decision` / `Decision Record`.** Uma família nomeada de subtipos de Decision: `CertificationGrant`, `CertificationRenewal`, `CertificationSuspension`, `CertificationRevocation`. O "certificado" **é** o Decision Record mais recente, não-superado, dessa família, referenciando uma `Versioned Identifier` específica.

**Por que não criar uma entidade `Certificate` dedicada:** faria exatamente o que a revisão institucional penalizou antes (C1) — um novo conceito paralelo a algo que já existe e já cumpre a função. `Decision`/`Decision Record` já modelam "escolha formal, autorizada, imutável, superável apenas por novo registro" — precisamente as propriedades que Certification precisa. Reaproveitar evita uma emenda ao Domain Model inteiramente.

**Consequência para o Registry (Fase 3, §12):** `RegistryEntry.certification_status` é a projeção computada: *"a Decision Record da família Certification mais recente, não superada, referenciando este Coordinate@Version."*

---

## 4. Pipeline Institucional (mapeado sobre o Kernel Lifecycle, não paralelo a ele)

```
Draft ──► Review ──► Approved ──► Active ──► Deprecated ──► Archived ──► Removed
  │           │                      │
  │      [Verification          [CERTIFICATION PIPELINE — opcional, aditivo, pós-Active]
  │       obrigatória              │
  │       p/ sair de Draft]        ├─► Pending ─► L1 ─► L2 ─► L3 ─► L4
  │                                │       (cada transição: Testing → Evidence → Validation → Decision)
  │      [Conformance          [Compliance contínua — Governance §13 — pode forçar Suspended]
  │       Validation dentro       │
  │       de Review]              └─► Expired / Suspended / Revoked (ver §6)
  ▼
[Duplication check via Registry search — Governance §7]
```

**Regra normativa:** Certificação **MUST** ocorrer apenas sobre um Component em `Active` ou `Deprecated` — nunca sobre `Draft`/`Review`/`Approved` (não há ainda nada publicamente consumível para certificar) nem sobre `Archived`/`Removed`.

---

## 5. Níveis de Certificação, Estados e Transições

| Nível | Nome | Critério de entrada | Evidência exigida | Role autorizante | Janela típica |
|---|---|---|---|---|---|
| **L0** | Unverified | Default ao entrar em `Active` | Nenhuma | Sistema (implícito) | N/A |
| **L1** | Structurally Valid | Verification (Kernel §8) passa | Structural Validation Evidence | Sistema (automatizado) | Perpétua enquanto Manifest não mudar |
| **L2** | Functionally Validated | Testing cobre Inputs/Outputs declarados, incl. modos de falha (Kernel §2.4-2.5) | Test Evidence | Reviewer | Proporcional ao risco (Governance §14) — ex. 6-12 meses |
| **L3** | Standards Certified | Conformance a todo Standard/Policy vinculado (Kernel §2.14) | Conformance Evidence por Standard | Governance Area Steward | Mais curta para domínios de alto risco |
| **L4** | Institutionally Certified | L3 + Reproducibility comprovada + assinatura humana | Tudo acima + Reproducibility Evidence + atestação do Certifier | **Certifier humano — obrigatório** | A mais curta; recertificação mandatória |

**Regra de composição de score:** avanço de nível exige o **mínimo por dimensão**, nunca uma média ponderada — uma Reproducibility = 0 **MUST NOT** ser compensada por Functional Score alto. Isso evita o anti-padrão clássico de rubricas de qualidade onde uma falha crítica é diluída pela média.

**Regra de separação de funções (continuidade do achado H2, revisão institucional anterior):** em L4, quando o Component sendo certificado é um `Agent`, o Certifier **MUST** ser um Role ocupado por humano — um `Agent` **MUST NOT** ser o único certificador L4 de outro `Agent` da mesma categoria operacional.

### Diagrama de Estados (Certificação)

```
[Active, L0] ──request──► Pending ──► L1 ──► L2 ──► L3 ──► L4
                                        │      │      │      │
                    validity elapses ───┴──────┴──────┴──────┴──► Expired(Ln) ──renewal──► Ln
                    compliance violation, grace exceeded (Governance §13) ─► Suspended(Ln) ──restored──► Ln
                    Certifier/Steward finds defect ─► Revoked ──full new cycle──► Pending
```

- **Expired:** passivo, automático, sem culpa — reversível por Renewal (revalidação rápida se nada mudou).
- **Suspended:** ativo, ligado à Compliance contínua (Governance §13) — reversível sem recomeçar o ciclo inteiro, apenas revalidando o que mudou.
- **Revoked:** o mais severo — Decision explícita, dispara notificação a todos os `consumers` (Kernel §2.7), exige ciclo completo novo, sem fast-path.

---

## 6. Evidências, Critérios, Score e Assinaturas

- **Evidência obrigatória por nível:** ver tabela §5, coluna "Evidência exigida" — nenhum nível avança sem sua Evidence correspondente registrada e referenciável (Domain Model §13).
- **Score:** rubrica multi-dimensional (Structural, Functional, Conformance, Reproducibility, Currency), 0-100 cada, **limiar mínimo por dimensão**, nunca média.
- **Assinatura:** todo `CertificationGrant` **MUST** incluir `{ certifier_role_id, timestamp, manifest_digest }`. `manifest_digest` é a propriedade de **Integrity**: se o Manifest resolvido hoje não bate com o digest assinado, a Certificação é automaticamente inválida independentemente do status registrado — Integrity é verificada em tempo de leitura, não apenas em tempo de escrita.
- **Reproducibility:** requisito sobre a própria Evidence, não um gate isolado — Evidence gerada por um processo que não pode ser re-executado de forma determinística **MUST** ser marcada `reproducible: false` e **MUST NOT**, sozinha, justificar avanço a L4.

---

## 7. Especialização por Tipo de Componente

`[ESCOLHA DE DESIGN]`: o pipeline (Draft→...→L4) é **idêntico em forma** para todo `component_type`, per Kernel §9 (Extension Model — validar forma, não enumerar tipos). Especialização ocorre **apenas** no método de coleta de Evidence:

| Tipo | Método de Evidence (Testing) | Foco da Conformance |
|---|---|---|
| **Skill** | Casos de teste funcionais contra Contract declarado | Corretude de I/O |
| **Agent** | Cenários comportamentais representativos; L4 exige avaliação humana | Comportamento sob ambiguidade + separação de funções (§5) |
| **Standard / Policy** | Revisão de completude e ausência de conflito de precedência (Governance §17) | Consistência normativa, não execução |
| **Template** | Validação contra Standards vinculados + checagem de renderabilidade | Completude estrutural |
| **Workflow** | Verificação de que todo Provider referenciado está em ≥L2; grafo de fases acíclico (reusa Kernel §7) | Integridade de composição |
| **Research** | Revisão metodológica por pares | Rigor institucional |
| **Playbook / Knowledge Asset** | Checagem de proveniência (`codifies` → `Knowledge` rastreável, RFC-DM-001 §3.1) + atualidade | Rastreabilidade e vigência |

---

## 8. Compatibilidade

- **SemVer:** Certificação é escopada a uma **Versioned Identifier** exata (Identity §4.1) — nunca a uma Coordinate sem versão.
- **Herança em PATCH:** um incremento de patch **MAY** herdar automaticamente o status de Certificação anterior **se** o Owner atestar formalmente que nenhuma mudança de Contract ocorreu (afirmação auditável, de baixo risco e reversível — Constitution, "fricção proporcional ao risco").
- **MINOR:** **MUST** repetir ao menos Verification (L1) antes de a Certificação anterior valer para a nova versão.
- **MAJOR:** **MUST** recertificar integralmente no nível antes detido — nenhuma herança.
- **Contract/Capability:** certificação é feita na granularidade do `Component`, não de `Capability` individual — evita explosão combinatória; Capabilities expostas herdam a certificação do Component que as `exposes` (Domain Model §5).

---

## 9. Revalidação, Expiração, Revogação, Histórico

- **Revalidação:** disparada por (a) expiração da janela de validade, (b) mudança em Standard/Policy vinculado (Governance §13, Compliance), ou (c) solicitação do Owner.
- **Histórico:** cada `CertificationGrant`/`Renewal`/`Suspension`/`Revocation` é um `Decision Record` permanente e imutável (`supersedes` encadeando a série) — a história completa de certificação de um Component é, por construção, sua cadeia de Decision Records, sem necessidade de armazenamento adicional.

---

## 10. Diagramas e Matrizes

### 10.1 Sequência — solicitação de certificação

```
Owner -> Certification Pipeline : request_certification(coordinate@version, target_level)
Pipeline -> Testing : execute(test_suite)
Testing --> Pipeline : Evidence[] (via Execution)
Pipeline -> Pipeline : score per dimension, check minimum thresholds
ALT score satisfaz target_level:
  Pipeline -> Role(Certifier) : request sign-off  [somente p/ L4]
  Role(Certifier) -> Pipeline : Decision(CertificationGrant)
  Pipeline -> Governance : produces Decision Record
  Pipeline -> Registry : notify (read-through update)
ELSE:
  Pipeline --> Owner : gaps[] (dimensão insuficiente)
```

### 10.2 Matriz Nível × Autoridade × Evidência — ver tabela §5 (consolidada, não duplicada aqui).

### 10.3 Matriz Tipo de Componente × Especialização — ver tabela §7.

---

## 11. Integrações

| Camada | Contrato |
|---|---|
| **Registry (Fase 3)** | Lê `certification_status` como projeção read-through sobre Decision Records; nunca grava. |
| **Governance** | Toda transição de nível **é** uma Decision sob a autoridade já definida em Governance §8 (Standards/Policies → Steward; estrutural → Council não se aplica aqui, é sempre nível Steward/Certifier). Compliance contínua (Governance §13) é o gatilho de `Suspended`. |
| **Kernel** | Certification nunca cria um segundo Lifecycle — opera estritamente dentro de `Active`/`Deprecated` (§4). Cycle detection de Workflow (§7 desta seção) reusa Kernel §7 sem modificação. |
| **Domain Model** | Zero entidades novas — reuso de `Evidence` e `Decision`/`Decision Record` (§3). |
| **Namespace** | Certificação referencia sempre a forma canônica totalmente qualificada (Identity §4.5) — nunca um alias. |
| **Futuras (Composition, Observability, Packaging)** | Composition Architecture poderá exigir nível mínimo de Providers (já antecipado em §7, linha Workflow); Observability consumirá Registry Events + Certification Decision Records como fonte de métricas de qualidade institucional (Governance §19) sem necessitar de nova integração. |

---

## 12. Regras Normativas (consolidado)

| # | Regra | Nível |
|---|---|---|
| C1 | Certificação MUST ser escopada a uma Versioned Identifier exata | MUST |
| C2 | Avanço de nível MUST satisfazer mínimo por dimensão, nunca média ponderada | MUST |
| C3 | L4 de um Agent MUST ter Certifier humano | MUST |
| C4 | MAJOR version MUST NOT herdar certificação anterior | MUST NOT |
| C5 | PATCH version MAY herdar certificação mediante atestação do Owner | MAY |
| C6 | Revocation MUST notificar todos os consumers (Kernel §2.7) | MUST |
| C7 | Nenhuma nova entidade de Domain Model MUST ser introduzida por este pipeline | MUST NOT (introduce) |
| C8 | Evidence não-reproduzível MUST NOT justificar L4 isoladamente | MUST NOT |

---

## 13. Exemplo

`core/skill.static-analysis.sql-injection-scan@2.1.0`: L1 automático na publicação (Verification); L2 após suite de testes funcionais aprovada por Reviewer (validade 9 meses, risco médio); L3 após Conformance ao Standard `core/standard.security.input-validation` verificada pelo Governance Area Steward de Security; L4 negado — Reproducibility Evidence marcada `false` (o test harness usa timestamp não determinístico) — gap reportado ao Owner, que corrige o harness e resubmete.

---

## 14. Validação Institucional Final

| Verificação cruzada | Resultado |
|---|---|
| Consistente com Kernel (Lifecycle não duplicado) | **PASS** |
| Consistente com Governance §11 (Certification), §13 (Compliance) | **PASS** — implementa integralmente o que já estava anunciado, não redefine |
| Consistente com Domain Model v1.1.0 | **PASS** — zero entidades novas |
| Consistente com Registry (Fase 3) | **PASS** — contrato de read-through respeitado nos dois sentidos |
| Exige RFC de emenda? | **Não** |
