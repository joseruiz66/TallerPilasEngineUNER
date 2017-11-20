'''
Created on 19 nov. 2017
Se definen las habilidades de los enemigos y del premio

@author: Ruiz jose
'''

from pilasengine.habilidades.habilidad import Habilidad

# Creamos una Habilidad personalizada donde el actor aparece a 
# cierta distancia del protagonista
class Aparecer_A_Cierta_Distancia_Del_Protagonista(Habilidad):

    def iniciar(self, receptor):
        self.receptor = receptor
        self.calcular_posicion()

    # Función que genera las coordenadas x e y del enemigo para situarlo en una 
    # posición aleatoria en la ventana.         
    def calcular_posicion(self):        
        # Para esto utilizamos la función randrange()
        # que devuelve un número al azar entre los dos dados.
        x = self.pilas.azar(-320, 320)
        y = self.pilas.azar(-240, 240)
        
        # Para evitar que el enemigo aparezca demasiado cerca del protagonista y 
        # haga el juego imposible, si las coordenadas generadas son menores de 100,
        # se le aleja una distancia de 180. 
        if x >= 0 and x <= 100:
            x = 180
        elif x <= 0 and x >= -100:
            x = -180

        if y >= 0 and y <= 100:
            y = 180
        elif y <= 0 and y >= -100:
            y = -180
            
        # Asigna la posición x e y donde se ubicará el actor
        self.receptor.x,  self.receptor.y =  x,y

        

        
class Agrandar_Actor(Habilidad):        
    def iniciar(self, receptor):
        self.receptor = receptor
        self.agrandar()

    # Efecto de agrardar el actor de 0 a 100%.         
    def agrandar(self):        
        # No queremos que el actor simplemente aparezca, sino que lo haga 
        # con un efecto vistoso. Haremos que el actor aparezca gradualmente,
        # aumentando de tamaño. Para ello vamos a poner el atributo escala del actor
        # creado a 0, de esta manera conseguimos que inicialmente no se visualice.
        self.escala = 0
        
        # La función pilas.utils.interpolar() es capaz de generar animaciones 
        # muy vistosas y variadas. Sus argumentos son:
        # 1)Indica el actor que se va a interpolar.
        # 2)Indica que atributo del actor va a modificarse, en este caso la escala.
        # 3)Valor final de la interpolación 0.5.
        # 4)Duración: es el tiempo que dura ese efecto, en nuestro caso, medio segundo.
        # 5)Tipo de animación, para este ejemplo elegimos ‘elastico’.
        # Esta animación hace que el actor aumente la escala (tamaño) de 0 al 1,
        # es decir, al 100% del tamaño original de la imagen del actor. 
        self.pilas.utils.interpolar(self.receptor, 'escala', 1, duracion=0.5, tipo='elastico')
        
        
        
class Ir_Contra_Actor(Habilidad):        
    def iniciar(self, receptor):
        self.receptor = receptor
        self.ir_contra_el_protagonista()
        
    # Se dirije contra el protagonista
    def ir_contra_el_protagonista(self):        
        # Lista de los movimientos que utilizaremos en la función interpolar. 
        tipo_interpolacion = ["lineal",
                              "aceleracion_gradual",
                              "desaceleracion_gradual",
                              "gradual"]

        # Importamos el módulo random para utilizar la función randrange() 
        from random import choice

        # Con la función random.choice() para elegir uno de un tipo de movimiento 
        # de la lista al azar 
        interpolacion = choice(tipo_interpolacion)
        
        # Dotar al enemigo de un movimiento irregular más impredecible    
        # En este caso vamos a interpolar el atributo 'x' e 'y' del actor. 
        # De manera que el mono se acerque al centro donde se encuentra la torreta
        # con diferentes animaciones. En duracion en  que un enemigo llegue a la torrera
        # esta definida en la variable tiempo. 
        self.pilas.utils.interpolar(self.receptor, 'x', 0, duracion=self.receptor.tiempo_de_choque, tipo=interpolacion)
        self.pilas.utils.interpolar(self.receptor, 'y', self.receptor.y_protagonista, duracion=self.receptor.tiempo_de_choque, tipo=interpolacion)
        
        
        
