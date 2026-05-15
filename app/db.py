import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'whatshappeing.db')

def get_connection():
    return sqlite3.connect(DB_PATH)

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # Tabela atividades
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS atividades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT,
            categoria TEXT,
            prioridade TEXT NOT NULL,
            responsavel TEXT,
            status TEXT NOT NULL,
            criado_em TEXT NOT NULL,
            atualizado_em TEXT,
            finalizado_em TEXT,
            cancelado_em TEXT,
            finalizado_por TEXT,
            cancelado_por TEXT,
            motivo_cancelamento TEXT,
            observacao_final TEXT
        )
    ''')

    # Tabela historico_status
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historico_status (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            atividade_id INTEGER NOT NULL,
            status_anterior TEXT,
            status_novo TEXT NOT NULL,
            usuario TEXT NOT NULL,
            motivo TEXT,
            criado_em TEXT NOT NULL,
            FOREIGN KEY (atividade_id) REFERENCES atividades (id)
        )
    ''')

    # Tabela periodos_terceiros
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS periodos_terceiros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            atividade_id INTEGER NOT NULL,
            motivo TEXT NOT NULL,
            iniciado_em TEXT NOT NULL,
            encerrado_em TEXT,
            criado_por TEXT NOT NULL,
            FOREIGN KEY (atividade_id) REFERENCES atividades (id)
        )
    ''')

    conn.commit()
    conn.close()

# Inicializar banco na primeira execução
create_tables()