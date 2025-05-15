
# Simulador Concurrente de Pedidos Online

Este proyecto es una simulación visual de un sistema de pedidos concurrente, desarrollado en Python. Utiliza hilos (`threading`), sincronización (`Lock`, `Queue`) y una interfaz gráfica con `Tkinter` para modelar un entorno donde múltiples clientes generan pedidos y varios repartidores los entregan en paralelo.

## Objetivo

Simular un entorno concurrente realista con:

- Clientes que generan pedidos (productores)
- Repartidores que los entregan (consumidores)
- Una cola compartida que sincroniza las operaciones
- Visualización del estado en tiempo real


## Cómo ejecutar
1) Asegúrate de tener todos los archivos en la misma carpeta.
2) Abre una terminal y ejecuta:

```bash
python main.py


