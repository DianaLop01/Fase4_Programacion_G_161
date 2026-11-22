
"""
Servicio especializado para asesorías.
"""

# ===========================================================================================
#                       LIBRERIAS
# ===========================================================================================

# Se importa la clase abstracta Servicio.
from .servicio import Servicio

# Se importan las excepciones.
from .excepciones import DatosServicioInvalidos


# ===========================================================================================
#                       CLASE ASESORIA
# ===========================================================================================

class Asesoria(Servicio):

    # ---------------------------------------------------------------------------------------
    #       METODO CONSTRUCTOR
    # ---------------------------------------------------------------------------------------

    def __init__(self, codigo, nombre, descripcion,
                 tarifa_hora, horas, modalidad):

        # Se inicializan los atributos heredados.
        super().__init__(codigo, nombre, descripcion, tarifa_hora)

        # Se validan las horas contratadas.
        if horas <= 0:
            raise DatosServicioInvalidos(
                "Las horas de asesoria deben ser mayores que cero."
            )

        if modalidad not in ("Virtual", "Presencial"):
            raise DatosServicioInvalidos(
                "La modalidad debe ser Virtual o Presencial."
            )

        self.tarifa_hora = tarifa_hora
        self.horas = horas
        self.modalidad = modalidad

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
            f"\nHoras contratadas: {self.horas}"
            f"\nModalidad: {self.modalidad}"
        )

        return informacion
