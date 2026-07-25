# Ciclo de Referência — CRM Equipamentos Ortopédicos

**Framework:** Framework Eng v1.1.0  
**Aplicação:** Gestão de Equipamentos Ortopédicos — Secretaria de Assistência Social  
**Data:** 2026-07-25

---

## Introdução

Este documento aplica os **12 Ciclos de Referência** do Framework Eng ao domínio do CRM Ortopédico. Cada ciclo descreve o que o sistema instancia, o que prova e como se relaciona com os demais.

---

## Ciclo 1: Standard, Policy, Skill, Agent, Workflow

**O que instancia:** O domínio "revisão de PR" (pull request de código) vira **registro de empréstimo**.

| Framework | CRM Ortopédico |
|-----------|----------------|
| Standard | Regras de empréstimo (prazo máximo, documentação obrigatória) |
| Policy | Política de renovação (máx. 2x), política de atraso (bloqueio) |
| Skill | `gestao-emprestimo` (7 capabilities) |
| Agent | Atendente (humano) + Notificador (automático) |
| Workflow | `wf-emprestimo` (5 fases, 13 steps) |

**O que prova:** A cadeia completa `Composition → Execution → Policy → Agent → Observability` funciona. O Skill `gestao-emprestimo` é um Operational Component puro, sem templates hardcoded — eles são resolvidos via `Template Architecture` (Doc 14).

---

## Ciclo 2: Organização, Standard, Policy, Workflow

**O que instancia:** `org.acme-corp` vira **Prefeitura Municipal / Secretaria de Assistência Social**.

| Framework | CRM Ortopédico |
|-----------|----------------|
| Organização (real) | Secretaria de Assistência Social |
| Standard via `extends` | Normas do SUS, Lei de Acesso à Informação, Portarias do TCE |
| Policy escopada | Política de aquisição de equipamentos, política de doação |
| Workflow com `Branch` | `wf-emprestimo` com branch condicional: se equipamento infantil, exige laudo médico |

**O que prova:** Isolamento multi-tenant (se outras secretarias quiserem usar), extensão normativa segura, acúmulo de policies e roteamento condicional.

---

## Ciclo 3: Certificação L1-L4 da Skill

**O que instancia:** A Skill `gestao-emprestimo` passa por certificação completa.

| Nível | O que é verificado | Artefato no CRM |
|-------|-------------------|-----------------|
| L0 | Sintaxe YAML válida | `skill.gestao-emprestimo.yaml` |
| L1 | Code review | `records/certification/core.gestao-emprestimo.code-review.yaml` |
| L2 | Dependency audit | `records/certification/core.gestao-emprestimo.dependency-audit.yaml` |
| L3 | Security scan | `records/certification/core.gestao-emprestimo.security-scan.yaml` |
| L4 | Runtime test | `runtime/demo/run_demo.py` executa workflow completo |

**O que prova:** O Registry carrega a certificação por read-through. A Skill só é descoberta (`discovery.py`) se todos os níveis estiverem aprovados.

---

## Ciclo 4: Correção de nomenclatura + Certificação do Agent

**O que instancia:** Os gates `human-only-gate` e `high-risk-gate` vira **GATE_AUTO** e **GATE_APPROVAL**.

| Gate | Quando usado | Exemplo no CRM |
|------|-------------|----------------|
| GATE_AUTO | Sem risco, sistema decide sozinho | Buscar beneficiário, calcular vencimento |
| GATE_APPROVAL | Requer aprovação humana | Confirmar empréstimo, aprovar renovação, manutenção > R$ 500 |

**O que prova:** Erro real encontrado e corrigido (AG2): se um atendente tenta aprovar sua própria renovação, o sistema bloqueia. O `RoleAssignment` formaliza que apenas `Gestor` pode aprovar `GATE_APPROVAL`.

---

## Ciclo 5: Validação & Certification Architecture

**O que instancia:** O pipeline de validação L0-L4 vira **verificação de cada empréstimo**.

| Validação | O que verifica | No CRM |
|-----------|---------------|--------|
| L0 | Sintaxe do manifesto | YAML do workflow válido |
| L1 | Code review do contrato | `ortho_contracts.py` revisado |
| L2 | Dependências | WhatsApp Gateway, Storage de fotos |
| L3 | Security scan | Dados de CPF, fotos de beneficiários |
| L4 | Runtime test | Workflow executado com dados reais |

**O que prova:** A Skill do Ciclo 1 só é publicada se L1-L4 passarem. Isso garante que nenhum empréstimo use uma Skill não certificada.

---

## Ciclo 6: Registry & Discovery

**O que instancia:** Resolução/descoberta de componentes.

| Mecanismo | No CRM |
|-----------|--------|
| Registry Entry | `REGISTRY_ENTRY` em `ortho_contracts.py` |
| Resolve | `ResolveSlot` encontra equipamento disponível por `capability` |
| Redirect | Se equipamento não disponível, redireciona para lista de espera |
| Lineage Index | Rastreia que `Emprestimo E-123` derivou de `Equipamento CAD-0002` e `Beneficiario P-1` |

**O que prova:** O `discovery.py` encontra a Skill `gestao-emprestimo` por `capability = cap-notificar-beneficiario`. O `loader.py` converte YAML institucional em Manifest.

---

## Ciclo 7: Composition + Template + Workflow

**O que instancia:** `detect_cycle()` encontra ciclos entre Composition, Template e Workflow.

| Ciclo detectado | No CRM |
|-----------------|--------|
| Composition → Template | `bind_variables` consulta `binding_source = COMPOSITION_RESOLVED` |
| Template → Workflow | `Step.params` usa `binding_source = PARAMETER` |
| Workflow → Composition | `Phase` contém `Step` que contém `Slot` resolvido por Composition |

**O que prova:** Não há ciclo infinito. O workflow `wf-emprestimo` termina em `Step 5.3` (gerar evidência). O template `confirmacao-emprestimo` é expandido com variáveis do Context.

---

## Ciclo 8: Execution + Domain Model + Context

**O que instancia:** `Dispatch()` cria Execution real.

| Elemento | No CRM |
|----------|--------|
| Context Snapshot (RFC-DM-001 C2) | Capturado ANTES de `Running` — dados do beneficiário, equipamento, checklist |
| Domain Model | `Equipamento`, `Beneficiario`, `Emprestimo` com lifecycle |
| Execution Plan | Sequência de 13 steps do `wf-emprestimo` |
| Artifact final | `ExecutionEvidence` com Provenance Chain |

**O que prova:** Se o sistema cair durante o Step 4.2 (fotos), o `Context Snapshot` permite `Recover` ou `Rollback` sem perda de dados.

---

## Ciclo 9: Agent Architecture (canônico)

**O que instancia:** Substitui o Doc 17 (depreciado).

| Conceito | No CRM |
|----------|--------|
| Goal = conteúdo de Context | O Agent "Atendente" tem como goal registrar um empréstimo válido |
| Action = Step reutilizado | Cada ação do atendente é um Step do workflow |
| Substitui Doc 17 | O Agent não é mais uma entidade separada; é um perfil de usuário que executa Steps |

**O que prova:** O `RoleAssignment` (`records/role-assignment/`) define que `Atendente` pode executar Steps 1.1-4.3, mas não 5.1 (revisão) sem `GATE_APPROVAL`.

---

## Ciclo 10: Testing Architecture (canônica)

**O que instancia:** Substitui o Doc 19 (depreciado).

| Conceito | No CRM |
|----------|--------|
| TestCase / TestKind (11 valores) | Cada Step do workflow é um caso de teste |
| TestResult = Evidence | O resultado do teste é a `Evidence` gerada |
| Coverage = Metric | Cobertura medida por % de Steps executados em demonstração |

**O que prova:** `runtime/demo/run_demo.py` executa todos os 13 steps do `wf-emprestimo`. Se algum falhar, a `Evidence` mostra exatamente qual Step e por quê.

---

## Ciclo 11: Quality Gate Architecture

**O que instancia:** Catálogo de 18 Gates nomeados.

| Gate | Configuração no CRM |
|------|---------------------|
| GATE_AUTO | Steps 1.1, 1.2, 2.1, 2.2, 3.1, 3.2, 4.1, 4.2, 4.3, 5.2, 5.3 |
| GATE_APPROVAL | Steps 5.1 (revisar dados), 2.2.3 (orçamento > R$ 500), 2.2.1 (renovação) |

**O que prova:** A configuração `Step(GATE_AUTO|GATE_APPROVAL)` determina corretamente se uma Partial Conformance satisfaz um Binding STRICT. Se um Step crítico (5.1) não tiver `GATE_APPROVAL`, o Compliance Assessment falha.

---

## Ciclo 12: Security Architecture

**O que instancia:** Catálogo de 21 controles de segurança.

| Controle | Uso no CRM |
|----------|-----------|
| decision_record_ref_required | Todo empréstimo exige `decision_record_ref` (R1) |
| manifest_digest_verification | SHA-256 do manifesto validado antes de execução |
| cpf_encryption | CPF do beneficiário criptografado em repouso |
| foto_access_control | Fotos de entrega/devolução acessíveis apenas por perfil adequado |
| audit_trail_immutable | Log de auditoria (Ciclo 8) não pode ser alterado |

**O que prova:** O `security.dependency-audit` da Skill `gestao-emprestimo` verifica que o WhatsApp Gateway não expõe dados PII. O `security.scan` verifica que fotos não contêm metadados GPS.

---

## Resumo: Como os 12 Ciclos se Conectam

```
Ciclo 1 (Skill) ──registry──→ Ciclo 6 (Discovery)
       │                            │
       ▼                            ▼
Ciclo 3 (Cert) ◄────valida──── Ciclo 5 (Validation)
       │                            │
       ▼                            ▼
Ciclo 7 (Composition) ──resolve──► Ciclo 8 (Execution)
       │                            │
       ▼                            ▼
Ciclo 2 (Org/Policy) ◄──escopo── Ciclo 9 (Agent)
       │                            │
       ▼                            ▼
Ciclo 11 (Quality Gate) ──control──► Ciclo 12 (Security)
       ▲                            │
       └────────────Ciclo 10 (Test)─┘
```

---

*Documento ratificado conforme Framework Eng — Reference Cycle (Doc 25, canônico)*
