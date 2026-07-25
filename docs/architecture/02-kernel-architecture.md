# KERNEL ARCHITECTURE
### Framework Eng — As Leis Estruturais do Sistema

*Versão 1.0.0 — Documento Técnico Fundacional*

> Este documento não descreve nenhum Agent, Skill, Workflow, Template, Standard ou Policy específico. Ele descreve **a lei estrutural que qualquer um deles deve obedecer para ser reconhecido como parte do Framework**. Onde a Constitution diz *por que* o Framework existe, o Kernel diz *o que é exigido para algo existir dentro dele*.

---

# 0. Papel do Kernel

O Kernel é a camada que transforma os princípios da Constitution em **regras verificáveis por máquina**. Ele não tem opinião sobre engenharia de software, sobre negócio, ou sobre qualidade de um agente específico — isso é responsabilidade de camadas abaixo dele (Standards, Governance, os próprios componentes). O Kernel tem opinião sobre uma coisa só: **a forma que qualquer coisa precisa ter para ser um cidadão válido do Framework.**

Um componente que obedece ao Kernel pode ser mau, ineficiente, ou redundante — mas nunca pode ser *ilegível pelo sistema*, *não rastreável*, ou *inconsistente com sua própria declaração*. O Kernel garante a forma; a qualidade do conteúdo é papel de outras camadas.

---

# 1. O que é um Componente

Um **Componente** é qualquer unidade do Framework que declara um propósito, expõe um contrato, e pode ser descoberta, versionada e executada ou consultada independentemente. Todo Agent, Skill, Workflow, Template, Standard, Policy, Checklist, Knowledge, Research e Playbook é, estruturalmente, um Componente — a diferença entre eles é o *tipo* (`component_type`), não a *forma*.

Um Componente é definido por três propriedades inseparáveis:

1. **Ele declara antes de agir.** Nada sobre um componente é inferido ou assumido pelo sistema — tudo é declarado no seu Manifest.
2. **Ele é endereçável.** Todo componente tem uma identidade única e estável, que não muda mesmo quando seu conteúdo muda.
3. **Ele é responsável.** Todo componente tem um dono, um contrato, e critérios pelos quais pode ser validado ou invalidado.

Um artefato que não satisfaz essas três propriedades não é um Componente — é, na melhor das hipóteses, um rascunho fora do sistema (ver Estado `Draft` na Seção 3).

---

# 2. O Component Contract

Todo Componente, independentemente do tipo, é regido pelo mesmo modelo estrutural: o **Component Contract**. É o equivalente, no Kernel, a uma interface que toda classe deve implementar — nenhum componente é reconhecido pelo sistema sem satisfazer integralmente este contrato.

### 2.1 Identity
A identidade única e permanente do componente. Não muda entre versões — a identidade é o que permite dizer que a v1 e a v3 de um componente são "o mesmo componente evoluindo", não dois componentes diferentes. Inclui um identificador namespaced (tipo + domínio + nome) e é a chave pela qual todo o resto do sistema referencia o componente.

### 2.2 Purpose
Uma declaração curta, obrigatória e não ambígua do problema que o componente resolve e do que ele explicitamente não resolve (seus limites de escopo). Purpose é o que permite ao sistema de descoberta (Seção 5) e ao processo de admissão (governança) detectar sobreposição com componentes existentes.

### 2.3 Owner
A entidade (pessoa, papel ou time) responsável pela manutenção, evolução e resposta por falhas do componente. Nenhum componente existe sem Owner — um componente sem dono é, por definição, um componente órfão e não pode estar em estado `Active` (Seção 3).

### 2.4 Inputs
A especificação formal do que o componente exige para operar: dados, contexto, ou artefatos de entrada, cada um com sua forma esperada e sua obrigatoriedade (requerido vs. opcional).

### 2.5 Outputs
A especificação formal do que o componente se compromete a produzir quando operado corretamente, incluindo tanto o resultado de sucesso quanto os modos de falha declarados (o componente também declara *como* falha, não apenas como funciona).

### 2.6 Dependencies
A lista explícita de outros componentes (por Identity + faixa de versão compatível) dos quais este componente precisa para funcionar. Um componente nunca depende de algo não declarado aqui — dependência implícita é uma violação estrutural (ver Seção 7).

### 2.7 Consumers
A lista, mantida pelo sistema (não pelo próprio componente), de quais outros componentes declaram este componente como dependência. É o inverso de Dependencies, e existe para que nenhum componente seja alterado ou removido sem visibilidade de impacto sobre quem depende dele.

### 2.8 Providers
No caso de componentes que atuam como agregadores ou orquestradores (por exemplo, um Workflow em relação aos Agents que invoca), Providers identifica quais componentes fornecem as capacidades que este componente orquestra, distinto de Dependencies por descrever uma relação de composição, não apenas de requisito técnico (ver Seção 10).

### 2.9 Capabilities
A declaração explícita do que o componente é capaz de fazer — o vocabulário de ações ou resultados que ele oferece ao restante do sistema. É o que permite que outro componente o descubra por capacidade, não apenas por nome (Seção 5).

### 2.10 Constraints
As condições sob as quais o componente **não deve** ser usado, ou os limites dentro dos quais sua garantia de correção é válida. Constraints é o mecanismo formal pelo qual um componente declara suas próprias limitações — nenhum componente pode ser considerado "geral" ou "sem limites" por omissão; a ausência de Constraints declarada é tratada como suspeita, não como permissão irrestrita.

### 2.11 Version
A versão do componente sob um esquema semântico estável, permitindo que consumidores declarem faixas de compatibilidade em vez de acoplamento a uma versão exata (ver Seção 8).

### 2.12 Lifecycle
O estado atual do componente dentro do ciclo de vida padrão (Seção 3), determinando se ele pode ser consumido, se está em avaliação, ou se está em processo de saída do sistema.

### 2.13 Compatibility
A declaração explícita de com quais versões de suas Dependencies o componente foi validado, e de qual é sua própria política de compatibilidade para seus Consumers (o que muda entre um patch, um minor e um major).

### 2.14 Metadata
Informação estrutural de suporte que não afeta o comportamento do componente mas é necessária para governança e descoberta: categoria, tags, data de criação, histórico de mudança, referências a Standards e Policies aos quais está vinculado.

### 2.15 Validation
A declaração de como o próprio componente pode ser verificado como correto — os critérios que um validador (automatizado ou humano) usa para confirmar que o componente cumpre o que declara (ver Seção 7).

**Regra estrutural central:** nenhum componente é admitido no Framework com qualquer um destes quinze campos ausente. Um campo pode ser declarado como vazio/não aplicável explicitamente — mas nunca pode estar simplesmente omitido.

---

# 3. Ciclo de Vida do Componente

Todo componente, de qualquer tipo, percorre o mesmo ciclo de vida. O estado do componente é um campo de primeira classe do Contract (`Lifecycle`), não uma convenção informal.

```
Draft → Review → Approved → Active → Deprecated → Archived → Removed
```

### Draft
O componente existe como proposta. Tem um Contract preenchido, mas ainda não foi validado nem verificado contra duplicação. **Não pode ser consumido por nenhum outro componente.** Existe apenas para permitir iteração antes do compromisso formal com o sistema.

### Review
O componente foi submetido à Governance para avaliação: verificação de conformidade com o Kernel, verificação de não-duplicação, verificação de conformidade com Standards e Policies aplicáveis. Um componente pode retornar a `Draft` se a revisão identificar lacunas. **Ainda não pode ser consumido.**

### Approved
O componente passou pela revisão e foi formalmente aceito, mas ainda não foi publicado para uso — este estado existe para permitir uma janela entre aprovação e disponibilização (por exemplo, aguardando uma janela de release coordenada, ou dependências ainda em `Draft`). **Consumo ainda não é permitido.**

### Active
O componente está disponível para descoberta e consumo por outros componentes. É o único estado em que um componente pode ganhar novos Consumers. Um componente `Active` continua sujeito a validação contínua (Seção 7) — permanecer `Active` é uma condição, não um destino permanente.

### Deprecated
O componente continua funcional para Consumers existentes, mas está formalmente marcado para saída, com um substituto indicado (quando aplicável) e uma data-alvo de sunset declarada em Compatibility. **Novos Consumers não devem adotá-lo** — isso é sinalizado pelo sistema de descoberta (Seção 5), embora consumo por Consumers já existentes continue tecnicamente possível durante a transição.

### Archived
O componente não está mais disponível para novo consumo, mas seu histórico, seu Contract e seu registro de decisão permanecem acessíveis para fins de auditoria e reconstrução de contexto histórico. Nenhum Consumer ativo pode depender de um componente `Archived` — se ainda existir algum, isso é uma violação a ser resolvida pela Governance antes do arquivamento poder se completar.

### Removed
O componente é retirado permanentemente do sistema de descoberta ativo. Seu registro histórico mínimo (Identity, motivo de remoção, o que o substituiu, quando existente) é preservado indefinidamente para auditabilidade — mas o componente em si deixa de existir operacionalmente.

**Regra de transição:** nenhum componente pula estados. A única exceção formal é retorno de `Review` para `Draft`. Toda transição de estado é, em si, um evento registrado (quem, quando, por quê) — o histórico de Lifecycle de um componente é parte permanente de seu registro, mesmo após `Removed`.

---

# 4. Como um Componente Nasce, Evolui e Declara Contexto

**Nascimento:** um componente nasce no estado `Draft` no momento em que seu Contract é preenchido pela primeira vez — antes disso, ele é apenas uma ideia, fora do domínio do Kernel.

**Evolução:** um componente evolui por meio de novas versões de si mesmo (Seção 8), nunca por edição silenciosa de uma versão já `Active`. Uma vez `Active`, o conteúdo associado a uma versão é imutável — mudança de comportamento exige uma nova versão, com sua própria passagem pelo ciclo de vida a partir de `Draft`.

**Context:** todo componente pode declarar, dentro de Metadata, o contexto no qual foi concebido e no qual é válido — por exemplo, se pertence ao núcleo reutilizável do Framework ou a uma camada de Domain específica de uma organização (ver Constitution, hierarquia de camadas). Um componente de Domain nunca pode ser promovido a Consumer de componentes de núcleo sem restrição — mas o inverso, componentes de núcleo sendo usados por Domain, é o fluxo esperado. Um componente nunca declara contexto de forma implícita: se não declarado, é assumido como escopo mais restrito possível (Domain local), nunca como núcleo.

---

# 5. Sistema de Descoberta

O princípio central: **um componente que não pode ser descoberto é, para efeitos práticos do sistema, equivalente a um componente que não existe** — e sua ausência do índice é o convite mais direto à duplicação.

### Como componentes são encontrados

A descoberta nunca depende de navegação manual de pastas ou memória de nomes. Todo componente é indexado automaticamente a partir do seu Manifest (Seção 6) em um registro central, consultável por múltiplas dimensões simultâneas:

- Por **Identity** (busca exata, quando o consumidor já sabe o que procura).
- Por **Capability** (busca por "o que preciso que seja feito", não por nome).
- Por **component_type** (todos os Agents, todos os Skills, etc.).
- Por **tags/Metadata** (domínio, categoria, organização).
- Por **Lifecycle** (por exemplo, excluir automaticamente tudo que não está `Active`).

### Como se evita duplicação

Toda submissão de um novo componente em `Draft` que avança para `Review` passa obrigatoriamente por uma consulta de descoberta por Capability e Purpose antes de poder ser aprovada — a Governance não pode aprovar um componente sem essa consulta ter sido executada e seu resultado registrado (mesmo que o resultado seja "nenhuma sobreposição relevante encontrada").

### Como um Agent sabe quais Skills existem

Um Agent nunca lista Skills manualmente em sua definição de forma fixa e exaustiva além do que precisa — ele declara, em Capabilities e Dependencies, o tipo de capacidade que necessita, e o sistema de descoberta resolve isso contra o registro de Skills `Active` compatíveis. Isso permite que novas Skills equivalentes ou superiores substituam as anteriores sem exigir reescrita do Agent, desde que respeitem o mesmo contrato de capacidade.

### Como um Workflow sabe quais Agents utilizar

Da mesma forma: um Workflow declara, por fase, a Capability ou o papel (`role`) necessário, resolvido contra o registro de Agents `Active` — com a opção de fixar uma Identity específica quando a fase exige um Agent determinado por motivo explícito (registrado em Constraints).

### Como um Template é localizado

Templates são descobertos por `artifact_type` (o tipo de artefato que produzem) cruzado com os Standards aos quais estão vinculados — garantindo que quem busca "o template para uma decisão arquitetural" encontre a opção correta mesmo sem saber seu nome exato.

---

# 6. O Manifest Padrão

O Manifest é a materialização declarativa do Component Contract (Seção 2) — a única forma pela qual um componente se torna legível pelo Kernel. Todo componente, de qualquer tipo, possui exatamente os mesmos campos obrigatórios (a estrutura não muda entre um Agent e um Standard — apenas o conteúdo dos campos muda).

**Campos obrigatórios do Manifest** (sem sintaxe de arquivo — apenas a estrutura conceitual exigida):

1. `identity` — identificador único e permanente, tipo do componente, namespace/domínio.
2. `purpose` — descrição do problema resolvido e do escopo explicitamente fora de alcance.
3. `owner` — responsável identificável.
4. `version` — versão semântica atual.
5. `lifecycle_state` — estado atual dentro do ciclo de vida (Seção 3).
6. `inputs` — especificação formal de entrada.
7. `outputs` — especificação formal de saída, incluindo modos de falha.
8. `dependencies` — lista de componentes requeridos, com faixa de versão compatível.
9. `consumers` — gerado e mantido pelo sistema, não pelo autor do componente.
10. `providers` — componentes cuja capacidade este componente agrega/orquestra (quando aplicável).
11. `capabilities` — vocabulário de ações/resultados oferecidos.
12. `constraints` — limites de uso e condições de não aplicabilidade.
13. `compatibility` — política de versionamento e faixa validada de dependências.
14. `metadata` — tags, categoria, contexto (núcleo vs. Domain), vínculos com Standards/Policies, histórico de criação.
15. `validation` — critérios pelos quais este componente é considerado correto.

**Regra de uniformidade:** um Standard, um Playbook e um Agent têm a mesma estrutura de Manifest. A diferença entre eles está inteiramente no conteúdo de `identity.component_type` e no que cada campo significa para aquele tipo — nunca na forma. Isso é o que permite ao Kernel validar, indexar e versionar qualquer componente com o mesmo mecanismo, independente de quantos tipos de componente existirem no futuro.

---

# 7. Modelo de Dependências

### Como um componente declara dependência de outro

Toda dependência é declarada explicitamente no campo `dependencies` do Manifest, referenciando a Identity do componente desejado mais uma faixa de compatibilidade de versão (não uma versão exata fixa, exceto quando Constraints justificar essa rigidez). Dependência não declarada não existe para o sistema — um componente que consome outro sem declarar viola a regra estrutural central do Kernel (Seção 2).

### Como detectar ciclos

O registro central constrói, a partir de todas as declarações de `dependencies`, um grafo dirigido de componentes. Antes de qualquer componente sair de `Review` para `Approved`, o grafo é verificado quanto à ausência de ciclos — uma dependência circular (A depende de B que depende de A) é rejeitada estruturalmente, nunca aceita "por enquanto". Isso é uma validação obrigatória, não opcional (Seção 8).

### Como detectar incompatibilidades

Toda vez que um componente do qual outros dependem publica uma nova versão, o sistema verifica automaticamente se essa nova versão ainda satisfaz as faixas de compatibilidade declaradas por seus Consumers atuais. Uma mudança que quebra essa faixa é, por definição, uma mudança de versão maior (major) — nunca pode ser publicada como patch ou minor (ver Seção 2.13, Compatibility).

### Como validar compatibilidade entre versões

Compatibilidade é validada em duas direções simultâneas: **retrocompatibilidade** (uma nova versão de um componente continua satisfazendo contratos que seus Consumers existentes esperam) e **compatibilidade declarada** (o próprio componente afirma explicitamente contra quais versões de suas Dependencies foi validado — nunca assume compatibilidade por ausência de teste).

---

# 8. Modelo de Validação

Todo componente é validado em duas camadas distintas, ambas obrigatórias:

### Validação Estrutural (sempre automatizada)
Verifica que o Manifest está completo (todos os quinze campos do Contract presentes), que a Identity é única no sistema, que não há ciclos de dependência, que as faixas de versão declaradas são bem formadas, e que todos os componentes referenciados em Dependencies e Providers efetivamente existem e estão em um estado de Lifecycle que permite consumo (`Active` ou, com aviso, `Deprecated`).

### Validação de Conformidade (automatizada onde possível, humana onde exigir julgamento)
Verifica que o componente respeita os Standards e Policies vinculados a ele, que seu Purpose não sobrepõe significativamente um componente já `Active` (checagem de duplicação), e que seus critérios de `validation` declarados são, eles próprios, verificáveis (um componente não pode declarar um critério de sucesso que ninguém consegue checar).

**Regra: nenhum componente avança de `Review` para `Approved` sem passar integralmente pelas duas camadas.** Falha em qualquer validação retorna o componente a `Draft` com o motivo explícito registrado — nunca é ignorada ou contornada por urgência.

---

# 9. Modelo de Extensão

O Kernel precisa permitir que terceiros — times, organizações, contribuidores externos — criem novos componentes, e até novos **tipos** de componente no futuro, sem jamais poder alterar o próprio Kernel para isso.

**Princípio central:** extensão acontece *dentro* da forma do Component Contract, nunca *contra* ela. Um novo tipo de componente (por exemplo, um tipo ainda não previsto hoje) é permitido desde que seu Manifest satisfaça integralmente os quinze campos obrigatórios do Contract — o Kernel não precisa saber, com antecedência, quais tipos de componente existirão em cinco anos, porque ele valida a *forma*, não a *lista fechada de tipos*.

Isso significa que a extensibilidade do Framework não é uma exceção ao Kernel — é uma consequência direta de o Kernel definir uma interface (o Component Contract) em vez de uma enumeração fixa de componentes conhecidos.

Toda extensão continua sujeita, sem exceção, à Governance (admissão, verificação de duplicação) e à Validação Estrutural — o Kernel nunca relaxa suas leis para acomodar um novo tipo de componente; ele apenas nunca as restringiu ao ponto de impedir um.

---

# 10. Modelo de Composição

Componentes pequenos formam componentes maiores por meio de duas relações estruturais distintas, ambas já presentes no Contract:

- **Dependency** — "eu preciso que isto exista e funcione para que eu funcione" (relação técnica de requisito).
- **Provider** — "eu organizo e dou sentido sequencial ao uso disto" (relação de composição/orquestração).

Um Workflow, por exemplo, não "contém" Agents no sentido de posse — ele os referencia como Providers, definindo a ordem e as condições em que suas capacidades são invocadas, enquanto cada Agent mantém sua própria identidade, versão e ciclo de vida independentes.

**Regra de composição:** um componente composto nunca herda automaticamente o estado de Lifecycle de seus componentes internos — ele deve declarar e validar sua própria composição sempre que qualquer Provider muda de versão de forma incompatível (isso é detectado pelo mesmo mecanismo de compatibilidade da Seção 7). Composição não é cópia — é referência viva e verificada continuamente.

Isso permite que a mesma Skill pequena seja reutilizada como parte de dezenas de Agents diferentes, e que o mesmo Agent seja reutilizado como Provider de dezenas de Workflows diferentes, sem nunca duplicar sua definição.

---

# 11. Modelo de Interoperabilidade

Para que todo tipo de componente "converse" de forma previsível com qualquer outro, a interoperabilidade depende inteiramente de três garantias que o Kernel impõe uniformemente:

1. **Toda comunicação entre componentes acontece através de Inputs/Outputs declarados** — nunca por acoplamento implícito ao funcionamento interno de outro componente. Um Agent não precisa saber *como* uma Skill funciona internamente, apenas seu contrato de entrada e saída.
2. **Toda referência entre componentes usa Identity + faixa de compatibilidade** — nunca nome livre, caminho de arquivo, ou suposição de versão. Isso garante que a comunicação sobrevive à evolução de qualquer uma das partes.
3. **Todo componente é validado sob o mesmo modelo (Component Contract)** — não existe um "tipo especial" de componente com regras estruturais diferentes. Um Standard, um Skill e um Workflow interoperam entre si porque todos falam exatamente a mesma "língua estrutural" — a diferença é apenas semântica (o que cada um significa), nunca sintática (como cada um é declarado e descoberto).

Interoperabilidade, no Kernel, não é um recurso adicional — é uma consequência direta de todos os componentes compartilharem a mesma forma. É por isso que o Kernel se recusa a permitir qualquer exceção estrutural, mesmo pequena: uma exceção na forma é, em potencial, uma quebra de interoperabilidade em algum ponto futuro da cadeia.

---

# 12. Diagrama — Como o Kernel Conecta o Sistema

```
┌──────────────────────────────────────────────────────────────────────┐
│                            CONSTITUTION                                 │
│      princípios permanentes — legitima e limita tudo abaixo             │
└───────────────────────────────┬────────────────────────────────────────┘
                                 │ rege
┌───────────────────────────────▼────────────────────────────────────────┐
│                              GOVERNANCE                                  │
│   admissão, versionamento, deprecação — decide o QUE entra e QUANDO      │
└───────────────────────────────┬────────────────────────────────────────┘
                                 │ opera sobre
┌───────────────────────────────▼────────────────────────────────────────┐
│                                KERNEL                                    │
│   Component Contract · Lifecycle · Discovery · Manifest · Dependency ·   │
│   Validation · Extension · Composition · Interoperability                │
│                                                                            │
│   ── toda camada abaixo desta linha É, estruturalmente, um Componente ── │
└───┬───────────┬────────────┬───────────┬───────────┬───────────┬────────┘
    │           │            │           │           │           │
┌───▼───┐  ┌────▼────┐  ┌────▼─────┐ ┌───▼────┐ ┌────▼─────┐ ┌───▼──────┐
│STANDARDS│ │ POLICIES │  │TEMPLATES │ │ SKILLS │ │  AGENTS  │ │WORKFLOWS │
└───┬───┘  └────┬────┘  └────┬─────┘ └───┬────┘ └────┬─────┘ └───┬──────┘
    │           │            │           │           │           │
    └───────────┴────────────┴─────┬─────┴───────────┴───────────┘
                                    │  todos descobertos, versionados e
                                    │  validados pelo mesmo Kernel
                              ┌─────▼─────┐
                              │ EXECUTION  │
                              │ instância  │
                              │ concreta   │
                              └────────────┘
```

**Leitura do diagrama:** a Constitution não conhece o Kernel — ela apenas o legitima. O Kernel não conhece Standards, Agents ou Workflows individualmente — ele conhece apenas a *forma* que qualquer um deles deve ter. Toda camada da direita (Standards até Workflows) é, para o Kernel, indistinguível em estrutura — apenas o `component_type` no Manifest as diferencia. Execution é o único ponto onde o sistema deixa de ser puramente declarativo e se torna ação real, sempre rastreável até os componentes e Manifests que a originaram.

---

## Fechamento

O Kernel não cria nada. Ele torna possível que tudo o mais seja criado de forma consistente, descobrível, versionada e verificável — hoje com dezenas de componentes, e daqui a anos com milhares, sem que a forma fundamental precise mudar.

Duas propriedades do Kernel merecem ênfase por serem o que realmente garante longevidade: **(1) ele valida forma, não conteúdo** — por isso comporta tipos de componente ainda não imaginados hoje; **(2) toda relação entre componentes é declarada e endereçável, nunca implícita** — por isso o sistema pode crescer em volume sem crescer em acoplamento oculto.
