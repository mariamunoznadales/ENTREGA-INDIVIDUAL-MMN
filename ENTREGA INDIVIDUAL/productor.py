import threading
import time
import random
from pedido import Pedido

class Productor(threading.Thread):
    def __init__(self, id_cliente, cola_pedidos):
        super().__init__()
        self.id_cliente = id_cliente
        self.cola_pedidos = cola_pedidos

    def run(self):
        for _ in range(random.randint(3, 6)):  # Pedidos por cliente
            pedido = Pedido(self.id_cliente)
            self.cola_pedidos.put(pedido)
            print(f"[CLIENTE {self.id_cliente}] Generó -> {pedido}")
            time.sleep(random.uniform(0.5, 2))
