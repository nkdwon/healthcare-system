from typing import Optional
from pydantic import BaseModel, ConfigDict
from .enums import TipoReceita


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
