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
        self.root.configure(bg="#edf2f8")
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(1, weight=1)

        # La navegación permanece visible; el historial tiene su propio scroll.
        self.historial_frame = tk.Frame(self.root, bg="#092747", width=200)
        self.historial_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.historial_frame.pack_propagate(False)
        img = Image.open(Path(__file__).resolve().parent / "imagenes" / "akinator_principal.png")
        img.thumbnail((90, 95))
        self.foto_lateral = ImageTk.PhotoImage(img)
        tk.Label(self.historial_frame, image=self.foto_lateral, bg="#092747").pack(pady=(12, 0))
        tk.Label(self.historial_frame, text="TICONATOR", font=("Segoe UI", -23, "bold"),
                 fg="white", bg="#092747").pack()
        tk.Label(self.historial_frame, text="S I S T E M A   E X P E R T O",
                 font=("Segoe UI", -8), fg="#dce8f6", bg="#092747").pack(pady=(0, 16))
        pie = tk.Frame(self.historial_frame, bg="#092747")
        pie.pack(side="bottom", fill="x", pady=16)
        tk.Label(pie, text="La Sele Nos Une", font=("Segoe Print", -16, "bold"),
                 fg="white", bg="#092747").pack()
        self.crear_bandera(pie, 78, 30).pack(pady=6)
        tk.Frame(self.historial_frame, bg="#26415e", height=1).pack(fill="x")
        tk.Label(self.historial_frame, text="◴  Historial de respuestas",
                 font=("Segoe UI", -10, "bold"), fg="white", bg="#092747").pack(pady=14)
        historial_area = tk.Frame(self.historial_frame, bg="#092747")
        historial_area.pack(fill="both", expand=True, padx=10)
        historial_canvas = tk.Canvas(historial_area, bg="#092747", highlightthickness=0, width=1)
        historial_scroll = ttk.Scrollbar(historial_area, command=historial_canvas.yview)
        historial_scroll.pack(side="right", fill="y")
        historial_canvas.pack(side="left", fill="both", expand=True)
        historial_canvas.configure(yscrollcommand=historial_scroll.set)
        self.historial_label = tk.Label(historial_canvas, text="Todavía no hay respuestas.",
            font=("Segoe UI", -9), bg="#203d5b", fg="#dce8f6", justify="left",
            anchor="nw", padx=10, pady=12, wraplength=150)
        historial_window = historial_canvas.create_window(0, 0, window=self.historial_label, anchor="nw")
        def ajustar_historial(event=None):
            ancho = max(1, historial_canvas.winfo_width())
            historial_canvas.itemconfigure(historial_window, width=ancho)
            self.historial_label.configure(wraplength=max(1, ancho - 20))
            historial_canvas.configure(scrollregion=historial_canvas.bbox("all"))
        historial_canvas.bind("<Configure>", ajustar_historial)
        self.historial_label.bind("<Configure>", ajustar_historial)
        def desplazar_historial(event):
            if self.historial_label.winfo_height() > historial_canvas.winfo_height():
                historial_canvas.yview_scroll(-1 if event.delta > 0 else 1, "units")
            return "break"
        for widget in (historial_canvas, self.historial_label):
            widget.bind("<MouseWheel>", desplazar_historial)

        # Estadio vectorial: graderías, estructura del techo y reflectores.
        encabezado = tk.Canvas(self.root, height=100, bg="#0a294b", highlightthickness=0)
        encabezado.grid(row=0, column=1, sticky="ew")
        def dibujar_estadio(event):
            w, h = event.width, event.height
            encabezado.delete("all")
            for y in range(h):
                c = int(22 + 16 * y / h)
                encabezado.create_line(0, y, w, y, fill=f"#{c//2:02x}{c+14:02x}{c+38:02x}")
            for lado in (0, 1):
                borde = w * lado
                centro = w * (0.22 if lado == 0 else 0.78)
                for j in range(6):
                    encabezado.create_line(borde, 35+j*11, centro, 85+j*4, fill="#355570")
                for j in range(8):
                    x = (12+j*19) if lado == 0 else (w-12-j*19)
                    y = 13+j*4
                    encabezado.create_line(x, y, centro, h, fill="#284762")
                    encabezado.create_oval(x-8, y-7, x+8, y+7, fill="#345977", outline="")
                    encabezado.create_oval(x-4, y-4, x+4, y+4, fill="#e5f6ff", outline="")
            encabezado.create_text(w/2, 36, text="TICONATOR", fill="white",
                                   font=("Segoe UI", -34, "bold"))
            encabezado.create_text(w/2, 78, text="F Ú T B O L   C O S T A R R I C E N S E",
                                   fill="#edf5ff", font=("Segoe UI", -10))
            for x in (w/2-212, w/2+178):
                self.dibujar_bandera(encabezado, x, 70, 34, 16)
        encabezado.bind("<Configure>", dibujar_estadio)

        contenido = tk.Frame(self.root, bg="#edf2f8")
        contenido.grid(row=1, column=1, sticky="nsew", padx=12, pady=(0, 10))
        contenido.columnconfigure(0, weight=1)
        contenido.rowconfigure(1, weight=1)
        panel_derecho = tk.Frame(contenido, bg="#ffffff", padx=10, pady=8)
        panel_derecho.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        informacion = tk.Frame(panel_derecho, bg="white")
        informacion.pack(fill="x", pady=(0, 5))
        self.contador_label = tk.Label(informacion, text="Pregunta 0",
            font=("Segoe UI", -11, "bold"), bg="white", fg="#092353")
        self.contador_label.pack(side="left")
        estado = tk.Frame(informacion, bg="#edf2f8")
        estado.pack(side="right")
        tk.Label(estado, text="●", fg="#00ba4a", bg="#edf2f8", font=("Segoe UI", -12)).pack(side="left")
        self.candidatos_label = tk.Label(estado, text="Sistema experto activo",
            font=("Segoe UI", -9), bg="#edf2f8", fg="#173965")
        self.candidatos_label.pack(side="left", padx=(0, 8))
        estilo = ttk.Style(self.root)
        estilo.theme_use("clam")
        estilo.configure("Ticonator.Horizontal.TProgressbar", background="#00b849",
                         troughcolor="#e6ebf2", borderwidth=0, lightcolor="#00b849",
                         darkcolor="#00b849")
        self.progreso = ttk.Progressbar(panel_derecho, orient="horizontal",
            mode="determinate", maximum=20, style="Ticonator.Horizontal.TProgressbar")
        self.progreso.pack(fill="x", pady=(0, 8))

        tarjeta = tk.Frame(panel_derecho, bg="white", highlightthickness=1,
                           highlightbackground="#e1e8f1", height=260)
        tarjeta.pack(fill="x")
        tarjeta.pack_propagate(False)
        tk.Label(tarjeta, text="PREGUNTA", font=("Segoe UI", -9, "bold"),
                 fg="#112f63", bg="white").pack(pady=(6, 0))
        self.frame_imagenes = tk.Frame(tarjeta, bg="white")
        self.frame_imagenes.place(relx=0.5, rely=0.5, anchor="center")
        self.imagen_estado_akinator_label = tk.Label(self.frame_imagenes, bg="white")
        self.imagen_estado_akinator_label.pack(anchor="center")
        self.imagen_resultado_label = tk.Label(self.frame_imagenes, bg="white")
        self.imagen_resultado_label.pack(anchor="center")
        pura = tk.Frame(encabezado, bg="#0a294b")
        pura.place(relx=1, x=-8, rely=1, y=-4, anchor="se")
        tk.Label(pura, text="Pura Vida", font=("Segoe Print", -10, "bold"),
                 fg="#8fa5c4", bg="#0a294b", justify="center").pack()
        self.crear_bandera(pura, 52, 24).pack(pady=3)
        self.pregunta_label = tk.Label(tarjeta, text="Conectando con Scheme...",
            font=("Segoe UI", -18, "bold"), bg="white", fg="#092353",
            wraplength=560, justify="center")
        self.pregunta_label.place(relx=0.5, rely=1, y=-4, anchor="s", relwidth=0.96)
        def ajustar_tarjeta(event=None):
            compacta = self.root.winfo_height() < 700
            tarjeta.configure(height=260 if compacta else 350)
            if self.foto_resultado is None:
                self.imagen_resultado_label.pack_forget()
                self.imagen_estado_akinator_label.pack(side="top", anchor="center", padx=0)
                self.frame_imagenes.place_configure(rely=0.5)
            else:
                self.imagen_estado_akinator_label.pack(side="left", anchor="center", padx=12)
                self.imagen_resultado_label.pack(side="left", anchor="center", padx=12)
                self.frame_imagenes.place_configure(rely=0.36)
            self.pregunta_label.configure(
                wraplength=max(1, tarjeta.winfo_width()-28),
                font=("Segoe UI", -((12 if compacta else 16) if not self.partida_activa
                      else (12 if compacta else 20)), "bold"))
        self.frame_imagenes.bind("<Configure>", ajustar_tarjeta)
        tarjeta.bind("<Configure>", ajustar_tarjeta)
        self.pregunta_label.bind("<Configure>", ajustar_tarjeta)
        self.root.bind("<Configure>", lambda event: ajustar_tarjeta() if event.widget == self.root else None)

        self.botones_frame = tk.Frame(panel_derecho, bg="white")
        self.botones_frame.pack(fill="x", pady=(8, 0))
        self.boton_si = self.crear_boton(self.botones_frame, "✓  Sí", 1.0)
        self.boton_prob_si = self.crear_boton(self.botones_frame, "≈  Probablemente", 0.7)
        self.boton_no_se = self.crear_boton(self.botones_frame, "?  No sé", 0.0)
        self.boton_prob_no = self.crear_boton(self.botones_frame, "≈  Probablemente no", -0.7)
        self.boton_no = self.crear_boton(self.botones_frame, "✕  No", -1.0)

        panel_inferior = tk.Frame(contenido, bg="white", padx=8, pady=6)
        panel_inferior.grid(row=1, column=0, sticky="nsew")
        tk.Label(panel_inferior, text="Jugadores de la Selección de Costa Rica",
                 font=("Segoe UI", -11, "bold"), fg="#092353", bg="white").pack(anchor="w", pady=(0, 6))
        jugadores_panel = tk.Frame(panel_inferior, bg="white")
        jugadores_panel.pack(fill="both", expand=True)
        jugadores_canvas = tk.Canvas(jugadores_panel, bg="#f7f9fc", highlightthickness=0, width=1, height=90)
        scroll_jugadores = ttk.Scrollbar(jugadores_panel, orient="vertical", command=jugadores_canvas.yview)
        scroll_jugadores.pack(side="right", fill="y")
        jugadores_canvas.pack(side="left", fill="both", expand=True)
        jugadores_canvas.configure(yscrollcommand=scroll_jugadores.set)
        grid_container = tk.Frame(jugadores_canvas, bg="#f7f9fc")
        ventana_jugadores = jugadores_canvas.create_window((0, 0), window=grid_container, anchor="nw")
        cuadros_jugadores = []
        def ajustar_jugadores(event):
            jugadores_canvas.itemconfigure(ventana_jugadores, width=event.width)
            columnas = max(1, event.width // 116)
            for col in range(len(cuadros_jugadores)):
                grid_container.columnconfigure(col, weight=1 if col < columnas else 0)
            for idx, cuadro in enumerate(cuadros_jugadores):
                cuadro.grid(row=idx // columnas, column=idx % columnas, sticky="n")
        def desplazar_jugadores(event):
            limites = jugadores_canvas.bbox("all")
            if limites and limites[3] > jugadores_canvas.winfo_height():
                paso = -1 if event.delta > 0 or event.num == 4 else 1
                jugadores_canvas.yview_scroll(paso, "units")
            return "break"
        jugadores_canvas.bind("<Configure>", ajustar_jugadores)
        grid_container.bind("<Configure>", lambda event: jugadores_canvas.configure(
            scrollregion=jugadores_canvas.bbox("all")))

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
                
                frame_j = tk.Frame(grid_container, bg="#FFFFFF", width=110, height=112, highlightthickness=1, highlightbackground="#e5ebf3")
                frame_j.pack_propagate(False)
                frame_j.grid(row=fila, column=columna, padx=3, pady=4)
                cuadros_jugadores.append(frame_j)
                
                lbl_img = tk.Label(frame_j, image=tk_img, bg="#FFFFFF")
                lbl_img.pack(pady=(5, 0))
                lbl_txt = tk.Label(frame_j, text=j_name, font=("Segoe UI", -9, "bold"), bg="#FFFFFF", fg="#0032A0", wraplength=100, justify="center")
                lbl_txt.pack(pady=(3, 0))
                for widget in (frame_j, lbl_img, lbl_txt):
                    widget.bind("<MouseWheel>", desplazar_jugadores)
                    widget.bind("<Button-4>", desplazar_jugadores)
                    widget.bind("<Button-5>", desplazar_jugadores)
                
        except Exception as e:
            print("Error cargando jugadores inferiores:", e)

        jugadores_canvas.bind("<MouseWheel>", desplazar_jugadores)
        grid_container.bind("<MouseWheel>", desplazar_jugadores)

    @staticmethod
    def dibujar_bandera(canvas, x, y, ancho, alto):
        # Proporción oficial de las cinco franjas: 1:1:2:1:1.
        offset = 0
        for color, unidades in (("#0032a0", 1), ("#ffffff", 1), ("#ce1126", 2),
                                ("#ffffff", 1), ("#0032a0", 1)):
            siguiente = offset + alto * unidades / 6
            canvas.create_rectangle(x, y+offset, x+ancho, y+siguiente,
                                    fill=color, outline="")
            offset = siguiente

    def crear_bandera(self, padre, ancho, alto):
        canvas = tk.Canvas(padre, width=ancho, height=alto, highlightthickness=0)
        self.dibujar_bandera(canvas, 0, 0, ancho, alto)
        return canvas

    def crear_boton(self, padre, texto, valor):

        boton = tk.Button(
            padre,
            text=texto,
            font=("Segoe UI", -12, "bold"),
            bg={1.0: "#00a644", 0.7: "#0062ed", 0.0: "#dbad19", -0.7: "#f36a20", -1.0: "#d51635"}[valor],
            fg="white",
            activebackground={1.0: "#008637", 0.7: "#004dc0", 0.0: "#bd9212", -0.7: "#cc4e12", -1.0: "#ad102b"}[valor],
            disabledforeground="#e5e9f0",
            wraplength=110,
            activeforeground="white",
            command=lambda: self.responder(valor),
            relief="flat",
            bd=0,
            padx=8,
            pady=12,
            cursor="hand2"
        )

        columna = len(padre.winfo_children()) - 1
        padre.columnconfigure(columna, weight=1, uniform="respuestas")
        boton.grid(row=0, column=columna, padx=3, sticky="nsew")
        boton.bind("<Configure>", lambda event: boton.configure(wraplength=max(1, event.width-12)))

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

                imagen.thumbnail((140, 140), Image.Resampling.LANCZOS)

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
                img.thumbnail((140, 140), Image.Resampling.LANCZOS)
            else:
                img = img.resize((round(img.width * 140 / img.height), 140), Image.Resampling.LANCZOS)
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
            font=("Segoe UI", -((12 if self.partida_activa else 12) if self.root.winfo_height() < 700 else 20), "bold")
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
            text=texto_resultado.replace("\n\n", "\n"),
            font=("Segoe UI", -((12 if self.partida_activa else 12) if self.root.winfo_height() < 700 else 20), "bold")
        )

        # ------------------------------------------------------
        # EXPLICACIÓN
        # ------------------------------------------------------

        self.explicacion_actual = explicacion

        self.actualizar_historial()

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

        # Las cinco respuestas permanecen visibles, deshabilitadas al terminar.

        self.boton_correcto = tk.Button(
            self.resultado_frame,
            text="✓  ¡Correcto!",
            font=("Segoe UI", -12, "bold"),
            command=self.prediccion_correcta,
            padx=8,
            pady=6,
            bg="#edf2f8",
            fg="#092353",
            relief="flat",
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
            font=("Segoe UI", -12, "bold"),
            command=self.prediccion_incorrecta,
            padx=8,
            pady=6,
            bg="#edf2f8",
            fg="#092353",
            relief="flat",
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
            font=("Segoe UI", -12, "bold"),
            command=self.nueva_partida,
            padx=8,
            pady=6,
            bg="#edf2f8",
            fg="#092353",
            relief="flat",
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
            font=("Segoe UI", -((12 if self.partida_activa else 12) if self.root.winfo_height() < 700 else 20), "bold")
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

        ultimas = self.historial

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

        if self.explicacion_actual:
            textos.append(
                "\n\U0001f4a1 \u00bfPor qu\u00e9 eleg\u00ed este jugador?\n\n"
                f"{self.explicacion_actual}"
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