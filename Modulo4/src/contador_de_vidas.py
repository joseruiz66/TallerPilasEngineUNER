'''
Created on 19 nov. 2017
Contador de vidas

@author: ruiz jose
'''
class ContadorDeVidas():

    def __init__(self, pilas, cantidad_de_vidas):
        self.crear_texto(pilas)
        self.cantidad_de_vidas = cantidad_de_vidas
        self.vidas = [pilas.actores.Actor(imagen="../data/imagenes/tanque2.png") for x in range(cantidad_de_vidas)]

        for indice, vida in enumerate(self.vidas):
            vida.x = -230 + indice * 30
            vida.arriba = 230
            vida.escala = 0.5

    def crear_texto(self, pilas):
        # Genera el texto que dice 'vidas'
        self.texto = pilas.actores.Texto("Vidas:", magnitud=15)
        self.texto.color = pilas.colores.blanco
        self.texto.izquierda = -300
        self.texto.arriba = 230

    def le_quedan_vidas(self):
        return self.cantidad_de_vidas > 0

    def quitar_una_vida(self):
        self.cantidad_de_vidas -= 1
        vida = self.vidas.pop()
        vida.eliminar()
