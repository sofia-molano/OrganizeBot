from machine import Pin
import time

# Pines de control de los motores
IN1 = Pin(25, Pin.OUT)  # Motor 1 (izquierda)
IN2 = Pin(26, Pin.OUT)  # Motor 1 (izquierda)
IN3 = Pin(27, Pin.OUT)  # Motor 2 (derecha)
IN4 = Pin(14, Pin.OUT)  # Motor 2 (derecha)

# Pines de los sensores IR
sensor_izquierdo = Pin(34, Pin.IN)
sensor_central = Pin(32, Pin.IN)
sensor_derecho = Pin(35, Pin.IN)

# Funciones de movimiento
def adelante():
    IN1.value(1)  # Motor 1 avanza
    IN2.value(0)
    IN3.value(0)  # Motor 2 avanza
    IN4.value(1)

def detener():
    IN1.value(0)
    IN2.value(0)
    IN3.value(0)
    IN4.value(0)

def derecha():
    IN1.value(1)  # Motor izquierdo avanza
    IN2.value(0)
    IN3.value(0)  # Motor derecho se detiene
    IN4.value(0)

def izquierda():
    IN1.value(0)  # Motor izquierdo se detiene
    IN2.value(0)
    IN3.value(1)  # Motor derecho avanza
    IN4.value(0)

# Bucle principal
while True:
    # Leer los sensores
    izq = sensor_izquierdo.value()   # 0 si detecta la línea negra
    centro = sensor_central.value()  # 0 si detecta la línea negra
    der = sensor_derecho.value()     # 0 si detecta la línea negra

    # Lógica de control
    if centro == 0 and izq == 1 and der == 1:
        adelante()  # Seguir la línea
    elif izq == 0:  # Si el sensor izquierdo detecta la línea
        izquierda()  # Girar a la izquierda
    elif der == 0:  # Si el sensor derecho detecta la línea
        derecha()    # Girar a la derecha
    else:
        detener()    # Detenerse si no se detecta la línea (robot fuera de la pista)

    time.sleep(0.1)  # Pequeño retardo para evitar lecturas demasiado rápidas
