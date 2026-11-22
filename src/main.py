
# NOMBRES:  BEATRIZ HELENA LEGRO LOAIZA
#           DIANA CATALINA LOPERA FRANCO
#           LUISA MARIA RAMOS HERNANDEZ
# GRUPO: 213023-161
# CURSO: PROGRAMACIÓN - 1604 - 2026 - UNAD
# FASE 4: COMPONENTE PRÁCTICO
# EJERCICIO 1: Sistema Integral de Gestión de Clientes, Servicios y Reservas - Software_FJ
# CÓDIGO FUENTE: AUTORÍA PROPIA


# ===========================================================================================
#                       LIBRERÍAS
# ===========================================================================================

# Se importa Tkinter para crear la ventana principal del sistema.
import tkinter as tk

# Se importa la función que muestra el inicio de sesión.
from inicio.inicio_sesion import Abrir_Ventana_Inicio_Sesion
# Se importa la función que muestra las reservas.
from reservas.interfaz import PanelReservas
# Se importa la función que muestra la interfaz de clientes.
from clientes.interfaz import Abrir_Ventana_Clientes
# Se importa la interfaz del modulo de servicios.
from servicios.interfaz import InterfazServicios

# ===========================================================================================
#                       PROGRAMA PRINCIPAL
# ===========================================================================================

# Clase encargada de iniciar el sistema y coordinar el programa.
class Programa_SoftwareFJ:

    # Se inicializa el programa y se abre la ventana principal.
    def __init__(self):
        self.ventana_principal = None
        self.clientes = []
        self.servicios = []
        self.reservas = []


# ---------------------------------------------------------------------------------------
#       MÉTODO PARA ABRIR LA VENTANA PRINCIPAL
# ---------------------------------------------------------------------------------------

# Recibe la ventana de inicio de sesión.
# Se crea una nueva ventana después de cerrar el inicio de sesión.

    def Abrir_Ventana_Principal_Software_FJ(self):

        self.ventana_principal = tk.Tk()

        # Se configura el título y el tamaño de la ventana.
        self.ventana_principal.title("Software FJ")
        self.ventana_principal.geometry("800x500")
        self.ventana_principal.resizable(False, False)

        # Se crea el título principal de la aplicación.
        tk.Label(
            self.ventana_principal,
            text="Software FJ",
            font=("Arial", 22, "bold"),
            fg="blue"
        ).pack(pady=(30, 10))

        # Se crea el subtítulo de la aplicación.
        tk.Label(
            self.ventana_principal,
            text="Sistema Integral de Gestión de Clientes, Servicios y Reservas",
            font=("Arial", 14)
        ).pack(pady=10)

        # Se crea el botón para abrir la interfaz de clientes.
        tk.Button(
            self.ventana_principal,
            text="Clientes",
            font=("Arial", 12, "bold"),
            bg="blue",
            fg="white",
            width=25,
            command=self.Abrir_Interfaz_Clientes
        ).pack(pady=10)

        # Se crea el botón para abrir la interfaz de servicios.
        tk.Button(
            self.ventana_principal,
            text="Gestionar Servicios",
            font=("Arial", 12, "bold"),
            bg="green",
            fg="white",
            width=25,
            command=self.Abrir_Modulo_Servicios
        ).pack(pady=10)

        # Se crea el botón para abrir la interfaz de reservas.
        tk.Button(
            self.ventana_principal,
            text="Gestionar Reservas",
            font=("Arial", 12, "bold"),
            bg="orange",
            fg="white",
            width=25,
            command=self.Abrir_Modulo_Reservas
        ).pack(pady=10)

        # Se mantiene activa la ventana principal.
        self.ventana_principal.mainloop()


# ---------------------------------------------------------------------------------------
#       MÉTODO PARA ABRIR EL MÓDULO DE SERVICIOS
# ---------------------------------------------------------------------------------------

# Se abre la interfaz de servicios usando la lista compartida del programa.

    def Abrir_Modulo_Servicios(self):
        InterfazServicios(self.ventana_principal, self.servicios)

# ---------------------------------------------------------------------------------------
#       MÉTODO PARA ABRIR EL MÓDULO DE CLIENTES
# ---------------------------------------------------------------------------------------

# Se comparte la lista de clientes y reservas con la interfaz de clientes.

    def Abrir_Interfaz_Clientes(self):
        Abrir_Ventana_Clientes(
            self.ventana_principal,
            self.clientes,
            self.reservas,
        )

# ---------------------------------------------------------------------------------------
#       MÉTODO PARA ABRIR EL MÓDULO DE RESERVAS
# ---------------------------------------------------------------------------------------

# Se crea una ventana secundaria y se comparten las listas necesarias.

    def Abrir_Modulo_Reservas(self):
        ventana_reservas = tk.Toplevel(self.ventana_principal)
        ventana_reservas.title("Gestión de Reservas - Software FJ")
        ventana_reservas.geometry("900x600")

        panel_reservas = PanelReservas(
            ventana_reservas,
            self.clientes,
            self.servicios,
            self.reservas,
        )
        panel_reservas.pack(fill="both", expand=True)


# ---------------------------------------------------------------------------------------
#       MÉTODO PARA INICIAR EL PROGRAMA
# ---------------------------------------------------------------------------------------

# Se muestra primero el inicio de sesión.
# Si las credenciales son correctas, se abre la ventana principal.

    def Ejecutar(self):

        inicio_exitoso = Abrir_Ventana_Inicio_Sesion()

        if inicio_exitoso:
            self.Abrir_Ventana_Principal_Software_FJ()


# ===========================================================================================
#                       EJECUCIÓN DEL PROGRAMA
# ===========================================================================================

# Se crea el programa y se ejecuta.
if __name__ == "__main__":

    programa = Programa_SoftwareFJ()
    programa.Ejecutar()
