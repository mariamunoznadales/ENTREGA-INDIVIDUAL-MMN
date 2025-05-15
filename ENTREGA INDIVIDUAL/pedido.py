import random
import time

class Pedido:
    def __init__(self, id_cliente):
        self.id_cliente = id_cliente
        self.timestamp = time.time()
        self.producto = random.choice(["Reloj", "Anillo", "Collar", "Pulsera"])
        self.cantidad = random.randint(1, 3)

    def __str__(self):
        return f"Pedido de {self.cantidad} {self.producto} del Cliente {self.id_cliente}"
