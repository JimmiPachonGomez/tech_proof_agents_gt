from pydantic import BaseModel, Field, field_validator
from typing import Any


"""
Modelos para validar los datos de entrada de la API de pokemón
"""

class Ability(BaseModel):
    name: str
    url: str

class AbilityDict(BaseModel):
    ability:Ability

class Type(BaseModel):
    name:str
    url:str

class Pokemon(BaseModel):
    id: int
    name: str
    height: float
    weight: float
    abilities: list[AbilityDict]
    types: list[Type] | None

    @field_validator('types', mode='before')
    @classmethod
    def transform_types(cls, v: list[dict]|None ) -> list[dict]|None:
        if isinstance(v, list):
            return [item.get('type') for item in v if isinstance(item, dict) and 'type' in item]
        return v