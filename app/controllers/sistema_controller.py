from __future__ import annotations

from fastapi import APIRouter

from app.services.metricas_service import consultar_metricas


router = APIRouter(tags=["Sistema"])


@router.get("/")
def raiz():
    return {
        "mensagem": "API de produtos e clientes de loja virtual",
        "documentacao": "/docs",
        "produtos": "/produtos",
        "clientes": "/clientes",
    }


@router.get("/saude")
def verificar_saude():
    return {
        "status": "ok",
        "protocolo": "HTTP",
        "cenario": "CRUD de produtos e clientes em uma loja virtual",
    }


@router.get("/metricas")
def obter_metricas():
    return consultar_metricas()
