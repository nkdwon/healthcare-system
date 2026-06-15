# Healthcare System

Sistema de gerenciamento de profissionais de saúde desenvolvido para a disciplina de Engenharia de Software II da PUC Minas.

## Integrantes

- Felipe Barros Ratton de Almeida
- Laura Menezes Héraclito Alves

## Disciplina

**Engenharia de Software II**  
Pontifícia Universidade Católica de Minas Gerais (PUC Minas)

## Tecnologias Utilizadas

### Frontend
- React
- Vite
- JavaScript

### Backend
- Python
- FastAPI

### Banco de Dados
- PostgreSQL

## Estrutura do Projeto

```text
healthcare-system/
│
├── frontend/
├── backend/
├── database/
└── README.md
```

## Funcionalidades

- Cadastro de Profissionais de Saúde
- Consulta de Profissionais
- Atualização de Dados
- Exclusão de Registros
- Gerenciamento de Atendimentos
- Gerenciamento de Receitas de Saúde
- Gerenciamento de Exames Laboratoriais

## Como Executar o Frontend

```bash
cd frontend
npm install
npm run dev
```

O frontend ficará disponível em:

```text
http://localhost:5173
```

## Como Executar o Backend

```bash
cd backend

python -m venv .venv

# Windows (Git Bash)
source .venv/Scripts/activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

A API ficará disponível em:

```text
http://localhost:8000
```

Documentação Swagger:

```text
http://localhost:8000/docs
```

## Arquitetura

O projeto é dividido em três camadas principais:

- Frontend (React)
- Backend (FastAPI)
- Banco de Dados (PostgreSQL)

## Status do Projeto

🚧 Em desenvolvimento.

## Licença

Projeto acadêmico desenvolvido exclusivamente para fins educacionais.