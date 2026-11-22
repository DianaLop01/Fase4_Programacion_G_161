
"""
Clase abstracta base para los servicios ofrecidos por Software FJ.
"""

# ===========================================================================================
#                       LIBRERIAS
# ===========================================================================================

# Se importan las herramientas para crear clases abstractas.
from abc import ABC, abstractmethod

# Se importan las excepciones del dominio de servicios.
from .excepciones import DatosServicioInvalidos, CostoServicioInvalido


# ===========================================================================================
#                       CLASE ABSTRACTA SERVICIO
# ===========================================================================================

class Servicio(ABC):

    # ---------------------------------------------------------------------------------------
    #       METODO CONSTRUCTOR
    # ---------------------------------------------------------------------------------------

    # Inicializa los atributos generales de todos los servicios.

    def __init__(self, codigo, nombre, descripcion, precio_base):

        if not codigo or not nombre or not descripcion:
            raise DatosServicioInvalidos(
                "El codigo, nombre y descripcion son obligatorios."
            )

        if precio_base <= 0:
            raise CostoServicioInvalido()

        self.codigo = codigo
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio_base = precio_base

    # ---------------------------------------------------------------------------------------
    #       METODO ABSTRACTO PARA CALCULAR EL COSTO
    # ---------------------------------------------------------------------------------------

    # Cada servicio especializado implementara su propio calculo.

    @abstractmethod
    def Calcular_Costo(self):
        pass

    # ---------------------------------------------------------------------------------------
    #       METODO PARA MOSTRAR LA INFORMACION
    # ---------------------------------------------------------------------------------------

    # Retorna los datos generales del servicio.

    def Mostrar_Informacion(self):

        informacion = (
            f"Codigo: {self.codigo}\n"
            f"Nombre: {self.nombre}\n"
            f"Descripcion: {self.descripcion}\n"
            f"Precio base: ${self.precio_base:,.2f}\n"
            f"Costo total: ${self.Calcular_Costo():,.2f}"
        )

        return informacion
