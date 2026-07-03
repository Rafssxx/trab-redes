from __future__ import annotations

import os
import sqlite3
from pathlib import Path


DATABASE_PATH = Path(
    os.getenv("DATABASE_PATH", Path(__file__).resolve().parent.parent / "loja.sqlite3")
)


def obter_conexao() -> sqlite3.Connection:
    conexao = sqlite3.connect(DATABASE_PATH, timeout=30)
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    conexao.execute("PRAGMA journal_mode = WAL")
    return conexao


def inicializar_banco() -> None:
    with obter_conexao() as conexao:
        conexao.executescript(
            """
            CREATE TABLE IF NOT EXISTS produtos (
                id TEXT PRIMARY KEY,
                nome TEXT NOT NULL,
                categoria TEXT NOT NULL,
                preco REAL NOT NULL CHECK (preco > 0),
                estoque INTEGER NOT NULL CHECK (estoque >= 0),
                descricao TEXT
            );

            CREATE TABLE IF NOT EXISTS clientes (
                id TEXT PRIMARY KEY,
                nome TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                telefone TEXT,
                endereco TEXT
            );
            """
        )
