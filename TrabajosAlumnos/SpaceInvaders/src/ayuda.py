# -*- coding: utf-8 -*-
'''
Created on 19 nov. 2017
Contador de vidas

@author: Kevin Kling
'''

import pilasengine

texto_ayuda = "El objetivo del juego es eliminar tanto aliens invasores como puedas, si tocas los planetas te daran un extra de 10 puntos. Usa las teclas direccionales del teclado para moverte y el espacio para disparar. No dejen que toquen tu nave porque moriras. Suerte piloto. QUE LA FUERZA TE ACOMPANIE"
                        
#se crea la escena de ayuda
class EscenaAyuda (pilasengine.escenas.Escena):
    def iniciar (self):
        self.pilas.fondos.Noche()
        self.pilas.actores.Texto(texto_ayuda,  magnitud = 16, ancho = 600, y = -30)
        self.pilas.actores.Texto("Como se juega?" , y = 50, fuente = "data/fuentes/Bangers.ttf")
        self.pilas.actores.BotonVolver()
