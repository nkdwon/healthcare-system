from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import ExameLab
from ..schemas import ExameLabCreate, ExameLabSchema, ExameLabUpdate
from .utils import get_atendimento_or_404, commit_or_bad_request, atualizar_modelo

router = APIRouter(prefix="/exames-lab", tags=["exames"])


@router.post("/", response_model=ExameLabSchema)
def criar_exame(exame: ExameLabCreate, db: Session = Depends(get_db)):
    get_atendimento_or_404(db, exame.atendimento_id)
    novo_exame = ExameLab(**exame.model_dump())
    db.add(novo_exame)
    commit_or_bad_request(db, "Não foi possível cadastrar o exame laboratorial")
    db.refresh(novo_exame)
    return novo_exame


@router.get("/", response_model=List[ExameLabSchema])
def listar_exames(
    atendimento_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    query = db.query(ExameLab)
    if atendimento_id is not None:
        query = query.filter(ExameLab.atendimento_id == atendimento_id)
    return query.order_by(ExameLab.id.desc()).all()


@router.put("/{exame_id}", response_model=ExameLabSchema)
def atualizar_exame(
    exame_id: int,
    dados: ExameLabUpdate,
    db: Session = Depends(get_db),
):
    exame = db.query(ExameLab).filter(ExameLab.id == exame_id).first()
    if not exame:
        raise HTTPException(status_code=404, detail="Exame laboratorial não encontrado")

    if dados.atendimento_id is not None:
        get_atendimento_or_404(db, dados.atendimento_id)

    atualizar_modelo(exame, dados)
    commit_or_bad_request(db, "Não foi possível atualizar o exame laboratorial")
    db.refresh(exame)
    return exame


@router.delete("/{exame_id}")
def excluir_exame(exame_id: int, db: Session = Depends(get_db)):
    exame = db.query(ExameLab).filter(ExameLab.id == exame_id).first()
    if not exame:
        raise HTTPException(status_code=404, detail="Exame laboratorial não encontrado")
    db.delete(exame)
    db.commit()
    return {"message": "Exame laboratorial excluído com sucesso"}
