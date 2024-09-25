from machine import Pin
import time

# Pines de control del motor
IN1 = Pin(25, Pin.OUT)  # Motor 1, Pin de dirección
IN2 = Pin(26, Pin.OUT)  # Motor 1, Pin de dirección
IN3 = Pin(27, Pin.OUT)  # Motor 2, Pin de dirección
IN4 = Pin(14, Pin.OUT)  # Motor 2, Pin de dirección

# Mover hacia adelante
def adelante():
    IN1.value(1)  # Motor 1 avanza
    IN2.value(0)
    IN3.value(0)  # Motor 2 avanza
    IN4.value(1)

# Mover hacia atrás
def atras():
    IN1.value(0)  # Motor 1 retrocede
    IN2.value(1)
    IN3.value(0)  # Motor 2 retrocede
    IN4.value(1)

# Girar a la derecha
def derecha():
    IN1.value(0)  # Motor 1 retrocede
    IN2.value(1)
    IN3.value(1)  # Motor 2 avanza
    IN4.value(0)

# Girar a la izquierda
def izquierda():
    IN1.value(1)  # Motor 1 avanza
    IN2.value(0)
    IN3.value(0)  # Motor 2 retrocede
    IN4.value(1)

# Detener
def detener():
    IN1.value(0)
    IN2.value(0)
    IN3.value(0)
    IN4.value(0)

# Bucle de prueba
while True:
    adelante()  # Avanzar
    time.sleep(2)
    detener()  # Detener
    time.sleep(1)
    
    derecha()  # Girar a la derecha
    time.sleep(1)
    detener()  # Detener
    time.sleep(1)
    
    izquierda()  # Girar a la izquierda
    time.sleep(1)
    detener()  # Detener
    time.sleep(1)
    
    atras()  # Mover hacia atrás
    time.sleep(2)
    detener()  # Detener
    time.sleep(2)
