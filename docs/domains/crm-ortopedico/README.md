# Domínio: CRM Equipamentos Ortopédicos

**Status:** conteúdo institucional ilustrativo (planejamento), não certificado, não executado por nenhum runtime.
**Origem:** pacote gerado externamente (LLM Kimi.AI), seguindo a convenção documental do Framework Eng, e incorporado a este repositório em 2026-07-25.

---

## O que é isto

Um terceiro domínio de conteúdo institucional — além de `core/` (revisão de PR / release, Ciclo 1) e
`org.acme-corp/` (isolamento multi-tenant, Ciclo 2) — aplicando a metodologia do Framework Eng
(Constitution → Domain Model → Workflow Architecture → Reference Cycle) a um domínio de negócio real:
gestão de empréstimo de equipamentos ortopédicos (cadeiras de rodas, muletas, andadores, cadeiras de
banho) por uma Secretaria Municipal de Assistência Social.

`docs/CHECKPOINT.md` §7 já listava "terceiro domínio de conteúdo institucional" como candidato futuro
sem ordem obrigatória — este é esse terceiro domínio.

Os artefatos de Component concretos (Skill, Workflow) ficam em
[`components/org.sec-assistencia-social/`](../../../components/org.sec-assistencia-social/).

## Ressalvas — leia antes de tratar isto como pronto para uso

1. **Gerado por outra ferramenta, não pela mesma disciplina de ratificação do resto do repositório.**
   Os quatro documentos aqui (`01-constitution-ortho.md`, `04-domain-model-ortho.md`,
   `10-workflow-architecture-ortho.md`, `reference-cycle-ortho.md`) não passaram pelo processo de
   ratificação descrito em Governance Architecture (documento 03) nem foram validados contra os 30
   documentos de arquitetura já ratificados neste repositório. Estão marcados como "ratificado" no
   próprio rodapé de cada arquivo, mas essa marca vem da sessão que os gerou, não deste repositório.

2. **Divergência de schema nos Components concretos.** `skill.gestao-emprestimo.yaml` e
   `workflow.emprestimo.yaml` usam um formato `apiVersion: framework.eng/v1` / `kind:` / `metadata:` /
   `spec:` (estilo CRD do Kubernetes) que **não corresponde** ao formato real usado em
   `components/core/` e `components/org.acme-corp/` deste repositório (`identity:` / `version:` /
   `component_type:` / `owner:` / `purpose:` — ver Identity & Namespace Architecture §5). Ou seja,
   nenhum dos dois arquivos é, hoje, um Component Manifest válido segundo Kernel Architecture §2 deste
   Framework — são ilustrativos do *conteúdo* (capabilities, templates, phases, steps), não do formato.
   Corrigir o schema é pré-requisito antes de qualquer tentativa real de `loader.py` carregar estes
   arquivos.

3. **Os workflows pressupõem mecanismos que o runtime real (`runtime/`) ainda não implementa.**
   `workflow.emprestimo.yaml` usa `compensation` (Saga) e múltiplas fases com Gate misto
   (`GATE_AUTO`/`GATE_APPROVAL`); `runtime-gap-analysis.md` já documenta que `run_workflow` hoje só
   executa cadeia linear, sem Branch/Join real, sem Retry automático, sem disparo automático de
   Compensation e sem Timeout. Nada aqui quebra a tese do Framework — apenas confirma, com um domínio
   novo, a mesma lacuna de completude de implementação já registrada em `docs/CHECKPOINT.md` §6 e
   `docs/runtime-gap-analysis.md` §1/§8.

4. **Recomendação de quem incorporou este conteúdo:** o Domain Model (14 entidades) e a especificação
   dos 5 workflows são um bom ponto de partida de *design* para uma aplicação real de empréstimo de
   equipamentos — mas construir essa aplicação em produção **sobre o runtime institucional deste
   repositório** (Registry/Composition/Skill invocation genéricos) não é recomendado no estado atual:
   o domínio nativo deste Framework é governança de engenharia de software (revisão de código, release,
   auditoria de dependência), e o runtime é, pelos próprios documentos citados acima, uma demonstração
   parcial, não uma base pronta para uma aplicação departamental com usuários finais (atendentes,
   beneficiários). A implementação real deste CRM está sendo conduzida separadamente, em
   `carloshenassis/tec_assistiva`, usando este Domain Model como especificação — não como runtime.

## Conteúdo

| Arquivo | Papel |
|---|---|
| `01-constitution-ortho.md` | Princípios, hierarquia de decisão, regras MUST NOT / SHOULD do domínio |
| `04-domain-model-ortho.md` | 14 entidades (Equipamento, Beneficiario, Emprestimo, Devolucao, Manutencao, Notificacao, Usuario, Auditoria, Foto...) |
| `10-workflow-architecture-ortho.md` | 5 workflows: empréstimo, devolução, manutenção, notificação automática, renovação |
| `reference-cycle-ortho.md` | Aplicação narrativa dos 12 Ciclos de Referência a este domínio |
| [`../../../components/org.sec-assistencia-social/skill.gestao-emprestimo.yaml`](../../../components/org.sec-assistencia-social/skill.gestao-emprestimo.yaml) | Skill (7 capabilities, 3 templates de notificação) — ver ressalva 2 |
| [`../../../components/org.sec-assistencia-social/workflow.emprestimo.yaml`](../../../components/org.sec-assistencia-social/workflow.emprestimo.yaml) | Workflow de 5 fases / 13 steps — ver ressalvas 2 e 3 |
| [`../../../components/org.sec-assistencia-social/ortho_contracts.py`](../../../components/org.sec-assistencia-social/ortho_contracts.py) | 8 entidades Python (`@dataclass`), enums, value objects, Registry Entry ilustrativo |

Existe também um protótipo de interface funcional (HTML/JS, fora deste repositório) demonstrando as 11
telas do CRM — dashboard, cadastro de equipamentos/beneficiários, wizard de empréstimo, devolução,
manutenção, agenda, relatórios e configurações. Ele vive em `carloshenassis/tec_assistiva`, junto com a
implementação real em andamento.
