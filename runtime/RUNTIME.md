# Runtime — primeira implementação executável do Framework Eng

*Não é um documento de arquitetura. É a implementação (código Python real,
em `runtime/`) do que os documentos institucionais já especificam —
Registry, Discovery, Composition, Workflow, Execution, Template, Skill.
Nenhuma regra nova. Nenhum conceito novo. Onde uma decisão de implementação
era inevitável e nenhum documento a determinava (formato de string de
`version_range`, algoritmo concreto de detecção de ciclo), isso está
declarado explicitamente no código e aqui — nunca silenciosamente.*

---

## 1. O que existe agora que não existia antes

Até esta tarefa, nada neste repositório executava — `docs/architecture/`
é especificação, `components/`/`records/` é conteúdo ilustrativo validado
manualmente (ver `components/README.md`), e o Caminho B (`.claude/`) traduz
uma fatia para o Claude Code. **Nenhum dos três produz, por si, o resultado
de rodar `ResolveSlot`, `Expand()` ou `Dispatch()` de verdade.**

`runtime/` é isso: uma implementação real, testada com dado real, dos sete
mecanismos pedidos. `python3 -m runtime.demo.run_demo` (a partir da raiz do
repositório) executa a cadeia completa e imprime cada etapa.

## 2. Estrutura

```
runtime/
  contracts/      Component Contract (15 campos, Kernel §2), Lifecycle (Kernel §3),
                   Coordinate/VersionedIdentifier/ULID (Identity §4), detecção de
                   ciclo compartilhada (Kernel §7 — um único mecanismo, reutilizado
                   por composition/template/workflow, nunca reimplementado por módulo)
  registry/        Registry (resolve/register/lineage/manifest_digest/validação
                   estrutural — Registry & Discovery §6, §8, Kernel §8),
                   discovery.py (search — §6.2), loader.py (YAML institucional -> Manifest)
  validation/      Certification mínima (L0-L4, integridade por manifest_digest —
                   Validation & Certification §5-§6) — só o que Composition precisa ler
  composition/     Slot (§4), ResolveSlot (§7) — verbatim
  template/        Template/Variable/Placeholder (§4.2), ResolveEffectiveTemplate,
                   BindVariables, Expand, ClassifyTemplateChange (§11) — verbatim
  skill/           InvokeSkillStep (Skill §9) — orquestração pura dos módulos acima
  execution/       Execution/Context/Context Snapshot/Artifact/Evidence (Execution §4,
                   Domain Model §8), Plan/Dispatch/Recover/Rollback (Execution §7)
  workflow/        Phase/Step/FailurePolicy (§4), ValidateWorkflowGraph,
                   EvaluateDecisionPoint (§7), run_workflow (orquestração de ponta a ponta)
  demo/            run_demo.py (demonstração obrigatória) + check_error_paths.py
                   (caminhos negativos — não pedido explicitamente, feito para não
                   afirmar fidelidade sem checar também as regras MUST NOT)
```

Nenhum módulo importa "para cima" na lista acima — `contracts` não conhece
`registry`; `registry` não conhece `composition`; e assim por diante. Isso
não é estilo, é a mesma disciplina de acoplamento que Kernel §11
(Interoperabilidade) exige entre Components: comunicação só pelo contrato
declarado, nunca por acoplamento oculto.

## 3. O que foi reaproveitado literalmente (não reimplementado por módulo)

- **Detecção de ciclo (Kernel §7):** um único `detect_cycle()` em
  `contracts/graph.py`. Composition, Template e Workflow chamam essa mesma
  função — nenhum dos três tem sua própria cópia, exatamente como os
  próprios documentos afirmam ("6ª aplicação", "3ª aplicação" etc.).
- **`Assembly` (Composition §4):** o mesmo Artifact genérico é o que
  `bind_variables` consulta para `binding_source=COMPOSITION_RESOLVED`
  (Template §5.2) — nenhuma estrutura paralela.
- **`Artifact` genérico (Domain Model §2 #7):** Assembly, ExpandedTemplate,
  Execution Plan e a saída final de uma Skill são todos a mesma classe
  Python (`execution/model.py:Artifact`), nunca especializados — mesma
  disciplina de "reusar Artifact, nunca criar subtipo" que os documentos
  aplicam entre si.
- **`Evidence` como especialização de Artifact (Domain Model §3):**
  implementada como tal, não como entidade irmã.

## 4. Demonstração obrigatória — o que ela prova

`python3 -m runtime.demo.run_demo` carrega o Manifest **real** e já
certificado (Ciclo 3) de `components/core/skill.static-analysis.code-
review.yaml` — nada é dado sintético no nível da Skill. Constrói um
Workflow mínimo (uma Phase, um Step, um Slot) porque os Workflows reais do
piloto (`core/workflow.pull-request-review`, etc.) envolvem um Agent na
segunda fase, e Agent está fora de escopo desta tarefa.

Executa, com saída impressa e verificada nesta sessão (não apenas
afirmada):

1. **Registry** carrega o YAML, calcula `manifest_digest` real (SHA-256
   sobre serialização canônica), valida os 15 campos, registra (exigindo
   `decision_record_ref`, R1).
2. **Certification** mínima concede L2 usando o digest real computado —
   não o placeholder ilustrativo (`sha256:PLACEHOLDER...`) que já existia
   em `records/certification/*.yaml`, que nunca foi de fato calculado.
3. **Discovery** (`search`) encontra a Skill por `capability`.
4. **Composition** (`ResolveSlot`) resolve o Slot do Step contra o
   candidato certificado.
5. **Execution** (`Dispatch`) cria uma Execution real: Context Snapshot
   capturado **antes** de `Running` (RFC-DM-001 C2 / EX2), nunca depois.
6. **Template**: o `PROMPT Template` (`prompt.main`) é resolvido, tem suas
   Variables vinculadas (`diff` via PARAMETER, `language` via
   PARAMETER-com-default) e expandido — vira a entrada do processamento
   opaco. O `OUTPUT Template` (`output.review_report`) é então resolvido,
   vinculado (`findings` do resultado do processamento via PARAMETER,
   `generated_at` do Context Snapshot via CONTEXT — nunca recalculado) e
   expandido — vira o Artifact final.
7. **Evidence**: uma verificação estrutural mínima (não o pipeline de
   Testing Architecture) confirma que o Artifact contém o achado esperado.
8. **O outro ramo do Skill Runtime**: `core/skill.security.dependency-
   audit`, que **não tem `templates[]`** (única Skill do piloto sem
   Templates), é invocada pelo mesmo `invoke_skill_step` — prova que o
   caminho "sem Templates" (Skill §5, ESCOLHA DE DESIGN) funciona sem
   nenhum código condicional especial no chamador.

Um segundo script, `check_error_paths.py`, verifica que os caminhos
negativos também se comportam como documentado: `Unauthorized` sem
`decision_record_ref`; `SlotError` quando a Certificação não atinge o
mínimo; `SKIPPED` (não erro) para um Slot opcional sem candidato; e a
proibição EX1 de reabrir uma Execution terminal.

## 5. Duas lacunas reais encontradas ao implementar — registradas, não escondidas

Consistente com a disciplina já usada nesta sessão (erros reais encontrados
durante instanciação são corrigidos ou registrados com nota explícita,
nunca silenciados):

### 5.1 `Step.params` — campo referenciado, nunca listado

Template Architecture §5.2 e Skill Architecture §9 referenciam
`Step.params` por nome (é a origem de `binding_source = PARAMETER`), mas o
struct de `Step` em Workflow Architecture §4 não o lista entre seus campos
(`id, slot, kind, failure_policy, timeout, compensated_by`). Não é um
conceito inexistente — já é usado por dois documentos ratificados — é uma
omissão pontual na listagem de campos de um terceiro. Este runtime adiciona
`params: dict` ao `Step` (`workflow/model.py`), documentado no código.
**Candidato a emenda de uma linha em Workflow Architecture §4** (MINOR,
aditiva, mesmo padrão já usado para a emenda v1.1.0 de Compliance
Architecture) — não implementada aqui porque está fora do escopo desta
tarefa (implementar o Runtime, não emendar arquitetura), mas sinalizada
explicitamente para decisão, não corrigida por conta própria em um
documento ratificado.

### 5.2 "Timeline" pedido para Execution Runtime é, formalmente, Observability

A tarefa pede "Timeline" entre os itens do Execution Runtime, mas o
construto nomeado `Execution Timeline` (reordenação por tempo de uma
orquestração inteira, consultável via `timeline(orchestration_id)`) é
definido em Observability Architecture §5.3 — documento cuja implementação
esta tarefa explicitamente exclui. **Não interrompi a implementação por
isso**, porque a peça que Execution genuinamente precisa (cada Execution
sabe sua própria sequência de transições — Initiated, Running, Completed —
com timestamp) já é implícita ao próprio Lifecycle (Domain Model §8) e não
depende de nenhum serviço de consulta cross-orquestração. O que foi
implementado (`Execution.transitions`, uma lista ordenada intrínseca à
própria Execution) é deliberadamente **mais estreito** que Observability's
`ExecutionTimeline` — sem `trace()`, sem `Span`, sem serviço de consulta
sobre múltiplas Executions. Se o pedido era pela superfície completa de
Observability, isso ainda não existe aqui — precisaria da implementação de
Observability Architecture (documento 16, já ratificado, mas fora do
escopo desta tarefa por instrução explícita).

## 6. O que NÃO foi implementado (por instrução explícita, não por lacuna)

Agent, Memory, Knowledge, Multi-Agent, Observability (além da nota acima),
Testing, Security, SDK, Marketplace — nenhum destes tem código em
`runtime/`. Certification (Validation & Certification) tem apenas a leitura
mínima que Composition exige (§5 da tarefa não a lista como módulo, mas
Composition §7 não funciona sem ela) — não o pipeline completo de Evidence/
Score/Certifier humano/Suspensão/Revogação.

## 7. Como rodar

```bash
cd framework_eng
python3 -m runtime.demo.run_demo           # demonstração obrigatória
python3 -m runtime.demo.check_error_paths  # caminhos negativos (suplementar)
```

Sem dependências além de `pyyaml` (já usado no restante do projeto) e a
biblioteca padrão do Python 3.
