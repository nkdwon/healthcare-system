from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import DateTime

from ..database import Base


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
