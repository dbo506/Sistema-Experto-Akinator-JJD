import tkinter as tk
from tkinter import ttk
from pathlib import Path

from PIL import Image, ImageTk

from frontend.comunicacion_scheme import ComunicacionScheme


class InterfazAkinator:

    def __init__(self, root):
        self.root = root

        self.root.title("Ticonator - Sistema Experto")
        self.root.geometry("1100x720")
        self.root.minsize(950, 650)

        self.scheme = ComunicacionScheme()

        self.pregunta_actual = None
        self.numero_pregunta = 0
        self.historial = []
        self.partida_activa = True
        self.explicacion_actual = ""
        self.foto_resultado = None

        self.crear_interfaz()

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.cerrar
        )

        self.iniciar_partida()

    # ==========================================================
    # INTERFAZ PRINCIPAL
    # ==========================================================

    def crear_interfaz(self):

        # ------------------------------------------------------
        # FONDO PRINCIPAL
        # ------------------------------------------------------

        self.root.configure(bg="#f4f6fb")

        # ------------------------------------------------------
        # ENCABEZADO
        # ------------------------------------------------------

        encabezado = tk.Frame(
            self.root,
            bg="#20243a",
            height=90
        )

        encabezado.pack(fill="x")
        encabezado.pack_propagate(False)

        titulo = tk.Label(
            encabezado,
            text="🧞 AKINATOR",
            font=("Arial", 28, "bold"),
            fg="white",
            bg="#20243a"
        )

        titulo.pack(pady=(15, 0))

        subtitulo = tk.Label(
            encabezado,
            text="Sistema Experto Basado en Reglas",
            font=("Arial", 11),
            fg="#d8dbea",
            bg="#20243a"
        )

        subtitulo.pack()

        # ------------------------------------------------------
        # CONTENEDOR PRINCIPAL
        # ------------------------------------------------------

        contenido = tk.Frame(
            self.root,
            bg="#f4f6fb"
        )

        contenido.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=25
        )

        # ------------------------------------------------------
        # PANEL IZQUIERDO
        # ------------------------------------------------------

        panel_izquierdo = tk.Frame(
            contenido,
            bg="#20243a",
            width=250
        )

        panel_izquierdo.pack(
            side="left",
            fill="y",
            padx=(0, 20)
        )

        panel_izquierdo.pack_propagate(False)

        titulo_akinator = tk.Label(
            panel_izquierdo,
            text="🧞",
            font=("Arial", 75),
            fg="white",
            bg="#20243a"
        )

        titulo_akinator.pack(
            pady=(35, 10)
        )

        texto_akinator = tk.Label(
            panel_izquierdo,
            text="Estoy pensando...",
            font=("Arial", 16, "bold"),
            fg="white",
            bg="#20243a"
        )

        texto_akinator.pack()

        texto_info = tk.Label(
            panel_izquierdo,
            text=(
                "Responde las preguntas\n"
                "para descubrir qué\n"
                "jugador estás pensando."
            ),
            font=("Arial", 11),
            fg="#d8dbea",
            bg="#20243a",
            justify="center"
        )

        texto_info.pack(
            pady=20
        )

        # ------------------------------------------------------
        # PANEL DERECHO
        # ------------------------------------------------------

        panel_derecho = tk.Frame(
            contenido,
            bg="#f4f6fb"
        )

        panel_derecho.pack(
            side="left",
            fill="both",
            expand=True
        )

        # ------------------------------------------------------
        # INFORMACIÓN DE PARTIDA
        # ------------------------------------------------------

        informacion = tk.Frame(
            panel_derecho,
            bg="#f4f6fb"
        )

        informacion.pack(
            fill="x",
            pady=(0, 8)
        )

        self.contador_label = tk.Label(
            informacion,
            text="Pregunta 0",
            font=("Arial", 11, "bold"),
            bg="#f4f6fb",
            fg="#20243a"
        )

        self.contador_label.pack(
            side="left"
        )

        self.candidatos_label = tk.Label(
            informacion,
            text="Sistema experto activo",
            font=("Arial", 10),
            bg="#f4f6fb",
            fg="#666666"
        )

        self.candidatos_label.pack(
            side="right"
        )

        # ------------------------------------------------------
        # BARRA DE PROGRESO
        # ------------------------------------------------------

        self.progreso = ttk.Progressbar(
            panel_derecho,
            orient="horizontal",
            mode="determinate",
            maximum=20
        )

        self.progreso.pack(
            fill="x",
            pady=(0, 20)
        )

        # ------------------------------------------------------
        # TARJETA DE PREGUNTA
        # ------------------------------------------------------

        tarjeta = tk.Frame(
            panel_derecho,
            bg="white",
            bd=1,
            relief="solid"
        )

        tarjeta.pack(
            fill="x"
        )

        titulo_pregunta = tk.Label(
            tarjeta,
            text="PREGUNTA",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#666666"
        )

        titulo_pregunta.pack(
            pady=(25, 5)
        )

        self.imagen_resultado_label = tk.Label(
            tarjeta,
            bg="white"
        )

        self.imagen_resultado_label.pack(
            pady=(10, 0)
        )

        self.pregunta_label = tk.Label(
            tarjeta,
            text="Conectando con Scheme...",
            font=("Arial", 23, "bold"),
            bg="white",
            fg="#20243a",
            wraplength=650,
            justify="center"
        )

        self.pregunta_label.pack(
            fill="x",
            padx=40,
            pady=(10, 20)
        )   

        # ------------------------------------------------------
        # BOTONES DE RESPUESTA
        # ------------------------------------------------------

        self.botones_frame = tk.Frame(
            panel_derecho,
            bg="#f4f6fb"
        )

        self.botones_frame.pack(
            fill="x",
            pady=(20, 10)
        )

        self.boton_si = self.crear_boton(
            self.botones_frame,
            "✓  Sí",
            1.0
        )

        self.boton_prob_si = self.crear_boton(
            self.botones_frame,
            "≈  Probablemente",
            0.7
        )

        self.boton_no_se = self.crear_boton(
            self.botones_frame,
            "?  No sé",
            0.0
        )

        self.boton_prob_no = self.crear_boton(
            self.botones_frame,
            "≈  Probablemente no",
            -0.7
        )

        self.boton_no = self.crear_boton(
            self.botones_frame,
            "✕  No",
            -1.0
        )

        # ------------------------------------------------------
        # PANEL DE HISTORIAL
        # ------------------------------------------------------

        self.historial_frame = tk.Frame(
            panel_derecho,
            bg="white",
            bd=1,
            relief="solid"
        )

        self.historial_frame.pack(
            fill="x",
            pady=(5, 0)
        )

        historial_titulo = tk.Label(
            self.historial_frame,
            text="Historial de respuestas",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#20243a"
        )

        historial_titulo.pack(
            anchor="w",
            padx=15,
            pady=(8, 3)
        )

        self.historial_label = tk.Label(
            self.historial_frame,
            text="Todavía no hay respuestas.",
            font=("Arial", 9),
            bg="white",
            fg="#777777",
            justify="left",
            anchor="w",
            wraplength=700
        )

        self.historial_label.pack(
            fill="x",
            padx=15,
            pady=(0, 10)
        )

    # ==========================================================
    # CREAR BOTÓN
    # ==========================================================

    def crear_boton(self, padre, texto, valor):

        boton = tk.Button(
            padre,
            text=texto,
            font=("Arial", 10, "bold"),
            command=lambda: self.responder(valor),
            relief="flat",
            bd=0,
            padx=8,
            pady=12,
            cursor="hand2"
        )

        boton.pack(
            side="left",
            padx=4,
            expand=True,
            fill="x"
        )

        return boton

    # ==========================================================
    # CARGAR IMAGEN DEL JUGADOR
    # ==========================================================

    def cargar_imagen_jugador(self, jugador):

        carpeta_imagenes = (
            Path(__file__).resolve().parent / "imagenes"
        )

        extensiones = [".jpg", ".jpeg", ".png"]

        for extension in extensiones:

            ruta_imagen = carpeta_imagenes / f"{jugador}{extension}"

            if ruta_imagen.exists():

                imagen = Image.open(ruta_imagen)

                imagen.thumbnail((260, 260))

                self.foto_resultado = ImageTk.PhotoImage(imagen)

                self.imagen_resultado_label.config(
                    image=self.foto_resultado
                )

                return

        # Si no existe la imagen, dejamos el espacio vacío.
        self.foto_resultado = None

        self.imagen_resultado_label.config(
            image=""
        )

    # ==========================================================
    # INICIAR PARTIDA
    # ==========================================================

    def iniciar_partida(self):

        try:

            respuesta = self.scheme.iniciar()

            if respuesta.get("tipo") == "pregunta":
                self.mostrar_pregunta(respuesta)

            else:
                self.mostrar_error(respuesta)

        except Exception as error:

            self.mostrar_error({
                "mensaje": str(error)
            })

    # ==========================================================
    # RESPONDER
    # ==========================================================

    def responder(self, valor):

        if not self.partida_activa:
            return

        self.deshabilitar_botones()

        try:

            respuesta = self.scheme.responder(valor)

            self.historial.append({
                "pregunta": self.pregunta_actual,
                "respuesta": valor
            })

            self.actualizar_historial()

            if respuesta.get("tipo") == "pregunta":

                self.mostrar_pregunta(respuesta)

            elif respuesta.get("tipo") == "resultado":

                self.mostrar_resultado(respuesta)

            else:

                self.mostrar_error(respuesta)

        except Exception as error:

            self.mostrar_error({
                "mensaje": str(error)
            })

    # ==========================================================
    # MOSTRAR PREGUNTA
    # ==========================================================

    def mostrar_pregunta(self, datos):

        self.partida_activa = True

        self.pregunta_actual = datos.get(
            "pregunta",
            "Pregunta desconocida"
        )

        self.numero_pregunta += 1

        texto = self.pregunta_actual.replace(
            "-",
            " "
        )

        texto = texto.capitalize()

        self.pregunta_label.config(
            text=f"¿La persona cumple con:\n\n{texto}?",
            font=("Arial", 23, "bold")
        )

        self.contador_label.config(
            text=f"Pregunta {self.numero_pregunta}"
        )

        self.progreso["value"] = self.numero_pregunta

        confianza = datos.get("confianza")

        if confianza is not None:

            self.candidatos_label.config(
                text=f"Confianza actual: {confianza:.0%}"
            )

        else:

            self.candidatos_label.config(
                text="Sistema experto activo"
            )

        self.habilitar_botones()

    # ==========================================================
    # MOSTRAR RESULTADO
    # ==========================================================

    def mostrar_resultado(self, datos):

        print(">>> ESTOY EN mostrar_resultado()")
        
        self.partida_activa = False

        jugador = datos.get(
            "jugador",
            "Desconocido"
        )

        self.cargar_imagen_jugador(jugador)

        confianza = datos.get(
            "confianza",
            0
        )

        explicacion = datos.get(
            "explicacion",
            "No se recibió explicación."
        )

        self.deshabilitar_botones()

        # ------------------------------------------------------
        # INFORMACIÓN SUPERIOR
        # ------------------------------------------------------

        self.contador_label.config(
            text=f"Preguntas realizadas: {self.numero_pregunta}"
        )

        self.candidatos_label.config(
            text="🎯 Predicción realizada"
        )

        # ------------------------------------------------------
        # RESULTADO
        # ------------------------------------------------------

        nombre_mostrado = jugador.replace(
            "-",
            " "
        ).title()

        texto_resultado = (
            "🎯 ¡Creo que lo tengo!\n\n"
            f"{nombre_mostrado}\n\n"
            f"Confianza: {confianza:.1%}\n\n"
            "¿Acerté?"
        )

        self.pregunta_label.config(
            text=texto_resultado,
            font=("Arial", 23, "bold")
        )

        # ------------------------------------------------------
        # EXPLICACIÓN
        # ------------------------------------------------------

        self.explicacion_actual = explicacion

        self.historial_label.config(
            text=(
                "💡 ¿Por qué elegí este jugador?\n\n"
                f"{explicacion}"
            ),
            justify="left",
            wraplength=700
        )

        # ------------------------------------------------------
        # BOTONES DEL RESULTADO
        # ------------------------------------------------------

        self.mostrar_botones_resultado()

    # ==========================================================
    # BOTONES DEL RESULTADO
    # ==========================================================

    def mostrar_botones_resultado(self):

        if hasattr(self, "resultado_frame"):

            self.resultado_frame.destroy()

        self.resultado_frame = tk.Frame(
            self.botones_frame.master,
            bg="#f4f6fb"
        )

        self.resultado_frame.pack(
            fill="x",
            pady=(20, 10),
            before=self.historial_frame
        )

        self.botones_frame.pack_forget()

        self.boton_correcto = tk.Button(
            self.resultado_frame,
            text="✓  ¡Correcto!",
            font=("Arial", 12, "bold"),
            command=self.prediccion_correcta,
            padx=30,
            pady=10,
            cursor="hand2"
        )

        self.boton_correcto.pack(
            side="left",
            padx=10,
            expand=True
        )

        self.boton_incorrecto = tk.Button(
            self.resultado_frame,
            text="✕  Incorrecto",
            font=("Arial", 12, "bold"),
            command=self.prediccion_incorrecta,
            padx=30,
            pady=10,
            cursor="hand2"
        )

        self.boton_incorrecto.pack(
            side="left",
            padx=10,
            expand=True
        )

        self.boton_nueva = tk.Button(
            self.resultado_frame,
            text="🔄  Nueva partida",
            font=("Arial", 12, "bold"),
            command=self.nueva_partida,
            padx=30,
            pady=10,
            cursor="hand2"
        )

        self.boton_nueva.pack(
            side="left",
            padx=10,
            expand=True
        )

    # ==========================================================
    # PREDICCIÓN CORRECTA
    # ==========================================================

    def prediccion_correcta(self):

        self.partida_activa = False

        self.pregunta_label.config(
            text=(
                "🎉 ¡Excelente!\n\n"
                "¡Ticonator acertó!\n\n"
                "Gracias por jugar."
            )
        )

        self.candidatos_label.config(
            text="Partida completada ✓"
        )

        self.deshabilitar_botones()

        self.historial_label.config(
            text=(
                "🎉 Resultado confirmado.\n\n"
                "Ticonator acertó el jugador."
            )
        )

    # ==========================================================
    # PREDICCIÓN INCORRECTA
    # ==========================================================

    def prediccion_incorrecta(self):

        self.partida_activa = False

        self.pregunta_label.config(
            text=(
                "😅 ¡Fallé!\n\n"
                "Esta vez no pude adivinarlo.\n\n"
                "Puedes comenzar una nueva partida."
            )
        )

        self.candidatos_label.config(
            text="Partida completada ✕"
        )

        self.deshabilitar_botones()

        self.historial_label.config(
            text=(
                "❌ Resultado incorrecto.\n\n"
                "Puedes iniciar una nueva partida."
            )
        )

    # ==========================================================
    # NUEVA PARTIDA
    # ==========================================================

    def nueva_partida(self):

        # ------------------------------------------------------
        # ELIMINAR BOTONES DEL RESULTADO
        # ------------------------------------------------------

        if hasattr(self, "resultado_frame"):

            self.resultado_frame.destroy()
            del self.resultado_frame

        self.botones_frame.pack(
            fill="x",
            pady=(20, 10),
            before=self.historial_frame
        )

        self.numero_pregunta = 0
        self.historial = []
        self.pregunta_actual = None
        self.partida_activa = True
        self.explicacion_actual = ""

        # ------------------------------------------------------
        # RESTAURAR INTERFAZ
        # ------------------------------------------------------

        self.pregunta_label.config(
            text="Iniciando nueva partida...",
            font=("Arial", 23, "bold")
        )

        self.contador_label.config(
            text="Pregunta 0"
        )

        self.candidatos_label.config(
            text="Sistema experto activo"
        )

        self.progreso["value"] = 0

        self.historial_label.config(
            text="Todavía no hay respuestas.",
            justify="left"
        )

        # ------------------------------------------------------
        # REINICIAR CONEXIÓN CON SCHEME
        # ------------------------------------------------------

        self.scheme.cerrar()

        self.scheme = ComunicacionScheme()

        self.iniciar_partida()

    # ==========================================================
    # ACTUALIZAR HISTORIAL
    # ==========================================================

    def actualizar_historial(self):

        if not self.historial:

            self.historial_label.config(
                text="Todavía no hay respuestas."
            )

            return

        ultimas = self.historial[-5:]

        nombres = {
            1.0: "Sí",
            0.7: "Probablemente",
            0.0: "No sé",
            -0.7: "Probablemente no",
            -1.0: "No"
        }

        textos = []

        for elemento in ultimas:

            pregunta = elemento["pregunta"]

            respuesta = nombres.get(
                elemento["respuesta"],
                "Desconocida"
            )

            pregunta = pregunta.replace(
                "-",
                " "
            )

            textos.append(
                f"• {pregunta}: {respuesta}"
            )

        self.historial_label.config(
            text="\n".join(textos),
            justify="left"
        )

    # ==========================================================
    # HABILITAR BOTONES
    # ==========================================================

    def habilitar_botones(self):

        self.boton_si.config(
            state="normal"
        )

        self.boton_prob_si.config(
            state="normal"
        )

        self.boton_no_se.config(
            state="normal"
        )

        self.boton_prob_no.config(
            state="normal"
        )

        self.boton_no.config(
            state="normal"
        )

    # ==========================================================
    # DESHABILITAR BOTONES
    # ==========================================================

    def deshabilitar_botones(self):

        self.boton_si.config(
            state="disabled"
        )

        self.boton_prob_si.config(
            state="disabled"
        )

        self.boton_no_se.config(
            state="disabled"
        )

        self.boton_prob_no.config(
            state="disabled"
        )

        self.boton_no.config(
            state="disabled"
        )

    # ==========================================================
    # MOSTRAR ERROR
    # ==========================================================

    def mostrar_error(self, datos):

        mensaje = datos.get(
            "mensaje",
            "Ocurrió un error."
        )

        self.partida_activa = False

        self.pregunta_label.config(
            text=f"⚠️ Error\n\n{mensaje}"
        )

        self.candidatos_label.config(
            text="Error de comunicación"
        )

        self.deshabilitar_botones()

    # ==========================================================
    # CERRAR APLICACIÓN
    # ==========================================================

    def cerrar(self):

        self.scheme.cerrar()

        self.root.destroy()


# ==============================================================
# MAIN
# ==============================================================

def main():

    root = tk.Tk()

    Interfaz(root)

    root.mainloop()


if __name__ == "__main__":
    main()