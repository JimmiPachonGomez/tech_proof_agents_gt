from sqlalchemy import create_engine
from app.config import DB_SYNC_URL

"""
Se construye motor síncrono postgres
"""
sync_engine = create_engine(DB_SYNC_URL, echo=False)