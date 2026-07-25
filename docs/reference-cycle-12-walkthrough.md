# Reference Cycle 12 — Observability: saída literal de consulta, não apenas prosa

*Não introduz nenhum `components/` nem `records/` novo — de propósito, não por
esquecimento. Ver "Por que este ciclo não vive em `records/`" abaixo.*

---

## O que este ciclo fecha

`docs/CHECKPOINT.md` §5 registrava a última lacuna sem gênero arquitetural
próprio (não é um mecanismo nomeado sem exemplo — todos os 21 documentos já
têm um, desde o Ciclo 11): nenhuma consulta real de `Observability Query
Service` (§7.1) tinha sido mostrada como **saída literal**, apenas narrada
em prosa (ex.: "`query_events()` retornaria as séries históricas..."). Este
ciclo mostra três das oito operações da superfície — `trace()`,
`provenance()`, `query_events()` — computadas sobre dado que já existe nos
Ciclos 10 e 11, sem nenhuma Execution nova.

## Por que este ciclo não vive em `records/`

`Trace`, `Span`, `Provenance Chain` são, por regra normativa explícita
(Observability Architecture, OB2): **"MUST NOT ser persistidos como
Artifact ou qualquer entidade do Domain Model."** São Value Objects
recomputados a cada consulta — nunca guardados. Um arquivo em `records/`
implicaria exatamente o oposto do que OB2 exige. As três saídas abaixo são,
portanto, blocos de código dentro deste walkthrough — a mesma forma que
qualquer exemplo ilustrativo assume nos próprios documentos de arquitetura
— nunca um Artifact novo no repositório. `query_events()` retorna `Event[]`
(telemetria operacional, retenção `BOUNDED` por padrão — Observability
§6.3), reforçando a mesma decisão pelo lado oposto: nem os Events
consultados pretendem ser permanentes.

---

## Consulta 1 — `trace(orchestration_id)`

Sobre a orquestração que o Ciclo 10 formalizou primeiro — o dispatch do
Ciclo 1 (`wf-01j-static-review.assessment.yaml`):

```
trace(orchestration_id: "wf-01J8Y1RQ0G2H4J6KVKX7ZC1PWN")

→ Trace {
    orchestration_id: "wf-01J8Y1RQ0G2H4J6KVKX7ZC1PWN"
    spans: [
      Span {
        execution_id:        "cmp-01J8Y1RQ2K4M6N8PVKX9ZC3RWA"
        component_ref:       core/skill.static-analysis.code-review@1.0.0
        orchestration_id:    "wf-01J8Y1RQ0G2H4J6KVKX7ZC1PWN"
        phase_id:             phase.static-review
        step_id:               step.run-code-review
        attempt:                0
        state:                  Completed
        performed_by:          role.system.compliance-service
        context_snapshot_ref: "cs-01J8Y1RQ0G2H4J6KVKX7ZC1PWN-0"
        produced_artifacts:   ["cc-01J8Y1RQ0G2H4J6KVKX7ZC1PWN-1"]   # o ConformanceClaim{STRICT}
        evidence_refs:         ["ev-01J8Y1RQ0G2H4J6KVKX7ZC1PWN-secrets"]
        started_at:             "2026-07-25T09:15:00Z"
        ended_at:               "2026-07-25T09:15:00Z"
      }
    ]
    complete: true
  }
```

**Nota de escopo, registrada em vez de escondida:** este Trace tem um único
Span porque este piloto, desde `components/README.md` e `records/README.md`,
nunca materializou a Execution do próprio Skill (o dispatch que produziria
`review_report`) como registro — apenas a Compliance Assessment que o
governa. Um `trace()` real, sobre um runtime real, teria pelo menos dois
Spans (`step.run-code-review` executando o Skill + a Assessment que o
autoriza) e, na Fase 2 já narrada em `docs/reference-cycle-walkthrough.md`,
um terceiro (`step.reviewer-decision`, o Agent). `complete: true` é
formalmente correto mesmo assim — a regra (OB5) é sobre todo Span retornado
estar em estado terminal, não sobre a orquestração inteira estar
representada; nada aqui viola a regra, mas seria enganoso não registrar o
porquê de haver só um Span.

---

## Consulta 2 — `provenance(subject)`

Sobre a Evidence que fundamentou a única Non-Conformance real do piloto
(`fixture-secret-pattern.assessment.yaml`, Ciclo 11) — exercitando o ramo
`raiz é Artifact` do algoritmo (§9.2, linha 2-3), que a Consulta 1 não
precisou usar:

```
provenance(subject: "ev-01J8Y5K1F6U0W2Z4NQRP1MD5VB-secrets")

→ ProvenanceChain {
    subject:      "ev-01J8Y5K1F6U0W2Z4NQRP1MD5VB-secrets"       # a Evidence STRUCTURAL

    origin:       "cmp-01J8Y5K1H8W2Y4B6PQRT3MF7VD"                # WalkBack(produces⁻¹):
                                                                     # a Compliance Assessment que a produziu

    context:      "cs-01J8Y5K1F6U0W2Z4NQRP1MD5VB-0"               # WalkBack(captured_as):
                                                                     # Context Snapshot daquela Assessment

    responsible:  role.system.compliance-service                  # WalkBack(performed_by)

    against:      core/skill.static-analysis.code-review@1.0.0    # WalkBack(declares/describes):
                                                                     # o subject que a Evidence descreve

    affects: [                                                     # WalkForward({derives_from⁻¹,
                                                                     #   informs, references⁻¹})
      "core/standard.code-quality.review-baseline@1.0.0#nr.no-hardcoded-secrets"  # o NR que a Evidence substancia
      "records/compliance/fixture-secret-pattern-risk-acceptance.yaml#decisions[0]"  # a Risk Acceptance
                                                                     # que a referenciou depois, via verdict_ref
    ]

    complete: true
  }
```

Este é o caso em que `provenance()` responde algo que nenhum registro
isolado, sozinho, responde: a Evidence de Non-Conformance do Ciclo 11 e a
Risk Acceptance que a resolveu são dois arquivos distintos, escritos em
momentos distintos — `affects` é o que os conecta mecanicamente, exatamente
a "quinta pergunta" de Domain Model §15 ("o que isto afeta ou referencia?"),
agora respondida como dado, não como algo que só se sabe por ter lido os
dois arquivos e notado a coincidência de nomes.

---

## Consulta 3 — `query_events(filter, time_range)`

Sobre os três Assessments dos Ciclos 10-11, mais o Drift e a Risk Acceptance
do Ciclo 11 — a única das três consultas que atravessa múltiplas
orquestrações, exatamente o que `trace()` (escopado a uma só) não pode
fazer:

```
query_events(
  filter: {
    component_ref: core/skill.static-analysis.code-review@1.0.0,
    event_type: [ComplianceAssessmentCompleted, ConformanceClaimEmitted,
                  ComplianceViolationDetected, ComplianceDriftDetected, RiskAccepted]
  },
  time_range: ["2026-07-25T00:00:00Z", "2026-07-26T23:59:59Z"]
)

→ Event[] = [
    { event_type: ComplianceAssessmentCompleted, timestamp: "2026-07-25T09:15:00Z",
      orchestration_id: "wf-01J8Y1RQ0G2H4J6KVKX7ZC1PWN", outcome: SATISFIED },
    { event_type: ConformanceClaimEmitted,        timestamp: "2026-07-25T09:15:00Z",
      claim_ref: "cc-01J8Y1RQ0G2H4J6KVKX7ZC1PWN-1", mode: STRICT },

    { event_type: ComplianceAssessmentCompleted, timestamp: "2026-07-25T11:00:00Z",
      orchestration_id: "wf-01J8Y5K1F6U0W2Z4NQRP1MD5VB", outcome: VIOLATED },
    { event_type: ComplianceViolationDetected,    timestamp: "2026-07-25T11:00:00Z",
      nr_id: "core/standard.code-quality.review-baseline@1.0.0#nr.no-hardcoded-secrets" },

    { event_type: ComplianceAssessmentCompleted, timestamp: "2026-07-25T17:30:00Z",
      orchestration_id: "wf-01J8Y3F90N4P6RVXMY9AD3SXA0", outcome: SATISFIED },
    { event_type: ConformanceClaimEmitted,        timestamp: "2026-07-25T17:30:00Z",
      claim_ref: "cc-01J8Y3F90N4P6RVXMY9AD3SXA0-1", mode: PARTIAL },

    { event_type: ComplianceDriftDetected,        timestamp: "2026-07-25T18:00:00Z",
      cause: APPLICABILITY, computed_over: ["wf-01J8Y1RQ0G2H4J6KVKX7ZC1PWN",
                                              "wf-01J8Y3F90N4P6RVXMY9AD3SXA0"] },

    { event_type: RiskAccepted,                    timestamp: "2026-07-26T10:00:00Z",
      nr_id: "core/standard.code-quality.review-baseline@1.0.0#nr.no-hardcoded-secrets",
      risk_tier: BAIXO }
  ]
```

Oito eventos, ordenados por `timestamp` — a mesma chave de índice já
normatizada em Observability §6.1 (`component_type, event_type,
timestamp`). Lidos em sequência, contam exatamente a história dos Ciclos
10-11 sem precisar reabrir nenhum dos seis arquivos que a produziram: uma
Assessment limpa, uma violação real, uma Assessment sob piloto com Partial
aceito, o drift entre as duas primeiras, e a Risk Acceptance que resolveu a
violação. `time_range` cabe dentro de qualquer janela de retenção razoável
(Observability §6.3) — nenhum `RETENTION_WINDOW_EXCEEDED` (B5) se aplica
aqui.

---

## O que este ciclo prova, em conjunto com os onze anteriores

- As três formas estruturalmente distintas de consulta que Observability
  oferece — reconstrução de uma orquestração (`trace`), rastreamento de
  proveniência de um dado específico (`provenance`), e busca agregada
  através de múltiplas orquestrações (`query_events`) — têm, agora, saída
  literal real, não apenas a afirmação de que "seria assim".
- `provenance()` respondeu uma pergunta real que nenhum arquivo isolado
  respondia sozinho — a ligação entre a Evidence de uma Non-Conformance e a
  Risk Acceptance que a resolveu, dias-narrativos depois, em outro arquivo.
- A decisão de manter esta consulta inteiramente dentro do walkthrough, sem
  nenhum arquivo novo em `records/`, é ela mesma uma aplicação de uma regra
  normativa (OB2) — não uma escolha de conveniência.
- Com isso, a única lacuna de "mecanismo narrado mas nunca mostrado como
  dado" registrada em `docs/CHECKPOINT.md` está fechada. O que resta em
  aberto no roadmap é expansão (terceiro domínio, biblioteca em volume),
  não mais validação de nenhuma peça nomeada da arquitetura.

**Nenhum mecanismo além dos já ratificados nos 21 documentos de arquitetura
foi necessário para este décimo segundo ciclo.**
