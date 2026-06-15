CREATE TABLE IF NOT EXISTS profissionais_saude (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    telefone VARCHAR(20),
    endereco VARCHAR(150),
    categoria VARCHAR(30) NOT NULL CHECK (
        categoria IN ('MEDICO', 'PSICOLOGO', 'FISIOTERAPEUTA')
    )
);

CREATE TABLE IF NOT EXISTS pacientes (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    data_nascimento DATE NOT NULL,
    telefone VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS atendimentos (
    id SERIAL PRIMARY KEY,
    profissional_saude_id INTEGER NOT NULL,
    paciente_id INTEGER,

    data_atendimento DATE NOT NULL,
    horario_atendimento TIME NOT NULL,
    problema_texto TEXT NOT NULL,

    status VARCHAR(20) DEFAULT 'AGENDADO' CHECK (
        status IN ('AGENDADO', 'REALIZADO', 'CANCELADO')
    ),

    CONSTRAINT fk_atendimentos_profissional_saude
        FOREIGN KEY (profissional_saude_id)
        REFERENCES profissionais_saude(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_atendimentos_paciente
        FOREIGN KEY (paciente_id)
        REFERENCES pacientes(id)
        ON DELETE SET NULL,

    CONSTRAINT uq_atendimentos_profissional_data_horario
        UNIQUE (profissional_saude_id, data_atendimento, horario_atendimento)
);

CREATE TABLE IF NOT EXISTS receitas_saude (
    id SERIAL PRIMARY KEY,
    atendimento_id INTEGER NOT NULL,

    descricao TEXT NOT NULL,
    tipo VARCHAR(30) NOT NULL CHECK (
        tipo IN ('REMEDIO', 'ATIVIDADE_FISICA', 'ATIVIDADE_MENTAL')
    ),

    CONSTRAINT fk_receitas_saude_atendimento
        FOREIGN KEY (atendimento_id)
        REFERENCES atendimentos(id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS exames_lab (
    id SERIAL PRIMARY KEY,
    atendimento_id INTEGER NOT NULL,

    descricao TEXT NOT NULL,

    CONSTRAINT fk_exames_lab_atendimento
        FOREIGN KEY (atendimento_id)
        REFERENCES atendimentos(id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS prontuarios (
    id SERIAL PRIMARY KEY,
    atendimento_id INTEGER UNIQUE NOT NULL,

    observacoes TEXT NOT NULL,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_prontuarios_atendimento
        FOREIGN KEY (atendimento_id)
        REFERENCES atendimentos(id)
        ON DELETE CASCADE
);