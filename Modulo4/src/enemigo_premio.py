'''
Created on 19 nov. 2017
Se define los propiedades y metodos de los actores
@author: Ruiz Jose
'''
from pilasengine.actores.actor import Actor

# Definimos las propiedas y metodos del enemigo
class Enemigo(Actor):
    # El contructor permite definir el tiempo que tarda en acercarse al protagonista
    # y el x e y donde se encuenta el protagonista, esto es porque utilizo la clase
    # Enemigo para la pantalla de presentacion donde creo enemigos que se dirigen al 
    # logo ubicado en una posicion definida
    def iniciar(self, y_protagonista, tiempo_de_choque):
        self.imagen = "../data/imagenes/piedra_grande.png"
        self.radio_de_colision = 25
        self.y_protagonista = y_protagonista
        self.tiempo_de_choque = tiempo_de_choque

        # Dotamos a nuestro enemigo de aparecer en una posición predefinida enemigo.x y enemigo.y
        # La Habilidad "Aparecer_A_Cierta_Distancia_Del_Protagonista" tiene definida la 
        # función calcular_posicion() que nos da una posición al azar dentro de cierta distancia del tanque
        self.aprender("Aparecer_A_Cierta_Distancia_Del_Protagonista")
        
        # Efecto que el actor inicie en cero de escala y aumente a 1.
        self.aprender("Agrandar_Actor")
        
        # Se dirije contra el protagonista
        self.aprender("Ir_Contra_Actor")
    
        # Dotar al enemigo con la habilidad "PuedeExplotar" al ser alcanzado 
        # por un disparo. Esto se consigue a través del método aprender de los actores. 
        self.aprender("PuedeExplotar")
        

class Premio(Actor):
    def iniciar(self):
        self.imagen = "../data/imagenes/estrella.png"
        self.radio_de_colision = 25
        self.tiempo_de_vida = 0
        musica_estrella = self.pilas.musica.cargar("../data/musica/saltar.wav")
        musica_estrella.reproducir(repetir=False)
        
        self.aprender("Aparecer_A_Cierta_Distancia_Del_Protagonista")
        self.aprender("Agrandar_Actor")
        # No queremos que el enemigo simplemente aparezca, sino que lo haga 
        # con un efecto vistoso. Haremos que el enemigo aparezca gradualmente,
        # aumentando de tamaño. Para ello vamos a poner el atributo escala del enemigo
        # creado a 0, de esta manera conseguimos que inicialmente no se visualice.
        self.escala = 0
        
        # La función pilas.utils.interpolar() es capaz de generar animaciones 
        # muy vistosas y variadas. Sus argumentos son:
        # 1)Indica el actor que se va a interpolar.
        # 2)Indica que atributo del actor va a modificarse, en este caso la escala.
        # 3)Valor final de la interpolación 0.5.
        # 4)Duración: es el tiempo que dura ese efecto, en nuestro caso, medio segundo.
        # 5)Tipo de animación, para este ejemplo elegimos ‘elastico’.
        # Esta animación hace que el enemigo aumente la escala (tamaño) de 0 al 0.5,
        # es decir, a la mitad del tamaño original de la imagen del enemigo, 
        # ya que el actor Mono tal como está predefinido en Pilas es muy grande 
        # para el tamaño de la ventana actual.
        self.pilas.utils.interpolar(self, 'escala', 1, duracion=0.5, tipo='elastico')
        # Dotar a la estrella con la habilidad "PuedeExplotarConHumo" al ser alcanzado 
        # por un disparo. Esto se consigue a través del método aprender de los actores. 
        self.aprender("PuedeExplotarConHumo")
    def actualizar(self):
        # Eliminarla pasado un tiempo, cada 3 segundos se lanzará la función
        # eliminar_estrella() que recibe como argumento el objeto estrella.
        # actualizar se ejecuta 60 veces en un segundo por eso es 180
        self.tiempo_de_vida += 1
        if (self.tiempo_de_vida == 180):
            self.eliminar() # pasado los 3 segundos se autoelimina el premio. 
    
