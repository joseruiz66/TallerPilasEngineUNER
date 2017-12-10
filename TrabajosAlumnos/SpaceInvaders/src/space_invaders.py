# -*- coding: utf-8 -*-
'''
Created on 19 nov. 2017
Contador de vidas

@author: Kevin Kling
'''


import pilasengine
import random
import ayuda
import menu

pilas = pilasengine.iniciar()

#creo el actor personalizado..
class Alien(pilasengine.actores.Actor):
    def iniciar(self): 
        self.imagen = "../data/imagenes/alien.png"
        self.escala = 0.2
        self.radio_de_colision = 40
        self.aprender("PuedeExplotarConHumo")

class EscenaInicial (pilasengine.escenas.Escena):

    def iniciar (self):
        self.pilas.actores.BotonVolver()
        puntaje = self.pilas.actores.Puntaje(-240, 210, color= self.pilas.colores.blanco)
        tiempo = 3
        self.pilas.avisar(u"Que la fueza te acompañe!!")
        enemigos = pilas.actores.Grupo()
        nave = pilas.actores.NaveRoja(y=-200)
        fondo = pilas.fondos.Galaxia(dy=-5)
        nave.aprender(pilas.habilidades.LimitadoABordesDePantalla)
        sony = pilas.actores.Sonido()
        aliados = pilas.actores.Grupo()
        
        #calcula una posicion al azar para que aparezca el alien/planeta
        def calcular_posicion():
            x = random.randrange(-320, 320)
            y = 250
            return x, y
            
        #crea el anemigo    
        def crear_alien ():
            alien = Alien(pilas)
            aliados.agregar(alien)
            alien.x, alien.y = calcular_posicion()
            tipo_interpolacion = ["lineal", "aceleracion_gradual", "desaceleracion_gradual", "gradual"]
            interpolacion = random.choice(tipo_interpolacion)
            pilas.utils.interpolar(alien, 'y', -300, duracion=tiempo, tipo=interpolacion)
            nave.definir_enemigos(alien, puntaje.aumentar)
        self.pilas.escena_actual().tareas.siempre(1, crear_alien)
        
        #crea el planeta
        def crear_planeta ():
            enemigo =  self.pilas.actores.Planeta()
            enemigo.x, enemigo.y = calcular_posicion()
            enemigos.agregar(enemigo)
            enemigo.escala = 0.5
            enemigo.radio_de_colision = 15
            tipo_interpolacion = ["lineal", "aceleracion_gradual", "desaceleracion_gradual", "gradual"]
            interpolacion = random.choice(tipo_interpolacion)
            pilas.utils.interpolar(enemigo, 'y', -300, duracion=tiempo, tipo=interpolacion)
        self.pilas.escena_actual().tareas.siempre(5, crear_planeta)
        
        #accion que se realiza al haber colision nave-planeta
        def cuando_coli (enemigos, nave):
            puntaje.aumentar(10)
        pilas.colisiones.agregar(nave, enemigos, cuando_coli)
        

        
        #acciones que se realizan al haber colision nave-enemigo
        def perder ():
            self.gameover = Gameover(self.pilas)
            puntaje.eliminar()
            sony.eliminar()
            nave.eliminar()
            self.pilas.camara.vibrar(3,0.3)
            self.pilas.escena_actual().tareas.eliminar_todas()
            self.pilas.avisar("CHOCASTE. Conseguiste %d puntos" %(puntaje.obtener()))
        pilas.colisiones.agregar(nave, aliados, perder)
        
#define la imagen ´gameover´
class Gameover(pilasengine.actores.Actor):
    def iniciar(self):
        self.imagen = "../data/imagenes/gameover.png"
        self.escala = [0.2], 1
        
alien = Alien(pilas)
pilas.actores.vincular(menu.BotonVolver)
pilas.escenas.vincular(ayuda.EscenaAyuda)
pilas.escenas.vincular(EscenaInicial)
pilas.escenas.vincular(menu.PantallaBienvenida)
pilas.escenas.PantallaBienvenida()
pilas.ejecutar()