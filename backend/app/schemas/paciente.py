from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict


class PacienteBase(BaseModel):
    nome: str
    cpf: str
    data_nascimento: date
    telefone: Optional[str] = None


class PacienteCreate(PacienteBase):
    pass


class PacienteUpdate(BaseModel):
    nome: Optional[str] = None
    cpf: Optional[str] = None
    data_nascimento: Optional[date] = None
    telefone: Optional[str] = None


class PacienteSchema(PacienteBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
