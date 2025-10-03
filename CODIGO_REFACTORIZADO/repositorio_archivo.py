"""
REPOSITORIO ARCHIVO
"""

import json
import os
from typing import List, Dict, Any, Optional
from irepositorio import IRepositorio

class RepositorioArchivo(IRepositorio):
    """
    Implementacion concreta del repositorio usando archivos JSON.
    """
    def __init__(self, archivo_path: str = "biblioteca.json"):
        """
        Inicializa el repositorio con la ruta del archivo.
        """
        self.archivo_path = archivo_path
        self._asegurar_archivo_existe()

    def guardar_datos(self, libros: List[Any], prestamos: List[Any], 
                     contador_libro: int, contador_prestamo: int) -> bool:
        """
        Guarda todos los datos del sistema en archivo JSON.
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
        Carga todos los datos desde el archivo JSON.
        """
        try:
            return self._leer_archivo()
        except Exception as e:
            print(f"Error al cargar datos: {e}")
            return None

    def limpiar_datos(self) -> bool:
        """
        Limpia el archivo de datos manteniendo estructura basica.
        """
        try:
            datos_limpios = {
                "libros": [],
                "prestamos": [],
                "contadores": {
                    "libro": 1,
                    "prestamo": 1
                }
            }

            return self._escribir_archivo(datos_limpios)
        except Exception as e:
            print(f"Error al limpiar datos: {e}")
            return False

    def existe_repositorio(self) -> bool:
        """
        Verifica si el archivo del repositorio existe.
        """
        return os.path.exists(self.archivo_path)

    def obtener_info(self) -> Dict[str, Any]:
        """
        Obtiene informacion sobre el archivo del repositorio.
        """
        try:
            if self.existe_repositorio():
                return {
                    "tipo": "archivo",
                    "existe": True,
                    "ruta": self.archivo_path
                }

            return {
                "tipo": "archivo",
                "existe": False,
                "ruta": self.archivo_path,
                "mensaje": "El archivo no existe"
            }
        except Exception as e:
            return {
                "tipo": "archivo",
                "existe": False,
                "error": str(e)
            }

    def _asegurar_archivo_existe(self):
        """
        Asegura que el archivo de persistencia exista.
        """
        if not self.existe_repositorio():
            datos_iniciales = {
                "libros": [],
                "prestamos": [],
                "contadores": {
                    "libro": 1,
                    "prestamo": 1
                }
            }

            self._escribir_archivo(datos_iniciales)

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

    def _escribir_archivo(self, datos: Dict[str, Any]) -> bool:
        """
        Escribe datos en el archivo JSON.
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
        Lee datos desde el archivo JSON.
        """
        try:
            with open(self.archivo_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return None
        except json.JSONDecodeError as e:
            print(f"Error al decodificar JSON: {e}")
            return None
        except Exception as e:
            print(f"Error al leer archivo: {e}")
            return None
