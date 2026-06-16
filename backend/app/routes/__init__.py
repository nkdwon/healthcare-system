from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from ..database import get_db
from ..models import (
    Atendimento,
    ExameLab,
    Paciente,
    ProfissionalSaude,
    Prontuario,
    ReceitaSaude,
)
from ..schemas import (
    AtendimentoCreate,
    AtendimentoSchema,
    AtendimentoUpdate,
    CategoriaProfissional,
    ExameLabCreate,
    ExameLabSchema,
    ExameLabUpdate,
    PacienteCreate,
    PacienteSchema,
    PacienteUpdate,
    ProfissionalSaudeCreate,
    ProfissionalSaudeSchema,
    ProfissionalSaudeUpdate,
    ProntuarioCreate,
    ProntuarioSchema,
    ProntuarioUpdate,
    ReceitaSaudeCreate,
    ReceitaSaudeSchema,
    ReceitaSaudeUpdate,
)
from ..services import validar_tipo_receita_por_atendimento

router = APIRouter()


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


@router.post("/profissionais-saude/", response_model=ProfissionalSaudeSchema)
def criar_profissional(
    profissional: ProfissionalSaudeCreate,
    db: Session = Depends(get_db),
):
    novo_profissional = ProfissionalSaude(**profissional.model_dump())
    db.add(novo_profissional)
    commit_or_bad_request(db, "Não foi possível cadastrar o profissional de saúde")
    db.refresh(novo_profissional)
    return novo_profissional


@router.get("/profissionais-saude/", response_model=List[ProfissionalSaudeSchema])
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


@router.get("/profissionais-saude/{profissional_id}", response_model=ProfissionalSaudeSchema)
def obter_profissional(profissional_id: int, db: Session = Depends(get_db)):
    return get_profissional_or_404(db, profissional_id)


@router.put("/profissionais-saude/{profissional_id}", response_model=ProfissionalSaudeSchema)
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


@router.delete("/profissionais-saude/{profissional_id}")
def excluir_profissional(profissional_id: int, db: Session = Depends(get_db)):
    profissional = get_profissional_or_404(db, profissional_id)
    db.delete(profissional)
    db.commit()
    return {"message": "Profissional de saúde excluído com sucesso"}


@router.post("/pacientes/", response_model=PacienteSchema)
def criar_paciente(paciente: PacienteCreate, db: Session = Depends(get_db)):
    novo_paciente = Paciente(**paciente.model_dump())
    db.add(novo_paciente)
    commit_or_bad_request(db, "CPF já cadastrado")
    db.refresh(novo_paciente)
    return novo_paciente


@router.get("/pacientes/", response_model=List[PacienteSchema])
def listar_pacientes(db: Session = Depends(get_db)):
    return db.query(Paciente).order_by(Paciente.nome).all()


@router.get("/pacientes/{paciente_id}", response_model=PacienteSchema)
def obter_paciente(paciente_id: int, db: Session = Depends(get_db)):
    return get_paciente_or_404(db, paciente_id)


@router.put("/pacientes/{paciente_id}", response_model=PacienteSchema)
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


@router.delete("/pacientes/{paciente_id}")
def excluir_paciente(paciente_id: int, db: Session = Depends(get_db)):
    paciente = get_paciente_or_404(db, paciente_id)
    db.delete(paciente)
    db.commit()
    return {"message": "Paciente excluído com sucesso"}


@router.post("/atendimentos/", response_model=AtendimentoSchema)
def criar_atendimento(atendimento: AtendimentoCreate, db: Session = Depends(get_db)):
    validar_atendimento_referencias(db, atendimento)
    validar_choque_atendimento(db, atendimento)

    novo_atendimento = Atendimento(**atendimento.model_dump())
    db.add(novo_atendimento)
    commit_or_bad_request(db, "Não foi possível cadastrar o atendimento")
    return get_atendimento_or_404(db, novo_atendimento.id)


@router.get("/atendimentos/", response_model=List[AtendimentoSchema])
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


@router.get("/atendimentos/{atendimento_id}", response_model=AtendimentoSchema)
def obter_atendimento(atendimento_id: int, db: Session = Depends(get_db)):
    return get_atendimento_or_404(db, atendimento_id)


@router.put("/atendimentos/{atendimento_id}", response_model=AtendimentoSchema)
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


@router.delete("/atendimentos/{atendimento_id}")
def excluir_atendimento(atendimento_id: int, db: Session = Depends(get_db)):
    atendimento = get_atendimento_or_404(db, atendimento_id)
    db.delete(atendimento)
    db.commit()
    return {"message": "Atendimento excluído com sucesso"}


@router.post("/receitas-saude/", response_model=ReceitaSaudeSchema)
def criar_receita(receita: ReceitaSaudeCreate, db: Session = Depends(get_db)):
    validar_tipo_receita_por_atendimento(db, receita.atendimento_id, receita.tipo.value)
    nova_receita = ReceitaSaude(**receita.model_dump())
    db.add(nova_receita)
    commit_or_bad_request(db, "Não foi possível cadastrar a receita de saúde")
    db.refresh(nova_receita)
    return nova_receita


@router.get("/receitas-saude/", response_model=List[ReceitaSaudeSchema])
def listar_receitas(
    atendimento_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    query = db.query(ReceitaSaude)
    if atendimento_id is not None:
        query = query.filter(ReceitaSaude.atendimento_id == atendimento_id)
    return query.order_by(ReceitaSaude.id.desc()).all()


@router.put("/receitas-saude/{receita_id}", response_model=ReceitaSaudeSchema)
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


@router.delete("/receitas-saude/{receita_id}")
def excluir_receita(receita_id: int, db: Session = Depends(get_db)):
    receita = db.query(ReceitaSaude).filter(ReceitaSaude.id == receita_id).first()
    if not receita:
        raise HTTPException(status_code=404, detail="Receita de saúde não encontrada")
    db.delete(receita)
    db.commit()
    return {"message": "Receita de saúde excluída com sucesso"}


@router.post("/exames-lab/", response_model=ExameLabSchema)
def criar_exame(exame: ExameLabCreate, db: Session = Depends(get_db)):
    get_atendimento_or_404(db, exame.atendimento_id)
    novo_exame = ExameLab(**exame.model_dump())
    db.add(novo_exame)
    commit_or_bad_request(db, "Não foi possível cadastrar o exame laboratorial")
    db.refresh(novo_exame)
    return novo_exame


@router.get("/exames-lab/", response_model=List[ExameLabSchema])
def listar_exames(
    atendimento_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    query = db.query(ExameLab)
    if atendimento_id is not None:
        query = query.filter(ExameLab.atendimento_id == atendimento_id)
    return query.order_by(ExameLab.id.desc()).all()


@router.put("/exames-lab/{exame_id}", response_model=ExameLabSchema)
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


@router.delete("/exames-lab/{exame_id}")
def excluir_exame(exame_id: int, db: Session = Depends(get_db)):
    exame = db.query(ExameLab).filter(ExameLab.id == exame_id).first()
    if not exame:
        raise HTTPException(status_code=404, detail="Exame laboratorial não encontrado")
    db.delete(exame)
    db.commit()
    return {"message": "Exame laboratorial excluído com sucesso"}


@router.post("/prontuarios/", response_model=ProntuarioSchema)
def criar_prontuario(prontuario: ProntuarioCreate, db: Session = Depends(get_db)):
    get_atendimento_or_404(db, prontuario.atendimento_id)
    novo_prontuario = Prontuario(**prontuario.model_dump())
    db.add(novo_prontuario)
    commit_or_bad_request(db, "Atendimento já possui prontuário")
    db.refresh(novo_prontuario)
    return novo_prontuario


@router.get("/prontuarios/", response_model=List[ProntuarioSchema])
def listar_prontuarios(db: Session = Depends(get_db)):
    return db.query(Prontuario).order_by(Prontuario.id.desc()).all()


@router.put("/prontuarios/{prontuario_id}", response_model=ProntuarioSchema)
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


@router.delete("/prontuarios/{prontuario_id}")
def excluir_prontuario(prontuario_id: int, db: Session = Depends(get_db)):
    prontuario = db.query(Prontuario).filter(Prontuario.id == prontuario_id).first()
    if not prontuario:
        raise HTTPException(status_code=404, detail="Prontuário não encontrado")
    db.delete(prontuario)
    db.commit()
    return {"message": "Prontuário excluído com sucesso"}
