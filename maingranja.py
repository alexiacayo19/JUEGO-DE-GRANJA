import pygame
import sys
import time
import random
from confi import *
from mapas import *
from plantar import *
from Jugador import *
from tiendita import *
from hud import *
from minijuego_ritmo import MinijuegoRitmo
from llama import *

# PANTALLA DE VICTORIA

def pantalla_victoria(tiempo_total):
    """
    Muestra la pantalla de victoria cuando el jugador alcanza 1000 monedas.
    Incluye el tiempo total de juego y permite salir con ESPACIO.
    """
    # Fondo verde claro para la pantalla de victoria
    VENTANA.fill(VERDE_CLARO)
    
    # Texto principal "¡Has ganado!"
    texto = fuente.render("¡Has ganado!", True, NEGRO)
    VENTANA.blit(texto, (ANCHO//2 - texto.get_width()//2, ALTO//2 - 70))

    # Convertir tiempo total a minutos y segundos
    minutos = int(tiempo_total // 60)
    segundos = int(tiempo_total % 60)
    
    # Mostrar tiempo total de juego
    texto2 = fuente_peq.render(f"Tiempo total: {minutos} min {segundos} seg", True, NEGRO)
    VENTANA.blit(texto2, (ANCHO//2 - texto2.get_width()//2, ALTO//2 - 10))

    # Instrucción para salir del juego
    texto3 = fuente_peq.render("Presiona SPACE para salir", True, NEGRO)
    VENTANA.blit(texto3, (ANCHO//2 - texto3.get_width()//2, ALTO//2 + 40))

    # Actualizar pantalla
    pygame.display.flip()

    # Bucle de espera hasta que el jugador presione ESPACIO
    esperando = True
    while esperando:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                pygame.quit()
                sys.exit()


# ------------------------
# INICIALIZACIÓN DEL JUEGO
# ------------------------

# Empezar en el mapa 1
mapa_actual = 1

# Configurar colisiones y parcelas para ambos mapas
generar_colisiones(mapa1)           # Crear obstáculos en mapa 1
generar_parcelas(mapa1, parcelas_mapa1)  # Crear parcelas cultivables en mapa 1
generar_parcelas(mapa2, parcelas_mapa2)  # Crear parcelas cultivables en mapa 2
parcelas = parcelas_mapa1           # Empezar con las parcelas del mapa 1

# Crear jugador y grupo de sprites
jugador = Jugador(ANCHO//2, ALTO//2)  # Posición inicial centrada
sprites = pygame.sprite.Group(jugador)  # Grupo para dibujar al jugador

# Inicializar minijuego de ritmo
minijuego = MinijuegoRitmo()
en_minijuego = False  # Controla si el minijuego de ritmo está activo

# Minijuego de llama (se activa automáticamente en mapa 2)
minijuego_llama = MinijuegoLlama(jugador)

# Registrar tiempo de inicio para calcular tiempo total de juego
tiempo_inicio_total = time.time()


# --- SISTEMA DE DÍAS ---
def avanzar_dia():
    """
    Avanza un día en el juego y hace crecer todas las plantas sembradas.
    Se llama automáticamente cada cierto tiempo (duracion_dia).
    """
    global dia_actual
    dia_actual += 1  # Incrementar contador de días
    
    # Hacer crecer todas las plantas en las parcelas
    for p in parcelas:
        if p.planta:  # Solo si hay una planta sembrada en la parcela
            p.planta.pasar_dia()  # Hacer que la planta crezca un día


# --- BUCLE PRINCIPAL DEL JUEGO ---
def juego():
    """
    Bucle principal que controla toda la lógica del juego:
    eventos, actualización, dibujado y cambio de estados.
    """
    global tiempo_inicio, dia_actual
    global mapa_actual, parcelas, en_minijuego, minijuego
    global tiempo_inicio_total

    tienda_abierta = False  # Controla si la interfaz de tienda está visible

    # Bucle infinito del juego
    while True:
        # --- MANEJO DE EVENTOS (teclas, mouse, etc.) ---
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # --- MINIJUEGO DE RITMO (cuando está activo) ---
            if en_minijuego:
                if e.type == pygame.KEYDOWN:
                    # Salir del minijuego cuando termina (con ESPACIO)
                    if minijuego.terminado and e.key == pygame.K_SPACE:
                        en_minijuego = False  # Desactivar minijuego
                        if minijuego.gano:
                            jugador.dinero += 500  # Recompensa por ganar
                        # Reposicionar jugador fuera de la puerta de ritmo
                        jugador.rect.center = (puerta_ritmo.right + 50, puerta_ritmo.centery)
                        minijuego = MinijuegoRitmo()  # Reiniciar minijuego
                    # Golpear notas durante el juego activo
                    elif not minijuego.terminado:
                        if e.key in [pygame.K_d, pygame.K_f, pygame.K_j, pygame.K_k]:
                            minijuego.golpear_nota(e.key)

            # --- JUEGO NORMAL (cuando no hay minijuego activo) ---
            else:
                if e.type == pygame.KEYDOWN:
                    # Abrir / cerrar tienda con tecla T
                    if e.key == pygame.K_t:
                        tienda_abierta = not tienda_abierta  # Alternar estado

                    # --- COMPRAR EN LA TIENDA ---
                    # Solo funciona cuando la tienda está abierta
                    if tienda_abierta:
                        if e.key == pygame.K_1: intentar_comprar(jugador, 1)  # Comprar uva
                        if e.key == pygame.K_2: intentar_comprar(jugador, 2)  # Comprar naranja
                        if e.key == pygame.K_3: intentar_comprar(jugador, 3)  # Comprar mandarina

                    # --- ACCIONES DE CULTIVO ---
                    else:
                        # Seleccionar tipo de semilla para plantar
                        if e.key == pygame.K_1: jugador.seleccion = "Uva"
                        if e.key == pygame.K_2: jugador.seleccion = "Naranja"
                        if e.key == pygame.K_3: jugador.seleccion = "Mandarina"

                        # Plantar semilla en parcela (tecla E)
                        if e.key == pygame.K_e:
                            for p in parcelas:  # Buscar entre todas las parcelas
                                if jugador.rect.colliderect(p.rect):  # Si el jugador está sobre una parcela
                                    # Verificar que tenga la semilla seleccionada en el inventario
                                    if jugador.seleccion == "Uva" and jugador.inventario.uvas > 0:
                                        if p.sembrar(Uva()):  # Intentar sembrar uva
                                            jugador.inventario.uvas -= 1  # Reducir inventario
                                    elif jugador.seleccion == "Naranja" and jugador.inventario.naranjas > 0:
                                        if p.sembrar(Naranja()):  # Intentar sembrar naranja
                                            jugador.inventario.naranjas -= 1
                                    elif jugador.seleccion == "Mandarina" and jugador.inventario.mandarinas > 0:
                                        if p.sembrar(Mandarina()):  # Intentar sembrar mandarina
                                            jugador.inventario.mandarinas -= 1
                                    break  # Solo sembrar en una parcela por pulsación

                        # Cosechar plantas maduras (tecla C)
                        if e.key == pygame.K_c:
                            for p in parcelas:
                                if jugador.rect.colliderect(p.rect):  # Si el jugador está sobre una parcela
                                    jugador.dinero += p.cosechar()  # Añadir dinero por cosecha
                                    break  # Solo cosechar una parcela por pulsación

        # --- ACTUALIZACIÓN DEL ESTADO DEL JUEGO ---
        # Obtener estado de todas las teclas para movimiento continuo
        teclas = pygame.key.get_pressed()
        
        # Mover al jugador solo si la tienda no está abierta
        if not tienda_abierta:
            jugador.mover(teclas)  # Mover jugador con teclas WASD/flechas
            
        jugador.update()  # Actualizar estado del jugador (mantener en pantalla)

        # --- ACTUALIZAR MINIJUEGO DE RITMO ---
        if en_minijuego:
            minijuego.actualizar()  # Actualizar lógica del minijuego de ritmo

        # --- AVANZAR DÍA (cada 10 segundos) ---
        # duracion_dia está definida en confi.py
        if time.time() - tiempo_inicio >= duracion_dia:
            avanzar_dia()  # Hacer crecer todas las plantas
            tiempo_inicio = time.time()  # Reiniciar temporizador

        # --- CONDICIÓN DE VICTORIA ---
        # El jugador gana al alcanzar 1000 monedas
        if jugador.dinero >= 1000:
            tiempo_total = time.time() - tiempo_inicio_total  # Calcular tiempo total
            pantalla_victoria(tiempo_total)  # Mostrar pantalla de victoria

        # --- CAMBIO DE MAPAS ---
        # Del mapa 1 al mapa 2 (puerta derecha del mapa 1)
        if mapa_actual == 1 and jugador.rect.colliderect(arco_mapa1):
            mapa_actual = 2  # Cambiar a mapa 2
            jugador.rect.center = (ANCHO//2, ALTO - 80)  # Posición inicial en mapa 2
            generar_colisiones(mapa2)  # Generar obstáculos del mapa 2
            parcelas = parcelas_mapa2  # Cambiar a parcelas del mapa 2
            minijuego_llama.empezar()  # Iniciar automáticamente minijuego de llama

        # Del mapa 2 al mapa 1 (puerta izquierda del mapa 2)
        elif mapa_actual == 2 and jugador.rect.colliderect(arco_mapa2):
            mapa_actual = 1  # Cambiar a mapa 1
            jugador.rect.center = (arco_mapa1.left - 30, arco_mapa1.centery)  # Posición inicial
            generar_colisiones(mapa1)  # Generar obstáculos del mapa 1
            parcelas = parcelas_mapa1  # Cambiar a parcelas del mapa 1

        # --- ENTRAR AL MINIJUEGO DE RITMO ---
        # Puerta izquierda en mapa 1 para minijuego de ritmo
        elif (mapa_actual == 1 and 
              jugador.rect.colliderect(puerta_ritmo) and 
              not en_minijuego):
            minijuego.empezar()  # Iniciar minijuego de ritmo
            en_minijuego = True  # Activar bandera del minijuego

        # --- ACTUALIZAR MINIJUEGO LLAMA ---
        # Solo se actualiza cuando estamos en el mapa 2
        if mapa_actual == 2:
            minijuego_llama.actualizar()

        # --- DIBUJADO EN PANTALLA ---
        VENTANA.fill((0, 0, 0))  # Limpiar pantalla con color negro
        
        # --- DIBUJAR MINIJUEGO DE RITMO ---
        if en_minijuego:
            minijuego.dibujar()  # Solo dibujar el minijuego de ritmo
            
        # --- DIBUJAR JUEGO NORMAL ---
        else:
            dibujar_mapa(parcelas, mapa_actual)  # Dibujar el mapa actual
            sprites.draw(VENTANA)  # Dibujar al jugador

            # Dibujar minijuego de llama si estamos en mapa 2
            if mapa_actual == 2:
                minijuego_llama.dibujar(VENTANA)  # Dibuja llama y mensajes

            # Mostrar HUD (interfaz de usuario)
            mostrar_hud(jugador, dia_actual, tienda_abierta, parcelas)

        # Actualizar pantalla y controlar FPS
        pygame.display.flip()
        clock.tick(60)  # 60 FPS (frames por segundo)


# --- INICIAR EL JUEGO ---
if __name__ == "__main__":
    juego()  # Ejecutar la función principal del juego