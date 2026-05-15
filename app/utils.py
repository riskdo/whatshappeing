from datetime import timedelta

def formatar_timedelta(td: timedelta) -> str:
    """Formata timedelta para string legível (dias horas:minutos:segundos)"""
    total_seconds = int(td.total_seconds())
    days, remainder = divmod(total_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    if days > 0:
        return f"{days}d {hours:02d}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def validar_prioridade(prioridade: str) -> bool:
    return prioridade in ['Baixa', 'Média', 'Alta', 'Crítica']

def validar_status(status: str) -> bool:
    return status in ['Aberta', 'Em andamento', 'Aguardando terceiros', 'Finalizada', 'Cancelada']