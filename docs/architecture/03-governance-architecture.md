# GOVERNANCE ARCHITECTURE
### Framework Eng — A Autoridade Operacional do Sistema

*Versão 1.0.0 — Documento Institucional-Técnico*

> A Constitution diz por que o Framework existe. O Kernel diz qual forma tudo deve ter. Este documento diz **quem decide, como se decide, e o que acontece quando algo dá errado**. Nenhum componente entra, muda ou sai do Framework fora dos processos aqui definidos.

---

# 0. Papel da Governance

Constitution e Kernel são, por desenho, estáveis e passivos — eles definem regras, mas não têm agência para aplicá-las. A Governance é a camada **ativa**: é ela que admite, revisa, aprova, certifica, audita, aposenta e resolve conflitos. Sem Governance, o Kernel é uma lei sem tribunal — pode ser violado sem consequência, e o Framework degrada exatamente do jeito que a Constitution existe para evitar.

A Governance não escreve componentes. Ela decide **se, quando e como** um componente pode existir, mudar, ou deixar de existir.

---

# 1. Princípios da Governança

1. **Autoridade é distribuída, nunca centralizada em uma pessoa.** Nenhuma decisão relevante depende de um único indivíduo insubstituível.
2. **Toda decisão de governança é registrada.** Uma decisão não documentada não tem validade institucional, mesmo que tenha sido tomada de fato.
3. **Rigor proporcional ao risco.** Uma mudança de patch em uma Skill não exige o mesmo processo que uma mudança no Kernel.
4. **Reversibilidade antes de permanência.** Sempre que possível, decisões são desenhadas para poderem ser desfeitas — isso barateia o custo de errar.
5. **Nenhuma exceção é silenciosa.** Toda exceção às regras é explícita, com prazo, dono e justificativa.
6. **Governança serve o sistema, não protege o status quo.** Um componente antigo não tem vantagem sobre um novo além da evidência de que ainda funciona melhor.
7. **Transparência por padrão, sigilo por exceção justificada.** Todo processo de governança é visível a qualquer participante do Framework, salvo motivo explícito de segurança.

---

# 2. Papéis Institucionais

| Papel | Responsabilidade | Autoridade |
|---|---|---|
| **Framework Council** | Órgão colegiado de maior autoridade operacional. Aprova mudanças no Kernel e conduz o processo de emenda constitucional. | Único papel com poder de aprovar mudança no Kernel; recomenda mudanças na Constitution. |
| **Domain Steward** | Responsável por uma camada ou domínio inteiro (ex: Standards de segurança, Skills de dados). Aprova componentes dentro de seu domínio. | Aprova/rejeita componentes de seu domínio; não pode alterar Kernel ou Constitution. |
| **Component Owner** | Responsável individual (pessoa ou time) por um componente específico. | Propõe mudanças, responde por qualidade, inicia deprecação do próprio componente. |
| **Reviewer** | Avalia formalmente uma proposta (RFC, novo componente, mudança) antes da aprovação. Pode ser um par do Owner ou um especialista de domínio. | Aprova, solicita mudanças, ou rejeita — não decide sozinho em mudanças de alto risco (exige quórum, Seção 8). |
| **Auditor** | Executa auditorias periódicas independentes (duplicação, staleness, conformidade). Não participa da criação dos componentes que audita. | Sinaliza não conformidade; não tem poder de remoção direta — encaminha ao Steward/Council. |
| **Certifier** | Avalia se um componente atende aos critérios de Certificação (Seção 11). Papel distinto de Reviewer — atua depois que o componente já está `Active`. | Concede, suspende ou revoga certificação. |
| **Framework Maintainer** (coletivo) | Comunidade de todos os Owners e Stewards ativos — participa de RFCs abertos e votação quando aplicável. | Voz consultiva em RFCs; voto formal apenas quando o processo de RFC exigir (Seção 9). |

**Regra de não concentração:** ninguém pode ser simultaneamente Reviewer e Owner do mesmo componente na mesma decisão. O Framework Council nunca é composto por uma única pessoa.

---

# 3. Ownership

**Ownership é a responsabilidade primária e contínua por um componente específico.** Todo componente `Active` tem exatamente um Owner declarado no Manifest (Seção 6 do Kernel Architecture) — Owner pode ser um time, mas nunca "ninguém" ou um grupo difuso sem ponto de contato único.

Responsabilidades do Owner:
- Manter o componente conforme com Standards e Policies vigentes.
- Responder a Consumers sobre comportamento, falhas e roadmap do componente.
- Iniciar e conduzir mudanças de versão.
- Iniciar deprecação quando o componente deixar de fazer sentido.

Ownership **não** confere autoridade para ignorar Reviewers, Stewards ou Auditors — é responsabilidade operacional, não autoridade de governança superior.

---

# 4. Stewardship

**Stewardship é a responsabilidade por um domínio inteiro** (uma categoria de Standards, uma família de Skills, uma camada como Policies de segurança) — não por um componente isolado.

O Steward:
- Aprova admissão de novos componentes dentro de seu domínio.
- Garante coerência entre componentes do mesmo domínio (evita que dois Standards do mesmo domínio se contradigam).
- Atua como escalonamento quando um conflito entre componentes do domínio não se resolve entre Owners.
- Não é dono de nenhum componente individual do seu domínio — Stewardship é supervisão, Ownership é execução.

**Diferença estrutural chave:** Ownership responde "este componente está correto?"; Stewardship responde "este domínio, como um todo, está coerente?".

---

# 5. Sucessão de Ownership

Todo componente deve ter um processo de sucessão definido antes de precisar dele — não depois.

- **Sucessão planejada:** quando um Owner sai de seu papel (por transição de time, saída da organização, etc.), a transferência de Ownership é obrigatória e registrada antes da saída efetiva. Nenhum componente `Active` pode ficar sem Owner mesmo temporariamente.
- **Sucessão não planejada:** se um Owner se torna inacessível sem transferência prévia, o Domain Steward do componente assume Ownership interino imediatamente e tem prazo definido para identificar um novo Owner permanente ou iniciar deprecação.
- **Componente sem sucessor identificável:** entra automaticamente em avaliação de Orfandade (Seção 6).

Toda sucessão é um evento registrado no histórico do componente — quem era, quem passou a ser, quando, e por quê.

---

# 6. Componentes Órfãos e Abandonados

**Órfão:** componente `Active` cujo Owner deixou de existir sem sucessão definida (Seção 5). Um componente órfão entra automaticamente em um estado de observação — continua funcional para Consumers existentes, mas é sinalizado publicamente no sistema de descoberta como sem responsável.

**Abandonado:** componente que permanece órfão além do prazo institucional definido para resolução, ou que não recebe manutenção apesar de sinais claros de necessidade (falhas de validação recorrentes, Standards vinculados que mudaram sem o componente se adaptar).

**Tratamento:**
1. Órfão é sinalizado imediatamente à Governance e ao Domain Steward correspondente.
2. Steward tem prazo para encontrar novo Owner ou decidir por deprecação formal.
3. Se abandonado sem resolução, o componente é movido compulsoriamente para `Deprecated` pelo Steward, independentemente de haver Consumers ativos — um componente sem dono não pode permanecer `Active` indefinidamente, pois representa risco não gerenciado.

---

# 7. Admission Process (como novos componentes entram)

Todo componente novo percorre o mesmo funil, independentemente do tipo:

1. **Proposta (`Draft`).** Autor preenche o Manifest completo (Kernel, Seção 6), incluindo Purpose, Contract e Owner proposto.
2. **Checagem de duplicação.** Consulta obrigatória ao sistema de descoberta por Capability/Purpose equivalente. Resultado registrado mesmo se negativo.
3. **Submissão a Review.** Componente muda para `Review`; Reviewer(s) designado(s) conforme domínio.
4. **Avaliação de Reviewer.** Verifica conformidade estrutural (Kernel), conformidade normativa (Standards/Policies aplicáveis do domínio), e qualidade do Purpose/Contract.
5. **Decisão do Steward do domínio.** Aprova (`Approved`), devolve para ajuste (retorno a `Draft`), ou rejeita formalmente com justificativa registrada.
6. **Ativação.** Componente aprovado é promovido a `Active` e passa a ser descobrível e consumível.

**Quem aprova:** o Domain Steward do domínio ao qual o componente pertence, mediante avaliação prévia de ao menos um Reviewer independente do Owner.
**Quem revisa:** um Reviewer indicado pelo Steward, nunca o próprio Owner.
**Quem rejeita:** o Steward do domínio; rejeições podem ser recorridas ao Framework Council apenas em caso de discordância sobre interpretação do Kernel ou da Constitution (nunca sobre mérito técnico isolado).

---

# 8. Quem Pode Alterar o Quê

Autoridade de mudança é estritamente hierárquica, espelhando a hierarquia de decisões da Constitution:

| Camada | Quem propõe | Quem aprova | Quórum |
|---|---|---|---|
| **Constitution** | Qualquer Maintainer, via RFC formal de emenda constitucional | Framework Council, por unanimidade ou supermaioria definida previamente | Máximo — mudança rara e deliberada |
| **Kernel** | Framework Council ou Maintainer via RFC | Framework Council | Alto — requer RFC completo (Seção 9) |
| **Governance (este documento)** | Framework Council ou Maintainer via RFC | Framework Council | Alto |
| **Standards / Policies** | Domain Steward ou Owner do domínio | Domain Steward, com Review de pares | Médio |
| **Templates / Skills / Agents / Workflows** | Component Owner | Domain Steward, com Review | Padrão (Admission Process) |

Nenhuma camada pode ser alterada por autoridade de uma camada abaixo dela — um Steward não pode alterar o Kernel; um Owner não pode alterar um Standard fora do processo de proposta formal ao Steward.

---

# 9. RFC Process (Request for Comments)

Usado para toda mudança estrutural relevante: Kernel, Governance, Standards de alto impacto, e qualquer Breaking Change (Seção 10).

**Etapas:**
1. **Draft do RFC** — problema, motivação, proposta, alternativas consideradas, impacto em componentes existentes.
2. **Discussão aberta** — período fixo em que qualquer Maintainer pode comentar; comentários são registrados, não descartados.
3. **Revisão formal** — Reviewers designados avaliam viabilidade técnica e conformidade com Constitution/Kernel.
4. **Decisão** — aprovação pela autoridade correspondente (Seção 8), com justificativa registrada mesmo em caso de rejeição.
5. **Registro permanente** — todo RFC, aprovado ou rejeitado, permanece acessível indefinidamente como parte do histórico institucional do Framework — inclusive os rejeitados, que evitam retrabalho de propostas já avaliadas.

Um RFC nunca é aprovado silenciosamente — a ausência de objeção durante a discussão não substitui aprovação formal da autoridade correspondente.

---

# 10. Breaking Changes

Uma Breaking Change é qualquer mudança que invalida uma expectativa de compatibilidade já assumida por Consumers existentes.

**Processo obrigatório:**
1. Identificação explícita de que a mudança é breaking (nunca disfarçada de minor/patch).
2. RFC obrigatório, com listagem de todos os Consumers afetados (obtida via campo `consumers`, Kernel Seção 2.7).
3. Definição de janela de transição — período em que versão antiga e nova coexistem (antiga entra em `Deprecated`, não é removida imediatamente).
4. Comunicação formal a todos os Consumers listados antes da mudança entrar em vigor.
5. Só após a janela de transição a versão antiga pode avançar para `Archived`.

Breaking Change sem RFC prévio é, por definição, uma violação de governança — mesmo que tecnicamente correta.

---

# 11. Certification

Certificação é o selo formal de que um componente `Active` continua, no presente, atendendo aos critérios de qualidade (Constitution, Seção 11) e conformidade normativa — distinto da aprovação inicial (Admission), que é um evento único no passado.

**Como ocorre:**
- Certifier avalia periodicamente (ciclo definido pelo Domain Steward, proporcional ao risco do componente) se o componente continua conforme.
- Componentes de alto risco (ex: vinculados a Policies de segurança/compliance) têm ciclo de recertificação mais curto que componentes de baixo risco.

**Como um componente perde certificação:**
- Falha em validação estrutural ou normativa (Kernel, Seção 8) detectada por Auditor ou Certifier.
- Standard/Policy vinculado mudou e o componente não se adaptou dentro do prazo de conformidade.
- Certificação revogada é publicamente visível no sistema de descoberta — um componente sem certificação vigente é sinalizado como risco a qualquer novo Consumer, mesmo permanecendo tecnicamente `Active`.

Perda de certificação não remove o componente automaticamente — é um sinal de risco que aciona revisão do Owner com prazo para correção, sob supervisão do Steward.

---

# 12. Audit

Auditorias são independentes: quem audita não pode ter aprovado ou sido Owner do que audita.

**O que é auditado periodicamente:**
- Duplicação (componentes com Capability/Purpose sobrepostos).
- Staleness (componentes não atualizados apesar de dependências ou Standards vinculados terem mudado).
- Órfãos e abandonados.
- Conformidade de Certificação vencida.
- Conflitos não resolvidos entre Standards do mesmo domínio.

**Saída da auditoria:** um relatório formal, público dentro do Framework, com achados classificados por severidade e encaminhados ao Steward correspondente com prazo de resposta. Auditorias não têm poder executivo direto — elas geram obrigação de resposta, não ação automática.

---

# 13. Compliance

Compliance é a verificação contínua (não pontual) de que componentes `Active` respeitam os Standards e Policies vigentes — inclusive quando esses Standards/Policies mudam depois que o componente já estava ativo.

Toda mudança em um Standard ou Policy dispara automaticamente uma lista de componentes potencialmente afetados (via `metadata` do Kernel, vínculos declarados). Cada Owner afetado é notificado e tem prazo proporcional ao risco da não conformidade para atualizar seu componente — findo o prazo sem resolução, o componente é suspenso de descoberta ativa até regularização.

---

# 14. Risk Management

Todo componente carrega um nível de risco implícito, determinado por: (a) reversibilidade de suas ações, (b) quantidade de Consumers, (c) domínio a que pertence (segurança e compliance são risco estruturalmente mais alto).

**Gestão de risco na prática:**
- Componentes de alto risco exigem quórum maior de Review na Admission e ciclo mais curto de Certification.
- Toda Breaking Change em componente de alto risco exige RFC mesmo quando, em componente de baixo risco, um processo simplificado seria aceitável.
- Risco é reavaliado quando o número de Consumers de um componente cresce significativamente — um componente que nasceu de baixo risco pode se tornar crítico pela adoção, e a Governance deve responder a essa mudança de perfil, não apenas ao risco declarado na origem.

---

# 15. Exception Process

Uma exceção é a permissão formal e temporária de desviar de um Standard, Policy ou processo de Governance para um caso específico.

**Regras:**
- Toda exceção tem: motivo registrado, prazo de validade, dono responsável, e o que precisa acontecer para a exceção deixar de ser necessária.
- Exceção sem prazo não é permitida — uma exceção permanente é, na prática, uma proposta disfarçada de mudança de Standard, e deve seguir o processo formal de mudança (Seção 8), não o de exceção.
- Exceções são aprovadas pelo mesmo nível de autoridade que aprovaria a mudança formal equivalente — uma exceção a um Standard é aprovada pelo Domain Steward; uma exceção a uma regra do Kernel exige Framework Council.
- Toda exceção ativa é visível no sistema de descoberta junto ao componente afetado — nunca oculta.

---

# 16. Technical Debt

Débito técnico é tratado como um artefato de primeira classe, não como conhecimento tácito perdido em conversas.

- Todo débito conhecido é registrado formalmente, vinculado ao componente que o carrega, com: descrição do desvio do ideal, risco que representa, e condição de resolução.
- Débito registrado não bloqueia automaticamente a Certification, mas é fator obrigatório na avaliação de risco (Seção 14) e é reportado nas métricas institucionais (Seção 19).
- Débito não registrado, quando descoberto por Auditoria, é tratado como falha de processo do Owner, não apenas como falha técnica — a Governance espera transparência proativa, não descoberta posterior.

---

# 17. Conflict Resolution

Conflitos ocorrem em três formas principais, cada uma com caminho de resolução próprio:

1. **Conflito entre Standards do mesmo domínio.** Resolvido pelo Domain Steward — se o Steward não conseguir reconciliar, escala ao Framework Council como RFC.
2. **Conflito entre Standards de domínios diferentes.** Aplica-se a hierarquia de precedência definida na Constitution (global > domínio > stack > projeto); se ambos estiverem no mesmo nível de precedência, o Framework Council arbitra.
3. **Conflito entre Reviewers/Stewards sobre uma decisão de Admission.** Escalado ao Framework Council, que decide com base exclusivamente em conformidade ao Kernel e à Constitution — nunca em preferência técnica pessoal.

Toda resolução de conflito é registrada como Decision Record (Seção 18) — o precedente fica disponível para conflitos futuros semelhantes, reduzindo retrabalho de arbitragem.

---

# 18. Decision Records

Toda decisão de governança com impacto além de um único componente (aprovações de RFC, resoluções de conflito, exceções, deprecações forçadas, revogações de certificação) gera um **Decision Record** formal: contexto, alternativas consideradas, decisão tomada, autoridade responsável, e data.

Decision Records são permanentes e nunca editados retroativamente — uma decisão revista gera um novo Decision Record que referencia e supera o anterior, preservando o histórico de como o entendimento institucional evoluiu ao longo do tempo.

---

# 19. Governance Metrics

Métricas institucionais medem a saúde do *processo de governança em si*, não a qualidade de componentes individuais (isso já é coberto pelas métricas de qualidade do Kernel/Constitution):

- **Tempo médio de Admission** (Draft → Active) — mede fricção do processo.
- **Taxa de rejeição em Review** — mede se o funil está filtrando adequadamente ou é apenas burocracia sem efeito.
- **Componentes órfãos/abandonados ativos** — mede saúde de Ownership.
- **Exceções ativas vencidas sem resolução** — mede disciplina de compliance.
- **RFCs abertos vs. resolvidos, por tempo médio de resolução** — mede capacidade de evolução do sistema.
- **Débito técnico registrado vs. resolvido no período** — mede se a dívida está sendo paga ou apenas acumulada.
- **Certificações vencidas sem recertificação** — mede risco latente não tratado.

Essas métricas são revisadas periodicamente pelo Framework Council como parte da própria evolução da Governance — se uma métrica mostra degradação persistente, a Governance em si é candidata a RFC de mudança.

---

# 20. Governance Lifecycle

A Governance sobre um componente segue o mesmo ciclo de vida do componente (Kernel, Seção 3), mas adiciona pontos de controle próprios:

```
Draft ──► Review ──► Approved ──► Active ──► Deprecated ──► Archived ──► Removed
  │           │                      │             │
  │      [checagem de           [Certification   [Compliance
  │       duplicação]            periódica]        contínua]
  │                                   │
  └── pode retornar ──────────────────┘
      de Review para Draft      [Auditoria pode sinalizar
                                  órfão/abandonado a qualquer
                                  momento durante Active]
```

A Governance nunca é um evento único (a aprovação inicial) — é supervisão contínua durante todo o tempo em que o componente permanece `Active`, encerrando-se apenas quando o componente chega a `Removed`.

---

# 21. Diagrama de Governança

```
┌───────────────────────────────────────────────────────────────────┐
│                         FRAMEWORK COUNCIL                            │
│   aprova: Kernel · Governance · emenda constitucional (recomenda)    │
│   arbitra: conflitos não resolvidos · recursos de rejeição            │
└───────────────────────────────┬──────────────────────────────────────┘
                                 │ delega autoridade de domínio
┌───────────────────────────────▼──────────────────────────────────────┐
│                          DOMAIN STEWARDS                               │
│   aprovam: Standards/Policies/componentes do próprio domínio           │
│   resolvem: conflitos intra-domínio · órfãos · deprecação forçada      │
└───┬──────────────┬───────────────┬───────────────┬────────────────────┘
    │              │               │               │
┌───▼───┐    ┌─────▼─────┐   ┌─────▼─────┐   ┌─────▼─────┐
│ OWNER  │    │ REVIEWER   │   │ AUDITOR    │   │ CERTIFIER  │
│propõe, │    │avalia antes│   │verifica    │   │reavalia    │
│mantém  │    │da aprovação│   │periodica-  │   │conformidade│
│        │    │            │   │mente       │   │no tempo    │
└───┬───┘    └─────┬─────┘   └─────┬─────┘   └─────┬─────┘
    │              │               │               │
    └──────────────┴───────┬───────┴───────────────┘
                            │
                  ┌─────────▼─────────┐
                  │  COMPONENT (Kernel) │
                  │  Draft→...→Removed  │
                  └────────────────────┘

     Todo evento relevante de qualquer papel acima ──► DECISION RECORD
     (permanente, nunca editado retroativamente)
```

---

## Fechamento

A Governance é o que impede que "escalabilidade" vire sinônimo de "caos organizado". Ela não acelera o Framework — ela garante que, quando ele acelerar (mais componentes, mais domínios, mais organizações usando o mesmo núcleo), a velocidade não seja comprada com perda de coerência.

Três garantias resumem esta camada: **(1) nenhuma mudança relevante acontece sem autoridade explícita e registrada; (2) nenhum componente existe sem responsável identificável e reavaliado no tempo; (3) todo conflito, exceção e decisão gera um precedente permanente, para que o Framework aprenda com sua própria história em vez de repeti-la.**
