"""
EXAMEN PRINCIPIOS SOLID - 2 HORAS
Sistema de Mini-Biblioteca

CODIGO REFACTORIZADO CUMPLIENDO SOLID
- Separacion de responsabilidades en clases especificas (SRP)
- Inyeccion de dependencias para mejorar testabilidad (DIP)
- Cada clase tiene UNA sola responsabilidad
- Dependencias de abstracciones, no de implementaciones concretas
"""

from dataclasses import dataclass
from busqueda import Busqueda
from validador_biblioteca import ValidadorBiblioteca
from irepositorio import IRepositorio
from servicio_notificaciones import ServicioNotificaciones
from repositorio_archivo import RepositorioArchivo
from repositorio_memoria import RepositorioMemoria

@dataclass
class Libro:
    id: int
    titulo: str
    autor: str
    isbn: str
    disponible: bool = True

@dataclass
class Prestamo:
    id: int
    libro_id: int
    usuario: str
    fecha: str
    devuelto: bool = False

class SistemaBiblioteca:
    """
    Clase principal del sistema que coordina las operaciones de biblioteca.
    
    CUMPLE DIP:
    - Depende de IRepositorio (abstraccion), no de implementacion concreta
    - Permite intercambiar repositorios sin cambiar codigo
    - Facilita testing con mocks
    """
    def __init__(self,
                 busqueda: Busqueda,
                 validador: ValidadorBiblioteca,
                 repositorio: IRepositorio,
                 notificaciones: ServicioNotificaciones):
        """
        Inicializa el sistema con todas sus dependencias.
        
        Todas las dependencias son obligatorias para cumplir con DIP.
        No hay creacion de objetos concretos dentro de la clase.
        """
        self.libros = []
        self.prestamos = []
        self.contador_libro = 1
        self.contador_prestamo = 1

        self.busqueda = busqueda
        self.validador = validador
        self.repositorio = repositorio
        self.notificaciones = notificaciones

        self._cargar_datos_iniciales()

    def _cargar_datos_iniciales(self):
        """
        Carga datos existentes desde el repositorio al inicializar el sistema.
        """
        datos = self.repositorio.cargar_datos()
        if datos:
            for libro_data in datos.get('libros', []):
                libro = Libro(
                    libro_data['id'],
                    libro_data['titulo'],
                    libro_data['autor'],
                    libro_data['isbn'],
                    libro_data['disponible']
                )
                self.libros.append(libro)

            for prestamo_data in datos.get('prestamos', []):
                prestamo = Prestamo(
                    prestamo_data['id'],
                    prestamo_data['libro_id'],
                    prestamo_data['usuario'],
                    prestamo_data['fecha'],
                    prestamo_data['devuelto'],
                )
                self.prestamos.append(prestamo)

            contadores = datos.get('contadores', {})
            self.contador_libro = contadores.get('libro', 1)
            self.contador_prestamo = contadores.get('prestamo', 1)

    def agregar_libro(self, titulo, autor, isbn):
        """
        Agrega un nuevo libro al sistema.
        """
        es_valido, mensaje_validacion = self.validador.validar_libro(titulo, autor, isbn)
        if not es_valido:
            return mensaje_validacion

        libro = Libro(self.contador_libro, titulo, autor, isbn)
        self.libros.append(libro)
        self.contador_libro += 1

        self._guardar_datos()

        self.notificaciones.notificar_libro_agregado(titulo, autor)

        return f"Libro '{titulo}' agregado exitosamente"

    def buscar_libro(self, criterio, valor):
        """
        Busca libros usando el metodo de busqueda.
        """
        try:
            return self.busqueda.buscar(criterio, self.libros, valor)
        except ValueError as e:
            print(f"Error de búsqueda: {e}")
            return []

    def realizar_prestamo(self, libro_id, usuario):
        """
        Realiza un prestamo de libro a un usuario.
        """
        es_valido_usuario, mensaje_usuario = self.validador.validar_usuario(usuario)
        if not es_valido_usuario:
            return mensaje_usuario

        es_valido_id, mensaje_id = self.validador.validar_id(libro_id, "libro")
        if not es_valido_id:
            return mensaje_id

        libro = self._buscar_libro_por_id(libro_id)
        if not libro:
            return "Error: Libro no encontrado"

        if not libro.disponible:
            return "Error: Libro no disponible"

        from datetime import datetime
        prestamo = Prestamo(
            self.contador_prestamo,
            libro_id,
            usuario,
            False,
            datetime.now().strftime("%Y-%m-%d")
        )

        self.prestamos.append(prestamo)
        self.contador_prestamo += 1
        libro.disponible = False

        self._guardar_datos()

        self.notificaciones.notificar_prestamo_realizado(usuario, libro.titulo, prestamo.fecha)

        return f"Prestamo realizado a {usuario}"

    def _buscar_libro_por_id(self, libro_id: int):
        """
        Metodo auxiliar para buscar un libro por su ID.
        """
        for libro in self.libros:
            if libro.id == libro_id:
                return libro
        return None

    def _buscar_prestamo_por_id(self, prestamo_id: int):
        """
        Metodo auxiliar para buscar un prestamo por su ID.
        """
        for prestamo in self.prestamos:
            if prestamo.id == prestamo_id:
                return prestamo
        return None

    def _guardar_datos(self):
        """
        Metodo auxiliar para guardar datos usando el repositorio.
        """
        exito = self.repositorio.guardar_datos(
            self.libros,
            self.prestamos,
            self.contador_libro,
            self.contador_prestamo
        )
        if not exito:
            self.notificaciones.notificar_error("Persistencia", "Error al guardar datos")

    def devolver_libro(self, prestamo_id):
        """
        Procesa la devolucion de un libro.
        """
        es_valido_id, mensaje_id = self.validador.validar_id(prestamo_id, "prestamo")
        if not es_valido_id:
            return mensaje_id

        prestamo = self._buscar_prestamo_por_id(prestamo_id)
        if not prestamo:
            return "Error: Prestamo no encontrado"

        if prestamo.devuelto:
            return "Error: Libro ya devuelto"

        libro = self._buscar_libro_por_id(prestamo.libro_id)
        if libro:
            libro.disponible = True

        prestamo.devuelto = True

        self._guardar_datos()

        if libro:
            self.notificaciones.notificar_libro_devuelto(prestamo.usuario, libro.titulo)
            self.notificaciones.notificar_libro_disponible(libro.titulo)

        return "Libro devuelto exitosamente"

    def obtener_todos_libros(self):
        """Retorna todos los libros del sistema."""
        return self.libros

    def obtener_libros_disponibles(self):
        """Retorna solo los libros disponibles."""
        return [libro for libro in self.libros if libro.disponible]

    def obtener_prestamos_activos(self):
        """Retorna solo los prestamos activos (no devueltos)."""
        return [p for p in self.prestamos if not p.devuelto]

def main(tipo_repositorio: IRepositorio):
    """
    Funcion principal que demuestra el uso del sistema refactorizado.
    Ahora con inyeccion completa de dependencias cumpliendo DIP.
    """
    busqueda = Busqueda()
    validador = ValidadorBiblioteca()
    notificaciones = ServicioNotificaciones()
    repositorio = tipo_repositorio

    sistema = SistemaBiblioteca(
        busqueda=busqueda,
        validador=validador,
        repositorio=repositorio,
        notificaciones=notificaciones
    )

    print("\n=== AGREGANDO LIBROS ===")
    print(sistema.agregar_libro("Cien Años de Soledad", "Gabriel Garcia Marquez", "9780060883287"))
    print(sistema.agregar_libro("El Principito", "Antoine de Saint-Exupery", "9780156012195"))
    print(sistema.agregar_libro("1984", "George Orwell", "9780451524935"))

    print("\n=== BUSQUEDA POR AUTOR ===")
    resultados = sistema.buscar_libro("autor", "Garcia")
    for libro in resultados:
        print(f"- {libro.titulo} por {libro.autor}")

    print("\n=== REALIZAR PRESTAMO ===")
    print(sistema.realizar_prestamo(1, "Juan Perez"))

    print("\n=== LIBROS DISPONIBLES ===")
    disponibles = sistema.obtener_libros_disponibles()
    for libro in disponibles:
        print(f"- {libro.titulo}")

    print("\n=== DEVOLVER LIBRO ===")
    print(sistema.devolver_libro(1))

if __name__ == "__main__":
    # Ejemplo con repositorio archivo
    main(tipo_repositorio=RepositorioArchivo("biblioteca_refactorizada.json"))

    # Ejemplo con repositorio memoria
    print("\n" + "="*60)
    main(tipo_repositorio=RepositorioMemoria())
