from langchain.tools import tool
from pydantic import BaseModel, Field
from app.services.poke_api_client import PokeAPIClient

"""
Se construye una tool para buscar información de un pokemon en específico
"""

class PokemonSearchInput(BaseModel):
    name: str = Field(description="Es el nombre del pokemon que debes buscar")

@tool("get_pokemon_info", args_schema=PokemonSearchInput)
async def get_pokemon_info(name: str):
    """
    Consulta la PokeAPI para obtener detalles e información de un Pokémon específico,
    se puede obtener su peso,altura,habilidades y tipos.
    """
    poke_client = PokeAPIClient()
    result = await poke_client.get_pokemon(name)
    return result