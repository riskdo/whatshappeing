from .db import get_connection
from .models import Atividade, HistoricoStatus, PeriodosTerceiros
from datetime import datetime
from typing import List, Optional

def atividade_to_dict(atividade: Atividade) -> dict:
    return {
        'id': atividade.id,
        'titulo': atividade.titulo,
        'descricao': atividade.descricao,
        'categoria': atividade.categoria,
        'prioridade': atividade.prioridade,
        'responsavel': atividade.responsavel,
        'status': atividade.status,
        'criado_em': atividade.criado_em.isoformat() if atividade.criado_em else None,
        'atualizado_em': atividade.atualizado_em.isoformat() if atividade.atualizado_em else None,
        'finalizado_em': atividade.finalizado_em.isoformat() if atividade.finalizado_em else None,
        'cancelado_em': atividade.cancelado_em.isoformat() if atividade.cancelado_em else None,
        'finalizado_por': atividade.finalizado_por,
        'cancelado_por': atividade.cancelado_por,
        'motivo_cancelamento': atividade.motivo_cancelamento,
        'observacao_final': atividade.observacao_final,
    }

def dict_to_atividade(data: dict) -> Atividade:
    return Atividade(
        id=data.get('id'),
        titulo=data.get('titulo', ''),
        descricao=data.get('descricao', ''),
        categoria=data.get('categoria', ''),
        prioridade=data.get('prioridade', 'Média'),
        responsavel=data.get('responsavel', ''),
        status=data.get('status', 'Aberta'),
        criado_em=datetime.fromisoformat(data['criado_em']) if data.get('criado_em') else None,
        atualizado_em=datetime.fromisoformat(data['atualizado_em']) if data.get('atualizado_em') else None,
        finalizado_em=datetime.fromisoformat(data['finalizado_em']) if data.get('finalizado_em') else None,
        cancelado_em=datetime.fromisoformat(data['cancelado_em']) if data.get('cancelado_em') else None,
        finalizado_por=data.get('finalizado_por'),
        cancelado_por=data.get('cancelado_por'),
        motivo_cancelamento=data.get('motivo_cancelamento'),
        observacao_final=data.get('observacao_final'),
    )

# Atividades
def criar_atividade(atividade: Atividade) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    data = atividade_to_dict(atividade)
    data['criado_em'] = datetime.now().isoformat()
    data['atualizado_em'] = data['criado_em']
    columns = ', '.join(data.keys())
    placeholders = ', '.join('?' * len(data))
    cursor.execute(f'INSERT INTO atividades ({columns}) VALUES ({placeholders})', list(data.values()))
    atividade_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return atividade_id

def atualizar_atividade(atividade: Atividade):
    conn = get_connection()
    cursor = conn.cursor()
    data = atividade_to_dict(atividade)
    data['atualizado_em'] = datetime.now().isoformat()
    set_clause = ', '.join(f'{k} = ?' for k in data.keys() if k != 'id')
    values = [data[k] for k in data.keys() if k != 'id'] + [atividade.id]
    cursor.execute(f'UPDATE atividades SET {set_clause} WHERE id = ?', values)
    conn.commit()
    conn.close()

def obter_atividade(atividade_id: int) -> Optional[Atividade]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM atividades WHERE id = ?', (atividade_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        columns = [desc[0] for desc in cursor.description]
        data = dict(zip(columns, row))
        return dict_to_atividade(data)
    return None

def listar_atividades(filtro_status: Optional[str] = None, filtro_prioridade: Optional[str] = None, filtro_responsavel: Optional[str] = None) -> List[Atividade]:
    conn = get_connection()
    cursor = conn.cursor()
    query = 'SELECT * FROM atividades WHERE 1=1'
    params = []
    if filtro_status:
        query += ' AND status = ?'
        params.append(filtro_status)
    if filtro_prioridade:
        query += ' AND prioridade = ?'
        params.append(filtro_prioridade)
    if filtro_responsavel:
        query += ' AND responsavel = ?'
        params.append(filtro_responsavel)
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    atividades = []
    columns = [desc[0] for desc in cursor.description]
    for row in rows:
        data = dict(zip(columns, row))
        atividades.append(dict_to_atividade(data))
    return atividades

# Histórico
def criar_historico(historico: HistoricoStatus):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO historico_status (atividade_id, status_anterior, status_novo, usuario, motivo, criado_em)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        historico.atividade_id,
        historico.status_anterior,
        historico.status_novo,
        historico.usuario,
        historico.motivo,
        datetime.now().isoformat()
    ))
    conn.commit()
    conn.close()

def obter_historico(atividade_id: int) -> List[HistoricoStatus]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM historico_status WHERE atividade_id = ? ORDER BY criado_em DESC', (atividade_id,))
    rows = cursor.fetchall()
    conn.close()
    historicos = []
    columns = [desc[0] for desc in cursor.description]
    for row in rows:
        data = dict(zip(columns, row))
        historicos.append(HistoricoStatus(
            id=data['id'],
            atividade_id=data['atividade_id'],
            status_anterior=data.get('status_anterior', ''),
            status_novo=data['status_novo'],
            usuario=data['usuario'],
            motivo=data.get('motivo'),
            criado_em=datetime.fromisoformat(data['criado_em']) if data.get('criado_em') else None
        ))
    return historicos

# Períodos terceiros
def iniciar_periodo_terceiro(periodo: PeriodosTerceiros):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO periodos_terceiros (atividade_id, motivo, iniciado_em, criado_por)
        VALUES (?, ?, ?, ?)
    ''', (
        periodo.atividade_id,
        periodo.motivo,
        datetime.now().isoformat(),
        periodo.criado_por
    ))
    conn.commit()
    conn.close()

def encerrar_periodo_terceiro(atividade_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE periodos_terceiros
        SET encerrado_em = ?
        WHERE atividade_id = ? AND encerrado_em IS NULL
    ''', (datetime.now().isoformat(), atividade_id))
    conn.commit()
    conn.close()

def obter_periodos_terceiros(atividade_id: int) -> List[PeriodosTerceiros]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM periodos_terceiros WHERE atividade_id = ? ORDER BY iniciado_em', (atividade_id,))
    rows = cursor.fetchall()
    conn.close()
    periodos = []
    columns = [desc[0] for desc in cursor.description]
    for row in rows:
        data = dict(zip(columns, row))
        periodos.append(PeriodosTerceiros(
            id=data['id'],
            atividade_id=data['atividade_id'],
            motivo=data['motivo'],
            iniciado_em=datetime.fromisoformat(data['iniciado_em']) if data.get('iniciado_em') else None,
            encerrado_em=datetime.fromisoformat(data['encerrado_em']) if data.get('encerrado_em') else None,
            criado_por=data['criado_por']
        ))
    return periodos