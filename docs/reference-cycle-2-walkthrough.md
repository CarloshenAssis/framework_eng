# Reference Cycle 2 — Organization, `extends`, Composição Cross-Namespace, Branch

*Companion de `components/org.acme-corp/` — não repete o que o Ciclo 1 já provou; foca no que é diferente.*

---

## O que este ciclo exercita que o Ciclo 1 não exercitou

| Mecanismo | Onde |
|---|---|
| `Organization` como Component real, Coordinate == raiz de Namespace | `org.acme-corp.yaml` |
| `Standard.extends` com elevação de força normativa (SHOULD→MUST) e adição de NR, sem enfraquecer o herdado | `standard.code-quality.strict.yaml` |
| Referência **cross-namespace totalmente qualificada** em Composition Slot (`pinned_coordinate`) | `workflow...strict.yaml`, `step.run-code-review` |
| **Duas Policies aplicáveis simultaneamente** ao mesmo sujeito, sem conflito (Standards diferentes → união, não arbitragem) | ver nota no fim do Workflow |
| `Branch`/Decision Point puro — Phase sem `steps`, apenas predicado sobre Artifact anterior | `phase.risk-branch` |
| L4 (Certifier humano obrigatório) usado como Constraint estrutural de um Slot, não só como regra de Certification | `phase.human-only-gate` |

---

## Resolução do Effective Policy Set — o ponto central deste ciclo

Quando `step.run-code-review` é despachado dentro da orquestração de `org.acme-corp/workflow.pull-request-review-strict`:

```
PolicyEval.resolve_effective_policy_set(subject=core/skill.static-analysis.code-review@1.0.0,
                                         ctx=Context Snapshot{ namespace_ancestry: org.acme-corp },
                                         plane=EXECUTION)

Fase 1 — candidatos por ancestralidade (Policy §11.1):
  ancestry = ["core", "org", "org.acme-corp"]
  candidatos = [ core/policy.code-quality.mandatory-review@1.0.0,        (scope=["core","org.*"])
                 org.acme-corp/policy.code-quality.strict-enforcement@1.0.0 ]  (scope=["org.acme-corp"])

Fase 2 — ambas passam nos filtros (Active, vigentes, scope match, sem condition)

Fase 3 — override chain: nenhuma das duas declara `overrides` — nada suprimido

Fase 4 — resolução por Standard (Policy §11.2):
  Standard A = core/standard.code-quality.review-baseline@1.0.0     (de policy 1)
  Standard B = org.acme-corp/standard.code-quality.strict@1.0.0     (de policy 2)
  → Coordinates DIFERENTES → SEM conflito a resolver → AMBOS os bindings entram no EPS

EffectivePolicySet.bindings = [
  { standard: core/standard.code-quality.review-baseline@1.0.0, level: BASE,  enforcement: BLOCKING },
  { standard: org.acme-corp/standard.code-quality.strict@1.0.0,  level: STRICT, enforcement: BLOCKING }
]
```

**Por que isso não é um caso de "conflito" (Policy §7.4):** conflito, naquele algoritmo, só existe quando duas Policies vinculam o **mesmo** Standard em níveis distintos. Aqui são dois Standards distintos — a Execution precisa satisfazer os dois simultaneamente, e a garantia de substituibilidade de `extends` (Standards §6.1) garante que isso não é redundante nem contraditório: os NRs herdados e não alterados (`nr.no-hardcoded-secrets`) só precisam ser verificados uma vez; `nr.test-coverage-present` é verificado sob a versão mais forte (MUST, do Standard estendido) — a versão SHOULD do base já está, por construção, coberta.

---

## Branch — o que o Scheduler faz em `phase.risk-branch`

```
Scheduler chega a phase.risk-branch (sem Steps a despachar)
  → lê o Artifact "review_report" produzido pela fase anterior (mesmo orchestration_id)
  → avalia os dois `condition` declarados em `next`
  → EXATAMENTE UM é verdadeiro (findings.any(blocker) é booleano, mutuamente exclusivo com sua negação)
  → Scheduler prossegue para o alvo correspondente
```

Nenhuma `Execution` é criada para a própria fase de Branch — ela é pura avaliação de predicado pelo Scheduler (Workflow §4: *"Decision Point cujo predicado MAY ser uma expressão pura avaliada pelo Scheduler sobre outputs anteriores... sem Execution"*), exatamente como já estava especificado antes de qualquer conteúdo real existir.

---

## O que este ciclo prova, em conjunto com o Ciclo 1

Com os dois ciclos publicados, o Framework demonstra, sobre conteúdo real (não apenas em prosa arquitetural):

- Isolamento multi-tenant funcional (`org.acme-corp` nunca alcança nem é alcançado por outra Organization além de `core/` compartilhado)
- Extensão normativa segura (`extends` nunca permite enfraquecimento — tentativa de reduzir `MUST` a `SHOULD` teria sido rejeitada na validação estrutural, Standards §12.3, invariante I8)
- Acúmulo correto de múltiplas Policies aplicáveis, sem exigir arbitragem quando os Standards vinculados são distintos
- Orquestração condicional (Branch) sem exigir Execution para a própria decisão de roteamento
- Uso de nível de Certificação (L4) como **Constraint de composição**, não apenas como rótulo — a diferença entre `phase.human-only-gate` e `phase.agent-gate` é inteiramente expressa por `min_certification_level`, sem nenhum campo especial de "requer humano"

**Nenhum mecanismo além dos já ratificados nos 20 documentos de arquitetura foi necessário para este segundo ciclo.**
