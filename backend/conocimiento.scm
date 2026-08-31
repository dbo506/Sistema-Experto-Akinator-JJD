#lang racket

;; Base de conocimiento del Akinator de futbolistas costarricenses.
;; Fecha de corte académica: 31 de agosto de 2026.

(provide conocimiento
         caracteristicas-disponibles
         obtener-entidades
         obtener-caracteristicas
         buscar-valor)

(define caracteristicas-disponibles
  '(portero
    defensor
    mediocampista
    delantero
    retirado
    mundialista
    mundial-2014
    mas-50-seleccion
    mas-100-seleccion
    capitan-seleccion
    jugo-europa
    jugo-mls
    jugo-mexico
    jugo-saprissa
    jugo-alajuelense
    jugo-herediano
    jugo-cartagines
    anoto-seleccion
    mundial-2002
    mundial-2006))

;; Convierte #t y #f en los símbolos si y no.
(define (si-no valor)
  (if valor 'si 'no))

;; Crea automáticamente las 20 características de un jugador.
(define (crear-jugador nombre
                       posicion
                       retirado
                       mundialista
                       mundial-2014
                       mas-50
                       mas-100
                       capitan
                       europa
                       mls
                       mexico
                       saprissa
                       alajuelense
                       herediano
                       cartagines
                       anoto
                       mundial-2002
                       mundial-2006)

  (list nombre
        (list 'portero
              (si-no (eq? posicion 'portero)))

        (list 'defensor
              (si-no (eq? posicion 'defensor)))

        (list 'mediocampista
              (si-no (eq? posicion 'mediocampista)))

        (list 'delantero
              (si-no (eq? posicion 'delantero)))

        (list 'retirado
              (si-no retirado))

        (list 'mundialista
              (si-no mundialista))

        (list 'mundial-2014
              (si-no mundial-2014))

        (list 'mas-50-seleccion
              (si-no mas-50))

        (list 'mas-100-seleccion
              (si-no mas-100))

        (list 'capitan-seleccion
              (si-no capitan))

        (list 'jugo-europa
              (si-no europa))

        (list 'jugo-mls
              (si-no mls))

        (list 'jugo-mexico
              (si-no mexico))

        (list 'jugo-saprissa
              (si-no saprissa))

        (list 'jugo-alajuelense
              (si-no alajuelense))

        (list 'jugo-herediano
              (si-no herediano))

        (list 'jugo-cartagines
              (si-no cartagines))

        (list 'anoto-seleccion
              (si-no anoto))

        (list 'mundial-2002
              (si-no mundial-2002))

        (list 'mundial-2006
              (si-no mundial-2006))))

;; Orden de los valores después de la posición:
;;
;; retirado
;; mundialista
;; mundial-2014
;; más de 50 partidos con la selección
;; más de 100 partidos con la selección
;; capitán
;; Europa
;; MLS
;; México
;; Saprissa
;; Alajuelense
;; Herediano
;; Cartaginés
;; anotó con la selección
;; Mundial 2002
;; Mundial 2006

(define conocimiento
  (list

   (crear-jugador
    'keylor-navas
    'portero
    #f #t #t #t #t #t
    #t #f #f
    #t #f #f #f
    #f #f #f)

   (crear-jugador
    'bryan-ruiz
    'mediocampista
    #t #t #t #t #t #t
    #t #f #f
    #f #t #f #f
    #t #f #f)

   (crear-jugador
    'celso-borges
    'mediocampista
    #f #t #t #t #t #t
    #t #f #f
    #t #t #f #f
    #t #f #f)

   (crear-jugador
    'joel-campbell
    'delantero
    #f #t #t #t #t #f
    #t #f #t
    #t #t #f #f
    #t #f #f)

   (crear-jugador
    'walter-centeno
    'mediocampista
    #t #t #f #t #t #f
    #f #f #f
    #t #f #f #f
    #t #t #t)

   (crear-jugador
    'luis-marin
    'defensor
    #t #t #f #t #t #t
    #f #f #f
    #f #t #f #f
    #t #t #t)

   (crear-jugador
    'rolando-fonseca
    'delantero
    #t #f #f #t #t #f
    #f #f #t
    #t #t #f #f
    #t #f #f)

   (crear-jugador
    'alvaro-saborio
    'delantero
    #t #t #f #t #t #f
    #t #t #f
    #t #f #f #f
    #t #t #t)

   (crear-jugador
    'paulo-wanchope
    'delantero
    #t #t #f #t #f #f
    #t #f #f
    #f #t #t #f
    #t #t #t)

   (crear-jugador
    'ronald-gomez
    'delantero
    #t #t #f #t #f #f
    #t #f #f
    #t #t #f #f
    #t #t #t)

   (crear-jugador
    'mauricio-solis
    'mediocampista
    #t #t #f #t #t #f
    #t #t #t
    #t #t #t #f
    #t #t #t)

   (crear-jugador
    'michael-umana
    'defensor
    #t #t #t #t #t #f
    #f #t #f
    #t #t #f #f
    #t #f #t)

   (crear-jugador
    'harold-wallace
    'defensor
    #t #t #f #t #t #f
    #f #f #f
    #t #t #f #f
    #t #t #t)

   (crear-jugador
    'christian-bolanos
    'mediocampista
    #t #t #t #t #t #f
    #t #f #f
    #t #f #f #f
    #t #t #t)

   (crear-jugador
    'yeltsin-tejeda
    'mediocampista
    #f #t #t #t #f #f
    #t #f #f
    #t #f #t #f
    #t #f #f)

   (crear-jugador
    'cristian-gamboa
    'defensor
    #t #t #t #t #f #f
    #t #f #f
    #f #f #f #f
    #t #f #f)

   (crear-jugador
    'junior-diaz
    'defensor
    #t #t #t #t #f #f
    #t #f #f
    #f #t #t #f
    #t #f #f)

   (crear-jugador
    'geancarlo-gonzalez
    'defensor
    #t #t #t #t #f #f
    #t #t #f
    #t #t #f #f
    #t #f #f)

   (crear-jugador
    'oscar-duarte
    'defensor
    #t #t #t #t #f #f
    #t #f #f
    #t #f #f #f
    #t #f #f)

   (crear-jugador
    'francisco-calvo
    'defensor
    #f #t #f #t #t #t
    #t #t #f
    #t #f #t #f
    #t #f #f)

   (crear-jugador
    'kendall-waston
    'defensor
    #t #t #f #t #f #f
    #f #t #f
    #t #f #f #f
    #t #f #f)

   (crear-jugador
    'johnny-acosta
    'defensor
    #t #t #t #t #f #f
    #f #f #f
    #f #t #t #f
    #t #f #f)

   (crear-jugador
    'marco-urena
    'delantero
    #t #t #t #t #f #f
    #t #t #f
    #t #t #f #f
    #t #f #f)

   (crear-jugador
    'patrick-pemberton
    'portero
    #t #t #t #t #f #f
    #f #f #f
    #f #t #f #f
    #f #f #f)

   (crear-jugador
    'esteban-alvarado
    'portero
    #t #t #f #f #f #f
    #t #f #f
    #t #t #t #f
    #f #f #f)

   (crear-jugador
    'randall-brenes
    'delantero
    #t #t #t #f #f #f
    #f #f #f
    #t #f #f #t
    #t #f #f)

   (crear-jugador
    'jose-miguel-cubero
    'mediocampista
    #t #t #t #t #f #f
    #f #f #f
    #f #t #t #f
    #t #f #f)

   (crear-jugador
    'mauricio-montero
    'defensor
    #t #t #f #t #f #t
    #f #f #f
    #f #t #f #f
    #t #f #f)

   (crear-jugador
    'hernan-medford
    'delantero
    #t #t #f #t #f #f
    #t #f #t
    #t #t #t #f
    #t #f #f)

   (crear-jugador
    'oscar-ramirez
    'mediocampista
    #t #t #f #t #f #f
    #f #f #f
    #t #t #f #f
    #t #f #f)))

;; Devuelve únicamente los nombres de las entidades.
(define (obtener-entidades)
  (map car conocimiento))

;; Devuelve las características de una entidad.
(define (obtener-caracteristicas entidad)
  (define jugador
    (assoc entidad conocimiento))

  (if jugador
      (cdr jugador)
      '()))

;; Busca el valor de una característica específica.
(define (buscar-valor entidad caracteristica)
  (define dato
    (assoc caracteristica
           (obtener-caracteristicas entidad)))

  (if dato
      (cadr dato)
      'desconocido))