from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, List

# --- Paciente ---
class PacienteBase(BaseModel):
    nome: str
    cpf: str
    data_nascimento: date
    telefone: Optional[str] = None

class PacienteCreate(PacienteBase):
    pass

class PacienteSchema(PacienteBase):
    id: int
    class Config:
        from_attributes = True

# --- Medico ---
class MedicoBase(BaseModel):
    nome: str
    crm: str
    especialidade: str

class MedicoCreate(MedicoBase):
    pass

class MedicoSchema(MedicoBase):
    id: int
    class Config:
        from_attributes = True

# --- Agendamento ---
class AgendamentoBase(BaseModel):
    paciente_id: int
    medico_id: int
    data_hora: datetime
    status: Optional[str] = "Agendado"

class AgendamentoCreate(AgendamentoBase):
    pass

class AgendamentoSchema(AgendamentoBase):
    id: int
    paciente: PacienteSchema
    medico: MedicoSchema
    class Config:
        from_attributes = True

# --- Prontuario ---
class ProntuarioBase(BaseModel):
    agendamento_id: int
    observacoes: str

class ProntuarioCreate(ProntuarioBase):
    pass

class ProntuarioSchema(ProntuarioBase):
    id: int
    data_criacao: datetime
    class Config:
        from_attributes = True
