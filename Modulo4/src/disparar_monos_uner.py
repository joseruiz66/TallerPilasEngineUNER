# -*- coding: utf-8 -*-
'''
Created on 19 nov. 2017
El objetivo del juego consiste en que el jugador (torreta) debe dispararles a
los monos que se generan al azar en pantalla y que intentan llegar hasta él
para destruirlo.
El juego incluye un sencillo marcador de puntuación que aumenta con cada
mono destruido, un control de sonido, un sistema de bonus (premios) que
mejora el arma de disparos , un contador de vidas y avisos de texto en
pantalla.
A medida que avanza el tiempo de ejecución se aumenta la velocidad de
los monos.


@author: Ruiz Jose
'''
# indica que use la librería pilasengine
import pilasengine

pilas = pilasengine.iniciar(ancho=800, alto=600, titulo="Disparar Monos")

# reinicia pilas automaticamente cuando se edita el archivo.
# Para ello debemos abril el archivo con un editor externo y a su vez
# abrirlo con pilas, con esto logramos que al guardar los cambios en el editor
# automaticamente  se reflejan en el visor de pilas
pilas.reiniciar_si_cambia(__file__)    


from escena_menu import EscenaMenu
from escena_juego import EscenaJuego
from escena_ayuda import EscenaAyuda
from escena_gameover import EscenaGameOver
from escena_perdiste_una_vida import EscenaPerdisteUnaVida


# Importamos del archivo protagonista.py la clase Enemigo y Premio
from habilidades_enemigo_premio import Aparecer_A_Cierta_Distancia_Del_Protagonista, Agrandar_Actor, Ir_Contra_Actor

# Incluimos nuestra habilidad a las habiliades en pilas
pilas.habilidades.vincular(Aparecer_A_Cierta_Distancia_Del_Protagonista)    
pilas.habilidades.vincular(Agrandar_Actor)        
pilas.habilidades.vincular(Ir_Contra_Actor)        


# Importamos del archivo protagonista.py la clase Enemigo y Premio
from enemigo_premio import Enemigo, Premio
# Importamos del archivo protagonista.py la clase Protagonista
from protagonista import Protagonista
# Incluimos nuestro actor a los actores en pilas
pilas.actores.vincular(Enemigo)        
pilas.actores.vincular(Premio)
pilas.actores.vincular(Protagonista)

# Incluimos nuestras escenas a las escenas de pilas        
pilas.escenas.vincular(EscenaMenu)
pilas.escenas.vincular(EscenaJuego)
pilas.escenas.vincular(EscenaAyuda)
pilas.escenas.vincular(EscenaGameOver)
pilas.escenas.vincular(EscenaPerdisteUnaVida)
        
# Seleccionamos escena Menu
pilas.escenas.EscenaMenu()

pilas.ejecutar()
