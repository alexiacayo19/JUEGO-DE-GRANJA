import pygame
from confi import ANCHO, ALTO
from mapas import colisiones

# --- INVENTARIO ---
class Inventario:
    """
    Gestiona las semillas que posee el jugador.
    Cada tipo de semilla tiene su propio contador.
    """
    def __init__(self):
        self.uvas = 0        # Cantidad de semillas de uva disponibles
        self.naranjas = 0    # Cantidad de semillas de naranja disponibles  
        self.mandarinas = 0  # Cantidad de semillas de mandarina disponibles

# --- JUGADOR ---

img_jugador= pygame.image.load('imagen/jugador.png')
img_jugador= pygame.transform.scale(img_jugador, (64, 64))

class Jugador(pygame.sprite.Sprite):
    """
    Representa al personaje principal del juego.
    Controla movimiento, dinero, selección de semillas e inventario.
    """
    def __init__(self, x, y):
        super().__init__()
        # Crear superficie visual del jugador (rectángulo color piel)
        self.image = img_jugador
        self.rect = self.image.get_rect(center=(x, y))  # Posición inicial
        
        # Propiedades del jugador
        self.velocidad = 5      # Píxeles por frame que se mueve
        self.dinero = 100       # Dinero inicial para comprar semillas
        self.seleccion = None   # Semilla actualmente seleccionada (None, "Uva", "Naranja", "Mandarina")
        self.inventario = Inventario()  # Gestor de semillas disponibles

    def mover(self, teclas):
        """
        Maneja el movimiento del jugador con detección de colisiones.
        Soporta teclas WASD y flechas direccionales.
        """
        # Inicializar vectores de movimiento
        vx = 0  # Velocidad en X (horizontal)
        vy = 0  # Velocidad en Y (vertical)
        
        # --- DETECCIÓN DE TECLAS PRESIONADAS ---
        # Movimiento horizontal (izquierda/derecha)
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]: 
            vx -= self.velocidad  # Mover izquierda
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]: 
            vx += self.velocidad  # Mover derecha
            
        # Movimiento vertical (arriba/abajo)  
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            vy -= self.velocidad  # Mover arriba
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            vy += self.velocidad  # Mover abajo

        # --- MOVIMIENTO HORIZONTAL CON COLISIONES ---
        self.rect.x += vx  # Aplicar movimiento horizontal
        
        # Verificar colisiones después del movimiento
        for r in colisiones:
            if self.rect.colliderect(r):
                # Resolver colisión: empujar al jugador fuera del obstáculo
                if vx > 0:  # Si se movía hacia la derecha
                    self.rect.right = r.left  # Colocar a la izquierda del obstáculo
                if vx < 0:  # Si se movía hacia la izquierda
                    self.rect.left = r.right  # Colocar a la derecha del obstáculo

        # --- MOVIMIENTO VERTICAL CON COLISIONES ---
        self.rect.y += vy  # Aplicar movimiento vertical
        
        # Verificar colisiones después del movimiento
        for r in colisiones:
            if self.rect.colliderect(r):
                # Resolver colisión: empujar al jugador fuera del obstáculo
                if vy > 0:  # Si se movía hacia abajo
                    self.rect.bottom = r.top  # Colocar arriba del obstáculo
                if vy < 0:  # Si se movía hacia arriba
                    self.rect.top = r.bottom  # Colocar debajo del obstáculo

    def update(self):
        """
        Actualiza el estado del jugador cada frame.
        Asegura que el jugador no salga de los límites de la pantalla.
        """
        # Mantener al jugador dentro de los límites de la pantalla
        self.rect.clamp_ip(pygame.Rect(0, 0, ANCHO, ALTO))