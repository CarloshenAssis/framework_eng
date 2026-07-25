# Framework Eng — Checkpoint Institucional

*Atualizado em: 2026-07-25 · Branch: `claude/software-engineering-framework-fatdob`*

> Este arquivo é um **ponto de controle**, não um documento arquitetural. Ele existe para que o estado do projeto sobreviva ao encerramento de qualquer sessão de conversa. Substitui integralmente a versão anterior deste checkpoint (que dizia "nenhum conteúdo real existe ainda" — isso deixou de ser verdade a partir dos ciclos de referência descritos na Seção 3; que dizia que o texto integral da arquitetura só existia no histórico da conversa — isso deixou de ser verdade com a persistência descrita na Seção 10; e que não mencionava nenhuma tradução executável — isso deixou de ser verdade com o Caminho B, Seção 4).

---

## 1. Onde estamos

A infraestrutura institucional está **completa**: 21 documentos de arquitetura ratificados (Compliance Architecture em v1.1.0 — ver nota da Seção 2), do Constitution ao Compliance Architecture, sem nenhuma RFC além de RFC-DM-001. Sobre essa base, existem **12 ciclos de referência** de conteúdo institucional ilustrativo (Seção 3) **e**, como frente distinta iniciada nesta sessão, uma primeira tradução real e executável para o Claude Code (Seção 4) — a primeira coisa neste repositório que roda como Skill/Subagent de verdade, fora do universo de especificação.

Analogia atualizada: o sistema operacional está completo, um programa de referência roda nele ponta a ponta em simulação, **e agora existe também um primeiro programa real, compilado para uma plataforma concreta (Claude Code)** — menor e mais simples que o programa de referência institucional, porque a plataforma concreta não tem todos os serviços que o sistema operacional oferece.

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
| 21 | Compliance Architecture **v1.1.0** | Compliance Assessment, Conformance Claim, Binding Satisfaction, Drift, Waiver/Risk Acceptance |

**Nota:** o rascunho de *Compliance Architecture* produzido no Bloco 4 foi **ratificado** nesta sessão como documento 21 (v1.0.0), após validação contra os sete documentos ratificados depois dele (Template, Skill, Observability, Agent, Organization & Tenancy, Testing, Packaging & Distribution) e contra a versão final de Standards/Policy. Essa validação encontrou e fechou uma lacuna real: `PolicyBinding.conformance_mode` não existia quando o rascunho foi escrito, e a versão ratificada introduziu `Binding Satisfaction` (§4.4) para determinar corretamente se uma Partial Conformance satisfaz um Binding `STRICT`.

Uma segunda lacuna, menor, foi encontrada logo em seguida ao tentar instanciar Risk Acceptance com dado real (Ciclo 11): a v1.0.0 nunca definia o efeito de um Waiver/Risk Acceptance de nível NR sobre `BindingSatisfaction` no caso Non-Conformance. Corrigida como **emenda v1.1.0** (MINOR — apenas aditiva), antes do Ciclo 11 ser escrito, não durante. Ver `docs/architecture/21-compliance-architecture.md`, notas de topo.

**Nenhuma RFC além de RFC-DM-001** foi necessária em vinte documentos consecutivos de arquitetura (01-20) — todos comprovaram formalmente, cada um, que a base é suficientemente expressiva. O único documento a receber uma emenda depois de ratificado foi o próprio Compliance Architecture (v1.0.0→v1.1.0, MINOR, aditiva — não uma RFC formal como RFC-DM-001, proporcional ao tamanho real da lacuna).

---

## 3. Conteúdo institucional real — 12 ciclos de referência

Ao contrário dos documentos da Seção 2 (arquitetura — regras de como qualquer coisa deve existir), o conteúdo abaixo é **instância real**, em `components/`, `records/` e `bundles/` — mas ainda ilustrativa quanto a runtime (ver ressalva abaixo). Distinto do Caminho B (Seção 4), que roda de verdade, com escopo menor.

| Ciclo | O que instancia | O que prova |
|---|---|---|
| 1 | Standard, Policy, Skill (com Templates), Agent, Workflow — domínio "revisão de PR" | Cadeia completa Composition→Execution→Policy→Agent→Observability funciona |
| 2 | `org.acme-corp` (Organization real), Standard via `extends`, Policy escopada, Workflow com `Branch` | Isolamento multi-tenant, extensão normativa segura, acúmulo de Policies, roteamento condicional |
| 3 | Certificação L1→L4 completa da Skill do Ciclo 1 | `records/` como home de Decision Records; Registry lendo certificação por read-through |
| 4 | Correção de nomenclatura (`human-only-gate`→`high-risk-gate`); certificação L1→L4 do Agent; RoleAssignment formalizada | Erro real encontrado e corrigido (AG2: certificação deve preceder RoleAssignment); gate antes bloqueado agora resolve |
| 5 | 3 Skills novas (uma sem `templates[]`); Workflow com paralelismo, Retry, Compensação (Saga) | Todo o vocabulário de Workflow §4 exercitado — nada ficou só em prosa |
| 6 | `Knowledge` derivada de Executions do Ciclo 5; `Playbook` (Knowledge Asset) que a `codifies` | Fecha RFC-DM-001 C1 em conteúdo real; `derives_from` e `provenance()` sobre Knowledge, não só Artifact |
| 7 | Segundo domínio (documentação de API); Workflow sem Agent/Branch/Decision; primeiro uso de `GATE_AUTO` | Arquitetura não impõe complexidade decisória onde não é necessária; vinculação normativa local (`standards_bound`) exercitada sozinha, sem Policy |
| 8 | `Bundle` — exporta o Workflow do Ciclo 1 com fecho de dependências via Composition, verifica digest, narra importação em deployment separado | Fecha o único documento de arquitetura (Packaging & Distribution) sem nenhum conteúdo até então; expõe deliberadamente que Standards/Policies não viajam no fecho de Composition |
| 9 | `Standard Package` (`standard_kind: PACKAGE`) agregando os dois Standards de `core/` via `includes` | Fecha o último mecanismo nomeado de arquitetura sem exemplo real (dos 20 documentos daquele momento) |
| 10 | `Compliance Assessment` real (RUNTIME) formalizando o dispatch do Ciclo 1; nova Policy `extended-pilot` (nível EXTENDED, `conformance_mode: PARTIAL_ACCEPTABLE`, `overrides`); `ConformanceClaim{PARTIAL}` real; `BindingSatisfaction` nos três ramos (`CLAIM_STRICT`, `CLAIM_PARTIAL_ACCEPTED`, `CLAIM_PARTIAL_REJECTED`); Waiver de Binding | Fecha o 21º documento (Compliance Architecture) sem nenhum conteúdo até então; exercita com dado real a lacuna encontrada e corrigida durante a ratificação (`conformance_mode` determinando satisfação de Binding) |
| 11 | `Compliance Drift` real (`detect_drift` sobre os dois Reports do Ciclo 10, sem nova Execution); primeira Non-Conformance genuína do piloto; primeira `Risk Acceptance` real (nível NR, com `risk_classification`) | Fecha as duas últimas peças nomeadas de Compliance Architecture sem exemplo real; expôs e motivou a emenda v1.1.0 (Waiver/Risk Acceptance de nível NR propagando para `BindingSatisfaction` no caso Non-Conformance) |
| 12 | Saída literal de `trace()`, `provenance()` e `query_events()` (Observability Query Service, §7.1) sobre dado já produzido nos Ciclos 10-11 — nenhum `components/`/`records/` novo, de propósito (OB2 proíbe persistir Trace/Span/Provenance Chain) | Fecha a última lacuna registrada que não era mecanismo sem exemplo, mas consulta narrada em vez de mostrada; `provenance()` liga mecanicamente a Evidence do Ciclo 11 à Risk Acceptance que a resolveu |

Ressalva presente em `components/README.md` e `records/README.md`: nenhuma Execution real foi processada por um runtime institucional próprio — os ciclos são ilustrativos, mostrando a forma exata que os artefatos assumiriam. Essa ressalva **não se aplica** ao Caminho B (Seção 4), que roda sob o runtime real do Claude Code, com escopo deliberadamente menor.

**Marco atingido no Ciclo 9** (temporariamente reaberto pela ratificação de Compliance como 21º documento, fechado de novo pelo Ciclo 10, refinado pelo Ciclo 11): todos os 21 documentos e todo mecanismo nomeado de arquitetura ratificados têm, agora, pelo menos um exemplo real exercitando-os — incluindo Drift e Risk Acceptance, as duas últimas peças de Compliance Architecture ainda em prosa depois do Ciclo 10. O Ciclo 12 fecha uma lacuna de natureza diferente: não um mecanismo sem exemplo, mas uma consulta (`Observability Query Service`) sempre narrada, nunca mostrada como dado literal. Ver `docs/reference-cycle-10-walkthrough.md` a `docs/reference-cycle-12-walkthrough.md`.

---

## 4. Caminho B — tradução executável para Claude Code

Frente nova, iniciada nesta sessão, distinta em natureza dos 12 ciclos da Seção 3: em vez de mais uma instância institucional ilustrativa, uma **tradução real** de uma fatia do piloto para os primitivos nativos do Claude Code — a primeira coisa neste repositório que uma sessão do Claude Code descobre e pode efetivamente invocar.

| Traduzido | De | Para |
|---|---|---|
| Skill de análise | `core/skill.static-analysis.code-review@1.0.0` | `.claude/skills/code-review/SKILL.md` |
| Agent de decisão | `core/agent.code-reviewer@1.0.0` | `.claude/agents/code-reviewer.md` |

Mapeamento completo, conceito a conceito (o que traduz bem, o que vira instrução textual, o que não tem equivalente) em `docs/claude-code-translation.md` — inclui, sem suavizar, que **Standard, Policy, Workflow, Certification e Compliance não têm primitivo nativo no Claude Code** e que AG4/AG5 (coautorização humana, proibição de autoaprovação) sobrevivem apenas como instrução no prompt, não como gate estrutural.

**Status de verificação:** frontmatter YAML dos dois arquivos validado estruturalmente (`yaml.safe_load`, campos corretos, caminhos corretos). Tentativa de invocação funcional real, dentro desta mesma sessão, **falhou** — não porque os arquivos estejam errados, mas porque a lista de agentes desta sessão foi fixada no início da conversa, antes destes arquivos existirem, e não recarrega dinamicamente. Verificação funcional real requer uma sessão nova do Claude Code aberta neste repositório. Isto está registrado explicitamente em `docs/claude-code-translation.md` §5 — nenhuma alegação de "funciona" sem a ressalva.

**Por que só esta fatia:** a mais madura e mais validada do piloto — certificada L1→L4 (Ciclo 3), já exercitada por Compliance Assessment real (Ciclos 10-11). Estabelece o padrão de tradução; os outros cinco Skills, os quatro Workflows restantes e a Organization ficam como candidato explícito (Seção 7), não como trabalho abandonado.

---

## 5. Princípios estruturais provados

- **Zero inflação de entidade** em 21 documentos de arquitetura + 12 ciclos de conteúdo institucional.
- **Reuso em vez de criação**: *cycle detection* (Kernel §7) reaplicado 6+ vezes; padrão "Value Object escopado a Contract" usado por Capability/Phase/Step/NormativeRequirement/PolicyBinding/Template/TestCase; padrão "família nomeada de Decision" usado por CertificationGrant/RoleAssignment/Waiver/Risk Acceptance; os dois caminhos de vinculação normativa (Policy derivada vs. `standards_bound` local) comprovadamente intercambiáveis, não um substituindo o outro por acidente — inclusive quando entram em níveis diferentes e precisam de união não trivial (Ciclo 10).
- **Correção sem reescrita silenciosa**: erros reais foram encontrados durante a instanciação de conteúdo (nome de fase prometendo garantia inexistente; ordem AG2 violada) e, duas vezes, durante a própria ratificação/instanciação de Compliance Architecture na mesma sessão (`conformance_mode` ausente do rascunho; depois, Waiver/Risk Acceptance de nível NR sem efeito sobre Binding) — todos corrigidos com nota explicando o quê, por quê, quando, nunca apagados.
- **Fronteiras arquiteturais expostas, não escondidas**: o Ciclo 8 mostra deliberadamente o que acontece quando alguém ignora uma fronteira documentada (fecho de Composition ≠ vinculação normativa) em vez de fingir que o problema não existe; o Caminho B (Seção 4) faz o mesmo com o que se perde ao sair da especificação institucional para um runtime real.
- **Nenhuma RFC adicional** foi necessária em nenhum momento, nem durante a arquitetura, nem durante os 12 ciclos de conteúdo — a única emenda em qualquer documento ratificado, em toda a sessão, foi a v1.1.0 de Compliance, MINOR e puramente aditiva.
- **Regras normativas aplicadas até na forma dos próprios registros do piloto**: o Ciclo 12 deliberadamente não criou nenhum arquivo em `records/` porque OB2 (Observability) proíbe persistir exatamente o tipo de dado que ele produz.
- **Alegação de "funciona" sempre acompanhada de como foi verificado**: o Caminho B distingue explicitamente validação estrutural (feita) de validação funcional (não feita nesta sessão, com o motivo exato registrado) — mesma disciplina de nunca superestimar o que foi provado, agora aplicada a software que roda de verdade, não só a YAML ilustrativo.

---

## 6. O que ainda NÃO existe

- Biblioteca ampla de Standards/Skills/Agents/Workflows institucionais (o piloto tem ~6 Skills, 1 Agent, 5 Workflows, 6 Standards, 4 Policies — não dezenas)
- Terceiro domínio de conteúdo institucional (os dois existentes são code-quality/release e documentação de API)
- `debug()`, `replay()`, `export_metrics()` — as três operações do Observability Query Service que o Ciclo 12 não exercitou
- Tradução Claude Code dos cinco Skills/quatro Workflows restantes do piloto (Seção 4 traduziu só a cadeia do Ciclo 1)
- Verificação funcional real (sessão nova) de que `code-review`/`code-reviewer` são descobertos e invocados corretamente pelo Claude Code
- Um hook `PreToolUse` real (scanner de segredo executável) para recuperar mecanicamente a garantia que `nr.no-hardcoded-secrets` perdeu ao virar só instrução textual na tradução

**Fechado nesta sessão:** ratificação de `Compliance Architecture` como documento 21; Ciclos 10-12 (Assessment, Conformance Claim, Binding Satisfaction, Drift, Risk Acceptance, consultas literais de Observability); emenda v1.1.0; e a abertura do Caminho B com a primeira tradução real e executável. Não há mais documento de arquitetura em rascunho não ratificado, nem mecanismo nomeado sem exemplo real, nem consulta central de Observability apenas narrada. O que resta em aberto é decisão de escala (biblioteca institucional em volume), de escopo (terceiro domínio, resto do Caminho B), ou de verificação (sessão nova para confirmar o Caminho B em runtime real) — não validação arquitetural de nenhum mecanismo central.

---

## 7. Roadmap

```
[RATIFICADO — infraestrutura completa, 21 documentos]
Constitution → ... → Testing → Packaging & Distribution → Compliance Architecture (v1.1.0)

[CONCLUÍDO — piloto institucional, 12 ciclos — todo mecanismo nomeado exercitado nos 21 documentos,
 e as três formas centrais de consulta de Observability mostradas como saída literal]
Reference Cycle 1-12 (components/, records/, bundles/)

[INICIADO — Caminho B, tradução executável para Claude Code]
code-review (Skill) + code-reviewer (Agent)          .claude/skills/, .claude/agents/
  ├── validado estruturalmente
  └── validação funcional em sessão nova              [PENDENTE]

[CANDIDATOS PARA CONTINUAÇÃO FUTURA — sem ordem obrigatória, nenhum bloqueante]
- Verificar o Caminho B em sessão nova; se confirmado, estender aos 5 Skills/4 Workflows restantes
- Hook PreToolUse real para nr.no-hardcoded-secrets (recupera garantia mecânica perdida na tradução)
- Terceiro domínio de conteúdo institucional
- `debug()`/`replay()`/`export_metrics()` de Observability como saída literal

[DEPOIS — biblioteca institucional em volume, só após decisão explícita de escalar]
Standards/Skills/Templates/Agents/Workflows reais em quantidade
Orchestrator (agente coordenador do ciclo completo)
```

---

## 8. Riscos e lacunas conhecidas

| Lacuna | Origem | Status |
|---|---|---|
| Armazenamento físico/escala do Provenance Service | Execution §14 | ✅ Fechada — Observability §6-§7 |
| Formato físico de serialização | Standards §3.2, Template §3.2 | ✅ Fechada — Packaging & Distribution §5 |
| Formato de exportação de métricas | Observability §17 | ✅ Fechada — Packaging & Distribution §9.4 |
| Modelo interno de Organization (billing, quotas) | Identity §10 | Deliberadamente deferida — `Resource & Quota Architecture` futura |
| Separação de funções, Role ocupado por Agent (caso geral) | Achado H2 | ✅ Fechada — Agent Architecture §7 (AG4/AG5) |
| Evidence para `EvaluationMethod=DYNAMIC` em escala | Standards §19 | ✅ Fechada — Testing Architecture |
| Mecanismo de verificação contínua de conformidade (Compliance) | Governance §13 | ✅ Fechada — Compliance Architecture (documento 21) |
| AG4/AG5 sem gate estrutural equivalente no Claude Code | Caminho B (Seção 4) | Aberta, registrada — instrução textual apenas, sem mecanismo de enforcement |
| `nr.no-hardcoded-secrets` sem verificação mecânica no Claude Code | Caminho B (Seção 4) | Aberta, registrada — candidato: hook `PreToolUse` real (Seção 7) |

**Risco psicológico** (mantido da versão anterior deste checkpoint, ainda vigente): tendência de introduzir conceitos que "parecem úteis" sem necessidade real. A disciplina de reuso continua sendo o ativo mais valioso do projeto — agora testada também contra a tentação oposta, no Caminho B: superestimar o quanto uma tradução simplificada preserva das garantias institucionais originais.

---

## 9. Estrutura do repositório

```
docs/
  CHECKPOINT.md                 este arquivo
  architecture/                  texto integral dos 21 documentos ratificados (ver Seção 2)
    01-constitution.md .. 21-compliance-architecture.md
  reference-cycle-N-walkthrough.md   narrativa de cada ciclo de conteúdo institucional (N=1..12)
  claude-code-translation.md    mapeamento completo do Caminho B (Seção 4) — o que traduz, o que se perde
components/                    Manifests reais de Component institucional (Standard/Policy/Skill/Agent/Workflow/Organization/Playbook)
  core/                          namespace compartilhado
  org.acme-corp/                 namespace de tenant, filho de core/
records/                       Decision Records e Artifacts institucionais (Certification, RoleAssignment,
                                 Knowledge, Compliance — ver records/README.md)
bundles/                       Bundle — codificação física de transporte (Packaging & Distribution), não é entidade
.claude/                       Caminho B — Skills e Agents REAIS, descobertos pelo Claude Code
  skills/code-review/SKILL.md    tradução de core/skill.static-analysis.code-review@1.0.0
  agents/code-reviewer.md        tradução de core/agent.code-reviewer@1.0.0
```

---

## 10. Ação pendente

**Fechada (persistência):** o texto integral dos 21 documentos de arquitetura está persistido em `docs/architecture/01-*.md` a `21-*.md` — deixou de existir apenas no histórico da conversa. Standards e Policy (`12`, `13`) usam a versão ratificada v1.0.0 que substitui integralmente o rascunho do Bloco 4; Compliance Architecture (`21`) foi ratificada nesta sessão, validada contra a base completa (Seção 2, nota).

**Aberta (verificação funcional):** o Caminho B (Seção 4) precisa ser confirmado em uma sessão nova do Claude Code — `code-review` e `code-reviewer` foram validados apenas estruturalmente nesta sessão, não invocados com sucesso (motivo registrado em `docs/claude-code-translation.md` §5, não é falha do arquivo).

O que resta em aberto além disso é decisão de escala ou escopo (Seção 7), não recuperação de conteúdo já produzido nem dúvida sobre a arquitetura.

---

*Fim do checkpoint.*
