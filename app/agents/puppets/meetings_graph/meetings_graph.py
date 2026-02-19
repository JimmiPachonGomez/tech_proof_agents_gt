from typing import Annotated, TypedDict, Any
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain.messages import HumanMessage,SystemMessage
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from sqlalchemy import select
from app.db.async_session_generator import get_async_session 
from app.models.db_models.document import Document
from langchain.chat_models import init_chat_model
from pydantic import BaseModel,Field

class State(TypedDict):
    messages: Annotated[list, add_messages]
    final_output: Any
    meeting_related: bool
    documents: list[str]

#--------------------------------------GUARDRAIL--------------------------------------------------------

guardrail_model = init_chat_model("gemini-2.5-flash", model_provider="google_genai", temperature=0.0)

class OutputParserGuardrail(BaseModel):
    meeting_related: bool = Field(description="Determina si la consulta está relacionada con las reuniones")


prompt_guardrail = """Tu misión es determinar si la consulta del usuario tiene 
                    relación con reuniones o si tiene preguntas.
                    
                    En caso de tener preguntas genuinas meeting_related es True"""


guardrail_chain = guardrail_model.with_structured_output(OutputParserGuardrail)


#------------------------------------ASSISTANT--------------------------------------------------------

assistant_model = init_chat_model("gemini-2.5-flash", model_provider="google_genai", temperature=0.0)

prompt_assistant = """El usuario te ha preguntado acerca de reuniones pasadas, respondele acorde a
                        la información que tengas"""


assistant_chain = assistant_model


#------------------------------------GRAFO-------------------------------------------------------------

class MeetingsGraph:
    """
    Contiene la lógica del grafo del agente de reuniones en LangGraph,
    tiene un Guardrail que impide hablar de otro tema. Envía un mensaje
    predeterminado pero perfectamente podría ser generado por IA.
    """

    def __init__(self,
                 guardrail_chain=guardrail_chain,
                 assistant_chain=assistant_chain):

        self.guardrail_chain = guardrail_chain
        self.assistant_chain = assistant_chain

    def build(self):
        builder = StateGraph(State)
        builder.add_node("guardrail", self.guardrail)
        builder.add_node("negative_response", self.negative_response)
        builder.add_node("retriever", self.retriever)
        builder.add_node("assistant", self.assistant)

        builder.add_edge(START, "guardrail")
        builder.add_conditional_edges("guardrail", self.router)
        builder.add_edge("retriever", "assistant")
        builder.add_edge("negative_response", END)
        builder.add_edge("assistant", END)

        graph = builder.compile()

        return graph
    

    async def guardrail(self,state: State):
         response = await self.guardrail_chain.ainvoke([
                                SystemMessage(prompt_guardrail),
                                state["messages"][-1]
                             ])
         return {"meeting_related": response.meeting_related}
    

    async def router(self,state: State):
        if state["meeting_related"]:
            return "retriever"
        return "negative_response"
    

    async def negative_response(self,state: State):
        return {"final_output": "Sólo se responden preguntas acerca de las reuniones"}
    

    async def retriever(self,state: State):
        user_input = state["messages"][-1].content
        
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            task_type="retrieval_query"
        )
      
        query_vector = await embeddings.aembed_query(user_input)
        
        async for session in get_async_session():
            statement = (
                select(Document)
                .order_by(Document.embedding.cosine_distance(query_vector))
                .limit(2)
            )
            result = await session.execute(statement)
            docs = result.scalars().all()

            return {"documents": [doc.content for doc in docs]}
        
    
    async def assistant(self,state: State):
        messages = [
            SystemMessage(prompt_assistant),
            state["messages"][-1],
            HumanMessage(content=f"Documents: {state['documents']}")
        ]
        response = await self.assistant_chain.ainvoke(messages)
        return {
            "final_output": response.content,
            "messages": [response]
        }
    

meeting_graph = MeetingsGraph()
meeting_graph = meeting_graph.build()


async def ask_meeting_agent(query: str):
    
    input_human = HumanMessage(query)
    response = await meeting_graph.ainvoke({"messages":[input_human]})
    return response["final_output"]