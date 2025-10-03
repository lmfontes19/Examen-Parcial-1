"""
REPOSITORIO BIBLIOTECA
"""

import json
import os
from typing import List, Dict, Any, Optional

class RepositorioBiblioteca:
    """
    Clase responsable de la persistencia de datos del sistema.
    """
    def __init__(self, archivo_path: str = "biblioteca.txt"):
        """
        Inicializa el repositorio con la ruta del archivo de persistencia.

        Args:
            archivo_path: Ruta del archivo donde se guardaran los datos
        """
        self.archivo_path = archivo_path
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        """
        Asegura que el archivo de persistencia exista.
        Si no existe, lo crea con estructura basica.
        """
        if not os.path.exists(self.archivo_path):
            datos_iniciales = {
                "libros": [],
                "prestamos": [],
                "contadores": {
                    "libro": 1,
                    "prestamo": 1
                }
            }
            self._escribir_archivo(datos_iniciales)

    def guardar_datos(self, libros: List[Any], prestamos: List[Any],
                     contador_libro: int, contador_prestamo: int) -> bool:
        """
        Guarda todos los datos del sistema en el archivo de persistencia.
        """
        try:
            datos = {
                "libros": [self._libro_a_dict(libro) for libro in libros],
                "prestamos": [self._prestamo_a_dict(prestamo) for prestamo in prestamos],
                "contadores": {
                    "libro": contador_libro,
                    "prestamo": contador_prestamo
                }
            }

            return self._escribir_archivo(datos)
        except Exception as e:
            print(f"Error al guardar datos: {e}")
            return False

    def cargar_datos(self) -> Optional[Dict[str, Any]]:
        """
        Carga todos los datos desde el archivo de persistencia.
        """
        try:
            return self._leer_archivo()
        except Exception as e:
            print(f"Error al cargar datos: {e}")
            return None

    def _libro_a_dict(self, libro: Any) -> Dict[str, Any]:
        """
        Convierte un objeto libro a diccionario para persistencia.
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
        Convierte un objeto préstamo a diccionario para persistencia.
        """
        return {
            "id": prestamo.id,
            "libro_id": prestamo.libro_id,
            "usuario": prestamo.usuario,
            "fecha": prestamo.fecha,
            "devuelto": prestamo.devuelto
        }

    def _escribir_archivo(self, datos: Dict[str, Any]) -> bool:
        """
        Escribe datos en el archivo de persistencia.
        """
        try:
            with open(self.archivo_path, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error al escribir archivo: {e}")
            return False

    def _leer_archivo(self) -> Optional[Dict[str, Any]]:
        """
        Lee datos desde el archivo de persistencia.
        """
        try:
            with open(self.archivo_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Archivo no encontrado: {self.archivo_path}")
            return None
        except json.JSONDecodeError as e:
            print(f"Error al decodificar JSON: {e}")
            return None
        except Exception as e:
            print(f"Error al leer archivo: {e}")
            return None
