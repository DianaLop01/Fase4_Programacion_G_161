
"""
Servicio especializado para la reserva de salas.
"""

# ===========================================================================================
#                       LIBRERIAS
# ===========================================================================================

# Se importa la clase abstracta Servicio.
from .servicio import Servicio

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

        self.tarifa_hora = tarifa_hora
        self.horas = horas
        self.capacidad = capacidad
        self.Validar_Parametros()

    # Valida las horas de uso y la capacidad requerida para la sala.
    def Validar_Parametros(self):
        self._validar_numero_positivo(self.horas, "Las horas de reserva")
        self._validar_entero_positivo(self.capacidad, "La capacidad")

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
