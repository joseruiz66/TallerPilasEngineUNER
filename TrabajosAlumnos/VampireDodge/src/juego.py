# coding: utf-8
'''
Created on 29 nov. 2017

@author: Dario Medina
'''

import pilasengine

pilas = pilasengine.iniciar()

VELOCIDAD = 6



##############VAMPIRO#########################
class Vampiro(pilasengine.actores.Actor):

    def iniciar(self):
        self.imagen = pilas.imagenes.cargar_animacion("imagenes/protagonista.png", 6)
        self.y = -155
        self.escala = 0.75
        self.radio_de_colision = 30

        self.imagen.definir_animacion('parado', [2], 10)
        self.imagen.definir_animacion('caminar', [3, 4, 5, 4], 15)
        self.imagen.definir_animacion('saltar', [0], 15)

        self.hacer_inmediatamente('ComportamientoNormal')

    def actualizar(self):
        if pilas.control.izquierda:
            self.x -= VELOCIDAD
            self.espejado = True

        if pilas.control.derecha:
            self.x += VELOCIDAD
            self.espejado = False

        if self.x > 280:
            self.x = 280

        if self.x < -280:
            self.x = -280

        self.imagen.avanzar()
        
class ComportamientoNormal(pilasengine.comportamientos.Comportamiento):

    def iniciar(self, receptor):
        self.receptor = receptor
        self.receptor.imagen.cargar_animacion('parado')

    def actualizar(self):
        if pilas.control.derecha or pilas.control.izquierda:
            self.receptor.hacer_inmediatamente('ComportamientoCaminar')

        if pilas.control.arriba:
            self.receptor.hacer_inmediatamente('ComportamientoSaltar')


class ComportamientoCaminar(pilasengine.comportamientos.Comportamiento):

    def iniciar(self, receptor):
        self.receptor = receptor
        self.receptor.imagen.cargar_animacion('caminar')

    def actualizar(self):
        if not pilas.control.derecha and not pilas.control.izquierda:
            self.receptor.hacer_inmediatamente('ComportamientoNormal')

        if pilas.control.arriba:
            self.receptor.hacer_inmediatamente('ComportamientoSaltar')

class ComportamientoSaltar(pilasengine.comportamientos.Comportamiento):

    def iniciar(self, receptor):
        self.receptor = receptor
        self.receptor.imagen.cargar_animacion('saltar')
        self.velocidad = 12
        self.coordenada_y_inicial = self.receptor.y

    def actualizar(self):
        self.receptor.y += self.velocidad
        self.velocidad -= 0.5

        if self.receptor.y < self.coordenada_y_inicial:
            self.receptor.hacer_inmediatamente('ComportamientoNormal')
            self.receptor.y = self.coordenada_y_inicial
########################################











############CALABAZA y SANGRE##################
class Calabaza(pilasengine.actores.Actor):

    def iniciar(self):
        self.imagen = "imagenes/calabaza.png"
        self.y = 300
        self.x = pilas.azar(-285, 285)
        self.velocidad = 0
        self.radio_de_colision = 50
        self.escala = 0.70

    def actualizar(self):
        self.velocidad += 0.05
        self.y -= self.velocidad
        self.rotacion += 2

        if self.y < -400:
            self.eliminar()
            
class Sangre(pilasengine.actores.Actor):

    def iniciar(self):
        self.imagen = "imagenes/sangre.png"
        self.y = 300
        self.x = pilas.azar(-285, 285)
        self.velocidad = 0
        self.radio_de_colision = 35
        self.escala = 0.70

    def actualizar(self):
        self.velocidad += 0.05
        self.y -= self.velocidad
        self.rotacion += 2

        if self.y < -400:
            self.eliminar()
            
            
            
            
            

########################################






##########ESCENAS##################
class EscenaMenu(pilasengine.escenas.Escena):
    def iniciar (self):
        #self.fondo_menu = pilas.fondos.Volley()
        self.fondo_menu = pilas.fondos.Fondo("imagenes/menu.png")
        
        self.sonido_de_menu = pilas.musica.cargar("imagenes/soundmenu.mp3")
        self.sonido_de_menu.reproducir(repetir=True)
        
        #Titulo del juego
        self.Nombre_de_mi_juego = pilas.actores.Texto(u'VAMPIRE DODGE')
        self.Nombre_de_mi_juego.color = pilas.colores.rojo
        self.Nombre_de_mi_juego.y = 170
        ################
        self.Mi_Menu = pilas.actores.Menu(
                    [
                                (u'Jugar', self.Ir_al_juego),
                                (u'Ayuda', self.Ir_a_ayuda),
                                (u'Salir', self.Salir_de_Pilas)
                                ])
        ####################
        
        
    def actualizar (self):
        pass
        
    def Salir_de_Pilas(self):
        pilas.terminar()
        
    def Ir_al_juego(self):
        pilas.escenas.EscenaJuego()
        self.sonido_de_menu.detener()
        
    def Ir_a_ayuda(self):
        pilas.escenas.EscenaAyuda()
        

        
class EscenaJuego(pilasengine.escenas.Escena):
    def iniciar (self):
        
        self.fondo_juego = pilas.fondos.Fondo("imagenes/juego.png")
        
        self.sonido_sangre=self.pilas.sonidos.cargar('imagenes/coin.wav')
        self.sonido_perder=self.pilas.sonidos.cargar('imagenes/perder.wav')
        
        self.calabazas=[]
        
        self.crear_personaje()
        
        self.pilas.actores.Sonido()
        self.puntos= self.pilas.actores.Puntaje (x=230, y=200, color=pilas.colores.blanco)
        
        #Boton regresar
        self.Boton_Volver =pilas.interfaz.Boton('Volver al menu')
        self.Boton_Volver.y = 210
        self.Boton_Volver.x = -230
        self.Boton_Volver.conectar(self.Volver)
        #######
        self.enemigos =[]
        
        pilas.tareas.siempre(2, self.crear_sangre)
        pilas.tareas.siempre(2, self.crear_calabaza)
    
    def crear_personaje(self):
        self.pilas.actores.Vampiro()
        #vampiro.definir_enemigos(self.calabazas)
        self.colisiones.agregar('vampiro','calabaza', self.destruido)
        self.colisiones.agregar('vampiro','sangre',self.mejorar)
         
               
    def crear_calabaza(self):
        self.pilas.actores.Calabaza()
        
    def crear_sangre(self):
        self.pilas.actores.Sangre()
        
    def mejorar(self,vampiro,sangre):
        sangre.eliminar()
        self.sonido_sangre.reproducir()
        
        self.puntos.aumentar(1)
            
        
    def destruido(self,vampiro,calabaza):
        vampiro.eliminar()
        self.sonido_perder.reproducir()
        self.pilas.avisar("Game over. Conseguiste %d puntos" %(self.puntos.obtener()))
      
   
        
        
            
    def Volver(self):
        pilas.escenas.EscenaMenu()
        
        
    def actualizar (self):
        pass
        
class EscenaAyuda(pilasengine.escenas.Escena):
    def iniciar (self):
        self.pilas.fondos.Fondo("imagenes/ayuda.png")
        self.crear_texto_ayuda()
        self.pulsa_tecla_escape.conectar(self.cuando_pulsa_tecla)
        
    def crear_texto_ayuda(self):
        self.pilas.actores.Texto("Mover el personaje con las flechas,",y=50)
        self.pilas.actores.Texto("esquivar las calabazas e intentar",y=0)
        self.pilas.actores.Texto(" recojer las sacos de sangre.",y=-50)
        #self.pilas.actores.Texto(MENSAJE_AYUDA, y=200)
        self.pilas.avisar("pulsa ESC para regresar")
        
    def cuando_pulsa_tecla(self, *k,**kw):
        self.pilas.escenas.EscenaMenu()
        
    def actualizar (self):
        pass
 
                    
##################################                   


 
                                                       
pilas.comportamientos.vincular(ComportamientoNormal)
pilas.comportamientos.vincular(ComportamientoCaminar)
pilas.comportamientos.vincular(ComportamientoSaltar)

                                                                                               
pilas.actores.vincular(Vampiro)
pilas.actores.vincular(Calabaza)
pilas.actores.vincular(Sangre)
                           
pilas.escenas.vincular(EscenaMenu)
pilas.escenas.vincular(EscenaJuego)
pilas.escenas.vincular(EscenaAyuda)

pilas.escenas.EscenaMenu()
      
pilas.ejecutar()