from sqlalchemy import Column, Date, ForeignKey, Integer, Text, Time, UniqueConstraint
from sqlalchemy.orm import relationship

from ..database import Base


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
