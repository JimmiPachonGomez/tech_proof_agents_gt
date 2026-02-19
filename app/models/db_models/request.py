import uuid
import enum
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from .base import Base


"""
Esta tabla se iba a usar para llevar un registro de las peticiones y calcular
el tiempo de duración, pero no llegó a implementarse

"""
class HttpMethod(enum.Enum):
    GET = "GET"
    POST = "POST"
    PATCH = "PATCH"
    DELETE = "DELETE"
    PUT = "PUT"

class Request(Base):
    __tablename__ = 'requests'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    method = Column(Enum(HttpMethod), nullable=False)
    headers = Column(JSONB)
    params = Column(JSONB)
    body = Column(JSONB)
    duration = Column(Integer) 
    start_time = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    end_time = Column(DateTime(timezone=True))