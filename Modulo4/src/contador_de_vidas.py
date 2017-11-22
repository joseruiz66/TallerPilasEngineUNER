# -*- coding: utf-8 -*-
'''
Created on 19 nov. 2017
Contador de vidas

@author: ruiz jose
'''
class ContadorDeVidas():

    def __init__(self, pilas, cantidad_de_vidas):
        self.cantidad_de_vidas = cantidad_de_vidas
        self.crear_texto(pilas)
        self.vidas = self.crear_vidas(pilas)

    def crear_texto(self, pilas):
        # Genera el texto que dice 'vidas'
        self.texto = pilas.actores.Texto("Vidas:", magnitud=15)
        self.texto.color = pilas.colores.blanco
        self.texto.izquierda = -300
        self.texto.arriba = 230

    def crear_vidas(self, pilas):
        vidas = pilas.actores.Actor() * self.cantidad_de_vidas
        vidas.imagen="../data/imagenes/tanque2.png"
        vidas.escala = 0.5
        vidas.arriba = 230
        indice = 0
        for  vida in vidas:
            vida.x = -230 + indice * 30
            indice += 1
        return vidas
        
    def le_quedan_vidas(self):
        return self.cantidad_de_vidas > 0

    def quitar_una_vida(self):
        self.cantidad_de_vidas -= 1
        self.vidas[self.cantidad_de_vidas].eliminar()

