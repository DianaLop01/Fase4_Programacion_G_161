"""Pruebas de validación de servicios y campos obligatorios."""

import unittest
from unittest.mock import patch

from servicios.alquiler_equipos import AlquilerEquipos
from servicios.asesoria import Asesoria
from servicios.excepciones import DatosServicioInvalidos, ErrorServicio
from servicios.interfaz import InterfazServicios
from servicios.reserva_salas import ReservaSalas
from clientes.interfaz import InterfazClientes
from reservas.interfaz import PanelReservas


class ValidacionServiciosTests(unittest.TestCase):
    """Comprueba que cada servicio valide sus parámetros específicos."""

    class EntradaFalsa:
        def __init__(self, valor):
            self.valor = valor
            self.opciones = {}

        def get(self):
            return self.valor

        def current(self):
            return 0 if self.valor else -1

        def delete(self, _inicio, _fin):
            self.valor = ""

        def configure(self, **opciones):
            self.opciones.update(opciones)

    class EtiquetaFalsa:
        def __init__(self, text=""):
            self.opciones = {"text": text}

        def config(self, **opciones):
            self.opciones.update(opciones)

        def cget(self, opcion):
            return self.opciones[opcion]

    class VariableFalsa:
        def __init__(self, valor):
            self.valor = valor

        def get(self):
            return self.valor

    def test_servicios_validos_conservan_su_comportamiento(self):
        servicios = (
            ReservaSalas("S1", "Sala", "Sala de reuniones", 100, 1.5, 10),
            AlquilerEquipos("E1", "Equipo", "Proyector", 50, 2, 3),
            Asesoria("A1", "Asesoría", "Consultoría", 120, 1.5, "Virtual"),
        )

        self.assertEqual(
            [servicio.Calcular_Costo() for servicio in servicios],
            [150, 300, 180],
        )

    def test_parametros_numericos_invalidos_generan_error_de_dominio(self):
        casos = (
            (
                "horas de sala",
                lambda: ReservaSalas("S1", "Sala", "Descripción", 100, "dos", 10),
            ),
            (
                "capacidad de sala",
                lambda: ReservaSalas("S1", "Sala", "Descripción", 100, 2, True),
            ),
            (
                "cantidad de equipos",
                lambda: AlquilerEquipos(
                    "E1", "Equipo", "Descripción", 100, "dos", 1
                ),
            ),
            (
                "días de alquiler",
                lambda: AlquilerEquipos("E1", "Equipo", "Descripción", 100, 2, 1.5),
            ),
            (
                "horas de asesoría",
                lambda: Asesoria("A1", "Asesoría", "Descripción", 100, "dos", "Virtual"),
            ),
            (
                "tarifa no finita",
                lambda: Asesoria(
                    "A1", "Asesoría", "Descripción", float("inf"), 2, "Virtual"
                ),
            ),
            (
                "modalidad inválida",
                lambda: Asesoria(
                    "A1", "Asesoría", "Descripción", 100, 2, None
                ),
            ),
        )

        for nombre, crear_servicio in casos:
            with self.subTest(parametro=nombre):
                with self.assertRaises(DatosServicioInvalidos):
                    crear_servicio()

    def test_textos_obligatorios_se_validan_antes_de_guardarse(self):
        with self.assertRaises(DatosServicioInvalidos):
            ReservaSalas("", "Sala", "Descripción", 100, 2, 10)

        with self.assertRaises(DatosServicioInvalidos):
            ReservaSalas("S1", "Sala", "Descripción", "cien", 2, 10)

    def test_campos_numericos_invalidos_muestran_error_en_espanol(self):
        with self.assertRaisesRegex(ErrorServicio, "Tarifa") as tarifa_error:
            InterfazServicios._convertir_decimal("SADD", "Tarifa")
        self.assertIsInstance(tarifa_error.exception.__cause__, ValueError)

        with self.assertRaisesRegex(ErrorServicio, "Duración"):
            InterfazServicios._convertir_decimal("SADD", "Duración")

        with self.assertRaisesRegex(ErrorServicio, "Cantidad de equipos"):
            InterfazServicios._convertir_entero("dos", "Cantidad de equipos")

    def test_error_de_registro_se_muestra_en_la_interfaz_y_conserva_datos(self):
        interfaz = InterfazServicios.__new__(InterfazServicios)
        interfaz.tipo_servicio = self.EntradaFalsa("Alquiler de equipos")
        interfaz.campos = {
            "codigo": self.EntradaFalsa("SADD"),
            "nombre": self.EntradaFalsa("Equipo"),
            "descripcion": self.EntradaFalsa("Descripción"),
            "tarifa": self.EntradaFalsa("SADD"),
            "duracion": self.EntradaFalsa("2"),
            "cantidad": self.EntradaFalsa("1"),
            "adicional": self.EntradaFalsa(""),
        }
        interfaz.etiquetas_campos = {
            clave: self.EtiquetaFalsa(text=f"{clave} *")
            for clave in interfaz.campos
        }
        interfaz.lbl_tipo_servicio = self.EtiquetaFalsa(
            text="Tipo de servicio *:"
        )
        interfaz.servicios_registrados = []
        interfaz.lbl_resultado = self.EtiquetaFalsa()

        with patch("servicios.interfaz.messagebox.showerror") as popup:
            interfaz.Registrar_Servicio()

        self.assertIn("Tarifa", interfaz.lbl_resultado.cget("text"))
        self.assertEqual(interfaz.lbl_resultado.cget("fg"), "red")
        self.assertEqual(interfaz.campos["tarifa"].get(), "SADD")
        self.assertEqual(
            interfaz.etiquetas_campos["tarifa"].cget("fg"),
            "red",
        )
        popup.assert_not_called()

    def test_campos_condicionales_de_servicios_se_identifican(self):
        interfaz = InterfazServicios.__new__(InterfazServicios)
        interfaz.tipo_servicio = self.EntradaFalsa("Asesoria")
        claves = (
            "codigo",
            "nombre",
            "descripcion",
            "tarifa",
            "cantidad",
            "duracion",
            "adicional",
        )
        interfaz.campos = {
            clave: self.EntradaFalsa("") for clave in claves
        }
        interfaz.etiquetas_campos = {
            clave: self.EtiquetaFalsa() for clave in claves
        }
        interfaz.lbl_tipo_servicio = self.EtiquetaFalsa()
        interfaz._actualizar_campos_servicio()

        self.assertEqual(
            interfaz.etiquetas_campos["adicional"].cget("text"),
            "Modalidad *",
        )
        self.assertIn(
            "no aplica",
            interfaz.etiquetas_campos["cantidad"].cget("text"),
        )
        self.assertEqual(
            interfaz.campos["cantidad"].opciones["state"],
            "disabled",
        )

    def test_campos_requeridos_de_servicio_vacios_se_resaltan(self):
        interfaz = InterfazServicios.__new__(InterfazServicios)
        interfaz.tipo_servicio = self.EntradaFalsa("Alquiler de equipos")
        claves = (
            "codigo",
            "nombre",
            "descripcion",
            "tarifa",
            "cantidad",
            "duracion",
            "adicional",
        )
        interfaz.campos = {
            clave: self.EntradaFalsa("") for clave in claves
        }
        interfaz.etiquetas_campos = {
            clave: self.EtiquetaFalsa(text=f"{clave} *")
            for clave in claves
        }
        interfaz.lbl_tipo_servicio = self.EtiquetaFalsa(
            text="Tipo de servicio *:"
        )
        interfaz.servicios_registrados = []
        interfaz.lbl_resultado = self.EtiquetaFalsa()

        interfaz.Registrar_Servicio()

        self.assertEqual(
            interfaz.etiquetas_campos["codigo"].cget("fg"),
            "red",
        )
        self.assertEqual(
            interfaz.etiquetas_campos["cantidad"].cget("fg"),
            "red",
        )
        self.assertEqual(
            interfaz.etiquetas_campos["adicional"].cget("fg"),
            "black",
        )
        self.assertIn(
            "obligatorios",
            interfaz.lbl_resultado.cget("text"),
        )

    def test_campos_obligatorios_vacios_de_cliente_se_resaltan(self):
        cliente_ui = InterfazClientes.__new__(InterfazClientes)
        valores = {
            "tipo_documento": "Cédula de ciudadanía",
            "documento": "",
            "primer_nombre": "Ana",
            "primer_apellido": "Pérez",
            "telefono": "3001234567",
            "correo_electronico": "ana@example.com",
            "pais_residencia": "Colombia",
            "departamento": "Cundinamarca",
            "ciudad_municipio": "Bogotá",
            "direccion": "Calle 1",
            "anio_nacimiento": "1990",
            "mes_nacimiento": "01",
            "dia_nacimiento": "01",
            "genero": "Otro",
        }
        for clave, valor in valores.items():
            setattr(cliente_ui, clave, self.VariableFalsa(valor))

        cliente_ui.etiquetas_requeridas = {
            clave: self.EtiquetaFalsa(text=f"{clave} *:")
            for clave in (
                "tipo_documento",
                "documento",
                "primer_nombre",
                "primer_apellido",
                "fecha_nacimiento",
                "anio_nacimiento",
                "mes_nacimiento",
                "dia_nacimiento",
                "genero",
                "telefono",
                "correo_electronico",
                "pais_residencia",
                "departamento",
                "ciudad_municipio",
                "direccion",
            )
        }
        cliente_ui.entradas_requeridas = {
            clave: self.EntradaFalsa("")
            for clave in (
                "tipo_documento",
                "documento",
                "primer_nombre",
                "primer_apellido",
                "anio_nacimiento",
                "mes_nacimiento",
                "dia_nacimiento",
                "telefono",
                "correo_electronico",
                "pais_residencia",
                "departamento",
                "ciudad_municipio",
                "direccion",
            )
        }
        cliente_ui.lbl_resultado = self.EtiquetaFalsa()

        self.assertFalse(cliente_ui._Validar_Campos_Obligatorios())
        self.assertEqual(
            cliente_ui.etiquetas_requeridas["documento"].cget("fg"),
            "red",
        )
        self.assertEqual(
            cliente_ui.entradas_requeridas["documento"].opciones["bg"],
            "#ffe6e6",
        )
        self.assertIn(
            "documento",
            cliente_ui.lbl_resultado.cget("text").lower(),
        )

    def test_campos_obligatorios_vacios_de_reserva_se_resaltan(self):
        reserva_ui = PanelReservas.__new__(PanelReservas)
        claves = ("id", "cliente", "servicio", "duracion", "descuento")
        reserva_ui.etiquetas_campos = {
            clave: self.EtiquetaFalsa(text=f"{clave} *:")
            for clave in claves
        }
        reserva_ui.campos_reserva = {
            clave: self.EntradaFalsa("")
            for clave in claves
        }
        reserva_ui.ent_id = reserva_ui.campos_reserva["id"]
        reserva_ui.cmb_cliente = reserva_ui.campos_reserva["cliente"]
        reserva_ui.cmb_servicio = reserva_ui.campos_reserva["servicio"]
        reserva_ui.ent_duracion = reserva_ui.campos_reserva["duracion"]
        reserva_ui.ent_descuento = reserva_ui.campos_reserva["descuento"]
        reserva_ui.lbl_resultado = self.EtiquetaFalsa()
        reserva_ui.reservas = []
        reserva_ui.actualizar_datos = lambda: None

        reserva_ui.crear_y_procesar_reserva()

        self.assertEqual(
            reserva_ui.etiquetas_campos["id"].cget("fg"),
            "red",
        )
        self.assertEqual(
            reserva_ui.campos_reserva["duracion"].opciones["bg"],
            "#ffe6e6",
        )
        self.assertIn(
            "obligatorios",
            reserva_ui.lbl_resultado.cget("text"),
        )


if __name__ == "__main__":
    unittest.main()
