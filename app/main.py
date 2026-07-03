from __future__ import annotations

import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request

from app.controllers import clientes_controller, produtos_controller, sistema_controller
from app.database import inicializar_banco
from app.services.metricas_service import registrar_requisicao


@asynccontextmanager
async def lifespan(app: FastAPI):
    inicializar_banco()
    yield


app = FastAPI(
    title="API de Produtos e Clientes",
    description="API simples de CRUD de produtos e clientes para uma loja virtual.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.middleware("http")
async def coletar_metricas(request: Request, call_next):
    inicio = time.perf_counter()
    response = await call_next(request)
    latencia_ms = round((time.perf_counter() - inicio) * 1000, 2)

    registrar_requisicao(request.method, latencia_ms)

    return response


app.include_router(sistema_controller.router)
app.include_router(produtos_controller.router)
app.include_router(clientes_controller.router)
