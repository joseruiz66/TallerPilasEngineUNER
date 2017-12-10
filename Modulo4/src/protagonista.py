# -*- coding: utf-8 -*-
'''
Created on 19 nov. 2017
Clase protagonista

@author: Ruiz jose
'''
from pilasengine.actores.torreta import Torreta

class Protagonista(Torreta):
    
    def iniciar(self, municion_bala_simple=None, enemigos=[], cuando_elimina_enemigo=None, x=0, y=0, frecuencia_de_disparo=10):
        Torreta.iniciar(self,municion_bala_simple, enemigos, cuando_elimina_enemigo,x,y,frecuencia_de_disparo)
        self.imagen = "../data/imagenes/tanque2.png"
        self.aprender("PuedeExplotarConHumo")