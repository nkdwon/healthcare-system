from fastapi import APIRouter
from .profissional_saude import router as profissional_router
from .paciente import router as paciente_router
from .atendimento import router as atendimento_router
from .receita_saude import router as receita_router
from .exame_lab import router as exame_router
from .prontuario import router as prontuario_router

router = APIRouter()

router.include_router(profissional_router)
router.include_router(paciente_router)
router.include_router(atendimento_router)
router.include_router(receita_router)
router.include_router(exame_router)
router.include_router(prontuario_router)
