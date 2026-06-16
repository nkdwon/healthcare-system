from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import ProfissionalSaude
from ..schemas import (
    ProfissionalSaudeCreate,
    ProfissionalSaudeSchema,
    ProfissionalSaudeUpdate,
    CategoriaProfissional,
)
from .utils import get_profissional_or_404, commit_or_bad_request, atualizar_modelo

router = APIRouter(prefix="/profissionais-saude", tags=["profissionais"])


@router.post("/", response_model=ProfissionalSaudeSchema)
def criar_profissional(
    profissional: ProfissionalSaudeCreate,
    db: Session = Depends(get_db),
):
    novo_profissional = ProfissionalSaude(**profissional.model_dump())
    db.add(novo_profissional)
    commit_or_bad_request(db, "Não foi possível cadastrar o profissional de saúde")
    db.refresh(novo_profissional)
    return novo_profissional


@router.get("/", response_model=List[ProfissionalSaudeSchema])
def listar_profissionais(
    nome: Optional[str] = None,
    categoria: Optional[CategoriaProfissional] = None,
    db: Session = Depends(get_db),
):
    query = db.query(ProfissionalSaude)
    if nome:
        query = query.filter(ProfissionalSaude.nome.ilike(f"%{nome}%"))
    if categoria:
        query = query.filter(ProfissionalSaude.categoria == categoria.value)
    return query.order_by(ProfissionalSaude.nome).all()


@router.get("/{profissional_id}", response_model=ProfissionalSaudeSchema)
def obter_profissional(profissional_id: int, db: Session = Depends(get_db)):
    return get_profissional_or_404(db, profissional_id)


@router.put("/{profissional_id}", response_model=ProfissionalSaudeSchema)
def atualizar_profissional(
    profissional_id: int,
    dados: ProfissionalSaudeUpdate,
    db: Session = Depends(get_db),
):
    profissional = get_profissional_or_404(db, profissional_id)
    atualizar_modelo(profissional, dados)
    commit_or_bad_request(db, "Não foi possível atualizar o profissional de saúde")
    db.refresh(profissional)
    return profissional


@router.delete("/{profissional_id}")
def excluir_profissional(profissional_id: int, db: Session = Depends(get_db)):
    profissional = get_profissional_or_404(db, profissional_id)
    db.delete(profissional)
    db.commit()
    return {"message": "Profissional de saúde excluído com sucesso"}
