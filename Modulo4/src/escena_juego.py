# -*- coding: utf-8 -*-
"""
 Created on 19 nov. 2017
    Módulo: Juego
    Este módulo contiene las vidas que va a tener el usuario y la cantidad de puntos al iniciar.
    En ella se generan los personajes, se llama a las tareas de actualizar a los personajes, chequear vidas, etc.
 
 @author: Ruiz Jose - Fabian Pineda 

 """
import pilasengine
        
# juego
class EscenaJuego(pilasengine.escenas.Escena):

    # Velocidad de los enemigos se acercan a la torreta.
    # Esta variable se usará para hacer más fácil o más difícil el juego.
    tiempo = 6
    # Variable booleana (bandera) que controlará si el juego ha terminado o no.
    fin_de_juego = False
    
    # Definimos un objeto del tipo actor Bala pero utilizamos pilasengine 
    # en vez de pilas, esto es porque solo queremos indicar el tipo de actor que 
    # vamos a utilizar pero no vamos a crearlo todavía porque eso no usamos Bala() 
    municion_bala_simple = pilasengine.actores.Bala

    # Definimos un objeto del tipo actor BalasDoblesDesviadas para asignar como
    # bonus cuando destruye una estrella
    municion_doble_bala = pilasengine.actores.BalasDoblesDesviadas
    
    # Lista de enemigos vacía, es el grupo de enemigos a los que se va a disparar.
    enemigos = []

    def iniciar(self, nombre_jugador):
        self.nombre_jugador= nombre_jugador
        self.iniciar_juego(nombre_jugador,puntaje="0",vidas=3)
        
    
    def crear_escenario(self, nombre_jugador, puntaje,vidas):
        self.pilas.fondos.Pasto()
        self.reproducir_musica_juego()
        self.pilas.avisar("Pulsa ESC para regresar")
        self.pulsa_tecla_escape.conectar(self.cuando_pulsa_tecla_escape)
        # Añadir un marcador al juego, lo ubicamos en la esquina superior derecha, 
        # de color blanco. El marcador es un actor predefinido en pilas de tipo Puntaje.
        # Los actores en pilas son objetos que aparecen en pantalla,
        # tiene una posición determinada y se pueden manipular.
        self.puntos = self.pilas.actores.Puntaje(x=230, y=200, color=self.pilas.colores.blanco)
        # El objeto puntos lo utilizamos para cambiar las propiedades del marcador. 
        # Ampliar el tamaño del marcador.
        self.puntos.magnitud = 40
        self.puntos.definir(puntaje)

        # Efecto que el actor inicie en cero de escala y aumente a 1.
        self.puntos.aprender("Agrandar_Actor")
        
        texto_nombre = self.pilas.actores.Texto("Jugador: " + nombre_jugador, x=0, y=220, magnitud=15)
        texto_nombre.color = self.pilas.colores.negro
        
        # Añadir el conmutador de Sonido al juego, 
        # Esto permite activar/desactivar el sonido haciendo click sobre él.
        self.pilas.actores.Sonido()

        # Invoco al metodo crear_contador_de_vidas y guardo el objeto
        # como una propiedad de la clase EscenaMenu
        self.contador_de_vidas=self.crear_contador_de_vidas(vidas)
        
    def reproducir_musica_juego(self):
        self.musica_fondo = self.pilas.musica.cargar("../data/musica/musica.mp3")
        self.musica_fondo.reproducir(repetir=True)
        
        
    # Función que se llamará cuando la munición que disparamos impacte
    # con un enemigo. Sus parámetros son disparo y enemigo.
    def enemigo_destruido(self, disparo, enemigo):
        # El mono al ser alcanzado por una munición explota pero no se elimina,
        # entonces se debe eliminar el mono con el método eliminar(). 
        enemigo.eliminar()
        # La munición también se debe eliminar al colisionar con un enemigo. 
        disparo.eliminar()
        # Actualizar en uno la puntuación del marcador con el método aumentar(1)
        self.puntos.aumentar(1)
    
    def crear_personajes(self):
        # Para crear el objeto torreta debemos pasarles los siguientes argumentos:
        # el tipo de munición que va a emplear, la lista de enemigos, 
        # la función que se debe llamar cuando colisionan una munición y un enemigo. 
        
        # Creamos el objeto torreta, obsérvese que al argumento cuando_elimina_enemigo 
        # le pasamos enemigo_destruido y no enemigo_destruido() ya que queremos pasarle
        # la función que ha de usarse y no el resultado de ejecutarla.
        self.torreta = self.pilas.actores.Protagonista( municion_bala_simple=self.municion_bala_simple,
                                        enemigos=self.enemigos,
                                        cuando_elimina_enemigo=self.enemigo_destruido)        


        
    # Cada vez que se llame hay que crear un nuevo enemigo
    def crear_enemigo(self):
        # Crear un objeto enemigo del tipo de actor mono
        enemigo = self.pilas.actores.Enemigo(0, self.tiempo)
        
        # Añadirlo a la lista de enemigos.
        self.enemigos.append(enemigo)
        
        # Mientras dure el juego, se tienen que crear monos (hay que devolver True) y 
        # cuando éste finalice, no (hay que devolver False).
        if not self.fin_de_juego:
            return True
        else:
            return False

    
    def crear_contador_de_vidas(self, vidas):
        from contador_de_vidas import ContadorDeVidas
        return ContadorDeVidas(self.pilas, vidas)

    
    # El jugador pierde cuando no es capaz de eliminar a todos los monos y uno de ellos  
    # alcanza la torreta.     
    def perder(self, torreta, enemigo):
        #intensidad=3, tiempo=0.3
        self.pilas.camara.vibrar(3,0.3)
        enemigo.eliminar()
        # elimino todos los otros monos que estan en la pantalla
        for cada_enemigo in self.enemigos:
            cada_enemigo.eliminar()
        self.detener_juego()
        #Invoca a la función eliminar() del actor torreta
        torreta.eliminar()
        self.contador_de_vidas.quitar_una_vida()
        if not self.contador_de_vidas.le_quedan_vidas():
            self.mostrar_escena_game_over()
            # Indicar ﬁn de juego
            self.fin_de_juego = True
            # Mostramos un breve mensaje en la parte inferior de la ventana,
            # con el puntaje conseguido a través del método obtener() del actor Puntaje.
            self.pilas.avisar("GAME OVER. Conseguiste %d puntos" %(self.puntos.obtener()))

        else:
            self.pilas.escenas.EscenaPerdisteUnaVida(self)

    # Asigna a la torreta munición simple.
    def asignar_arma_simple(self):
        self.torreta.municion = self.municion_bala_simple
        # Esta función no devolveremos True para que, así, se ejecute una única vez.

    # Asigna a la torreta munición doble.
    def asignar_arma_doble(self, estrella, disparo):
        # Cambiar la munición de la torreta a balas_dobles
        self.torreta.municion = self.municion_doble_bala
        # Eliminar la estrella a la que hemos disparado y acertado
        
        #estrella.aprender("PuedeExplotarConHumo")
        estrella.eliminar()
        disparo.eliminar()
        #darle una temporalidad a la munición extra que acabamos de activa
        # A los 10 segundos se ejecuta la función asignar_arma_simple()
        # que hace lo propio, devolviendo la torreta a su munición estándar.
        self.pilas.escena_actual().tareas.siempre(10, self.asignar_arma_simple)
        # Avisar de cambio de munición con un texto
        self.pilas.avisar("ARMA MEJORADA")
        # Esta función no devolveremos True para que, así, se ejecute una única vez.




    # Cada cierto tiempo aparece una estrella en pantalla que, si es destruida,
    # cambia temporalmente la munición que usa la torreta a unas balas dobles.    
    def crear_estrella(self):
        # El argumento del if tiene la misión de generar un número aleatorio en el rango 
        # del 0 al 10 y, solo si dicho número es mayor de 5, se procede a continuar. 
        if self.pilas.azar(0, 10) > 5:
            # No se debe crear una estrella si ya estamos en periodo de bonus,
            # ya que ya hemos sido premiados. Para ello, vamos a utilizar la función
            # de Python issubclass(). Esta función toma dos argumentos y devuelve True 
            # si son instancias de la misma clase. Por lo tanto, devolverá True 
            # (y en consecuencia, se continuará con la ejecución del contenido del
            # bloque if) si la torreta está usando la munición de balas simples.
            # La torreta posee la habilidad de DispararConClick una determinada 
            # munición que es la que estamos chequeando.
            if (self.torreta.habilidades.DispararConClick.municion == self.municion_bala_simple):

                # crear la Premio
                estrella = self.pilas.actores.Premio()
                self.reproducir_musica_juego()
                # Permitir que la torreta pueda destruirla, cuando la estrella colisione
                # con uno de los torreta.habilidades.DispararConClick.proyectiles se 
                # lanzará la función asignar_arma_doble().
                self.pilas.escena_actual().colisiones.agregar(estrella,
                                         self.torreta.habilidades.DispararConClick.proyectiles,
                                         self.asignar_arma_doble)
                

        
    
    def aumentar_nivel_dificultad(self):
        # Disminuir la variable tiempo que acelera el movimiento de los monos
        self.tiempo -= 1
        # Avisamos al jugador que aumenta la dificultad a través de un aviso 
        self.pilas.avisar("HURRY UP!!! Se vienen los monos.")
        # No queremos que la variable tiempo llegue a 0, entonces el mayor nivel de
        # dificultad es medio segundo.
        if self.tiempo < 1:
            self.tiempo = 0.5
        
        # Devolvemos True para asegurarnos que la tarea repetitiva no deje de realizarse
        return True
    
    def mostrar_escena_game_over(self):
        self.pilas.escenas.EscenaGameOver(self)


    def cuando_pulsa_tecla_escape(self, *k, **kv):
        # Si es la tecla ESC
        self.musica_fondo.detener()
        self.pilas.escenas.EscenaMenu()    
        
    def iniciar_juego(self, nombre_jugador,puntaje, vidas):
        self.crear_escenario(nombre_jugador,puntaje,vidas)
        self.crear_personajes()
        # La manera de conseguir con Pilas que se realice una tarea cada cierto tiempo 
        # es usar la función tareas.siempre(1, crear_enemigo), debemos indicarle el 
        # tiempo en segundos que queremos que pase cada vez que se realice la tarea 
        # y la función que queremos que se invoque en este caso "crear_enemigo" 
        # cada un segundo. Para que la tarea siga ejecutandose deben devolver True.
        # Un juego más elaborado consta de diferentes niveles, pantallas, 
        # presentaciones, en el siguiente practico explicaremos el método escena_actual().
        self.pilas.escena_actual().tareas.siempre(1, self.crear_enemigo)

        # Crear un bonus (premio) para que el jugador cambie de munición.
        # Invocar a la función crear_estrella cada 5 segundos.
        self.pilas.escena_actual().tareas.siempre(5, self.crear_estrella)

        # Aumentar la diﬁcultad del juego cada 20 segundos.
        # Agregamos la tarea de, cada 20 segundos, lanzar la función reducir_tiempo().
        self.pilas.escena_actual().tareas.siempre(20, self.aumentar_nivel_dificultad)

        # Cuando un mono colisiona con la torreta, el juego tiene que realizar las tareas 
        # que se encargan de darlo por terminado. Para ello, usamos método colisiones.agregar()
        # predefinido en Pilas para añadir un tipo de colisión y su respuesta. Este método 
        # genera que se invoque la función que le pasamos como tercer argumento perder() cuando 
        # colisionen los actores indicados en los otros dos argumentos (torreta y enemigos).
        self.pilas.escena_actual().colisiones.agregar(self.torreta, self.enemigos, self.perder)
        
        # Agregamos un aviso inicial con las instrucciones de juego, indicando que se
        # usa el ratón y se dispara al hacer click. La "u" delante de la cadena de texto
        # significa versión unicode de caracteres y evita que se muestren caracteres
        # extraños al usar el acento en ‘ratón’.
        self.pilas.avisar(u"Mueve el ratón y haz click para destruirlos.")
        

    def detener_juego(self):
        # Eliminamos todas las tareas que se están realizando
        self.pilas.escena_actual().tareas.eliminar_todas()
        self.musica_fondo.detener_gradualmente(segundos = 2)

