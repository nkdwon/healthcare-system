from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import Paciente, Medico, Agendamento, Prontuario
from ..schemas import (
    PacienteCreate, PacienteSchema,
    MedicoCreate, MedicoSchema,
    AgendamentoCreate, AgendamentoSchema,
    ProntuarioCreate, ProntuarioSchema
)

router = APIRouter()

# --- Rotas de Pacientes ---
@router.post("/pacientes/", response_model=PacienteSchema)
def criar_paciente(paciente: PacienteCreate, db: Session = Depends(get_db)):
    db_paciente = db.query(Paciente).filter(Paciente.cpf == paciente.cpf).first()
    if db_paciente:
        raise HTTPException(status_code=400, detail="CPF já cadastrado")
    novo_paciente = Paciente(**paciente.model_dump())
    db.add(novo_paciente)
    db.commit()
    db.refresh(novo_paciente)
    return novo_paciente

@router.get("/pacientes/", response_model=List[PacienteSchema])
def listar_pacientes(db: Session = Depends(get_db)):
    return db.query(Paciente).all()

# --- Rotas de Médicos ---
@router.post("/medicos/", response_model=MedicoSchema)
def criar_medico(medico: MedicoCreate, db: Session = Depends(get_db)):
    db_medico = db.query(Medico).filter(Medico.crm == medico.crm).first()
    if db_medico:
        raise HTTPException(status_code=400, detail="CRM já cadastrado")
    novo_medico = Medico(**medico.model_dump())
    db.add(novo_medico)
    db.commit()
    db.refresh(novo_medico)
    return novo_medico

@router.get("/medicos/", response_model=List[MedicoSchema])
def listar_medicos(db: Session = Depends(get_db)):
    return db.query(Medico).all()

# --- Rotas de Agendamentos ---
@router.post("/agendamentos/", response_model=AgendamentoSchema)
def criar_agendamento(agendamento: AgendamentoCreate, db: Session = Depends(get_db)):
    # Verifica se médico já tem consulta nesse horário
    choque = db.query(Agendamento).filter(
        Agendamento.medico_id == agendamento.medico_id,
        Agendamento.data_hora == agendamento.data_hora
    ).first()
    if choque:
        raise HTTPException(status_code=400, detail="Médico já possui agendamento neste horário")
    
    novo_agendamento = Agendamento(**agendamento.model_dump())
    db.add(novo_agendamento)
    db.commit()
    db.refresh(novo_agendamento)
    return novo_agendamento

@router.get("/agendamentos/", response_model=List[AgendamentoSchema])
def listar_agendamentos(db: Session = Depends(get_db)):
    return db.query(Agendamento).all()

# --- Rotas de Prontuários ---
@router.post("/prontuarios/", response_model=ProntuarioSchema)
def criar_prontuario(prontuario: ProntuarioCreate, db: Session = Depends(get_db)):
    db_prontuario = Prontuario(**prontuario.model_dump())
    db.add(db_prontuario)
    db.commit()
    db.refresh(db_prontuario)
    return db_prontuario
