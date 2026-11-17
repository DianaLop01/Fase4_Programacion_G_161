"""Modelo y ciclo de vida de las reservas."""

import excepciones


class Reserva:
    """Gestiona el ciclo de vida de una reserva: pendiente, confirmada, cancelada."""

    def __init__(
        self,
        identificador: str,
        cliente,
        servicio,
        duracion: int,
        descuento: float = 0.0,
        logger=None,
    ):
        if not identificador or not identificador.strip():
            raise excepciones.ErrorParametrofaltante("El identificador de la reserva no puede estar vacío.")
        if cliente is None or servicio is None:
            raise excepciones.ErrorReservaIncorrecta("Debe asociar un cliente y un servicio válidos.")
        if not isinstance(duracion, int) or duracion <= 0:
            raise excepciones.ErrorReservaIncorrecta("La duración de la reserva debe ser un número entero positivo.")

        self._identificador = identificador.strip()
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.descuento = descuento
        self.estado = "pendiente"  # Estados posibles: pendiente, confirmada, cancelada
        self.logger = logger
        self.costo_total = self.calcular_costo_total()

    @property
    def identificador(self):
        return self._identificador

    @identificador.setter
    def identificador(self, valor):
        if not valor or not str(valor).strip():
            raise excepciones.ErrorParametrofaltante("El identificador de la reserva no puede estar vacío.")
        self._identificador = str(valor).strip()

    def _log(self, nivel: str, mensaje: str):
        if self.logger:
            self.logger.registar(nivel, mensaje)

    def calcular_costo_total(self):
        if self.servicio is None:
            return 0.0
        try:
            return self.servicio.calcular_costo(self.duracion, self.descuento)
        except excepciones.SoftwareFJExcepcion as e:
            raise excepciones.ErrorReservaIncorrecta(
                f"No se pudo calcular el costo de la reserva {self.identificador}: {e}"
            ) from e
        except Exception as e:
            raise excepciones.ErrorReservaIncorrecta(
                f"Error inesperado al calcular el costo de la reserva {self.identificador}: {e}"
            ) from e

    def procesar(self):
        """Calcula el costo aplicando polimorfismo y control avanzado de excepciones."""
        try:
            self._log("INFO", f"iniciando procesamiento de la reserva {self.identificador}.")
            if self.estado == "cancelada":
                raise excepciones.ErrorOperacionNoPermitida("No se puede procesar una reserva cancelada.")

            self.costo_total = self.servicio.calcular_costo(self.duracion, self.descuento)
            self.estado = "procesada"

        except excepciones.SoftwareFJExcepcion as e:
            self.estado = "fallida"
            self._log("ERROR", f"fallo controlado en reserva {self.identificador}: {e}")
            raise excepciones.ErrorReservaIncorrecta(
                f"no se pudo procesar la reserva {self.identificador}: {e}"
            ) from e
        except Exception as e:
            self.estado = "fallida"
            self._log("ERROR_CRITICO", f"Error inesperado en reserva {self.identificador}: {e}")
            raise excepciones.ErrorReservaIncorrecta(
                f"Error inesperado al procesar la reserva {self.identificador}: {e}"
            ) from e
        else:
            self._log(
                "EXITO",
                f"reserva {self.identificador} procesada exitosamente. Costo total: {self.costo_total:.2f}",
            )
        finally:
            self._log(
                "AUDITORIA",
                f"Cierre de transaccion para la reserva {self.identificador} (estado: {self.estado}).",
            )

    def confirmar(self):
        if self.estado != "procesada":
            raise excepciones.ErrorOperacionNoPermitida(
                f"Solo se pueden confirmar reservas procesadas (estado actual: {self.estado})."
            )
        self.estado = "confirmada"
        self._log("INFO", f"reserva {self.identificador} confirmada.")

    def cancelar(self):
        if self.estado == "cancelada":
            raise excepciones.ErrorOperacionNoPermitida("La reserva ya está cancelada.")
        self.estado = "cancelada"
        self._log("INFO", f"reserva {self.identificador} cancelada.")

    def obtener_detalles(self):
        return {
            "identificador": self.identificador,
            "cliente": self.cliente.nombre if self.cliente else None,
            "servicio": self.servicio.nombre if self.servicio else None,
            "duracion": self.duracion,
            "descuento": self.descuento,
            "estado": self.estado,
            "costo_total": self.costo_total,
        }