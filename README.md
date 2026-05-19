# user_roles API

API REST para gerenciamento de usuários com hierarquia de papéis (admin/user), construída com FastAPI e PostgreSQL.

---

## Como rodar o projeto

### Pré-requisitos

- Python 3.10+
- PostgreSQL
- pip

### Instalação

```bash
# Clone o repositório
git clone <url-do-repositorio>
cd user_roles

# Instale as dependências
pip install -r requirements.txt
```

### Configuração do banco

Crie um arquivo `.env` na raiz do projeto:

```env
DATABASE_URL=postgresql://postgres:suasenha@localhost:5432/user_roles
```

### Rodando

```bash
# Popula o banco com roles e usuários iniciais
python seed.py

# Sobe o servidor
uvicorn main:app --reload
```

A API estará disponível em `http://localhost:8000`.
Documentação interativa em `http://localhost:8000/docs`.

### Dados iniciais (seed)

O `seed.py` popula o banco com os seguintes registros:

**Roles**

| id | name |
|----|------|
| 1 | admin |
| 2 | user |

**Usuários**

| id | name | email | role |
|----|------|-------|------|
| 1 | Pedro | pedro@email.com | admin |
| 2 | Matheus | matheus@email.com | user |

Para testar as rotas como admin, use `X-User-Id: 1`.
Para testar como user comum, use `X-User-Id: 2`.

---

## Rotas disponíveis

| Método | Rota | Descrição | Requer papel |
|--------|------|-----------|--------------|
| POST | `/users` | Cria um usuário | admin |
| GET | `/users` | Lista usuários | admin ou user* |
| GET | `/users/{id}` | Busca usuário por id | admin ou user* |
| PUT | `/users/{id}` | Atualiza usuário | admin |
| DELETE | `/users/{id}` | Remove usuário | admin |

*admin vê todos os usuários, user vê apenas ele mesmo.

### Autenticação

Passe o id do usuário autenticado no header de cada requisição:

```
X-User-Id: 1
```

---

## Decisões técnicas

### Modelagem

O projeto possui duas entidades: `users` e `roles`.

`Role` foi modelado como uma tabela separada em vez de um enum fixo no código. Isso garante flexibilidade — se no futuro surgir a necessidade de adicionar um novo papel (como `moderador`), basta inserir um registro no banco sem precisar alterar o código ou fazer um novo deploy.

A relação entre usuário e papel é de muitos-para-um: um usuário possui exatamente um papel, definido pelo campo `role_id` (chave estrangeira). Se fosse necessário que um usuário tivesse múltiplos papéis, seria preciso uma tabela intermediária — mas para este desafio, um papel por usuário é suficiente.

### Autenticação simplificada

A identificação do usuário é feita via header `X-User-Id`. Essa abordagem foi escolhida para manter o foco do desafio nas regras de acesso e na modelagem, evitando a complexidade de JWT, hash de senha e fluxo de login.

### Stack

- **FastAPI** — escolhido por ser moderno, ter documentação automática via Swagger e permitir explorar um novo framework Python.
- **PostgreSQL** — banco relacional já utilizado em projetos anteriores, adequado para dados estruturados com relações.
- **SQLAlchemy** — ORM que evita escrever SQL puro, permitindo trabalhar com o banco usando Python. O `create_all` também automatiza a criação das tabelas.

### Estrutura do projeto

```
app/
├── database.py     # Conexão com o banco, SessionLocal e Base
├── main.py         # Ponto de entrada, registro de routers
├── seed.py         # Popula o banco com os papéis iniciais
├── models/
│   ├── role.py     # Tabela roles
│   └── user.py     # Tabela users
├── schemas/
│   ├── role.py     # Validação de entrada e saída de roles
│   └── user.py     # Validação de entrada e saída de usuários
└── routers/
    └── users.py    # Rotas de usuários e regras de acesso
```

Cada camada tem uma responsabilidade única: `models` fala com o banco, `schemas` valida os dados que entram e saem da API, e `routers` define as rotas e aplica as regras de negócio. Isso facilita manutenção — uma mudança no banco afeta só os models, uma mudança no contrato da API afeta só os schemas.

### Decisões de API

- A existência do `role_id` é validada antes de criar o usuário, evitando inconsistências no banco.
- Status HTTP seguem as convenções REST: `201` para criação, `404` para recurso não encontrado, `403` para acesso negado.
