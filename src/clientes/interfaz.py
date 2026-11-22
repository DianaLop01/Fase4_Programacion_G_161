"""Interfaz de clientes del programa Software FJ"""

# ===========================================================================================
#                       LIBRERÍAS
# ===========================================================================================

# Se importan las librerías necesarias para crear la interfaz gráfica del programa.

import tkinter as tk

# Se importa ttk para utilizar cuadros de selección y estilos compatibles con Tkinter.
from tkinter import ttk

# Se importa date para calcular la edad a partir de la fecha de nacimiento.
from datetime import date


# ===========================================================================================
#                       VENTANA DE GESTIÓN DE CLIENTES
# ===========================================================================================

# Clase que crea y administra el formulario de información de los clientes.

class InterfazClientes(tk.Frame):

# Se recibe la ventana donde se mostrará el formulario de clientes.
    def __init__(self, ventana):
        super().__init__(ventana)

# Se almacenan los objetos que se utilizarán en la interfaz de Tkinter.
        self.ventana = ventana

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

        tk.Entry(
            formulario,
            textvariable = self.documento,
            width = 30
        ).grid(row = 1, column = 2, sticky = "w")


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

# Se crean los botones que permiten limpiar o cerrar el formulario.
        botones = tk.Frame(self)
        botones.grid(row = 2, column = 0, columnspan = 4, pady = (18, 12))

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


# ===========================================================================================
#                       FUNCIÓN PARA ABRIR LA INTERFAZ
# ===========================================================================================

# Función que crea la ventana y muestra el formulario de clientes.

def Abrir_Ventana_Clientes(ventana_padre = None):

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
    ventana.geometry("820x620")
    ventana.resizable(False, False)

# Se crea el formulario de clientes y se agrega a la ventana.
    interfaz = InterfazClientes(ventana)
    interfaz.pack(fill = "both", expand = True)

# Se mantiene activo el bucle si el formulario se ejecuta de forma independiente.
    if ejecutar_bucle:
        ventana.mainloop()

# Se devuelve la ventana creada para permitir su administración desde main.py.
    return ventana
