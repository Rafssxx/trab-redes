import csv
import os
import random
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

URL_API = os.getenv("URL_API", "http://127.0.0.1:8000")
ARQUIVO_RESULTADOS = "resultados/resultados.csv"

GRUPOS_CLIENTES = [1, 5, 10]
REPETICOES = 10


NOMES_PRODUTOS = [
    "Notebook",
    "Mouse",
    "Teclado",
    "Monitor",
    "Headset",
    "Webcam",
]

CATEGORIAS = [
    "Informática",
    "Periféricos",
    "Eletrônicos",
]


def requisicao_temporizada(metodo, url, **kwargs):
    inicio = time.perf_counter()
    try:
        resposta = requests.request(metodo, url, timeout=10, **kwargs)
        latencia_ms = (time.perf_counter() - inicio) * 1000
        return resposta, round(latencia_ms, 2), True
    except requests.RequestException:
        latencia_ms = (time.perf_counter() - inicio) * 1000
        return None, round(latencia_ms, 2), False


def simular_crud(cliente_id: int, repeticao: int, total_clientes: int):
    rows = []

    produto_payload = {
        "nome": f"{random.choice(NOMES_PRODUTOS)} {cliente_id}-{repeticao}",
        "categoria": random.choice(CATEGORIAS),
        "preco": round(random.uniform(50, 5000), 2),
        "estoque": random.randint(0, 100),
        "descricao": "Produto criado durante simulação HTTP de uma loja virtual.",
    }

    # CRIAR - POST /produtos
    resposta, latencia_ms, requisicao_realizada = requisicao_temporizada(
        "POST",
        f"{URL_API}/produtos",
        json=produto_payload,
    )

    produto_id = None
    codigo_status = resposta.status_code if resposta is not None else 0
    sucesso = requisicao_realizada and codigo_status == 201

    if sucesso:
        produto_id = resposta.json()["id"]

    rows.append({
        "clientes": total_clientes,
        "cliente_id": cliente_id,
        "repeticao": repeticao,
        "operacao": "CRIAR",
        "metodo": "POST",
        "rota": "/produtos",
        "codigo_status": codigo_status,
        "sucesso": sucesso,
        "latencia_ms": latencia_ms,
    })

    if produto_id is None:
        return rows

    # LISTAR - GET /produtos
    resposta, latencia_ms, requisicao_realizada = requisicao_temporizada(
        "GET",
        f"{URL_API}/produtos",
    )
    codigo_status = resposta.status_code if resposta is not None else 0

    rows.append({
        "clientes": total_clientes,
        "cliente_id": cliente_id,
        "repeticao": repeticao,
        "operacao": "LISTAR",
        "metodo": "GET",
        "rota": "/produtos",
        "codigo_status": codigo_status,
        "sucesso": requisicao_realizada and codigo_status == 200,
        "latencia_ms": latencia_ms,
    })

    # CONSULTAR - GET /produtos/{id}
    resposta, latencia_ms, requisicao_realizada = requisicao_temporizada(
        "GET",
        f"{URL_API}/produtos/{produto_id}",
    )
    codigo_status = resposta.status_code if resposta is not None else 0

    rows.append({
        "clientes": total_clientes,
        "cliente_id": cliente_id,
        "repeticao": repeticao,
        "operacao": "CONSULTAR",
        "metodo": "GET",
        "rota": "/produtos/{id}",
        "codigo_status": codigo_status,
        "sucesso": requisicao_realizada and codigo_status == 200,
        "latencia_ms": latencia_ms,
    })

    # ATUALIZAR - PUT /produtos/{id}
    resposta, latencia_ms, requisicao_realizada = requisicao_temporizada(
        "PUT",
        f"{URL_API}/produtos/{produto_id}",
        json={"preco": round(random.uniform(50, 5000), 2), "estoque": random.randint(1, 100)},
    )
    codigo_status = resposta.status_code if resposta is not None else 0

    rows.append({
        "clientes": total_clientes,
        "cliente_id": cliente_id,
        "repeticao": repeticao,
        "operacao": "ATUALIZAR",
        "metodo": "PUT",
        "rota": "/produtos/{id}",
        "codigo_status": codigo_status,
        "sucesso": requisicao_realizada and codigo_status == 200,
        "latencia_ms": latencia_ms,
    })

    # EXCLUIR - DELETE /produtos/{id}
    resposta, latencia_ms, requisicao_realizada = requisicao_temporizada(
        "DELETE",
        f"{URL_API}/produtos/{produto_id}",
    )
    codigo_status = resposta.status_code if resposta is not None else 0

    rows.append({
        "clientes": total_clientes,
        "cliente_id": cliente_id,
        "repeticao": repeticao,
        "operacao": "EXCLUIR",
        "metodo": "DELETE",
        "rota": "/produtos/{id}",
        "codigo_status": codigo_status,
        "sucesso": requisicao_realizada and codigo_status == 204,
        "latencia_ms": latencia_ms,
    })

    return rows


def main():
    os.makedirs("resultados", exist_ok=True)
    todas_linhas = []

    for total_clientes in GRUPOS_CLIENTES:
        print(f"Executando teste com {total_clientes} cliente(s) simultâneo(s)...")

        for repeticao in range(1, REPETICOES + 1):
            with ThreadPoolExecutor(max_workers=total_clientes) as executor:
                futures = [
                    executor.submit(simular_crud, cliente_id, repeticao, total_clientes)
                    for cliente_id in range(1, total_clientes + 1)
                ]

                for future in as_completed(futures):
                    todas_linhas.extend(future.result())

            time.sleep(0.2)

    with open(ARQUIVO_RESULTADOS, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "clientes",
                "cliente_id",
                "repeticao",
                "operacao",
                "metodo",
                "rota",
                "codigo_status",
                "sucesso",
                "latencia_ms",
            ],
        )
        writer.writeheader()
        writer.writerows(todas_linhas)

    requisicoes_com_sucesso = [row for row in todas_linhas if row["sucesso"]]
    latencia_media = (
        sum(row["latencia_ms"] for row in todas_linhas) / len(todas_linhas)
        if todas_linhas
        else 0
    )

    print("\nResumo:")
    print(f"Total de requisições: {len(todas_linhas)}")
    print(f"Requisições com sucesso: {len(requisicoes_com_sucesso)}")
    print(f"Taxa de sucesso: {(len(requisicoes_com_sucesso) / len(todas_linhas)) * 100:.2f}%")
    print(f"Latência média: {latencia_media:.2f} ms")
    print(f"Resultados salvos em: {ARQUIVO_RESULTADOS}")


if __name__ == "__main__":
    main()
