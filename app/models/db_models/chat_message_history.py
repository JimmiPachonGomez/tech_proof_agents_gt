from sqlalchemy import Column, Text, Integer
from sqlalchemy.dialects.postgresql import JSONB
from .base import Base


"""Esta tabla serviría para agregarle memoria a los agentes,
pero no llegó a implementarse"""
class ChatMessageHistory(Base):
    __tablename__ = 'chat_message_history'
    
    id = Column(
                Integer, 
                primary_key=True, 
                autoincrement=True
            )
    
    session_id = Column(Text, nullable=False, index=True)
    
    message = Column(JSONB, nullable=False)