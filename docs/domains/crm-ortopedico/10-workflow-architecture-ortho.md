# Workflow Architecture v1.0.0 — CRM Equipamentos Ortopédicos

**Base:** Framework Eng Workflow Architecture v1.1.0  
**Workflows definidos:** 3 principais + 2 auxiliares

---

## 1. Workflow: wf-emprestimo (Novo Empréstimo)

**Trigger:** Usuário clica "+ Novo Empréstimo"  
**Goal:** Registrar empréstimo com evidência completa  
**FailurePolicy:** ROLLBACK (se falhar no passo 4 ou 5, desfaz reserva do equipamento)

```
Phase: identificacao
  Step 1.1: buscar_beneficiario
    Slot: beneficiario_id
    Kind: HUMAN_INPUT
    Gate: GATE_AUTO
    Params:
      binding_source: PARAMETER
      search_fields: [cpf, nome, telefone]

  Step 1.2: validar_beneficiario
    Slot: validacao_beneficiario
    Kind: SYSTEM
    Gate: GATE_AUTO
    Validation: CPF válido, sem atrasos pendentes, documentos completos

Phase: selecao
  Step 2.1: buscar_equipamento
    Slot: equipamento_id
    Kind: HUMAN_INPUT
    Gate: GATE_AUTO
    Params:
      binding_source: PARAMETER
      filter: status = 'Disponível'

  Step 2.2: reservar_equipamento
    Slot: reserva
    Kind: SYSTEM
    Gate: GATE_AUTO
    Action: UPDATE equipamento.status = 'Reservado'

Phase: configuracao
  Step 3.1: definir_prazo
    Slot: prazo_dias
    Kind: HUMAN_INPUT
    Gate: GATE_AUTO
    Params:
      binding_source: PARAMETER
      options: [30, 60, 90, 'Personalizado']

  Step 3.2: calcular_vencimento
    Slot: data_prevista_devolucao
    Kind: SYSTEM
    Gate: GATE_AUTO
    Action: data_emprestimo + prazo_dias

Phase: evidencia
  Step 4.1: checklist_entrega
    Slot: checklist_entrega
    Kind: HUMAN_INPUT
    Gate: GATE_AUTO
    Params:
      binding_source: PARAMETER
      items: [rodas, freios, apoio_braco, apoio_pe, ferrugem, higienizado]

  Step 4.2: fotos_entrega
    Slot: fotos_entrega
    Kind: HUMAN_INPUT
    Gate: GATE_AUTO
    Validation: Mínimo 2 fotos (frontal + lateral)

  Step 4.3: assinatura_termo
    Slot: assinatura
    Kind: HUMAN_INPUT
    Gate: GATE_AUTO
    Options: [digital, foto_termo]

Phase: confirmacao
  Step 5.1: revisar_dados
    Slot: revisao
    Kind: HUMAN_INPUT
    Gate: GATE_APPROVAL
    Display: Beneficiário, Equipamento, Prazo, Vencimento, Checklist

  Step 5.2: confirmar_emprestimo
    Slot: confirmacao
    Kind: SYSTEM
    Gate: GATE_AUTO
    Actions:
      - INSERT Emprestimo
      - UPDATE Equipamento.status = 'Emprestado'
      - INSERT Notificacao (tipo: Confirmacao)
      - DISPATCH Skill: notificacao-whatsapp

  Step 5.3: gerar_evidencia
    Slot: artifact
    Kind: SYSTEM
    Gate: GATE_AUTO
    Action: Gerar Context Snapshot (RFC-DM-001 C2)
```

**Compensation (Saga):**
- Se falhar após Step 2.2: liberar reserva do equipamento
- Se falhar após Step 5.2: marcar empréstimo como CANCELADO, liberar equipamento

---

## 2. Workflow: wf-devolucao (Devolução)

**Trigger:** Usuário clica "Devolver" ou QR Code scan  
**Goal:** Registrar devolução com evidência e definir destino final  
**FailurePolicy:** RETRY (3 tentativas, depois ALERT)

```
Phase: localizacao
  Step 1.1: buscar_emprestimo_ativo
    Slot: emprestimo_id
    Kind: HUMAN_INPUT | QR_SCAN
    Gate: GATE_AUTO

  Step 1.2: validar_prazo
    Slot: situacao_prazo
    Kind: SYSTEM
    Gate: GATE_AUTO
    Action: Calcular dias de atraso (se houver)

Phase: recebimento
  Step 2.1: checklist_devolucao
    Slot: checklist_devolucao
    Kind: HUMAN_INPUT
    Gate: GATE_AUTO
    Items: [estado_igual, limpa, funcionando]

  Step 2.2: fotos_devolucao
    Slot: fotos_devolucao
    Kind: HUMAN_INPUT
    Gate: GATE_AUTO
    Validation: Obrigatório mínimo 1 foto

  Step 2.3: registrar_problemas
    Slot: problemas
    Kind: HUMAN_INPUT
    Gate: GATE_AUTO
    Options: [pequeno_risco, pneu_furado, freio_quebrado, nenhum]

Phase: destino
  Step 3.1: definir_destino
    Slot: destino_final
    Kind: HUMAN_INPUT
    Gate: GATE_APPROVAL (se problemas selecionados)
    Options: [Disponível, Manutenção]

  Step 3.2: confirmar_devolucao
    Slot: confirmacao
    Kind: SYSTEM
    Gate: GATE_AUTO
    Actions:
      - UPDATE Emprestimo.status = 'Devolvido'
      - UPDATE Emprestimo.data_devolucao_real = now()
      - UPDATE Equipamento.status = destino_final
      - IF destino = 'Manutenção' THEN INSERT Manutencao
      - INSERT Notificacao (tipo: Confirmacao_Devolucao)
      - DISPATCH Skill: notificacao-whatsapp
```

---

## 3. Workflow: wf-manutencao (Manutenção)

**Trigger:** Equipamento enviado para manutenção  
**Goal:** Rastrear reparo até disponibilização  
**FailurePolicy:** ALERT (notificar gestor se ultrapassar 15 dias)

```
Phase: entrada
  Step 1.1: registrar_problema
    Slot: problema
    Kind: HUMAN_INPUT
    Gate: GATE_AUTO

  Step 1.2: designar_fornecedor
    Slot: fornecedor
    Kind: HUMAN_INPUT
    Gate: GATE_AUTO

  Step 1.3: orcar_valor
    Slot: valor
    Kind: HUMAN_INPUT
    Gate: GATE_APPROVAL (se valor > R$ 500)

Phase: execucao
  Step 2.1: acompanhar_reparo
    Slot: status_reparo
    Kind: SYSTEM
    Gate: GATE_AUTO
    Timeout: 15 dias → ALERT

  Step 2.2: registrar_conclusao
    Slot: conclusao
    Kind: HUMAN_INPUT
    Gate: GATE_AUTO
    Action: UPDATE Manutencao.status = 'Concluído'

Phase: liberacao
  Step 3.1: liberar_equipamento
    Slot: liberacao
    Kind: SYSTEM
    Gate: GATE_AUTO
    Actions:
      - UPDATE Equipamento.status = 'Disponível'
      - INSERT Auditoria
```

---

## 4. Workflow Auxiliar: wf-notificacao-automatica

**Trigger:** CRON diário 06:00  
**Goal:** Enviar lembretes e alertas  
**Kind:** FULLY_AUTOMATED

```
Phase: scan
  Step 1.1: detectar_vencimentos_7d
    Slot: lista_7d
    Kind: SYSTEM
    Gate: GATE_AUTO

  Step 1.2: detectar_vencimentos_hoje
    Slot: lista_hoje
    Kind: SYSTEM
    Gate: GATE_AUTO

  Step 1.3: detectar_atrasos
    Slot: lista_atraso
    Kind: SYSTEM
    Gate: GATE_AUTO

Phase: dispatch
  Step 2.1: enviar_notificacoes
    Slot: envios
    Kind: SYSTEM
    Gate: GATE_AUTO
    Action: Para cada item, DISPATCH Skill: notificacao-whatsapp

  Step 2.2: registrar_envios
    Slot: registros
    Kind: SYSTEM
    Gate: GATE_AUTO
    Action: INSERT Notificacao para cada envio
```

---

## 5. Workflow Auxiliar: wf-renovacao

**Trigger:** Beneficiário solicita renovação  
**Goal:** Estender prazo com aprovação  
**FailurePolicy:** ROLLBACK

```
Phase: solicitacao
  Step 1.1: buscar_emprestimo_ativo
    Slot: emprestimo_id
    Kind: HUMAN_INPUT
    Gate: GATE_AUTO

  Step 1.2: verificar_historico
    Slot: historico
    Kind: SYSTEM
    Gate: GATE_AUTO
    Validation: Máximo 2 renovações consecutivas

Phase: aprovacao
  Step 2.1: solicitar_aprovacao
    Slot: aprovacao
    Kind: HUMAN_INPUT
    Gate: GATE_APPROVAL
    Approver: perfil = Gestor

  Step 2.2: atualizar_prazo
    Slot: novo_prazo
    Kind: SYSTEM
    Gate: GATE_AUTO
    Actions:
      - UPDATE Emprestimo.prazo_dias += 30
      - UPDATE Emprestimo.data_prevista_devolucao
      - UPDATE Emprestimo.status = 'Renovado'
      - INSERT Notificacao (tipo: Renovacao)
```

---

*Documento ratificado conforme Framework Eng — Workflow Architecture (Doc 10)*
