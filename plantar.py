# --- SISTEMA DE PLANTAS ---
import pygame
from mapas import TAM_TILE

class Planta:
    """
    Clase base para todas las plantas del juego.
    Define el comportamiento común: crecimiento, costo y valor de venta.
    """
    def __init__(self, dias_crecimiento, costo, precio_venta, nombre):
        # Configuración de crecimiento de la planta
        self.dias_crecimiento = dias_crecimiento  # Días necesarios para madurar
        self.costo = costo                        # Precio de compra en la tienda
        self.precio_venta = precio_venta          # Valor al cosechar
        self.dias_actuales = 0                    # Días transcurridos desde que se plantó
        self.lista = False                        # Si está lista para cosechar
        self.nombre = nombre                      # Nombre identificador de la planta

    def pasar_dia(self):
        """
        Avanza un día en el crecimiento de la planta.
        Si alcanza los días necesarios, marca la planta como lista para cosechar.
        """
        if not self.lista:  # Solo crece si no está lista
            self.dias_actuales += 1
            # Verificar si la planta ha alcanzado la madurez
            if self.dias_actuales >= self.dias_crecimiento:
                self.lista = True  # Marcar como lista para cosechar

class Naranja(Planta):
    """
    Planta de naranja: crecimiento rápido, bajo costo, ganancia moderada
    Estrategia: ideal para ganancias rápidas y constantes
    """
    def __init__(self):
        # 3 días de crecimiento, cuesta 15 monedas, se vende por 35
        super().__init__(3, 15, 35, "Naranja")

class Uva(Planta):
    """
    Planta de uva: crecimiento medio, costo medio, ganancia buena
    Estrategia: balance entre tiempo de espera y ganancia
    """
    def __init__(self):
        # 5 días de crecimiento, cuesta 35 monedas, se vende por 50
        super().__init__(5, 35, 50, "Uva")

class Mandarina(Planta):
    """
    Planta de mandarina: crecimiento lento, alto costo, gran ganancia
    Estrategia: inversión a largo plazo con alta recompensa
    """
    def __init__(self):
        # 10 días de crecimiento, cuesta 100 monedas, se vende por 1000
        super().__init__(10, 100, 1000, "Mandarina")







# --- SISTEMA DE PARCELAS ---
class Parcela:
    """
    Representa una parcela de tierra donde se pueden sembrar plantas.
    Cada parcela es un área cultivable en el mapa.
    """
    def __init__(self, x, y):
        # Rectángulo que define la posición y tamaño de la parcela   (x,y son pixeles)
        self.rect = pygame.Rect(x, y, TAM_TILE, TAM_TILE) #horizontal,vertical,ancho,alto del tile (el juego se da cuenta de que estas encima de tierra )
        # Planta actualmente sembrada (None es de que esta vacia)
        self.planta = None

    def sembrar(self, planta):
        """
        Intenta sembrar una planta en la parcela.
        Retorna True si la siembra fue exitosa, False si la parcela ya está ocupada.
        """
        if self.planta is None:  # Solo sembrar si la parcela está vacía
            self.planta = planta
            return True  # Siembra exitosa
        return False  # Parcela ya ocupada

    def cosechar(self):
        """
        Cosecha la planta si está lista y retorna el dinero ganado.
        Retorna 0 si no hay planta o no está lista.
        """
        if self.planta and self.planta.lista:  # Verificar que hay planta y está lista
            dinero = self.planta.precio_venta  # Obtener valor de venta
            self.planta = None  # Liberar la parcela
            return dinero  # Retornar ganancia
        return 0  # No se pudo cosechar






# --- GESTIÓN DE PARCELAS POR MAPA ---
# Listas que almacenan todas las parcelas cultivables de cada mapa
parcelas_mapa1 = []  # Parcelas del mapa 1
parcelas_mapa2 = []  # Parcelas del mapa 2
parcelas = parcelas_mapa1  # Referencia a las parcelas del mapa actual

def generar_parcelas(mapa, lista):
    """
    Genera parcelas cultivables en las posiciones de tierra ('T') del mapa.
    Evita generar duplicados si ya existen parcelas.
    """
    if len(lista) > 0:  
        # Si ya hay parcelas en la lista, no generar duplicados
        return
    
    # Recorrer cada fila del mapa
    for f, linea in enumerate(mapa): #enumarate me da la fila (y en pixeles) columna(x en pixeles) y el valor tile ("T")
        # Recorrer cada columna (tile) de la fila
        for c, t in enumerate(linea):
            if t == "T":  # 'T' representa tierra cultivable
                # Calcular posición en píxeles y crear nueva parcela
                x = c * TAM_TILE  # Posición X en píxeles    columna 0 -> x=0 columna 1= x=4 ()
                y = f * TAM_TILE  # Posición Y en píxeles
                lista.append(Parcela(x, y))  # Añadir parcela a la listaS