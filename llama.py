import pygame
import random
from confi import *

# Cargar imagen de la llama y escalarla 
img_llama = pygame.image.load('imagen/llama.png')
img_llama = pygame.transform.scale(img_llama, (64, 64))  

# MOVIMIENTO , REBOTE Y ATRAPAR

class Llama(pygame.sprite.Sprite):  #sprite - sub modulo
   
    def __init__(self, x, y):
        super().__init__()   # Clase padre 
        self.image = img_llama  
        self.rect = self.image.get_rect(center=(x, y))  # Posición inicial centrada
        self.velocidad = 2  # Píxeles por frame
    
        # Dirección inicial 
        self.vel_x = random.choice([-self.velocidad, self.velocidad])  
        self.vel_y = random.choice([-self.velocidad, self.velocidad])  

    def update(self):
        
        # Maneja rebote y actualiza posicion
        # Se ejecuta en cada frame del juego
    
        # Mover la llama según su velocidad actual
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        # REBOTE EN BORDES HORIZONTALES 
        if self.rect.left <= 0 or self.rect.right >= ANCHO:
            self.vel_x *= -1  
            
        # REBOTE EN BORDES VERTICALES
        if self.rect.top <= 0 or self.rect.bottom >= ALTO:
            self.vel_y *= -1


class MinijuegoLlama:

    # Creación, movimiento y atrapar a la llama, y las recompensas.

    def __init__(self, jugador):
        
        # Inicializa el minijuego con referencia al jugador para otorgar recompensas.
        
        self.jugador = jugador  # Referencia al jugador para modificar su dinero
        self.sprites = pygame.sprite.Group()  # Grupo de sprites del minijuego
        self.llama = None  
        self.mensaje = None
        self.tiempo_mensaje = 0  # Momento en que se mostró el último mensaje

    def empezar(self):
    
        if self.llama is None:
            self.llama = Llama(ANCHO//2, ALTO//2) # Creamos
            self.sprites.add(self.llama)  # agregamos a grupo de sprites para actualizar

    def actualizar(self): # Movimiento de la llama y deteccion de colisiones
        
        if self.llama: # Actualizar cada frame
            self.sprites.update() # Movimiento + rebote
            
            if self.jugador.rect.colliderect(self.llama.rect):
                self.jugador.dinero += 300  # Si atrapa a la llama
                self.mensaje = "¡Ganaste 300 monedas!"  
                self.tiempo_mensaje = pygame.time.get_ticks()  # Registrar momento del mensaje
                self.sprites.remove(self.llama) # Se elimina
                self.llama = None  # Permitir que se cree una nueva llama después

    def dibujar(self, ventana):
        
        self.sprites.draw(ventana) # Dibujar llama 
        
        # MOSTRAR MENSAJE TEMPORAL

        if self.mensaje and pygame.time.get_ticks() - self.tiempo_mensaje < 1000: # 1 segundo es igual a 1000

            texto = fuente_peq.render(self.mensaje,True , (255, 255, 0)) # Mensaje color amarillo
            ventana.blit(texto, (ANCHO//2 - texto.get_width()//2, 50)) # Dibujar y centrar