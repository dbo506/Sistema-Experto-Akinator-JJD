#lang racket
(require rackunit rackunit/text-ui json racket/runtime-path
         "../backend/motor.scm")
(define (valor-perfil nombre pregunta)
  (if (equal? (assoc pregunta (cdr (assoc nombre conocimiento-expandido)))
              (list pregunta 'si)) 1.0 -1.0))
(define (simular nombre [intensidad 1.0])
  (let loop ([respuestas '()])
    (define pregunta (siguiente-pregunta respuestas))
    (if pregunta
        (loop (cons (cons pregunta (* intensidad (valor-perfil nombre pregunta))) respuestas))
        respuestas)))
(define-runtime-path servidor "../backend/servidor.scm")
(define casos
  (test-suite
   "Requisitos funcionales del motor"
   (test-case "1. Keylor Navas: identificacion correcta con pocas preguntas"
     (define respuestas (simular 'keylor-navas))
     (check-true (<= (length respuestas) 10))
     (check-equal? (hash-ref (resultado-final respuestas) 'jugador) "keylor-navas"))
   (test-case "2. Perfiles similares: pregunta discriminante antes de predecir"
     (let loop ([respuestas '()])
       (define pregunta (siguiente-pregunta respuestas))
       (check-not-false pregunta)
       (define medford (valor-perfil 'hernan-medford pregunta))
       (define gomez (valor-perfil 'ronald-gomez pregunta))
       (if (= medford gomez)
           (loop (cons (cons pregunta medford) respuestas))
           (begin
             (check-equal? (hash-ref (resultado-final respuestas) 'tipo) "sin_certeza")
             (check-not-equal? medford gomez)))))
   (test-case "3. No se: no cambia puntuaciones ni elimina candidatos"
     (define pregunta (siguiente-pregunta '()))
     (define respuestas (list (cons pregunta 0.0)))
     (check-equal? (puntuar-candidatos respuestas) (puntuar-candidatos '()))
     (check-equal? (length (candidatos-activos-hechos
                           (ordenar-candidatos (puntuar-candidatos respuestas)))) 30)
     (check-not-false (siguiente-pregunta respuestas))
     (check-not-equal? (siguiente-pregunta respuestas) pregunta))
   (test-case "4. Respuestas probabilisticas: signo, magnitud y confianza"
     (define probable '((mundial-2006 . 0.7) (mas-50-seleccion . 1.0)))
     (define improbable '((mundial-2006 . -0.7) (mas-50-seleccion . 1.0)))
     (define (score respuestas)
       (cdr (assoc 'keylor-navas (puntuar-candidatos respuestas))))
     (check-= (score probable) 0.3 0.000001)
     (check-= (score improbable) 1.7 0.000001)
     (check-= (confianza (score probable) probable) (/ 0.3 1.7) 0.000001)
     (check-= (confianza (score improbable) improbable) 1.0 0.000001)
     (check-true (< (confianza (score probable) probable)
                    (confianza (score improbable) improbable))))
   (test-case "5. Perfil ambiguo: veinte No se no inventan un jugador"
     (define respuestas
       (let loop ([rs '()])
         (define q (siguiente-pregunta rs))
         (if q (loop (cons (cons q 0.0) rs)) rs)))
     (define resultado (resultado-final respuestas))
     (check-equal? (length respuestas) 20)
     (check-equal? (hash-ref resultado 'tipo) "sin_certeza")
     (check-= (hash-ref resultado 'confianza) 0.0 0.000001)
     (check-false (hash-has-key? resultado 'jugador)))
   (test-case "6. Hernan Medford es preferido sobre Ronald Gomez"
     (define respuestas (simular 'hernan-medford))
     (define puntuaciones (puntuar-candidatos respuestas))
     (check-equal? (hash-ref (resultado-final respuestas) 'jugador) "hernan-medford")
     (check-true (> (cdr (assoc 'hernan-medford puntuaciones))
                    (cdr (assoc 'ronald-gomez puntuaciones)))))
   (test-case "7. JSON real: todas las respuestas No se devuelven sin_certeza"
     (define-values (proc salida entrada errores)
       (subprocess #f #f #f (find-executable-path "racket") servidor))
     (dynamic-wind
       void
       (lambda ()
         (define (enviar mensaje)
           (write-json mensaje entrada) (newline entrada) (flush-output entrada)
           (read-json salida))
         (define final
           (let loop ([dato (enviar (hash 'accion "iniciar"))] [n 0])
             (check-true (<= n 20))
             (if (equal? (hash-ref dato 'tipo) "pregunta")
                 (loop (enviar (hash 'accion "responder" 'valor 0.0)) (add1 n))
                 dato)))
         (check-equal? (hash-ref final 'tipo) "sin_certeza")
         (check-false (hash-has-key? final 'jugador))
         (check-= (hash-ref final 'confianza) 0.0 0.000001))
       (lambda ()
         (close-output-port entrada)
         (subprocess-wait proc)
         (close-input-port salida)
         (close-input-port errores))))))
(exit (if (zero? (run-tests casos)) 0 1))
