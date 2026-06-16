from typing import Optional
from pydantic import BaseModel, ConfigDict


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
