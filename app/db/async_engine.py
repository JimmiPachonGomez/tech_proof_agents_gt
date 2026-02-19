from sqlalchemy.ext.asyncio import create_async_engine
from app.config import DB_ASYNC_URL

"""
Se construye motor asíncrono postgres
"""
async_engine = create_async_engine(DB_ASYNC_URL, echo=False)