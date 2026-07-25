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
  knowledge/
    <slug>.yaml            # Knowledge derivada de Executions, e Knowledge Asset que a
                            # `codifies` (RFC-DM-001 C1/C2) — ver Reference Cycle 6
  compliance/
    <subject-or-scope>.assessment.yaml   # ComplianceReport — Compliance Architecture §4-§5
    <slug>-waiver.yaml                   # Decision Record, família Waiver (Governance §15,
                                          # Compliance §4.7) — ver Reference Cycle 10
```

## Por que Compliance também vive aqui, não em `components/`

Um `ComplianceReport` é um `Artifact` — instância produzida por uma `Execution`
(a Compliance Assessment), nunca um Component definicional. Mesma lógica de
`certification/`: o que é definição vive em `components/`; o que é evento
institucional ocorrido — mesmo quando ilustrativo, como todo este piloto — vive
aqui (Compliance Architecture §4, §5).
