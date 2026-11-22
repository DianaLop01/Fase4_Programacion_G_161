
"""
Servicio especializado para la reserva de salas.
"""

# ===========================================================================================
#                       LIBRERIAS
# ===========================================================================================

# Se importa la clase abstracta Servicio.
from .servicio import Servicio

# Se importan las excepciones.
from .excepciones import DatosServicioInvalidos


# ===========================================================================================
#                       CLASE RESERVA DE SALAS
# ===========================================================================================

class ReservaSalas(Servicio):

    # ---------------------------------------------------------------------------------------
    #       METODO CONSTRUCTOR
    # ---------------------------------------------------------------------------------------

    def __init__(self, codigo, nombre, descripcion,
                 tarifa_hora, horas, capacidad):

        # Se inicializan los atributos heredados.
        super().__init__(codigo, nombre, descripcion, tarifa_hora)

        # Se validan las horas y la capacidad.
        if horas <= 0 or capacidad <= 0:
            raise DatosServicioInvalidos(
                "Las horas y la capacidad deben ser mayores que cero."
            )

        self.tarifa_hora = tarifa_hora
        self.horas = horas
        self.capacidad = capacidad

    # ---------------------------------------------------------------------------------------
    #       METODO PARA CALCULAR EL COSTO
    # ---------------------------------------------------------------------------------------

    def Calcular_Costo(self):

        costo_total = self.tarifa_hora * self.horas

        return costo_total

    # ---------------------------------------------------------------------------------------
    #       METODO PARA MOSTRAR LA INFORMACION
    # ---------------------------------------------------------------------------------------

    def Mostrar_Informacion(self):

        informacion = super().Mostrar_Informacion()

        informacion += (
            f"\nTarifa por hora: ${self.tarifa_hora:,.2f}"
            f"\nHoras reservadas: {self.horas}"
            f"\nCapacidad de la sala: {self.capacidad} personas"
        )

        return informacion
