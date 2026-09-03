import json
import subprocess
from pathlib import Path


class ComunicacionScheme:
    """
    Maneja la comunicación entre Python y el servidor Scheme.

    Python envía mensajes JSON por stdin.
    Scheme responde mensajes JSON por stdout.
    """

    def __init__(self):
        # Ubicación principal del proyecto
        ruta_proyecto = Path(__file__).resolve().parent.parent

        # Servidor Scheme que creamos en el paso anterior
        self.motor_scheme = ruta_proyecto / "backend" / "servidor.scm"

        self.proceso = None

    def iniciar_servidor(self):
        """Inicia el proceso de Scheme."""

        if self.proceso is not None:
            return

        self.proceso = subprocess.Popen(
            ["racket", str(self.motor_scheme)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            bufsize=1
        )

    def enviar(self, mensaje):
        """
        Envía un mensaje JSON a Scheme y devuelve su respuesta.
        """

        if self.proceso is None:
            self.iniciar_servidor()

        texto = json.dumps(mensaje)

        self.proceso.stdin.write(texto + "\n")
        self.proceso.stdin.flush()

        respuesta = self.proceso.stdout.readline()

        if not respuesta:
            error = self.proceso.stderr.read()
            raise RuntimeError(
                "Scheme no devolvió una respuesta."
                + (f"\nError: {error}" if error else "")
            )

        return json.loads(respuesta)

    def iniciar(self):
        """Inicia una nueva partida."""

        return self.enviar({
            "accion": "iniciar"
        })

    def responder(self, valor):
        """
        Envía la respuesta del usuario.

        Valores esperados:
        1.0  = Sí
        -1.0 = No
        0.0  = No sé
        0.7  = Probablemente
        -0.7 = Probablemente no
        """

        return self.enviar({
            "accion": "responder",
            "valor": valor
        })

    def cerrar(self):
        """Cierra correctamente el proceso Scheme."""

        if self.proceso is not None:
            try:
                self.proceso.stdin.close()
            except Exception:
                pass

            self.proceso.terminate()
            self.proceso.wait()

            self.proceso = None