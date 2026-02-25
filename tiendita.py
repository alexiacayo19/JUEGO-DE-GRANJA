import pygame
from confi import VENTANA, ANCHO, ALTO, NEGRO, fuente, fuente_peq, VERDE_CLARO

# --- SISTEMA DE TIENDA ---
def mostrar_tienda_overlay(jugador):
    """
    Muestra la interfaz de tienda como un overlay semitransparente
    Permite al jugador comprar semillas usando las teclas 1, 2, 3
    """
    # Crear fondo semitransparente para el overlay de tienda
    s = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    s.fill((0, 0, 0, 150))  # Negro con transparencia (150/255)
    VENTANA.blit(s, (0, 0))

    # Dibujar cuadro principal de la tienda
    cuadro = pygame.Rect(ANCHO//2 - 180, ALTO//2 - 140, 360, 280)
    pygame.draw.rect(VENTANA, (200, 200, 200), cuadro)  # Fondo gris claro
    pygame.draw.rect(VENTANA, (50, 50, 50), cuadro, 3)  # Borde gris oscuro

    # Título de la tienda
    txt_tit = fuente.render("TIENDA", True, NEGRO)
    VENTANA.blit(txt_tit, (cuadro.x + 8, cuadro.y + 8))

    # Mostrar items disponibles para comprar
    # Uva: costo 35 monedas
    VENTANA.blit(fuente_peq.render("1) Uva: 35 monedas", True, NEGRO), (cuadro.x + 12, cuadro.y + 60))
    VENTANA.blit(fuente_peq.render(f"Tienes: {jugador.inventario.uvas}", True, NEGRO), (cuadro.x + 250, cuadro.y + 60))

    # Naranja: costo 15 monedas
    VENTANA.blit(fuente_peq.render("2) Naranja: 15 monedas", True, NEGRO), (cuadro.x + 12, cuadro.y + 100))
    VENTANA.blit(fuente_peq.render(f"Tienes: {jugador.inventario.naranjas}", True, NEGRO), (cuadro.x + 250, cuadro.y + 100))

    # Mandarina: costo 100 monedas
    VENTANA.blit(fuente_peq.render("3) Mandarina: 100 monedas", True, NEGRO), (cuadro.x + 12, cuadro.y + 140))
    VENTANA.blit(fuente_peq.render(f"Tienes: {jugador.inventario.mandarinas}", True, NEGRO), (cuadro.x + 250, cuadro.y + 140))

    # Instrucciones para cerrar la tienda
    VENTANA.blit(fuente_peq.render("Presiona T para cerrar la tienda", True, NEGRO), (cuadro.x + 12, cuadro.y + 200))

def intentar_comprar(jugador, op):
    """
    Intenta comprar un item de la tienda
    op: 1=Uva, 2=Naranja, 3=Mandarina
    Solo realiza la compra si el jugador tiene suficiente dinero
    """
    # Comprar Uva (35 monedas)
    if op == 1 and jugador.dinero >= 35:
        jugador.dinero -= 35  # Restar dinero
        jugador.inventario.uvas += 1  # Añadir al inventario
    
    # Comprar Naranja (15 monedas)
    if op == 2 and jugador.dinero >= 15:
        jugador.dinero -= 15
        jugador.inventario.naranjas += 1
    
    # Comprar Mandarina (100 monedas)
    if op == 3 and jugador.dinero >= 100:
        jugador.dinero -= 100
        jugador.inventario.mandarinas += 1