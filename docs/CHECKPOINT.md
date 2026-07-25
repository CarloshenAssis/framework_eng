# Framework Eng — Checkpoint Institucional

*Atualizado em: 2026-07-25 · Branch: `claude/software-engineering-framework-fatdob`*

> Este arquivo é um **ponto de controle**, não um documento arquitetural. Ele existe para que o estado do projeto sobreviva ao encerramento de qualquer sessão de conversa. Substitui integralmente a versão anterior deste checkpoint (que dizia "nenhum conteúdo real existe ainda" — isso deixou de ser verdade a partir dos ciclos de referência descritos na Seção 3).

---

## 1. Onde estamos

A infraestrutura institucional está **completa**: 20 documentos de arquitetura ratificados, do Constitution ao Packaging & Distribution, sem nenhuma RFC além de RFC-DM-001. Sobre essa base, já existem **6 ciclos de referência** de conteúdo real (Standards, Policies, Skills, Agent, Workflows, Organization, records de Certificação/RoleAssignment/Knowledge) — um piloto pequeno e deliberado, não uma biblioteca em volume, cujo objetivo foi validar cada peça da arquitetura sobre dado concreto antes de qualquer geração em escala.

Analogia atualizada: o sistema operacional está completo e **um programa de referência já roda nele**, ponta a ponta, com falhas e recuperação reais — mas a "loja de aplicativos" (biblioteca ampla de Standards/Skills/Agents/Workflows) ainda não existe.

---

## 2. Documentos de arquitetura ratificados (base normativa congelada)

| # | Documento | Papel institucional |
|---|---|---|
| 1 | Constitution | Princípios permanentes, hierarquia de decisões, regras imutáveis |
| 2 | Kernel Architecture | Component Contract, Lifecycle, Manifest, composição, interoperabilidade |
| 3 | Governance Architecture | Ownership, Stewardship, RFC Process, Admission, Audit, Risk, Exception |
| 4 | Domain Model v1.1.0 | 14 entidades fundamentais |
| 5 | RFC-DM-001 | Emenda: C1 (Knowledge/Knowledge Asset), C2 (Context Snapshot), C3 (`derives_from`), C4, H1, H3 |
| 6 | Identity & Namespace Architecture | Coordinate/Versioned/Instance Identifier, Namespaces, lineage |
| 7 | Registry & Discovery Architecture | Resolução/descoberta, Registry Entry, Redirect, Lineage Index |
| 8 | Validation & Certification Architecture | Verification/Testing/Validation/Certification distintos; L0–L4 |
| 9 | Composition Architecture | Assembly, Composition Slot, resolução de Providers |
| 10 | Workflow Architecture | Phase, Step, Gate, Branch, Compensation, Failure Policy |
| 11 | Execution Architecture | Scheduler, correlação via Context, Provenance Service |
| 12 | Standards Architecture v1.0.0 | Normative Requirement, Conformance Level, Strict/Partial Conformance |
| 13 | Policy Architecture v1.0.0 | Policy Binding, Scope, Effective Policy Set |
| 14 | Template Architecture v1.0.0 | Prompt/Input/Output Template, determinismo de expansão |
| 15 | Skill Architecture v1.0.0 | Skill = Operational Component puro |
| 16 | Observability Architecture v1.0.0 | Trace, Span, Provenance Chain, fecha Provenance Service |
| 17 | Agent Architecture v1.0.0 | RoleAssignment, Decision institucional, fecha H2 |
| 18 | Organization & Tenancy Architecture v1.0.0 | Organization como Component, Membership, isolamento |
| 19 | Testing Architecture v1.0.0 | Test Case, Test Run Report, Cobertura, Regressão |
| 20 | Packaging & Distribution Architecture v1.0.0 | Bundle, integridade em trânsito, exportação de métricas |

**Nota:** um rascunho de *Compliance Architecture* foi produzido no Bloco 4, mas **não foi ratificado** — permanece consumidor downstream, não congelado.

**Nenhuma RFC além de RFC-DM-001** foi necessária em dezenove documentos consecutivos de arquitetura — todos comprovaram formalmente, cada um, que a base é suficientemente expressiva.

---

## 3. Conteúdo real — 6 ciclos de referência

Ao contrário dos documentos da Seção 2 (arquitetura — regras de como qualquer coisa deve existir), o conteúdo abaixo é **instância real**, em `components/` e `records/`.

| Ciclo | O que instancia | O que prova |
|---|---|---|
| 1 | Standard, Policy, Skill (com Templates), Agent, Workflow — domínio "revisão de PR" | Cadeia completa Composition→Execution→Policy→Agent→Observability funciona |
| 2 | `org.acme-corp` (Organization real), Standard via `extends`, Policy escopada, Workflow com `Branch` | Isolamento multi-tenant, extensão normativa segura, acúmulo de Policies, roteamento condicional |
| 3 | Certificação L1→L4 completa da Skill do Ciclo 1 | `records/` como home de Decision Records; Registry lendo certificação por read-through |
| 4 | Correção de nomenclatura (`human-only-gate`→`high-risk-gate`); certificação L1→L4 do Agent; RoleAssignment formalizada | Erro real encontrado e corrigido (AG2: certificação deve preceder RoleAssignment); gate antes bloqueado agora resolve |
| 5 | 3 Skills novas (uma sem `templates[]`); Workflow com paralelismo, Retry, Compensação (Saga) | Todo o vocabulário de Workflow §4 exercitado — nada ficou só em prosa |
| 6 | `Knowledge` derivada de Executions do Ciclo 5; `Playbook` (Knowledge Asset) que a `codifies` | Fecha RFC-DM-001 C1 em conteúdo real; `derives_from` e `provenance()` sobre Knowledge, não só Artifact |

Ressalva presente em `components/README.md` e `records/README.md`: nenhuma Execution real foi processada por um runtime — os ciclos são ilustrativos, mostrando a forma exata que os artefatos assumiriam.

---

## 4. Princípios estruturais provados

- **Zero inflação de entidade** em 20 documentos de arquitetura + 6 ciclos de conteúdo.
- **Reuso em vez de criação**: *cycle detection* (Kernel §7) reaplicado 6+ vezes; padrão "Value Object escopado a Contract" usado por Capability/Phase/Step/NormativeRequirement/PolicyBinding/Template/TestCase; padrão "família nomeada de Decision" usado por CertificationGrant/RoleAssignment.
- **Correção sem reescrita silenciosa**: dois erros reais foram encontrados durante a instanciação de conteúdo (nome de fase prometendo garantia inexistente; ordem AG2 violada) — ambos corrigidos com nota explicando o quê, por quê, quando — nunca apagados.
- **Nenhuma RFC adicional** foi necessária em nenhum momento, nem durante a arquitetura, nem durante os 6 ciclos de conteúdo.

---

## 5. O que ainda NÃO existe

- Biblioteca ampla de Standards/Skills/Agents/Workflows (o piloto tem ~4 Skills, 1 Agent, 4 Workflows — não dezenas)
- `Compliance Architecture` ratificada
- `Standard Package` (`standard_kind: PACKAGE`) instanciado em conteúdo
- `Bundle` (export/import via Packaging & Distribution) demonstrado em conteúdo
- Query real de `Observability` (trace/provenance) mostrada como saída literal, não só narrada
- Domínio de conteúdo fora de "revisão de código/release" — todo o piloto é de um único domínio

---

## 6. Roadmap

```
[RATIFICADO — infraestrutura completa, 20 documentos]
Constitution → ... → Agent → Organization & Tenancy → Testing → Packaging & Distribution

[EM ANDAMENTO — piloto de conteúdo, 6 ciclos]
Reference Cycle 1-6 (components/, records/)

[CANDIDATOS PARA PRÓXIMOS CICLOS — sem ordem obrigatória]
- Standard Package (agregação via includes)
- Export/import de Bundle (Packaging & Distribution)
- Segundo domínio de conteúdo (fora de code-quality/release)
- Compliance Architecture (se decidido ratificar)

[DEPOIS — biblioteca em volume, só após decisão explícita de escalar]
Standards/Skills/Templates/Agents/Workflows reais em quantidade
Orchestrator (agente coordenador do ciclo completo)
```

---

## 7. Riscos e lacunas conhecidas

| Lacuna | Origem | Status |
|---|---|---|
| Armazenamento físico/escala do Provenance Service | Execution §14 | ✅ Fechada — Observability §6-§7 |
| Formato físico de serialização | Standards §3.2, Template §3.2 | ✅ Fechada — Packaging & Distribution §5 |
| Formato de exportação de métricas | Observability §17 | ✅ Fechada — Packaging & Distribution §9.4 |
| Modelo interno de Organization (billing, quotas) | Identity §10 | Deliberadamente deferida — `Resource & Quota Architecture` futura |
| Separação de funções, Role ocupado por Agent (caso geral) | Achado H2 | ✅ Fechada — Agent Architecture §7 (AG4/AG5) |
| Evidence para `EvaluationMethod=DYNAMIC` em escala | Standards §19 | ✅ Fechada — Testing Architecture |

**Risco psicológico** (mantido da versão anterior deste checkpoint, ainda vigente): tendência de introduzir conceitos que "parecem úteis" sem necessidade real. A disciplina de reuso — inclusive durante a instanciação de conteúdo, onde dois erros reais foram corrigidos em vez de mascarados — continua sendo o ativo mais valioso do projeto.

---

## 8. Estrutura do repositório

```
docs/                          arquitetura (índice — texto integral só no histórico da conversa)
  CHECKPOINT.md                 este arquivo
  reference-cycle-N-walkthrough.md   narrativa de cada ciclo de conteúdo (N=1..6)
components/                    Manifests reais de Component (Standard/Policy/Skill/Agent/Workflow/Organization/Playbook)
  core/                          namespace compartilhado
  org.acme-corp/                 namespace de tenant, filho de core/
records/                       Decision Records instanciados (Certification, RoleAssignment, Knowledge)
```

---

## 9. Ação pendente

O texto integral dos 20 documentos de arquitetura existe apenas no histórico desta conversa — este checkpoint continua sendo índice/status, não o conteúdo normativo completo. Transcrição para arquivos físicos (`docs/constitution.md` etc.) permanece em aberto, sob demanda explícita.

---

*Fim do checkpoint.*
