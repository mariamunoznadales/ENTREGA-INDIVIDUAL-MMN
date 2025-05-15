import threading
import time
from monitor import Monitor

class Consumidor(threading.Thread):
    def __init__(self, id_repartidor, cola_pedidos, monitor, lock):
        super().__init__()
        self.id_repartidor = id_repartidor
        self.cola_pedidos = cola_pedidos
        self.monitor = monitor
        self.lock = lock

    def run(self):
        while True:
            pedido = self.cola_pedidos.get()
            if pedido is None:
                break  # Señal de fin
            tiempo_inicio = time.time()
            print(f"--> [REPARTIDOR {self.id_repartidor}] Procesando {pedido}")
            time.sleep(2)  # Simula entrega
            tiempo_fin = time.time()
            with self.lock:
                self.monitor.registrar_entrega(self.id_repartidor, pedido, tiempo_fin - tiempo_inicio)
