from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.orm import relationship

from ..database import Base


class Paciente(Base):
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    cpf = Column(String(14), unique=True, index=True, nullable=False)
    data_nascimento = Column(Date, nullable=False)
    telefone = Column(String(20))

    atendimentos = relationship("Atendimento", back_populates="paciente")
