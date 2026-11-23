
"""
Clase abstracta base para los servicios ofrecidos por Software FJ.
"""

# ===========================================================================================
#                       LIBRERIAS
# ===========================================================================================

# Se importan las herramientas para crear clases abstractas.
from abc import ABC, abstractmethod
from math import isfinite

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

        if not all(
            isinstance(valor, str) and valor.strip()
            for valor in (codigo, nombre, descripcion)
        ):
            raise DatosServicioInvalidos(
                "El código, nombre y descripción deben ser textos obligatorios."
            )

        if not self._es_numero_finito(precio_base):
            raise DatosServicioInvalidos(
                "El precio base debe ser un valor numérico finito."
            )
        if precio_base <= 0:
            raise CostoServicioInvalido()

        self.codigo = codigo.strip()
        self.nombre = nombre.strip()
        self.descripcion = descripcion.strip()
        self.precio_base = precio_base

    # Comprueba que un valor sea numérico, finito y distinto de un booleano.
    @staticmethod
    def _es_numero_finito(valor):
        if not isinstance(valor, (int, float)) or isinstance(valor, bool):
            return False
        try:
            return isfinite(valor)
        except OverflowError:
            return False

    # Valida los valores positivos que pueden expresarse con decimales.
    @classmethod
    def _validar_numero_positivo(cls, valor, campo):
        if not cls._es_numero_finito(valor) or valor <= 0:
            raise DatosServicioInvalidos(
                f"{campo} debe ser un número finito mayor que cero."
            )

    # Valida los valores que deben ser números enteros positivos.
    @classmethod
    def _validar_entero_positivo(cls, valor, campo):
        if (
            not isinstance(valor, int)
            or isinstance(valor, bool)
            or not cls._es_numero_finito(valor)
            or valor <= 0
        ):
            raise DatosServicioInvalidos(
                f"{campo} debe ser un número entero mayor que cero."
            )

    # ---------------------------------------------------------------------------------------
    #       METODO ABSTRACTO PARA CALCULAR EL COSTO
    # ---------------------------------------------------------------------------------------

    # Cada servicio especializado implementara su propio calculo.

    @abstractmethod
    def Calcular_Costo(self):
        pass

    # Cada servicio especializado valida sus parámetros particulares.
    @abstractmethod
    def Validar_Parametros(self):
        """Valida los parámetros específicos del servicio."""

    # Calcula el costo de una reserva aplicando duración y descuento porcentual.

    def calcular_costo(self, duracion, descuento=0.0):

        if not isinstance(duracion, int) or isinstance(duracion, bool) or duracion <= 0:
            raise DatosServicioInvalidos(
                "La duración de la reserva debe ser un entero positivo."
            )

        if (
            not self._es_numero_finito(descuento)
            or not 0 <= descuento < 100
        ):
            raise DatosServicioInvalidos(
                "El descuento debe ser un porcentaje entre 0 y menos de 100."
            )

        costo_base = self.Calcular_Costo()
        return costo_base * duracion * (1 - descuento / 100)

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
