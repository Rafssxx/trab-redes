from __future__ import annotations

import sqlite3
from typing import List, Optional
from uuid import uuid4

from app.models.cliente import Cliente, ClienteAtualizar, ClienteCriar
from app.repositories import clientes_repository


class EmailClienteJaCadastradoError(Exception):
    pass


def criar_cliente(payload: ClienteCriar) -> Cliente:
    cliente = Cliente(id=str(uuid4()), **payload.model_dump())

    try:
        return clientes_repository.criar_cliente(cliente)
    except sqlite3.IntegrityError as erro:
        if "clientes.email" in str(erro):
            raise EmailClienteJaCadastradoError from erro
        raise


def listar_clientes() -> List[Cliente]:
    return clientes_repository.listar_clientes()


def obter_cliente(cliente_id: str) -> Optional[Cliente]:
    return clientes_repository.obter_cliente(cliente_id)


def atualizar_cliente(cliente_id: str, payload: ClienteAtualizar) -> Optional[Cliente]:
    dados_atualizados = payload.model_dump(exclude_unset=True)

    try:
        return clientes_repository.atualizar_cliente(cliente_id, dados_atualizados)
    except sqlite3.IntegrityError as erro:
        if "clientes.email" in str(erro):
            raise EmailClienteJaCadastradoError from erro
        raise


def deletar_cliente(cliente_id: str) -> bool:
    return clientes_repository.deletar_cliente(cliente_id)
