
"""
Interfaz grafica para las operaciones de servicios.
"""

# ===========================================================================================
#                       LIBRERIAS
# ===========================================================================================

# Se importa Tkinter para construir la interfaz grafica.
import tkinter as tk
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

    def __init__(self, ventana_principal):

        self.ventana = tk.Toplevel(ventana_principal)

        # Se configura la ventana.
        self.ventana.title("Gestion de Servicios - Software FJ")
        self.ventana.geometry("750x650")
        self.ventana.resizable(False, False)

        # Lista para almacenar los servicios registrados.
        self.servicios_registrados = []

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

        # Contenedor de los campos.
        formulario = tk.Frame(self.ventana)
        formulario.pack(pady=15)

        # Seleccion del tipo de servicio.
        tk.Label(
            formulario,
            text="Tipo de servicio:",
            font=("Arial", 10, "bold")
        ).grid(row=0, column=0, padx=10, pady=8, sticky="w")

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

        # Campos generales.
        self.campos = {}

        datos = [
            ("Codigo:", "codigo"),
            ("Nombre:", "nombre"),
            ("Descripcion:", "descripcion"),
            ("Tarifa ($):", "tarifa"),
            ("Cantidad de equipos:", "cantidad"),
            ("Duracion (dias / horas):", "duracion"),
            ("Dato adicional:", "adicional")
        ]

        for fila, (etiqueta, clave) in enumerate(datos, start=1):

            tk.Label(
                formulario,
                text=etiqueta,
                font=("Arial", 10)
            ).grid(row=fila, column=0, padx=10, pady=6, sticky="w")

            entrada = tk.Entry(formulario, width=33)
            entrada.grid(row=fila, column=1, padx=10, pady=6)

            self.campos[clave] = entrada

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

    def Registrar_Servicio(self):

        try:

            # Se obtienen los datos del formulario.
            tipo = self.tipo_servicio.get()

            codigo = self.campos["codigo"].get().strip()
            nombre = self.campos["nombre"].get().strip()
            descripcion = self.campos["descripcion"].get().strip()

            tarifa = float(self.campos["tarifa"].get())
            duracion = float(self.campos["duracion"].get())

            adicional = self.campos["adicional"].get().strip()

            # Se verifica que los campos generales esten completos.
            if not all([tipo, codigo, nombre, descripcion]):
                raise ErrorServicio(
                    "Debe completar todos los campos obligatorios."
                )

            if any(s.codigo == codigo for s in self.servicios_registrados):
                raise ErrorServicio(
                    "Ya existe un servicio registrado con ese codigo."
                )

            # Se crea el objeto segun el tipo de servicio.
            if tipo == "Alquiler de equipos":

                cantidad = int(self.campos["cantidad"].get())

                servicio = AlquilerEquipos(
                    codigo,
                    nombre,
                    descripcion,
                    tarifa,
                    cantidad,
                    int(duracion)
                )

            elif tipo == "Asesoria":

                servicio = Asesoria(
                    codigo,
                    nombre,
                    descripcion,
                    tarifa,
                    duracion,
                    adicional.capitalize()
                )

            elif tipo == "Reserva de salas":

                capacidad = int(adicional)

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

            messagebox.showinfo(
                "Registro exitoso",
                "El servicio fue registrado correctamente.\n\n"
                f"Costo total: ${servicio.Calcular_Costo():,.2f}"
            )

            self.Limpiar_Campos()

        except (ValueError, ErrorServicio) as error:

            messagebox.showerror(
                "Error de registro",
                str(error)
            )

    # ---------------------------------------------------------------------------------------
    #       METODO PARA CONSULTAR SERVICIOS
    # ---------------------------------------------------------------------------------------

    def Consultar_Servicio(self):

        seleccion = self.lista_servicios.curselection()

        if not seleccion:

            messagebox.showwarning(
                "Seleccion requerida",
                "Seleccione un servicio de la lista."
            )

            return

        # Se obtiene el servicio seleccionado.
        indice = seleccion[0]
        servicio = self.servicios_registrados[indice]

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
            entrada.delete(0, tk.END)
