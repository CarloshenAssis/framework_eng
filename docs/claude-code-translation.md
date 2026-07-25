# Tradução para Claude Code — Caminho B

*Primeira peça de uma direção distinta do resto deste repositório. `docs/architecture/` e `components/`/`records/` são a especificação institucional e sua prova de consistência — este documento e `.claude/` são a tentativa de tornar uma fatia dela **executável** dentro do Claude Code, hoje, sem esperar por um runtime próprio do Framework (que nunca existiu — ver a ressalva já presente em `components/README.md`).*

---

## 1. O que este documento é e o que não é

**É:** um mapeamento honesto entre os conceitos institucionais do Framework (Component, Standard, Policy, Workflow, Certification) e os primitivos reais do Claude Code (Skill, Subagent, tool permissions, hooks) — dizendo explicitamente, para cada um, se a tradução é fiel, aproximada, ou impossível sem perda.

**Não é:** uma alegação de que o Framework institucional e o Claude Code são a mesma coisa em formatos diferentes. Não são. O Claude Code não tem Registry, não tem Certification, não tem Composition por Capability, não tem Compliance Assessment. Traduzir para Claude Code significa **abrir mão** de quase toda a camada de governança institucional (RFC, Ownership, ciclo de vida formal, conformidade verificável mecanicamente) em troca de algo que roda de verdade, hoje. §3 lista essa perda item a item, não apenas em geral.

---

## 2. O que foi traduzido nesta primeira fatia

Escolha deliberada: traduzir a fatia mais madura e mais validada do piloto — a cadeia de revisão de código do Ciclo 1, já certificada L1→L4 (Ciclo 3) e já exercitada por Compliance Assessment real (Ciclos 10-11) — em vez de tentar traduzir os seis Skills, o Agent e os cinco Workflows de uma vez. Estabelece o padrão; os demais podem seguir o mesmo molde depois, sob demanda.

| Componente institucional | Arquivo Claude Code | Tipo |
|---|---|---|
| `core/skill.static-analysis.code-review@1.0.0` | `.claude/skills/code-review/SKILL.md` | Skill |
| `core/agent.code-reviewer@1.0.0` | `.claude/agents/code-reviewer.md` | Subagent |

## 3. Mapeamento completo, conceito a conceito

| Conceito institucional | Equivalente no Claude Code | Fidelidade |
|---|---|---|
| `Skill` (Operational Component puro, Kernel Contract) | Skill (`.claude/skills/*/SKILL.md`) | **Boa.** Ambos são unidades de instrução invocável, sem estado próprio. Perde: Identity/Coordinate versionada, Certification, test_suite formal. |
| `Agent` (Component com autoridade decisória) | Subagent (`.claude/agents/*.md`) | **Boa como forma, fraca como garantia.** Isolamento de contexto e restrição de `tools` têm equivalente direto. AG4 (coautorização humana obrigatória acima de risco médio) e AG5 (proibição de autoaprovação) viram **instrução textual no prompt** — não há gate estrutural que impeça o agente de ignorá-las. Ver a nota no rodapé de `.claude/agents/code-reviewer.md`. |
| `Standard` (Normative Requirement, RFC 2119, Evidence Requirement) | Nenhum. Vira prosa dentro do Skill/Agent. | **Perda real.** Não existe no Claude Code um `MUST`/`SHOULD` verificável mecanicamente por serviço externo à própria leitura do agente. `nr.no-hardcoded-secrets` (MUST_NOT) virou uma instrução no SKILL.md — o Skill segue por bom senso, não por validação estrutural. Um `PreToolUse` hook rodando um scanner real (ex.: `gitleaks`, `trufflehog`) sobre o diff, antes do Skill rodar, seria a forma de recuperar parte dessa garantia mecanicamente — não implementado nesta fatia; candidato natural para a próxima. |
| `Policy` (Binding, Scope, `enforcement_mode: BLOCKING`) | Nenhum equivalente direto. `allowed-tools`/`disallowedTools` restringe *o quê* uma Skill/Agent pode fazer, nunca *quando* uma norma se aplica a um sujeito. | **Perda real.** Não há Effective Policy Set, não há resolução por Namespace, não há distinção STRICT/PARTIAL_ACCEPTABLE. O `enforcement_mode: BLOCKING` da Policy institucional (impede o dispatch) não tem análogo — o mais próximo é um hook que rejeita a chamada de ferramenta (exit code 2), o que é uma ideia adjacente, não a mesma coisa. |
| `Workflow` (Phase, Step, Gate, Branch, Compensation) | Nenhum primitivo dedicado. | **Perda estrutural, recuperada parcialmente por composição de prompt.** Em vez de uma terceira peça (um "orquestrador"), o Subagent `code-reviewer` foi desenhado para invocar a Skill `code-review` ele mesmo, como primeiro passo do seu próprio prompt — a sequência de duas fases do Workflow institucional (`phase.static-review` → `phase.decision-gate`) vira instrução de ordem dentro de um único agente, não dois Components declarativos coordenados por um Scheduler. Não há `GATE_APPROVAL` real (pausa estrutural aguardando aprovação humana antes de prosseguir) — apenas a instrução textual do passo 6 no Agent, que o modelo pode ignorar. Não há Retry, Compensação (Saga), nem paralelismo declarativo. |
| `Certification` (L0-L4, Evidence, janelas de validade) | Nenhum. | **Sem equivalente.** Um Skill/Agent do Claude Code não tem nível de confiança declarado nem histórico de certificação — existe ou não existe no diretório, ponto. |
| `Compliance` (Assessment, Conformance Claim, Binding Satisfaction, Drift, Waiver) | Nenhum. | **Sem equivalente.** Nenhuma verificação contínua, nenhum drift detectável, nenhuma Risk Acceptance formal. |
| `Registry & Discovery`, `Composition` (resolução por Capability) | Nenhum. Um Subagent que quer usar uma Skill a referencia pelo nome, fixo, no próprio prompt. | **Sem equivalente.** Não há resolução dinâmica "qual Skill satisfaz esta Capability com Certificação ≥ L2" — a referência é estática, decidida por quem escreveu o Agent. |
| `Observability` (`trace`, `provenance`, `query_events`) | Nenhum nativo equivalente para este conteúdo específico; Claude Code tem seu próprio sistema de logging/transcript, não relacionado. | **Sem equivalente para o domínio institucional.** O que o Ciclo 12 mostrou como saída literal não tem contrapartida aqui. |

---

## 4. O que isso significa na prática

Antes desta tradução: zero linhas deste Framework rodavam dentro do Claude Code — tudo era YAML ilustrativo, descrevendo a forma que artefatos assumiriam sob um runtime que nunca foi construído.

Depois desta tradução: `code-review` e `code-reviewer` são um Skill e um Subagent reais, no formato correto, prontos para serem descobertos por qualquer sessão do Claude Code aberta neste repositório. O que eles **fazem** é uma versão simplificada — sem Certification, sem Policy, sem Compliance — do que os Components institucionais equivalentes descrevem. O que eles **preservam** do original: os dois requisitos normativos que mais importavam (segredo é sempre bloqueante; decisão sempre cita evidência; nunca autoaprovação) sobreviveram à tradução como instrução explícita, não foram silenciosamente descartados.

## 5. Status de verificação — o que foi validado e o que não foi

- ✅ **Estrutural:** os dois arquivos têm frontmatter YAML bem formado (validado com `yaml.safe_load`), nos campos documentados pelo Claude Code atual (`name`, `description`, `allowed-tools`/`tools`, `model`), nos caminhos corretos (`.claude/skills/<nome>/SKILL.md`, `.claude/agents/<nome>.md`).
- ❌ **Funcional, nesta sessão:** tentei invocar `code-reviewer` via a ferramenta Agent, com um diff de teste contendo uma chave de API exposta e sem teste correspondente — exatamente o caso que deveria produzir `REQUEST_CHANGES` com achado `blocker`. A chamada falhou: `Agent type 'code-reviewer' not found. Available agents: claude, claude-code-guide, Explore, general-purpose, Plan, statusline-setup`. A lista de agentes desta sessão foi fixada no início da conversa (antes destes arquivos existirem) e não é recarregada dinamicamente. **Isto não é evidência de que o arquivo está errado** — é uma limitação conhecida de testar dentro da mesma sessão que criou o arquivo. Verificação funcional real exige uma sessão nova do Claude Code aberta neste repositório (ou reinício desta).
- **Não afirmo que o comportamento descrito no prompt do Agent (recusar autoaprovação, exigir rationale com evidência, sinalizar risco alto) foi observado em execução real — apenas que está escrito e é estruturalmente válido.**

## 6. Próximos passos naturais (não iniciados)

- Verificar em sessão nova se `code-reviewer` e `code-review` são de fato descobertos e invocados corretamente.
- Se confirmado, estender o mesmo padrão aos demais Skills/Agent do piloto (`skill.security.dependency-audit`, `skill.release.deploy`, `skill.documentation.*`, os Workflows de release e documentação).
- Considerar um `PreToolUse` hook real (scanner de segredo executável) para recuperar mecanicamente parte da garantia que `nr.no-hardcoded-secrets` perdeu ao virar só instrução textual — candidato mais valioso da lista, porque é o único NR `MUST_NOT` desta fatia.
