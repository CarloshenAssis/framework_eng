# Tradução para Claude Code — Caminho B

*Primeira peça de uma direção distinta do resto deste repositório. `docs/architecture/` e `components/`/`records/` são a especificação institucional e sua prova de consistência — este documento e `.claude/` são a tentativa de tornar uma fatia dela **executável** dentro do Claude Code, hoje, sem esperar por um runtime próprio do Framework (que nunca existiu — ver a ressalva já presente em `components/README.md`).*

---

## 1. O que este documento é e o que não é

**É:** um mapeamento honesto entre os conceitos institucionais do Framework (Component, Standard, Policy, Workflow, Certification) e os primitivos reais do Claude Code (Skill, Subagent, tool permissions, hooks) — dizendo explicitamente, para cada um, se a tradução é fiel, aproximada, ou impossível sem perda.

**Não é:** uma alegação de que o Framework institucional e o Claude Code são a mesma coisa em formatos diferentes. Não são. O Claude Code não tem Registry, não tem Certification, não tem Composition por Capability, não tem Compliance Assessment. Traduzir para Claude Code significa **abrir mão** de quase toda a camada de governança institucional (RFC, Ownership, ciclo de vida formal, conformidade verificável mecanicamente) em troca de algo que roda de verdade, hoje. §3 lista essa perda item a item, não apenas em geral.

---

## 2. O que foi traduzido nesta primeira fatia

Escolha deliberada: traduzir a fatia mais madura e mais validada do piloto — a cadeia de revisão de código do Ciclo 1, já certificada L1→L4 (Ciclo 3) e já exercitada por Compliance Assessment real (Ciclos 10-11) — mais uma segunda Skill standalone (`dependency-audit`), em vez de tentar traduzir os seis Skills, o Agent e os cinco Workflows de uma vez. Estabelece o padrão; os demais podem seguir o mesmo molde depois, sob demanda.

| Componente institucional | Arquivo Claude Code | Tipo |
|---|---|---|
| `core/skill.static-analysis.code-review@1.0.0` | `.claude/skills/code-review/SKILL.md` | Skill |
| `core/agent.code-reviewer@1.0.0` | `.claude/agents/code-reviewer.md` | Subagent |
| `core/skill.security.dependency-audit@1.0.0` | `.claude/skills/dependency-audit/SKILL.md` | Skill |

## 3. Mapeamento completo, conceito a conceito

| Conceito institucional | Equivalente no Claude Code | Fidelidade |
|---|---|---|
| `Skill` (Operational Component puro, Kernel Contract) | Skill (`.claude/skills/*/SKILL.md`) | **Boa.** Ambos são unidades de instrução invocável, sem estado próprio. Perde: Identity/Coordinate versionada, Certification, test_suite formal. |
| `Agent` (Component com autoridade decisória) | Subagent (`.claude/agents/*.md`) | **Boa como forma, fraca como garantia.** Isolamento de contexto e restrição de `tools` têm equivalente direto. AG4 (coautorização humana obrigatória acima de risco médio) e AG5 (proibição de autoaprovação) viram **instrução textual no prompt** — não há gate estrutural que impeça o agente de ignorá-las. Ver a nota no rodapé de `.claude/agents/code-reviewer.md`. |
| `Standard` (Normative Requirement, RFC 2119, Evidence Requirement) | Nenhum primitivo dedicado; `nr.no-hardcoded-secrets` especificamente recuperou uma barreira mecânica parcial via `PreToolUse` hook (`.claude/hooks/check-no-secrets.sh` + `.claude/settings.json`) — ver §7. | **Perda real, parcialmente recuperada para um único NR.** Não existe no Claude Code um `MUST`/`SHOULD` verificável mecanicamente por serviço externo de forma geral. Para este NR específico, o hook scaneia o diff staged de um `git commit` contra um conjunto pequeno de padrões de segredo, independente de o modelo ter seguido a instrução textual da Skill — mas continua sem status de verificação em runtime real dentro desta sessão (§7). Os demais NRs (ex.: `nr.test-coverage-present`) permanecem só prosa. |
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

- ✅ **Estrutural (todos):** os três arquivos têm frontmatter YAML bem formado (validado com `yaml.safe_load`), nos campos documentados pelo Claude Code atual, nos caminhos corretos.

- ✅ **Funcional — `code-review` (Skill), confirmado:** invocado via ferramenta `Skill` com um diff de teste (chave Stripe `sk_live_...` hardcoded, sem teste correspondente). Resultado: segredo classificado `blocker`/`secret` sem exceção, ausência de teste classificada `major` (nunca `blocker`) — a mesma distinção MUST_NOT vs. SHOULD do Standard original, obtida por instrução textual real, com resultado real.

- ✅ **Funcional — `code-reviewer` (Subagent), confirmado:** invocado via ferramenta Agent com o mesmo diff. O agente invocou a skill `code-review` internamente (exatamente o comportamento desenhado no passo 1 do seu prompt), decidiu `REQUEST_CHANGES` citando o achado `blocker` concreto na `rationale` (nr.rationale-references-evidence, satisfeito), confirmou explicitamente que não era autor do diff (nr.no-self-referential-authority/AG5, satisfeito), e sinalizou que a decisão envolvia risco alto e não deveria ser tratada como final sem revisão humana (aproximação de AG4, satisfeita). Os três comportamentos institucionais mais importantes que a tradução tentou preservar por instrução textual **foram observados funcionando**, não apenas escritos.

- ✅ **Funcional — `dependency-audit` (Skill), confirmado:** invocado com um manifesto de três pacotes, incluindo `event-stream@3.3.6` (o ataque de supply chain real de 2018) e `left-pad@1.0.0`. Classificou corretamente `event-stream` como `critical`, e — mais revelador — **não** classificou `left-pad@1.0.0` como vulnerabilidade, distinguindo corretamente o incidente famoso de 2016 (remoção do pacote do npm, um problema de disponibilidade) de uma vulnerabilidade de segurança real. Aplicou a ressalva de não-exaustividade (regra 3) sem que fosse preciso pedir.

- **Correção em relação a uma nota anterior desta mesma sessão:** eu havia registrado que Subagents "não recarregam dinamicamente" dentro da mesma sessão, diferente de Skills. Isso estava **errado** — os dois `.claude/skills/dependency-audit/` e `.claude/agents/code-reviewer.md` foram criados bem depois do início da conversa e ambos passaram a aparecer disponíveis pouco depois. A observação correta: **o registro de Skills e de Subagents refresca dentro da mesma sessão, mas não instantaneamente após a criação do arquivo** — há uma janela de atraso (a causa exata do gatilho de atualização não é algo que eu tenha visibilidade para afirmar com certeza). A tentativa imediatamente após criar `code-reviewer` falhou; a tentativa depois de mais alguns turnos funcionou. Isto está registrado aqui, corrigindo a afirmação anterior, em vez de deixá-la incorreta no repositório.

## 6. Próximos passos naturais

- ~~Verificar se `code-review` é descoberto e invocado corretamente~~ — **feito**, ver §5.
- ~~Verificar se `code-reviewer` é descoberto e invocado corretamente~~ — **feito**, ver §5.
- ~~Traduzir uma segunda Skill standalone (`dependency-audit`) e verificá-la~~ — **feito**, ver §5.
- ~~Um `PreToolUse` hook real para `nr.no-hardcoded-secrets`~~ — **escrito e testado diretamente, verificação de disparo real ainda pendente**, ver §7.
- Reconfirmar o hook (§7) em sessão nova, já que a hipótese mais provável para ele não ter disparado é a mesma classe de cache de configuração que afetou Skills/Subagents no início desta sessão.
- Estender o mesmo padrão às Skills de release e documentação (`skill.release.deploy`, `skill.release.record-keeping`, `skill.documentation.*`) do piloto.

---

## 7. O hook `PreToolUse` — o que foi comprovado e o que não foi

`.claude/hooks/check-no-secrets.sh` + `.claude/settings.json` implementam, para o caminho de `git commit`, uma barreira mecânica independente do modelo: escaneia o diff staged contra um conjunto pequeno e deliberadamente não-exaustivo de padrões de segredo (chave Stripe, AWS, GitHub, Google, blocos de chave privada) e bloqueia o commit (`exit 2`) se algum bater.

**Comprovado, por simulação direta do script (4 casos, fora do harness):**
1. Comando Bash que não é `git commit` → permite (`exit 0`).
2. `git commit` sem nada staged → permite.
3. `git commit` com diff staged limpo → permite.
4. `git commit` com um segredo Stripe no diff staged → **bloqueia** (`exit 2`), com mensagem explicando o motivo, citando `nr.no-hardcoded-secrets` e o Standard de origem.

Os quatro casos rodaram alimentando o script diretamente com o mesmo JSON via stdin que a documentação do Claude Code descreve como o payload real de um `PreToolUse` — a lógica do script está correta.

**Não comprovado — o disparo real pelo harness, dentro desta sessão:** tentei um `git commit` de verdade (em um repositório git descartável, fora deste, para não poluir o histórico real), com o mesmo segredo staged, esperando que o hook registrado em `.claude/settings.json` interceptasse. **O commit passou sem ser bloqueado.** Não afirmo que o hook "funciona no Claude Code" com base só na simulação do script — afirmo que o script está correto e que o disparo real não foi observado nesta sessão.

**Hipótese mais provável, não confirmada com certeza:** a mesma classe de limitação que afetou a lista de Subagents no início desta sessão — configuração (`settings.json`, incluindo hooks) carregada no início da sessão, não recarregada por escrever um arquivo novo depois. Para hooks especificamente, isso seria uma propriedade de segurança sensata, não um defeito: se hooks recarregassem instantaneamente a cada escrita de arquivo, um arquivo malicioso escrito por engano (ou por conteúdo externo/injeção) poderia instalar um hook e vê-lo valer imediatamente, sem qualquer janela de revisão humana. Não tenho visibilidade para confirmar esta hipótese com certeza — apenas que é consistente com o padrão já observado em Skills/Subagents (delay, não ausência de recarregamento) e com um motivo de design razoável.

**Ação necessária, não tomada nesta sessão:** confirmar em uma sessão nova (ou depois de reinício) se o hook dispara de verdade contra um `git commit` real com segredo staged.
