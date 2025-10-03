"""
SERVICIO NOTIFICACIONES
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
from datetime import datetime
from enum import Enum

class TipoNotificacion(Enum):
    """Enumeracion de tipos de notificaciones disponibles."""
    PRESTAMO_REALIZADO = "prestamo_realizado"
    LIBRO_DEVUELTO = "libro_devuelto"
    LIBRO_AGREGADO = "libro_agregado"
    RECORDATORIO_DEVOLUCION = "recordatorio_devolucion"
    LIBRO_DISPONIBLE = "libro_disponible"
    ERROR_SISTEMA = "error_sistema"


class CanalNotificacion(ABC):
    """
    Interfaz abstracta para diferentes canales de notificacion.
    Permite implementar diferentes tipos de notificaciones (consola, email, SMS, etc.)
    """

    @abstractmethod
    def enviar(self, mensaje: str, tipo: TipoNotificacion, datos: Dict[str, Any] = None) -> bool:
        """
        Envia una notificacion a traves del canal especifico.

        Args:
            mensaje: Mensaje a enviar
            tipo: Tipo de notificacion
            datos: Datos adicionales para la notificacion

        Returns:
            bool: True si se envio exitosamente, False en caso contrario
        """
        pass

class NotificacionConsola(CanalNotificacion):
    """
    Implementacion de notificaciones por consola.
    Muestra mensajes formateados en la consola del sistema.
    """

    def enviar(self, mensaje: str, tipo: TipoNotificacion, datos: Dict[str, Any] = None) -> bool:
        """
        Envia notificacion por consola con formato especifico.
        """
        try:
            timestamp = datetime.now().strftime("%H:%M:%S")

            mensaje_formateado = f"[{timestamp}] {mensaje}"

            if datos:
                detalles = []

                for clave, valor in datos.items():
                    detalles.append(f"{clave}: {valor}")

                if detalles:
                    mensaje_formateado += f" | {' | '.join(detalles)}"

            print(mensaje_formateado)
            return True

        except Exception as e:
            print(f"Error al enviar notificacion por consola: {e}")
            return False

class NotificacionArchivo(CanalNotificacion):
    """
    Implementacion de notificaciones por archivo de log.
    """
    def __init__(self, archivo_log: str = "notificaciones.log"):
        """
        Inicializa el canal de notificaciones por archivo.
        """
        self.archivo_log = archivo_log

    def enviar(self, mensaje: str, tipo: TipoNotificacion, datos: Dict[str, Any] = None) -> bool:
        """
        Guarda la notificacion en un archivo de log.
        """
        try:
            timestamp = datetime.now().isoformat()

            linea_log = f"{timestamp} | {tipo.value.upper()} | {mensaje}"
            if datos:
                linea_log += f" | Datos: {datos}"

            linea_log += "\n"

            with open(self.archivo_log, 'a', encoding='utf-8') as f:
                f.write(linea_log)

            return True

        except Exception as e:
            print(f"Error al escribir notificacion en archivo: {e}")
            return False

class ServicioNotificaciones:
    """
    Clase responsable de gestionar notificaciones del sistema.
    """
    def __init__(self):
        """
        Inicializa el servicio con canales de notificacion por defecto.
        """
        self.canales: List[CanalNotificacion] = [
            NotificacionConsola(),
            NotificacionArchivo()
        ]
        self.activo = True

    def agregar_canal(self, canal: CanalNotificacion) -> None:
        """
        Agrega un nuevo canal de notificacion al servicio.
        """
        if canal not in self.canales:
            self.canales.append(canal)

    def remover_canal(self, tipo_canal: type) -> bool:
        """
        Remueve un canal de notificacion especifico.
        """
        for i, canal in enumerate(self.canales):
            if isinstance(canal, tipo_canal):
                del self.canales[i]
                return True
        return False

    def activar(self) -> None:
        """Activa el servicio de notificaciones."""
        self.activo = True

    def desactivar(self) -> None:
        """Desactiva el servicio de notificaciones."""
        self.activo = False

    def notificar_prestamo_realizado(self, usuario: str, titulo_libro: str, fecha: str) -> bool:
        """
        Envia notificacion cuando se realiza un prestamo.
        """
        mensaje = f"Prestamo realizado a {usuario}"
        datos = {
            "usuario": usuario,
            "libro": titulo_libro,
            "fecha": fecha,
            "accion": "prestamo"
        }

        return self._enviar_notificacion(mensaje, TipoNotificacion.PRESTAMO_REALIZADO, datos)

    def notificar_libro_devuelto(self, usuario: str, titulo_libro: str) -> bool:
        """
        Envia notificacion cuando se devuelve un libro.
        """
        mensaje = f"Libro '{titulo_libro}' devuelto por {usuario}"
        datos = {
            "usuario": usuario,
            "libro": titulo_libro,
            "accion": "devolucion"
        }

        return self._enviar_notificacion(mensaje, TipoNotificacion.LIBRO_DEVUELTO, datos)

    def notificar_libro_agregado(self, titulo: str, autor: str) -> bool:
        """
        Envia notificacion cuando se agrega un nuevo libro.
        """
        mensaje = f"Nuevo libro agregado: '{titulo}' por {autor}"
        datos = {
            "titulo": titulo,
            "autor": autor,
            "accion": "agregar_libro"
        }

        return self._enviar_notificacion(mensaje, TipoNotificacion.LIBRO_AGREGADO, datos)

    def notificar_error(self, tipo_error: str, detalles: str) -> bool:
        """
        Envia notificacion de error del sistema.
        """
        mensaje = f"Error en el sistema: {tipo_error}"
        datos = {
            "tipo_error": tipo_error,
            "detalles": detalles,
            "accion": "error"
        }

        return self._enviar_notificacion(mensaje, TipoNotificacion.ERROR_SISTEMA, datos)

    def notificar_libro_disponible(self, titulo: str) -> bool:
        """
        Envia notificacion cuando un libro vuelve a estar disponible.
        """
        mensaje = f"Libro disponible: '{titulo}'"
        datos = {
            "libro": titulo,
            "accion": "disponible"
        }

        return self._enviar_notificacion(mensaje, TipoNotificacion.LIBRO_DISPONIBLE, datos)

    def _enviar_notificacion(self, mensaje: str, tipo: TipoNotificacion, 
                           datos: Dict[str, Any] = None) -> bool:
        """
        Metodo interno para enviar notificaciones a traves de todos los canales.
        """
        if not self.activo:
            return False

        exitos = 0
        for canal in self.canales:
            try:
                if canal.enviar(mensaje, tipo, datos):
                    exitos += 1
            except Exception as e:
                print(f"Error en canal de notificacion: {e}")

        return exitos > 0
