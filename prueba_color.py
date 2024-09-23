from machine import Pin
import time

# Pines de control para el TCS3200
S2 = Pin(12, Pin.OUT)  # Filtro de color
S3 = Pin(13, Pin.OUT)  # Filtro de color
sensorOut = Pin(14, Pin.IN)  # Salida de frecuencia

# Umbral para determinar si hay un color predominante
UMBRAL = 500  # Puedes ajustar este valor

# Configuración para seleccionar el filtro de color
def set_filter(color):
    if color == 'red':
        S2.value(0)
        S3.value(0)
    elif color == 'blue':
        S2.value(0)
        S3.value(1)
    elif color == 'green':
        S2.value(1)
        S3.value(1)

# Función para leer la frecuencia de color (cuenta pulsos en un intervalo)
def read_frequency():
    start_time = time.ticks_us()  # Tiempo de inicio en microsegundos
    count = 0
    while time.ticks_diff(time.ticks_us(), start_time) < 100000:  # 100ms intervalo
        if sensorOut.value() == 1:
            count += 1
    return count

# Función para detectar el color predominante
def detectar_color():
    set_filter('red')
    time.sleep(0.1)
    rojo = read_frequency()

    set_filter('green')
    time.sleep(0.1)
    verde = read_frequency()

    set_filter('blue')
    time.sleep(0.1)
    azul = read_frequency()

    print("Valores -> Rojo: {}, Verde: {}, Azul: {}".format(rojo, verde, azul))

    # Comparar los valores para encontrar el color predominante
    if rojo > verde and rojo > azul and rojo > UMBRAL:
        return "Rojo"
    elif verde > rojo and verde > azul and verde > UMBRAL:
        return "Verde"
    elif azul > rojo and azul > verde and azul > UMBRAL:
        return "Azul"
    else:
        return "Ninguno"

# Bucle principal
while True:
    color = detectar_color()
    print("Color Detectado: {}".format(color))
    time.sleep(1)
