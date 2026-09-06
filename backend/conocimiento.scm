#lang racket

; Estas funciones y variables podrán utilizarse
; desde los demás archivos del proyecto.
(provide conocimiento
         caracteristicas-disponibles
         obtener-entidades
         obtener-caracteristicas
         buscar-valor)

; Lista de las 20 características que utilizará el sistema.
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

; Convierte los valores booleanos #t y #f
; en los símbolos si y no.
(define (si-no valor)
  (cond
    [valor
     'si]

    [else
     'no]))

; Crea automáticamente las 20 características
; correspondientes a cada futbolista.
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

; Orden de los valores después de la posición:
;
; 1. Retirado.
; 2. Mundialista.
; 3. Participó en el Mundial 2014.
; 4. Más de 50 partidos con la selección.
; 5. Más de 100 partidos con la selección.
; 6. Capitán de la selección.
; 7. Jugó en Europa.
; 8. Jugó en la MLS.
; 9. Jugó en México.
; 10. Jugó en Saprissa.
; 11. Jugó en Alajuelense.
; 12. Jugó en Herediano.
; 13. Jugó en Cartaginés.
; 14. Anotó con la selección.
; 15. Participó en el Mundial 2002.
; 16. Participó en el Mundial 2006.

; Base de conocimiento conformada por 30 futbolistas.
(define conocimiento
  (list

   ; 1. Keylor Navas
   (crear-jugador
    'keylor-navas
    'portero
    #f #t #t #t #t #t
    #t #f #f
    #t #f #f #f
    #f #f #f)

   ; 2. Bryan Ruiz
   (crear-jugador
    'bryan-ruiz
    'mediocampista
    #t #t #t #t #t #t
    #t #f #f
    #f #t #f #f
    #t #f #f)

   ; 3. Celso Borges
   (crear-jugador
    'celso-borges
    'mediocampista
    #f #t #t #t #t #t
    #t #f #f
    #t #t #f #f
    #t #f #f)

   ; 4. Joel Campbell
   (crear-jugador
    'joel-campbell
    'delantero
    #f #t #t #t #t #f
    #t #f #t
    #t #t #f #f
    #t #f #f)

   ; 5. Walter Centeno
   (crear-jugador
    'walter-centeno
    'mediocampista
    #t #t #f #t #t #f
    #f #f #f
    #t #f #f #f
    #t #t #t)

   ; 6. Luis Marín
   (crear-jugador
    'luis-marin
    'defensor
    #t #t #f #t #t #t
    #f #f #f
    #f #t #f #f
    #t #t #t)

   ; 7. Rolando Fonseca
   (crear-jugador
    'rolando-fonseca
    'delantero
    #t #f #f #t #t #f
    #f #f #t
    #t #t #f #f
    #t #f #f)

   ; 8. Álvaro Saborío
   (crear-jugador
    'alvaro-saborio
    'delantero
    #t #t #f #t #t #f
    #t #t #f
    #t #f #f #f
    #t #t #t)

   ; 9. Paulo Wanchope
   (crear-jugador
    'paulo-wanchope
    'delantero
    #t #t #f #t #f #f
    #t #f #f
    #f #t #t #f
    #t #t #t)

   ; 10. Rónald Gómez
   (crear-jugador
    'ronald-gomez
    'delantero
    #t #t #f #t #f #f
    #t #f #f
    #t #t #f #f
    #t #t #t)

   ; 11. Mauricio Solís
   (crear-jugador
    'mauricio-solis
    'mediocampista
    #t #t #f #t #t #f
    #t #t #t
    #t #t #t #f
    #t #t #t)

   ; 12. Michael Umaña
   (crear-jugador
    'michael-umana
    'defensor
    #t #t #t #t #t #f
    #f #t #f
    #t #t #f #f
    #t #f #t)

   ; 13. Harold Wallace
   (crear-jugador
    'harold-wallace
    'defensor
    #t #t #f #t #t #f
    #f #f #f
    #t #t #f #f
    #t #t #t)

   ; 14. Christian Bolaños
   (crear-jugador
    'christian-bolanos
    'mediocampista
    #t #t #t #t #t #f
    #t #f #f
    #t #f #f #f
    #t #t #t)

   ; 15. Yeltsin Tejeda
   (crear-jugador
    'yeltsin-tejeda
    'mediocampista
    #f #t #t #t #f #f
    #t #f #f
    #t #f #t #f
    #t #f #f)

   ; 16. Cristian Gamboa
   (crear-jugador
    'cristian-gamboa
    'defensor
    #t #t #t #t #f #f
    #t #f #f
    #f #f #f #f
    #t #f #f)

   ; 17. Júnior Díaz
   (crear-jugador
    'junior-diaz
    'defensor
    #t #t #t #t #f #f
    #t #f #f
    #f #t #t #f
    #t #f #f)

   ; 18. Giancarlo González
   (crear-jugador
    'geancarlo-gonzalez
    'defensor
    #t #t #t #t #f #f
    #t #t #f
    #t #t #f #f
    #t #f #f)

   ; 19. Óscar Duarte
   (crear-jugador
    'oscar-duarte
    'defensor
    #t #t #t #t #f #f
    #t #f #f
    #t #f #f #f
    #t #f #f)

   ; 20. Francisco Calvo
   (crear-jugador
    'francisco-calvo
    'defensor
    #f #t #f #t #t #t
    #t #t #f
    #t #f #t #f
    #t #f #f)

   ; 21. Kendall Waston
   (crear-jugador
    'kendall-waston
    'defensor
    #t #t #f #t #f #f
    #f #t #f
    #t #f #f #f
    #t #f #f)

   ; 22. Johnny Acosta
   (crear-jugador
    'johnny-acosta
    'defensor
    #t #t #t #t #f #f
    #f #f #f
    #f #t #t #f
    #t #f #f)

   ; 23. Marco Ureña
   (crear-jugador
    'marco-urena
    'delantero
    #t #t #t #t #f #f
    #t #t #f
    #t #t #f #f
    #t #f #f)

   ; 24. Patrick Pemberton
   (crear-jugador
    'patrick-pemberton
    'portero
    #t #t #t #t #f #f
    #f #f #f
    #f #t #f #f
    #f #f #f)

   ; 25. Esteban Alvarado
   (crear-jugador
    'esteban-alvarado
    'portero
    #t #t #f #f #f #f
    #t #f #f
    #t #t #t #f
    #f #f #f)

   ; 26. Randall Brenes
   (crear-jugador
    'randall-brenes
    'delantero
    #t #t #t #f #f #f
    #f #f #f
    #t #f #f #t
    #t #f #f)

   ; 27. José Miguel Cubero
   (crear-jugador
    'jose-miguel-cubero
    'mediocampista
    #t #t #t #t #f #f
    #f #f #f
    #f #t #t #f
    #t #f #f)

   ; 28. Mauricio Montero
   (crear-jugador
    'mauricio-montero
    'defensor
    #t #t #f #t #f #t
    #f #f #f
    #f #t #f #f
    #t #f #f)

   ; 29. Hernán Medford
   (crear-jugador
    'hernan-medford
    'delantero
    #t #t #f #t #f #f
    #t #f #t
    #t #f #f #f
    #t #t #f)

   ; 30. Óscar Ramírez
   (crear-jugador
    'oscar-ramirez
    'mediocampista
    #t #t #f #t #f #f
    #f #f #f
    #t #t #f #f
    #t #f #f)))

; Devuelve una lista con los nombres
; de todas las entidades registradas.
(define (obtener-entidades)
  (map car conocimiento))

; Busca una entidad y devuelve todas sus características.
; Si la entidad no existe, devuelve una lista vacía.
(define (obtener-caracteristicas entidad)
  (define jugador
    (assoc entidad conocimiento))

  (cond
    [jugador
     (cdr jugador)]

    [else
     '()]))

; Busca el valor de una característica específica.
; Si la entidad o característica no existe,
; devuelve el símbolo desconocido.
(define (buscar-valor entidad caracteristica)
  (define dato
    (assoc caracteristica
           (obtener-caracteristicas entidad)))

  (cond
    [dato
     (cadr dato)]

    [else
     'desconocido]))