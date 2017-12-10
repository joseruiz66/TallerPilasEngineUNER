import pilasengine

import random

pilas = pilasengine.iniciar()
class EscenaMenu(pilasengine.escenas.Escena):
    
  
    
    def iniciar(self):

        
 
        self.pilas.fondos.Fondo(imagen="data/fondomenu.jpg")
        self.crear_titulo_del_juego()
        
        opciones = [
            ("Comenzar a jugar", self.comenzar_a_jugar),
            ("Ver ayuda", self.mostrar_ayuda_del_juego),
            ("Salir", self.salir_del_juego)
            ]
        self.pilas.actores.Menu(opciones, y=-50)
        
    def crear_titulo_del_juego(self):
        logotipo = self.pilas.actores.Actor(imagen="data/nave_roja/nave.png")
        logotipo.decir("BIENVENIDO")
        logotipo.y = 350
        logotipo.y = [150]

    def comenzar_a_jugar(self):
        self.pilas.escenas.EscenaJuego()
        sonido_de_tick = pilas.sonidos.cargar('data/audio/tick.wav')
        sonido_de_tick.reproducir()

    def salir_del_juego(self):
        self.pilas.terminar()
        sonido_de_tick = pilas.sonidos.cargar('data/audio/tick.wav')
        sonido_de_tick.reproducir()
    def mostrar_ayuda_del_juego(self):
        self.pilas.escenas.EscenaAyuda()
        sonido_de_tick = pilas.sonidos.cargar('data/audio/tick.wav')
        sonido_de_tick.reproducir()

class EscenaJuego(pilasengine.escenas.Escena):
    def iniciar(self):
        self.pilas.fondos.Fondo(imagen="data/fondonave.jpg")  
        puntos=pilas.actores.Puntaje(x=230, y=200, color=pilas.colores.rojo)
        puntos.magnitud=40
        pilas.actores.Sonido()
        municion_bala_simple=pilasengine.actores.Bala 
        municion_doble_bala=pilasengine.actores.BalasDoblesDesviadas
        self.tiempo=6
        self.fin_de_juego=False
       
        enemigos=[]
        
        def enemigo_destruido(disparo, enemigo):
            enemigo.eliminar()
            disparo.eliminar()
            sonido_de_explosion=pilas.sonidos.cargar('data/audio/explosion.wav')
            sonido_de_explosion.reproducir()
            puntos.escala=0
            pilas.utils.interpolar(puntos, 'escala', 1, duracion=0.5, tipo='elastico')
            puntos.aumentar(1)
            
        torreta=pilas.actores.Torreta(municion_bala_simple=municion_bala_simple,
                                                    enemigos=enemigos,
                                                    cuando_elimina_enemigo=enemigo_destruido)
        torreta.imagen="data/nave_roja/nave.png"
        torreta.x=0
        torreta.y=-180
        def crear_enemigo():
            enemigo=pilas.actores.Mono()
            enemigo.imagen="data/alien.png"
            enemigo.escala=0
            pilas.utils.interpolar(enemigo, 'escala', 0.5, duracion=0.5, tipo='elastico')
            enemigo.aprender("PuedeExplotar")
            enemigo.x, enemigo.y =calcular_posicion()
            enemigos.append(enemigo)
            tipo_interpolacion=["lineal",
                                            "aceleracion_gradual",
                                            "desaceleracion_gradual",
                                            "gradual"]
            interpolacion=random.choice(tipo_interpolacion)
            pilas.utils.interpolar(enemigo, 'x', 0, duracion=self.tiempo, tipo=interpolacion)
            pilas.utils.interpolar(enemigo, 'y', -180, duracion=self.tiempo, tipo=interpolacion)
            
            if not self.fin_de_juego:
                return True
            else:
                return False
                
        def calcular_posicion():
            x= random.randrange(-320, 320)
            y= random.randrange(-240, 240)
            
            if x>= 0 and x<=100:
                x=180
            elif x<=0 and x>=-100:
                x=-180
            
            if y>= 0 and x<=100:
                 y=180
            elif y<=0 and x>=-100:
                y=-180
            return x,y
        
        def perder(torreta, enemigo):
   
                alien=pilas.actores.Actor(imagen="data/alien.png")
                alien.x=0
                alien.y=-180
                alien.decir("GAME OVER")
                torreta.eliminar()
                pilas.escena_actual().tareas.eliminar_todas()
                self.fin_de_juego = True
                pilas.avisar("GAME OVER. Conseguiste %d puntos" %(puntos.obtener()))
                    
        def asignar_arma_simple():
            torreta.municion=municion_bala_simple
        
        def asignar_arma_doble(estrella, disparo):
            torreta.municion=municion_doble_bala
            estrella.eliminar()
            pilas.escena_actual().tareas.siempre(10, asignar_arma_simple)
            pilas.avisar("ARMA MEJORADA")
            
        def eliminar_estrella(estrella):
            estrella.eliminar()
            
        def crear_estrella():
            if random.randrange(0, 10)>5:
                if issubclass(torreta.habilidades.DispararConClick.municion,
                                    municion_bala_simple):
                    x, y=calcular_posicion()
                    estrella=pilas.actores.Estrella(x,y)
                    pilas.utils.interpolar(estrella, 'escala', 0.5, duracion=0.5, tipo='elastico')
                    pilas.escena_actual().colisiones.agregar(estrella,
                                                        torreta.habilidades.DispararConClick.proyectiles,
                                                        asignar_arma_doble)
                    pilas.escena_actual().tareas.siempre(3, eliminar_estrella, estrella)
        
        def reducir_tiempo():
   
            
            self.tiempo-=1
            pilas.avisar("HURRY UP!!! Se vienen los aliens.")
            
            if self.tiempo<1:
                self.tiempo=0.5
            return True
            
        pilas.escena_actual().tareas.siempre(1, crear_enemigo)
        
        pilas.escena_actual().tareas.siempre(5, crear_estrella)
        
        pilas.escena_actual().tareas.siempre(20, reducir_tiempo)
        
        pilas.escena_actual().colisiones.agregar(torreta, enemigos, perder)
        
        pilas.avisar(u"Mueve el ratón y haz click para destruirlos.")
        pass

        self.pulsa_tecla_escape.conectar(self.cuando_pulsa_tecla_escape)
       
    
 
    def cuando_pulsa_tecla_escape(self, *k, **kv):
        sonido_de_tick = pilas.sonidos.cargar('data/audio/tick.wav')
        sonido_de_tick.reproducir()
        self.pilas.escenas.EscenaMenu() 


MENSAJE_AYUDA = "Mueve el mouse y haz click para disparar a los aliens."


class EscenaAyuda(pilasengine.escenas.Escena):

    def iniciar(self):
    
        self.pilas.fondos.Fondo(imagen="data/mifondoayuda.jpg")
        self.crear_texto_ayuda()
      
        self.pulsa_tecla_escape.conectar(self.cuando_pulsa_tecla_escape)

    def crear_texto_ayuda(self):
        self.pilas.actores.Texto("Instrucciones del juego", y=200)
        
        self.pilas.actores.Texto(MENSAJE_AYUDA, y=0 )
        
        self.pilas.avisar("Pulsa ESC para regresar")


    def cuando_pulsa_tecla_escape(self, *k, **kv):
        sonido_de_tick = pilas.sonidos.cargar('data/audio/tick.wav')
        sonido_de_tick.reproducir()
        self.pilas.escenas.EscenaMenu()
        

pilas.escenas.vincular(EscenaMenu)
pilas.escenas.vincular(EscenaJuego)
pilas.escenas.vincular(EscenaAyuda)

pilas.escenas.EscenaMenu()


pilas.ejecutar()