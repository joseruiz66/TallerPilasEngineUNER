'''
Created on 19 nov. 2017
Muestra la pantalla que termino el juego
@author: Ruiz Jose
'''
import pilasengine

class EscenaPerdisteUnaVida(pilasengine.escenas.Escena):

    def iniciar(self, juego):
        self.pilas.fondos.Pasto()
        self.juego = juego
        self.juego.detener_juego()
        self.manchas = self.pilas.actores.Actor(imagen="../data/imagenes/manchas.png")
        self.manchas.transparencia = 80

        self.textoFin = self.pilas.actores.Texto("Perdiste una vida!!!", fuente = "../data/fuentes/Bangers.ttf", magnitud = 40)
        self.textoFin.color = pilasengine.colores.rojo
        self.animacion_textoEscalar(self.textoFin)

        self.textoAviso = self.pilas.actores.Texto(u"Pulsá espacio para volver a jugar", y=-50)
        self.pilas.eventos.pulsa_tecla.conectar(self.cuando_pulsa_tecla)
        
    def animacion_textoEscalar(self, texto):
        texto.escala = 2
        texto.escala = [1], 1.5

    def cuando_pulsa_tecla(self, evento):
        if evento.texto == " ": # Si es la tecla espacio
            self.juego.iniciar_juego(self.juego.nombre_jugador, self.juego.puntos.obtener(), self.juego.contador_de_vidas.cantidad_de_vidas)
            self.manchas.eliminar()
            self.textoFin.eliminar()
            self.textoAviso.eliminar()