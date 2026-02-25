#objetos (plantas, inventario etc)
class Planta:
    def __init__(self, dias_crecimiento, costo, precio_venta, nombre):
        self.dias_crecimiento = dias_crecimiento
        self.costo = costo
        self.precio_venta = precio_venta
        self.dias_actuales = 0
        self.lista = False
        self.nombre = nombre

    def pasar_dia(self):
        if not self.lista:
            self.dias_actuales += 1
            if self.dias_actuales >= self.dias_crecimiento:
                self.lista = True


class Naranja(Planta):
    def __init__(self):
        super().__init__(3, 15, 35, "Naranja")


class Uva(Planta):
    def __init__(self):
        super().__init__(5, 35, 50, "Uva")


class Mandarina(Planta):
    def __init__(self):
        super().__init__(10, 100, 1000, "Mandarina")


class Inventario:
    def __init__(self):
        self.uvas = 0
        self.naranjas = 0
        self.mandarinas = 0
