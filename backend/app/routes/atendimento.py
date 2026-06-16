from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, selectinload
from ..database import get_db
from ..models import Atendimento
from ..schemas import AtendimentoCreate, AtendimentoSchema, AtendimentoUpdate
from .utils import (
    get_atendimento_or_404,
    commit_or_bad_request,
    atualizar_modelo,
    validar_atendimento_referencias,
    validar_choque_atendimento,
)

router = APIRouter(prefix="/atendimentos", tags=["atendimentos"])


@router.post("/", response_model=AtendimentoSchema)
def criar_atendimento(atendimento: AtendimentoCreate, db: Session = Depends(get_db)):
    validar_atendimento_referencias(db, atendimento)
    validar_choque_atendimento(db, atendimento)

    novo_atendimento = Atendimento(**atendimento.model_dump())
    db.add(novo_atendimento)
    commit_or_bad_request(db, "Não foi possível cadastrar o atendimento")
    return get_atendimento_or_404(db, novo_atendimento.id)


@router.get("/", response_model=List[AtendimentoSchema])
def listar_atendimentos(db: Session = Depends(get_db)):
    return (
        db.query(Atendimento)
        .options(
            selectinload(Atendimento.profissional_saude),
            selectinload(Atendimento.paciente),
            selectinload(Atendimento.receitas_saude),
            selectinload(Atendimento.exames_lab),
            selectinload(Atendimento.prontuario),
        )
        .order_by(Atendimento.data_atendimento.desc(), Atendimento.horario_atendimento.desc())
        .all()
    )


@router.get("/{atendimento_id}", response_model=AtendimentoSchema)
def obter_atendimento(atendimento_id: int, db: Session = Depends(get_db)):
    return get_atendimento_or_404(db, atendimento_id)


@router.put("/{atendimento_id}", response_model=AtendimentoSchema)
def atualizar_atendimento(
    atendimento_id: int,
    dados: AtendimentoUpdate,
    db: Session = Depends(get_db),
):
    atendimento = get_atendimento_or_404(db, atendimento_id)
    atualizar_modelo(atendimento, dados)
    validar_atendimento_referencias(db, atendimento)
    validar_choque_atendimento(db, atendimento, atendimento_id)

    commit_or_bad_request(db, "Não foi possível atualizar o atendimento")
    return get_atendimento_or_404(db, atendimento_id)


@router.delete("/{atendimento_id}")
def excluir_atendimento(atendimento_id: int, db: Session = Depends(get_db)):
    atendimento = get_atendimento_or_404(db, atendimento_id)
    db.delete(atendimento)
    db.commit()
    return {"message": "Atendimento excluído com sucesso"}
