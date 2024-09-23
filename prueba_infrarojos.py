from machine import Pin
import time

# Definir los pines de los sensores IR con pull-up
sensor_1 = Pin(34, Pin.IN, Pin.PULL_UP)  
sensor_2 = Pin(32, Pin.IN, Pin.PULL_UP)   
sensor_3 = Pin(35, Pin.IN, Pin.PULL_UP)  
sensor_4 = Pin(2, Pin.IN, Pin.PULL_UP)
sensor_5 = Pin(33, Pin.IN, Pin.PULL_UP)

# Bucle principal
while True:
    # Leer el estado de los sensores
    estado_1 = sensor_1.value()  # 1 si no detecta línea, 0 si detecta
    estado_2 = sensor_2.value()  # 1 si no detecta línea, 0 si detecta
    estado_3 = sensor_3.value()
    estado_4 = sensor_4.value()
    estado_5 = sensor_5.value()
    
    # Mostrar el estado en el monitor serie
    print("Sensor 1:", estado_1, "Sensor 2:", estado_2, "Sensor 3:", estado_3, "Sensor 4:", estado_4, "Sensor 5:", estado_5)
    
    # Esperar un poco antes de la próxima lectura
    time.sleep(1)

