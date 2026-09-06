import unittest
from unittest.mock import Mock, patch
from frontend.interfaz import InterfazAkinator


class EstadisticasTest(unittest.TestCase):
    def setUp(self):
        self.app = InterfazAkinator.__new__(InterfazAkinator)
        for field in ("partidas_finalizadas", "aciertos", "fallos", "total_preguntas"):
            setattr(self.app, field, 0)
        self.app.promedio_preguntas = 0.0
        self.app.partida_registrada = False
        self.app.prediccion_disponible = True
        self.app.numero_pregunta = 7
        self.app.actualizar_historial = Mock()

    def test_confirmaciones_no_duplican_y_promedio(self):
        app = self.app
        self.assertTrue(app.registrar_estadisticas(True))
        self.assertFalse(app.registrar_estadisticas(True))
        self.assertFalse(app.registrar_estadisticas(False))
        self.assertEqual((app.partidas_finalizadas, app.aciertos, app.fallos), (1, 1, 0))
        app.partida_registrada = False
        app.numero_pregunta = 8
        self.assertTrue(app.registrar_estadisticas(False))
        self.assertEqual((app.partidas_finalizadas, app.aciertos, app.fallos), (2, 1, 1))
        self.assertEqual(app.total_preguntas, 15)
        self.assertEqual(app.promedio_preguntas, 7.5)

    def test_sin_certeza_no_registra(self):
        self.app.prediccion_disponible = False
        self.assertFalse(self.app.registrar_estadisticas(True))
        self.assertFalse(self.app.registrar_estadisticas(False))
        self.assertEqual(self.app.partidas_finalizadas, 0)

    @patch("frontend.interfaz.ComunicacionScheme")
    def test_nueva_partida_conserva_estadisticas(self, scheme):
        app = self.app
        app.registrar_estadisticas(True)
        for field in ("botones_frame", "imagen_resultado_label", "pregunta_label",
                      "contador_label", "candidatos_label", "root", "scheme"):
            setattr(app, field, Mock())
        app.root.winfo_height.return_value = 600
        app.progreso = {}
        app.historial = [{"pregunta": "portero", "respuesta": 1.0}]
        app.iniciar_partida = Mock()
        app.nueva_partida()
        self.assertEqual(app.historial, [])
        self.assertEqual(app.total_preguntas, 7)
        self.assertEqual(app.partidas_finalizadas, 1)
        self.assertEqual(app.aciertos, 1)
        self.assertEqual(app.promedio_preguntas, 7)
        self.assertFalse(app.partida_registrada)
        self.assertFalse(app.prediccion_disponible)
        app.iniciar_partida.assert_called_once()


if __name__ == "__main__":
    unittest.main()
