from __future__ import annotations

from app.database import inicializar_banco, obter_conexao


PRODUTOS_SEED = [
    {
        "id": "headphone-aurora-x1",
        "nome": "Headphone Aurora X1",
        "categoria": "Eletronicos",
        "descricao": "Cancelamento de ruido, bateria de longa duracao e conexao multiponto.",
        "preco": 429.9,
        "estoque": 18,
        "avaliacao": 4.8,
        "imagem_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=900&q=80",
    },
    {
        "id": "mochila-urban-flex",
        "nome": "Mochila Urban Flex",
        "categoria": "Moda",
        "descricao": "Compartimento para notebook, tecido impermeavel e organizadores internos.",
        "preco": 189.9,
        "estoque": 24,
        "avaliacao": 4.6,
        "imagem_url": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=900&q=80",
    },
    {
        "id": "luminaria-nordic-desk",
        "nome": "Luminaria Nordic Desk",
        "categoria": "Casa",
        "descricao": "Iluminacao ajustavel com acabamento metalico e base compacta.",
        "preco": 149.9,
        "estoque": 12,
        "avaliacao": 4.7,
        "imagem_url": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=900&q=80",
    },
    {
        "id": "tenis-runner-pulse",
        "nome": "Tenis Runner Pulse",
        "categoria": "Esporte",
        "descricao": "Solado responsivo, cabedal respiravel e suporte para treinos diarios.",
        "preco": 329.9,
        "estoque": 31,
        "avaliacao": 4.5,
        "imagem_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=900&q=80",
    },
    {
        "id": "smartwatch-core-fit",
        "nome": "Smartwatch Core Fit",
        "categoria": "Eletronicos",
        "descricao": "Monitoramento de saude, GPS integrado e resistencia a agua.",
        "preco": 599.9,
        "estoque": 10,
        "avaliacao": 4.9,
        "imagem_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=900&q=80",
    },
    {
        "id": "kit-organizadores-linen",
        "nome": "Kit Organizadores Linen",
        "categoria": "Casa",
        "descricao": "Conjunto modular para gavetas, armarios e prateleiras.",
        "preco": 89.9,
        "estoque": 40,
        "avaliacao": 4.4,
        "imagem_url": "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?auto=format&fit=crop&w=900&q=80",
    },
]


def popular_produtos() -> int:
    inicializar_banco()

    with obter_conexao() as conexao:
        conexao.executemany(
            """
            INSERT INTO produtos (
                id,
                nome,
                categoria,
                preco,
                estoque,
                descricao,
                imagem_url,
                avaliacao
            )
            VALUES (
                :id,
                :nome,
                :categoria,
                :preco,
                :estoque,
                :descricao,
                :imagem_url,
                :avaliacao
            )
            ON CONFLICT(id) DO UPDATE SET
                nome = excluded.nome,
                categoria = excluded.categoria,
                preco = excluded.preco,
                estoque = excluded.estoque,
                descricao = excluded.descricao,
                imagem_url = excluded.imagem_url,
                avaliacao = excluded.avaliacao
            """,
            PRODUTOS_SEED,
        )

    return len(PRODUTOS_SEED)


if __name__ == "__main__":
    total_produtos = popular_produtos()
    print(f"Seed concluido: {total_produtos} produtos cadastrados ou atualizados.")
