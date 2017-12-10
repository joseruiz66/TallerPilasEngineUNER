# -*- coding: utf-8 -*-
'''
Created on 19 nov. 2017
Muestra la pantalla que termino el juego
@author: Ruiz Jose
'''
import pilasengine
class EscenaGameOver(pilasengine.escenas.Escena):

    def iniciar(self, juego):
        self.pilas.fondos.Pasto()
        self.juego =juego
        self.manchas = self.pilas.actores.Actor(imagen="../data/imagenes/manchas.png")
        self.manchas.transparencia = 50

        self.textoPuntaje =self.pilas.actores.Texto("Tu puntaje es: %d" %(self.juego.puntos.obtener()), magnitud=40, y=20)
        self.textoAviso =self.pilas.actores.Texto(u"Pulsá espacio para volver a empezar", y=-50)
        self.pilas.eventos.pulsa_tecla.conectar(self.cuando_pulsa_tecla)

    def cuando_pulsa_tecla(self, evento):
        if evento.texto == " ": # Si es la tecla espacio
            self.manchas.eliminar()
            self.textoPuntaje.eliminar()
            self.textoAviso.eliminar()
            self.juego.iniciar_juego(self.juego.nombre_jugador, puntaje="0",vidas=3)