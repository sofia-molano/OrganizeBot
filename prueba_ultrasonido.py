from machine import Pin, time_pulse_us
import time

# Configuración de los pines
trigger = Pin(14, Pin.OUT)
echo = Pin(27, Pin.IN)

def medir_distancia():
    # Enviar un pulso ultrasonico
    trigger.value(0)
    time.sleep_us(2)
    trigger.value(1)
    time.sleep_us(10)
    trigger.value(0)

    # Medir la duración del pulso de eco
    duracion = time_pulse_us(echo, 1, 30000)  # tiempo en microsegundos

    # Calcular la distancia (velocidad del sonido = 34300 cm/s)
    distancia = (duracion / 2) * 0.0343

    return distancia

# Bucle principal
while True:
    distancia = medir_distancia()
    print('Distancia: {:.2f} cm'.format(distancia))
    time.sleep(1)  # Esperar un segundo
