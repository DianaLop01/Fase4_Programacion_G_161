"""Modelo del cliente y validación de sus datos personales."""

# ===========================================================================================
#                       LIBRERÍAS
# ===========================================================================================

# Se importa re para validar formatos de nombres, documentos, teléfonos y correos.
import re

# Se importan los tipos para validar fechas de nacimiento.
from datetime import date, datetime
from typing import Optional

# Se importan la entidad base y la excepción del dominio de clientes.
from comun.entidad import Entidad
from clientes.excepciones import (
    ErrorClienteConReservas,
    ErrorClienteNoEncontrado,
    ErrorDatoClienteInvalido,
    ErrorIdentificacionClienteInvalida,
)


# ===========================================================================================
#                       OPCIONES VÁLIDAS PARA LOS DATOS DEL CLIENTE
# ===========================================================================================

# Tipos de documento permitidos en el formulario de clientes.
TIPOS_DOCUMENTO = (
    "Cédula de ciudadanía",
    "Cédula de extranjería",
    "Pasaporte",
    "Tarjeta de identidad",
    "Otro",
)

# Opciones de género disponibles para registrar un cliente.
GENEROS = ("F", "M", "Otro")


# ===========================================================================================
#                       CLASE CLIENTE
# ===========================================================================================

# La clase hereda de Entidad y mantiene sus datos validados y encapsulados.
class Cliente(Entidad):
    """Representa un cliente con datos validados y de solo lectura."""

# Se reciben los datos personales, de identificación, contacto y residencia.
    def __init__(
        self,
        tipo_documento: str,
        documento: str,
        primer_nombre: str,
        primer_apellido: str,
        fecha_nacimiento: date,
        genero: str,
        telefono: str,
        correo_electronico: str,
        pais_residencia: str,
        departamento: str,
        ciudad_municipio: str,
        direccion: str,
        segundo_nombre: str = "",
        segundo_apellido: str = "",
    ):

# Se valida el tipo y el número de documento; el documento identifica al cliente.
        self._tipo_documento = self._validar_opcion(
            tipo_documento, TIPOS_DOCUMENTO, "tipo de documento"
        )
        self._documento = self._validar_documento(documento)
        super().__init__(self._documento)

# Se validan los nombres y apellidos; los segundos nombres y apellidos son opcionales.
        self._primer_nombre = self._validar_nombre(primer_nombre, "primer nombre")
        self._segundo_nombre = self._validar_nombre(
            segundo_nombre, "segundo nombre", obligatorio=False
        )
        self._primer_apellido = self._validar_nombre(
            primer_apellido, "primer apellido"
        )
        self._segundo_apellido = self._validar_nombre(
            segundo_apellido, "segundo apellido", obligatorio=False
        )

# Se validan la fecha de nacimiento y el género.
        self._fecha_nacimiento = self._validar_fecha(fecha_nacimiento)
        self._genero = self._validar_opcion(genero, GENEROS, "género")

# Se validan los datos de contacto y residencia.
        self._telefono = self._validar_telefono(telefono)
        self._correo_electronico = self._validar_correo(correo_electronico)
        self._pais_residencia = self._validar_texto(
            pais_residencia, "país de residencia"
        )
        self._departamento = self._validar_texto(departamento, "departamento")
        self._ciudad_municipio = self._validar_texto(
            ciudad_municipio, "ciudad o municipio"
        )
        self._direccion = self._validar_texto(direccion, "dirección")

# -------------------------------------------------------------------------------------------
#       MÉTODO PARA ACTUALIZAR LOS DATOS DEL CLIENTE
# -------------------------------------------------------------------------------------------

# Se actualizan los datos personales sin cambiar el tipo ni el número de documento.
# Los valores se validan primero para evitar dejar el objeto parcialmente modificado.
    def actualizar_datos(
        self,
        primer_nombre: str,
        primer_apellido: str,
        fecha_nacimiento: date,
        genero: str,
        telefono: str,
        correo_electronico: str,
        pais_residencia: str,
        departamento: str,
        ciudad_municipio: str,
        direccion: str,
        segundo_nombre: str = "",
        segundo_apellido: str = "",
    ) -> None:

# Se validan los nombres y apellidos antes de modificar el objeto.
        primer_nombre_validado = self._validar_nombre(
            primer_nombre, "primer nombre"
        )
        segundo_nombre_validado = self._validar_nombre(
            segundo_nombre, "segundo nombre", obligatorio=False
        )
        primer_apellido_validado = self._validar_nombre(
            primer_apellido, "primer apellido"
        )
        segundo_apellido_validado = self._validar_nombre(
            segundo_apellido, "segundo apellido", obligatorio=False
        )

# Se validan la fecha, el género, los datos de contacto y la residencia.
        fecha_nacimiento_validada = self._validar_fecha(fecha_nacimiento)
        genero_validado = self._validar_opcion(genero, GENEROS, "género")
        telefono_validado = self._validar_telefono(telefono)
        correo_validado = self._validar_correo(correo_electronico)
        pais_validado = self._validar_texto(pais_residencia, "país de residencia")
        departamento_validado = self._validar_texto(
            departamento, "departamento"
        )
        ciudad_validada = self._validar_texto(
            ciudad_municipio, "ciudad o municipio"
        )
        direccion_validada = self._validar_texto(direccion, "dirección")

# Se asignan los valores solo después de validar correctamente todos los campos.
        self._primer_nombre = primer_nombre_validado
        self._segundo_nombre = segundo_nombre_validado
        self._primer_apellido = primer_apellido_validado
        self._segundo_apellido = segundo_apellido_validado
        self._fecha_nacimiento = fecha_nacimiento_validada
        self._genero = genero_validado
        self._telefono = telefono_validado
        self._correo_electronico = correo_validado
        self._pais_residencia = pais_validado
        self._departamento = departamento_validado
        self._ciudad_municipio = ciudad_validada
        self._direccion = direccion_validada

# -------------------------------------------------------------------------------------------
#       MÉTODOS PARA VALIDAR LOS DATOS DEL CLIENTE
# -------------------------------------------------------------------------------------------

# Se comprueba que un campo de texto obligatorio no esté vacío.
    @staticmethod
    def _validar_texto(valor: str, campo: str) -> str:
        if not isinstance(valor, str) or not valor.strip():
            raise ErrorDatoClienteInvalido(f"El campo {campo} es obligatorio.")
        return valor.strip()

# Se valida que los nombres contengan letras y separadores permitidos.
    @classmethod
    def _validar_nombre(
        cls, valor: str, campo: str, obligatorio: bool = True
    ) -> str:
        if not isinstance(valor, str):
            raise ErrorDatoClienteInvalido(f"El campo {campo} debe ser texto.")
        valor = valor.strip()
        if not valor and not obligatorio:
            return ""
        if not valor:
            raise ErrorDatoClienteInvalido(f"El campo {campo} es obligatorio.")
        partes = re.split(r"[\s'-]+", valor)
        if not all(parte and parte.isalpha() for parte in partes):
            raise ErrorDatoClienteInvalido(
                f"El campo {campo} solo puede contener letras, espacios, "
                "apóstrofes o guiones."
            )
        return valor

# Se verifica que el documento contenga letras, números o guiones.
    @staticmethod
    def _validar_documento(valor: str) -> str:
        if not isinstance(valor, str):
            raise ErrorDatoClienteInvalido("El documento debe ingresarse como texto.")
        valor = valor.strip()
        if not valor or not re.fullmatch(r"[A-Za-z0-9-]+", valor):
            raise ErrorDatoClienteInvalido(
                "El documento es obligatorio y solo admite letras, números y guiones."
            )
        return valor

# Se valida que el dato seleccionado pertenezca a las opciones permitidas.
    @staticmethod
    def _validar_opcion(valor: str, opciones: tuple, campo: str) -> str:
        if valor not in opciones:
            raise ErrorDatoClienteInvalido(f"Seleccione un {campo} válido.")
        return valor

# Se rechazan fechas inválidas y fechas posteriores al día actual.
    @staticmethod
    def _validar_fecha(valor: date) -> date:
        if not isinstance(valor, date) or isinstance(valor, datetime):
            raise ErrorDatoClienteInvalido(
                "La fecha de nacimiento debe ser una fecha válida."
            )
        if valor > date.today():
            raise ErrorDatoClienteInvalido(
                "La fecha de nacimiento no puede estar en el futuro."
            )
        return valor

# Se valida que el teléfono tenga entre 7 y 15 dígitos.
    @staticmethod
    def _validar_telefono(valor: str) -> str:
        if not isinstance(valor, str) or not valor.strip():
            raise ErrorDatoClienteInvalido("El teléfono es obligatorio.")
        valor = valor.strip()
        digitos = re.sub(r"[\s()+-]", "", valor)
        if not digitos.isdigit() or not 7 <= len(digitos) <= 15:
            raise ErrorDatoClienteInvalido(
                "El teléfono debe contener entre 7 y 15 dígitos."
            )
        return valor

# Se comprueba que el correo tenga un formato básico válido.
    @staticmethod
    def _validar_correo(valor: str) -> str:
        if not isinstance(valor, str):
            raise ErrorDatoClienteInvalido("El correo electrónico debe ser texto.")
        valor = valor.strip()
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", valor):
            raise ErrorDatoClienteInvalido("Ingrese un correo electrónico válido.")
        return valor

# -------------------------------------------------------------------------------------------
#       PROPIEDADES DE LECTURA DEL CLIENTE
# -------------------------------------------------------------------------------------------

# Se exponen los datos mediante propiedades para evitar su modificación directa.
    @property
    def tipo_documento(self) -> str:
        return self._tipo_documento

# Se devuelve el número de documento del cliente.
    @property
    def documento(self) -> str:
        return self._documento

# Se construye el nombre completo omitiendo los campos opcionales vacíos.
    @property
    def nombre(self) -> str:
        return " ".join(
            parte
            for parte in (
                self._primer_nombre,
                self._segundo_nombre,
                self._primer_apellido,
                self._segundo_apellido,
            )
            if parte
        )

# Se devuelve el primer nombre.
    @property
    def primer_nombre(self) -> str:
        return self._primer_nombre

# Se devuelve el segundo nombre, si fue registrado.
    @property
    def segundo_nombre(self) -> str:
        return self._segundo_nombre

# Se devuelve el primer apellido.
    @property
    def primer_apellido(self) -> str:
        return self._primer_apellido

# Se devuelve el segundo apellido, si fue registrado.
    @property
    def segundo_apellido(self) -> str:
        return self._segundo_apellido

# Se devuelve la fecha de nacimiento validada.
    @property
    def fecha_nacimiento(self) -> date:
        return self._fecha_nacimiento

# Se calcula la edad teniendo en cuenta si ya ocurrió el cumpleaños este año.
    @property
    def edad(self) -> int:
        hoy = date.today()
        return hoy.year - self._fecha_nacimiento.year - (
            (hoy.month, hoy.day)
            < (self._fecha_nacimiento.month, self._fecha_nacimiento.day)
        )

# Se devuelve el género registrado.
    @property
    def genero(self) -> str:
        return self._genero

# Se devuelve el teléfono de contacto.
    @property
    def telefono(self) -> str:
        return self._telefono

# Se devuelve el correo electrónico de contacto.
    @property
    def correo_electronico(self) -> str:
        return self._correo_electronico

# Se devuelve el país de residencia.
    @property
    def pais_residencia(self) -> str:
        return self._pais_residencia

# Se devuelve el departamento de residencia.
    @property
    def departamento(self) -> str:
        return self._departamento

# Se devuelve la ciudad o el municipio de residencia.
    @property
    def ciudad_municipio(self) -> str:
        return self._ciudad_municipio

# Se devuelve la dirección registrada.
    @property
    def direccion(self) -> str:
        return self._direccion

# Se implementa el método abstracto de Entidad con una descripción del cliente.
    def describir(self) -> str:
        return f"Cliente {self.nombre} (documento: {self.identificador})"


# ===========================================================================================
#                       FUNCIÓN PARA BUSCAR UN CLIENTE
# ===========================================================================================

# Se busca un cliente en la lista mediante su número de identificación.
def buscar_cliente_por_identificacion(
    lista_clientes: list,
    identificacion: str,
    tipo_documento: Optional[str] = None,
) -> Cliente:
    """Devuelve el cliente encontrado o lanza una excepción de búsqueda."""

# Se comprueba que la colección y el número de identificación sean válidos.
    if not isinstance(lista_clientes, list):
        raise TypeError("lista_clientes debe ser una lista.")
    if not isinstance(identificacion, str) or not re.fullmatch(
        r"[A-Za-z0-9-]+", identificacion.strip()
    ):
        raise ErrorIdentificacionClienteInvalida(
            "Ingrese un número de identificación válido para realizar la búsqueda."
        )

# Si se proporciona el tipo de documento, también debe ser una opción permitida.
    if tipo_documento is not None and (
        not isinstance(tipo_documento, str)
        or not any(
            tipo_documento.strip().casefold() == tipo.casefold()
            for tipo in TIPOS_DOCUMENTO
        )
    ):
        raise ErrorIdentificacionClienteInvalida(
            "Seleccione un tipo de documento válido para realizar la búsqueda."
        )

# Se normaliza el texto para que espacios y diferencias entre mayúsculas y
# minúsculas no impidan encontrar un documento alfanumérico.
    identificacion_normalizada = identificacion.strip().casefold()
    for cliente in lista_clientes:
        coincide_identificacion = (
            cliente.identificador.casefold() == identificacion_normalizada
        )
        coincide_tipo = (
            tipo_documento is None
            or cliente.tipo_documento.casefold() == tipo_documento.strip().casefold()
        )
        if coincide_identificacion and coincide_tipo:
            return cliente

# Se comunica explícitamente que la búsqueda válida no encontró coincidencias.
    raise ErrorClienteNoEncontrado(
        "No se encontró un cliente con esos datos de identificación."
    )


# ===========================================================================================
#                       FUNCIÓN PARA ELIMINAR UN CLIENTE
# ===========================================================================================

# Se elimina el cliente identificado, siempre que no tenga reservas asociadas.
def eliminar_cliente(
    lista_clientes: list,
    identificacion: str,
    tipo_documento: str,
    lista_reservas: Optional[list] = None,
) -> Cliente:
    """Elimina y devuelve el cliente; conserva clientes referenciados por reservas."""
    if lista_reservas is not None and not isinstance(lista_reservas, list):
        raise TypeError("lista_reservas debe ser una lista.")

# Se localiza el cliente antes de modificar la colección.
    cliente = buscar_cliente_por_identificacion(
        lista_clientes,
        identificacion,
        tipo_documento=tipo_documento,
    )

# Se impide la eliminación si una reserva mantiene una referencia al cliente.
    for reserva in lista_reservas or []:
        cliente_reservado = getattr(reserva, "cliente", None)
        if cliente_reservado is cliente or (
            getattr(cliente_reservado, "identificador", None)
            == cliente.identificador
            and getattr(cliente_reservado, "tipo_documento", None)
            == cliente.tipo_documento
        ):
            raise ErrorClienteConReservas(
                "No se puede eliminar el cliente porque tiene reservas asociadas."
            )

# Se quita el registro de la lista compartida y se devuelve para informar el resultado.
    lista_clientes.remove(cliente)
    return cliente
