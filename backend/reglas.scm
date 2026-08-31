#lang racket

(provide reglas
         cumple-condiciones?
         aplicar-regla
         aplicar-reglas)

;; Estructura de cada regla:
;;
;; (nombre
;;   ((caracteristica valor) ...)
;;   (conclusion valor))

(define reglas
  '(
    (es-area-defensiva-por-portero
     ((portero si))
     (area-defensiva si))

    (es-area-defensiva-por-defensor
     ((defensor si))
     (area-defensiva si))

    (es-creador-de-juego
     ((mediocampista si))
     (area-creativa si))

    (es-atacante
     ((delantero si))
     (area-ofensiva si))

    (pertenece-generacion-2014
     ((mundialista si)
      (mundial-2014 si))
     (generacion-2014 si))

    (es-referente-seleccion
     ((mas-100-seleccion si)
      (capitan-seleccion si))
     (referente-seleccion si))

    (es-legionario-europeo
     ((jugo-europa si))
     (legionario-europeo si))

    (es-legionario-norteamericano
     ((jugo-mls si))
     (legionario-norteamerica si))

    (es-legionario-mexicano
     ((jugo-mexico si))
     (legionario-mexico si))

    (es-leyenda-mundialista-retirada
     ((retirado si)
      (mundialista si))
     (leyenda-mundialista-retirada si))
    ))

;; Comprueba que todas las condiciones de una regla
;; se encuentren dentro de los hechos del jugador.
(define (cumple-condiciones? hechos condiciones)
  (andmap
   (lambda (condicion)
     (member condicion hechos))
   condiciones))

;; Aplica una sola regla.
(define (aplicar-regla hechos regla)
  (define condiciones
    (cadr regla))

  (define conclusion
    (caddr regla))

  (if (and
       (cumple-condiciones? hechos condiciones)
       (not (member conclusion hechos)))

      (cons conclusion hechos)

      hechos))

;; Aplica todas las reglas.
;;
;; Si aparecen hechos nuevos, vuelve a ejecutar las reglas.
;; El proceso termina cuando ya no aparecen conclusiones nuevas.
(define (aplicar-reglas hechos)
  (define nuevos-hechos
    (foldl
     (lambda (regla hechos-acumulados)
       (aplicar-regla hechos-acumulados regla))
     hechos
     reglas))

  (if (= (length nuevos-hechos)
         (length hechos))

      nuevos-hechos

      (aplicar-reglas nuevos-hechos)))