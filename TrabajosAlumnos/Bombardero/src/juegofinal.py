# coding: utf-8
'''
Created on 29 nov. 2017

@author: Jeremías Lapalma
'''

import pilasengine
from random import random
import math

'''
Objetos auxiliares
'''
class Config():
    ANCHO_DE_PANTALLA = 640
    ALTO_DE_PANTALLA = 480
    PASADAS_POR_NIVEL = 10
    INCREMENTO_DIFICULTAD = 10
    TIEMPO_INICIAL_PASADA = 10
    PUNTOS_POR_HIT = 10
    PUNTOS_POR_FALLO = -10
    PUNTOS_POR_NO_DISPARO = -50

class Capas():
    fondo = 30
    cajas = 20
    bomba = 10
    avion = 1

'''
Variables globales
'''    
pilas = pilasengine.iniciar(
           ancho = Config.ANCHO_DE_PANTALLA, 
           alto = Config.ALTO_DE_PANTALLA)
sonido_encendido = True


cancion_de_fondo = pilas.musica.cargar('des.mp3')
cancion_de_fondo.reproducir()
cancion_de_fondo.detener_gradualmente(10)


'''
Objetos del juego
'''
class Bomba(pilasengine.actores.Actor):
    def iniciar(self):
        self.imagen = 'bomba.png'
        self.escala = 0.15
        self.z = Capas.bomba
        self.figura_de_colision = pilas.fisica.Rectangulo(
                    0, 0, 35, 10,
                    sensor = True, dinamica = False)
        self.evento_explosion_solitaria = pilas.evento.Evento(
            'Explosión solitaria')
    
    def actualizar(self):
        self.x -= 1
        self.y -= 2
        if self.rotacion < 90:
            self.rotacion += 0.5
        if (self.y < -Config.ALTO_DE_PANTALLA/2.0 
                or self.x < -Config.ANCHO_DE_PANTALLA/2.0):
            self.evento_explosion_solitaria.emitir()
            self.eliminar()
    
class Avion(pilasengine.actores.Actor):
    def iniciar(self):
        self.tiempo_por_pasada = \
            Config.TIEMPO_INICIAL_PASADA
        self.imagen = 'globo.png'
        self.escala = 0.25
        self.click_de_mouse(self.on_click)
        self.puedo_disparar = True
        self.evento_fin_de_vuelo = pilas.evento.Evento(
            'Fin de vuelo')
        self.evento_disparo_errado = pilas.evento.Evento(
            'Disparo errado')
        
    def volar(self):
        self.y = 150
        self.x = 400
        pilas.utils.interpolar(self, 'x', -400, 
                duracion = self.tiempo_por_pasada, 
                tipo = 'lineal')
        
    def fin_del_vuelo(self):
        self.evento_fin_de_vuelo.emitir()
        self.volar()
        self.puedo_disparar = True
    
    def actualizar(self):
        if self.x <= -400:
            self.fin_del_vuelo()
    
    def soltar_bomba(self):
        bomba = Bomba(pilas)
        bomba.x = self.x
        bomba.y = self.y - 20
        bomba.evento_explosion_solitaria.conectar(
            self.on_disparo_errado)
    
    def on_disparo_errado(self, *ignore):
        self.evento_disparo_errado.emitir()
        
    def on_click(self, evento):
        if self.puedo_disparar:
            self.soltar_bomba()
            self.puedo_disparar = False

class Objetivo(pilasengine.actores.Actor):
    def iniciar(self):
        self.imagen = 'caja.png'
        self.z = Capas.cajas
        self.transparencia = 40
    
    def definir_como_principal(self):
        self.transparencia = 0
        self.figura_de_colision = pilas.fisica.Rectangulo(
                0, 0, 48, 48, sensor = True, dinamica = False)
        self.etiquetas.agregar('blanco')
        self.aprender(pilas.habilidades.PuedeExplotar)

'''
Escenas
'''
class MenuPrincipal(pilasengine.escenas.Escena):
    def iniciar(self):
        self.fondo = pilas.fondos.FondoMozaico('juego.jpg')
        
        self.title = pilas.actores.Actor()
        self.title.imagen = 'bombardero_titulo.png'
        self.title.y = Config.ALTO_DE_PANTALLA * .25
        self.title.x = 0
        
        self.boton_iniciar = pilas.interfaz.Boton('Iniciar')
        self.boton_iniciar.escala = 2
        self.boton_iniciar.conectar(self.iniciar_juego)
        
        self.boton_sonido = pilas.interfaz.Boton('Sonido')
        self.boton_sonido.escala = 2
        self.boton_sonido.conectar(self.alternar_sonido)
        self.boton_sonido.y = (self.boton_iniciar.y
            - self.boton_sonido.alto * self.boton_sonido.escala)
        self.texto_sonido = pilas.actores.Texto('Encendido')
        self.texto_sonido.y = (self.boton_sonido.y
            - self.texto_sonido.alto)
        self.texto_sonido.x = 0
        self.texto_sonido.color = pilas.colores.amarillo
        self.setear_texto_sonido()
        
        self.boton_salir = pilas.interfaz.Boton('Salir')
        self.boton_salir.escala = 2
        self.boton_salir.conectar(self.salir_del_juego)
        self.boton_salir.y = (self.texto_sonido.y 
            - self.boton_salir.alto * self.boton_salir.escala)
            
    def ejecutar(self):
        pass
        
    def iniciar_juego(self):
        pilas.escenas.JuegoPrincipal()
        pilas.escena.ejecutar()
        
    def salir_del_juego(self):
        pilas.terminar()
    
    def alternar_sonido(self):
        global sonido_encendido 
        sonido_encendido = not sonido_encendido
        self.setear_texto_sonido()
        
    def setear_texto_sonido(self):
        if sonido_encendido:
            self.texto_sonido.texto = 'Encendido'
        else:
            self.texto_sonido.texto = 'Apagado'
        
class JuegoPrincipal(pilasengine.escenas.Escena):
    def iniciar(self):
        self.fondo = pilas.fondos.FondoMozaico('juego.jpg')
        self.objetivos = pilas.actores.Grupo()
        self.avion = Avion(pilas)
        self.avion.evento_fin_de_vuelo.conectar(
            self.on_fin_pasada)
        self.avion.evento_disparo_errado.conectar(
            self.on_disparo_errado)
            
        self.texto_errar_disparo = pilas.actores.Texto(
            'Disparo errado!!!!')
        self.texto_errar_disparo.transparencia = 100
        self.texto_errar_disparo.color = pilas.colores.rojo
        self.texto_puntos_hit = pilas.actores.Texto(
            '0000')
        self.texto_puntos_hit.transparencia = 100
        self.texto_puntos_hit.color = pilas.colores.verdeoscuro

        self.puntaje = 0
        self.pasada = 1
        self.nivel = 1
        self.texto_puntaje = pilas.actores.Texto(
            'Puntaje 0000000')
        self.texto_puntaje.y = (
            Config.ALTO_DE_PANTALLA/2.0 
            - self.texto_puntaje.alto)
        self.texto_puntaje.x = (
            -Config.ANCHO_DE_PANTALLA/2.0 * .9 
            + self.texto_puntaje.ancho/2.0)
        self.texto_pasada = pilas.actores.Texto('Pasada 0000')
        self.texto_pasada.y = (
            Config.ALTO_DE_PANTALLA/2.0 
            - self.texto_puntaje.alto)
        self.texto_pasada.x = (
            Config.ANCHO_DE_PANTALLA/2.0 * .9 
            - self.texto_puntaje.ancho/2.0)
        self.texto_nivel = pilas.actores.Texto('Nivel 0000')
        self.texto_nivel.y = (
            Config.ALTO_DE_PANTALLA/2.0 
            - self.texto_puntaje.alto)
        self.texto_nivel.x = 0
        self.actualizar_ui()
    
    def ejecutar(self):
        self.poner_objetivos()
        pilas.colisiones.agregar('bomba', 'blanco', self.caboom)
        self.avion.volar()
    
    def juego_terminado(self):
        pilas.escenas.JuegoTerminado(self.nivel)
        pilas.escena.ejecutar()
        
    def actualizar(self):
        if (self.puntaje <= 0
                and not (self.nivel == 1 and self.pasada == 1)):
            self.juego_terminado()
    
    def eliminar_objetivos(self):
        for obj in self.objetivos:
            obj.eliminar()
            
    def reposicionar_objetivos(self):
        self.eliminar_objetivos()
        self.poner_objetivos()
        
    def poner_objetivos(self):
        cantidad = 5 + int(math.ceil(random()*5))
        for n in range(cantidad):
            obj = Objetivo(pilas)
            obj.y = (
                -Config.ALTO_DE_PANTALLA/2.0 
                + obj.alto/2.0)
            obj.x = (
                Config.ANCHO_DE_PANTALLA/2.0 
                - obj.ancho/2.0 
                - obj.ancho * n)
            if (n == cantidad - 1):
                obj.definir_como_principal()
            self.objetivos.agregar(obj)

    def caboom(self, objeto1, objeto2):
        self.puntaje += Config.PUNTOS_POR_HIT
        self.actualizar_ui()
        
        self.texto_puntos_hit.texto = str(Config.PUNTOS_POR_HIT)
        self.texto_puntos_hit.x = objeto1.x
        self.texto_puntos_hit.y = (objeto1.y
            + self.texto_puntos_hit.alto)
        self.texto_puntos_hit.transparencia = 0
        self.texto_puntos_hit.escala = 1
        self.texto_puntos_hit.transparencia = [100], 2
        self.texto_puntos_hit.escala = [15], 4
        
        objeto2.eliminar()
        objeto1.eliminar()
        pilas.tareas.agregar(1, self.reposicionar_objetivos)
    
    def on_disparo_errado(self, *ignore):
        self.puntaje += Config.PUNTOS_POR_FALLO
        self.actualizar_ui()
        self.texto_errar_disparo.transparencia = 0
        self.texto_errar_disparo.escala = 1
        self.texto_errar_disparo.transparencia = [100], 2
        self.texto_errar_disparo.escala = [7], 4
    
    def on_fin_pasada(self, *ignore):
        if self.avion.puedo_disparar:
            self.puntaje += Config.PUNTOS_POR_NO_DISPARO
        self.pasada += 1
        if self.pasada > Config.PASADAS_POR_NIVEL:
            self.pasada = 1
            self.nivel += 1
            self.puntaje += 100
            # Reduzco el tiempo por pasada para aumentar 
            # la dificultad
            self.avion.tiempo_por_pasada = (
                self.avion.tiempo_por_pasada 
                * (1 - Config.INCREMENTO_DIFICULTAD/100.0))
            pilas.avisar(
                'Tiempo por pasada de ' 
                + str(self.avion.tiempo_por_pasada) 
                + ' segundos!')
        self.actualizar_ui()
        
    def actualizar_ui(self):
        self.texto_puntaje.texto = (
            'Puntaje ' + ('000000' + str(self.puntaje))[-6:])
        self.texto_nivel.texto = (
            'Nivel ' + ('00' + str(self.nivel))[-2:])
        self.texto_pasada.texto = (
            'Pasada ' + ('00' + str(self.pasada))[-2:])

class JuegoTerminado(pilasengine.escenas.Escena):
    def iniciar(self, nivel_final):
        self.fondo = pilas.fondos.FondoMozaico('juego.jpg')
        self.boton_menu = pilas.interfaz.Boton('Menu Principal')
        self.boton_menu.escala = 2
        self.boton_menu.conectar(self.on_boton_menu)
        
        texto = ('Ha finalizado el juego alcanzando el nivel '
            + str(nivel_final) + '!!')
        self.texto = pilas.actores.Texto(texto)
        self.texto.y += 100
    
    def ejecutar(self):
        pass
        
    def on_boton_menu(self):
        pilas.escenas.MenuPrincipal()
        pilas.escena.ejecutar()
        
pilas.escenas.vincular(MenuPrincipal)
pilas.escenas.vincular(JuegoPrincipal)
pilas.escenas.vincular(JuegoTerminado)
pilas.escenas.MenuPrincipal()
pilas.escena.ejecutar()