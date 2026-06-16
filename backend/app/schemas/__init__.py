from datetime import date, datetime, time
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class CategoriaProfissional(str, Enum):
    MEDICO = "MEDICO"
    PSICOLOGO = "PSICOLOGO"
    FISIOTERAPEUTA = "FISIOTERAPEUTA"


class TipoReceita(str, Enum):
    REMEDIO = "REMEDIO"
    ATIVIDADE_FISICA = "ATIVIDADE_FISICA"
    ATIVIDADE_MENTAL = "ATIVIDADE_MENTAL"


class StatusAtendimento(str, Enum):
    AGENDADO = "AGENDADO"
    REALIZADO = "REALIZADO"
    CANCELADO = "CANCELADO"


class ProfissionalSaudeBase(BaseModel):
    nome: str
    telefone: Optional[str] = None
    endereco: Optional[str] = None
    categoria: CategoriaProfissional


class ProfissionalSaudeCreate(ProfissionalSaudeBase):
    pass


class ProfissionalSaudeUpdate(BaseModel):
    nome: Optional[str] = None
    telefone: Optional[str] = None
    endereco: Optional[str] = None
    categoria: Optional[CategoriaProfissional] = None


class ProfissionalSaudeSchema(ProfissionalSaudeBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


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


class ReceitaSaudeBase(BaseModel):
    atendimento_id: int
    descricao: str
    tipo: TipoReceita


class ReceitaSaudeCreate(ReceitaSaudeBase):
    pass


class ReceitaSaudeUpdate(BaseModel):
    atendimento_id: Optional[int] = None
    descricao: Optional[str] = None
    tipo: Optional[TipoReceita] = None


class ReceitaSaudeSchema(ReceitaSaudeBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class ExameLabBase(BaseModel):
    atendimento_id: int
    descricao: str


class ExameLabCreate(ExameLabBase):
    pass


class ExameLabUpdate(BaseModel):
    atendimento_id: Optional[int] = None
    descricao: Optional[str] = None


class ExameLabSchema(ExameLabBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class ProntuarioBase(BaseModel):
    atendimento_id: int
    observacoes: str


class ProntuarioCreate(ProntuarioBase):
    pass


class ProntuarioUpdate(BaseModel):
    atendimento_id: Optional[int] = None
    observacoes: Optional[str] = None


class ProntuarioSchema(ProntuarioBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    data_criacao: datetime


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
