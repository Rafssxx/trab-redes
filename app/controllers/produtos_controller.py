from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, HTTPException, Response, status

from app.models.produto import Produto, ProdutoAtualizar, ProdutoCriar
from app.services import produtos_service


router = APIRouter(prefix="/produtos", tags=["Produtos"])


@router.post("", response_model=Produto, status_code=status.HTTP_201_CREATED)
def criar_produto(payload: ProdutoCriar):
    return produtos_service.criar_produto(payload)


@router.get("", response_model=List[Produto])
def listar_produtos(categoria: Optional[str] = None):
    return produtos_service.listar_produtos(categoria)


@router.get("/{produto_id}", response_model=Produto)
def obter_produto(produto_id: str):
    produto = produtos_service.obter_produto(produto_id)
    if produto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto nao encontrado",
        )
    return produto


@router.put("/{produto_id}", response_model=Produto)
def atualizar_produto(produto_id: str, payload: ProdutoAtualizar):
    produto = produtos_service.atualizar_produto(produto_id, payload)
    if produto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto nao encontrado",
        )
    return produto


@router.delete("/{produto_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_produto(produto_id: str):
    produto_deletado = produtos_service.deletar_produto(produto_id)
    if not produto_deletado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto nao encontrado",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
