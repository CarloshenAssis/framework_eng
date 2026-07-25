# Reference Cycle 11 — Compliance Drift, Risk Acceptance, e uma emenda encontrada ao instanciar

*Companion de `records/compliance/`. Fecha as duas últimas peças nomeadas de
Compliance Architecture sem exemplo real (§4.6 Drift, §4.7 Risk Acceptance) —
e, ao tentar instanciar Risk Acceptance, expôs uma lacuna real na v1.0.0 do
documento, corrigida como emenda v1.1.0 antes deste ciclo ser escrito.*

---

## O que este ciclo exercita que nenhum ciclo anterior exercitou

| Mecanismo | Onde |
|---|---|
| `Compliance Drift` real (`detect_drift` sobre dois Reports já existentes, sem nova Execution) | `drift-wf01j-to-extended-pilot.yaml` |
| Distinção real entre Applicability drift e Normative drift (Compliance §4.6) | idem — Standard não mudou, só o nível vinculado |
| Non-Conformance genuína (`MUST` falho) — nenhum dos 10 Assessments anteriores tinha um | `fixture-secret-pattern.assessment.yaml` |
| `Risk Acceptance` real, distinta de Waiver (sem promessa de remediação, com `risk_classification` — Governance §14) | `fixture-secret-pattern-risk-acceptance.yaml` |
| A emenda v1.1.0 de Compliance Architecture (§4.4) — Waiver/Risk Acceptance de nível NR propagando para `BindingSatisfaction` | idem — recomputo antes/depois |

---

## Por que uma emenda foi necessária antes deste ciclo

Ao desenhar o registro de Risk Acceptance, a pergunta óbvia era: depois de
`ComplianceVerdict.waiver_ref` ser preenchido, o que acontece com
`BindingSatisfaction`? A resposta, na v1.0.0 de
`docs/architecture/21-compliance-architecture.md`, era: **nada**. A tabela
CM14 (§4.4) só consultava Waiver para o ramo `CLAIM_PARTIAL_REJECTED` (Ciclo
10); para o ramo `NO_CLAIM_NON_CONFORMANT`, nenhuma linha considerava
`waiver_ref` — o que tornaria uma Risk Acceptance real, formalmente
concedida, sem nenhum efeito sobre se o Binding seria tratado como satisfeito.
Isso não é apenas uma lacuna cosmética: dispensar um `MUST` sem que isso
jamais destrave o dispatch tornaria o próprio ato de conceder Risk
Acceptance institucionalmente inútil.

Esta é exatamente a mesma classe de achado que motivou a ratificação de
Compliance Architecture a corrigir o rascunho do Bloco 4 (`conformance_mode`
ausente) — só que desta vez encontrada um passo adiante, na primeira
tentativa de instanciar Risk Acceptance com dado real, dentro da mesma
sessão em que o documento foi ratificado. A resposta seguiu a mesma
disciplina: **emenda registrada, versão incrementada (v1.0.0→v1.1.0,
MINOR), nada apagado, nada corrigido em silêncio** — ver a "Nota de emenda"
no topo de `docs/architecture/21-compliance-architecture.md` e o §4.4
atualizado, antes de qualquer arquivo deste ciclo ser escrito.

---

## Drift — comparando dois Reports que já existiam

`drift-wf01j-to-extended-pilot.yaml` não dispara nenhuma nova Execution.
`detect_drift` (Compliance §5) é uma função pura sobre dois `ComplianceReport`
imutáveis já produzidos no Ciclo 10:

```
report_a = wf-01j-static-review.assessment.yaml     (09:15Z, EPS = mandatory-review@BASE)
report_b = extended-pilot.assessment.yaml            (17:30Z, EPS = extended-pilot@EXTENDED)

subject_drift     = ∅   (mesma versão do Component nos dois)
normative_drift   = ∅   (mesmo Standard, mesma versão do Standard nos dois)
applicability_drift = { EPS mudou: mandatory-review suprimida por extended-pilot via `overrides` }
```

O ponto fino, registrado explicitamente no arquivo: a diferença entre os
dois Reports **não** é o Standard evoluindo (isso seria Normative drift) —
é a Policy vigente mudando qual nível do **mesmo** Standard é exigido
(Applicability drift). Compliance §4.6 traça essa distinção em prosa; este
é o primeiro dado real que a torna verificável.

Nota deliberada no registro: este drift específico **não é um problema** —
foi um piloto institucional planejado (a própria Policy `extended-pilot`
existe para isso). Drift, por si, é descritivo — "sem juízo de valor"
(Compliance §4.6). Julgar se um drift é aceitável ou exige ação é sempre
Governance §13, nunca o próprio mecanismo de detecção.

---

## Risk Acceptance — quando o achado é real mas o risco não

`fixture-secret-pattern.assessment.yaml` é a primeira Non-Conformance
genuína do piloto inteiro — em 10 ciclos anteriores, todo `MUST` avaliado
foi sempre satisfeito. O achado é real e reprodutível: um valor com forma
de chave de API, detectado por varredura estática, dentro de
`tests/fixtures/sample_keys.py` — um fixture de teste, deliberadamente
parecido com uma credencial para que o próprio scanner tenha algo para
detectar em seus testes.

```
Verdict:  nr.no-hardcoded-secrets → NON_CONFORMANT (Evidence real, não indeterminação)
Claim:    nenhum emitido (CM15 — MUST falho impede emissão)
Binding:  satisfied=false, reason=NO_CLAIM_NON_CONFORMANT
```

`fixture-secret-pattern-risk-acceptance.yaml` resolve isso institucionalmente
— não corrigindo nada (não há o que corrigir: o valor precisa continuar
parecendo uma credencial para o teste continuar significativo), mas
**aceitando formalmente o risco residual**, com classificação BAIXO
(Governance §14), prazo obrigatório de revisão anual (não de remediação —
Governance §15 exige prazo mesmo quando não há promessa de correção), e
dupla autorização.

Recomputando `BindingSatisfaction` depois da Risk Acceptance, sob a regra
v1.1.0:

```
BindingSatisfaction antes:  satisfied=false, reason=NO_CLAIM_NON_CONFORMANT
BindingSatisfaction depois: satisfied=true,  reason=WAIVED
```

`ComplianceVerdict.outcome` permanece `NON_CONFORMANT` para sempre (CM4,
herdada sem alteração pela emenda) — a Evidence original nunca é
reescrita. O que muda é exclusivamente se o Binding, ao ser reavaliado, trata
essa Non-Conformance específica como já tratada institucionalmente.

---

## O que este ciclo prova, em conjunto com os dez anteriores

- As duas últimas peças nomeadas de Compliance Architecture sem exemplo real
  — Drift (§4.6) e Risk Acceptance (§4.7) — agora têm um. **Nenhum mecanismo
  nomeado em nenhum dos 21 documentos de arquitetura permanece "só em
  prosa".**
- A disciplina de encontrar erros reais ao instanciar conteúdo, e corrigi-los
  com nota explícita em vez de silenciosamente, se estende agora à própria
  arquitetura recém-ratificada, na mesma sessão — não é um comportamento
  específico do conteúdo, é uma propriedade de como este Framework inteiro
  foi construído.
- Risk Acceptance e Waiver, apesar de convergirem no mesmo mecanismo
  (`ComplianceVerdict.waiver_ref` / `BindingSatisfaction.waiver_ref`, ambos
  Governance §15), permanecem distinguíveis institucionalmente por
  `risk_classification` e pela ausência de promessa de remediação — a
  diferença é de intenção registrada, não de estrutura de dados.

**Nenhum mecanismo além dos já ratificados nos 21 documentos de arquitetura
foi necessário para este décimo primeiro ciclo — a única mudança na própria
arquitetura foi a emenda v1.1.0 de Compliance, registrada antes deste ciclo,
não durante.**
