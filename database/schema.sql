-- Tabela de Pacientes
CREATE TABLE IF NOT EXISTS pacientes (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    data_nascimento DATE NOT NULL,
    telefone VARCHAR(20)
);

-- Tabela de Médicos
CREATE TABLE IF NOT EXISTS medicos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    crm VARCHAR(20) UNIQUE NOT NULL,
    especialidade VARCHAR(100) NOT NULL
);

-- Tabela de Agendamentos (Consultas)
CREATE TABLE IF NOT EXISTS agendamentos (
    id SERIAL PRIMARY KEY,
    paciente_id INTEGER REFERENCES pacientes(id) ON DELETE CASCADE,
    medico_id INTEGER REFERENCES medicos(id) ON DELETE CASCADE,
    data_hora TIMESTAMP NOT NULL,
    status VARCHAR(20) DEFAULT 'Agendado', -- Agendado, Realizado, Cancelado
    UNIQUE(medico_id, data_hora) -- Evita choque de horário para o mesmo médico
);

-- Tabela de Prontuários
CREATE TABLE IF NOT EXISTS prontuarios (
    id SERIAL PRIMARY KEY,
    agendamento_id INTEGER UNIQUE REFERENCES agendamentos(id) ON DELETE CASCADE,
    observacoes TEXT NOT NULL,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
