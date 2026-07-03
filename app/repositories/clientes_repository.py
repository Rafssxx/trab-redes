from __future__ import annotations

from typing import List, Optional

from app.database import obter_conexao
from app.models.cliente import Cliente


CAMPOS_ATUALIZAVEIS = ("nome", "email", "telefone", "endereco")


def _mapear_cliente(linha) -> Cliente:
    return Cliente(**dict(linha))


def criar_cliente(cliente: Cliente) -> Cliente:
    with obter_conexao() as conexao:
        conexao.execute(
            """
            INSERT INTO clientes (id, nome, email, telefone, endereco)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                cliente.id,
                cliente.nome,
                cliente.email,
                cliente.telefone,
                cliente.endereco,
            ),
        )
    return cliente


def listar_clientes() -> List[Cliente]:
    with obter_conexao() as conexao:
        linhas = conexao.execute(
            """
            SELECT id, nome, email, telefone, endereco
            FROM clientes
            ORDER BY nome
            """
        ).fetchall()

    return [_mapear_cliente(linha) for linha in linhas]


def obter_cliente(cliente_id: str) -> Optional[Cliente]:
    with obter_conexao() as conexao:
        linha = conexao.execute(
            """
            SELECT id, nome, email, telefone, endereco
            FROM clientes
            WHERE id = ?
            """,
            (cliente_id,),
        ).fetchone()

    return _mapear_cliente(linha) if linha else None


def atualizar_cliente(cliente_id: str, dados_atualizados: dict) -> Optional[Cliente]:
    cliente = obter_cliente(cliente_id)
    if cliente is None:
        return None

    if dados_atualizados:
        campos = [campo for campo in CAMPOS_ATUALIZAVEIS if campo in dados_atualizados]
        campos_sql = ", ".join(f"{campo} = ?" for campo in campos)
        valores = [dados_atualizados[campo] for campo in campos]

        with obter_conexao() as conexao:
            conexao.execute(
                f"UPDATE clientes SET {campos_sql} WHERE id = ?",
                [*valores, cliente_id],
            )

    return obter_cliente(cliente_id)


def deletar_cliente(cliente_id: str) -> bool:
    with obter_conexao() as conexao:
        cursor = conexao.execute(
            "DELETE FROM clientes WHERE id = ?",
            (cliente_id,),
        )

    return cursor.rowcount > 0
