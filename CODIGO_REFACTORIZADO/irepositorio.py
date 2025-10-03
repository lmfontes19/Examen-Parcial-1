"""
INTERFAZ REPOSITORIO
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class IRepositorio(ABC):
    """
    Interfaz abstracta que define el contrato para la persistencia de datos.
    """
    @abstractmethod
    def guardar_datos(self, libros: List[Any], prestamos: List[Any], 
                     contador_libro: int, contador_prestamo: int) -> bool:
        """
        Guarda todos los datos del sistema.
        """
        pass

    @abstractmethod
    def cargar_datos(self) -> Optional[Dict[str, Any]]:
        """
        Carga todos los datos del sistema.
        """
        pass

    @abstractmethod
    def limpiar_datos(self) -> bool:
        """
        Limpia todos los datos del repositorio.
        """
        pass
