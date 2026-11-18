"""Excepciones específicas del dominio de reservas.

Contiene excepciones personalizadas para manejar errores relacionados con reservas de servicios.
"""


class SoftwareFJExcepcion(Exception):
    """Excepción base personalizada para todo el sistema softwarefj."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje)


class ErrorReservaIncorrecta(SoftwareFJExcepcion):
    pass
    """Se lanza cuando la reserva presenta inconsistencias al crearse o procesarse."""


class ErrorParametroFaltante(SoftwareFJExcepcion):
    pass
    """Se lanza cuando faltan parámetros obligatorios en una operación."""


class ErrorOperacionNoPermitida(SoftwareFJExcepcion):
    pass 
    """Se lanza al intentar ejecutar una acción inválida según el estado actual."""


class ErrorServicioNoDisponible(SoftwareFJExcepcion):
    pass 
    """Se lanza si se intenta reservar un servicio inactivo."""


class ErrorCalculoInconsistente(SoftwareFJExcepcion):
    pass 
    """Se lanza si el resultado de un cálculo financiero es negativo o erróneo."""

class ErrorDatoInvalido(SoftwareFJExcepcion):
    pass
    