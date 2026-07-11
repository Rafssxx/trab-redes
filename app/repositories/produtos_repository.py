from __future__ import annotations

from typing import List, Optional

from app.database import obter_conexao
from app.models.produto import Produto


CAMPOS_ATUALIZAVEIS = (
    "nome",
    "categoria",
    "preco",
    "estoque",
    "descricao",
    "imagem_url",
    "avaliacao",
)


def _mapear_produto(linha) -> Produto:
    return Produto(**dict(linha))


def criar_produto(produto: Produto) -> Produto:
    with obter_conexao() as conexao:
        conexao.execute(
            """
            INSERT INTO produtos (
                id,
                nome,
                categoria,
                preco,
                estoque,
                descricao,
                imagem_url,
                avaliacao
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                produto.id,
                produto.nome,
                produto.categoria,
                produto.preco,
                produto.estoque,
                produto.descricao,
                produto.imagem_url,
                produto.avaliacao,
            ),
        )
    return produto


def listar_produtos(categoria: Optional[str] = None) -> List[Produto]:
    with obter_conexao() as conexao:
        if categoria:
            linhas = conexao.execute(
                """
                SELECT id, nome, categoria, preco, estoque, descricao, imagem_url, avaliacao
                FROM produtos
                WHERE LOWER(categoria) = LOWER(?)
                ORDER BY nome
                """,
                (categoria,),
            ).fetchall()
        else:
            linhas = conexao.execute(
                """
                SELECT id, nome, categoria, preco, estoque, descricao, imagem_url, avaliacao
                FROM produtos
                ORDER BY nome
                """
            ).fetchall()

    return [_mapear_produto(linha) for linha in linhas]


def obter_produto(produto_id: str) -> Optional[Produto]:
    with obter_conexao() as conexao:
        linha = conexao.execute(
            """
            SELECT id, nome, categoria, preco, estoque, descricao, imagem_url, avaliacao
            FROM produtos
            WHERE id = ?
            """,
            (produto_id,),
        ).fetchone()

    return _mapear_produto(linha) if linha else None


def atualizar_produto(produto_id: str, dados_atualizados: dict) -> Optional[Produto]:
    produto = obter_produto(produto_id)
    if produto is None:
        return None

    if dados_atualizados:
        campos = [campo for campo in CAMPOS_ATUALIZAVEIS if campo in dados_atualizados]
        campos_sql = ", ".join(f"{campo} = ?" for campo in campos)
        valores = [dados_atualizados[campo] for campo in campos]

        with obter_conexao() as conexao:
            conexao.execute(
                f"UPDATE produtos SET {campos_sql} WHERE id = ?",
                [*valores, produto_id],
            )

    return obter_produto(produto_id)


def deletar_produto(produto_id: str) -> bool:
    with obter_conexao() as conexao:
        cursor = conexao.execute(
            "DELETE FROM produtos WHERE id = ?",
            (produto_id,),
        )

    return cursor.rowcount > 0
