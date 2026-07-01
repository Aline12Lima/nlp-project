from pydantic import BaseModel, Field
from typing import Literal


class TextRequest(BaseModel):
    """Texto de entrada para análise NLP genérica."""
    text: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="Texto a ser analisado (1 a 5000 caracteres)",
        examples=["I absolutely love this new project!"]
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"text": "I absolutely love this new project!"},
                {"text": "This is the worst experience I've had."},
                {"text": "Aline Silva works at Google in São Paulo."}
            ]
        }
    }


class TranslationRequest(BaseModel):
    """Texto em inglês para tradução para português."""
    text: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="Texto em inglês a ser traduzido"
    )
    source: Literal["en"] = Field(
        default="en",
        description="Idioma de origem (atualmente apenas 'en' suportado)"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"text": "Hello, how are you today?", "source": "en"},
                {"text": "Machine learning is fascinating.", "source": "en"}
            ]
        }
    }


class DocumentRequest(BaseModel):
    """Documento a ser adicionado ao banco vetorial para busca semântica."""
    text: str = Field(
        ...,
        min_length=1,
        description="Conteúdo do documento"
    )
    metadata: dict = Field(
        default={},
        description="Metadados livres (categoria, autor, data etc)"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "text": "FastAPI é um framework Python moderno e muito rápido.",
                    "metadata": {"tema": "tecnologia", "autor": "docs"}
                }
            ]
        }
    }


class SearchRequest(BaseModel):
    """Consulta de busca semântica no banco vetorial."""
    query: str = Field(
        ...,
        min_length=1,
        description="Texto de busca (pergunta ou palavras-chave)"
    )
    top_k: int = Field(
        default=3,
        ge=1,
        le=20,
        description="Quantidade de resultados a retornar (1 a 20)"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"query": "linguagem de programação rápida", "top_k": 3},
                {"query": "framework web moderno", "top_k": 5}
            ]
        }
    }