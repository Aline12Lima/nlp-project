from fastapi import APIRouter, HTTPException
from app.schemas.requests import DocumentRequest, SearchRequest
from app.schemas.responses import DocumentResponse, SearchResponse, SearchResult
from app.services.chroma_service import add_document, search_documents, count_documents

router = APIRouter()


@router.post("/documents", response_model=DocumentResponse)
def add_doc(body: DocumentRequest):
    try:
        doc_id = add_document(body.text, body.metadata)
        return DocumentResponse(id=doc_id, text=body.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/search", response_model=SearchResponse)
def search(body: SearchRequest):
    try:
        results = search_documents(body.query, body.top_k)
        return SearchResponse(
            query=body.query,
            results=[SearchResult(**r) for r in results],
            total=len(results),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
def get_stats():
    return {"total_documents": count_documents()}