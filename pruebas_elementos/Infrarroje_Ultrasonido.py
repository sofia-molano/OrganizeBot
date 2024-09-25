from time import sleep
from machine import Pin
from hcsr04 import HCSR04  # Librería para el sensor ultrasónico

# Pines de los sensores infrarrojos (IR)
sensor_1 = Pin(34, Pin.IN, Pin.PULL_UP)
sensor_2 = Pin(32, Pin.IN, Pin.PULL_UP)
sensor_3 = Pin(35, Pin.IN, Pin.PULL_UP)  # Sensor central
sensor_4 = Pin(2, Pin.IN, Pin.PULL_UP)
sensor_5 = Pin(33, Pin.IN, Pin.PULL_UP)

# Pines de control del motor
IN1 = Pin(25, Pin.OUT)
IN2 = Pin(26, Pin.OUT)
IN3 = Pin(12, Pin.OUT)
IN4 = Pin(13, Pin.OUT)

# Pines del sensor ultrasónico
trigger_pin = 22
echo_pin = 21
sensor_ultrasonico = HCSR04(trigger_pin, echo_pin)

# Funciones de movimiento de motores
def adelante():
    IN1.value(1)
    IN2.value(0)
    IN3.value(1)
    IN4.value(0)

def atras():
    IN1.value(0)
    IN2.value(1)
    IN3.value(0)
    IN4.value(1)

def derecha():
    IN1.value(1)
    IN2.value(0)
    IN3.value(0)
    IN4.value(1)

def izquierda():
    IN1.value(0)
    IN2.value(1)
    IN3.value(1)
    IN4.value(0)

def detener():
    IN1.value(0)
    IN2.value(0)
    IN3.value(0)
    IN4.value(0)

# Función para verificar el ultrasonido cada segundo
def verificar_obstaculo():
    distancia = sensor_ultrasonico.distance_cm()
    if distancia is not None and distancia <= 5:
        print(f"Obstáculo detectado a {distancia:.2f} cm, deteniendo motores.")
        detener()
        return True
    return False

# Función para seguir la línea utilizando los sensores IR
def seguir_linea():
    while True:
        # Leer el estado de los sensores
        s1 = sensor_1.value()
        s2 = sensor_2.value()
        s3 = sensor_3.value()
        s4 = sensor_4.value()
        s5 = sensor_5.value()

        # Invertir los valores de los sensores para que detecten línea blanca
        s1 = 1 if s1 == 0 else 0
        s2 = 1 if s2 == 0 else 0
        s3 = 1 if s3 == 0 else 0
        s4 = 1 if s4 == 0 else 0
        s5 = 1 if s5 == 0 else 0

        # Verificar la distancia con el sensor ultrasónico
        if verificar_obstaculo():
            sleep(1)  # Pausa de 1 segundo antes de la siguiente verificación
            continue  # Salta a la siguiente iteración si hay obstáculo
        
        # Lógica para seguir la línea basándonos en los sensores
        if s3 == 1:  # Avanza si el sensor central detecta la línea blanca
            adelante()
        elif s1 == 1 or s2 == 1:  # Si los sensores izquierdos detectan la línea, gira a la izquierda
            izquierda()
        elif s4 == 1 or s5 == 1:  # Si los sensores derechos detectan la línea, gira a la derecha
            derecha()
        else:
            detener()  # Detenerse si ningún sensor detecta la línea blanca

        sleep(0.1)  # Pequeña pausa para dar estabilidad

# Función principal que controla el inicio y parada del programa
def control_robot():
    while True:
        comando = input("Escribe 'S' para iniciar o 'N' para detener: ").upper()
        if comando == "S":
            print("Iniciando seguimiento de línea...")
            seguir_linea()
        elif comando == "N":
            print("Deteniendo robot...")
            detener()
            break
        else:
            print("Comando no reconocido. Usa 'S' o 'N'.")

if __name__ == "__main__":
    control_robot()
