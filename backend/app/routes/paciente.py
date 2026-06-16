from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Paciente
from ..schemas import PacienteCreate, PacienteSchema, PacienteUpdate
from .utils import get_paciente_or_404, commit_or_bad_request, atualizar_modelo

router = APIRouter(prefix="/pacientes", tags=["pacientes"])


@router.post("/", response_model=PacienteSchema)
def criar_paciente(paciente: PacienteCreate, db: Session = Depends(get_db)):
    novo_paciente = Paciente(**paciente.model_dump())
    db.add(novo_paciente)
    commit_or_bad_request(db, "CPF já cadastrado")
    db.refresh(novo_paciente)
    return novo_paciente


@router.get("/", response_model=List[PacienteSchema])
def listar_pacientes(db: Session = Depends(get_db)):
    return db.query(Paciente).order_by(Paciente.nome).all()


@router.get("/{paciente_id}", response_model=PacienteSchema)
def obter_paciente(paciente_id: int, db: Session = Depends(get_db)):
    return get_paciente_or_404(db, paciente_id)


@router.put("/{paciente_id}", response_model=PacienteSchema)
def atualizar_paciente(
    paciente_id: int,
    dados: PacienteUpdate,
    db: Session = Depends(get_db),
):
    paciente = get_paciente_or_404(db, paciente_id)
    atualizar_modelo(paciente, dados)
    commit_or_bad_request(db, "Não foi possível atualizar o paciente")
    db.refresh(paciente)
    return paciente


@router.delete("/{paciente_id}")
def excluir_paciente(paciente_id: int, db: Session = Depends(get_db)):
    paciente = get_paciente_or_404(db, paciente_id)
    db.delete(paciente)
    db.commit()
    return {"message": "Paciente excluído com sucesso"}
