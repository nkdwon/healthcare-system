from enum import Enum


class CategoriaProfissional(str, Enum):
    MEDICO = "MEDICO"
    PSICOLOGO = "PSICOLOGO"
    FISIOTERAPEUTA = "FISIOTERAPEUTA"


class TipoReceita(str, Enum):
    REMEDIO = "REMEDIO"
    ATIVIDADE_FISICA = "ATIVIDADE_FISICA"
    ATIVIDADE_MENTAL = "ATIVIDADE_MENTAL"


class StatusAtendimento(str, Enum):
    AGENDADO = "AGENDADO"
    REALIZADO = "REALIZADO"
    CANCELADO = "CANCELADO"
