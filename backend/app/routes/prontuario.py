from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Prontuario
from ..schemas import ProntuarioCreate, ProntuarioSchema, ProntuarioUpdate
from .utils import get_atendimento_or_404, commit_or_bad_request, atualizar_modelo

router = APIRouter(prefix="/prontuarios", tags=["prontuarios"])


@router.post("/", response_model=ProntuarioSchema)
def criar_prontuario(prontuario: ProntuarioCreate, db: Session = Depends(get_db)):
    get_atendimento_or_404(db, prontuario.atendimento_id)
    novo_prontuario = Prontuario(**prontuario.model_dump())
    db.add(novo_prontuario)
    commit_or_bad_request(db, "Atendimento já possui prontuário")
    db.refresh(novo_prontuario)
    return novo_prontuario


@router.get("/", response_model=List[ProntuarioSchema])
def listar_prontuarios(db: Session = Depends(get_db)):
    return db.query(Prontuario).order_by(Prontuario.id.desc()).all()


@router.get("/{prontuario_id}", response_model=ProntuarioSchema)
def obter_prontuario(prontuario_id: int, db: Session = Depends(get_db)):
    prontuario = db.query(Prontuario).filter(Prontuario.id == prontuario_id).first()
    if not prontuario:
        raise HTTPException(status_code=404, detail="Prontuário não encontrado")
    return prontuario


@router.put("/{prontuario_id}", response_model=ProntuarioSchema)
def atualizar_prontuario(
    prontuario_id: int,
    dados: ProntuarioUpdate,
    db: Session = Depends(get_db),
):
    prontuario = db.query(Prontuario).filter(Prontuario.id == prontuario_id).first()
    if not prontuario:
        raise HTTPException(status_code=404, detail="Prontuário não encontrado")

    if dados.atendimento_id is not None:
        get_atendimento_or_404(db, dados.atendimento_id)

    atualizar_modelo(prontuario, dados)
    commit_or_bad_request(db, "Não foi possível atualizar o prontuário")
    db.refresh(prontuario)
    return prontuario


@router.delete("/{prontuario_id}")
def excluir_prontuario(prontuario_id: int, db: Session = Depends(get_db)):
    prontuario = db.query(Prontuario).filter(Prontuario.id == prontuario_id).first()
    if not prontuario:
        raise HTTPException(status_code=404, detail="Prontuário não encontrado")
    db.delete(prontuario)
    db.commit()
    return {"message": "Prontuário excluído com sucesso"}
