from typing import Optional
from pydantic import BaseModel, ConfigDict
from .enums import CategoriaProfissional


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
