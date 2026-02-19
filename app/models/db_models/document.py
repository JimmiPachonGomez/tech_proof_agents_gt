from sqlalchemy import Column, Text, Integer
from pgvector.sqlalchemy import Vector
from .base import Base


"""
Es el registro que deja el embedding en la tabla documents,
se usa para el sistema RAG
"""
class Document(Base):
    __tablename__ = 'documents'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text, nullable=False)
    embedding = Column(Vector(3072))
