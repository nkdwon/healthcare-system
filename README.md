# Healthcare System

Sistema de gerenciamento de profissionais de saúde desenvolvido para a disciplina de Engenharia de Software II da PUC Minas.

## Integrantes

* Felipe Barros Ratton de Almeida
* Laura Menezes Heráclito Alves

## Tecnologias

* Frontend: React + Vite
* Backend: Python + FastAPI
* Banco de Dados: PostgreSQL
* Containerização: Docker e Docker Compose
* CI/CD: GitHub Actions
* Hospedagem: Render

## Arquitetura

O projeto é dividido em três camadas principais:

* Frontend: interface web em React
* Backend: API REST em FastAPI
* Banco de Dados: PostgreSQL

Estrutura principal:

```text
healthcare-system/
├── frontend/
├── backend/
├── database/
├── .github/
├── docker-compose.yml
└── README.md
```

## Modelo de Dados

O arquivo `database/schema.sql` define o modelo principal utilizado pela aplicação.

### Entidades

* `profissionais_saude`
* `pacientes`
* `atendimentos`
* `receitas_saude`
* `exames_lab`
* `prontuarios`

### Categorias de Profissionais

* `MEDICO`
* `PSICOLOGO`
* `FISIOTERAPEUTA`

### Tipos de Receita

* `REMEDIO`
* `ATIVIDADE_FISICA`
* `ATIVIDADE_MENTAL`

### Regras de Negócio

Validadas no backend:

* `MEDICO` permite receitas do tipo `REMEDIO`
* `FISIOTERAPEUTA` permite receitas do tipo `ATIVIDADE_FISICA`
* `PSICOLOGO` permite receitas do tipo `ATIVIDADE_MENTAL`

## Ambientes

### Desenvolvimento Local (Vite)

Frontend:

```text
http://localhost:5173
```

### Desenvolvimento Local (Docker)

Frontend:

```text
http://localhost:3000
```

### Backend Local

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

### Produção

Frontend:

```text
https://healthcare-frontend-ie0k.onrender.com
```

Backend:

```text
https://healthcare-backend-j3sk.onrender.com/
```

## Configuração do Banco de Dados

### Utilizando Docker Compose

Ao executar o Compose pela primeira vez, o PostgreSQL cria automaticamente:

* Usuário: `postgres`
* Senha: `root`
* Banco: `healthcare_db`
* Porta: `5432`

O arquivo `database/schema.sql` é executado automaticamente na criação inicial do volume.

```bash
docker compose up --build
```

Observação:

Caso o volume `postgres_data` já exista, o PostgreSQL não executará novamente os scripts presentes em:

```text
/docker-entrypoint-initdb.d
```

Nesse caso, recrie o volume ou execute o schema manualmente.

### Utilizando PostgreSQL Local

Configuração para conexão via pgAdmin:

```text
Host: localhost
Porta: 5432
Usuário: postgres
Senha: sua_senha_local
Banco: healthcare_db
```

Após criar o banco, execute o conteúdo de:

```text
database/schema.sql
```

### Configuração do Backend Local

Copie o arquivo de exemplo:

```bash
copy backend\.env.example backend\.env
```

Edite o arquivo:

```text
DATABASE_URL=postgresql://postgres:sua_senha_local@localhost:5432/healthcare_db
```

## Configuração no Render

### Banco PostgreSQL

O Render fornece duas URLs:

* Internal Database URL → utilizada pelo backend hospedado no Render
* External Database URL → utilizada por pgAdmin, scripts locais e conexões externas

No backend hospedado no Render, configure:

```text
DATABASE_URL=<Internal Database URL>
```

### Aplicação do Schema

O banco PostgreSQL criado no Render não executa automaticamente o arquivo:

```text
database/schema.sql
```

O schema deve ser aplicado manualmente antes da primeira utilização da aplicação.

Isso pode ser feito por:

* pgAdmin
* psql
* PSQL Command fornecido pelo próprio Render

### Frontend

Configure a variável de ambiente:

```text
VITE_API_URL=https://url-do-backend.onrender.com/api
```

Essa variável é utilizada durante o processo de build do Vite.

## Executar com Docker

```bash
docker compose up --build
```

Serviços disponíveis:

| Serviço    | Endereço                   |
| ---------- | -------------------------- |
| Frontend   | http://localhost:3000      |
| Backend    | http://localhost:8000      |
| Swagger    | http://localhost:8000/docs |
| PostgreSQL | localhost:5432             |

## Executar Localmente

### Backend

Criar ambiente virtual:

```bash
cd backend
python -m venv .venv
```

Ativar ambiente:

PowerShell:

```bash
.venv\Scripts\Activate.ps1
```

Git Bash:

```bash
source .venv/Scripts/activate
```

Instalar dependências:

```bash
pip install -r requirements.txt
```

Executar:

```bash
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Variável opcional:

```text
VITE_API_URL=http://localhost:8000/api
```

## Principais Rotas

### Profissionais de Saúde

* `GET /api/profissionais-saude`
* `POST /api/profissionais-saude`
* `GET /api/profissionais-saude/{id}`
* `PUT /api/profissionais-saude/{id}`
* `DELETE /api/profissionais-saude/{id}`

### Pacientes

* `GET /api/pacientes`
* `POST /api/pacientes`
* `GET /api/pacientes/{id}`
* `PUT /api/pacientes/{id}`
* `DELETE /api/pacientes/{id}`

### Atendimentos

* `GET /api/atendimentos`
* `POST /api/atendimentos`
* `GET /api/atendimentos/{id}`
* `PUT /api/atendimentos/{id}`
* `DELETE /api/atendimentos/{id}`

### Receitas

* `GET /api/receitas-saude`
* `POST /api/receitas-saude`
* `PUT /api/receitas-saude/{id}`
* `DELETE /api/receitas-saude/{id}`

### Exames

* `GET /api/exames-lab`
* `POST /api/exames-lab`
* `PUT /api/exames-lab/{id}`
* `DELETE /api/exames-lab/{id}`

### Prontuários

* `GET /api/prontuarios`
* `POST /api/prontuarios`
* `PUT /api/prontuarios/{id}`
* `DELETE /api/prontuarios/{id}`

## Validação

### Frontend

```bash
cd frontend
npm run lint
npm run build
```

### Backend

```bash
cd backend
python -m compileall app
```

## CI/CD

O projeto utiliza GitHub Actions para:

* validação do backend
* validação do frontend
* build das imagens Docker

O deploy é realizado automaticamente pelo Render quando alterações são enviadas para a branch principal do repositório.

## Status

Projeto em desenvolvimento.

## Licença

Projeto acadêmico desenvolvido exclusivamente para fins educacionais.
