#lang racket

(require json
         "motor.scm")

;; Estado actual de la partida
(define respuestas '())
(define pregunta-actual #f)

;; Convierte un símbolo de Racket a texto
(define (simbolo->string valor)
  (if (symbol? valor)
      (symbol->string valor)
      (format "~a" valor)))

;; Envía una respuesta JSON
(define (enviar datos)
  (displayln (jsexpr->string datos))
  (flush-output))

;; Inicia una nueva partida
(define (iniciar)
  (set! respuestas '())
  (set! pregunta-actual (siguiente-pregunta respuestas))

  (enviar
   (hash
    'tipo "pregunta"
    'pregunta (simbolo->string pregunta-actual))))

;; Procesa una respuesta
(define (responder valor)
  (if (not pregunta-actual)
      (enviar
       (resultado-final respuestas))

      (let* ([nuevas-respuestas
              (cons (cons pregunta-actual valor) respuestas)]

             [puntuaciones
              (ordenar-candidatos
               (puntuar-candidatos nuevas-respuestas))]

             [mejor
              (car puntuaciones)]

             [nombre
              (car mejor)]

             [score
              (cdr mejor)]

             [conf
              (confianza score nuevas-respuestas)]

             [nueva-pregunta
              (siguiente-pregunta nuevas-respuestas)])

        ;; Actualizamos el estado
        (set! respuestas nuevas-respuestas)
        (set! pregunta-actual nueva-pregunta)

        (if nueva-pregunta
            (enviar
             (hash
              'tipo "pregunta"
              'pregunta (simbolo->string nueva-pregunta)
              'confianza conf))

            (enviar (resultado-final nuevas-respuestas))))))

;; Procesa una línea recibida
(define (procesar-linea linea)
  (with-handlers
      ([exn:fail?
        (lambda (e)
          (enviar
           (hash
            'tipo "error"
            'mensaje (exn-message e))))])

    (define mensaje
      (string->jsexpr linea))

    (define accion
      (hash-ref mensaje 'accion))

    (cond
      [(equal? accion "iniciar")
       (iniciar)]

      [(equal? accion "responder")
       (define valor
         (hash-ref mensaje 'valor))
       (responder valor)]

      [else
       (enviar
        (hash
         'tipo "error"
         'mensaje "Acción desconocida"))])))

;; Servidor principal
(let loop ()
  (define linea (read-line))

  (unless (eof-object? linea)
    (unless (string=? (string-trim linea) "")
      (procesar-linea linea))
    (loop)))