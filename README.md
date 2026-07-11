# Avaliação do Protocolo HTTP em uma API de Produtos para Loja Virtual

## 1. Tema do projeto

Este projeto implementa uma API HTTP simples para simular o CRUD de produtos de uma loja virtual. A aplicação foi desenvolvida em Python com FastAPI e representa um cenário real de comunicação cliente-servidor, no qual uma interface web, aplicativo ou sistema administrativo envia requisições para um servidor responsável por gerenciar produtos.

O objetivo do trabalho é observar como o protocolo HTTP pode ser utilizado em uma aplicação real, testando métodos HTTP, códigos de status, troca de dados em JSON e requisições simultâneas.

## 2. Cenário real escolhido

O cenário escolhido foi uma loja virtual, também chamada de comércio eletrônico.

Em uma loja virtual real, o sistema precisa permitir que administradores cadastrem, consultem, editem e removam produtos. Esses produtos podem ser exibidos posteriormente para clientes em uma página web ou aplicativo.

Exemplo de funcionamento real:

1. O administrador acessa o painel da loja.
2. O painel envia uma requisição HTTP para cadastrar um novo produto.
3. O servidor recebe os dados, valida as informações e salva o produto.
4. A interface consulta a lista de produtos por HTTP.
5. O usuário visualiza os produtos disponíveis na loja.

Esse tipo de cenário é comum em sistemas web, como lojas virtuais, sistemas de estoque, catálogos online, sistemas de gestão e marketplaces.

## 3. Por que HTTP é adequado para esse caso?

O HTTP é adequado para esse cenário porque ele é o protocolo base da Web e segue o modelo cliente-servidor. Nesse modelo, um cliente envia uma requisição e o servidor devolve uma resposta.

Em uma loja virtual, esse comportamento é natural:

- a interface solicita a lista de produtos;
- o servidor responde com os dados em JSON;
- a interface envia um novo produto;
- o servidor processa a requisição e retorna o produto criado;
- a interface solicita a alteração ou exclusão de um produto;
- o servidor retorna um código de status indicando sucesso ou erro.

Além disso, HTTP é muito utilizado em APIs REST, permitindo organizar as operações do sistema com métodos claros:

| Método HTTP | Uso no projeto | Exemplo |
|---|---|---|
| GET | Consultar dados | Listar produtos |
| POST | Criar dados | Cadastrar produto |
| PUT | Atualizar dados | Editar produto |
| DELETE | Remover dados | Excluir produto |

Outro ponto importante é que HTTP utiliza códigos de status que ajudam a entender o resultado da requisição:

| Código | Significado no projeto |
|---|---|
| 200 | Requisição executada com sucesso |
| 201 | Produto criado com sucesso |
| 204 | Produto removido com sucesso |
| 404 | Produto não encontrado |
| 422 | Erro de validação nos dados enviados |

## 4. Objetivo da implementação

Implementar uma API pequena em FastAPI para demonstrar o uso do protocolo HTTP em um cenário real de loja virtual.

A API permite:

- verificar o status da aplicação;
- cadastrar produtos;
- listar produtos;
- consultar um produto específico;
- atualizar um produto;
- remover um produto;
- consultar métricas simples das requisições HTTP.

## 5. Tecnologias utilizadas

- Python
- FastAPI
- Uvicorn
- Requests
- SQLite
- Vue 3
- Vite
- TypeScript

## 6. Como executar o projeto

### 6.1. Preparar o backend

Crie um ambiente virtual:

```bash
python -m venv venv
```

Ative o ambiente virtual no Linux ou macOS:

```bash
source venv/bin/activate
```

Ative o ambiente virtual no Windows:

```bash
venv\Scripts\activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Inicialize o banco e cadastre os produtos da loja:

```bash
python -m app.seed
```

O seed popula a tabela `produtos` no SQLite com produtos reais para a vitrine, incluindo preço, estoque, avaliação e `imagem_url` compatível com cada produto cadastrado. O comando é idempotente: se for executado novamente, atualiza os produtos do seed em vez de duplicá-los.

Execute a API:

```bash
uvicorn app.main:app --reload
```

Acesse a API em:

```txt
http://127.0.0.1:8000
```

Acesse a documentação automática em:

```txt
http://127.0.0.1:8000/docs
```

### 6.2. Preparar o frontend

Em outro terminal, acesse a pasta do frontend:

```bash
cd clientApp
```

Instale as dependências:

```bash
npm install
```

Execute a aplicação web:

```bash
npm run dev
```

Acesse a vitrine em:

```txt
http://localhost:5173
```

Por padrão, o frontend consome a API em `http://127.0.0.1:8000`. Para usar outra URL, crie um arquivo `clientApp/.env` com:

```env
VITE_API_URL=http://127.0.0.1:8001
```

### 6.3. Fluxo completo recomendado

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m app.seed
uvicorn app.main:app --reload
```

Em outro terminal:

```bash
cd clientApp
npm install
npm run dev
```

## 7. Rotas da API

### Verificar status da API

```http
GET /saude
```

Resposta esperada:

```json
{
  "status": "ok",
  "protocolo": "HTTP",
  "cenario": "CRUD de produtos em uma loja virtual"
}
```

### Criar produto

```http
POST /produtos
```

Exemplo de corpo JSON:

```json
{
  "nome": "Notebook Dell",
  "categoria": "Informática",
  "preco": 3500.00,
  "estoque": 10,
  "descricao": "Notebook para uso profissional",
  "imagem_url": "https://exemplo.com/notebook.jpg",
  "avaliacao": 4.8
}
```

### Listar produtos

```http
GET /produtos
```

### Buscar produto por ID

```http
GET /produtos/{produto_id}
```

### Atualizar produto

```http
PUT /produtos/{produto_id}
```

Exemplo de corpo JSON:

```json
{
  "preco": 3299.90,
  "estoque": 8
}
```

### Excluir produto

```http
DELETE /produtos/{produto_id}
```

### Consultar métricas

```http
GET /metricas
```

Resposta esperada:

```json
{
  "total_requisicoes": 10,
  "requisicoes_por_metodo": {
    "GET": 4,
    "POST": 2,
    "PUT": 2,
    "DELETE": 2
  },
  "ultima_latencia_ms": 1.25
}
```

## 8. Como testar o projeto

### Testar a API e o seed

Depois de executar o seed e iniciar a API, consulte os produtos:

```bash
curl http://127.0.0.1:8000/produtos
```

A resposta deve trazer os produtos cadastrados no SQLite com `imagem_url` e `avaliacao`.

### Testar o frontend

Com a API e o Vite rodando, abra:

```txt
http://localhost:5173
```

A vitrine deve carregar os produtos pela rota `GET /produtos`. Se a API estiver desligada, a tela exibirá uma mensagem de erro no catálogo.

### Testar o protocolo HTTP

Com a API em execução, rode o script de simulação:

```bash
python scripts/simular_clientes_http.py
```

O script simula vários clientes realizando operações de CRUD por HTTP.

Ele testa:

- requisições `POST` para criar produtos;
- requisições `GET` para consultar produtos;
- requisições `PUT` para atualizar produtos;
- requisições `DELETE` para remover produtos;
- clientes simultâneos;
- latência das requisições;
- códigos de status retornados pelo servidor;
- taxa de sucesso das requisições.

Os resultados são salvos em:

```txt
resultados/resultados.csv
```

Por padrão, o script usa a URL `http://127.0.0.1:8000`. Para usar outra URL, defina a variável de ambiente `URL_API`:

```bash
URL_API=http://127.0.0.1:8001 python scripts/simular_clientes_http.py
```

## 9. Métricas coletadas no CSV

O script gera um arquivo CSV com as seguintes informações:

| Campo | Descrição |
|---|---|
| clientes | Quantidade de clientes simultâneos |
| cliente_id | Identificação do cliente simulado |
| repeticao | Número da repetição do teste |
| operacao | Operação executada |
| metodo | Método HTTP utilizado |
| rota | Rota acessada |
| codigo_status | Código de status HTTP retornado |
| sucesso | Indica se a requisição teve sucesso |
| latencia_ms | Tempo de resposta em milissegundos |

## 10. O que analisar no relatório

No relatório, podem ser analisados os seguintes pontos:

1. O HTTP permitiu organizar bem as operações da API usando métodos como GET, POST, PUT e DELETE.
2. Os códigos de status facilitaram a identificação de sucesso e erro.
3. O formato JSON facilitou a comunicação entre cliente e servidor.
4. A API respondeu corretamente com múltiplos clientes simultâneos.
5. O protocolo é adequado para aplicações web e sistemas de gestão, como uma loja virtual.
6. Em sistemas que exigem comunicação em tempo real constante, HTTP pode não ser a melhor opção, pois protocolos como WebSocket ou MQTT podem ser mais eficientes.

## 11. Conclusão

O HTTP se mostrou adequado para o cenário de uma loja virtual, pois permite a comunicação entre cliente e servidor de forma simples, padronizada e amplamente compatível com aplicações web.

A implementação demonstrou que operações comuns de um sistema real, como cadastrar, listar, editar e remover produtos, podem ser representadas diretamente por métodos HTTP.

Portanto, o HTTP é uma boa escolha para APIs de sistemas web, especialmente em aplicações como comércio eletrônico, sistemas administrativos, catálogos de produtos e sistemas de gestão.
