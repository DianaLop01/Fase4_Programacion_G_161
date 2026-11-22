"""Interfaz de clientes del programa Software FJ"""

# ===========================================================================================
#                       LIBRERÍAS
# ===========================================================================================

# Se importan las librerías necesarias para crear la interfaz gráfica del programa.

import tkinter as tk
import logging

# Se importa ttk para utilizar cuadros de selección y estilos compatibles con Tkinter.
from tkinter import messagebox, ttk

# Se importa date para calcular la edad a partir de la fecha de nacimiento.
from datetime import date

from clientes.cliente import (
    Cliente,
    buscar_cliente_por_identificacion,
    eliminar_cliente,
)
from clientes.excepciones import (
    ErrorCliente,
    ErrorClienteDuplicado,
    ErrorClienteNoEncontrado,
    ErrorDatoClienteInvalido,
    ErrorIdentificacionClienteInvalida,
)

logger = logging.getLogger(__name__)


# ===========================================================================================
#                       VENTANA DE GESTIÓN DE CLIENTES
# ===========================================================================================

# Clase que crea y administra el formulario de información de los clientes.

class InterfazClientes(tk.Frame):

# Se recibe la ventana donde se mostrará el formulario de clientes.
    def __init__(self, ventana, lista_clientes=None, lista_reservas=None):
        super().__init__(ventana)

# Se almacenan los objetos que se utilizarán en la interfaz de Tkinter.
        self.ventana = ventana
        self.lista_clientes = (
            [] if lista_clientes is None else lista_clientes
        )
        if not isinstance(self.lista_clientes, list):
            raise TypeError("lista_clientes debe ser una lista.")
        self.lista_reservas = (
            [] if lista_reservas is None else lista_reservas
        )
        if not isinstance(self.lista_reservas, list):
            raise TypeError("lista_reservas debe ser una lista.")

# Se almacena el cliente seleccionado para permitir su modificación posterior.
        self.cliente_encontrado = None

# Se crean las variables relacionadas con los datos del cliente.
        self._Crear_Variables()

# Se crean los campos, las etiquetas y los botones del formulario.
        self._Crear_Formulario()


# ---------------------------------------------------------------------------------------
#       MÉTODO PARA CREAR LAS VARIABLES DE LOS CAMPOS
# ---------------------------------------------------------------------------------------

# Se crean las variables utilizadas por los cuadros de texto y opciones.

    def _Crear_Variables(self):

# Campo para seleccionar el tipo de documento.
        self.tipo_documento = tk.StringVar()

# Campos relacionados con la identificación personal del cliente.
        self.documento = tk.StringVar()
        self.primer_nombre = tk.StringVar()
        self.segundo_nombre = tk.StringVar()
        self.primer_apellido = tk.StringVar()
        self.segundo_apellido = tk.StringVar()

# Campos separados para registrar año, mes y día de nacimiento.
        self.anio_nacimiento = tk.StringVar()
        self.mes_nacimiento = tk.StringVar()
        self.dia_nacimiento = tk.StringVar()

# Campo donde se muestra la edad calculada y que no puede ser modificada.
        self.edad = tk.StringVar(value = "")

# Campo para seleccionar el género del cliente.
        self.genero = tk.StringVar(value = "Otro")

# Campos relacionados con el teléfono y la residencia.
        self.telefono = tk.StringVar()
        self.correo_electronico = tk.StringVar()
        self.pais_residencia = tk.StringVar()
        self.departamento = tk.StringVar()
        self.ciudad_municipio = tk.StringVar()
        self.direccion = tk.StringVar()


# ---------------------------------------------------------------------------------------
#       MÉTODO PARA CREAR EL FORMULARIO
# ---------------------------------------------------------------------------------------

# Se crean los campos para ingresar los datos personales del cliente.

    def _Crear_Formulario(self):

# Se crea el título principal del formulario.
        tk.Label(
            self,
            text = "Datos del cliente",
            font = ("arial", 18, "bold"),
            fg = "blue"
        ).grid(row = 0, column = 0, columnspan = 4, pady = (15, 12))

# Se crea un contenedor para organizar las columnas del formulario.
        formulario = tk.Frame(self)
        formulario.grid(row = 1, column = 0, columnspan = 4, padx = 25)


# -----------------------------------------------------------------------------------
#       IDENTIFICACIÓN DEL CLIENTE
# -----------------------------------------------------------------------------------

# Campo para seleccionar el tipo de documento.
        tk.Label(
            formulario,
            text = "Tipo de documento:",
            font = ("arial", 10, "bold")
        ).grid(row = 0, column = 0, sticky = "w", pady = (8, 2))

        self.cmb_tipo_documento = ttk.Combobox(
            formulario,
            textvariable = self.tipo_documento,
            state = "readonly",
            width = 27,
            values = (
                "Cédula de ciudadanía",
                "Cédula de extranjería",
                "Pasaporte",
                "Tarjeta de identidad",
                "Otro"
            )
        )
        self.cmb_tipo_documento.grid(row = 1, column = 0, sticky = "w")

# Campo para ingresar el número de documento.
        tk.Label(
            formulario,
            text = "Documento:",
            font = ("arial", 10, "bold")
        ).grid(row = 0, column = 2, sticky = "w", pady = (8, 2))

        self.txt_documento = tk.Entry(
            formulario,
            textvariable = self.documento,
            width = 30
        )
        self.txt_documento.grid(row = 1, column = 2, sticky = "w")
        self.txt_documento.bind(
            "<Return>", lambda evento: self.Buscar_Cliente()
        )


# -----------------------------------------------------------------------------------
#       NOMBRES DEL CLIENTE
# -----------------------------------------------------------------------------------

# Campo para ingresar el primer nombre.
        tk.Label(
            formulario,
            text = "Primer nombre:",
            font = ("arial", 10, "bold")
        ).grid(row = 2, column = 0, sticky = "w", pady = (8, 2))

        tk.Entry(
            formulario,
            textvariable = self.primer_nombre,
            width = 30
        ).grid(row = 3, column = 0, sticky = "w")

# Campo opcional para ingresar el segundo nombre.
        tk.Label(
            formulario,
            text = "Segundo nombre (opcional):",
            font = ("arial", 10, "bold")
        ).grid(row = 2, column = 2, sticky = "w", pady = (8, 2))

        tk.Entry(
            formulario,
            textvariable = self.segundo_nombre,
            width = 30
        ).grid(row = 3, column = 2, sticky = "w")


# -----------------------------------------------------------------------------------
#       APELLIDOS DEL CLIENTE
# -----------------------------------------------------------------------------------

# Campo para ingresar el primer apellido.
        tk.Label(
            formulario,
            text = "Primer apellido:",
            font = ("arial", 10, "bold")
        ).grid(row = 4, column = 0, sticky = "w", pady = (8, 2))

        tk.Entry(
            formulario,
            textvariable = self.primer_apellido,
            width = 30
        ).grid(row = 5, column = 0, sticky = "w")

# Campo opcional para ingresar el segundo apellido.
        tk.Label(
            formulario,
            text = "Segundo apellido (opcional):",
            font = ("arial", 10, "bold")
        ).grid(row = 4, column = 2, sticky = "w", pady = (8, 2))

        tk.Entry(
            formulario,
            textvariable = self.segundo_apellido,
            width = 30
        ).grid(row = 5, column = 2, sticky = "w")


# -----------------------------------------------------------------------------------
#       FECHA DE NACIMIENTO Y EDAD
# -----------------------------------------------------------------------------------

# Campo para ingresar la fecha de nacimiento.
        tk.Label(
            formulario,
            text = "Fecha de nacimiento:",
            font = ("arial", 10, "bold")
        ).grid(row = 6, column = 0, sticky = "w", pady = (10, 2))

# Se utiliza un contenedor para organizar el año, el mes y el día.
        fecha_nacimiento = tk.Frame(formulario)
        fecha_nacimiento.grid(row = 7, column = 0, sticky = "w")

# Se indican la cantidad de espacios que corresponden a cada parte.
        tk.Label(fecha_nacimiento, text = "Año (4)").grid(
            row = 0, column = 0, sticky = "w")
        tk.Label(fecha_nacimiento, text = "Mes (2)").grid(
            row = 0, column = 1, padx = (8, 0), sticky = "w")
        tk.Label(fecha_nacimiento, text = "Día (2)").grid(
            row = 0, column = 2, padx = (8, 0), sticky = "w")

# Cuadro para ingresar el año con cuatro espacios.
        self.txt_anio_nacimiento = tk.Entry(
            fecha_nacimiento,
            textvariable = self.anio_nacimiento,
            width = 6,
            justify = "center"
        )
        self.txt_anio_nacimiento.grid(row = 1, column = 0)

# Cuadro para ingresar el mes con dos espacios.
        self.txt_mes_nacimiento = tk.Entry(
            fecha_nacimiento,
            textvariable = self.mes_nacimiento,
            width = 4,
            justify = "center"
        )
        self.txt_mes_nacimiento.grid(row = 1, column = 1, padx = (8, 0))

# Cuadro para ingresar el día con dos espacios.
        self.txt_dia_nacimiento = tk.Entry(
            fecha_nacimiento,
            textvariable = self.dia_nacimiento,
            width = 4,
            justify = "center"
        )
        self.txt_dia_nacimiento.grid(row = 1, column = 2, padx = (8, 0))

# Se limita la cantidad de caracteres permitida en cada parte de la fecha.
        self.txt_anio_nacimiento.bind(
            "<KeyRelease>",
            lambda evento: self._Limitar_Texto(
                self.anio_nacimiento, self.txt_anio_nacimiento, 4)
        )
        self.txt_mes_nacimiento.bind(
            "<KeyRelease>",
            lambda evento: self._Limitar_Texto(
                self.mes_nacimiento, self.txt_mes_nacimiento, 2)
        )
        self.txt_dia_nacimiento.bind(
            "<KeyRelease>",
            lambda evento: self._Limitar_Texto(
                self.dia_nacimiento, self.txt_dia_nacimiento, 2)
        )

# Campo no modificable donde se muestra la edad calculada.
        tk.Label(
            formulario,
            text = "Edad:",
            font = ("arial", 10, "bold")
        ).grid(row = 6, column = 2, sticky = "w", pady = (10, 2))

        self.txt_edad = tk.Entry(
            formulario,
            textvariable = self.edad,
            width = 8,
            state = "readonly",
            readonlybackground = "#f2f2f2",
            justify = "center"
        )
        self.txt_edad.grid(row = 7, column = 2, sticky = "w")

# Cada modificación de la fecha permite calcular nuevamente la edad.
        self.anio_nacimiento.trace_add(
            "write", lambda *argumentos: self._Calcular_Edad())
        self.mes_nacimiento.trace_add(
            "write", lambda *argumentos: self._Calcular_Edad())
        self.dia_nacimiento.trace_add(
            "write", lambda *argumentos: self._Calcular_Edad())


# -----------------------------------------------------------------------------------
#       GÉNERO
# -----------------------------------------------------------------------------------

# Campo para seleccionar el género del cliente.
        tk.Label(
            formulario,
            text = "Género:",
            font = ("arial", 10, "bold")
        ).grid(row = 8, column = 0, sticky = "w", pady = (10, 2))

        generos = tk.Frame(formulario)
        generos.grid(row = 9, column = 0, columnspan = 3, sticky = "w")

        tk.Radiobutton(
            generos,
            text = "F (Femenino)",
            variable = self.genero,
            value = "F"
        ).pack(side = "left", padx = (0, 10))

        tk.Radiobutton(
            generos,
            text = "M (Masculino)",
            variable = self.genero,
            value = "M"
        ).pack(side = "left", padx = (0, 10))

        tk.Radiobutton(
            generos,
            text = "Otro",
            variable = self.genero,
            value = "Otro"
        ).pack(side = "left")


# -----------------------------------------------------------------------------------
#       INFORMACIÓN DE CONTACTO
# -----------------------------------------------------------------------------------

# Campo para ingresar el teléfono.
        tk.Label(
            formulario,
            text = "Teléfono:",
            font = ("arial", 10, "bold")
        ).grid(row = 10, column = 0, sticky = "w", pady = (10, 2))

        tk.Entry(
            formulario,
            textvariable = self.telefono,
            width = 30
        ).grid(row = 11, column = 0, sticky = "w")

# Campo para ingresar el correo electrónico.
        tk.Label(
            formulario,
            text = "Correo electrónico:",
            font = ("arial", 10, "bold")
        ).grid(row = 10, column = 2, sticky = "w", pady = (10, 2))

        tk.Entry(
            formulario,
            textvariable = self.correo_electronico,
            width = 30
        ).grid(row = 11, column = 2, sticky = "w")


# -----------------------------------------------------------------------------------
#       INFORMACIÓN DE RESIDENCIA
# -----------------------------------------------------------------------------------

# Campo para ingresar el país de residencia.
        tk.Label(
            formulario,
            text = "País de residencia:",
            font = ("arial", 10, "bold")
        ).grid(row = 12, column = 0, sticky = "w", pady = (10, 2))

        tk.Entry(
            formulario,
            textvariable = self.pais_residencia,
            width = 30
        ).grid(row = 13, column = 0, sticky = "w")

# Campo para ingresar el departamento.
        tk.Label(
            formulario,
            text = "Departamento:",
            font = ("arial", 10, "bold")
        ).grid(row = 12, column = 2, sticky = "w", pady = (10, 2))

        tk.Entry(
            formulario,
            textvariable = self.departamento,
            width = 30
        ).grid(row = 13, column = 2, sticky = "w")

# Campo para ingresar la ciudad o el municipio.
        tk.Label(
            formulario,
            text = "Ciudad o Municipio:",
            font = ("arial", 10, "bold")
        ).grid(row = 14, column = 0, sticky = "w", pady = (10, 2))

        tk.Entry(
            formulario,
            textvariable = self.ciudad_municipio,
            width = 30
        ).grid(row = 15, column = 0, sticky = "w")

# Campo para ingresar la dirección.
        tk.Label(
            formulario,
            text = "Dirección:",
            font = ("arial", 10, "bold")
        ).grid(row = 14, column = 2, sticky = "w", pady = (10, 2))

        tk.Entry(
            formulario,
            textvariable = self.direccion,
            width = 30
        ).grid(row = 15, column = 2, sticky = "w")


# -----------------------------------------------------------------------------------
#       BOTONES DE ACCIÓN
# -----------------------------------------------------------------------------------

# Se crean los botones de registro y mantenimiento del formulario.
        botones = tk.Frame(self)
        botones.grid(row = 2, column = 0, columnspan = 4, pady = (18, 12))

# Botón para buscar y cargar los datos de un cliente existente.
        tk.Button(
            botones,
            text = "Buscar cliente",
            width = 16,
            command = self.Buscar_Cliente
        ).pack(side = "left", padx = 8)

# Botón para validar y guardar el cliente en la lista en memoria.
        self.btn_registrar = tk.Button(
            botones,
            text = "Registrar cliente",
            width = 16,
            command = self.Registrar_Cliente
        )
        self.btn_registrar.pack(side = "left", padx = 8)

# Botón para guardar los cambios del cliente encontrado.
        self.btn_modificar = tk.Button(
            botones,
            text = "Modificar cliente",
            width = 16,
            command = self.Modificar_Cliente,
            state = tk.DISABLED,
        )
        self.btn_modificar.pack(side = "left", padx = 8)

# Botón para eliminar el cliente encontrado, inicialmente deshabilitado.
        self.btn_eliminar = tk.Button(
            botones,
            text = "Eliminar cliente",
            width = 16,
            command = self.Eliminar_Cliente,
            state = tk.DISABLED,
        )
        self.btn_eliminar.pack(side = "left", padx = 8)

# Botón para borrar los datos escritos en el formulario.
        tk.Button(
            botones,
            text = "Limpiar",
            width = 12,
            command = self.Limpiar_Formulario
        ).pack(side = "left", padx = 8)

# Botón para cerrar la ventana de clientes.
        tk.Button(
            botones,
            text = "Cerrar",
            width = 12,
            command = self.ventana.destroy
        ).pack(side = "left", padx = 8)

# Etiqueta para comunicar el resultado de las búsquedas y operaciones.
        self.lbl_resultado = tk.Label(self, text = "")
        self.lbl_resultado.grid(row = 3, column = 0, columnspan = 4, pady = 4)

# Se muestra una lista con los clientes registrados durante la sesión.
        tk.Label(
            self,
            text = "Clientes registrados en esta sesión",
            font = ("arial", 10, "bold")
        ).grid(row = 4, column = 0, columnspan = 4, sticky = "w", padx = 25)

        self.lista_visual_clientes = tk.Listbox(self, height = 5, width = 95)
        self.lista_visual_clientes.grid(
            row = 5, column = 0, columnspan = 4, padx = 25, pady = (4, 10)
        )
        self._Actualizar_Lista_Visual()


# ---------------------------------------------------------------------------------------
#       MÉTODO PARA BUSCAR UN CLIENTE
# ---------------------------------------------------------------------------------------

# Se busca el cliente por tipo y número de documento y se cargan sus datos.

    def Buscar_Cliente(self):
# Se obtienen los datos de identificación ingresados en el formulario.
        tipo_documento = self.tipo_documento.get().strip()
        identificacion = self.documento.get().strip()

        try:
# El tipo y el número de documento se utilizan para localizar al cliente.
            if not tipo_documento:
                raise ErrorIdentificacionClienteInvalida(
                    "Seleccione el tipo de documento para realizar la búsqueda."
                )
            cliente = buscar_cliente_por_identificacion(
                self.lista_clientes,
                identificacion,
                tipo_documento=tipo_documento,
            )
# Se informa cuando la búsqueda es válida, pero no hay coincidencias.
        except ErrorClienteNoEncontrado as error:
            self._Limpiar_Datos_Buscados()
            self._Restablecer_Modo_Registro()
            self.lbl_resultado.config(text = str(error), fg = "red")
            logger.info("Búsqueda de cliente sin coincidencias.")
            return
# Se comunican los errores de formato o de parámetros de búsqueda.
        except ErrorCliente as error:
            logger.warning("Búsqueda de cliente rechazada: %s", error)
            self.lbl_resultado.config(text = str(error), fg = "red")
            return

# Se carga el cliente encontrado y se habilita el modo de modificación.
        self.cliente_encontrado = cliente
        self._Cargar_Datos_Cliente(cliente)
        self.cmb_tipo_documento.config(state = tk.DISABLED)
        self.txt_documento.config(state = tk.DISABLED)
        self.btn_registrar.config(state = tk.DISABLED)
        self.btn_modificar.config(state = tk.NORMAL)
        self.btn_eliminar.config(state = tk.NORMAL)
        self.lbl_resultado.config(
            text = f"Datos de {cliente.nombre} cargados correctamente.",
            fg = "green",
        )
        logger.info("Datos de cliente encontrados y cargados en el formulario.")

# Se confirma y procesa la eliminación del cliente seleccionado.
    def Eliminar_Cliente(self):
# Se valida que haya un cliente seleccionado antes de iniciar la operación.
        if self.cliente_encontrado is None:
            self.lbl_resultado.config(
                text = "Busque un cliente antes de eliminarlo.",
                fg = "red",
            )
            return

# Se solicita confirmación para evitar una eliminación accidental.
        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            "¿Está seguro de que desea eliminar el cliente seleccionado?",
            parent=self.ventana,
        )
        if not confirmar:
            return

        try:
            cliente_eliminado = eliminar_cliente(
                self.lista_clientes,
                self.cliente_encontrado.identificador,
                self.cliente_encontrado.tipo_documento,
                self.lista_reservas,
            )
        except ErrorCliente as error:
            logger.warning("Eliminación de cliente rechazada: %s", error)
            self.lbl_resultado.config(text = str(error), fg = "red")
            return

# Se actualiza la lista y se limpia el formulario después de eliminar.
        self._Actualizar_Lista_Visual()
        self.Limpiar_Formulario()
        self.lbl_resultado.config(
            text = f"Cliente {cliente_eliminado.nombre} eliminado correctamente.",
            fg = "green",
        )
        logger.info("Cliente eliminado correctamente.")

# Se validan y guardan los cambios realizados al cliente encontrado.
    def Modificar_Cliente(self):
# Se evita modificar un registro si no se ha seleccionado mediante la búsqueda.
        if self.cliente_encontrado is None:
            self.lbl_resultado.config(
                text = "Busque un cliente antes de modificar sus datos.",
                fg = "red",
            )
            return

        try:
            self.cliente_encontrado.actualizar_datos(
                primer_nombre=self.primer_nombre.get(),
                segundo_nombre=self.segundo_nombre.get(),
                primer_apellido=self.primer_apellido.get(),
                segundo_apellido=self.segundo_apellido.get(),
                fecha_nacimiento=self._Obtener_Fecha_Nacimiento(),
                genero=self.genero.get(),
                telefono=self.telefono.get(),
                correo_electronico=self.correo_electronico.get(),
                pais_residencia=self.pais_residencia.get(),
                departamento=self.departamento.get(),
                ciudad_municipio=self.ciudad_municipio.get(),
                direccion=self.direccion.get(),
            )
        except ErrorCliente as error:
# Si algún dato no es válido, se informa el error sin actualizar la lista visual.
            logger.warning("Modificación de cliente rechazada: %s", error)
            self.lbl_resultado.config(text = str(error), fg = "red")
            return

# Se refresca la lista después de actualizar el objeto del cliente.
        self._Actualizar_Lista_Visual()
        self.lbl_resultado.config(
            text = f"Datos de {self.cliente_encontrado.nombre} actualizados.",
            fg = "green",
        )
        logger.info("Datos del cliente actualizados correctamente.")

# Se copian los datos del objeto encontrado a los campos del formulario.
    def _Cargar_Datos_Cliente(self, cliente: Cliente):
        self.primer_nombre.set(cliente.primer_nombre)
        self.segundo_nombre.set(cliente.segundo_nombre)
        self.primer_apellido.set(cliente.primer_apellido)
        self.segundo_apellido.set(cliente.segundo_apellido)
        self.anio_nacimiento.set(f"{cliente.fecha_nacimiento.year:04d}")
        self.mes_nacimiento.set(f"{cliente.fecha_nacimiento.month:02d}")
        self.dia_nacimiento.set(f"{cliente.fecha_nacimiento.day:02d}")
        self.edad.set(str(cliente.edad))
        self.genero.set(cliente.genero)
        self.telefono.set(cliente.telefono)
        self.correo_electronico.set(cliente.correo_electronico)
        self.pais_residencia.set(cliente.pais_residencia)
        self.departamento.set(cliente.departamento)
        self.ciudad_municipio.set(cliente.ciudad_municipio)
        self.direccion.set(cliente.direccion)

# Se restablecen los controles al modo de registro y se habilita otra búsqueda.
    def _Restablecer_Modo_Registro(self):
        self.cliente_encontrado = None
        self.cmb_tipo_documento.config(state = "readonly")
        self.txt_documento.config(state = tk.NORMAL)
        self.btn_registrar.config(state = tk.NORMAL)
        self.btn_modificar.config(state = tk.DISABLED)
        self.btn_eliminar.config(state = tk.DISABLED)

# Se limpian los datos personales cuando la búsqueda no encuentra coincidencias.
    def _Limpiar_Datos_Buscados(self):
        self.primer_nombre.set("")
        self.segundo_nombre.set("")
        self.primer_apellido.set("")
        self.segundo_apellido.set("")
        self.anio_nacimiento.set("")
        self.mes_nacimiento.set("")
        self.dia_nacimiento.set("")
        self.edad.set("")
        self.genero.set("Otro")
        self.telefono.set("")
        self.correo_electronico.set("")
        self.pais_residencia.set("")
        self.departamento.set("")
        self.ciudad_municipio.set("")
        self.direccion.set("")

# ---------------------------------------------------------------------------------------
#       MÉTODO PARA REGISTRAR UN CLIENTE
# ---------------------------------------------------------------------------------------

# Se valida el formulario y se agrega el cliente a la lista compartida.

    def Registrar_Cliente(self):
        try:
            fecha_nacimiento = self._Obtener_Fecha_Nacimiento()
            cliente = Cliente(
                tipo_documento=self.tipo_documento.get(),
                documento=self.documento.get(),
                primer_nombre=self.primer_nombre.get(),
                segundo_nombre=self.segundo_nombre.get(),
                primer_apellido=self.primer_apellido.get(),
                segundo_apellido=self.segundo_apellido.get(),
                fecha_nacimiento=fecha_nacimiento,
                genero=self.genero.get(),
                telefono=self.telefono.get(),
                correo_electronico=self.correo_electronico.get(),
                pais_residencia=self.pais_residencia.get(),
                departamento=self.departamento.get(),
                ciudad_municipio=self.ciudad_municipio.get(),
                direccion=self.direccion.get(),
            )

            if any(
                cliente_existente.tipo_documento == cliente.tipo_documento
                and cliente_existente.documento.casefold()
                == cliente.documento.casefold()
                for cliente_existente in self.lista_clientes
            ):
# Se impide registrar otra vez un cliente con el mismo documento.
                raise ErrorClienteDuplicado(
                    "Ya existe un cliente con ese tipo y número de documento."
                )

            self.lista_clientes.append(cliente)
        except ErrorCliente as error:
            logger.warning("Registro de cliente rechazado: %s", error)
            self.lbl_resultado.config(text = str(error), fg = "red")
            return

# Se informa el registro exitoso y se actualiza la lista visible.
        logger.info("Cliente registrado correctamente.")
        self._Actualizar_Lista_Visual()
        self.lbl_resultado.config(
            text = f"Cliente {cliente.nombre} registrado correctamente.",
            fg = "green"
        )

# Se construye una fecha a partir de los campos de año, mes y día.
    def _Obtener_Fecha_Nacimiento(self):
        valores = (
            self.anio_nacimiento.get().strip(),
            self.mes_nacimiento.get().strip(),
            self.dia_nacimiento.get().strip(),
        )
        if not all(valores):
# Se rechaza la búsqueda o el registro cuando faltan partes de la fecha.
            raise ErrorDatoClienteInvalido(
                "La fecha de nacimiento es obligatoria."
            )
        try:
            return date(*(int(valor) for valor in valores))
        except ValueError as error:
# Se transforma el error de conversión en una excepción del dominio.
            raise ErrorDatoClienteInvalido(
                "Ingrese una fecha de nacimiento válida."
            ) from error

# Se vuelve a mostrar la lista compartida después de registrar o modificar.
    def _Actualizar_Lista_Visual(self):
        self.lista_visual_clientes.delete(0, tk.END)
        for cliente in self.lista_clientes:
            self.lista_visual_clientes.insert(
                tk.END, f"{cliente.identificador} - {cliente.nombre}"
            )

# ---------------------------------------------------------------------------------------
#       MÉTODO PARA LIMITAR LA LONGITUD DE LA FECHA
# ---------------------------------------------------------------------------------------

# Se permite únicamente escribir números y se limita la longitud indicada.

    def _Limitar_Texto(self, variable, entrada, longitud):
        texto = variable.get()
        texto = "".join(caracter for caracter in texto if caracter.isdigit())
        texto = texto[:longitud]

        if entrada.get() != texto:
            variable.set(texto)


# ---------------------------------------------------------------------------------------
#       MÉTODO PARA CALCULAR LA EDAD
# ---------------------------------------------------------------------------------------

# Se calcula la edad cuando el año, el mes y el día forman una fecha válida.
# La edad se presenta en un campo que no puede ser modificado por el usuario.

    def _Calcular_Edad(self):
        texto_anio = self.anio_nacimiento.get().strip()
        texto_mes = self.mes_nacimiento.get().strip()
        texto_dia = self.dia_nacimiento.get().strip()

# Se verifica que la fecha tenga las cantidades de espacios indicadas.
        if len(texto_anio) != 4 or len(texto_mes) != 2 or len(texto_dia) != 2:
            self.edad.set("")
            return

        try:

# Se convierten el año, el mes y el día en valores enteros.
            anio = int(texto_anio)
            mes = int(texto_mes)
            dia = int(texto_dia)

# Se comprueba que la fecha de nacimiento sea una fecha existente.
            fecha_nacimiento = date(anio, mes, dia)

# Se obtiene la fecha actual del sistema.
            hoy = date.today()

# Se calcula inicialmente la edad a partir de la diferencia de años.
            edad = hoy.year - fecha_nacimiento.year

# Si todavía no ha ocurrido el cumpleaños, se resta un año.
            if (hoy.month, hoy.day) < (mes, dia):
                edad -= 1

# Una fecha futura no debe generar una edad negativa.
            if edad < 0:
                self.edad.set("")
            else:
                self.edad.set(str(edad))

        except (TypeError, ValueError):

# Si la fecha no es válida, el campo de edad se mantiene vacío.
            self.edad.set("")


# ---------------------------------------------------------------------------------------
#       MÉTODO PARA LIMPIAR EL FORMULARIO
# ---------------------------------------------------------------------------------------

# Se restablecen todos los campos a su estado inicial.

    def Limpiar_Formulario(self):
        self._Restablecer_Modo_Registro()
        self.tipo_documento.set("")
        self.documento.set("")
        self.primer_nombre.set("")
        self.segundo_nombre.set("")
        self.primer_apellido.set("")
        self.segundo_apellido.set("")
        self.anio_nacimiento.set("")
        self.mes_nacimiento.set("")
        self.dia_nacimiento.set("")
        self.edad.set("")
        self.genero.set("Otro")
        self.telefono.set("")
        self.correo_electronico.set("")
        self.pais_residencia.set("")
        self.departamento.set("")
        self.ciudad_municipio.set("")
        self.direccion.set("")
        self.lbl_resultado.config(text = "")


# ===========================================================================================
#                       FUNCIÓN PARA ABRIR LA INTERFAZ
# ===========================================================================================

# Función que crea la ventana y muestra el formulario de clientes.

def Abrir_Ventana_Clientes(
    ventana_padre=None,
    lista_clientes=None,
    lista_reservas=None,
):

# Se crea una ventana independiente si no se recibe una ventana principal.
    if ventana_padre is None:
        ventana = tk.Tk()
        ventana.title("Software FJ")
        ejecutar_bucle = True
    else:

# Si se recibe la ventana principal, se abre el formulario como ventana secundaria.
        ventana = tk.Toplevel(ventana_padre)
        ventana.title("Software FJ")
        ejecutar_bucle = False

# Se configura el tamaño y el comportamiento de la ventana.
    ventana.geometry("820x700")
    ventana.resizable(False, False)

# Se crea el formulario de clientes y se agrega a la ventana.
    interfaz = InterfazClientes(ventana, lista_clientes, lista_reservas)
    interfaz.pack(fill = "both", expand = True)

# Se mantiene activo el bucle si el formulario se ejecuta de forma independiente.
    if ejecutar_bucle:
        ventana.mainloop()

# Se devuelve la ventana creada para permitir su administración desde main.py.
    return ventana
