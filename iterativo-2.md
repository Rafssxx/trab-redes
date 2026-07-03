# Iterativo 2 - Arquitetura MVC, Clientes e SQLite

## Entendimento

O projeto tinha uma `main.py` concentrando rotas, schemas, armazenamento em memoria e metricas. A alteracao separa essas responsabilidades, adiciona a entidade `clientes` e passa a persistir os dados em um banco SQLite.

## Alteracoes realizadas

- `app/main.py`
  - Ficou responsavel apenas por criar a aplicacao FastAPI, inicializar o banco, registrar o middleware de metricas e incluir os controllers.
- `app/controllers/`
  - Recebeu os controllers HTTP de sistema, produtos e clientes.
  - Os controllers validam a entrada via Pydantic, chamam os services e retornam respostas HTTP.
- `app/services/`
  - Recebeu a coordenacao dos fluxos de produtos, clientes e metricas.
  - A criacao dos IDs foi movida para os services.
- `app/repositories/`
  - Recebeu o acesso ao SQLite para produtos e clientes.
  - As operacoes de CRUD ficaram isoladas dos controllers.
- `app/models/`
  - Recebeu os models Pydantic de produtos e clientes.
- `app/database.py`
  - Centraliza a conexao com SQLite e cria as tabelas `produtos` e `clientes`.
- `loja.sqlite3`
  - Banco SQLite usado pela aplicacao. O arquivo e criado automaticamente na primeira execucao.

## Nova entidade: clientes

A entidade `Cliente` possui:

- `id`
- `nome`
- `email`
- `telefone`
- `endereco`

O campo `email` e unico no banco. Quando um email ja cadastrado e enviado, a API retorna `409 Conflict`.

## Rotas adicionadas

```http
POST /clientes
GET /clientes
GET /clientes/{cliente_id}
PUT /clientes/{cliente_id}
DELETE /clientes/{cliente_id}
```

## Rotas mantidas

As rotas de produtos continuam disponiveis:

```http
POST /produtos
GET /produtos
GET /produtos/{produto_id}
PUT /produtos/{produto_id}
DELETE /produtos/{produto_id}
```

Tambem continuam disponiveis:

```http
GET /
GET /saude
GET /metricas
```

## Como testar

Instale as dependencias:

```bash
pip install -r requirements.txt
```

Execute a API:

```bash
uvicorn app.main:app --reload
```

Acesse:

```txt
http://127.0.0.1:8000/docs
```

Exemplo de criacao de cliente:

```json
{
  "nome": "Maria Silva",
  "email": "maria@email.com",
  "telefone": "11999999999",
  "endereco": "Rua Principal, 100"
}
```

## Pontos de atencao

- O armazenamento deixou de ser em memoria e passou a ser persistente em SQLite.
- Dados criados permanecem salvos entre reinicializacoes da API.
- A API ainda usa uma estrutura simples, adequada ao tamanho atual do projeto, sem introduzir camadas extras desnecessarias.
