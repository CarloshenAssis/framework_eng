# Reference Cycle 7 — Segundo Domínio, GATE_AUTO, Workflow sem Agent

*Companion de `components/core/workflow.api-documentation-pipeline.yaml`.*

---

## 1. Por que este ciclo existe

O `docs/CHECKPOINT.md` (Seção 5) listava explicitamente como lacuna: *"Domínio
de conteúdo fora de 'revisão de código/release' — todo o piloto é de um único
domínio."* Seis ciclos consecutivos usando o mesmo domínio (revisão de
código) arriscavam provar apenas que a arquitetura funciona **para aquele
formato específico** — sempre com Gate de decisão, quase sempre com Agent.
Este ciclo testa a hipótese contrária.

---

## 2. O que é estruturalmente diferente aqui

| Dimensão | Ciclos 1–6 (revisão de código/release) | Ciclo 7 (documentação de API) |
|---|---|---|
| Agent envolvido | Sim, em 3 dos 4 Workflows | **Nenhum** |
| Tipo de Gate | `GATE_APPROVAL` (Decision institucional) | **`GATE_AUTO`** (Evidence, sem Decision) — primeira vez |
| Branch/Decision Point | Presente no Ciclo 2 e implícito no 5 | Ausente — pipeline puramente linear |
| Vinculação normativa | Sempre via Policy (derivada) | Via `standards_bound` direto na Skill (local) — Policy nem existe para este domínio |
| Papel do "gate" | Decidir se um humano/Agent aprova | Decidir se o pipeline falha automaticamente |

---

## 3. GATE_AUTO — a peça que faltava

Workflow Architecture §4 sempre definiu dois tipos de Gate:

```
Gate (automatizado)  →  realizado como uma Execution que produz Evidence
Gate (aprovação)     →  realizado como uma Decision que produz Decision Record
```

Os cinco Workflows anteriores usaram exclusivamente o segundo. Aqui,
`step.check-completeness` é `kind: GATE_AUTO`: sua Execution produz
`completeness_report` (um Artifact/Evidence comum), e o `failure_policy`
reage diretamente ao conteúdo desse Artifact — **sem** nenhum `Role`
envolvido, sem `ClassifyAgentOutput` (Agent §9), sem `RoleAssignment`. É
estruturalmente mais simples que tudo que veio antes, e essa simplicidade
é o ponto: nem todo gate precisa de autoridade institucional.

```
Execution de step.check-completeness → Completed, produz completeness_report
  → completeness_report.violations = []  →  Workflow prossegue (implícito: fim, sucesso)
  → completeness_report.violations ≠ []  →  failure_policy.on_failure=ABORT dispara
```

---

## 4. Vinculação normativa sem Policy

Nenhuma Policy foi criada para este domínio. `core/skill.documentation.
completeness-check` vincula o Standard diretamente via `metadata.
standards_bound` (Kernel §2.14) — o mecanismo **local e explícito** que
Policy Architecture §7.5 sempre disse coexistir com o mecanismo **derivado**
(Policy), nunca exigir os dois. Os seis ciclos anteriores usavam quase
sempre Policy; este mostra o outro caminho legítimo, exercitado pela
primeira vez sozinho (sem nenhuma Policy do domínio presente).

---

## 5. O que isso prova, em conjunto com os seis ciclos anteriores

- Um Workflow **não precisa** de Agent, Decision, Gate de aprovação ou
  Branch para ser válido — um pipeline linear de duas Skills já satisfaz
  toda a arquitetura.
- `GATE_AUTO` funciona exatamente como descrito desde Workflow §4, sem
  nenhuma peça adicional.
- Vinculação normativa local (`standards_bound`) e derivada (`Policy`) são
  intercambiáveis por design, não uma substituindo a outra por acidente de
  domínio.
- O padrão de Skill generativa + Templates (Ciclo 1) e Skill funcional sem
  Templates (Ciclos 5 e este) continuam coexistindo sem atrito no mesmo
  repositório.

**Sete ciclos, dois domínios, nenhum mecanismo além dos 20 documentos de
arquitetura ratificados.**
