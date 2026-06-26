from pydantic import BaseModel
from typing import Literal

class TextRequest(BaseModel):
    text: str

    model_config = {
        "json_schema_extra": {
            "examples": [{"text": "I love this product!"}]
        }
    }

class TranslationRequest(BaseModel):
    text: str
    source: Literal["en"] = "en"  # apenas EN→PT por enquanto

    model_config = {
        "json_schema_extra": {
            "examples": [{"text": "I love this product!", "source": "en"}]
        }
    }

class DocumentRequest(BaseModel):
    text: str
    metadata: dict = {}

class SearchRequest(BaseModel):
    query: str
    top_k: int = 3