from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


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
