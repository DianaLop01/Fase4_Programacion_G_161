
"""
Servicio especializado para asesorías.
"""

# ===========================================================================================
#                       LIBRERIAS
# ===========================================================================================

# Se importa la clase abstracta Servicio.
from .servicio import Servicio

# Se importa la excepción para los parámetros inválidos de la asesoría.
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

        self.tarifa_hora = tarifa_hora
        self.horas = horas
        self.modalidad = modalidad
        self.Validar_Parametros()

    # Valida las horas contratadas y la modalidad de la asesoría.
    def Validar_Parametros(self):
        self._validar_numero_positivo(self.horas, "Las horas de asesoría")
        if not isinstance(self.modalidad, str) or self.modalidad not in (
            "Virtual",
            "Presencial",
        ):
            raise DatosServicioInvalidos(
                "La modalidad debe ser Virtual o Presencial."
            )

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
