#lang racket

(require rackunit
         "../backend/conocimiento.scm"
         "../backend/reglas.scm")

(displayln
 "Ejecutando pruebas de conocimiento y reglas...")

;; Prueba 1:
;; La base debe contener exactamente 30 entidades.
(check-equal?
 (length conocimiento)
 30)

(check-equal?
 (length (obtener-entidades))
 30)

;; Prueba 2:
;; Deben existir 20 características distintas.
(check-equal?
 (length caracteristicas-disponibles)
 20)

(check-equal?
 (length
  (remove-duplicates caracteristicas-disponibles))
 20)

;; Prueba 3:
;; Cada futbolista debe tener las 20 características.
(for-each
 (lambda (entidad)
   (check-equal?
    (length
     (obtener-caracteristicas entidad))
    20))
 (obtener-entidades))

;; Prueba 4:
;; Consultas básicas de la base de conocimiento.
(check-equal?
 (buscar-valor 'keylor-navas 'portero)
 'si)

(check-equal?
 (buscar-valor 'keylor-navas 'mundial-2014)
 'si)

(check-equal?
 (buscar-valor 'bryan-ruiz 'mediocampista)
 'si)

(check-equal?
 (buscar-valor 'paulo-wanchope 'delantero)
 'si)

;; Si la persona no existe, debe responder desconocido.
(check-equal?
 (buscar-valor
  'persona-inexistente
  'portero)
 'desconocido)

;; Prueba 5:
;; Aplicación de reglas sobre Keylor Navas.
(define hechos-keylor
  (obtener-caracteristicas
   'keylor-navas))

(define inferencias-keylor
  (aplicar-reglas hechos-keylor))

;; Como Keylor es portero, debe pertenecer al área defensiva.
(check-not-false
 (member
  '(area-defensiva si)
  inferencias-keylor))

;; Como participó en 2014, pertenece a esa generación.
(check-not-false
 (member
  '(generacion-2014 si)
  inferencias-keylor))

;; Como posee más de 100 partidos y fue capitán,
;; debe considerarse referente de la selección.
(check-not-false
 (member
  '(referente-seleccion si)
  inferencias-keylor))

;; Como jugó en Europa, debe inferirse que fue
;; legionario europeo.
(check-not-false
 (member
  '(legionario-europeo si)
  inferencias-keylor))

;; Prueba 6:
;; Una regla no debe activarse cuando no se cumplen
;; todas sus condiciones.
(define inferencias-rolando
  (aplicar-reglas
   (obtener-caracteristicas
    'rolando-fonseca)))

(check-false
 (member
  '(generacion-2014 si)
  inferencias-rolando))

(displayln
 "Todas las pruebas finalizaron correctamente.")