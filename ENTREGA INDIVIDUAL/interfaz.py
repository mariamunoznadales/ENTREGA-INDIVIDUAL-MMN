import threading
import queue
import tkinter as tk
from tkinter import ttk
from productor import Productor
from consumidor import Consumidor
from monitor import Monitor
from pedido import Pedido
import time

class SimuladorGUI:
    def __init__(self):
        # Configuración inicial de la ventana principal
        self.root = tk.Tk()
        self.root.title("Simulador de Pedidos Online")
        self.root.geometry("800x600")
        self.root.configure(bg="#f4f4f4")  # Fondo claro

        # Parámetros de simulación
        self.NUM_CLIENTES = 5
        self.NUM_REPARTIDORES = 3

        # Recursos compartidos
        self.cola_pedidos = queue.Queue()  # Cola sincronizada para pedidos
        self.lock = threading.Lock()       # Lock para proteger acceso al monitor
        self.monitor = Monitor()           # Objeto para guardar estadísticas

        # Listas para hilos
        self.productores = []
        self.consumidores = []

        # ---- Interfaz gráfica ----

        # Título principal
        titulo = tk.Label(self.root, text="Simulador de Pedidos Online", font=("Helvetica", 18, "bold"), bg="#f4f4f4", fg="#222")
        titulo.pack(pady=10)

        # Panel para mostrar el estado de cada repartidor
        self.panel_repartidores = tk.Frame(self.root, bg="#e0e0e0", bd=2, relief="groove")
        self.panel_repartidores.pack(pady=10, padx=20, fill="x")

        etiqueta = tk.Label(self.panel_repartidores, text="Estado de los Repartidores", font=("Helvetica", 12, "bold"), bg="#e0e0e0", fg="#000")
        etiqueta.pack(pady=5)

        # Diccionario con etiquetas por repartidor
        self.labels_estado = {}
        for i in range(1, self.NUM_REPARTIDORES + 1):
            label = tk.Label(self.panel_repartidores, text=f"Repartidor {i}: LIBRE", font=("Helvetica", 11), fg="green", bg="#e0e0e0", anchor="w")
            label.pack(fill="x", padx=10)
            self.labels_estado[i] = label

        # Área de texto para mostrar eventos del sistema
        self.log_text = tk.Text(self.root, state="disabled", height=20, width=95, bg="white", font=("Courier", 10))
        self.log_text.pack(pady=10, padx=20)

        # Botón que lanza la simulación
        self.boton_iniciar = ttk.Button(self.root, text="Iniciar Simulación", command=self.iniciar_simulacion)
        self.boton_iniciar.pack(pady=10)

    # Función para registrar eventos en el área de texto
    def log(self, mensaje, color="black"):
        self.log_text.config(state="normal")
        timestamp = time.strftime("%H:%M:%S")  # Hora actual
        self.log_text.insert(tk.END, f"[{timestamp}] {mensaje}\n", color)

        # Definimos colores por tipo de mensaje
        self.log_text.tag_config("cliente", foreground="blue")
        self.log_text.tag_config("repartidor", foreground="darkgreen")
        self.log_text.tag_config("entrega", foreground="orange")
        self.log_text.tag_config("final", foreground="purple", font=("Courier", 10, "bold"))

        self.log_text.see(tk.END)  # Scroll automático
        self.log_text.config(state="disabled")

    # Cambia el estado visual de un repartidor (libre u ocupado)
    def actualizar_estado(self, repartidor_id, ocupado):
        label = self.labels_estado[repartidor_id]
        if ocupado:
            label.config(text=f"Repartidor {repartidor_id}: OCUPADO", fg="red")
        else:
            label.config(text=f"Repartidor {repartidor_id}: LIBRE", fg="green")

    # Acción del botón: iniciar la simulación en un hilo aparte
    def iniciar_simulacion(self):
        self.boton_iniciar.config(state="disabled")
        hilo = threading.Thread(target=self.simular)
        hilo.start()

    # Lógica principal de la simulación
    def simular(self):
        # Subclase de Productor adaptada para GUI (con log)
        class ProductorGUI(Productor):
            def run(p_self):
                for _ in range(4):
                    pedido = Pedido(p_self.id_cliente)
                    self.cola_pedidos.put(pedido)  # Añadir pedido a la cola
                    self.log(f"Cliente {p_self.id_cliente} realizó un pedido: {pedido}", color="cliente")
                    threading.Event().wait(0.7)  # Espera entre pedidos

        # Subclase de Consumidor adaptada para GUI
        class ConsumidorGUI(Consumidor):
            def run(c_self):
                while True:
                    pedido = self.cola_pedidos.get()
                    if pedido is None:
                        break  # Señal de fin

                    # Marcar repartidor como ocupado
                    self.actualizar_estado(c_self.id_repartidor, True)
                    self.log(f"Repartidor {c_self.id_repartidor} está entregando el pedido de Cliente {pedido.id_cliente}", color="repartidor")

                    threading.Event().wait(2.0)  # Simular tiempo de entrega

                    with self.lock:
                        self.monitor.registrar_entrega(c_self.id_repartidor, pedido, 2.0)

                    self.log(f"Repartidor {c_self.id_repartidor} completó la entrega del pedido de Cliente {pedido.id_cliente}", color="entrega")
                    self.actualizar_estado(c_self.id_repartidor, False)  # Marcar como libre

        # Crear hilos de productores y consumidores
        self.productores = [ProductorGUI(i+1, self.cola_pedidos) for i in range(self.NUM_CLIENTES)]
        self.consumidores = [ConsumidorGUI(i+1, self.cola_pedidos, self.monitor, self.lock) for i in range(self.NUM_REPARTIDORES)]

        # Iniciar hilos
        for p in self.productores:
            p.start()
        for c in self.consumidores:
            c.start()

        # Esperar a que terminen los clientes
        for p in self.productores:
            p.join()

        # Enviar señal de finalización a repartidores
        for _ in self.consumidores:
            self.cola_pedidos.put(None)

        # Esperar a que terminen los repartidores
        for c in self.consumidores:
            c.join()

        # Mostrar resumen final de estadísticas
        self.log("\nResultados Finales:", color="final")
        resultados = self.monitor.get_estadisticas()
        for rid, datos in resultados.items():
            media = datos["tiempo_total"] / datos["pedidos"] if datos["pedidos"] > 0 else 0
            self.log(f"Repartidor {rid}: {datos['pedidos']} pedidos entregados, tiempo promedio: {media:.2f} s", color="final")

    # Ejecuta la ventana principal
    def run(self):
        self.root.mainloop()
