# Pydantic
from pydantic import BaseModel, Field


class ResponseSchema(BaseModel):
    response: str = Field(...) 

    