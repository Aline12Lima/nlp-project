from fastapi import APIRouter

router = APIRouter()


@router.get(
    "/",
    summary="Health check da API",
    responses={200: {"description": "API está saudável e respondendo"}},
)
def health_check():
    """
    Endpoint simples de verificação de saúde.

    Usado por orquestradores (Docker, Kubernetes) para saber se a API
    está pronta para receber requisições.
    """
    return {"status": "ok"}
