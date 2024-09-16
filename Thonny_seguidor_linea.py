from machine import Pin, PWM
from mfrc522 import MFRC522
from time import sleep

# Pines para el control de motores
motor_izquierdo = PWM(Pin(5), freq=1000)  # Motor izquierdo (GPIO 5)
motor_derecho = PWM(Pin(18), freq=1000)   # Motor derecho (GPIO 18)

lector_RFID = MFRC522(42, 35)  # Configuración del lector NFC
sensor_ultrasonico = Pin(1,2)
sensor_infrarojo = Pin(24)

# Pines para el sensor de color TCS3200
S0 = Pin(10, Pin.OUT)  
S1 = Pin(4, Pin.OUT)
S2 = Pin(12, Pin.OUT)
S3 = Pin(13, Pin.OUT)
OUT = Pin(34, Pin.IN)  # Salida de frecuencia del sensor de color

# Variables para el color del paquete
codigo_paquete = None

# Funciones de movimiento
def mover_adelante():
    motor_izquierdo.duty(512)  # Avanzar ambos motores
    motor_derecho.duty(512)
    print("Avanzando en línea recta")

def girar_izquierda():
    motor_izquierdo.duty(0)  # Apagar motor izquierdo, encender motor derecho
    motor_derecho.duty(512)
    print("Girando a la izquierda")

def girar_derecha():
    motor_izquierdo.duty(512)  # Encender motor izquierdo, apagar motor derecho
    motor_derecho.duty(0)
    print("Girando a la derecha")

def detenerse():
    motor_izquierdo.duty(0)  # Apagar ambos motores
    motor_derecho.duty(0)
    print("Deteniéndose")

# Función para leer el código del NFC
def leer_RFID():
    global codigo_paquete
    print("Aproxime el paquete con el NFC")
    
    while True:
        estado_lec= lector_RFID.request(nfc.REQIDL)
        if estado_lec == lector_RFID.OK: #Se verifica si fué detectada una tarjeta
            stat, codigo = nfc.anticoll() #Leemos el UID (código único de la tarjeta)
            if stat == nfc.OK:
                uid = "".join([hex(i) for i in raw_uid]).upper() #Convierte los bytes del código a hexadecimales
                print("UID leído: ", uid)
                
                if uid == '0x12 0x34 0x56 0x78':  # Ejemplo de UID para el paquete azul
                    codigo_paquete = 'azul'
                elif uid == '0x87 0x65 0x43 0x21':  # Ejemplo de UID para el paquete rojo
                    codigo_paquete = 'rojo'
                elif uid == '0xAB 0xCD 0xEF 0x01':  # Ejemplo de UID para el paquete amarillo
                    codigo_paquete = 'amarillo'
                else:
                    codigo_paquete = 'desconocido'
                    
                print(f"Paquete con código: {codigo_paquete}")
                break

# Función para contar la frecuencia en el pin de salida
def contar_frecuencia(pin):
    contador = 0
    while pin.value() == 1:
        contador += 1
    return contador

# Función para detectar el color de la línea usando el sensor TCS3200
def detectar_color_linea():
    # Configura el sensor para detectar colores
    S0.value(1)
    S1.value(1)
    sleep(0.1)
    
    # Lee la salida del sensor para el color rojo
    S2.value(0)
    S3.value(0)
    sleep(0.1)
    freq_r = contar_frecuencia(OUT)
    print(f"Frecuencia roja: {freq_r}")

    # Lee la salida del sensor para el color verde
    S2.value(1)
    S3.value(1)
    sleep(0.1)
    freq_g = contar_frecuencia(OUT)
    print(f"Frecuencia verde: {freq_g}")

    # Lee la salida del sensor para el color azul
    S2.value(0)
    S3.value(1)
    sleep(0.1)
    freq_b = contar_frecuencia(OUT)
    print(f"Frecuencia azul: {freq_b}")

    # Determina el color detectado basado en las frecuencias
    if freq_r > freq_g and freq_r > freq_b:
        color = "rojo"
    elif freq_g > freq_r and freq_g > freq_b:
        color = "verde"
    elif freq_b > freq_r and freq_b > freq_g:
        color = "azul"
    else:
        color = "desconocido"
    
    print(f"Color detectado: {color}")
    return color

# Lógica de seguimiento de línea basada en el color del paquete
def seguir_linea():
    global codigo_paquete
    while True:
        color_detectado = detectar_color_linea()  # Detectar el color de la línea
        print(f"Color detectado: {color_detectado}")
        
        if color_detectado == codigo_paquete:
            print(f"Siguiendo la línea {codigo_paquete}")
            mover_adelante()  # Avanzar si coincide el color
        else:
            print(f"Color {color_detectado} no coincide con {codigo_paquete}, detenerse")
            detenerse()
        sleep(1)

# Main
if __name__ == "__main__":
    # Paso 1: Leer el código del paquete a través de NFC
    leer_RFID()
    
    if codigo_paquete:
        print(f"Iniciando seguimiento de línea {codigo_paquete}")
        seguir_linea()  # Empezar a seguir la línea