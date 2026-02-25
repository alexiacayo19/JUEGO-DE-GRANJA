#paso dias
import time

dia_actual = 1
tiempo_inicio = time.time()
duracion_dia = 5  # segundos

def actualizar_dia(parcelas):
    global dia_actual, tiempo_inicio

    if time.time() - tiempo_inicio >= duracion_dia:
        dia_actual += 1
        tiempo_inicio = time.time()

        for p in parcelas:
            p.pasar_dia()

    return dia_actual
