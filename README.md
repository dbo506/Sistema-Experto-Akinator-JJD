# Ticonator - Sistema Experto

**Ticonator** es un sistema experto basado en inteligencia artificial estructurado al estilo del clásico juego "Akinator". Su objetivo es adivinar en qué jugador de fútbol (especialmente leyendas y seleccionados de Costa Rica) estás pensando, a través de una serie de preguntas de deducción lógica.

El proyecto está diseñado con una arquitectura dividida en un motor de inferencia lógico desarrollado en **Racket (Scheme)** y una interfaz gráfica de usuario moderna construida en **Python (Tkinter)**.

---

## Arquitectura y Tecnologías

El sistema sigue un patrón de diseño donde el motor de lógica (backend) y la interfaz (frontend) están desacoplados y se comunican en tiempo real mediante tuberías de entrada/salida (stdin/stdout) usando JSON.

### Backend (Motor Lógico)
* **Lenguaje:** Racket / Scheme.
* **Componentes:**
  * `conocimiento.scm`: Base de conocimientos donde se definen los jugadores y sus atributos base (ej. portero, mediocampista).
  * `reglas.scm`: Base de reglas de deducción (encadenamiento hacia adelante) para inferir atributos derivados basados en los iniciales (Asunción de Mundo Cerrado).
  * `preguntas.scm`: Sistema heurístico (basado en entropía) que selecciona inteligentemente la mejor pregunta posible para dividir y descartar la mayor cantidad de candidatos activos.
  * `motor.scm`: Núcleo de inferencia que evalúa puntajes, penaliza faltas de características y decide en qué momento la confianza es suficiente para emitir una respuesta.

### Frontend (Interfaz Gráfica)
* **Lenguaje:** Python 3.
* **Librerías:** `tkinter` (para ventanas nativas), `Pillow` (para procesamiento y manipulación de imágenes circulares), y `subprocess` (para orquestar la comunicación con Scheme).
* **Características:**
  * Diseño fluido adaptado con los colores patrios de Costa Rica (Azul, Blanco, Rojo).
  * Fotografías dinámicas del estado mental de Akinator.
  * Cuadrícula interactiva y dinámica (Grid) con todos los jugadores disponibles para adivinar.
  * Registro visual en vivo del historial de preguntas respondidas durante la partida.

---

## Requisitos de Instalación

Para poder ejecutar el juego en tu computadora, debes tener instalados los siguientes entornos:

1. **Python 3.x:** Para la interfaz gráfica.
2. **Pillow (Python Image Library):** Para manejar imágenes.
   ```bash
   pip install Pillow
   ```
3. **Racket:** Entorno de ejecución necesario para el backend lógico en Scheme. Debes tener `racket` disponible en las variables de entorno de tu sistema (PATH).

---

## ¿Cómo Jugar?

1. Clona o descarga este repositorio en tu computadora.
2. Abre tu terminal o consola de comandos en la carpeta raíz del proyecto.
3. Ejecuta el archivo principal:
   ```bash
   python main.py
   ```
4. **Piensa en uno de los 30 jugadores** que aparecen en la cuadrícula inferior.
5. **Responde las preguntas** ("Sí", "Probablemente", "No sé", "Probablemente no", "No").
6. ¡Deja que Ticonator utilice su motor de lógica y adivine en quién estás pensando!

---

## Funcionamiento del Sistema Experto

Este no es un árbol binario de decisiones simple. Ticonator evalúa a los 30 personajes con cada respuesta utilizando un **sistema de puntuación**:

1. **Puntajes Directos:** Cada respuesta de usuario suma o resta 1.0 punto a los candidatos dependiendo de si cumplen o no la característica preguntada. Se utiliza *Closed World Assumption* (si no tiene el atributo, se da por hecho que es "no").
2. **Encadenamiento hacia adelante:** Respuestas concretas activan reglas lógicas (ej. si el usuario indica que "es defensor", se infiere que pertenece al "área defensiva").
3. **Puntajes Inferidos:** Los jugadores son recompensados o penalizados extra en base a estos hechos derivados.
4. **Descarte Inteligente:** El motor descarta automáticamente a los jugadores que se alejen por más de `2.0` puntos del candidato líder para optimizar y acortar la cantidad de preguntas realizadas.

---

## Autor y Licencia
Desarrollado como proyecto de Sistema Experto de deducción lógica por Joel Montiel Dura, Daniel Badilla Olivas y Jose Carlos Rodriguez Varela
