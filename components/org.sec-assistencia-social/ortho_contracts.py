"""
Contratos de Componentes — CRM Equipamentos Ortopédicos
Framework Eng — Component Contract (Kernel §2)

Este módulo define os contratos formais das entidades do domínio,
validáveis pelo Runtime do Framework Eng.
"""

from dataclasses import dataclass, field
from datetime import date, datetime
from decimal import Decimal
from enum import Enum, auto
from typing import List, Optional, Dict, Any
from uuid import UUID, uuid4


# ============================================================
# Enums
# ============================================================

class StatusEquipamento(str, Enum):
    DISPONIVEL = "Disponível"
    EMPRESTADO = "Emprestado"
    MANUTENCAO = "Manutenção"
    BAIXADO = "Baixado"
    RESERVADO = "Reservado"  # temporário durante workflow


class TipoEquipamento(str, Enum):
    CADEIRA_RODAS = "Cadeira de Rodas"
    MULETAS = "Muletas"
    ANDADOR = "Andador"
    CADEIRA_BANHO = "Cadeira de Banho"


class OrigemEquipamento(str, Enum):
    COMPRA = "Compra"
    DOACAO = "Doação"


class StatusEmprestimo(str, Enum):
    ATIVO = "Ativo"
    DEVOLVIDO = "Devolvido"
    ATRASADO = "Atrasado"
    RENOVADO = "Renovado"
    CANCELADO = "Cancelado"


class StatusManutencao(str, Enum):
    AGUARDANDO = "Aguardando"
    CONCLUIDO = "Concluído"


class StatusNotificacao(str, Enum):
    ENVIADA = "Enviada"
    ENTREGUE = "Entregue"
    FALHA = "Falha"


class TipoNotificacao(str, Enum):
    CONFIRMACAO = "Confirmacao"
    LEMBRETE_7D = "Lembrete_7d"
    VENCIMENTO = "Vencimento"
    ATRASO = "Atraso"
    RENOVACAO = "Renovacao"
    CONFIRMACAO_DEVOLUCAO = "Confirmacao_Devolucao"


class PerfilUsuario(str, Enum):
    ADMINISTRADOR = "Administrador"
    ATENDENTE = "Atendente"
    GESTOR = "Gestor"
    MANUTENCAO = "Manutenção"


class TipoAssinatura(str, Enum):
    DIGITAL = "Digital"
    FOTO_TERMO = "Foto do Termo"


class DestinoDevolucao(str, Enum):
    DISPONIVEL = "Disponível"
    MANUTENCAO = "Manutenção"


# ============================================================
# Value Objects
# ============================================================

@dataclass(frozen=True)
class Checklist:
    """Value Object imutável para checklist de entrega/devolução."""
    rodas: bool = False
    freios: bool = False
    apoio_braco: bool = False
    apoio_pe: bool = False
    ferrugem: bool = False
    higienizado: bool = False

    def is_completo(self) -> bool:
        return all([
            self.rodas, self.freios, self.apoio_braco,
            self.apoio_pe, self.ferrugem, self.higienizado
        ])


@dataclass(frozen=True)
class Endereco:
    rua: str
    numero: str
    complemento: Optional[str] = None
    bairro: str = ""
    cidade: str = "São José dos Campos"
    cep: str = ""


@dataclass(frozen=True)
class ContatoEmergencia:
    nome: str
    telefone: str
    relacao: str


# ============================================================
# Entidades (Component Contract — 15 campos mínimos)
# ============================================================

@dataclass
class Equipamento:
    """Component: Equipamento (Kernel §2, Identity §4)"""
    # Identity
    id: UUID = field(default_factory=uuid4)
    codigo: str = ""  # TIPO-NNNN

    # Core Attributes (15 campos)
    tipo: TipoEquipamento = TipoEquipamento.CADEIRA_RODAS
    marca: str = ""
    modelo: str = ""
    patrimonio: str = ""  # PM-XXXXX
    serial: str = ""
    data_aquisicao: Optional[date] = None
    origem: OrigemEquipamento = OrigemEquipamento.COMPRA
    tamanho: str = "Adulto"
    peso_suportado: str = ""
    status: StatusEquipamento = StatusEquipamento.DISPONIVEL
    observacoes: str = ""
    fotos: List[Dict[str, Any]] = field(default_factory=list)

    # Lifecycle (Kernel §3)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    # Versioned Identifier (Identity §4)
    version: int = 1

    def pode_emprestar(self) -> bool:
        return self.status == StatusEquipamento.DISPONIVEL

    def pode_baixar(self) -> bool:
        return self.status in (StatusEquipamento.DISPONIVEL, StatusEquipamento.MANUTENCAO)


@dataclass
class Beneficiario:
    """Component: Beneficiario"""
    id: UUID = field(default_factory=uuid4)
    nome: str = ""
    cpf: str = ""
    rg: str = ""
    data_nascimento: Optional[date] = None
    telefone: str = ""
    whatsapp: str = ""
    email: Optional[str] = None
    endereco: Endereco = field(default_factory=lambda: Endereco(rua="", numero="", bairro=""))
    contato_emergencia: Optional[ContatoEmergencia] = None
    status: str = "Ativo"

    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    version: int = 1

    def esta_bloqueado(self) -> bool:
        return self.status == "Em Atraso"


@dataclass
class Emprestimo:
    """Component: Emprestimo — Ciclo de vida principal do sistema"""
    id: UUID = field(default_factory=uuid4)
    equipamento_id: UUID = field(default_factory=uuid4)
    beneficiario_id: UUID = field(default_factory=uuid4)
    atendente_id: UUID = field(default_factory=uuid4)

    data_emprestimo: datetime = field(default_factory=datetime.now)
    data_prevista_devolucao: Optional[date] = None
    data_devolucao_real: Optional[datetime] = None
    prazo_dias: int = 30
    status: StatusEmprestimo = StatusEmprestimo.ATIVO

    checklist_entrega: Checklist = field(default_factory=Checklist)
    fotos_entrega: List[Dict[str, Any]] = field(default_factory=list)
    assinatura_tipo: Optional[TipoAssinatura] = None
    assinatura_dados: Optional[bytes] = None

    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    version: int = 1

    def dias_restantes(self) -> int:
        if not self.data_prevista_devolucao:
            return 0
        return (self.data_prevista_devolucao - date.today()).days

    def esta_atrasado(self) -> bool:
        if self.status != StatusEmprestimo.ATIVO or not self.data_prevista_devolucao:
            return False
        return date.today() > self.data_prevista_devolucao

    def pode_renovar(self, renovacoes_anteriores: int = 0) -> bool:
        return (
            self.status == StatusEmprestimo.ATIVO
            and not self.esta_atrasado()
            and renovacoes_anteriores < 2
        )


@dataclass
class Devolucao:
    """Component: Devolucao"""
    id: UUID = field(default_factory=uuid4)
    emprestimo_id: UUID = field(default_factory=uuid4)
    atendente_id: UUID = field(default_factory=uuid4)

    data_devolucao: datetime = field(default_factory=datetime.now)
    checklist_devolucao: Checklist = field(default_factory=Checklist)
    fotos_devolucao: List[Dict[str, Any]] = field(default_factory=list)
    observacoes: str = ""
    destino_final: DestinoDevolucao = DestinoDevolucao.DISPONIVEL

    created_at: datetime = field(default_factory=datetime.now)
    version: int = 1


@dataclass
class Manutencao:
    """Component: Manutencao"""
    id: UUID = field(default_factory=uuid4)
    equipamento_id: UUID = field(default_factory=uuid4)

    problema: str = ""
    fornecedor: str = ""
    responsavel: str = ""
    data_entrada: Optional[date] = None
    data_conclusao: Optional[date] = None
    valor: Decimal = Decimal("0.00")
    status: StatusManutencao = StatusManutencao.AGUARDANDO

    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    version: int = 1


@dataclass
class Notificacao:
    """Component: Notificacao"""
    id: UUID = field(default_factory=uuid4)
    tipo: TipoNotificacao = TipoNotificacao.CONFIRMACAO
    beneficiario_id: UUID = field(default_factory=uuid4)
    emprestimo_id: Optional[UUID] = None
    canal: str = "WhatsApp"
    status: StatusNotificacao = StatusNotificacao.ENVIADA
    conteudo: str = ""
    enviada_em: Optional[datetime] = None

    created_at: datetime = field(default_factory=datetime.now)
    version: int = 1


@dataclass
class Usuario:
    """Component: Usuario (Atendente/Admin/Gestor/Manutencao)"""
    id: UUID = field(default_factory=uuid4)
    nome: str = ""
    email: str = ""
    perfil: PerfilUsuario = PerfilUsuario.ATENDENTE
    ativo: bool = True

    created_at: datetime = field(default_factory=datetime.now)
    version: int = 1

    def pode_aprovar_renovacao(self) -> bool:
        return self.perfil in (PerfilUsuario.GESTOR, PerfilUsuario.ADMINISTRADOR)

    def pode_gerenciar_manutencao(self) -> bool:
        return self.perfil in (PerfilUsuario.MANUTENCAO, PerfilUsuario.ADMINISTRADOR)


@dataclass
class Auditoria:
    """Component: Auditoria (Compliance & Evidence)"""
    id: UUID = field(default_factory=uuid4)
    entidade_tipo: str = ""  # "Equipamento", "Emprestimo", etc.
    entidade_id: UUID = field(default_factory=uuid4)
    acao: str = ""  # "CRIAR", "ATUALIZAR", "EXCLUIR_SOFT"
    dados_anteriores: Optional[Dict[str, Any]] = None
    dados_novos: Optional[Dict[str, Any]] = None
    usuario_id: UUID = field(default_factory=uuid4)
    timestamp: datetime = field(default_factory=datetime.now)
    version: int = 1


# ============================================================
# Registry Entry (Kernel §6, Registry & Discovery §7)
# ============================================================

REGISTRY_ENTRY = {
    "apiVersion": "framework.eng/v1",
    "kind": "ComponentRegistry",
    "metadata": {
        "name": "ortho-crm-registry",
        "namespace": "ortho-crm",
        "version": "1.0.0",
    },
    "spec": {
        "components": [
            {
                "name": "Equipamento",
                "contract": "runtime.contracts.ortho.Equipamento",
                "lifecycle": ["Disponível", "Emprestado", "Manutenção", "Baixado"],
                "coordinates": {
                    "namespace": "ortho-crm",
                    "name": "equipamento",
                    "version": "1.0.0"
                }
            },
            {
                "name": "Beneficiario",
                "contract": "runtime.contracts.ortho.Beneficiario",
                "coordinates": {
                    "namespace": "ortho-crm",
                    "name": "beneficiario",
                    "version": "1.0.0"
                }
            },
            {
                "name": "Emprestimo",
                "contract": "runtime.contracts.ortho.Emprestimo",
                "lifecycle": ["Ativo", "Devolvido", "Atrasado", "Renovado", "Cancelado"],
                "coordinates": {
                    "namespace": "ortho-crm",
                    "name": "emprestimo",
                    "version": "1.0.0"
                }
            },
            {
                "name": "Devolucao",
                "contract": "runtime.contracts.ortho.Devolucao",
                "coordinates": {
                    "namespace": "ortho-crm",
                    "name": "devolucao",
                    "version": "1.0.0"
                }
            },
            {
                "name": "Manutencao",
                "contract": "runtime.contracts.ortho.Manutencao",
                "lifecycle": ["Aguardando", "Concluído"],
                "coordinates": {
                    "namespace": "ortho-crm",
                    "name": "manutencao",
                    "version": "1.0.0"
                }
            },
            {
                "name": "Notificacao",
                "contract": "runtime.contracts.ortho.Notificacao",
                "coordinates": {
                    "namespace": "ortho-crm",
                    "name": "notificacao",
                    "version": "1.0.0"
                }
            },
            {
                "name": "Usuario",
                "contract": "runtime.contracts.ortho.Usuario",
                "coordinates": {
                    "namespace": "ortho-crm",
                    "name": "usuario",
                    "version": "1.0.0"
                }
            },
            {
                "name": "Auditoria",
                "contract": "runtime.contracts.ortho.Auditoria",
                "coordinates": {
                    "namespace": "ortho-crm",
                    "name": "auditoria",
                    "version": "1.0.0"
                }
            }
        ],
        "workflows": [
            {
                "name": "wf-emprestimo",
                "file": "components/core/workflow.emprestimo.yaml",
                "trigger": "human",
                "compliance": "L2"
            },
            {
                "name": "wf-devolucao",
                "trigger": "human | qr_scan",
                "compliance": "L2"
            },
            {
                "name": "wf-manutencao",
                "trigger": "human",
                "compliance": "L2"
            },
            {
                "name": "wf-notificacao-automatica",
                "trigger": "cron",
                "schedule": "0 6 * * *",
                "compliance": "L1"
            }
        ],
        "skills": [
            {
                "name": "gestao-emprestimo",
                "file": "components/core/skill.gestao-emprestimo.yaml",
                "capabilities": 7,
                "compliance": "L2"
            }
        ]
    }
}
