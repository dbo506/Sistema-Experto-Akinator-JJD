#lang racket

(require "conocimiento.scm")
(require "reglas.scm")

(provide seleccionar-pregunta
         todas-las-caracteristicas)

;; Extraer características derivadas de las reglas
(define caracteristicas-derivadas
  (map (lambda (r) (car (caddr r))) reglas))

;; Lista total de características (base + derivadas)
(define todas-las-caracteristicas
  (remove-duplicates (append caracteristicas-disponibles caracteristicas-derivadas)))

;; Evalúa qué tan buena es una pregunta para dividir a los candidatos activos
;; Usa un puntaje basado en la entropía/balance. Menor puntaje es mejor.
(define (evaluar-pregunta pregunta candidatos-hechos)
  (define conteo
    (foldl (lambda (cand-hechos acc)
             (let ([val (assoc pregunta cand-hechos)])
               ;; Si no está definido, se asume 'no' (dominio cerrado booleano)
               (if (and val (eq? (cadr val) 'si))
                   (list (add1 (car acc)) (cadr acc))
                   (list (car acc) (add1 (cadr acc))))))
           '(0 0)
           candidatos-hechos))
  
  (define si (car conteo))
  (define no (cadr conteo))
  
  ;; Si una pregunta no divide a los candidatos restantes en absoluto 
  ;; (es decir, todos tienen 'si' o todos tienen 'no'), 
  ;; no aporta nueva información y es ilógico/redundante preguntarla.
  (if (or (= si 0) (= no 0))
      9999 ; Puntaje altísimo para descartarla
      (- (abs (- si no)) (+ si no))))

;; Selecciona la característica que mejor discrimina a los candidatos activos
;; y que no se haya preguntado todavía.
(define (seleccionar-pregunta candidatos-activos-hechos preguntas-hechas)
  (define candidatas 
    (filter (lambda (p) (not (member p preguntas-hechas)))
            todas-las-caracteristicas))
            
  (if (null? candidatas)
      #f
      (let* ([evaluaciones (map (lambda (p) (cons p (evaluar-pregunta p candidatos-activos-hechos))) candidatas)]
             ;; Filtramos las que sacaron 9999 (las que no dividen a los candidatos)
             [utiles (filter (lambda (eval) (< (cdr eval) 9999)) evaluaciones)])
        
        (if (null? utiles)
            #f ; Ya no hay ninguna pregunta útil que logre separar a los candidatos restantes
            (let ([mejor (foldl (lambda (eval mejor-actual)
                                  (if (< (cdr eval) (cdr mejor-actual))
                                      eval
                                      mejor-actual))
                                (car utiles)
                                (cdr utiles))])
              (car mejor))))))
