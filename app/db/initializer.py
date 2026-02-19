from sqlalchemy import create_engine, text
from sqlalchemy_utils import database_exists, create_database, drop_database
from app.models.db_models.base import Base
from app.models.db_models.request import Request
from app.models.db_models.document import Document
from app.models.db_models.chat_message_history import ChatMessageHistory
from .sync_engine import sync_engine
from app.config import DB_SYNC_URL, DB_NAME, BASE_SYNC_URL


"""
init_db se usa para construir la base de datos apenas se arranca la aplicación,
esto claramente no se debe hacer en producción
"""


def init_db():
    admin_engine = create_engine(f"{BASE_SYNC_URL}postgres", isolation_level="AUTOCOMMIT")
    
    with admin_engine.connect() as conn:
        
        conn.execute(text(f"""
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = '{DB_NAME}'
              AND pid <> pg_backend_pid();
        """))
    if database_exists(DB_SYNC_URL):
        drop_database(DB_SYNC_URL)
    create_database(DB_SYNC_URL)

    sync_engine = create_engine(DB_SYNC_URL)
    with sync_engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        conn.commit()

    Base.metadata.create_all(sync_engine)

if __name__ == "__main__":
    init_db()