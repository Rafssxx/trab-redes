from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class ProdutoBase(BaseModel):
    nome: str = Field(..., min_length=2, example="Mouse gamer")
    categoria: str = Field(..., min_length=2, example="Perifericos")
    preco: float = Field(..., gt=0, example=149.90)
    estoque: int = Field(..., ge=0, example=25)
    descricao: Optional[str] = Field(default=None, example="Mouse optico USB com RGB")


class ProdutoCriar(ProdutoBase):
    pass


class ProdutoAtualizar(BaseModel):
    nome: Optional[str] = Field(default=None, min_length=2)
    categoria: Optional[str] = Field(default=None, min_length=2)
    preco: Optional[float] = Field(default=None, gt=0)
    estoque: Optional[int] = Field(default=None, ge=0)
    descricao: Optional[str] = None


class Produto(ProdutoBase):
    id: str
