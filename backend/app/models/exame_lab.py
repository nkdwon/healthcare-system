from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from ..database import Base


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
