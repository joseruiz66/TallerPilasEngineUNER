# -*- coding: UTF-8 -*-
"""
Created on 19 nov. 2017

    Módulo: Menu
    La clase EscenaMenu es la pantalla de inicio del juego, donde se encuentra el menu para iniciar o ver ayuda o bien salir del juego.
    El método que lleva al juego en si es 'comenzar_a_juego', y la llamada a EscenaJuego que se le pasa el nombre del jugador.

@author: Jose Ruiz
"""

import pilasengine

# Todas las escenas derivan de una misma clase, la clase padre
# de todas las escenas: pilas.escena.Base

# Menu princial del juego
class EscenaMenu(pilasengine.escenas.Escena):
    # Es la escena de presentacion donde se elijen las opciones del juego.

    # En método iniciar() debemos colocar todo aquello que queremos que
    # se ejecute al comenzar la escena
    def iniciar(self):
        # Definimos el fondo para la pantalla de ayuda.
        self.pilas.fondos.Noche()
        self.crear_titulo_del_juego()
        self.enemigos_contra_protagonista()
        self.poner_musica_de_fondo()
        self.ingresar_nombre_jugador()
        self.crear_menu_principal()

    # Carga la imagen del logo, lo ubica y produce un efecto al aparecer.
    def crear_titulo_del_juego(self):
        self.logo = self.pilas.actores.Actor(imagen="../data/imagenes/logotanque.png")
        self.logo.y = 190
        self.logo.escala = 1
        self.logo.escala = [0.5], 1.5

    # crea enemigos y los lanza contra el protagonista.
    def enemigos_contra_protagonista(self):
        self.pilas.actores.Enemigo(190, 16)
        self.pilas.actores.Enemigo(190, 16)
        self.pilas.actores.Enemigo(190, 16)
        self.pilas.actores.Enemigo(190, 16)
        self.pilas.actores.Enemigo(190, 16)
        
    # coloca musica en la escena menu
    def poner_musica_de_fondo(self):
        self.musica_fondo = self.pilas.musica.cargar('../data/musica/musica_menu.wav')
        self.musica_fondo.detener()
        self.musica_fondo.reproducir(repetir = True)

    # Permite al jugador ingresar el nombre que se mostrara durante el juego
    def ingresar_nombre_jugador(self):
        self.nombre_jugador = self.pilas.interfaz.IngresoDeTexto("", y=80)
        self.nombre_jugador.texto = u''
        self.pilas.actores.Texto("Nombre:", x=-210, y=80)
        
    # Creamos las tuplas en las que el primer elemento
    # es el texto que se quiere mostrar y el segundo es 
    # la función que se ejecutará al seleccionarlo.
    def crear_menu_principal(self):
        opciones = [
            ("Comenzar a jugar", self.comenzar_a_jugar),
            ("Ver ayuda", self.mostrar_ayuda_del_juego),
            ("Salir", self.salir_del_juego)
            ]
        # Utiliza el actor predefinido de Pilas pilas.actores.Menu
        self.pilas.actores.Menu(opciones)
        
    def comenzar_a_jugar(self):
        self.musica_fondo.detener()
        self.pilas.escenas.EscenaJuego(self.nombre_jugador.texto)

    def salir_del_juego(self):
        self.musica_fondo.detener()
        self.pilas.terminar()
        
    def mostrar_ayuda_del_juego(self):
        self.musica_fondo.detener()
        self.pilas.escenas.EscenaAyuda()
        