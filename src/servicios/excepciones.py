
"""
Excepciones especificas del dominio de servicios.
"""


# ===========================================================================================
#                       EXCEPCIONES DE SERVICIOS
# ===========================================================================================

# Excepcion general para los errores relacionados con los servicios.
class ErrorServicio(Exception):

    def __init__(self, mensaje):
        super().__init__(mensaje)


# Excepcion para datos incorrectos o incompletos.
class DatosServicioInvalidos(ErrorServicio):

    def __init__(self, mensaje="Los datos del servicio no son validos."):
        super().__init__(mensaje)


# Excepcion para valores monetarios negativos o iguales a cero.
class CostoServicioInvalido(ErrorServicio):

    def __init__(self, mensaje="El costo del servicio debe ser mayor que cero."):
        super().__init__(mensaje)


# Excepcion cuando se intenta registrar un servicio sin informacion.
class ServicioIncompleto(ErrorServicio):

    def __init__(self, mensaje="Debe completar todos los datos del servicio."):
        super().__init__(mensaje)
