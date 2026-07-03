from __future__ import annotations


metricas = {
    "total_requisicoes": 0,
    "requisicoes_por_metodo": {},
    "ultima_latencia_ms": 0.0,
}


def registrar_requisicao(metodo: str, latencia_ms: float) -> None:
    metricas["total_requisicoes"] += 1
    metricas["ultima_latencia_ms"] = latencia_ms
    metricas["requisicoes_por_metodo"][metodo] = (
        metricas["requisicoes_por_metodo"].get(metodo, 0) + 1
    )


def consultar_metricas() -> dict:
    return metricas
