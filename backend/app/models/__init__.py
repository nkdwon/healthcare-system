from sqlalchemy import Column, Date, ForeignKey, Integer, String, Text, Time, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import DateTime

from ..database import Base


class ProfissionalSaude(Base):
    __tablename__ = "profissionais_saude"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    telefone = Column(String(20))
    endereco = Column(String(150))
    categoria = Column(String(30), nullable=False)

    atendimentos = relationship(
        "Atendimento",
        back_populates="profissional_saude",
        cascade="all, delete-orphan",
    )


class Paciente(Base):
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    cpf = Column(String(14), unique=True, index=True, nullable=False)
    data_nascimento = Column(Date, nullable=False)
    telefone = Column(String(20))

    atendimentos = relationship("Atendimento", back_populates="paciente")


class Atendimento(Base):
    __tablename__ = "atendimentos"
    __table_args__ = (
        UniqueConstraint(
            "profissional_saude_id",
            "data_atendimento",
            "horario_atendimento",
            name="uq_atendimentos_profissional_data_horario",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    profissional_saude_id = Column(
        Integer,
        ForeignKey("profissionais_saude.id", ondelete="CASCADE"),
        nullable=False,
    )
    paciente_id = Column(Integer, ForeignKey("pacientes.id", ondelete="SET NULL"))
    data_atendimento = Column(Date, nullable=False)
    horario_atendimento = Column(Time, nullable=False)
    problema_texto = Column(Text, nullable=False)
    status = Column(String(20), default="AGENDADO")

    profissional_saude = relationship("ProfissionalSaude", back_populates="atendimentos")
    paciente = relationship("Paciente", back_populates="atendimentos")
    receitas_saude = relationship(
        "ReceitaSaude",
        back_populates="atendimento",
        cascade="all, delete-orphan",
    )
    exames_lab = relationship(
        "ExameLab",
        back_populates="atendimento",
        cascade="all, delete-orphan",
    )
    prontuario = relationship(
        "Prontuario",
        back_populates="atendimento",
        cascade="all, delete-orphan",
        uselist=False,
    )


class ReceitaSaude(Base):
    __tablename__ = "receitas_saude"

    id = Column(Integer, primary_key=True, index=True)
    atendimento_id = Column(
        Integer,
        ForeignKey("atendimentos.id", ondelete="CASCADE"),
        nullable=False,
    )
    descricao = Column(Text, nullable=False)
    tipo = Column(String(30), nullable=False)

    atendimento = relationship("Atendimento", back_populates="receitas_saude")


class ExameLab(Base):
    __tablename__ = "exames_lab"

    id = Column(Integer, primary_key=True, index=True)
    atendimento_id = Column(
        Integer,
        ForeignKey("atendimentos.id", ondelete="CASCADE"),
        nullable=False,
    )
    descricao = Column(Text, nullable=False)

    atendimento = relationship("Atendimento", back_populates="exames_lab")


class Prontuario(Base):
    __tablename__ = "prontuarios"

    id = Column(Integer, primary_key=True, index=True)
    atendimento_id = Column(
        Integer,
        ForeignKey("atendimentos.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    observacoes = Column(Text, nullable=False)
    data_criacao = Column(DateTime, server_default=func.current_timestamp())

    atendimento = relationship("Atendimento", back_populates="prontuario")
