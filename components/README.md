# components/

Esta pasta contém **conteúdo real** do Framework Eng — instâncias concretas de Component (Standard, Policy, Skill, Agent, Workflow), diferente de `docs/`, que contém a arquitetura normativa (as regras de como qualquer Component deve existir).

## Convenção de caminho

O caminho do arquivo espelha diretamente o `Coordinate` do Component (Identity & Namespace Architecture §5):

```
components/<namespace>/<component_type>.<nome>.yaml
```

Exemplo: `core/skill.static-analysis.code-review.yaml` ⟺ Coordinate `core/skill.static-analysis.code-review`.

## Status: Ciclo de Referência (Reference Instantiation)

Os cinco arquivos em `core/` são o **primeiro conteúdo real do Framework** — um ciclo mínimo e completo (Standard → Policy → Skill → Agent → Workflow) instanciado deliberadamente pequeno, para validar que toda a infraestrutura institucional (Kernel, Registry, Composition, Execution, Validation & Certification, Observability, Agent) funciona de ponta a ponta antes de qualquer geração de conteúdo em volume.

Ver `docs/CHECKPOINT.md` para o status completo do Framework e o raciocínio por trás desta decisão.

**Este ciclo NÃO deve ser tratado como certificado ou pronto para produção** — nenhuma Execution real, nenhuma Certification real e nenhum RoleAssignment real foram processados por um runtime; os exemplos abaixo (incluindo o Decision Record de RoleAssignment) são ilustrativos, mostrando a forma exata que esses artefatos assumiriam quando processados pelo mecanismo já especificado nos documentos de arquitetura.
