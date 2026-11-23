"""Interfaz gráfica para las operaciones de reservas."""

from math import isfinite
import os
import sys
import tkinter as tk
from tkinter import messagebox, ttk

# Asegura que Python lea la carpeta actual (src/reservas)
ruta_actual = os.path.dirname(os.path.abspath(__file__))
if ruta_actual not in sys.path:
  sys.path.insert(0, ruta_actual)

from excepciones import (
    ErrorDatoInvalido,
    ErrorParametroFaltante,
    SoftwareFJExcepcion,
)
from reserva import Reserva 


class PanelReservas(tk.Frame):
    """Módulo de interfaz gráfica para gestionar reservas de servicios."""

    def __init__(
        self,
        parent,
        lista_clientes: list,
        lista_servicios: list,
        lista_reservas: list,
        logger=None,
    ):
        super().__init__(parent, bg="#f4f6f9")
        self.clientes = lista_clientes
        self.servicios = lista_servicios
        self.reservas = lista_reservas
        self.logger = logger

        self._construir_ui()
        self.actualizar_datos()

    def _consruir_ui(self):
        """Mantiene compatibilidad con el nombre usado por versiones anteriores."""
        self._construir_ui()

    def _construir_ui(self):
        self.etiquetas_campos = {}
        self.campos_reserva = {}
        estilo = ttk.Style(self)
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

        form = tk.LabelFrame(
            self,
            text="Gestión de reservas - SoftwareFJ",
            font=("Arial", 14, "bold"),
            bg="#f4f6f9",
            padx=12,
            pady=10,
        )
        form.pack(fill="x", padx=15, pady=10)

        self.etiquetas_campos["id"] = tk.Label(
            form, text="ID Reserva *:", bg="#f4f6f9"
        )
        self.etiquetas_campos["id"].grid(
            row=0, column=0, sticky="w", pady=4
        )
        self.ent_id = tk.Entry(form, width=15)
        self.ent_id.grid(row=0, column=1, padx=6, sticky="w")
        self.campos_reserva["id"] = self.ent_id

        self.etiquetas_campos["cliente"] = tk.Label(
            form, text="Cliente *:", bg="#f4f6f9"
        )
        self.etiquetas_campos["cliente"].grid(
            row=0, column=2, sticky="w", pady=4
        )
        self.cmb_cliente = ttk.Combobox(form, state="readonly", width=30)
        self.cmb_cliente.grid(row=0, column=3, padx=6)
        self.campos_reserva["cliente"] = self.cmb_cliente

        self.etiquetas_campos["servicio"] = tk.Label(
            form, text="Servicio *:", bg="#f4f6f9"
        )
        self.etiquetas_campos["servicio"].grid(
            row=1, column=0, sticky="w", pady=4
        )
        self.cmb_servicio = ttk.Combobox(form, state="readonly", width=30)
        self.cmb_servicio.grid(row=1, column=1, columnspan=2, padx=6, sticky="w")
        self.campos_reserva["servicio"] = self.cmb_servicio

        self.etiquetas_campos["duracion"] = tk.Label(
            form,
            text="Duración (Horas/Días/Sesiones) *:",
            bg="#f4f6f9",
        )
        self.etiquetas_campos["duracion"].grid(
            row=1, column=3, sticky="w"
        )
        self.ent_duracion = tk.Entry(form, width=12)
        self.ent_duracion.grid(row=1, column=4, padx=6, sticky="w")
        self.campos_reserva["duracion"] = self.ent_duracion

        self.etiquetas_campos["descuento"] = tk.Label(
            form, text="Descuento (%) (opcional):", bg="#f4f6f9"
        )
        self.etiquetas_campos["descuento"].grid(
            row=2, column=0, sticky="w", pady=4
        )
        self.ent_descuento = tk.Entry(form, width=12)
        self.ent_descuento.insert(0, "0")
        self.ent_descuento.grid(row=2, column=1, padx=6, sticky="w")
        self.campos_reserva["descuento"] = self.ent_descuento

        tk.Button(
            form,
            text="Crear y Procesar Reserva",
            bg="#007bff",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=10,
            command=self.crear_y_procesar_reserva,
        ).grid(row=2, column=3, columnspan=2, pady=6, sticky="e")

        tk.Label(
            form,
            text="* Campo obligatorio. El descuento es opcional.",
            bg="#f4f6f9",
            font=("Arial", 9),
        ).grid(row=3, column=0, columnspan=5, sticky="w", pady=(4, 0))

        acciones = tk.Frame(self, bg="#f4f6f9")
        acciones.pack(fill="x", padx=15, pady=5)

        tk.Button(
            acciones,
            text="Confirmar reserva",
            bg="#28a745",
            fg="white",
            padx=10,
            command=self.confirmar_reserva,
        ).pack(side="left", padx=5)

        tk.Button(
            acciones,
            text="Cancelar reserva",
            bg="#dc3545",
            fg="white",
            padx=10,
            command=self.cancelar_reserva,
        ).pack(side="left", padx=5)

        tk.Button(
            acciones,
            text="Actualizar listas",
            bg="#6c757d",
            fg="white",
            padx=10,
            command=self.actualizar_datos,
        ).pack(side="right", padx=5)

        self.lbl_resultado = tk.Label(
            self,
            text="",
            bg="#f4f6f9",
            font=("Arial", 10, "bold"),
            wraplength=850,
        )
        self.lbl_resultado.pack(fill="x", padx=15, pady=(4, 0))

        self.listbox_reservas = tk.Listbox(self, font=("consolas", 10), height=14)
        self.listbox_reservas.pack(fill="both", expand=True, padx=15, pady=10)

    def _limpiar_resaltado_campos(self):
        """Restablece los estilos de los campos después de una corrección."""
        for etiqueta in self.etiquetas_campos.values():
            etiqueta.config(fg="black")
        for clave, campo in self.campos_reserva.items():
            if clave in ("cliente", "servicio"):
                campo.configure(style="TCombobox")
            else:
                campo.configure(bg="white")

    def _resaltar_campos(self, claves):
        """Resalta las etiquetas y los controles de los campos inválidos."""
        for clave in claves:
            self.etiquetas_campos[clave].config(fg="red")
            campo = self.campos_reserva[clave]
            if clave in ("cliente", "servicio"):
                campo.configure(style="CampoInvalido.TCombobox")
            else:
                campo.configure(bg="#ffe6e6")

    def _mostrar_resultado(self, mensaje, color):
        """Muestra mensajes de validación y resultado en el panel."""
        self.lbl_resultado.config(text=mensaje, fg=color)

    @staticmethod
    def _formatear_reserva(reserva_objeto):
        """Convierte los datos de una reserva en una línea legible para la lista."""
        detalles = reserva_objeto.obtener_detalles()
        if isinstance(detalles, dict):
            identificador = detalles.get("identificador", "-")
            cliente = detalles.get("cliente", "-")
            servicio = detalles.get("servicio", "-")
            duracion = detalles.get("duracion", "-")
            estado = detalles.get("estado", "-")
            costo = detalles.get("costo_total", 0)
            try:
                costo_formateado = f"${float(costo):,.2f}"
            except (TypeError, ValueError):
                costo_formateado = "$0.00"
            return (
                f"{identificador} | Cliente: {cliente} | Servicio: {servicio} | "
                f"Duración: {duracion} | Estado: {estado} | Total: {costo_formateado}"
            )
        return str(detalles)

    def actualizar_datos(self):
        """Refresca los desplegables de clientes y servicios y la lista de reservas."""
        cliente_actual = self.cmb_cliente.get()
        servicio_actual = self.cmb_servicio.get()

        valores_clientes = [
            f"{c.identificador} - {c.nombre}" for c in self.clientes
        ]
        valores_servicios = [
            f"{s.codigo} - {s.nombre}" for s in self.servicios
        ]
        self.cmb_cliente["values"] = valores_clientes
        self.cmb_servicio["values"] = valores_servicios

        if cliente_actual in valores_clientes:
            self.cmb_cliente.set(cliente_actual)
        elif valores_clientes:
            self.cmb_cliente.current(0)
        else:
            self.cmb_cliente.set("")

        if servicio_actual in valores_servicios:
            self.cmb_servicio.set(servicio_actual)
        elif valores_servicios:
            self.cmb_servicio.current(0)
        else:
            self.cmb_servicio.set("")

        seleccion = self.listbox_reservas.curselection()
        indice_actual = seleccion[0] if seleccion else None
        self.listbox_reservas.delete(0, tk.END)
        for res in self.reservas:
            self.listbox_reservas.insert(tk.END, res.obtener_detalles())

    def crear_y_procesar_reserva(self):
        creada = False
        campo_actual = None
        self._limpiar_resaltado_campos()
        try:
            faltantes = []
            if not self.ent_id.get().strip():
                faltantes.append("id")
            if self.cmb_cliente.current() < 0:
                faltantes.append("cliente")
            if self.cmb_servicio.current() < 0:
                faltantes.append("servicio")
            if not self.ent_duracion.get().strip():
                faltantes.append("duracion")

            if faltantes:
                self._resaltar_campos(faltantes)
                raise ErrorParametroFaltante(
                    "Complete los campos obligatorios marcados con asterisco."
                )

            cliente = self.clientes[self.cmb_cliente.current()]
            servicio = self.servicios[self.cmb_servicio.current()]

            campo_actual = "duracion"
            try:
                duracion = int(self.ent_duracion.get())
            except (TypeError, ValueError) as error:
                raise ErrorDatoInvalido(
                    "La duración debe ser un número entero válido."
                ) from error
            if duracion <= 0:
                raise ErrorDatoInvalido(
                    "La duración debe ser mayor que cero."
                )

            texto_descuento = self.ent_descuento.get().strip()
            campo_actual = "descuento"
            try:
                descuento = (
                    float(texto_descuento) if texto_descuento else 0.0
                )
            except (TypeError, ValueError) as error:
                raise ErrorDatoInvalido(
                    "El descuento debe ser un número válido."
                ) from error
            if not isfinite(descuento) or not 0 <= descuento < 100:
                raise ErrorDatoInvalido(
                    "El descuento debe estar entre 0 y menos de 100."
                )

            campo_actual = None
            nueva_reserva = Reserva(
                identificador=self.ent_id.get().strip(),
                cliente=cliente,
                servicio=servicio,
                duracion=duracion,
                descuento=descuento,
                logger=self.logger,
            )
            nueva_reserva.procesar()
            self.reservas.append(nueva_reserva)
            creada = True

            self._mostrar_resultado(
                f"Reserva {nueva_reserva.identificador} creada y procesada. "
                f"Total: ${nueva_reserva.costo_total:,.2f}",
                "green",
            )
            self.ent_id.delete(0, tk.END)
            self.ent_duracion.delete(0, tk.END)
            self.ent_descuento.delete(0, tk.END)
            self.ent_descuento.insert(0, "0")

        except SoftwareFJExcepcion as e:
            if campo_actual:
                self._resaltar_campos([campo_actual])
            self._mostrar_resultado(str(e), "red")
        except (TypeError, ValueError, AttributeError) as e:
            if campo_actual:
                self._resaltar_campos([campo_actual])
            self._mostrar_resultado(str(e), "red")
        except Exception as e:
            self._mostrar_resultado(str(e), "red")
        finally:
            self.actualizar_datos()
            if creada:
                ultimo = len(self.reservas) - 1
                self.listbox_reservas.selection_clear(0, tk.END)
                self.listbox_reservas.selection_set(ultimo)
                self.listbox_reservas.activate(ultimo)

    def confirmar_reserva(self):
        seleccion = self.listbox_reservas.curselection()
        if not seleccion:
            self._mostrar_resultado(
                "Seleccione una reserva de la lista.",
                "red",
            )
            return

        try:
            reserva_seleccionada = self.reservas[seleccion[0]]
            reserva_seleccionada.confirmar()
            messagebox.showinfo(
                "Confirmada",
                f"La reserva {reserva_seleccionada.identificador} ha sido confirmada exitosamente.",
            )
        except SoftwareFJExcepcion as e:
            messagebox.showerror("Operación no permitida", str(e))
        except (IndexError, AttributeError, TypeError):
            messagebox.showerror("Operación no permitida", "La reserva seleccionada ya no está disponible.")
        except Exception as e:
            messagebox.showerror("Operación no permitida", str(e))
        finally:
            self.actualizar_datos()

    def cancelar_reserva(self):
        seleccion = self.listbox_reservas.curselection()
        if not seleccion:
            self._mostrar_resultado(
                "Seleccione una reserva de la lista.",
                "red",
            )
            return

        try:
            reserva_seleccionada = self.reservas[seleccion[0]]
            reserva_seleccionada.cancelar()
            messagebox.showinfo(
                "Cancelada",
                f"La reserva {reserva_seleccionada.identificador} ha sido cancelada exitosamente.",
            )
        except SoftwareFJExcepcion as e:
            messagebox.showerror("Operación no permitida", str(e))
        except (IndexError, AttributeError, TypeError):
            messagebox.showerror("Operación no permitida", "La reserva seleccionada ya no está disponible.")
        except Exception as e:
            messagebox.showerror("Operación no permitida", str(e))
        finally:
            self.actualizar_datos()


# BLOQUE DE PRUEBA DE LA INTERFAZ GRÁFICA
if __name__ == "__main__":
    # Objetos simulados (mocks) para probar la interfaz antes de unirla con la de mis compañeras
    class clienteMock:
        def __init__(self, identificador, nombre):
            self.identificador = identificador
            self.nombre = nombre

    class servicioMock:
        def __init__(self, identificador, nombre, tarifa):
            self.identificador = identificador
            self.nombre = nombre
            self.tarifa = tarifa

        def calcular_costo(self, cantidad: int, descuento: float = 0.0) -> float:
            if cantidad < 0:
                raise ErrorDatoInvalido("La duración debe ser mayor o igual que cero.")
            if descuento < 0 or descuento >= 100:
                raise ErrorDatoInvalido("El descuento debe estar entre 0 y 100.")
            return (self.tarifa * cantidad) * (1 - descuento / 100)

    root = tk.Tk()
    root.title("Prueba Modulo de Reservas - SoftwareFJ")
    root.geometry("800x500")

    clientes_prueba = [
        clienteMock("C-01", "Beatriz Legro"),
        clienteMock("C-02", "Marina Loaiza"),
    ]
    servicios_prueba = [
        servicioMock("S-01", "Sala ejecutiva", 50000),
        servicioMock("S-02", "Equipo VR", 35000),
    ]
    reserva_lista = []

    panel = PanelReservas(root, clientes_prueba, servicios_prueba, reserva_lista)
    panel.pack(fill="both", expand=True)
    root.mainloop()
