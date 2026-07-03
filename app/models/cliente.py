from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class ClienteBase(BaseModel):
    nome: str = Field(..., min_length=2, example="Maria Silva")
    email: str = Field(
        ...,
        min_length=5,
        pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
        example="maria@email.com",
    )
    telefone: Optional[str] = Field(default=None, example="11999999999")
    endereco: Optional[str] = Field(default=None, example="Rua Principal, 100")


class ClienteCriar(ClienteBase):
    pass


class ClienteAtualizar(BaseModel):
    nome: Optional[str] = Field(default=None, min_length=2)
    email: Optional[str] = Field(
        default=None,
        min_length=5,
        pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
    )
    telefone: Optional[str] = None
    endereco: Optional[str] = None


class Cliente(ClienteBase):
    id: str
