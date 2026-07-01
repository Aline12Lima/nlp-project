from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.requests import TextRequest, TranslationRequest
from app.schemas.responses import (
    SentimentResponse,
    NERResponse,
    EntityResponse,
    TranslationResponse,
    EmbeddingResponse,
)
from app.models.hf_loader import (
    get_sentiment_model,
    get_ner_model,
    get_translation_model,
    get_embeddings_model,
)
from app.database.connection import get_db
from app.services.history_service import save_history
from app.services.redis_service import get_cached, set_cached

router = APIRouter()


@router.post(
    "/sentiment",
    response_model=SentimentResponse,
    summary="Analisa o sentimento de um texto",
    responses={
        200: {"description": "Análise concluída com sucesso"},
        422: {"description": "Payload inválido"},
        500: {"description": "Erro interno ao processar o modelo"},
    },
)
def analyze_sentiment(body: TextRequest, db: Session = Depends(get_db)):
    """
    Classifica um texto em **positive**, **negative** ou **neutral** usando o modelo
    `cardiffnlp/twitter-roberta-base-sentiment-latest`.

    ### Fluxo
    1. Verifica se o resultado está em cache no Redis (TTL 1h)
    2. Se estiver, retorna imediatamente (~50ms)
    3. Se não estiver, roda o modelo (~900ms), salva em cache e no histórico

    ### Casos de uso
    - Análise de feedback de clientes
    - Monitoramento de redes sociais
    - Priorização de tickets de suporte
    """
    try:
        cached = get_cached("sentiment", body.text)
        if cached:
            return SentimentResponse(**cached)

        model = get_sentiment_model()
        result = model(body.text)[0]
        response = SentimentResponse(
            text=body.text,
            label=result["label"],
            score=round(result["score"], 4),
        )

        set_cached("sentiment", body.text, response.model_dump())
        save_history(db, "sentiment", body.text, response.model_dump())
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/ner",
    response_model=NERResponse,
    summary="Reconhece entidades nomeadas em um texto",
    responses={
        200: {"description": "Entidades identificadas com sucesso"},
        422: {"description": "Payload inválido"},
        500: {"description": "Erro interno ao processar o modelo"},
    },
)
def extract_entities(body: TextRequest, db: Session = Depends(get_db)):
    """
    Identifica entidades nomeadas (pessoas, organizações, lugares) usando
    o modelo `dbmdz/bert-large-cased-finetuned-conll03-english`.

    ### Tipos de entidades detectadas
    - **PER** — pessoas (nomes próprios)
    - **ORG** — organizações e empresas
    - **LOC** — lugares e localizações geográficas
    - **MISC** — outras entidades relevantes

    ### Retorno
    Cada entidade inclui a posição (start/end) no texto original,
    útil para destacar ou processar em pipelines posteriores.
    """
    try:
        cached = get_cached("ner", body.text)
        if cached:
            return NERResponse(**cached)

        model = get_ner_model()
        results = model(body.text)
        entities = [
            EntityResponse(
                word=r["word"],
                entity=r["entity_group"],
                score=round(r["score"], 4),
                start=r["start"],
                end=r["end"],
            )
            for r in results
        ]
        response = NERResponse(text=body.text, entities=entities)

        set_cached("ner", body.text, response.model_dump())
        save_history(db, "ner", body.text, response.model_dump())
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/translate",
    response_model=TranslationResponse,
    summary="Traduz texto do inglês para o português",
    responses={
        200: {"description": "Tradução concluída"},
        422: {"description": "Payload inválido"},
        500: {"description": "Erro interno ao processar o modelo"},
    },
)
def translate_text(body: TranslationRequest, db: Session = Depends(get_db)):
    """
    Traduz um texto em inglês para português usando o modelo
    `Helsinki-NLP/opus-mt-tc-big-en-pt` (arquitetura MarianMT).

    ### Direção suportada
    Atualmente apenas **EN → PT**. A direção inversa pode ser adicionada
    em versões futuras com um segundo modelo.

    ### Notas
    - Boa qualidade em textos formais e conversacionais
    - Textos muito curtos podem ter menor precisão
    - Resultado é cacheado por 1 hora
    """
    try:
        cached = get_cached("translate", body.text)
        if cached:
            return TranslationResponse(**cached)

        model = get_translation_model()
        result = model(body.text)[0]
        response = TranslationResponse(
            original=body.text,
            translated=result["translation_text"],
            source="en",
            target="pt",
        )

        set_cached("translate", body.text, response.model_dump())
        save_history(db, "translate", body.text, response.model_dump())
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/embeddings",
    response_model=EmbeddingResponse,
    summary="Gera vetor semântico de 384 dimensões",
    responses={
        200: {"description": "Embedding gerado"},
        422: {"description": "Payload inválido"},
        500: {"description": "Erro interno ao processar o modelo"},
    },
)
def generate_embeddings(body: TextRequest, db: Session = Depends(get_db)):
    """
    Transforma um texto em um vetor numérico de **384 dimensões** usando
    o modelo `sentence-transformers/all-MiniLM-L6-v2`.

    ### Aplicações
    - Base para busca semântica (RAG)
    - Cálculo de similaridade entre textos
    - Clustering e classificação não-supervisionada
    - Input para outros modelos de ML

    ### Observação sobre cache
    Este endpoint **não usa cache Redis** — vetores de 384 floats ocupam
    memória demais e são raramente reutilizados. Se precisar armazenar,
    considere usar o endpoint `/rag/documents`.
    """
    try:
        model = get_embeddings_model()
        vector = model.encode(body.text).tolist()
        response = EmbeddingResponse(
            text=body.text,
            embedding=vector,
            dimensions=len(vector),
        )
        save_history(db, "embeddings", body.text, {"dimensions": len(vector)})
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))