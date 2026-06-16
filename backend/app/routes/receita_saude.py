from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import ReceitaSaude
from ..schemas import ReceitaSaudeCreate, ReceitaSaudeSchema, ReceitaSaudeUpdate
from ..services import validar_tipo_receita_por_atendimento
from .utils import commit_or_bad_request, atualizar_modelo

router = APIRouter(prefix="/receitas-saude", tags=["receitas"])


@router.post("/", response_model=ReceitaSaudeSchema)
def criar_receita(receita: ReceitaSaudeCreate, db: Session = Depends(get_db)):
    validar_tipo_receita_por_atendimento(db, receita.atendimento_id, receita.tipo.value)
    nova_receita = ReceitaSaude(**receita.model_dump())
    db.add(nova_receita)
    commit_or_bad_request(db, "Não foi possível cadastrar a receita de saúde")
    db.refresh(nova_receita)
    return nova_receita


@router.get("/", response_model=List[ReceitaSaudeSchema])
def listar_receitas(
    atendimento_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    query = db.query(ReceitaSaude)
    if atendimento_id is not None:
        query = query.filter(ReceitaSaude.atendimento_id == atendimento_id)
    return query.order_by(ReceitaSaude.id.desc()).all()


@router.put("/{receita_id}", response_model=ReceitaSaudeSchema)
def atualizar_receita(
    receita_id: int,
    dados: ReceitaSaudeUpdate,
    db: Session = Depends(get_db),
):
    receita = db.query(ReceitaSaude).filter(ReceitaSaude.id == receita_id).first()
    if not receita:
        raise HTTPException(status_code=404, detail="Receita de saúde não encontrada")

    novos_dados = dados.model_dump(exclude_unset=True)
    atendimento_id = novos_dados.get("atendimento_id", receita.atendimento_id)
    tipo = novos_dados.get("tipo", receita.tipo)
    if hasattr(tipo, "value"):
        tipo = tipo.value

    validar_tipo_receita_por_atendimento(db, atendimento_id, tipo)
    atualizar_modelo(receita, dados)
    commit_or_bad_request(db, "Não foi possível atualizar a receita de saúde")
    db.refresh(receita)
    return receita


@router.delete("/{receita_id}")
def excluir_receita(receita_id: int, db: Session = Depends(get_db)):
    receita = db.query(ReceitaSaude).filter(ReceitaSaude.id == receita_id).first()
    if not receita:
        raise HTTPException(status_code=404, detail="Receita de saúde não encontrada")
    db.delete(receita)
    db.commit()
    return {"message": "Receita de saúde excluída com sucesso"}
