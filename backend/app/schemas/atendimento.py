from datetime import date, time
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field
from .enums import StatusAtendimento
from .profissional_saude import ProfissionalSaudeSchema
from .paciente import PacienteSchema
from .receita_saude import ReceitaSaudeSchema
from .exame_lab import ExameLabSchema
from .prontuario import ProntuarioSchema


class AtendimentoBase(BaseModel):
    profissional_saude_id: int
    paciente_id: Optional[int] = None
    data_atendimento: date
    horario_atendimento: time
    problema_texto: str
    status: StatusAtendimento = StatusAtendimento.AGENDADO


class AtendimentoCreate(AtendimentoBase):
    pass


class AtendimentoUpdate(BaseModel):
    profissional_saude_id: Optional[int] = None
    paciente_id: Optional[int] = None
    data_atendimento: Optional[date] = None
    horario_atendimento: Optional[time] = None
    problema_texto: Optional[str] = None
    status: Optional[StatusAtendimento] = None


class AtendimentoSchema(AtendimentoBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    profissional_saude: ProfissionalSaudeSchema
    paciente: Optional[PacienteSchema] = None
    receitas_saude: List[ReceitaSaudeSchema] = Field(default_factory=list)
    exames_lab: List[ExameLabSchema] = Field(default_factory=list)
    prontuario: Optional[ProntuarioSchema] = None
