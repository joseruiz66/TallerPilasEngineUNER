# -*- coding: UTF-8 -*-
"""
    Created on 19 nov. 2017
    
    Módulo: ayuda
    La clase EscenaAyuda es la escena que contiene las instrucciones del juego.

@author: Ruiz Jose
"""
import pilasengine

MENSAJE_AYUDA = "Mueve el mouse y haz click para disparar."

# Ayuda
class EscenaAyuda(pilasengine.escenas.Escena):

    def iniciar(self):
        # Definimos el fondo para la pantalla de ayuda.
        self.pilas.fondos.Tarde()
        self.crear_texto_ayuda()
        # Habilitar el abandono de la pantalla de algún modo.
        self.pulsa_tecla_escape.conectar(self.cuando_pulsa_tecla_escape)

    # Añadir el Titulo y texto de la ayuda     
    def crear_texto_ayuda(self):
        # Se escribe el texto “Instrucciones del juego”
        # en el centro a la altura y=200
        self.pilas.actores.Texto("Instrucciones del juego", y=200)
        # texto alnacenado en la constante MENSAJE_AYUDA en otra posición
        self.pilas.actores.Texto(MENSAJE_AYUDA, y=0)
        # Muestra la advertencia de que se pulse la tecla escape para salir.
        self.pilas.avisar("Pulsa ESC para regresar")

    # La forma de declarar los argumentos de esta función es un
    # estándar en Python y son obligatorios
    def cuando_pulsa_tecla_escape(self, *k, **kv):
        #Volver a la escena principal, abandonando la ayuda.
        self.pilas.escenas.EscenaMenu()