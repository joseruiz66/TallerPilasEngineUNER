# -*- coding: utf-8 -*-
'''
Created on 29 nov. 2017
Trabajo Final: Programación de Videojuegos con Pilasengine
@author: Chiarella, Martín - Vargas, Walter
'''

import pilasengine
pilas = pilasengine.iniciar()

class EscenaMenu(pilasengine.escenas.Escena):
    def iniciar(self):
        self.pilas.fondos.Tarde()
        self.texto = pilas.actores.Texto('Shaolin vs. Coop', y=170)
        self.texto.escala = 1.35
        self.texto.color = pilas.colores.negro
        self.shao = pilas.actores.Actor(x=-100, y=65)
        self.shao.imagen = ("Shaolin/shao.png")
        self.shao.escala = 0.95
        self.coop = pilas.actores.Actor(x=100, y=35)
        self.coop.imagen = ("Cooperativista/coop_parado.png")        
        self.menuInicial()
		
    def menuInicial(self):
        self.menu = self.pilas.actores.Menu([
            ("Iniciar Juego", self.iniciarJuego), 
            ("Creditos", self.creditos),
            ("Salir", self.salir)
            ], y = -70)
    def iniciarJuego(self): 
        self.pilas.escenas.EscenaPelea()
    def creditos(self):
        self.pilas.escenas.EscenaCreditos()
    def salir(self):
        self.pilas.escenas.EscenaSalir()         

class EscenaCreditos(pilasengine.escenas.Escena):
    def iniciar(self):
        self.pilas.fondos.Nubes()             
        self.texto = pilas.actores.Texto(
            '- Chiarella, Martin\n- Vargas, Walter', y=100)
        self.texto.color = pilas.colores.amarillo
        self.volver()            
    def volver(self):
        self.menu = self.pilas.actores.Menu([
            ("Volver", self.menuInicial)], y=-170)        
    def menuInicial(self):
        self.pilas.escenas.EscenaMenu()

class EscenaSalir(pilasengine.escenas.Escena):
    def iniciar(self):
        self.pilas.fondos.Noche()
        self.texto = pilas.actores.Texto('Bye bye...')
        pilas.tareas.agregar(2, self.cerrar)        
    def cerrar(self):
        pilas.terminar()

class EscenaPelea(pilasengine.escenas.Escena):
    def regresar(self, evento):
        self.pilas.escenas.EscenaMenu()
    def iniciar(self):
        pilas.fondos.Volley()
        pilas.eventos.pulsa_tecla_escape.conectar(self.regresar)
        
        #########################
        #CONFIGURANDO LAS TECLAS#
        #########################
        #Para SHAOLIN
        teclas_shao = {pilas.simbolos.a: 'izquierda',
                                pilas.simbolos.d: 'derecha',
                                pilas.simbolos.w: 'arriba',
                                pilas.simbolos.ESPACIO: 'disparar',
                                pilas.simbolos.t: 'ganador',
                                pilas.simbolos.y: 'muerto'}
        mando_shao = pilas.control.Control(teclas_shao)
        
        #Para COOPERATIVISTA
        teclas_coop = {pilas.simbolos.IZQUIERDA: 'izquierda',
                                pilas.simbolos.DERECHA: 'derecha',
                                pilas.simbolos.ARRIBA: 'arriba',
                                pilas.simbolos.CTRL: 'disparar',
                                pilas.simbolos.o: 'ganador',
                                pilas.simbolos.p: 'muerto'}
        mando_coop = pilas.control.Control(teclas_coop) 

        #########################
        #    "CODIGO SHAOLIN"    #
        #########################
        class MyShaolin(pilasengine.actores.Actor):
            def iniciar(self, x=0, y=0):
                self.vida = pilas.actores.Energia(x=-180, y=200,color_relleno=pilas.colores.azul)
                self.x = x
                self.y = y
                self.crear_figura_de_colision_rectangular(0, -80, 100, 150)
                self.aprender(pilas.habilidades.LimitadoABordesDePantalla) #Evita que el personaje salga de la pantalla.
                self.hacer_inmediatamente(ParadoShao)                       
            def actualizar(self):
                if self.figura_de_colision.figuras_en_contacto:
                    self.vida.progreso -= 10
                                                                                                                
        class ParadoShao(pilasengine.comportamientos.Comportamiento):
        #"Define el comportamiento del personaje mientras esta quieto"  
            def iniciar(self, receptor):
                self.receptor = receptor
                self.control = mando_shao
                self.receptor.imagen = self.pilas.imagenes.cargar_grilla("Shaolin/shao_parado.png", 4)
                self.receptor.centro = ("centro", "abajo")
            def actualizar(self):
                self.receptor.imagen.avanzar(7) #Velocidad de la animacion al estar parado.
                if self.control.derecha or self.control.izquierda:
                    self.receptor.hacer_inmediatamente(CaminarShao) #Camina si a o d.        
                if self.control.arriba:
                    self.receptor.hacer_inmediatamente(SaltoShao) #Salta si w.
                if self.control.disparar:
                    self.receptor.hacer_inmediatamente(DisparoShao) #Dispara con 'g'.   
                if self.control.ganador:
                    self.receptor.hacer_inmediatamente(VictoriaShao) #Pose de victoria apretando 't'.
                if self.control.muerto:
                    self.receptor.hacer_inmediatamente(MorirShao) #Muere apretando 'y'.

        class CaminarShao(pilasengine.comportamientos.Comportamiento):
        #"Permite que el personaje camine de un lado al otro"  
            def iniciar(self, receptor):
                self.receptor = receptor
                self.control = mando_shao
                self.receptor.imagen = self.pilas.imagenes.cargar_grilla("Shaolin/shao_caminando.png", 4)
                self.receptor.centro = ("centro", "abajo")        
            def actualizar(self):
                self.receptor.imagen.avanzar(10) #Determina la velocidad de la animacion al moverse.            
                if self.control.derecha:
                    self.receptor.x += 5 #Determina la velocidad de desplazamiento hacia la derecha.
                    self.receptor.espejado = False
                elif self.control.izquierda:
                    self.receptor.x -= 5 #Idem hacia la izquierda.
                    self.receptor.espejado = True          
                if self.control.arriba: #Permite saltar durante el movimiento.
                    self.receptor.hacer_inmediatamente(SaltoShao)
                if self.control.disparar: #Permite disparar en movimiento pero detiene al personaje.                      
                    self.receptor.hacer_inmediatamente(DisparoShao)
                if self.control.muerto: #Permite morir en movimiento.                      
                    self.receptor.hacer_inmediatamente(MorirShao)
                if not self.control.derecha and not self.control.izquierda: #Detiene el avance al soltar la tecla.
                    self.receptor.hacer_inmediatamente(ParadoShao)
                    
        class SaltoShao(pilasengine.comportamientos.Comportamiento):
        #"Permite que el personaje haga un salto"   
            def iniciar(self, receptor):
                self.receptor = receptor
                self.control = mando_shao
                self.receptor.imagen = self.pilas.imagenes.cargar_grilla("Shaolin/shao_saltando.png", 3)
                self.receptor.centro = ("centro", "abajo")
                self.y_inicial = self.receptor.y
                self.vy = 17 #Determina la altura del salto.     
            def actualizar(self):
                self.receptor.y += self.vy
                self.vy -= 0.7
                self.distancia_al_suelo = self.receptor.y - self.y_inicial
                self.receptor.altura_del_salto = self.distancia_al_suelo
                #Se detiene al llegar al suelo.
                if self.distancia_al_suelo < 0:
                    self.receptor.y = self.y_inicial
                    self.receptor.altura_del_salto = 0
                    self.receptor.hacer_inmediatamente(ParadoShao)                 
                #Permite el movimiento en el aire.
                if self.control.derecha:
                    self.receptor.x += 5
                    self.receptor.espejado = False
                elif self.control.izquierda:
                    self.receptor.x -= 5
                    self.receptor.espejado = True
                #Permite morir en el aire
                if self.control.muerto:                      
                    self.receptor.hacer_inmediatamente(MorirShao)

        class DisparoShao(pilasengine.comportamientos.Comportamiento):
            def iniciar(self, receptor):
                self.receptor = receptor
                self.control = mando_shao
                self.receptor.imagen = self.pilas.imagenes.cargar_grilla("Shaolin/shao_ataque.png", 2) 
                self.receptor.centro = ("centro", "abajo")
            def actualizar(self):
                self.receptor.imagen.avanzar(-45)
                if self.receptor.imagen.avanzar() == False:
                    self.receptor.hacer_inmediatamente(ParadoShao)

        class MorirShao(pilasengine.comportamientos.Comportamiento):
        #"Realiza una animacion de muerte"
            def iniciar(self, receptor):
                self.receptor = receptor         
                self.receptor.imagen = self.pilas.imagenes.cargar_grilla("Shaolin/shao_caida.png", 2) 
                self.receptor.centro = ("centro", "abajo")
                self.x = 0
            def actualizar(self):
                self.receptor.imagen.avanzar(-55)
                if self.receptor.imagen.avanzar() == False:
                    self.receptor.imagen = ("Shaolin/shao_muerto.png")
                    self.receptor.centro = ("centro", "abajo")
                #El cuerpo cae despues de morir. 
                self.distancia_al_suelo =  -200 - self.receptor.y   
                if self.receptor.y > -200:
                    self.receptor.y -= 7

        class VictoriaShao(pilasengine.comportamientos.Comportamiento):
        #"Realiza una pose de victoria"
            def iniciar(self, receptor):
                self.receptor = receptor 
                self.receptor.imagen = self.pilas.imagenes.cargar_grilla("Shaolin/shao_ganador.png", 2)
                self.receptor.centro = ("centro", "abajo")
                self.receptor.decir('Yo gano')
                
        #################################
        #    " CODIGO COOPERATIVISTA"    #
        #################################
        class MyCooperativista(pilasengine.actores.Actor):
            def iniciar(self, x=0, y=0):
                self.vida = pilas.actores.Energia(x=180, y=200,color_relleno=pilas.colores.amarillo)
                self.x = x
                self.y = y
                self.crear_figura_de_colision_circular(50, x=0, y=-50)
                self.aprender(pilas.habilidades.LimitadoABordesDePantalla) #Evita que el personaje salga de la pantalla
                self.hacer_inmediatamente(ParadoCoop)       
            def actualizar(self):
                if self.figura_de_colision.figuras_en_contacto:
                    self.vida.progreso -= 10
                                                                                                                        
        class ParadoCoop(pilasengine.comportamientos.Comportamiento):
        #"Define el comportamiento del personaje mientras esta quieto"  
            def iniciar(self, receptor):
                self.receptor = receptor
                self.control = mando_coop
                self.receptor.imagen = ("Cooperativista/coop_parado.png")
                self.receptor.centro = ("centro", "abajo")
            def actualizar(self):
                if self.control.derecha or self.control.izquierda:
                    self.receptor.hacer_inmediatamente(CaminarCoop) #Camina si izq o der           
                if self.control.arriba:
                    self.receptor.hacer_inmediatamente(SaltoCoop) #Salta si arriba
                if self.control.disparar:
                    self.receptor.hacer_inmediatamente(DisparoCoop) #Dispara con 'l'.   
                if self.control.ganador:
                    self.receptor.hacer_inmediatamente(VictoriaCoop) #Pose de victoria apretando 'o'.
                if self.control.muerto:
                    self.receptor.hacer_inmediatamente(MorirCoop) #Muere apretando 'p'.

        class CaminarCoop(pilasengine.comportamientos.Comportamiento):
        #"Permite que el personaje camine de un lado al otro"  
            def iniciar(self, receptor):
                self.receptor = receptor
                self.control = mando_coop
                self.receptor.imagen = self.pilas.imagenes.cargar_grilla("Cooperativista/coop_caminando.png", 4)
                self.receptor.centro = ("centro", "abajo")        
            def actualizar(self):
                self.receptor.imagen.avanzar(10) #Determina la velocidad de la animacion al moverse            
                if self.control.derecha:
                    self.receptor.x += 5 #Determina la velocidad de desplazamiento hacia la derecha
                    self.receptor.espejado = True
                elif self.control.izquierda:
                    self.receptor.x -= 5 #Idem hacia la izquierda
                    self.receptor.espejado = False           
                if self.control.arriba: #Esto permite saltar durante el movimiento
                    self.receptor.hacer_inmediatamente(SaltoCoop)
                if self.control.disparar: #Permite disparar en movimiento pero detiene al personaje.                      
                    self.receptor.hacer_inmediatamente(DisparoCoop)
                if self.control.muerto: #Permite morir en movimiento.                      
                    self.receptor.hacer_inmediatamente(MorirCoop)
                if not self.control.derecha and not self.control.izquierda: #Detiene el avance al soltar la tecla.
                    self.receptor.hacer_inmediatamente(ParadoCoop)
                    
        class SaltoCoop(pilasengine.comportamientos.Comportamiento):
        #"Permite que el personaje haga un salto"   
            def iniciar(self, receptor):
                self.receptor = receptor
                self.control = mando_coop
                self.receptor.imagen = self.pilas.imagenes.cargar_grilla("Cooperativista/coop_caminando.png", 4)
                self.receptor.centro = ("centro", "abajo")
                self.y_inicial = self.receptor.y
                self.vy = 17 #Determina la altura del salto     
            def actualizar(self):
                self.receptor.y += self.vy
                self.vy -= 0.7
                distancia_al_suelo = self.receptor.y - self.y_inicial
                self.receptor.altura_del_salto = distancia_al_suelo
                #Se detiene al llegar al suelo.
                if distancia_al_suelo < 0:
                    self.receptor.y = self.y_inicial
                    self.receptor.altura_del_salto = 0
                    self.receptor.hacer_inmediatamente(ParadoCoop)                 
                #Permite el movimiento en el aire.
                if self.control.derecha:
                    self.receptor.x += 5
                    self.receptor.espejado = True
                elif self.control.izquierda:
                    self.receptor.x -= 5
                    self.receptor.espejado = False 
                #Permite morir en el aire
                if self.control.muerto:                      
                    self.receptor.hacer_inmediatamente(MorirCoop)
                    
        class DisparoCoop(pilasengine.comportamientos.Comportamiento):
            def iniciar(self, receptor):
                self.receptor = receptor
                self.control = mando_coop
                self.receptor.imagen = self.pilas.imagenes.cargar_grilla("Cooperativista/coop_ataque.png", 2)
                self.receptor.imagen.definir_cuadro(1) 
                self.receptor.centro = ("centro", "abajo")
            def actualizar(self):
                self.receptor.imagen.avanzar(-50)
                if self.receptor.imagen.avanzar() == False:
                    self.receptor.hacer_inmediatamente(ParadoCoop)

        class MorirCoop(pilasengine.comportamientos.Comportamiento):
        #"Realiza una animacion de muerte"
            def iniciar(self, receptor):
                self.receptor = receptor         
                self.receptor.imagen = self.pilas.imagenes.cargar_grilla("Cooperativista/coop_muerto.png", 2) 
                self.receptor.centro = ("centro", "abajo")
            def actualizar(self):
                self.receptor.imagen.avanzar(-55)
                if self.receptor.imagen.avanzar() == False:
                    self.receptor.imagen.definir_cuadro(1)
                    if self.receptor.obtener_espejado() == True:
                        self.receptor.rotacion = 90
                    else:
                        self.receptor.rotacion = -90
                #El cuerpo cae despues de morir.
                self.distancia_al_suelo =  -190 - self.receptor.y   
                if self.receptor.y > -190:
                    self.receptor.y -= 7

        class VictoriaCoop(pilasengine.comportamientos.Comportamiento):
        #"Realiza una pose de victoria"
            def iniciar(self, receptor):
                self.receptor = receptor 
                self.receptor.imagen = ("Cooperativista/coop_ganador.png")
                self.receptor.centro = ("centro", "abajo")
                self.receptor.decir('Yo gano')

        #########################
        #    "CODIGO MUNICIONES"    #
        #########################
        #Un shuriken para que lance el Shaolin.
        class Shuriken(pilasengine.actores.Actor):
            def pre_iniciar(self, x=0, y=0):
                self.x = x
                self.y = y
                self.imagen = self.pilas.imagenes.cargar('Shaolin/shuriken.png')
                self.rotacion = 0
                self.escala = 0.5
                self.radio_de_colision = 20
                self.hacer(self.pilas.comportamientos.Proyectil, 
                            velocidad_maxima=7,
                            aceleracion=5,
                            angulo_de_movimiento=0,
                            gravedad=0)
                self.aprender(pilasengine.habilidades.eliminarse_si_sale_de_pantalla)
            def actualizar(self):
                self.rotacion -= 100
                if self.figura_de_colision.figuras_en_contacto:
                    self.eliminar()
                    
        #Una dinamita para que lance el Cooperativista.            
        class TNT(pilasengine.actores.Actor):
            def pre_iniciar(self, x=0, y=0):
                self.x = x
                self.y = y
                self.imagen = self.pilas.imagenes.cargar_grilla('Cooperativista/tnt.png', 2)
                self.imagen.definir_cuadro(1)
                self.rotacion = 0
                self.escala = 1
                self.radio_de_colision = 20
                self.hacer(self.pilas.comportamientos.Proyectil, 
                            velocidad_maxima=7,
                            aceleracion=5,
                            angulo_de_movimiento=180,
                            gravedad=0)
                self.aprender(pilasengine.habilidades.eliminarse_si_sale_de_pantalla)
            def actualizar(self):
                self.rotacion -= 10
                if self.figura_de_colision.figuras_en_contacto:
                    self.eliminar()
                    
        #####################
        #"Las vinculaciones"#
        #####################
        #SHAOLIN
        pilas.actores.vincular(MyShaolin)
        pilas.comportamientos.vincular(ParadoShao)
        pilas.comportamientos.vincular(CaminarShao)
        pilas.comportamientos.vincular(SaltoShao)
        pilas.comportamientos.vincular(DisparoShao)
        pilas.comportamientos.vincular(MorirShao)
        pilas.comportamientos.vincular(VictoriaShao)
        #COOPERATIVISTA        
        pilas.actores.vincular(MyCooperativista)
        pilas.comportamientos.vincular(ParadoCoop)
        pilas.comportamientos.vincular(CaminarCoop)
        pilas.comportamientos.vincular(SaltoCoop)
        pilas.comportamientos.vincular(DisparoCoop)
        pilas.comportamientos.vincular(MorirCoop)
        pilas.comportamientos.vincular(VictoriaCoop)
        
        ########################
        #CREANDO LOS PERSONAJES#
        ########################
        #Instanciando.
        shao = pilas.actores.MyShaolin(x=-200, y=-200) 
        coop = pilas.actores.MyCooperativista(x=200, y=-190)
            
        #Aprendiendo a disparar.
        
        #Nuevas teclas para poder disparar.
            #Para Shaolin.
        tecla_disparo_shao = {pilas.simbolos.ESPACIO: 'boton'}
        mando_disparo_shao = pilas.control.Control(tecla_disparo_shao)
            #Para Cooperativista.
        tecla_disparo_coop = {pilas.simbolos.CTRL: 'boton'}
        mando_disparo_coop = pilas.control.Control(tecla_disparo_coop)
        #Shaolin aprendiendo.            
        shao.aprender(pilas.habilidades.Disparar,
                 municion = Shuriken,
                 parametros_municion = {},
                 grupo_enemigos=[],
                 cuando_elimina_enemigo=None,
                 frecuencia_de_disparo=2,
                 angulo_salida_disparo=0,
                 distancia=0,
                 offset_origen_actor=(100,90),
                 cuando_dispara=None,
                 escala=0.5,
                 rotacion_disparo=100,
                 control=mando_disparo_shao)
        #Cooperativista aprendiendo.         
        coop.aprender(pilas.habilidades.Disparar,
                 municion = TNT,
                 parametros_municion = {},
                 grupo_enemigos=[],
                 cuando_elimina_enemigo=None,
                 frecuencia_de_disparo=2,
                 angulo_salida_disparo=0,
                 distancia=0,
                 offset_origen_actor=(-100,60),
                 cuando_dispara=None,
                 escala=0.9,
                 rotacion_disparo=100,
                 control=mando_disparo_coop)                 
        
        #Creando miniaturas para las barras de vida.
        pilas.actores.Actor(-300,200,imagen='Shaolin/mini_shao.png')
        pilas.actores.Actor(300,200,imagen='Cooperativista/mini_coop.png')

            
pilas.escenas.vincular(EscenaMenu)
pilas.escenas.vincular(EscenaPelea)
pilas.escenas.vincular(EscenaCreditos)
pilas.escenas.vincular(EscenaSalir)
pilas.escenas.EscenaMenu()
pilas.ejecutar()