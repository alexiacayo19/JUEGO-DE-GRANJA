import pygame
from confi import VENTANA, ANCHO, BLANCO, HUD_BG, fuente, fuente_peq, VERDE_CLARO, MARRON, AZUL, NEGRO
from tiendita import mostrar_tienda_overlay


# --- HUD (Heads-Up Display) ---
def mostrar_hud(jugador, dia, tienda, parcelas):
    """
    Muestra la interfaz de usuario en la parte superior de la pantalla
    Incluye información esencial del juego: día, dinero, selección actual e inventario
    """
    
    # Dibujar fondo del HUD - rectángulo verde sólido en la parte superior
    # (ANCHO, 50) significa que ocupa todo el ancho de la pantalla y 50 píxeles de alto
    pygame.draw.rect(VENTANA, VERDE_CLARO, (0, 0, ANCHO, 50))
    
    # Mostrar el día actual en la esquina superior derecha
    # Formato: "Día X" - se actualiza automáticamente cuando avanza el día
    VENTANA.blit(fuente.render(f"Día {dia}", True, BLANCO), (ANCHO - 140, 8))
    
    # Mostrar dinero del jugador en la esquina superior izquierda  
    # Color amarillo (255,255,0) para destacar el dinero
    VENTANA.blit(fuente.render(f"${jugador.dinero}", True, (255, 255, 0)), (10, 8))

    # Mostrar la semilla actualmente seleccionada para plantar
    # Si no hay selección, muestra "Nada"
    sel = jugador.seleccion if jugador.seleccion else "Nada"
    VENTANA.blit(fuente_peq.render(f"Seleccionado: {sel}", True, BLANCO), (110, 10))

    # Mostrar inventario del jugador: cantidad de cada tipo de semilla
    # Formato: "Uva:X Naranja:Y Mandarina:Z"
    inv = jugador.inventario
    texto = f"Uva:{inv.uvas}  Naranja:{inv.naranjas}  Mandarina:{inv.mandarinas}"
    VENTANA.blit(fuente_peq.render(texto, True, BLANCO), (360, 10))

    # Si la tienda está abierta, mostrar el overlay de la tienda
    # Esto cubre el juego con una interfaz de compra/venta
    if tienda:
        mostrar_tienda_overlay(jugador)