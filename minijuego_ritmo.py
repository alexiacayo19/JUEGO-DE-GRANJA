import pygame
import random
import time
from confi import VENTANA, ANCHO, ALTO, BLANCO, NEGRO, VERDE_CLARO

class Nota:
    """
    Clase que representa una nota musical en el minijuego de ritmo.
    Cada nota tiene una tecla asociada, posición en pantalla y estado.
    """
    def __init__(self, tecla, x):
        self.tecla = tecla      # Tecla que debe presionarse (pygame.K_d, etc.)
        self.x = x              # Posición horizontal fija (carril)
        self.y = -100           # Posición vertical inicial (fuera de pantalla arriba)
        self.golpeada = False   # Si la nota ya fue presionada correctamente


class MinijuegoRitmo:
    """
    Minijuego de ritmo donde el jugador debe presionar teclas cuando las notas
    alcanzan la línea de golpeo. Gana con 5+ puntos en 16 segundos.
    """

    def __init__(self):
        # Lista que almacena todas las notas activas (objetos Nota)
        self.notas = []
        
        # Control de tiempo del juego
        self.tiempo_inicio = 0      # Momento en que empezó el minijuego
        self.tiempo_juego = 0       # Tiempo real de juego (sin cuenta regresiva)
        self.puntos = 0             # Puntuación actual del jugador
        
        # Estados del juego
        self.activo = False         # Si el minijuego está en ejecución
        self.terminado = False      # Si el minijuego ha terminado
        self.gano = False           # Si el jugador ganó (5+ puntos)
        
        # Control de cuenta regresiva y generación de notas
        self.contador_inicio = 3    # Cuenta regresiva inicial (3, 2, 1)
        self.ultimo_tiempo_nota = 0 # Cuándo se generó la última nota
        self.tecla_anterior = None  # Última tecla usada (para evitar repeticiones)
        
        # Configuración de teclas del minijuego
        self.tecla_d = pygame.K_d   # Tecla D del teclado
        self.tecla_f = pygame.K_f   # Tecla F del teclado
        self.tecla_j = pygame.K_j   # Tecla J del teclado
        self.tecla_k = pygame.K_k   # Tecla K del teclado
        
        # Posiciones X donde aparecen las notas para cada tecla
        self.posicion_d = 200  # Carril para tecla D
        self.posicion_f = 300  # Carril para tecla F
        self.posicion_j = 400  # Carril para tecla J
        self.posicion_k = 500  # Carril para tecla K
        
        # Listas para manejar teclas y posiciones sin diccionarios
        self.lista_teclas = [self.tecla_d, self.tecla_f, self.tecla_j, self.tecla_k]
        self.lista_posiciones = [self.posicion_d, self.posicion_f, self.posicion_j, self.posicion_k]


    def empezar(self):
        """Reinicia y comienza el minijuego desde el estado inicial"""
        self.activo = True
        self.terminado = False
        self.gano = False
        self.puntos = 0
        self.tiempo_inicio = time.time()  # Registrar momento de inicio
        self.tiempo_juego = 0
        self.contador_inicio = 3
        self.ultimo_tiempo_nota = 0
        self.tecla_anterior = None
        self.notas = []  # Limpiar todas las notas anteriores


    def actualizar(self):
        """Actualiza la lógica del minijuego: tiempo, generación y movimiento de notas"""
        # Si el juego no está activo o ya terminó, no hacer nada
        if not self.activo or self.terminado:
            return

        # Calcular tiempo transcurrido desde el inicio
        tiempo_actual = time.time() - self.tiempo_inicio

        # --- CUENTA REGRESIVA INICIAL (3 segundos) ---
        if tiempo_actual < 3:
            # Actualizar contador (3, 2, 1)
            self.contador_inicio = 3 - int(tiempo_actual)
            return  # No generar notas durante la cuenta regresiva

        # --- JUEGO PRINCIPAL ---
        # Tiempo real de juego (excluyendo la cuenta regresiva)
        self.tiempo_juego = tiempo_actual - 3

        # --- GENERACIÓN DE NOTAS ---
        # Crear notas cada 1.5 segundos durante los primeros 10 segundos de juego
        if self.tiempo_juego < 10 and self.tiempo_juego - self.ultimo_tiempo_nota >= 1.5:
            
            # Decidir cuántas notas crear (1-4 notas por generación)
            cantidad_notas = random.choice([1, 2, 3, 4])
            
            # Crear copias de las listas de teclas y posiciones disponibles
            teclas_disponibles = self.lista_teclas.copy()
            posiciones_disponibles = self.lista_posiciones.copy()
            
            # --- EVITAR REPETICIÓN DE TECLAS ---
            # Si hay una tecla anterior y hay opciones disponibles, removerla
            if self.tecla_anterior and len(teclas_disponibles) > 1:
                indice = teclas_disponibles.index(self.tecla_anterior)
                teclas_disponibles.pop(indice)
                posiciones_disponibles.pop(indice)
            
            # --- CREAR LAS NOTAS (como objetos) ---
            for _ in range(cantidad_notas):
                if teclas_disponibles:  # Si todavía hay teclas disponibles
                    # Elegir una tecla aleatoria de las disponibles
                    indice_aleatorio = random.randint(0, len(teclas_disponibles) - 1)
                    tecla = teclas_disponibles[indice_aleatorio]
                    posicion_x = posiciones_disponibles[indice_aleatorio]
                    
                    # Crear nuevo objeto Nota y añadirlo a la lista
                    nueva_nota = Nota(tecla, posicion_x)
                    self.notas.append(nueva_nota)

                    self.tecla_anterior = tecla  # Recordar esta tecla para la próxima generación
                    
                    # Remover la tecla usada para evitar duplicados en esta generación
                    teclas_disponibles.pop(indice_aleatorio)
                    posiciones_disponibles.pop(indice_aleatorio)
            
            # Registrar el momento de esta generación de notas
            self.ultimo_tiempo_nota = self.tiempo_juego

        # --- MOVIMIENTO DE NOTAS ---
        # Mover todas las notas no golpeadas hacia abajo
        for nota in self.notas:
            if not nota.golpeada:
                nota.y += 3  # Velocidad de caída: 3 píxeles por frame

        # --- VERIFICAR FIN DEL JUEGO ---
        # El juego termina después de 16 segundos totales (3s cuenta + 13s juego)
        if tiempo_actual >= 16:
            self.terminado = True
            self.activo = False
            self.gano = self.puntos >= 5  # Ganar con 5 o más puntos


    def golpear_nota(self, tecla):
        """
        Intenta golpear una nota con la tecla presionada
        Retorna True si se golpeó una nota correctamente, False en caso contrario
        """
        # Verificar que el juego esté activo y no haya terminado
        if not self.activo or self.terminado:
            return False
        
        # No permitir golpear durante la cuenta regresiva
        if time.time() - self.tiempo_inicio < 3:
            return False
        
        # Buscar entre todas las notas no golpeadas
        for nota in self.notas:
            # Verificar: nota no golpeada, tecla correcta, y en zona de golpeo
            if (not nota.golpeada and 
                nota.tecla == tecla and 
                450 < nota.y < 550):  # Zona de golpeo entre Y=450 y Y=550
                
                nota.golpeada = True  # Marcar como golpeada
                self.puntos += 1      # Aumentar puntuación
                return True           # Éxito al golpear
        
        return False  # No se golpeó ninguna nota


    def dibujar(self):
        """Dibuja todos los elementos del minijuego en pantalla"""
        # Fondo negro para el minijuego
        VENTANA.fill(NEGRO)
        
        # Calcular tiempo transcurrido
        tiempo_actual = time.time() - self.tiempo_inicio
        
        # --- PANTALLA DE CUENTA REGRESIVA ---
        if tiempo_actual < 3:
            fuente_grande = pygame.font.SysFont(None, 100)
            texto = fuente_grande.render(str(self.contador_inicio), True, BLANCO)
            VENTANA.blit(texto, (ANCHO//2 - 25, ALTO//2 - 50))
            return  # No dibujar el resto durante cuenta regresiva
        
        # --- LÍNEA DE GOLPEO ---
        # Línea donde deben presionarse las notas
        pygame.draw.line(VENTANA, BLANCO, (150, 500), (550, 500), 3)
        
        # Configurar fuente para textos
        fuente = pygame.font.SysFont(None, 36)
        
        # --- DIBUJAR TECLAS EN LA PARTE INFERIOR ---
        # Mostrar las letras D, F, J, K debajo de cada carril
        VENTANA.blit(fuente.render("D", True, BLANCO), (self.posicion_d - 10, 520))
        VENTANA.blit(fuente.render("F", True, BLANCO), (self.posicion_f - 10, 520))
        VENTANA.blit(fuente.render("J", True, BLANCO), (self.posicion_j - 10, 520))
        VENTANA.blit(fuente.render("K", True, BLANCO), (self.posicion_k - 10, 520))
        
        # --- DIBUJAR NOTAS ---
        # Dibujar círculos amarillos para cada nota no golpeada
        for nota in self.notas:
            if not nota.golpeada:
                pygame.draw.circle(VENTANA, (255, 255, 0), (nota.x, int(nota.y)), 20)
        
        # --- INFORMACIÓN DE JUEGO ---
        # Calcular tiempo restante (no negativo)
        tiempo_restante = max(0, 16 - tiempo_actual)
        
        # Crear y posicionar textos informativos
        VENTANA.blit(fuente.render(f"Puntos: {self.puntos}", True, BLANCO), (50, 50))
        VENTANA.blit(fuente.render(f"Tiempo: {tiempo_restante:.1f}", True, BLANCO), (500, 50))
        VENTANA.blit(fuente.render("Objetivo: 5", True, (255, 255, 0)), (ANCHO//2 - 50, 50))
        
        # --- PANTALLA DE RESULTADOS ---
        if self.terminado:
            if self.gano:
                # Mensaje de victoria (verde)
                texto = fuente.render("GANASTE 500 MONEDAS!", True, (0, 255, 0))
            else:
                # Mensaje de derrota (rojo)
                texto = fuente.render("PERDISTE", True, (255, 0, 0))
            
            # Mostrar resultado centrado
            VENTANA.blit(texto, (ANCHO//2 - 150, ALTO//2))
            
            # Instrucción para continuar
            instruccion = fuente.render("Presiona ESPACIO", True, BLANCO)
            VENTANA.blit(instruccion, (ANCHO//2 - 100, ALTO//2 + 50))