from __future__ import annotations

from typing import List, Optional
from uuid import uuid4

from app.models.produto import Produto, ProdutoAtualizar, ProdutoCriar
from app.repositories import produtos_repository


def criar_produto(payload: ProdutoCriar) -> Produto:
    produto = Produto(id=str(uuid4()), **payload.model_dump())
    return produtos_repository.criar_produto(produto)


def listar_produtos(categoria: Optional[str] = None) -> List[Produto]:
    return produtos_repository.listar_produtos(categoria)


def obter_produto(produto_id: str) -> Optional[Produto]:
    return produtos_repository.obter_produto(produto_id)


def atualizar_produto(produto_id: str, payload: ProdutoAtualizar) -> Optional[Produto]:
    dados_atualizados = payload.model_dump(exclude_unset=True)
    return produtos_repository.atualizar_produto(produto_id, dados_atualizados)


def deletar_produto(produto_id: str) -> bool:
    return produtos_repository.deletar_produto(produto_id)
