from typing import Optional
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload
from ..models import Atendimento, Paciente, ProfissionalSaude


def get_profissional_or_404(db: Session, profissional_id: int) -> ProfissionalSaude:
    profissional = db.query(ProfissionalSaude).filter(ProfissionalSaude.id == profissional_id).first()
    if not profissional:
        raise HTTPException(status_code=404, detail="Profissional de saúde não encontrado")
    return profissional


def get_paciente_or_404(db: Session, paciente_id: int) -> Paciente:
    paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    return paciente


def get_atendimento_or_404(db: Session, atendimento_id: int) -> Atendimento:
    atendimento = (
        db.query(Atendimento)
        .options(
            selectinload(Atendimento.profissional_saude),
            selectinload(Atendimento.paciente),
            selectinload(Atendimento.receitas_saude),
            selectinload(Atendimento.exames_lab),
            selectinload(Atendimento.prontuario),
        )
        .filter(Atendimento.id == atendimento_id)
        .first()
    )
    if not atendimento:
        raise HTTPException(status_code=404, detail="Atendimento não encontrado")
    return atendimento


def commit_or_bad_request(db: Session, detail: str):
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail=detail)


def atualizar_modelo(modelo, dados):
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(modelo, campo, valor)


def validar_atendimento_referencias(db: Session, atendimento):
    get_profissional_or_404(db, atendimento.profissional_saude_id)
    if atendimento.paciente_id is not None:
        get_paciente_or_404(db, atendimento.paciente_id)


def validar_choque_atendimento(db: Session, atendimento, atendimento_id: Optional[int] = None):
    query = db.query(Atendimento).filter(
        Atendimento.profissional_saude_id == atendimento.profissional_saude_id,
        Atendimento.data_atendimento == atendimento.data_atendimento,
        Atendimento.horario_atendimento == atendimento.horario_atendimento,
    )
    if atendimento_id is not None:
        query = query.filter(Atendimento.id != atendimento_id)

    if query.first():
        raise HTTPException(
            status_code=400,
            detail="Profissional já possui atendimento neste dia e horário",
        )
