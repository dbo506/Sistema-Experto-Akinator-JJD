#lang racket

(require "conocimiento.scm")
(require "reglas.scm")
(require "preguntas.scm")

(provide conocimiento-expandido
         calcular-hechos-base
         calcular-hechos-totales
         puntuar-candidatos
         ordenar-candidatos
         score-maximo
         confianza
         candidatos-activos-hechos
         siguiente-pregunta
         explicacion)

;; 1. Inicialización y pre-cálculo
;; Expandimos los hechos de todos los candidatos con las reglas para
;; no tener que hacerlo repetidamente durante la inferencia.
(define conocimiento-expandido
  (map (lambda (entidad)
         (let ([hechos (obtener-caracteristicas entidad)])
           (cons entidad (aplicar-reglas hechos))))
       (obtener-entidades)))

;; 2. Lógica de Puntuación
;; Convierte el historial de respuestas ((caracteristica . valor) ...) en hechos booleanos
;; Umbral: > 0.5 es 'si', < -0.5 es 'no'
(define (calcular-hechos-base respuestas)
  (foldr (lambda (resp acc)
           (let ([F (car resp)]
                 [val (cdr resp)])
             (cond
               [(>= val 0.5) (cons (list F 'si) acc)]
               [(<= val -0.5) (cons (list F 'no) acc)]
               [else acc])))
           '()
           respuestas))

;; Aplica las reglas a los hechos base deducidos de las respuestas
(define (calcular-hechos-totales respuestas)
  (aplicar-reglas (calcular-hechos-base respuestas)))

;; Evalúa a un solo candidato contra el perfil del usuario (respuestas + reglas)
(define (score-candidato candidato-hechos respuestas hechos-totales)
  ;; match con respuestas directas
  (define score-respuestas
    (foldl (lambda (resp acc)
             (let* ([F (car resp)]
                    [val (cdr resp)]
                    [hecho-cand (assoc F candidato-hechos)])
               (if hecho-cand
                   (let ([cand-val (cadr hecho-cand)])
                     (+ acc (* val (if (eq? cand-val 'si) 1.0 -1.0))))
                   acc)))
           0.0
           respuestas))
           
  ;; match con características inferidas
  (define score-inferidos
    (foldl (lambda (hecho acc)
             (let* ([F (car hecho)]
                    [val-inf (cadr hecho)]
                    [ya-respondido? (assoc F respuestas)])
               (if ya-respondido?
                   acc
                   (let ([hecho-cand (assoc F candidato-hechos)])
                     (if (and hecho-cand (eq? (cadr hecho-cand) val-inf))
                         (+ acc 1.0)
                         (- acc 1.0)))))) ; penalizamos si no cumple el hecho derivado
           0.0
           hechos-totales))
           
  (+ score-respuestas score-inferidos))

;; Puntúa todos los candidatos
(define (puntuar-candidatos respuestas)
  (let ([hechos-totales (calcular-hechos-totales respuestas)])
    (map (lambda (cand)
           (let ([nombre (car cand)]
                 [hechos (cdr cand)])
             (cons nombre (score-candidato hechos respuestas hechos-totales))))
         conocimiento-expandido)))

;; Ordena puntuaciones de mayor a menor
(define (ordenar-candidatos puntuaciones)
  (sort puntuaciones (lambda (a b) (> (cdr a) (cdr b)))))

;; Calcula la confianza de un puntaje dado
(define (score-maximo respuestas)
  (let ([hechos-totales (calcular-hechos-totales respuestas)])
    (define max-resp
      (foldl (lambda (resp acc) (+ acc (abs (cdr resp)))) 0.0 respuestas))
    (define max-inf
      (foldl (lambda (hecho acc)
               (if (assoc (car hecho) respuestas)
                   acc
                   (+ acc 1.0)))
             0.0
             hechos-totales))
    (if (= 0.0 (+ max-resp max-inf))
        1.0 ; evitar division por 0 para la confianza
        (+ max-resp max-inf))))

(define (confianza mejor-score respuestas)
  (let ([maximo (score-maximo respuestas)])
    (max 0.0 (min 1.0 (/ mejor-score maximo)))))

;; Obtiene los hechos de los candidatos que compiten fuertemente
(define (candidatos-activos-hechos puntuaciones-ordenadas)
  (define mejor-score (if (null? puntuaciones-ordenadas) 0.0 (cdr (car puntuaciones-ordenadas))))
  ;; Aumentamos el umbral a 4.5 para ser más tolerantes a errores del usuario
  ;; (permite sobrevivir hasta a 2 respuestas totalmente erróneas).
  (define umbral (- mejor-score 4.5)) 
  (define activos (filter (lambda (p) (>= (cdr p) umbral)) puntuaciones-ordenadas))
  (map (lambda (act)
         (cdr (assoc (car act) conocimiento-expandido)))
       activos))

;; Obtiene la siguiente mejor pregunta
(define (siguiente-pregunta respuestas)
  (define puntuaciones (ordenar-candidatos (puntuar-candidatos respuestas)))
  (define mejor-score (if (null? puntuaciones) 0.0 (cdr (first puntuaciones))))
  (define segundo-score (if (> (length puntuaciones) 1) (cdr (second puntuaciones)) -9999.0))
  
  ;; Condición de finalización:
  ;; Si el líder le saca una ventaja irremontable al segundo lugar (>= 4.5 puntos)
  ;; o si ya hemos hecho muchas preguntas (ej. 20), forzamos el resultado.
  (if (or (>= (- mejor-score segundo-score) 4.5)
          (>= (length respuestas) 20))
      #f
      (let ([activos-hechos (candidatos-activos-hechos puntuaciones)])
        (define preguntas-hechas (map car respuestas))
        (seleccionar-pregunta activos-hechos preguntas-hechas))))

;; Justifica la predicción
(define (explicacion nombre-candidato respuestas)
  (define hechos-totales (calcular-hechos-totales respuestas))
  (define hechos-cand (cdr (assoc nombre-candidato conocimiento-expandido)))
  
  (define influencias-respuestas
    (filter-map (lambda (resp)
                  (let* ([F (car resp)]
                         [val (cdr resp)]
                         [hecho-cand (assoc F hechos-cand)])
                    (if (and hecho-cand (> (abs val) 0.0))
                        (let ([cand-val (cadr hecho-cand)])
                          ;; si el candidato tiene el valor correcto según la respuesta
                          (if (eq? cand-val (if (> val 0) 'si 'no))
                              (format "~a (~a)" F cand-val)
                              #f))
                        #f)))
                respuestas))
                
  (define influencias-reglas
    (filter-map (lambda (hecho)
                  (let ([F (car hecho)]
                        [val-inf (cadr hecho)])
                    (if (assoc F respuestas)
                        #f
                        (let ([hecho-cand (assoc F hechos-cand)])
                          (if (and hecho-cand (eq? (cadr hecho-cand) val-inf))
                              (format "~a (derivado)" F)
                              #f)))))
                hechos-totales))
                
  (string-append "El personaje coincide fuertemente en las respuestas explícitas: "
                 (if (null? influencias-respuestas) "Ninguna" (string-join influencias-respuestas ", "))
                 ". Además, cumple con características deducidas por reglas: "
                 (if (null? influencias-reglas) "Ninguna" (string-join influencias-reglas ", "))))


;; ----------------- PRUEBAS DEL MOTOR -----------------
(module+ test
  (require rackunit)

  ;; Respuestas simuladas para Keylor Navas
  (define respuestas-test '((portero . 1.0) (jugo-europa . 1.0) (delantero . -1.0)))
  
  ;; Comprobar el orden de candidatos
  (define puntuaciones (ordenar-candidatos (puntuar-candidatos respuestas-test)))
  (define mejor-candidato (car (car puntuaciones)))
  
  (check-equal? mejor-candidato 'keylor-navas)
  
  ;; Comprobar confianza
  (define conf (confianza (cdr (car puntuaciones)) respuestas-test))
  (check-true (> conf 0.8))

  ;; Comprobar selección dinámica de preguntas
  (define proxima (siguiente-pregunta respuestas-test))
  (check-not-false proxima)
  (check-false (member proxima (map car respuestas-test)))
  
  (displayln "Pruebas del motor ejecutadas exitosamente.")
)