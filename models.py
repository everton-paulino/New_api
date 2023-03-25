import uuid
from typing import Optional
from pydantic import BaseModel, Field

class Register(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)
    cpf: str = Field(...)
    createdAt: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "name": "Don Quixote",
                "cpf": "767.633.970-70",
                "createdAt": "25/03/2023"
            }
        }


class RegisterUpdate(BaseModel):
    name: Optional[str]
    cpf: Optional[str]
    createdAt: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "name": "Don Quixote",
                "cpf": "Miguel de Cervantes",
                "createdAt": "25/03/2023"
            }
        }
