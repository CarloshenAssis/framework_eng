# Reference Cycle 10 — Compliance Architecture: Assessment, Conformance Claim, Binding Satisfaction

*Companion de `records/compliance/` e `components/core/policy.code-quality.extended-pilot.yaml`.
Primeiro ciclo a exercitar o 21º documento de arquitetura — o único, até aqui, sem
nenhum conteúdo real (Compliance Architecture foi ratificada nesta sessão, a partir
do rascunho não ratificado do Bloco 4).*

---

## O que este ciclo exercita que nenhum ciclo anterior exercitou

| Mecanismo | Onde |
|---|---|
| `Compliance Assessment` real (RUNTIME), como `Execution` com Context Snapshot | `wf-01j-static-review.assessment.yaml` |
| `ConformanceClaim` (Standards §8.1) efetivamente **emitido**, não apenas definido | ambos os `*.assessment.yaml` |
| `Kernel §2.14 standards_bound` ∪ `Policy-derivado`, mesmo nível — união trivial | `wf-01j-static-review.assessment.yaml`, `resolution_trace.standards_bound_merged` |
| `Kernel §2.14` ∪ `Policy-derivado`, **níveis diferentes** (BASE ∪ EXTENDED) — união não trivial, primeira vez no piloto | `extended-pilot.assessment.yaml`, `resolution_trace.standards_bound_merged` |
| `Policy.overrides` (§7.3) suprimindo outra Policy — primeira vez no piloto | `policy.code-quality.extended-pilot.yaml`, `resolution_trace.suppressed_by_override` |
| `ConformanceClaim{mode: PARTIAL}` real, com `unsatisfied_should` não vazio | `extended-pilot.assessment.yaml` |
| `BindingSatisfaction` (Compliance §4.4, CM14) — os três ramos: `CLAIM_STRICT`, `CLAIM_PARTIAL_ACCEPTED`, `CLAIM_PARTIAL_REJECTED` | os três registros deste ciclo, um ramo cada |
| Waiver de **Binding** (Compliance §4.7) — distinto de Waiver de NR já usado no Ciclo 4 (esse era de RoleAssignment/Certification, não de Compliance) | `extended-pilot-strict-waiver.yaml` |
| Filtro **TEMPORAL** do algoritmo de Policy (§11.1, Fase 2) decidindo por relógio, não por conteúdo | os dois `*.assessment.yaml`, comparar `evaluated_at` com `effective_from` das duas Policies |

---

## Por que este ciclo era necessário

`docs/CHECKPOINT.md` registrava, desde a ratificação de Compliance Architecture como
documento 21, uma quebra do marco estabelecido no Ciclo 9: *"todos os documentos e
todo mecanismo nomeado de arquitetura ratificados agora têm pelo menos um exemplo
real exercitando-os."* Compliance, sendo o 21º documento, não tinha nenhum. Este
ciclo fecha essa lacuna — e, ao fazê-lo, dá o primeiro caso real a uma distinção que
só passou a existir nesta sessão: `PolicyBinding.conformance_mode` (Policy §5.3.1)
determinando se uma Partial Conformance satisfaz ou não um Binding específico
(Compliance §4.4) — exatamente a lacuna encontrada e fechada durante a ratificação
de Compliance Architecture.

---

## Assessment 1 — formalizando o dispatch do Ciclo 1

`wf-01j-static-review.assessment.yaml` não é conteúdo novo em espírito — é a
materialização, como `ComplianceReport` real, de uma verificação que
`docs/reference-cycle-walkthrough.md` §2 Fase 1 já descrevia em prosa: *"Policy
check (BLOCKING, applies_at=EXECUTION) ... dispatch só prossegue se [conformidade]
satisfizer BASE STRICT."* Até este ciclo, essa frase nunca tinha um Artifact por
trás dela — apenas a afirmação. Agora tem:

```
Subject:  core/skill.static-analysis.code-review@1.0.0
Contexto: mesma orchestration_id da Fase 1 do Ciclo 1, namespace_ancestry=[core]
EPS:      1 binding — core/policy.code-quality.mandatory-review@1.0.0
          (review-baseline@BASE, conformance_mode=STRICT)
Verdict:  nr.no-hardcoded-secrets → CONFORMANT (única NR em requires(BASE))
Claim:    mode=STRICT (trivial — zero SHOULD no conjunto resolvido)
Binding:  satisfied=true, reason=CLAIM_STRICT
```

Nota lateral, capturada em `resolution_trace.standards_bound_merged`: o próprio
Manifest do Skill já declara `standards_bound: [review-baseline@BASE]` (Kernel
§2.14). A Policy deriva **o mesmo** Standard, **o mesmo** nível — união trivial
(Policy §7.5), sem conflito, porque os dois mecanismos concordam. É a primeira vez
que essa coexistência é computada com dado real em vez de apenas citada como regra.

---

## Assessment 2 — o piloto EXTENDED e a Partial Conformance aceita

`core/policy.code-quality.extended-pilot@1.0.0` é a única peça de conteúdo
genuinamente nova deste ciclo. Ela existe porque nenhuma Policy do piloto, até
aqui, vinculava um Standard num nível cujo `requires()` misturasse MUST e SHOULD:

- `core/policy.code-quality.mandatory-review` vincula BASE — só tem
  `nr.no-hardcoded-secrets` (MUST_NOT).
- `org.acme-corp/policy.code-quality.strict-enforcement` vincula STRICT do Standard
  `org.acme-corp/standard.code-quality.strict` — mas esse Standard **eleva**
  `nr.test-coverage-present` de SHOULD (no base) para MUST (Standards §6.1); não
  sobra nenhum SHOULD para ser "parcialmente" satisfeito.

O nível **EXTENDED** de `core/standard.code-quality.review-baseline` — que existe
desde o Ciclo 1, nunca vinculado por nenhuma Policy — é o único lugar do piloto
inteiro onde um MUST e um SHOULD coexistem no mesmo `requires()`. A nova Policy o
vincula, com `conformance_mode: PARTIAL_ACCEPTABLE` — uma decisão institucional
real e comum (piloto de elevação de critério, sem quebrar quem ainda não tem a
tooling de cobertura madura).

```
Subject:  core/skill.static-analysis.code-review@1.0.0 (mesmo, execução distinta)
EPS:      1 binding — extended-pilot suprime mandatory-review via `overrides` (Policy §7.3)
Verdicts: nr.no-hardcoded-secrets → CONFORMANT
          nr.test-coverage-present → NON_CONFORMANT (Evidence real de ausência de
             teste correspondente — não INDETERMINATE, que exigiria ausência de Evidence)
Claim:    mode=PARTIAL, unsatisfied_should=[nr.test-coverage-present]
Binding:  conformance_mode=PARTIAL_ACCEPTABLE → satisfied=true, reason=CLAIM_PARTIAL_ACCEPTED
```

Nenhum Waiver é necessário aqui — e nenhum foi emitido (`waiver_ref: null`). Isso
é o ponto: sob `PARTIAL_ACCEPTABLE`, uma Partial Conformance é um resultado
**válido por construção** (Standards §8.2), não uma violação disfarçada.

---

## O comparativo — quando o mesmo Claim é rejeitado

`extended-pilot-strict-waiver.yaml` responde à pergunta que motivou este ciclo:
*o que muda se o Binding, em vez de `PARTIAL_ACCEPTABLE`, exigisse `STRICT`?*

Sem alterar uma linha de Evidence ou recomputar o Claim — a **mesma**
`ConformanceClaim{mode: PARTIAL}` do Assessment 2 é reavaliada contra um Binding
hipotético idêntico em tudo, exceto `conformance_mode: STRICT`:

```
BindingSatisfaction sem Waiver: satisfied=false, reason=CLAIM_PARTIAL_REJECTED
```

Este é exatamente o ramo que o rascunho pré-ratificação de Compliance Architecture
(Bloco 4) não conseguia expressar — ele não tinha `conformance_mode` para
consultar, porque esse campo só passou a existir quando Policy Architecture foi
re-ratificada depois do rascunho de Compliance ter sido escrito. É a lacuna
registrada na nota de ratificação de `docs/architecture/21-compliance-architecture.md`,
agora com um caso de dado real, não só a prosa que a descreve.

O registro então concede um **Waiver de Binding** (Compliance §4.7 — distinto de
Waiver de NR, que já existe desde o Ciclo 4 em outro contexto: RoleAssignment/
Certification, não Compliance): motivo registrado, prazo obrigatório
(30 dias), dono, condição de encerramento, dupla autorização (Governance §15), e
visibilidade pública. Depois do Waiver:

```
BindingSatisfaction com Waiver: satisfied=true, reason=WAIVED
```

`claim.mode` permanece `PARTIAL` para sempre — o Waiver nunca o reclassifica para
`STRICT` (CM4). A distinção auditável entre "atingiu o rigor exigido" e "foi
dispensado de precisar atingi-lo" nunca é apagada, mesmo quando o resultado prático
(dispatch prossegue) é o mesmo.

---

## O que este ciclo prova, em conjunto com os nove anteriores

- Compliance Architecture, o 21º e último documento a ganhar conteúdo real, agora
  produz `ComplianceReport`, `ConformanceClaim` e `BindingSatisfaction` com dados
  concretos — os três ramos de CM14 (`CLAIM_STRICT`, `CLAIM_PARTIAL_ACCEPTED`,
  `CLAIM_PARTIAL_REJECTED`) todos exercitados, não apenas dois de três.
- A lacuna real encontrada durante a ratificação de Compliance (`conformance_mode`
  inexistente no rascunho original) tem, agora, um cenário de dado real que mostra
  exatamente por que ela importava — não apenas a correção textual no documento.
- Dois mecanismos de Policy Architecture nunca antes exercitados com dado real
  neste piloto — `overrides` (§7.3) e união de mesmo Standard em níveis diferentes
  (§7.4, caso "comparável", distinto do caso "Standards diferentes" já provado no
  Ciclo 2) — agora têm exemplo concreto.
- Waiver de Binding (Compliance §4.7) tem sua primeira instância real, seguindo
  integralmente Governance §15, sem nenhum mecanismo paralelo.

**Nenhum mecanismo além dos já ratificados nos 21 documentos de arquitetura foi
necessário para este décimo ciclo.**
