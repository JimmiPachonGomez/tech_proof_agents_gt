import asyncio
from functools import wraps
from .logger import logger




"""
En este archivo se deben definen los decoradores que 
se usen de forma auxiliar en otros archivos
"""

def async_retry(times: int = 3, delay: float = 3.0):
    """
    Este decorador se encarga de reintentar una función
    un número determinado de veces(por defecto 3) en caso
    de error
    """


    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, times + 1):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    logger.error(f"Error en intento {attempt}/{times}: {e}")

                    if attempt < times and delay > 0:
                        await asyncio.sleep(delay)
            
            
            raise last_exception
        return wrapper
    return decorator



