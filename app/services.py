from .models import Atividade, HistoricoStatus, PeriodosTerceiros
from .repository import (
    criar_atividade, atualizar_atividade, obter_atividade, listar_atividades,
    criar_historico, obter_historico,
    iniciar_periodo_terceiro, encerrar_periodo_terceiro, obter_periodos_terceiros
)
from datetime import datetime, timedelta
from typing import List, Tuple

def calcular_tempos(atividade: Atividade) -> Tuple[timedelta, timedelta, timedelta]:
    agora = datetime.now()
    criado_em = atividade.criado_em or agora

    # Tempo total: desde criação até agora (ou finalização/cancelamento)
    fim_total = atividade.finalizado_em or atividade.cancelado_em or agora
    tempo_total = fim_total - criado_em

    # Tempo aguardando terceiros: soma de todos os períodos
    periodos = obter_periodos_terceiros(atividade.id)
    tempo_terceiros = timedelta()
    for periodo in periodos:
        if periodo.encerrado_em:
            tempo_terceiros += periodo.encerrado_em - periodo.iniciado_em
        elif atividade.status == 'Aguardando terceiros':
            # Período atual ainda aberto
            tempo_terceiros += agora - periodo.iniciado_em

    # Tempo operacional interno: total - terceiros
    tempo_operacional = tempo_total - tempo_terceiros

    return tempo_total, tempo_terceiros, tempo_operacional

def criar_nova_atividade(titulo: str, descricao: str, categoria: str, prioridade: str, responsavel: str, usuario: str) -> int:
    atividade = Atividade(
        titulo=titulo,
        descricao=descricao,
        categoria=categoria,
        prioridade=prioridade,
        responsavel=responsavel,
        status='Aberta'
    )
    atividade_id = criar_atividade(atividade)

    # Histórico inicial
    historico = HistoricoStatus(
        atividade_id=atividade_id,
        status_anterior='',
        status_novo='Aberta',
        usuario=usuario
    )
    criar_historico(historico)

    return atividade_id

def alterar_status(atividade_id: int, novo_status: str, usuario: str, motivo: str = None):
    atividade = obter_atividade(atividade_id)
    if not atividade:
        raise ValueError("Atividade não encontrada")

    status_anteriores_invalidos = ['Finalizada', 'Cancelada']
    if atividade.status in status_anteriores_invalidos:
        raise ValueError("Não é possível alterar status de atividade finalizada ou cancelada")

    status_anterior = atividade.status

    # Regras específicas
    if novo_status == 'Aguardando terceiros':
        if not motivo:
            raise ValueError("Motivo obrigatório para aguardar terceiros")
        # Iniciar período
        periodo = PeriodosTerceiros(
            atividade_id=atividade_id,
            motivo=motivo,
            criado_por=usuario
        )
        iniciar_periodo_terceiro(periodo)
    elif status_anterior == 'Aguardando terceiros' and novo_status != 'Aguardando terceiros':
        # Encerrar período atual
        encerrar_periodo_terceiro(atividade_id)

    # Atualizar atividade
    atividade.status = novo_status
    if novo_status == 'Finalizada':
        atividade.finalizado_em = datetime.now()
        atividade.finalizado_por = usuario
    elif novo_status == 'Cancelada':
        if not motivo:
            raise ValueError("Motivo obrigatório para cancelar")
        atividade.cancelado_em = datetime.now()
        atividade.cancelado_por = usuario
        atividade.motivo_cancelamento = motivo

    atualizar_atividade(atividade)

    # Histórico
    historico = HistoricoStatus(
        atividade_id=atividade_id,
        status_anterior=status_anterior,
        status_novo=novo_status,
        usuario=usuario,
        motivo=motivo
    )
    criar_historico(historico)

def finalizar_atividade(atividade_id: int, usuario: str, observacao: str = None):
    atividade = obter_atividade(atividade_id)
    if not atividade or atividade.status in ['Finalizada', 'Cancelada']:
        raise ValueError("Atividade já finalizada ou cancelada")

    alterar_status(atividade_id, 'Finalizada', usuario)
    atividade = obter_atividade(atividade_id)
    atividade.observacao_final = observacao
    atualizar_atividade(atividade)

def cancelar_atividade(atividade_id: int, usuario: str, motivo: str):
    if not motivo:
        raise ValueError("Motivo obrigatório para cancelar")
    alterar_status(atividade_id, 'Cancelada', usuario, motivo)

def obter_relatorio() -> List[Tuple[Atividade, timedelta, timedelta, timedelta]]:
    atividades = listar_atividades()
    relatorio = []
    for atividade in atividades:
        if atividade.status in ['Finalizada', 'Cancelada']:
            tempos = calcular_tempos(atividade)
            relatorio.append((atividade, *tempos))
    return relatorio