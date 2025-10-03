"""
VALIDADOR BIBLIOTECA
"""

from typing import Tuple

class ValidadorBiblioteca:
    """
    Clase responsable de validar datos del sistema de biblioteca.
    """
    @staticmethod
    def validar_libro(titulo: str, autor: str, isbn: str) -> Tuple[bool, str]:
        """
        Valida los datos de un libro antes de agregarlo al sistema.
        """
        if not titulo or not isinstance(titulo, str):
            return False, "Error: Titulo invalido - debe ser una cadena no vacia"

        if len(titulo.strip()) < 2:
            return False, "Error: Titulo invalido - debe tener al menos 2 caracteres"

        if not autor or not isinstance(autor, str):
            return False, "Error: Autor invalido - debe ser una cadena no vacia"

        if len(autor.strip()) < 3:
            return False, "Error: Autor invalido - debe tener al menos 3 caracteres"

        if not isbn or not isinstance(isbn, str):
            return False, "Error: ISBN invalido - debe ser una cadena no vacia"

        if len(isbn.strip()) < 10:
            return False, "Error: ISBN invalido - debe tener al menos 10 caracteres"

        isbn_limpio = isbn.replace('-', '').replace(' ', '')
        if not isbn_limpio.isalnum():
            return False, "Error: ISBN invalido - solo debe contener numeros, letras y guiones"

        return True, "Datos del libro validos"

    @staticmethod
    def validar_usuario(usuario: str) -> Tuple[bool, str]:
        """
        Valida los datos de un usuario para préstamos.
        """
        if not usuario or not isinstance(usuario, str):
            return False, "Error: Nombre de usuario invalido - debe ser una cadena no vacia"

        if len(usuario.strip()) < 3:
            return False, "Error: Nombre de usuario invalido - debe tener al menos 3 caracteres"

        if not usuario.strip():
            return False, "Error: Nombre de usuario invalido - no puede ser solo espacios"

        return True, "Nombre de usuario valido"

    @staticmethod
    def validar_id(id_objeto: int, tipo_objeto: str) -> Tuple[bool, str]:
        """
        Valida que un ID sea valido para el tipo de objeto especificado.

        Args:
            id_objeto: ID a validar
            tipo_objeto: Tipo de objeto ("libro", "prestamo", etc.)

        Returns:
            Tuple[bool, str]: (es_valido, mensaje)
            - es_valido: True si el ID es valido, False en caso contrario
            - mensaje: Mensaje descriptivo del resultado de la validacion
        """
        if not isinstance(id_objeto, int):
            return False, f"Error: ID de {tipo_objeto} debe ser un numero entero"

        if id_objeto <= 0:
            return False, f"Error: ID de {tipo_objeto} debe ser mayor que 0"

        return True, f"ID de {tipo_objeto} valido"

    @staticmethod
    def validar_criterio_busqueda(criterio: str, valor: str) -> Tuple[bool, str]:
        """
        Valida que los parametros de busqueda sean validos.
        """
        if not criterio or not isinstance(criterio, str):
            return False, "Error: Criterio de busqueda debe ser una cadena no vacia"

        if not valor or not isinstance(valor, str):
            return False, "Error: Valor de busqueda debe ser una cadena no vacia"

        if len(criterio.strip()) == 0:
            return False, "Error: Criterio de busqueda no puede estar vacio"

        if len(valor.strip()) == 0:
            return False, "Error: Valor de busqueda no puede estar vacio"

        return True, "Parametros de busqueda validos"
