# Constituição — CRM Equipamentos Ortopédicos

**Versão:** 1.0.0  
**Data:** 2026-07-25  
**Domínio:** Gestão de Equipamentos Ortopédicos — Secretaria de Assistência Social  
**Framework:** Framework Eng v1.1.0

---

## 1. Princípios Permanentes

1. **Rastreabilidade Total**: Todo equipamento público deve ter histórico completo de movimentação, desde a aquisição até a baixa.
2. **Acessibilidade Operacional**: O sistema deve funcionar tanto em desktop (secretaria) quanto em mobile (campo/entrega).
3. **Conformidade Legal**: Atender à Lei de Acesso à Informação (LAI) e às normas de auditoria do TCE/TCU sobre bens públicos.
4. **Autonomia do Beneficiário**: O beneficiário deve receber confirmação por WhatsApp e ter visibilidade do prazo de devolução.
5. **Integridade de Dados**: Fotos de entrega e devolução são evidência obrigatória; checklist é registro imutável.

## 2. Hierarquia de Decisões

| Nível | Decisor | Escopo |
|-------|---------|--------|
| Estratégico | Secretário de Assistência Social | Política de aquisição, parcerias, orçamento |
| Tático | Coordenador do Centro Operacional | Definição de prazos padrão, regras de renovação |
| Operacional | Atendente/Assistente Social | Empréstimo, devolução, manutenção no dia a dia |
| Sistema | Agentes automatizados | Notificações de vencimento, alertas de atraso |

## 3. Regras Imutáveis (MUST NOT)

- R1: Não é permitido emprestar equipamento marcado como "Baixado" ou "Em Manutenção".
- R2: Não é permitido registrar devolução sem foto de evidência.
- R3: Não é permitido excluir permanentemente um registro de empréstimo; apenas anular com justificativa.
- R4: Não é permitido alterar o prazo de devolução sem aprovação do coordenador (GATE_APPROVAL).
- R5: Não é permitido cadastrar beneficiário sem CPF e comprovante de residência.

## 4. Regras Mutáveis (SHOULD)

- S1: O prazo padrão de empréstimo é 30 dias, podendo ser estendido para 60 ou 90.
- S2: A notificação de vencimento deve ser enviada 7 dias antes, no dia do vencimento e após 7 dias de atraso.
- S3: Equipamentos com mais de 3 empréstimos no ano devem passar por revisão técnica.

---

*Documento ratificado conforme Framework Eng — Constitution (Doc 01)*
