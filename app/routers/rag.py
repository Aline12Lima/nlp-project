from fastapi import APIRouter, HTTPException

from app.schemas.requests import DocumentRequest, SearchRequest
from app.schemas.responses import DocumentResponse, SearchResponse, SearchResult
from app.services.chroma_service import add_document, count_documents, search_documents

router = APIRouter()


@router.post(
    "/documents",
    response_model=DocumentResponse,
    summary="Adiciona documento ao banco vetorial",
    responses={
        200: {"description": "Documento indexado com sucesso"},
        500: {"description": "Erro ao gerar embedding ou salvar no ChromaDB"},
    },
)
def add_doc(body: DocumentRequest):
    """
    Adiciona um documento ao ChromaDB para busca semântica posterior.

    ### Fluxo interno
    1. Gera embedding de 384 dimensões do texto
    2. Cria UUID único para o documento
    3. Persiste vetor + texto + metadados no ChromaDB

    ### Metadados
    Os metadados são livres — pode ser categoria, autor, data, tags etc.
    São úteis para filtrar resultados em buscas futuras.
    """
    try:
        doc_id = add_document(body.text, body.metadata)
        return DocumentResponse(id=doc_id, text=body.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post(
    "/search",
    response_model=SearchResponse,
    summary="Busca documentos por similaridade semântica",
    responses={
        200: {"description": "Busca concluída"},
        500: {"description": "Erro ao processar a query"},
    },
)
def search(body: SearchRequest):
    """
    Realiza busca por **significado** (não por palavras-chave) usando
    similaridade de cosseno entre vetores.

    ### Como funciona
    1. Query é transformada em embedding
    2. ChromaDB calcula distância para todos os documentos indexados
    3. Retorna os `top_k` mais próximos

    ### Interpretação da distância
    - **Menor** = mais similar semanticamente
    - Valores típicos: 0 a 2 (depende da normalização)

    ### Exemplo prático
    Query: `"linguagem de programação rápida"`
    Retorna: `"FastAPI é um framework Python moderno"` mesmo sem palavras em comum,
    porque o **significado** é próximo no espaço vetorial.
    """
    try:
        results = search_documents(body.query, body.top_k)
        return SearchResponse(
            query=body.query,
            results=[SearchResult(**r) for r in results],
            total=len(results),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get(
    "/stats",
    summary="Estatísticas do banco vetorial",
    responses={200: {"description": "Estatísticas retornadas"}},
)
def get_stats():
    """
    Retorna a quantidade total de documentos indexados no ChromaDB.

    Útil para monitorar o crescimento da base de conhecimento.
    """
    return {"total_documents": count_documents()}
