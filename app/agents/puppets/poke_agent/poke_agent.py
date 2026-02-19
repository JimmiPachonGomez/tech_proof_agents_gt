from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model
from .search_pokemon_tool import get_pokemon_info
from langchain_core.messages import HumanMessage, SystemMessage
from app.config import GEMINI_API_KEY
from pydantic import BaseModel

"""
En este archivo se construye el agente que responde acerca de Pokemón,
en este caso se usa una construcción predeterminada. Sin embargo estas construcciones
no son tan confiables ni tan escalables y personalizables como los grafos.
"""


class BasicOutput(BaseModel):
    output:str



model = init_chat_model("gemini-2.5-flash", model_provider="google_genai", temperature=0.0)

poke_prompt = """
                Eres un experto Profesor Pokémon. Responde de forma breve y trata de ayudar al
                usuario conociendo todo lo que puedan sobre los pokemon
                """


tools = [get_pokemon_info]

agent_executor = create_react_agent(model, tools, response_format=BasicOutput) 

async def ask_poke_agent(query: str):
    inputs = {
        "messages": [
            SystemMessage(content=poke_prompt), 
            HumanMessage(content=query)
        ]
    }
    
    response = await agent_executor.ainvoke(inputs)
    
    
    return response["structured_response"].output


