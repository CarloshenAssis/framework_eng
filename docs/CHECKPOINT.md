# Framework Eng — Checkpoint Institucional

*Registrado em: 2026-07-25 · Branch: `claude/software-engineering-framework-fatdob`*

> Este arquivo é um **ponto de controle**, não um documento arquitetural. Ele existe para que o estado do projeto sobreviva ao encerramento de qualquer sessão de conversa — todo o conteúdo integral dos documentos abaixo foi produzido ao longo da conversa, mas **ainda não foi transcrito para arquivos físicos no repositório** (ver "Ação pendente" ao final).

---

## 1. Onde estamos

O Framework Eng está na fase de **infraestrutura institucional (kernel-layer)**. Nenhum conteúdo de produto (Skills reais, Standards reais, Agentes reais, Templates reais, Workflows reais) foi criado ainda — o que existe é a **especificação normativa completa de como esse conteúdo deverá existir, ser validado, versionado, certificado e descoberto**.

Analogia útil: construímos um sistema operacional completo (kernel, registry, scheduler, sistema de arquivos, controle de versão, política de segurança) e ainda não instalamos nenhum programa nele.

---

## 2. Documentos ratificados (base normativa congelada)

Ordem de dependência — cada um assume os anteriores como imutáveis e reutiliza-os, nunca os altera.

| # | Documento | Papel institucional | Status |
|---|---|---|---|
| 1 | **Constitution** | Princípios permanentes; missão, valores, hierarquia de decisões, regras imutáveis | ✅ Ratificado |
| 2 | **Kernel Architecture** | Component Contract, Lifecycle (Draft→...→Removed), Manifest, dependências, validação, composição, interoperabilidade | ✅ Ratificado |
| 3 | **Governance Architecture** | Ownership, Stewardship, RFC Process, Admission, Certification, Audit, Risk, Exception, Conflict Resolution | ✅ Ratificado |
| 4 | **Domain Model v1.1.0** | As 14 entidades fundamentais (Component, Manifest, Execution, Artifact, Knowledge, Decision, Role, Metric...) | ✅ Ratificado (v1.0.0 → v1.1.0) |
| 5 | **RFC-DM-001** | Emenda ao Domain Model: resolve C1 (colisão Knowledge/Knowledge Asset), C2 (Context Snapshot), C3 (`derives_from`), C4 (Framework/Domain indefinidos), H1 (overload "Domain"), H3 (cardinalidade Component:Manifest) | ✅ Ratificado |
| 6 | **Identity & Namespace Architecture** | Coordinate/Versioned/Instance Identifier, ULID, árvore de Namespaces, resolução, lineage | ✅ Ratificado |
| 7 | **Registry & Discovery Architecture** | Autoridade de resolução/descoberta; Registry Entry, Alias, Redirect, Lineage Index | ✅ Ratificado |
| 8 | **Validation & Certification Architecture** | Verification/Testing/Validation/Conformance/Compliance/Certification distintos; níveis L0–L4 | ✅ Ratificado |
| 9 | **Composition Architecture** | Assembly, Composition Slot, resolução de Providers, compatibilidade | ✅ Ratificado |
| 10 | **Workflow Architecture** | Phase, Step, Gate (automático/aprovação), Branch, Join, Compensation, Failure Policy | ✅ Ratificado |
| 11 | **Execution Architecture** | Execution Plan, Scheduler, correlação via Context (`orchestration_id`), Provenance Service (contrato conceitual) | ✅ Ratificado |
| 12 | **Standards Architecture** | Normative Requirement, Requirement Identifier, Conformance Level, Strict/Partial Conformance, Standard Packages | ✅ Ratificado v1.0.0 |
| 13 | **Policy Architecture** | Policy Binding, Scope, Effective Policy Set, resolução de conflito, `applies_at` | ✅ Ratificado v1.0.0 |
| 14 | **Template Architecture** | Prompt/Input/Output Template como Value Object; determinismo de expansão | ✅ Ratificado v1.0.0 |
| 15 | **Skill Architecture** | Skill = Operational Component puro; fecha certificação de Skill (Validation §7) | ✅ Ratificado v1.0.0 |
| 16 | **Observability Architecture** | Trace, Span, Provenance Chain (Value Objects efêmeros); fecha Provenance Service (Execution §14) | ✅ Ratificado v1.0.0 |

**Nota:** um rascunho de *Compliance Architecture* foi produzido no Bloco 4, mas **não foi ratificado** como base normativa — permanece explicitamente como consumidor downstream, não congelado.

---

## 3. Princípios estruturais provados ao longo de 16 documentos

- **Zero inflação de entidade**: nenhum documento após o Domain Model introduziu uma entidade nova sem RFC formal — apenas RFC-DM-001 alterou o Domain Model (uma única vez, no início).
- **Reuso em vez de criação**: mecanismos como *cycle detection* (Kernel §7) foram reaplicados no mínimo 6 vezes (dependências de Component, `derives_from`, grafo de Workflow, grafo de Composition, `extends/includes` de Standards, cadeia de `overrides` de Policy, herança de Templates).
- **Distinção Entity vs. Value Object (DDD)** aplicada consistentemente: Component/Execution/Artifact/Knowledge/Decision/Role têm identidade própria; Capability/Phase/Step/NormativeRequirement/PolicyBinding/Template/Trace/Span são Value Objects sem identidade, escopados ao Contract que os contém.
- **Separação de responsabilidade normativa**: Standard define critério (nunca contexto) · Policy define aplicabilidade (nunca critério) · Compliance avalia continuamente (não ratificado) · Certification atesta pontualmente · Observability apenas consulta, nunca decide ou executa.
- **Nenhuma RFC adicional** foi necessária desde RFC-DM-001 — dez documentos consecutivos (Composition até Observability) provaram formalmente, cada um, que a base é suficientemente expressiva.

---

## 4. O que NÃO existe ainda

- Nenhuma Skill real (DDD, REST, PostgreSQL, LGPD...)
- Nenhum Standard real (coding-standard, security-standard...)
- Nenhum Agente (Discovery Agent, Product Manager, Architect...)
- Nenhum Template real (PRD, ADR, User Story...)
- Nenhum Workflow real (SaaS, GovTech, HealthTech...)
- **Agent Architecture** — o último documento de infraestrutura pendente (Skill *faz*; Agent *decide*)

---

## 5. Roadmap

```
[RATIFICADO — infraestrutura]
Constitution → Kernel → Governance → Domain Model v1.1 (RFC-DM-001) →
Identity & Namespace → Registry & Discovery → Validation & Certification →
Composition → Workflow → Execution → Standards → Policy →
Template → Skill → Observability

[PRÓXIMO — fecha a infraestrutura]
17. Agent Architecture           ← decide vs. executa; fecha H2 (separação de funções) no caso geral
18. Organization & Tenancy Architecture   ← preenche slot já reservado (Identity §8/§10)
19. Testing Architecture         ← desbloqueado por Observability (trace/debug/query_events)
20. Packaging & Distribution Architecture

[DEPOIS — camada de conteúdo, só começa com infraestrutura fechada]
21. Standards reais (biblioteca)
22. Skills reais (biblioteca)
23. Templates reais (biblioteca)
24. Agentes reais (biblioteca)
25. Workflows reais (biblioteca)
26. Orchestrator (agente coordenador de todo o ciclo)
```

---

## 6. Riscos e lacunas abertas (`[LACUNA proposital]` declaradas)

| Lacuna | Origem | Endereçada por |
|---|---|---|
| Armazenamento físico/escala do Provenance Service | Execution §14 | ✅ Fechada por Observability §6-§7 |
| Formato físico de serialização (bytes, encoding) | Standards §3.2, Template §3.2 | Pendente — Packaging & Distribution |
| Formato de exportação de métricas (wire format) | Observability §17 | Pendente — Packaging & Distribution |
| Modelo interno de Organization (billing, membership, quotas) | Identity §10, Policy §3.2 | Pendente — Organization & Tenancy |
| Evidence para `EvaluationMethod = DYNAMIC` em escala | Standards §19, Skill §17 | Pendente — Testing Architecture |
| Separação de funções para Role ocupado por Agent (caso geral, além de L4) | Achado H2, parcialmente resolvido em Validation & Certification §5 | Pendente — **Agent Architecture** |

**Risco psicológico identificado e aceito como vigilância contínua:** tendência de introduzir conceitos "que parecem úteis" (Memory Manager, Prompt Manager, Runtime Engine, Agent Controller) sem necessidade real. A disciplina de reuso mantida até aqui é o ativo mais valioso do projeto — deve ser preservada com o mesmo rigor em Agent Architecture.

---

## 7. Ação pendente

O texto integral dos 16 documentos existe apenas no histórico desta conversa. Este checkpoint registra **status e índice**, não o conteúdo normativo completo. Transcrição dos documentos para arquivos físicos (`docs/constitution.md`, `docs/kernel-architecture.md`, etc.) permanece uma tarefa em aberto, a ser feita sob demanda explícita.

---

*Fim do checkpoint.*
