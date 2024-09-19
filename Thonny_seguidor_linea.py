from machine import Pin, SoftSPI, PWM, time_pulse_us
from mfrc522 import MFRC522
import time
from time import sleep

# Pines para el control de motores
motor_izquierdo = PWM(Pin(5), freq=1000)  # Motor izquierdo (GPIO 5)
motor_derecho = PWM(Pin(18), freq=1000)   # Motor derecho (GPIO 18)

# Pines para el RFID
sck = Pin(18, Pin.OUT)
mosi = Pin(23, Pin.OUT)
miso = Pin(19, Pin.IN)  # El pin MISO debe ser de entrada
sda = Pin(4, Pin.OUT)   # Chip select (SDA)

# Configurar SoftSPI
spi = SoftSPI(
    baudrate=1000000,
    polarity=0,
    phase=0,
    sck=sck,
    mosi=mosi,
    miso=miso
)

# Pines para el sensor ultrasónico
trigger = Pin(14, Pin.OUT)
echo = Pin(27, Pin.IN)

# Variable para almacenar el UID del RFID
codigo_paquete = None

# MOVIMIENTO DE LOS MOTORES
def mover_adelante():
    motor_izquierdo.duty(512)  # Avanzar ambos motores
    motor_derecho.duty(512)
    print("Avanzando en línea recta")

def detenerse():
    motor_izquierdo.duty(0)  # Apagar ambos motores
    motor_derecho.duty(0)
    print("Deteniéndose")

# FUNCIÓN LEER CÓDIGO DEL RFID
def leer_RFID():
    global codigo_paquete
    try:
        print("Iniciando lectura de RFID...")
        rdr = MFRC522(spi, sda)  # Inicializar el lector RFID fuera del bucle
        while True:
            (stat, tag_type) = rdr.request(rdr.REQIDL)
            if stat == rdr.OK:
                print("Etiqueta detectada")
                (stat, raw_uid) = rdr.anticoll()
                if stat == rdr.OK:
                    uid = "0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])
                    print(f"UID leído: {uid}")
                    codigo_paquete = uid  # Asignar el UID leído a la variable global
                    break  # Salir del bucle después de leer el UID correctamente
            else:
                print("Esperando una etiqueta...")
            sleep(100)
    except KeyboardInterrupt:
        print("Detenido por el usuario")

# FUNCIÓN PARA ULTRASONIDO
def medir_distancia():
    # Asegurarse de que los pines trigger y echo estén inicializados correctamente
    trigger.value(0)
    time.sleep_us(2)
    trigger.value(1)
    time.sleep_us(10)
    trigger.value(0)

    # Medir la duración del pulso de eco
    duracion = time_pulse_us(echo, 1, 30000)
    
    if duracion == -1:  # Si no se recibe un eco, devuelve una distancia fuera de rango
        return float('inf')

    # Calcular la distancia (en cm)
    distancia = (duracion / 2) * 0.0343
    return distancia

# Lógica de movimiento basada en el RFID y el sensor ultrasónico
def seguir_instrucciones():
    while True:
        distancia = medir_distancia()
        
        if distancia < 10:  # Si el obstáculo está a menos de 10 cm
            print("Obstáculo detectado, deteniéndose")
            detenerse()  # Detener los motores
        else:
            mover_adelante()  # Seguir avanzando si no hay obstáculos
        
        sleep(1)

# Main
if __name__ == "__main__":
    # Leer el UID del paquete a través del RFID
    leer_RFID()
    
    # Si se ha leído un UID, iniciar el movimiento y la detección de obstáculos
    if codigo_paquete:
        print(f"UID leído, iniciando movimiento. UID: {codigo_paquete}")
        seguir_instrucciones()

