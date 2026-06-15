from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class Paciente(Base):
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    cpf = Column(String(14), unique=True, index=True, nullable=False)
    data_nascimento = Column(Date, nullable=False)
    telefone = Column(String(20))

    agendamentos = relationship("Agendamento", back_populates="paciente")

class Medico(Base):
    __tablename__ = "medicos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    crm = Column(String(20), unique=True, index=True, nullable=False)
    especialidade = Column(String(100), nullable=False)

    agendamentos = relationship("Agendamento", back_populates="medico")

class Agendamento(Base):
    __tablename__ = "agendamentos"

    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id", ondelete="CASCADE"))
    medico_id = Column(Integer, ForeignKey("medicos.id", ondelete="CASCADE"))
    data_hora = Column(DateTime, nullable=False)
    status = Column(String(20), default="Agendado")

    paciente = relationship("Paciente", back_populates="agendamentos")
    medico = relationship("Medico", back_populates="agendamentos")
    prontuario = relationship("Prontuario", back_populates="agendamento", uselist=False)

class Prontuario(Base):
    __tablename__ = "prontuarios"

    id = Column(Integer, primary_key=True, index=True)
    agendamento_id = Column(Integer, ForeignKey("agendamentos.id", ondelete="CASCADE"), unique=True)
    observacoes = Column(Text, nullable=False)
    data_criacao = Column(DateTime, default=datetime.utcnow)

    agendamento = relationship("Agendamento", back_populates="prontuario")
