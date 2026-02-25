import pygame
from confi import ANCHO, ALTO
from confi import *

# SISTEMA DE MAPAS MÚLTIPLES
TAM_TILE = 64  

# Mapa 1: Zona principal de cultivo con puerta al mapa 2 y minijuego de ritmo
mapa1 = [
    list("GGGGGGGGGGGGG"),  # G = Pasto, T = Tierra cultivable, A = Agua
    list("GTTTTTTTGGPGG"),  # D = Árbol, P = Tronco, F = Flor amarilla  
    list("GTTTTTTTGGDGG"),  # C = Árbol 2
    list("GTTTGGGFGGCGG"),
    list("GTTTGFGGGGGGG"),
    list("GTTTGGGGGGGGG"),
    list("GGGGGGAAAAAGG"),
    list("GGGGGGAAAAAGG"),
    list("GGGGGGFGGGGFG"),
    list("GGGGGGGGGGGGG"),
]

# Mapa 2: Zona secundaria con decoración de flores y minijuego de llama automático
mapa2 = [
    list("GGGGGGGGGGGGG"),  # G = Pasto, R = Flor roja, B = Flor azul
    list("GRGGGRGGGGBGG"),  # F = Flor amarilla
    list("GGGFGGGGGGRGG"),
    list("GGGGGFGGGGBGG"),
    list("GGBGGGGGGGFGG"),
    list("GGRGGGGGFGGGG"),
    list("GGGGGGGBGGGGG"),
    list("GFGGGGGGGGGGG"),
    list("GFGGGGGGGFGGG"),
    list("GGGRGGBGGGGGG"),
    list("GGGGGGGGGGGGG"),
]

# --- CONFIGURACIÓN DE PUERTAS/ARCOS ---
ancho_arco = 40    # Ancho de las puertas
alto_arco = 120    # Alto de las puertas

# Puerta derecha del mapa 1 que lleva al mapa 2
arco_mapa1 = pygame.Rect(ANCHO - ancho_arco, (ALTO - alto_arco) // 2, ancho_arco, alto_arco)

# Puerta izquierda del mapa 2 que lleva de vuelta al mapa 1
arco_mapa2 = pygame.Rect(4, (ALTO - alto_arco) // 2, ancho_arco, alto_arco)

# Puerta izquierda del mapa 1 para el minijuego de ritmo
puerta_ritmo = pygame.Rect(4, (ALTO - alto_arco) // 2 + 150, ancho_arco, alto_arco)

# SISTEMA DE COLISIONES
colisiones = []

def generar_colisiones(mapa1):
    colisiones.clear()
    for fila, linea in enumerate(mapa1):
        for col, tile in enumerate(linea):
            if tile in ["A" , "D" , "W" , "P"]:
                x = col * TAM_TILE
                y = fila * TAM_TILE
                colision = pygame.Rect(x,y,TAM_TILE,TAM_TILE)
                colisiones.append(colision)

generar_colisiones(mapa1)

# CARGA DE RECURSOS GRÁFICOS
# Cargar y escalar todas las imágenes del juego

# Agua - tile azul para zonas de agua
agua = pygame.image.load('imagen/agua.png')
agua = pygame.transform.scale(agua, (TAM_TILE, TAM_TILE))

# Árbol normal - obstáculo decorativo
arbol = pygame.image.load('imagen/arbol.png')
arbol = pygame.transform.scale(arbol, (TAM_TILE, TAM_TILE))

# Pasto - tile base para la mayoría del mapa
pasto = pygame.image.load('imagen/pasto.png')
pasto = pygame.transform.scale(pasto, (100, 80))

# Tronco - obstáculo decorativo
tronco = pygame.image.load('imagen/tronco.png')
tronco = pygame.transform.scale(tronco, (40, 40))

# Flor amarilla - decoración
flor1 = pygame.image.load('imagen/flor.amarilla.png')
flor1 = pygame.transform.scale(flor1, (TAM_TILE, TAM_TILE))

# Árbol 2 - variante de árbol decorativo
arbol2 = pygame.image.load('imagen/arbol_2.png')
arbol2 = pygame.transform.scale(arbol2, (TAM_TILE, TAM_TILE))

# Flor azul - decoración
florazul = pygame.image.load('imagen/flor.azul.png')
florazul = pygame.transform.scale(florazul, (TAM_TILE, TAM_TILE))

# Flor roja - decoración
florroja = pygame.image.load('imagen/flor.roja.png')
florroja = pygame.transform.scale(florroja, (TAM_TILE, TAM_TILE))

# --- FUNCIÓN PARA DIBUJAR EL MAPA ---
def dibujar_mapa(parcelas, mapa_actual):
    """
    Dibuja todo el mapa actual incluyendo tiles, decoraciones, puertas y plantas
    """
    # Seleccionar el mapa correcto (1 o 2)
    if mapa_actual == 1:
        mapa = mapa1
    else:
        mapa = mapa2

    # DIBUJAR TILES BASE
    # Recorrer cada posición del mapa y dibujar el tile correspondiente
    for f, linea in enumerate(mapa):
        for c, t in enumerate(linea):
            x = c * TAM_TILE  # Posición X en píxeles
            y = f * TAM_TILE  # Posición Y en píxeles

            # Asignar color de fondo según el tipo de tile
            if t == "G": color = VERDE_CLARO  # Pasto
            elif t == "T": color = MARRON     # Tierra cultivable
            elif t == "A": color = AZUL       # Agua
            else: color = VERDE_CLARO         # Por defecto, pasto

            # Dibujar el tile de fondo
            pygame.draw.rect(VENTANA, color, (x, y, TAM_TILE, TAM_TILE))

            # --- DIBUJAR DECORACIONES SOBRE EL FONDO ---
            # Agua - tile especial con imagen
            if t == "A": VENTANA.blit(agua, (x, y))
            # Árbol normal - obstáculo decorativo
            if t == "D": VENTANA.blit(arbol, (x, y))
            # Tronco - obstáculo pequeño
            if t == "P": VENTANA.blit(tronco, (x, y))
            # Flor amarilla - decoración
            if t == "F": VENTANA.blit(flor1, (x, y))
            # Flor azul - decoración
            if t == "B": VENTANA.blit(florazul, (x, y))
            # Árbol 2 - variante decorativa
            if t == "C": VENTANA.blit(arbol2, (x, y))
            # Flor roja - decoración
            if t == "R": VENTANA.blit(florroja, (x, y))

    # --- DIBUJAR PUERTAS ---
    # Todas las puertas se dibujan en color negro
    if mapa_actual == 1:
        # Mapa 1 tiene dos puertas: derecha (mapa 2) e izquierda (ritmo)
        pygame.draw.rect(VENTANA, NEGRO, arco_mapa1)    # Puerta derecha al mapa 2
        pygame.draw.rect(VENTANA, NEGRO, puerta_ritmo)  # Puerta izquierda al minijuego de ritmo

    elif mapa_actual == 2:
        # Mapa 2 tiene una puerta: izquierda (regreso al mapa 1 / minijuego llama)
        pygame.draw.rect(VENTANA, NEGRO, arco_mapa2)    # Puerta para minijuego llama

    # --- DIBUJAR PLANTAS EN PARCELAS ---
    for p in parcelas:
        if p.planta:
            # Asignar color según el tipo de planta
            if p.planta.nombre == "Uva": color = (150, 0, 150)      # Morado para uva
            elif p.planta.nombre == "Naranja": color = (255, 140, 0) # Naranja para naranja
            else: color = (255, 255, 0)                             # Amarillo para mandarina

            # Si la planta no está lista para cosechar, hacer el color más oscuro
            if not p.planta.lista:
                color = (color[0] // 2, color[1] // 2, color[2] // 2)

            # Dibujar la planta como un rectángulo coloreado en la parcela
            pygame.draw.rect(VENTANA, color, p.rect)