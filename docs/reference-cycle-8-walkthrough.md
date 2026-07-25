# Reference Cycle 8 — Bundle: Exportação, Verificação, Importação

*Companion de `bundles/core.workflow.pull-request-review.bundle.yaml`.*

---

## 1. O último documento de arquitetura sem conteúdo

Dos 20 documentos ratificados, Packaging & Distribution era o único sem
nenhum conteúdo real exercitando-o. Este ciclo fecha isso, usando o cenário
para o qual aquele documento foi desenhado: transportar Components para
**fora** do Registry institucional deste repositório — não entre
`core/` e `org.acme-corp` (que já compartilham o mesmo Registry lógico,
Registry §1, e por isso nunca precisaram de Bundle), mas para um
**deployment hipoteticamente separado**, chamado aqui de "Deployment B" —
ilustrativo, fora deste repositório, exatamente o caso de uso real de
portabilidade (ex.: instalação air-gapped, outra instância do Framework).

---

## 2. Exportação e verificação

```
export_bundle(core/workflow.pull-request-review@1.0.0,
              include_dependency_closure=true,
              include_certification_evidence=true)

  → Composition.resolve_assembly percorre os `pinned_coordinate` dos Steps
    → core/skill.static-analysis.code-review@1.0.0
    → core/agent.code-reviewer@1.0.0
  → cada Manifest serializado canonicamente (Identity §4.4), digest computado
  → certification_evidence anexada (L4 de ambos — records/certification/)
  → Bundle materializado: bundles/core.workflow.pull-request-review.bundle.yaml

"Deployment B" recebe o arquivo (transporte fora de escopo — Packaging §3.2)

verify_bundle(bundle):
  PARA CADA manifest EM bundle.manifests:
     digest_recomputado ← ComputeDigest(Serialize(manifest))
     ASSERT digest_recomputado == manifest.manifest_digest
  → PASS (neste ciclo) — nenhuma adulteração
  → SE qualquer byte do Manifest tivesse mudado em trânsito: FAIL(DIGEST_MISMATCH),
    Bundle inteiro rejeitado (PK10) — nenhuma aceitação parcial
```

---

## 3. Importação — e o erro que este exercício deliberadamente expõe

```
import_bundle(bundle, target_namespace="core")   # Deployment B também usa "core" como raiz compartilhada

PARA CADA (coordinate, manifest, digest) EM bundle.manifests:
   Governance.Admit(coordinate, manifest, requested_by)   # §7 — SEM atalho, PK3
   Registry.register(...)
→ os três Manifests (Workflow, Skill, Agent) admitidos com sucesso em Deployment B
```

**Neste ponto, a importação estrutural teve sucesso — e é exatamente aqui
que um operador incauto declararia o Workflow "pronto para uso" em
Deployment B. Estaria errado.**

`bundles/....bundle.yaml` já documentava, em `not_included_by_design`, que
`core/standard.code-quality.review-baseline@1.0.0`,
`core/standard.governance.agent-decision-integrity@1.0.0` e
`core/policy.code-quality.mandatory-review@1.0.0` **não** viajam com este
Bundle — não são dependências de Composition, são vinculação normativa.

```
Primeira invocação real do Workflow em Deployment B:
  step.run-code-review dispatch
    → Policy check (applies_at=EXECUTION, BLOCKING)
    → PolicyEval tenta resolver Effective Policy Set
    → core/policy.code-quality.mandatory-review NÃO EXISTE em Deployment B
    → EPS = ∅ (nenhuma Policy aplicável) — a Execution NÃO É bloqueada por
      ausência de Policy (Policy §14/F11: EPS vazio é resultado legítimo)
    → mas Skill.metadata.standards_bound="" também está ausente de facto,
      porque o próprio Standard core/standard.code-quality.review-baseline
      não existe no Registry de Deployment B
    → Certification.current_level consultada por Composition.ResolveSlot
      ainda funciona (a Evidence de certificação viajou como
      certification_evidence — mas é ADVISÓRIA, PK4) — o Slot resolve
    → a Execution PROSSEGUE, mas SEM NENHUMA das duas garantias normativas
      que existiam no repositório de origem
```

**A consequência real não é um erro travado — é um Workflow que roda,
aparentemente com sucesso, mas silenciosamente sem as garantias de
qualidade que o justificavam.** Isso não é uma falha da arquitetura: é
exatamente o motivo pelo qual Packaging §6.3/§9 documenta explicitamente
que Standards e Policies não fazem parte do fecho de Composition — a
arquitetura nunca prometeu que "importar o Workflow" bastasse. O erro é
operacional (esquecer de exportar os Standards/Policies junto), não
arquitetural, e este ciclo o torna visível em vez de escondê-lo.

**Correção:** Deployment B precisaria de dois Bundles adicionais —
`core/standard.code-quality.review-baseline@1.0.0` e
`core/standard.governance.agent-decision-integrity@1.0.0` — mais o Bundle
de `core/policy.code-quality.mandatory-review@1.0.0`, importados **antes**
de qualquer Execution real ser disparada.

---

## 4. Evidência de Certificação é advisória, não vinculante (PK4)

Mesmo com `certification_evidence` presente no Bundle, a Certificação L4
**não é automaticamente restabelecida** em Deployment B — sua autoridade de
Certificação é local (Governance §4/§8 de Deployment B, distinta da deste
repositório). O que o operador de Deployment B ganha é **Evidence de
suporte** que **MAY** acelerar uma recertificação local (ex.: pular
diretamente para revisão do Certifier, sem refazer Testing do zero) — nunca
uma Certificação já válida por transitividade.

---

## 5. O que este ciclo prova, em conjunto com os sete anteriores

- `Bundle` funciona exatamente como especificado: digest protege contra
  adulteração, Admissão nunca é contornada, evidência de Certificação nunca
  cruza fronteira de autoridade automaticamente.
- O fecho de dependências de Composition é **real e limitado** — inclui
  Providers resolvidos por Slot, não inclui vinculação normativa. Isso não
  é uma lacuna: é uma fronteira de responsabilidade deliberada (Packaging
  §3.2), e este ciclo mostra a consequência prática de não respeitá-la.
- Dos 20 documentos de arquitetura, todos os que produzem algo transportável
  agora têm pelo menos um exemplo real: Standard, Policy, Skill, Agent,
  Workflow, Organization, Certificação, RoleAssignment, Knowledge/Knowledge
  Asset, e agora Bundle.

**Oito ciclos, dois domínios, um erro operacional deliberadamente exposto
(não escondido), nenhum mecanismo além dos 20 documentos ratificados.**
