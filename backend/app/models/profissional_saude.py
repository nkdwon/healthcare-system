from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

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
