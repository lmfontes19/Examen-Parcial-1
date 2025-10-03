"""
ESTRATEGIAS DE BUSQUEDA
"""

from abc import ABC, abstractmethod
from typing import List


class Libro: ...

class Buscador(ABC):
    """
    Clase abstracta que define la interfaz para todas las estrategias de busqueda.
    """
    @abstractmethod
    def buscar(self, libros: List[Libro], valor: str) -> List[Libro]:
        """
        Metodo abstracto que debe implementar cada estrategia de busqueda.

        Args:
            libros: Lista de libros donde buscar
            valor: Valor a buscar segun el criterio de la estrategia

        Returns:
            Lista de libros que coinciden con el criterio
        """
        pass

class BusquedaPorTitulo(Buscador):
    """
    Estrategia de busqueda por titulo del libro.
    Realiza busqueda parcial case-insensitive.
    """
    def buscar(self, libros: List[Libro], valor: str) -> List[Libro]:
        """
        Busca libros que contengan el valor en el nombre del titulo.
        """
        return [
            libro for libro in libros 
            if valor.lower() in libro.titulo.lower()
        ]

class BusquedaPorAutor(Buscador):
    """
    Estrategia de busqueda por autor del libro.
    Realiza busqueda parcial case-insensitive.
    """
    def buscar(self, libros: List[Libro], valor: str) -> List[Libro]:
        """
        Busca libros que contengan el valor en el nombre del autor.
        """
        return [
            libro for libro in libros 
            if valor.lower() in libro.autor.lower()
        ]

class BusquedaPorISBN(Buscador):
    """
    Estrategia de busqueda por ISBN del libro.
    Realiza busqueda exacta.
    """
    def buscar(self, libros: List[Libro], valor: str) -> List[Libro]:
        """
        Busca libros con el ISBN exacto.
        """
        return [
            libro for libro in libros
            if libro.isbn == valor
        ]

class BusquedaPorDisponibilidad(Buscador):
    """
    Estrategia de busqueda por disponibilidad del libro.
    """
    def buscar(self, libros: List[Libro], valor: str) -> List[Libro]:
        """
        Busca libros segun su disponibilidad.
        """
        disponible = valor.lower() == "true"
        return [
            libro for libro in libros
            if libro.disponible == disponible
        ]

class Busqueda:
    """
    Esta clase permite cambiar el algoritmo de busqueda dinamicamente
    sin modificar el codigo cliente.
    """
    def __init__(self):
        """
        Inicializa el contexto con un diccionario de estrategias disponibles.
        """
        self._estrategias = {
            "titulo": BusquedaPorTitulo(),
            "autor": BusquedaPorAutor(),
            "isbn": BusquedaPorISBN(),
            "disponible": BusquedaPorDisponibilidad()
        }

    def agregar_estrategia(self, nombre: str, estrategia: Buscador):
        """
        Permite agregar nuevas estrategias dinamicamente.

        Args:
            nombre: Nombre del criterio de busqueda
            estrategia: Instancia de la estrategia de busqueda
        """
        self._estrategias[nombre] = estrategia

    def buscar(self, criterio: str, libros: List[Libro], valor: str) -> List[Libro]:
        """
        Ejecuta la busqueda usando la estrategia correspondiente al criterio.

        Args:
            criterio: Tipo de busqueda ("titulo", "autor", "isbn", "disponible")
            libros: Lista de libros donde buscar
            valor: Valor a buscar

        Returns:
            Lista de libros que coinciden con el criterio
        """
        if criterio not in self._estrategias:
            raise ValueError(f"Criterio de busqueda '{criterio}' no soportado. "
                           f"Criterios disponibles: {list(self._estrategias.keys())}")

        estrategia = self._estrategias[criterio]
        return estrategia.buscar(libros, valor)

    def obtener_criterios_disponibles(self) -> List[str]:
        """
        Retorna la lista de criterios de busqueda disponibles.

        Returns:
            Lista de nombres de criterios disponibles
        """
        return list(self._estrategias.keys())
