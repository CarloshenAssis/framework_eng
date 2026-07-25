# records/

Diferente de `components/` (Manifests de Component — dados **definicionais**),
esta pasta contém **instâncias de `Decision Record`** (Domain Model §14) —
eventos institucionais já ocorridos, imutáveis, nunca editados retroativamente
(uma correção gera um novo registro com `supersedes`, nunca sobrescreve o
anterior).

## Por que Certificação não vive em `components/`

`RegistryEntry.certification_status` é um **read-through** sobre a última
`Decision Record` da família `CertificationGrant` não superada — o Registry
nunca armazena esse dado, e o Manifest do Component **nunca** o carrega
(Registry & Discovery §12; Validation & Certification §3). Por isso os
registros de certificação vivem aqui, separados dos Manifests que certificam.

## Estrutura

```
records/
  certification/
    <coordinate>.yaml     # histórico de CertificationGrant para um Component
  role-assignment/
    <role-class>.yaml     # histórico de RoleAssignment (ver também
                           # docs/reference-cycle-walkthrough.md §1, exemplo inline)
```
