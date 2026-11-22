"""Excepciones del dominio de clientes."""

# ===========================================================================================
#                       LIBRERÍAS
# ===========================================================================================

# Se importa la excepción base compartida por los módulos del sistema.
from comun.excepciones_base import ErrorSistema


# ===========================================================================================
#                       EXCEPCIONES DEL DOMINIO DE CLIENTES
# ===========================================================================================

# Excepción base para identificar y manejar errores relacionados con clientes.
class ErrorCliente(ErrorSistema):
    """Error base para operaciones relacionadas con clientes."""


# Se lanza cuando uno o más datos ingresados para un cliente son inválidos.
class ErrorDatoClienteInvalido(ErrorCliente):
    """Se lanza cuando uno o más datos del cliente no son válidos."""


# Se lanza cuando ya existe un cliente con el mismo tipo y número de documento.
class ErrorClienteDuplicado(ErrorCliente):
    """Se lanza cuando ya existe un cliente con el mismo tipo y documento."""


# -------------------------------------------------------------------------------------------
#       EXCEPCIONES PARA LA BÚSQUEDA DE CLIENTES
# -------------------------------------------------------------------------------------------

# Excepción base para los errores que ocurren durante una búsqueda de clientes.
class ErrorBusquedaCliente(ErrorCliente):
    """Error general al buscar un cliente por sus datos de identificación."""


# Se lanza cuando el tipo o el número de documento de búsqueda no son válidos.
class ErrorIdentificacionClienteInvalida(ErrorBusquedaCliente):
    """Se lanza cuando los datos de identificación no permiten realizar la búsqueda."""


# Se lanza cuando la búsqueda es válida, pero no hay coincidencias en la lista.
class ErrorClienteNoEncontrado(ErrorBusquedaCliente):
    """Se lanza cuando no existe un cliente con la identificación solicitada."""


# Se lanza cuando el cliente tiene reservas que deben conservar su referencia.
class ErrorClienteConReservas(ErrorCliente):
    """Se lanza cuando no se permite eliminar un cliente con reservas asociadas."""
