from .rag_loader import RAGLoader
import os
from app.models.db_models.document import Document 
from langchain_community.document_loaders import TextLoader
from app.db.sync_session_generator import get_session
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.config import GEMINI_API_KEY



class SmallTextRAGLoader(RAGLoader):

    """
    Clase abstracta que se utilizara para cargar archivos
    de texto pequeños como los de la prueba técnical,
    se podrían usar text_splitters pero en este caso me conviene
    dejar los archivos completos ya que no tienen mucha información
    """
    def __init__(self):
  
        self.embeddings_model = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001", 
            google_api_key=GEMINI_API_KEY,
            task_type="retrieval_document"
        )

    def load_from_file(self, path: str) -> None:

        if not path.endswith(".txt"):
            raise Exception(f"{path} No es un archivo de tipo .txt")
        
        loader = TextLoader(path, encoding="utf-8")
        docs = loader.load()

        session = next(get_session())
        
        try:
            for doc in docs:
                vector = self.embeddings_model.embed_query(doc.page_content)
                
                nuevo_doc = Document(
                    content=doc.page_content,
                    embedding=vector
                )
                session.add(nuevo_doc)
            
            session.commit()
            print(f"Éxito: Documento '{path}' guardado íntegramente.")
        except Exception as e:
            session.rollback()
            print(f"Error: {e}")
            raise
        finally:
            session.close()

    def load_from_folder(self, path:str) -> None:

        files = os.listdir(path)

        for file in files:
            self.load_from_file(path+"/"+file)


