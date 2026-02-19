from fastapi import FastAPI
from app.agents.puppets.meetings_graph.meetings_graph import ask_meeting_agent
from app.agents.puppets.poke_agent.poke_agent import ask_poke_agent
from app.models.validation_models.local_api_models import Query
import uvicorn

"""
Se construyen dos endpoints sencillos de consumo en el archivo main
"""


app = FastAPI(title="AI Agents")

@app.post("/ask")
async def ask_meeting(query: Query):
    """
    Endpoint para interactuar con el agente de reuniones.
    """
    query_string = query.query
    response = await ask_meeting_agent(query_string)
    return {"ai": response}

@app.post("/agent")
async def ask_pokemon(query: Query):
    """
    Endpoint para interactuar con el agente de Pokémon.
    """
    query_string = query.query
    response = await ask_poke_agent(query_string)
    return {"ai": response}


if __name__ == "__main__":

    from app.db.initializer import init_db
    from app.agents.loaders.text_rag_loader import SmallTextRAGLoader

    """
    Se construye la base de datos en el arranque de la aplicación,
    también se crean los vectores para el sistema RAG
    """
    init_db()
    text_loader = SmallTextRAGLoader()
    text_loader.load_from_folder("app/agents/rag_documents")



    
    uvicorn.run(
        "app.api.main:app",
        host="0.0.0.0", 
        port=8000, 
        reload=True
    )