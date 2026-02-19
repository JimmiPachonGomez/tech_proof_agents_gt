
from app.utils.async_request_handler import AsyncRequestHandler
from app.models.validation_models.poke_api_models import Pokemon


"""
Clase Cliente de la API de Pokemon, con el método que me pareció suficiente
para cumplir con los enunciados. Trae varia información de los pokemones
"""
class PokeAPIClient:
    def __init__(self):
        self.base_url = "https://pokeapi.co/api/v2"

    async def get_pokemon(self, name: str):
        """Obtiene un pokemon por nombre"""
        url = f"{self.base_url}/pokemon/{str(name).lower()}"
        response= await AsyncRequestHandler.do_request("GET", url)

        if response.status_code!=200:
            return {"message":f"El Pokemón no existe"}
        
        return Pokemon.model_validate(response.json()).model_dump()




