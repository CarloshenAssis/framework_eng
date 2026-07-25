# Reference Cycle 9 — Standard Package

*Companion de `components/core/standard.code-quality.baseline-package.yaml`. Ciclo de fechamento — mais curto que os anteriores por natureza: uma única peça, já bem delimitada pela arquitetura.*

---

## O que fecha

Standards Architecture §9 definiu `standard_kind: PACKAGE` desde a
ratificação daquele documento, com quatro restrições estruturais (I11):
`requirements[]` vazio, `extends[]` vazio, `includes[]` não vazio, e
versionamento MAJOR obrigatório quando qualquer incluído publica MAJOR
(ST13). Nenhum conteúdo havia instanciado isso até agora.

`core/standard.code-quality.baseline-package@1.0.0` agrega os dois
Standards `core/` já existentes (`review-baseline`,
`agent-decision-integrity`) sob uma única Coordinate. O nível
`PACKAGE_BASE` lista o fecho transitivo dos RIDs qualificados de ambos —
exatamente a garantia que Standards §6.2 já promete para `includes`: nenhum
NR é modificado, apenas reexposto sob nova identidade agregadora.

## Consequência prática

Uma Policy futura poderia trocar dois `bindings` separados por um único:

```yaml
bindings:
  - standard: core/standard.code-quality.baseline-package@1.0.0
    conformance_level: PACKAGE_BASE
```

em vez de vincular `review-baseline` e `agent-decision-integrity`
individualmente — sem que nenhum dos dois Standards originais mude, sem
duplicar nenhum NR, e sem que Composition, Certification ou Registry
precisem reconhecer um tipo novo (Standards §9, ESCOLHA DE DESIGN original:
Package é um perfil restrito de Standard, não um `component_type` novo).

---

Com este ciclo, todo mecanismo nomeado nos 20 documentos de arquitetura tem
exemplo real. Não há mais lacunas de cobertura conhecidas no piloto de
conteúdo — o que resta é decisão de escala (biblioteca em volume), não de
validação de mecanismo.
