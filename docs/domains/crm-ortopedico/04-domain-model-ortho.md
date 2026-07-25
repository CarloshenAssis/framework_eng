# Domain Model v1.0.0 — CRM Equipamentos Ortopédicos

**Base:** Framework Eng Domain Model v1.1.0  
**Entidades:** 14 fundamentais

---

## 1. Entidades Fundamentais

### 1.1 Equipamento
| Campo | Tipo | Regras |
|-------|------|--------|
| id | ULID | Gerado pelo sistema |
| codigo | string | Único, formato `TIPO-NNNN` (ex: CAD-0001) |
| tipo | enum | Cadeira de Rodas, Muletas, Andador, Cadeira de Banho |
| marca | string | Ortobras, Jaguaribe, Mobilator, Dellamed, Ortopé |
| modelo | string | Livre, mas obrigatório |
| patrimonio | string | Código patrimonial da Prefeitura (PM-XXXXX) |
| serial | string | Número de série do fabricante |
| data_aquisicao | date | Obrigatório |
| origem | enum | Compra, Doação |
| tamanho | enum | Adulto, Infantil |
| peso_suportado | string | Ex: "120 kg" |
| status | enum | Disponível, Emprestado, Manutenção, Baixado |
| observacoes | text | Livre |
| fotos | List<Foto> | Principal, lateral, traseira, patrimônio |

**Lifecycle (Kernel §3):**
```
Disponível → Emprestado → Devolvido → Disponível
Disponível → Manutenção → Concluído → Disponível
Disponível → Baixado (irreversível)
Emprestado → Renovação → Emprestado (prazo estendido)
```

### 1.2 Beneficiario
| Campo | Tipo | Regras |
|-------|------|--------|
| id | ULID | Único |
| nome | string | Obrigatório |
| cpf | string | Único, validado via algoritmo |
| rg | string | Obrigatório |
| data_nascimento | date | Obrigatório |
| telefone | string | Com DDD |
| whatsapp | string | Para notificações |
| email | string | Opcional |
| endereco | string | Rua, número |
| cidade | string | Default: São José dos Campos |
| bairro | string | Obrigatório |
| cep | string | Validado |
| contato_emergencia_nome | string | Obrigatório |
| contato_emergencia_telefone | string | Obrigatório |
| contato_emergencia_relacao | string | Filha, Esposa, etc. |
| status | enum | Ativo, Com Empréstimo, Em Atraso |

### 1.3 Emprestimo
| Campo | Tipo | Regras |
|-------|------|--------|
| id | ULID | Único |
| equipamento_id | FK | Referência a Equipamento |
| beneficiario_id | FK | Referência a Beneficiario |
| data_emprestimo | datetime | Auto (now) |
| data_prevista_devolucao | date | Calculada do prazo |
| data_devolucao_real | datetime | Null até devolução |
| prazo_dias | int | 30, 60, 90 ou personalizado |
| status | enum | Ativo, Devolvido, Atrasado, Renovado |
| atendente_id | FK | Quem registrou |
| checklist_entrega | Checklist | JSON estruturado |
| fotos_entrega | List<Foto> | Evidência |
| assinatura_tipo | enum | Digital, Foto do Termo |
| assinatura_dados | blob | SVG ou imagem |

### 1.4 Devolucao
| Campo | Tipo | Regras |
|-------|------|--------|
| id | ULID | Único |
| emprestimo_id | FK | Referência |
| data_devolucao | datetime | Auto (now) |
| checklist_devolucao | Checklist | JSON estruturado |
| fotos_devolucao | List<Foto> | Evidência obrigatória |
| observacoes | text | Problemas encontrados |
| destino_final | enum | Disponível, Manutenção |
| atendente_id | FK | Quem recebeu |

### 1.5 Manutencao
| Campo | Tipo | Regras |
|-------|------|--------|
| id | ULID | Único |
| equipamento_id | FK | Referência |
| problema | string | Descrição do defeito |
| fornecedor | string | Quem vai consertar |
| responsavel | string | Interno/externo |
| data_entrada | date | Início da manutenção |
| data_conclusao | date | Null até terminar |
| valor | decimal | Custo do reparo |
| status | enum | Aguardando, Concluído |

### 1.6 Foto
| Campo | Tipo | Regras |
|-------|------|--------|
| id | ULID | Único |
| entidade_tipo | enum | Equipamento, Emprestimo, Devolucao |
| entidade_id | FK | Referência polimórfica |
| categoria | enum | Principal, Lateral, Traseira, Patrimônio, Entrega, Devolucao |
| url | string | Caminho no storage |
| timestamp | datetime | Quando foi tirada |

### 1.7 Notificacao
| Campo | Tipo | Regras |
|-------|------|--------|
| id | ULID | Único |
| tipo | enum | Confirmacao, Lembrete 7d, Vencimento, Atraso |
| beneficiario_id | FK | Destinatário |
| emprestimo_id | FK | Referência |
| canal | enum | WhatsApp, SMS, Email |
| status | enum | Enviada, Entregue, Falha |
| conteudo | text | Texto da mensagem |
| enviada_em | datetime | Timestamp |

### 1.8 Usuario (Atendente/Admin)
| Campo | Tipo | Regras |
|-------|------|--------|
| id | ULID | Único |
| nome | string | Obrigatório |
| email | string | Único |
| perfil | enum | Administrador, Atendente, Gestor, Manutenção |
| ativo | boolean | Default true |

### 1.9 Auditoria (Log)
| Campo | Tipo | Regras |
|-------|------|--------|
| id | ULID | Único |
| entidade_tipo | string | Qual tabela |
| entidade_id | FK | Qual registro |
| acao | enum | Criar, Atualizar, Excluir (soft) |
| dados_anteriores | JSON | Snapshot antes |
| dados_novos | JSON | Snapshot depois |
| usuario_id | FK | Quem fez |
| timestamp | datetime | Quando |

---

## 2. Relacionamentos (derives_from)

```
Equipamento 1---* Emprestimo
Beneficiario 1---* Emprestimo
Emprestimo 1---1 Devolucao (opcional)
Equipamento 1---* Manutencao
Emprestimo 1---* Notificacao
Usuario 1---* Emprestimo (como atendente)
Usuario 1---* Devolucao (como atendente)
```

## 3. Value Objects Escapados a Component

- **Checklist**: `{rodas: bool, freios: bool, apoio_braco: bool, apoio_pe: bool, ferrugem: bool, higienizado: bool}`
- **Endereco**: `{rua, numero, complemento, bairro, cidade, cep}`
- **Periodo**: `{data_inicio, data_fim}`

---

*Documento ratificado conforme Framework Eng — Domain Model (Doc 04)*
