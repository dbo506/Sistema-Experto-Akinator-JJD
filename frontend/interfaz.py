import tkinter as tk
from tkinter import ttk
from pathlib import Path

from PIL import Image, ImageTk

from frontend.comunicacion_scheme import ComunicacionScheme


class InterfazAkinator:

    def __init__(self, root):
        self.root = root

        self.root.title("Ticonator - Sistema Experto")
        ancho = min(1100, self.root.winfo_screenwidth() - 80)
        alto = min(720, self.root.winfo_screenheight() - 100)
        self.root.geometry(f"{ancho}x{alto}")
        self.root.minsize(850, 600)

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

        self.root.configure(bg="#FFFFFF")

        # ------------------------------------------------------
        # ENCABEZADO
        # ------------------------------------------------------

        encabezado = tk.Frame(
            self.root,
            bg="#0032A0",
            height=90
        )

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(2, weight=1)
        encabezado.grid(row=0, column=0, sticky="ew")
        encabezado.pack_propagate(False)

        titulo = tk.Label(
            encabezado,
            text="TICONATOR",
            font=("Segoe UI", 28, "bold"),
            fg="white",
            bg="#0032A0"
        )

        titulo.pack(pady=(15, 0))

      



        # ------------------------------------------------------
        # CONTENEDOR PRINCIPAL
        # ------------------------------------------------------

        contenido = tk.Frame(
            self.root,
            bg="#FFFFFF"
        )

                # ------------------------------------------------------
        # PANEL INFERIOR (LISTA DE JUGADORES Y HISTORIAL)
        # ------------------------------------------------------
        panel_inferior = tk.Frame(self.root, bg="#FFFFFF")
        panel_inferior.grid(row=2, column=0, sticky="nsew", pady=(0, 10), padx=20)
        
        self.historial_frame = tk.Frame(
            panel_inferior,
            bg="#f4f6fb",
            bd=0,
            width=250
        )
        self.historial_frame.pack(side="left", fill="y", padx=(0, 20))
        self.historial_frame.pack_propagate(False)

        historial_titulo = tk.Label(
            self.historial_frame,
            text="Historial de respuestas",
            font=("Segoe UI", 10, "bold"),
            bg="#f4f6fb",
            fg="#0032A0"
        )
        historial_titulo.pack(anchor="w", padx=15, pady=(8, 3))

        self.historial_label = tk.Label(
            self.historial_frame,
            text="Todavía no hay respuestas.",
            font=("Segoe UI", 9),
            bg="#f4f6fb",
            fg="#333333",
            justify="left",
            anchor="w",
            wraplength=220
        )
        self.historial_label.pack(fill="x", padx=15, pady=(0, 10))

        # Contenedor de la cuadricula de jugadores
        jugadores_panel = tk.Frame(panel_inferior, bg="#FFFFFF")
        jugadores_panel.pack(side="left", fill="both", expand=True)
        jugadores_canvas = tk.Canvas(
            jugadores_panel, bg="#FFFFFF", highlightthickness=0,
            width=1, height=100
        )
        scroll_jugadores = ttk.Scrollbar(
            jugadores_panel, orient="vertical", command=jugadores_canvas.yview
        )
        scroll_jugadores.pack(side="right", fill="y")
        jugadores_canvas.pack(side="left", fill="both", expand=True)
        jugadores_canvas.configure(yscrollcommand=scroll_jugadores.set)
        grid_container = tk.Frame(jugadores_canvas, bg="#FFFFFF")
        ventana_jugadores = jugadores_canvas.create_window(
            (0, 0), window=grid_container, anchor="nw"
        )
        cuadros_jugadores = []

        def ajustar_jugadores(event):
            jugadores_canvas.itemconfigure(ventana_jugadores, width=event.width)
            columnas = max(1, event.width // 116)
            for idx, cuadro in enumerate(cuadros_jugadores):
                cuadro.grid(row=idx // columnas, column=idx % columnas)

        def desplazar_jugadores(event):
            if jugadores_canvas.bbox("all")[3] > jugadores_canvas.winfo_height():
                paso = -1 if event.delta > 0 or event.num == 4 else 1
                jugadores_canvas.yview_scroll(paso, "units")
            return "break"

        jugadores_canvas.bind("<Configure>", ajustar_jugadores)
        grid_container.bind(
            "<Configure>",
            lambda event: jugadores_canvas.configure(
                scrollregion=jugadores_canvas.bbox("all")
            )
        )

        # Cargar jugadores y hacer circulos
        def make_circle_image(img_path, size=(70, 70)):
            from PIL import Image, ImageDraw
            try:
                img = Image.open(img_path).convert("RGBA")
            except:
                img = Image.new("RGBA", size, (200,200,200,255))
            
            min_dim = min(img.size)
            left = (img.width - min_dim)/2
            top = (img.height - min_dim)/2
            img = img.crop((left, top, left+min_dim, top+min_dim))
            img = img.resize(size, Image.Resampling.LANCZOS)
            
            mask = Image.new('L', size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0) + size, fill=255)
            
            result = Image.new('RGBA', size, (255, 255, 255, 0))
            result.paste(img, (0, 0), mask=mask)
            return result

        self.fotos_inferior = []
        try:
            import re
            ruta_conocimiento = Path(__file__).resolve().parent.parent / "backend" / "conocimiento.scm"
            cont_scm = ruta_conocimiento.read_text(encoding="utf-8")
            matches = re.findall(r"\'([a-z-]+)\n\s+\'(portero|defensor|mediocampista|delantero)", cont_scm)
            jugadores_ids = [m[0] for m in matches]
            ruta_img = Path(__file__).resolve().parent / "imagenes"
            
            sorted_jugadores = sorted(jugadores_ids)
            for idx, j_id in enumerate(sorted_jugadores):
                j_name = j_id.replace("-", " ").title()
                
                img_file = None
                for ext in [".jpg", ".jpeg", ".png"]:
                    p = ruta_img / f"{j_id}{ext}"
                    if p.exists():
                        img_file = p
                        break
                
                if img_file:
                    circ_img = make_circle_image(img_file, (70, 70))
                else:
                    circ_img = Image.new("RGBA", (70,70), (200,200,200,255))
                
                tk_img = ImageTk.PhotoImage(circ_img)
                self.fotos_inferior.append(tk_img)
                
                # Fila y Columna
                fila = idx // 10
                columna = idx % 10
                
                frame_j = tk.Frame(grid_container, bg="#FFFFFF")
                frame_j.grid(row=fila, column=columna, padx=8, pady=5)
                cuadros_jugadores.append(frame_j)
                
                lbl_img = tk.Label(frame_j, image=tk_img, bg="#FFFFFF")
                lbl_img.pack()
                lbl_txt = tk.Label(frame_j, text=j_name, font=("Segoe UI", 10, "bold"), bg="#FFFFFF", fg="#0032A0", wraplength=100, justify="center")
                lbl_txt.pack(pady=(3, 0))
                for widget in (frame_j, lbl_img, lbl_txt):
                    widget.bind("<MouseWheel>", desplazar_jugadores)
                    widget.bind("<Button-4>", desplazar_jugadores)
                    widget.bind("<Button-5>", desplazar_jugadores)
                
        except Exception as e:
            print("Error cargando jugadores inferiores:", e)

        jugadores_canvas.bind("<MouseWheel>", desplazar_jugadores)
        grid_container.bind("<MouseWheel>", desplazar_jugadores)

        contenido.grid(
            row=1, column=0, sticky="ew", padx=20, pady=10
        )

        # ------------------------------------------------------
        # PANEL DERECHO
        # ------------------------------------------------------

        panel_derecho = tk.Frame(
            contenido,
            bg="#FFFFFF"
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
            bg="#FFFFFF"
        )

        informacion.pack(
            fill="x",
            pady=(0, 8)
        )

        self.contador_label = tk.Label(
            informacion,
            text="Pregunta 0",
            font=("Segoe UI", 11, "bold"),
            bg="#FFFFFF",
            fg="#20243a"
        )

        self.contador_label.pack(
            side="left"
        )

        self.candidatos_label = tk.Label(
            informacion,
            text="Sistema experto activo",
            font=("Segoe UI", 10),
            bg="#FFFFFF",
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
            pady=(0, 10)
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
            font=("Segoe UI", 11, "bold"),
            bg="white",
            fg="#666666"
        )

        titulo_pregunta.pack(
            pady=(10, 5)
        )

        self.frame_imagenes = tk.Frame(tarjeta, bg="white")
        self.frame_imagenes.pack(pady=(10, 0))
        
        self.imagen_estado_akinator_label = tk.Label(
            self.frame_imagenes,
            bg="white"
        )
        self.imagen_estado_akinator_label.pack(side="left", padx=10)
        
        self.imagen_resultado_label = tk.Label(
            self.frame_imagenes,
            bg="white"
        )
        self.imagen_resultado_label.pack(side="left", padx=10)

        self.pregunta_label = tk.Label(
            tarjeta,
            text="Conectando con Scheme...",
            font=("Segoe UI", 20, "bold"),
            bg="white",
            fg="#20243a",
            wraplength=650,
            justify="center"
        )

        self.pregunta_label.pack(
            fill="x",
            padx=40,
            pady=(5, 10)
        )
        tarjeta.bind(
            "<Configure>",
            lambda event: self.pregunta_label.configure(
                wraplength=max(1, event.width - 80)
            )
        )

        # ------------------------------------------------------
        # BOTONES DE RESPUESTA
        # ------------------------------------------------------

        self.botones_frame = tk.Frame(
            panel_derecho,
            bg="#FFFFFF"
        )

        self.botones_frame.pack(
            fill="x",
            pady=(10, 5)
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

        # ==========================================================
    # CREAR BOTÓN
    # ==========================================================

    def crear_boton(self, padre, texto, valor):

        boton = tk.Button(
            padre,
            text=texto,
            font=("Segoe UI", 11, "bold"),
            bg="#0032A0",
            fg="white",
            activebackground="#002270",
            activeforeground="white",
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

                imagen.thumbnail((160, 160))

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

    def actualizar_imagen_estado(self, estado="pensando"):
        ruta_img = Path(__file__).resolve().parent / "imagenes"
        nombre_arch = "akinator_principal.png"
        
        if estado == "encontro":
            nombre_arch = "akinator_encontró.png"
        elif self.numero_pregunta == 1:
            nombre_arch = "akinator_principal.png"
        else:
            ciclo = (self.numero_pregunta - 2) % 3
            if ciclo == 0:
                nombre_arch = "akinator_pensando1.png"
            elif ciclo == 1:
                nombre_arch = "akinator_pensando2.png"
            else:
                nombre_arch = "akinator_sonriente.png"
                
        try:
            img = Image.open(ruta_img / nombre_arch)
            if estado == "encontro":
                img.thumbnail((160, 160))
            else:
                img.thumbnail((120, 120))
            self.foto_estado = ImageTk.PhotoImage(img)
            self.imagen_estado_akinator_label.config(image=self.foto_estado)
        except Exception as e:
            print("Error cargando imagen de estado:", e)

    def mostrar_pregunta(self, datos):

        self.partida_activa = True

        self.pregunta_actual = datos.get(
            "pregunta",
            "Pregunta desconocida"
        )

        self.numero_pregunta += 1
        self.actualizar_imagen_estado("pensando")


        texto = self.pregunta_actual.replace(
            "-",
            " "
        )

        texto = texto.capitalize()

        self.pregunta_label.config(
            text=f"¿La persona cumple con:\n\n{texto}?",
            font=("Segoe UI", 20, "bold")
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

        self.actualizar_imagen_estado("encontro")
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
            font=("Segoe UI", 20, "bold")
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
            bg="#FFFFFF"
        )

        self.resultado_frame.pack(
            fill="x",
            pady=(10, 5),
            
        )

        self.botones_frame.pack_forget()

        self.boton_correcto = tk.Button(
            self.resultado_frame,
            text="✓  ¡Correcto!",
            font=("Segoe UI", 12, "bold"),
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
            font=("Segoe UI", 12, "bold"),
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
            font=("Segoe UI", 12, "bold"),
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
            pady=(10, 5),
            
        )

        self.numero_pregunta = 0
        self.historial = []
        self.pregunta_actual = None
        self.partida_activa = True
        self.explicacion_actual = ""

        # ------------------------------------------------------
        # RESTAURAR INTERFAZ
        # ------------------------------------------------------

        # Limpiar la imagen mostrada
        self.foto_resultado = None
        self.imagen_resultado_label.config(image="")

        self.pregunta_label.config(
            text="Iniciando nueva partida...",
            font=("Segoe UI", 20, "bold")
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

        ultimas = self.historial[-12:]

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