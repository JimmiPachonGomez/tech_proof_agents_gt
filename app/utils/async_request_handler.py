import httpx
from .decorators import async_retry
from .logger import logger

"""
En este archivo se define una clase para manejar las peticiones asíncronas
"""


class AsyncRequestHandler:

    @async_retry()
    @staticmethod
    async def do_request(method,url,headers=None,body=None,params=None,timeout=10):
        logger.info(f"Iniciando petición {method} a {url}")

        async with httpx.AsyncClient(timeout=httpx.Timeout(10.0, connect=5.0)) as client:
            response = await client.request(
                                            method=method,
                                            url=url,
                                            headers=headers,
                                            json=body,
                                            params=params,
                                            timeout=timeout
                                            )
            logger.debug(f"Status de respuesta: {response.status_code}")

            return response
          