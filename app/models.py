from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Atividade:
    id: Optional[int] = None
    titulo: str = ""
    descricao: str = ""
    categoria: str = ""
    prioridade: str = "Média"  # Baixa, Média, Alta, Crítica
    responsavel: str = ""
    status: str = "Aberta"  # Aberta, Em andamento, Aguardando terceiros, Finalizada, Cancelada
    criado_em: Optional[datetime] = None
    atualizado_em: Optional[datetime] = None
    finalizado_em: Optional[datetime] = None
    cancelado_em: Optional[datetime] = None
    finalizado_por: Optional[str] = None
    cancelado_por: Optional[str] = None
    motivo_cancelamento: Optional[str] = None
    observacao_final: Optional[str] = None

@dataclass
class HistoricoStatus:
    id: Optional[int] = None
    atividade_id: int = 0
    status_anterior: str = ""
    status_novo: str = ""
    usuario: str = ""
    motivo: Optional[str] = None
    criado_em: Optional[datetime] = None

@dataclass
class PeriodosTerceiros:
    id: Optional[int] = None
    atividade_id: int = 0
    motivo: str = ""
    iniciado_em: Optional[datetime] = None
    encerrado_em: Optional[datetime] = None
    criado_por: str = ""