"""Clase abstracta base para las entidades de Software FJ."""

# ===========================================================================================
#                       LIBRERÍAS
# ===========================================================================================

# Se importan las herramientas para definir una clase abstracta y sus métodos.
from abc import ABC, abstractmethod


# ===========================================================================================
#                       CLASE ABSTRACTA ENTIDAD
# ===========================================================================================

# Clase base para las entidades que comparten un identificador y una descripción.
class Entidad(ABC):
    """Define el identificador y la descripción común de una entidad."""

# Se valida y almacena el identificador común de la entidad.
    def __init__(self, identificador: str):
        if not isinstance(identificador, str) or not identificador.strip():
            raise ValueError("El identificador no puede estar vacío.")
        self._identificador = identificador.strip()

# Se expone el identificador sin permitir su modificación mediante la propiedad.
    @property
    def identificador(self) -> str:
        return self._identificador

# Se obliga a las clases derivadas a definir su propia descripción.
    @abstractmethod
    def describir(self) -> str:
        """Devuelve una descripción legible de la entidad."""
