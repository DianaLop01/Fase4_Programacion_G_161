# Inicio de sesión del programa Software FJ

# ===========================================================================================
#                       LIBRERÍAS
# ===========================================================================================

# Se importan las librerías necesarias para crear la interfaz gráfica del programa.

import tkinter as tk


# ===========================================================================================
#                        CLASE USUARIO (Contiene Usuario y Contraseña)
# ===========================================================================================

# Se crea una clase llamada Usuario con los atributos privados de Usuario y Contraseña.

class Usuario:
    def __init__(self):
        self._usuario = "SoftwareFJ"
        self._contraseña = "SoftwareFJ"

# ---------------------------------------------------------------------------------------
#       MÉTODO PARA VALIDAR LAS CREDENCIALES
# ---------------------------------------------------------------------------------------

# Se comparan las credenciales ingresadas con las almacenadas.

    def validar (self, usuario, contraseña):
        return (usuario == self._usuario and contraseña == self._contraseña)


# ===========================================================================================
#                       VENTANA DE INICIO DE SESIÓN
# ===========================================================================================

# Clase que crea y administra la ventana de inicio de sesión.
class InicioSesion(tk.Frame):

# Se recibe la ventana, el objeto Usuario y la función definida en main.py
    def __init__(self, ventana, usuario):
        super().__init__(ventana)

# Se almacenan los objetos y la función que se utilizarán en la interfaz de Tkinter.
        self.ventana = ventana
        self.usuario = usuario

# Se indica si las credenciales ingresadas son correctas o incorrectas.
        self.inicio_exitoso = False
        

# -----------------------------------------------------------------------------------
#       CAMPOS PARA INGRESAR LAS CREDENCIALES USUARIO Y CONTRASEÑA
# -----------------------------------------------------------------------------------
  
# Campos para ingresar usuario.
        tk.Label(self, 
                text = "Usuario:", 
                font = ("arial", 16), 
                fg = "blue").pack()
        self.txt_Usuario = tk.Entry(self)
        self.txt_Usuario.pack()

# Campos para ingresar contraseña.
        tk.Label(self, 
                text = "Contraseña:", 
                font = ("arial", 16), 
                fg = "blue").pack()
        self.txt_Contraseña = tk.Entry(self, show = "*")
        self.txt_Contraseña.pack()


# -----------------------------------------------------------------------------------
#       MENSAJE DE RESULTADO Y BOTÓN DE ACCESO
# -----------------------------------------------------------------------------------

# Etiqueta utilizada para mostrar el resultado del inicio de sesión.
        self.lbl_resultado = tk.Label(self, text = "")
        self.lbl_resultado.pack()

# Botón para iniciar sesión
        tk.Button(self, 
              text = "Iniciar Sesión", 
              command = self.Iniciar_Sesion).pack (pady = 10)


# ---------------------------------------------------------------------------------------
#       MÉTODO PARA VALIDAR LAS CREDENCIALES
# ---------------------------------------------------------------------------------------

# Se validan el usuario y la contraseña ingresados.

    def Iniciar_Sesion(self):
        if self.usuario.validar(self.txt_Usuario.get(), self.txt_Contraseña.get()):
            self.inicio_exitoso = True
            
            self.lbl_resultado.config(text = "Inicio de sesión exitoso!", 
                                      font = ("arial", 13), 
                                      fg = "green")

            # Espera 2 segundos y se destruye la ventana de inicio de sesión.
            self.ventana.after(2000, self.ventana.destroy)
        else:
            self.lbl_resultado.config(text = "Usuario o contraseña incorrectos!", 
                                      font = ("arial", 13), 
                                      fg = "red")


# ===========================================================================================
#                       FUNCIÓN PARA INICIAR EL LOGIN
# ===========================================================================================

# Función que crea la ventana y muestra el inicio de sesión.

def Abrir_Ventana_Inicio_Sesion():

# Se crea un objeto de la clase Usuario.
    usuario = Usuario()


# ---------------------------------------------------------------------------------------
#       CONFIGURACIÓN DE LA VENTANA PRINCIPAL DE TKINTER
# ---------------------------------------------------------------------------------------

# Se crea y configura la ventana de inicio de sesión.
    ventana = tk.Tk()
    ventana.title("Software FJ")
    ventana.geometry("300x220")


# ---------------------------------------------------------------------------------------
#       CREACIÓN DE LA INTERFAZ DE INICIO DE SESIÓN
# ---------------------------------------------------------------------------------------

# Se crea y configura la interfaz de inicio de sesión.
    inicio_sesion = InicioSesion(ventana, usuario)
    inicio_sesion.pack(fill = "both", expand = True)


# ---------------------------------------------------------------------------------------
#       EJECUCIÓN DE LA INTERFAZ
# ---------------------------------------------------------------------------------------

# Se mantiene activa la interfaz gráfica.
    ventana.mainloop()

# Se devuelve el resultado del inicio de sesión.
    return inicio_sesion.inicio_exitoso