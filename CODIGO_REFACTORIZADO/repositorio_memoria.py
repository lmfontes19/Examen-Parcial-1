"""
REPOSITORIO MEMORIA
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from irepositorio import IRepositorio

class RepositorioMemoria(IRepositorio):
    """
    Implementacion del repositorio que mantiene datos en memoria.
    """
    def __init__(self):
        """
        Inicializa el repositorio en memoria.
        """
        self.datos = {
            "libros": [],
            "prestamos": [],
            "contadores": {
                "libro": 1,
                "prestamo": 1
            }
        }

    def guardar_datos(self, libros: List[Any], prestamos: List[Any],
                     contador_libro: int, contador_prestamo: int) -> bool:
        """
        Guarda datos en la estructura de memoria.
        """
        try:
            self.datos = {
                "libros": [self._libro_a_dict(libro) for libro in libros],
                "prestamos": [self._prestamo_a_dict(prestamo) for prestamo in prestamos],
                "contadores": {
                    "libro": contador_libro,
                    "prestamo": contador_prestamo
                }
            }
            return True
        except Exception as e:
            print(f"Error al guardar en memoria: {e}")
            return False

    def cargar_datos(self) -> Optional[Dict[str, Any]]:
        """
        Retorna los datos almacenados en memoria.
        """
        try:
            import copy
            return copy.deepcopy(self.datos)
        except Exception as e:
            print(f"Error al cargar datos de memoria: {e}")
            return None

    def limpiar_datos(self) -> bool:
        """
        Limpia todos los datos manteniendo estructura basica.
        """
        try:
            self.datos = {
                "libros": [],
                "prestamos": [],
                "contadores": {
                    "libro": 1,
                    "prestamo": 1
                }
            }
            return True

        except Exception as e:
            print(f"Error al limpiar memoria: {e}")
            return False

    def _libro_a_dict(self, libro: Any) -> Dict[str, Any]:
        """
        Convierte un objeto libro a diccionario.
        """
        return {
            "id": libro.id,
            "titulo": libro.titulo,
            "autor": libro.autor,
            "isbn": libro.isbn,
            "disponible": libro.disponible
        }

    def _prestamo_a_dict(self, prestamo: Any) -> Dict[str, Any]:
        """
        Convierte un objeto prestamo a diccionario.
        """
        return {
            "id": prestamo.id,
            "libro_id": prestamo.libro_id,
            "usuario": prestamo.usuario,
            "devuelto": prestamo.devuelto,
            "fecha": prestamo.fecha
        }
