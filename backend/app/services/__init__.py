from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..models import Atendimento
from ..schemas import CategoriaProfissional, TipoReceita


TIPOS_RECEITA_POR_CATEGORIA = {
    CategoriaProfissional.MEDICO.value: TipoReceita.REMEDIO.value,
    CategoriaProfissional.FISIOTERAPEUTA.value: TipoReceita.ATIVIDADE_FISICA.value,
    CategoriaProfissional.PSICOLOGO.value: TipoReceita.ATIVIDADE_MENTAL.value,
}


def validar_tipo_receita_por_atendimento(
    db: Session,
    atendimento_id: int,
    tipo_receita: str,
) -> Atendimento:
    atendimento = db.query(Atendimento).filter(Atendimento.id == atendimento_id).first()
    if not atendimento:
        raise HTTPException(status_code=404, detail="Atendimento não encontrado")

    categoria = atendimento.profissional_saude.categoria
    tipo_permitido = TIPOS_RECEITA_POR_CATEGORIA.get(categoria)

    if tipo_receita != tipo_permitido:
        raise HTTPException(
            status_code=400,
            detail=(
                "Tipo de receita incompatível com a categoria do profissional. "
                f"Categoria {categoria} permite apenas {tipo_permitido}."
            ),
        )

    return atendimento
