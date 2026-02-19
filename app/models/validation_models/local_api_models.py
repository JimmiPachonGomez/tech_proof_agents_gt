from pydantic import BaseModel

"""
Es el body que se espera en la petición,
solamente es una query
"""

class Query(BaseModel):
    query:str