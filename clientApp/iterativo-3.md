# Iterativo 3 - Atualizacoes

## O que foi desenvolvido

- Frontend de loja virtual com vitrine de produtos, busca e filtro por categoria.
- Carrinho de compras com abertura lateral, incremento, decremento, remocao de itens e subtotal.
- Fluxo de login local com validacao simples de e-mail e senha.
- Feedback de checkout exigindo login antes de finalizar a compra.

## Arquivos principais

- `src/features/store/StorefrontPage.vue`: pagina principal da loja.
- `src/features/store/components`: componentes visuais de cabecalho, filtros, produto, carrinho e login.
- `src/features/store/composables`: estado local de carrinho e sessao do cliente.
- `src/features/store/data/products.ts`: catalogo mockado de produtos.
- `src/features/store/types/storeTypes.ts`: contratos TypeScript da feature.

## Decisoes tecnicas

- A feature foi isolada em `src/features/store` para manter o `App.vue` simples.
- O catalogo foi mockado porque ainda nao ha API no projeto.
- O carrinho e o login ficaram em composables para separar estado/regra de tela dos componentes visuais.
- Nao foram adicionadas dependencias novas.

## Como validar

- Rodar `npm run build` para validar TypeScript e build de producao.
- Rodar `npm run test:unit` para validar o teste unitario atualizado.
- Rodar `npm run dev` e acessar a aplicacao para testar busca, filtro, carrinho e login.

## Pontos de atencao

- O login ainda e apenas local e demonstrativo.
- O checkout nao envia pedido para backend.
- As imagens dos produtos usam URLs externas; em producao, o ideal e servir imagens controladas pela aplicacao ou por um CDN proprio.
