from pydantic import BaseModel

class TextRequest(BaseModel):
    text: str

    model_config = {
        "json_schema_extra": {
            "examples": [{"text": "I love this product!"}]
        }
    }