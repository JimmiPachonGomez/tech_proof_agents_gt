from sqlalchemy.orm import sessionmaker
from .sync_engine import sync_engine  


"""
Se construye generador de sesiones síncrono
"""

SessionLocal = sessionmaker(bind=sync_engine, autocommit=False, autoflush=False)

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()