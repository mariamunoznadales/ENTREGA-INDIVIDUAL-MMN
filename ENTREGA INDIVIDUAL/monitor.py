from collections import defaultdict

class Monitor:
    def __init__(self):
        self.estadisticas = defaultdict(lambda: {"pedidos": 0, "tiempo_total": 0.0})

    def registrar_entrega(self, repartidor_id, pedido, tiempo_entrega):
        self.estadisticas[repartidor_id]["pedidos"] += 1
        self.estadisticas[repartidor_id]["tiempo_total"] += tiempo_entrega

    def mostrar_resultados(self):
        print("\n📊 Estadísticas finales:")
        for rid, datos in self.estadisticas.items():
            pedidos = datos["pedidos"]
            media = datos["tiempo_total"] / pedidos if pedidos > 0 else 0
            print(f"Repartidor {rid}: {pedidos} pedidos, tiempo promedio: {media:.2f}s")

    def get_estadisticas(self):
        return self.estadisticas
