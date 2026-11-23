
"""
Interfaz grafica para las operaciones de servicios.
"""

# ===========================================================================================
#                       LIBRERIAS
# ===========================================================================================

# Se importa Tkinter para construir la interfaz grafica.
import tkinter as tk
from math import isfinite
from tkinter import ttk, messagebox

# Se importan las clases especializadas.
from .alquiler_equipos import AlquilerEquipos
from .asesoria import Asesoria
from .reserva_salas import ReservaSalas

# Se importan las excepciones.
from .excepciones import ErrorServicio


# ===========================================================================================
#                       CLASE INTERFAZ DE SERVICIOS
# ===========================================================================================

class InterfazServicios:

    # ---------------------------------------------------------------------------------------
    #       METODO CONSTRUCTOR
    # ---------------------------------------------------------------------------------------

    def __init__(self, ventana_principal, lista_servicios=None):

        self.ventana = tk.Toplevel(ventana_principal)

        # Se configura la ventana.
        self.ventana.title("Gestion de Servicios - Software FJ")
        self.ventana.geometry("750x650")
        self.ventana.resizable(False, False)

        # Se usa la lista compartida para que reservas consulten los servicios.
        self.servicios_registrados = (
            [] if lista_servicios is None else lista_servicios
        )
        if not isinstance(self.servicios_registrados, list):
            raise TypeError("lista_servicios debe ser una lista.")

        # Se crean los elementos de la interfaz.
        self.Crear_Interfaz()

    # ---------------------------------------------------------------------------------------
    #       METODO PARA CREAR LA INTERFAZ
    # ---------------------------------------------------------------------------------------

    def Crear_Interfaz(self):

        # Titulo principal.
        tk.Label(
            self.ventana,
            text="GESTION DE SERVICIOS",
            font=("Arial", 20, "bold"),
            fg="blue"
        ).pack(pady=15)

        tk.Label(
            self.ventana,
            text="Software FJ - Registro y administracion de servicios",
            font=("Arial", 11)
        ).pack(pady=5)

        tk.Label(
            self.ventana,
            text="* Campo obligatorio. Los campos que no aplican se deshabilitan.",
            font=("Arial", 9),
        ).pack()

        # Contenedor de los campos.
        formulario = tk.Frame(self.ventana)
        formulario.pack(pady=15)

        # Seleccion del tipo de servicio.
        self.etiquetas_campos = {}
        self.lbl_tipo_servicio = tk.Label(
            formulario,
            text="Tipo de servicio *:",
            font=("Arial", 10, "bold")
        )
        self.lbl_tipo_servicio.grid(
            row=0, column=0, padx=10, pady=8, sticky="w"
        )

        self.tipo_servicio = ttk.Combobox(
            formulario,
            values=[
                "Alquiler de equipos",
                "Asesoria",
                "Reserva de salas"
            ],
            state="readonly",
            width=30
        )

        self.tipo_servicio.grid(row=0, column=1, padx=10, pady=8)
        self.tipo_servicio.current(0)
        estilo = ttk.Style(self.ventana)
        estilo.configure(
            "CampoInvalido.TCombobox",
            fieldbackground="#ffe6e6",
        )
        estilo.map(
            "CampoInvalido.TCombobox",
            fieldbackground=[
                ("readonly", "#ffe6e6"),
                ("!disabled", "#ffe6e6"),
            ],
        )

        # Campos generales.
        self.campos = {}

        datos = [
            ("Código", "codigo"),
            ("Nombre", "nombre"),
            ("Descripción", "descripcion"),
            ("Tarifa ($)", "tarifa"),
            ("Cantidad de equipos", "cantidad"),
            ("Duración (días / horas)", "duracion"),
            ("Dato adicional", "adicional")
        ]

        for fila, (etiqueta, clave) in enumerate(datos, start=1):

            self.etiquetas_campos[clave] = tk.Label(
                formulario,
                text=etiqueta,
                font=("Arial", 10)
            )
            self.etiquetas_campos[clave].grid(
                row=fila, column=0, padx=10, pady=6, sticky="w"
            )

            entrada = tk.Entry(formulario, width=33)
            entrada.grid(row=fila, column=1, padx=10, pady=6)

            self.campos[clave] = entrada

        self.tipo_servicio.bind(
            "<<ComboboxSelected>>",
            lambda _: self._actualizar_campos_servicio(),
        )
        self._actualizar_campos_servicio()

        # Botones de operaciones.
        botones = tk.Frame(self.ventana)
        botones.pack(pady=10)

        tk.Button(
            botones,
            text="Registrar servicio",
            command=self.Registrar_Servicio,
            bg="green",
            fg="white",
            font=("Arial", 10, "bold"),
            width=18
        ).grid(row=0, column=0, padx=10)

        tk.Button(
            botones,
            text="Limpiar campos",
            command=self.Limpiar_Campos,
            font=("Arial", 10),
            width=18
        ).grid(row=0, column=1, padx=10)

        # Etiqueta para informar errores y resultados sin abrir ventanas emergentes.
        self.lbl_resultado = tk.Label(
            self.ventana,
            text="",
            font=("Arial", 10, "bold"),
            wraplength=680,
        )
        self.lbl_resultado.pack(pady=(0, 8))

        # Lista de servicios registrados.
        tk.Label(
            self.ventana,
            text="Servicios registrados:",
            font=("Arial", 12, "bold")
        ).pack(pady=5)

        self.lista_servicios = tk.Listbox(
            self.ventana,
            width=85,
            height=8
        )

        self.lista_servicios.pack(pady=5)

        # Boton para consultar el servicio seleccionado.
        tk.Button(
            self.ventana,
            text="Consultar servicio seleccionado",
            command=self.Consultar_Servicio,
            font=("Arial", 10, "bold"),
            width=30
        ).pack(pady=10)

    # ---------------------------------------------------------------------------------------
    #       METODO PARA REGISTRAR SERVICIOS
    # ---------------------------------------------------------------------------------------

    # Convierte un valor decimal y traduce errores de entrada a mensajes del sistema.
    @staticmethod
    def _convertir_decimal(valor, campo):
        try:
            return float(valor)
        except (TypeError, ValueError) as error:
            raise ErrorServicio(
                f"El campo {campo} debe contener un número válido."
            ) from error

    # Convierte un valor entero y traduce errores de entrada a mensajes del sistema.
    @staticmethod
    def _convertir_entero(valor, campo):
        try:
            return int(valor)
        except (TypeError, ValueError) as error:
            raise ErrorServicio(
                f"El campo {campo} debe contener un número entero válido."
            ) from error

    # Muestra el resultado de una operación dentro de la ventana actual.
    def _mostrar_resultado(self, mensaje, color):
        self.lbl_resultado.config(text=mensaje, fg=color)

    # Ajusta los nombres y los campos requeridos al tipo de servicio seleccionado.
    def _actualizar_campos_servicio(self):
        tipo = self.tipo_servicio.get()
        requeridos = {"codigo", "nombre", "descripcion", "tarifa", "duracion"}

        if tipo == "Alquiler de equipos":
            requeridos.add("cantidad")
            textos = {
                "cantidad": "Cantidad de equipos",
                "adicional": "Dato adicional (no aplica)",
            }
        elif tipo == "Asesoria":
            requeridos.add("adicional")
            textos = {
                "cantidad": "Cantidad de equipos (no aplica)",
                "adicional": "Modalidad",
            }
        else:
            requeridos.add("adicional")
            textos = {
                "cantidad": "Cantidad de equipos (no aplica)",
                "adicional": "Capacidad de sala",
            }

        textos.update(
            {
                "codigo": "Código",
                "nombre": "Nombre",
                "descripcion": "Descripción",
                "tarifa": "Tarifa ($)",
                "duracion": "Duración (días / horas)",
            }
        )
        self.lbl_tipo_servicio.config(fg="black")
        self.tipo_servicio.configure(style="TCombobox")
        for clave, etiqueta in self.etiquetas_campos.items():
            requerido = clave in requeridos
            etiqueta.config(
                text=f"{textos[clave]}{' *' if requerido else ''}",
                fg="black",
            )
            self.campos[clave].configure(
                state=tk.NORMAL if requerido else tk.DISABLED,
            )
        self._limpiar_resaltado_campos()

    # Restablece el resaltado cuando inicia una corrección o cambia el servicio.
    def _limpiar_resaltado_campos(self):
        self.lbl_tipo_servicio.config(fg="black")
        self.tipo_servicio.configure(style="TCombobox")
        for etiqueta in self.etiquetas_campos.values():
            etiqueta.config(fg="black")
        for entrada in self.campos.values():
            entrada.configure(bg="white")

    # Resalta las etiquetas y entradas requeridas que deben corregirse.
    def _resaltar_campos(self, claves):
        if "tipo" in claves:
            self.lbl_tipo_servicio.config(fg="red")
            self.tipo_servicio.configure(style="CampoInvalido.TCombobox")
        for clave in claves:
            if clave in self.etiquetas_campos:
                self.etiquetas_campos[clave].config(fg="red")
                self.campos[clave].configure(bg="#ffe6e6")

    def Registrar_Servicio(self):
        campo_actual = None
        self._limpiar_resaltado_campos()

        try:

            # Se obtienen los datos del formulario.
            tipo = self.tipo_servicio.get()

            codigo = self.campos["codigo"].get().strip()
            nombre = self.campos["nombre"].get().strip()
            descripcion = self.campos["descripcion"].get().strip()
            tarifa_ingresada = self.campos["tarifa"].get().strip()
            duracion_ingresada = self.campos["duracion"].get().strip()
            adicional = self.campos["adicional"].get().strip()

            requeridos = ["codigo", "nombre", "descripcion", "tarifa", "duracion"]
            if tipo == "Alquiler de equipos":
                requeridos.append("cantidad")
            elif tipo in ("Asesoria", "Reserva de salas"):
                requeridos.append("adicional")

            valores_campos = {
                "codigo": codigo,
                "nombre": nombre,
                "descripcion": descripcion,
                "tarifa": tarifa_ingresada,
                "duracion": duracion_ingresada,
                "cantidad": self.campos["cantidad"].get().strip(),
                "adicional": adicional,
            }
            faltantes = [
                clave for clave in requeridos if not valores_campos[clave]
            ]
            if not tipo:
                faltantes.append("tipo")
            if faltantes:
                self._resaltar_campos(faltantes)
                nombres = [
                    self.lbl_tipo_servicio.cget("text").rstrip(":")
                    if clave == "tipo"
                    else self.etiquetas_campos[clave].cget("text").rstrip(" *:")
                    for clave in faltantes
                ]
                raise ErrorServicio(
                    "Complete los campos obligatorios: "
                    + ", ".join(nombres)
                    + "."
                )

            campo_actual = "tarifa"
            tarifa = self._convertir_decimal(tarifa_ingresada, "Tarifa")
            campo_actual = "duracion"
            duracion = self._convertir_decimal(
                duracion_ingresada, "Duración"
            )
            if not isfinite(tarifa) or tarifa <= 0:
                campo_actual = "tarifa"
                raise ErrorServicio("La tarifa debe ser mayor que cero.")
            if not isfinite(duracion) or duracion <= 0:
                campo_actual = "duracion"
                raise ErrorServicio("La duración debe ser mayor que cero.")

            campo_actual = "codigo"
            if any(s.codigo == codigo for s in self.servicios_registrados):
                raise ErrorServicio(
                    "Ya existe un servicio registrado con ese codigo."
                )
            campo_actual = None

            # Se crea el objeto segun el tipo de servicio.
            if tipo == "Alquiler de equipos":

                campo_actual = "cantidad"
                cantidad = self._convertir_entero(
                    self.campos["cantidad"].get().strip(),
                    "Cantidad de equipos",
                )
                if cantidad <= 0:
                    campo_actual = "cantidad"
                    raise ErrorServicio(
                        "La cantidad de equipos debe ser mayor que cero."
                    )
                if not duracion.is_integer():
                    campo_actual = "duracion"
                    raise ErrorServicio(
                        "Los días de alquiler deben ser un número entero."
                    )

                servicio = AlquilerEquipos(
                    codigo,
                    nombre,
                    descripcion,
                    tarifa,
                    cantidad,
                    int(duracion)
                )

            elif tipo == "Asesoria":

                campo_actual = "adicional"
                servicio = Asesoria(
                    codigo,
                    nombre,
                    descripcion,
                    tarifa,
                    duracion,
                    adicional.capitalize()
                )

            elif tipo == "Reserva de salas":

                campo_actual = "adicional"
                capacidad = self._convertir_entero(adicional, "Capacidad")
                if capacidad <= 0:
                    raise ErrorServicio(
                        "La capacidad de la sala debe ser mayor que cero."
                    )

                servicio = ReservaSalas(
                    codigo,
                    nombre,
                    descripcion,
                    tarifa,
                    duracion,
                    capacidad
                )

            # Se almacena el objeto creado.
            self.servicios_registrados.append(servicio)

            # Se actualiza la lista de servicios.
            self.lista_servicios.insert(
                tk.END,
                f"{codigo} - {nombre} - ${servicio.Calcular_Costo():,.2f}"
            )

            self.Limpiar_Campos()
            campo_actual = None
            self._mostrar_resultado(
                "El servicio fue registrado correctamente. "
                f"Costo total: ${servicio.Calcular_Costo():,.2f}",
                "green",
            )

        except (ValueError, ErrorServicio) as error:
            if campo_actual:
                self._resaltar_campos([campo_actual])
            self._mostrar_resultado(str(error), "red")

    # ---------------------------------------------------------------------------------------
    #       METODO PARA CONSULTAR SERVICIOS
    # ---------------------------------------------------------------------------------------

    def Consultar_Servicio(self):

        seleccion = self.lista_servicios.curselection()

        if not seleccion:
            self._mostrar_resultado(
                "Seleccione un servicio de la lista.",
                "red",
            )
            return

        # Se obtiene el servicio seleccionado.
        indice = seleccion[0]
        servicio = self.servicios_registrados[indice]
        self._mostrar_resultado("", "black")

        # Se muestra toda la informacion.
        messagebox.showinfo(
            "Informacion del servicio",
            servicio.Mostrar_Informacion()
        )

    # ---------------------------------------------------------------------------------------
    #       METODO PARA LIMPIAR LOS CAMPOS
    # ---------------------------------------------------------------------------------------

    def Limpiar_Campos(self):

        for entrada in self.campos.values():
            entrada.configure(state=tk.NORMAL)
            entrada.delete(0, tk.END)
        self._actualizar_campos_servicio()
        self._mostrar_resultado("", "black")
