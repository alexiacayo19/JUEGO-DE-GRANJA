import pygame
import time

pygame.init()

# --- CONFIGURACIÓN ---
ANCHO, ALTO = 800, 600
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("olas")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
VERDE_CLARO = (89, 193, 52)
MARRON = (179, 121, 78)
AZUL = (159, 213, 220)
HUD_BG = (20,20,20)

#pantalla de tienda
screen = pygame.display.set_mode((800, 600))

# Fuente
fuente = pygame.font.SysFont("comicsansms", 36)
fuente_peq = pygame.font.SysFont("comicsansms", 18)

# Reloj
clock = pygame.time.Clock()

# --- DÍA ---
dia_actual = 1
tiempo_inicio = time.time()
duracion_dia = 10