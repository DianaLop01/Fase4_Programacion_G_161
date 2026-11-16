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

# ===========================================================================================
#                       PROGRAMA PRINCIPAL
# ===========================================================================================

# Clase encargada de iniciar el sistema y coordinar el programa.
class Programa_SoftwareFJ:

# Se inicializa el programa y se abre la ventana principal.
    def __init__(self):
        self.ventana_principal = None


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
        tk.Label(self.ventana_principal,
            text = "Software FJ",
            font = ("arial", 22, "bold"),
            fg = "blue").pack(pady = (30, 10))

# Se crea el subtítulo de la aplicación.
        tk.Label(self.ventana_principal,
            text = "Sistema Integral de Gestión de Clientes, Servicios y Reservas",
            font = ("arial", 14)).pack(pady = 10)

# Aquí se integrarán las opciones para gestionar clientes, servicios y reservas.

# Se mantiene activa la nueva ventana principal.
        self.ventana_principal.mainloop()


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