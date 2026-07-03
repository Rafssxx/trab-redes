from __future__ import annotations

from typing import List

from fastapi import APIRouter, HTTPException, Response, status

from app.models.cliente import Cliente, ClienteAtualizar, ClienteCriar
from app.services import clientes_service


router = APIRouter(prefix="/clientes", tags=["Clientes"])


@router.post("", response_model=Cliente, status_code=status.HTTP_201_CREATED)
def criar_cliente(payload: ClienteCriar):
    try:
        return clientes_service.criar_cliente(payload)
    except clientes_service.EmailClienteJaCadastradoError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ja existe um cliente cadastrado com este email",
        )


@router.get("", response_model=List[Cliente])
def listar_clientes():
    return clientes_service.listar_clientes()


@router.get("/{cliente_id}", response_model=Cliente)
def obter_cliente(cliente_id: str):
    cliente = clientes_service.obter_cliente(cliente_id)
    if cliente is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente nao encontrado",
        )
    return cliente


@router.put("/{cliente_id}", response_model=Cliente)
def atualizar_cliente(cliente_id: str, payload: ClienteAtualizar):
    try:
        cliente = clientes_service.atualizar_cliente(cliente_id, payload)
    except clientes_service.EmailClienteJaCadastradoError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ja existe um cliente cadastrado com este email",
        )

    if cliente is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente nao encontrado",
        )
    return cliente


@router.delete("/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_cliente(cliente_id: str):
    cliente_deletado = clientes_service.deletar_cliente(cliente_id)
    if not cliente_deletado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente nao encontrado",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
