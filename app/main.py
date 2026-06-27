from __future__ import annotations

import time
from typing import Dict, List, Optional
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request, Response, status
from pydantic import BaseModel, Field


app = FastAPI(
    title="API de Produtos",
    description="API simples de CRUD de produtos para uma loja virtual.",
    version="1.0.0",
)


class ProdutoBase(BaseModel):
    nome: str = Field(..., min_length=2, example="Mouse gamer")
    categoria: str = Field(..., min_length=2, example="Periféricos")
    preco: float = Field(..., gt=0, example=149.90)
    estoque: int = Field(..., ge=0, example=25)
    descricao: Optional[str] = Field(default=None, example="Mouse óptico USB com RGB")


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


produtos: Dict[str, Produto] = {}
metricas = {
    "total_requisicoes": 0,
    "requisicoes_por_metodo": {},
    "ultima_latencia_ms": 0.0,
}


@app.middleware("http")
async def coletar_metricas(request: Request, call_next):
    inicio = time.perf_counter()
    response = await call_next(request)
    latencia_ms = round((time.perf_counter() - inicio) * 1000, 2)

    metodo = request.method
    metricas["total_requisicoes"] += 1
    metricas["ultima_latencia_ms"] = latencia_ms
    metricas["requisicoes_por_metodo"][metodo] = (
        metricas["requisicoes_por_metodo"].get(metodo, 0) + 1
    )

    return response


@app.get("/")
def raiz():
    return {
        "mensagem": "API de produtos de loja virtual",
        "documentacao": "/docs",
        "produtos": "/produtos",
    }


@app.get("/saude")
def verificar_saude():
    return {
        "status": "ok",
        "protocolo": "HTTP",
        "cenario": "CRUD de produtos em uma loja virtual",
    }


@app.get("/metricas")
def consultar_metricas():
    return metricas


@app.post("/produtos", response_model=Produto, status_code=status.HTTP_201_CREATED)
def criar_produto(payload: ProdutoCriar):
    produto = Produto(id=str(uuid4()), **payload.model_dump())
    produtos[produto.id] = produto
    return produto


@app.get("/produtos", response_model=List[Produto])
def listar_produtos(categoria: Optional[str] = None):
    itens = list(produtos.values())
    if categoria:
        itens = [
            produto
            for produto in itens
            if produto.categoria.lower() == categoria.lower()
        ]
    return itens


@app.get("/produtos/{produto_id}", response_model=Produto)
def obter_produto(produto_id: str):
    produto = produtos.get(produto_id)
    if produto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado",
        )
    return produto


@app.put("/produtos/{produto_id}", response_model=Produto)
def atualizar_produto(produto_id: str, payload: ProdutoAtualizar):
    produto = produtos.get(produto_id)
    if produto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado",
        )

    dados_atualizados = produto.model_dump()
    dados_atualizados.update(payload.model_dump(exclude_unset=True))

    produto_atualizado = Produto(**dados_atualizados)
    produtos[produto_id] = produto_atualizado
    return produto_atualizado


@app.delete("/produtos/{produto_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_produto(produto_id: str):
    if produto_id not in produtos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado",
        )
    produtos.pop(produto_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
