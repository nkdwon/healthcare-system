from sqlalchemy import Column, ForeignKey, Integer, Text, String
from sqlalchemy.orm import relationship

from ..database import Base


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
