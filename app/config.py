import os
from dotenv import load_dotenv

"""
En este archivo cargo las variables de entorno
"""

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")


BASE_SYNC_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/"
DB_SYNC_URL = f"{BASE_SYNC_URL}{DB_NAME}"

DB_ASYNC_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")