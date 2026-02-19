from abc import ABC,abstractmethod


class RAGLoader(ABC):
    """
    Clase abstracta que se utilizaría para cargar diferentes
    tipos de archivo en base de datos vectorial
    """

    @abstractmethod
    def load_from_file(self, path:str) -> None:
        pass

    @abstractmethod
    def load_from_folder(self, path:str) -> None:
        pass
