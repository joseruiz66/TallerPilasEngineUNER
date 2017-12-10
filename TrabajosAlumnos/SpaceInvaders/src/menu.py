# -*- coding: utf-8 -*-
'''
Created on 19 nov. 2017
Contador de vidas

@author: Kevin Kling
'''


import pilasengine

#se crea el boton volver
class BotonVolver(pilasengine.actores.Actor):
    def iniciar(self):
        self.imagen = "../data/imagenes/volver_patra.png"
        self.cuando_hace_click = self._volver_a_la_escena_inicial
        self.y = 320
        self.y = [210]
        self.x = -290
        self.escala=0.09
    def _volver_a_la_escena_inicial(self, evento):
        self.pilas.escenas.PantallaBienvenida()

#se crea el menu
class PantallaBienvenida(pilasengine.escenas.Escena):
    def iniciar(self):
        
        self.logo = Logo(self.pilas)
        marciano =  self.pilas.actores.Martian()
        marciano.decir('BIENVENIDO. Elije una opcion')
        self.fondo = self.pilas.fondos.Galaxia(dy=+5)
        self.pilas.actores.Menu(
        [
            ('Iniciar juego', self.iniciar_juego),
            ('Ayuda', self.salir_ayuda),
            ('Salir', self.salir_del_juego)
        ])
        
    def salir_del_juego(self):
        self.pilas.terminar()
    def salir_ayuda(self):
        self.pilas.escenas.EscenaAyuda()
    def iniciar_juego(self):
        self.pilas.escenas.EscenaInicial()
       
#creamos el titulo
class Logo(pilasengine.actores.Actor):
    def iniciar(self):
        self.imagen = "../data/imagenes/banne.png"
        self.y = 150
        self.escala = 0.6
        

       # t.escala = , 1