from time import sleep_ms, sleep
from machine import Pin, SoftSPI
from mfrc522 import MFRC522

# Pines de los sensores infrarrojos (IR)
sensor_1 = Pin(34, Pin.IN, Pin.PULL_UP)  
sensor_2 = Pin(32, Pin.IN, Pin.PULL_UP)   
sensor_3 = Pin(35, Pin.IN, Pin.PULL_UP)  
sensor_4 = Pin(2, Pin.IN, Pin.PULL_UP)
sensor_5 = Pin(33, Pin.IN, Pin.PULL_UP)

# Pines de control del motor
IN1 = Pin(25, Pin.OUT)
IN2 = Pin(26, Pin.OUT)
IN3 = Pin(27, Pin.OUT)
IN4 = Pin(14, Pin.OUT)

# Pines del RFID
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

# Funciones de movimiento de motores
def adelante():
    IN1.value(1)  # Motor 1 avanza
    IN2.value(0)
    IN3.value(1)  # Motor 2 avanza
    IN4.value(0)

def atras():
    IN1.value(0)  # Motor 1 retrocede
    IN2.value(1)
    IN3.value(0)  # Motor 2 retrocede
    IN4.value(1)

def derecha():
    IN1.value(1)  # Motor izquierdo avanza
    IN2.value(0)
    IN3.value(0)  # Motor derecho se detiene o retrocede
    IN4.value(1)

def izquierda():
    IN1.value(0)  # Motor izquierdo se detiene o retrocede
    IN2.value(1)
    IN3.value(1)  # Motor derecho avanza
    IN4.value(0)

def detener():
    IN1.value(0)
    IN2.value(0)
    IN3.value(0)
    IN4.value(0)

# Función para seguir la línea utilizando los sensores IR
def seguir_linea():
    while True:
        # Leer el estado de los sensores
        s1 = sensor_1.value()
        s2 = sensor_2.value()
        s3 = sensor_3.value()
        s4 = sensor_4.value()
        s5 = sensor_5.value()
        
        # Logica para seguir la línea basándonos en los sensores
        if s2 == 0 and s3 == 0 and s4 == 0:  # Centrados en la línea
            adelante()
        elif s1 == 0 or s2 == 0:  # Gira hacia la izquierda si el sensor izquierdo detecta la línea
            izquierda()
        elif s4 == 0 or s5 == 0:  # Gira hacia la derecha si el sensor derecho detecta la línea
            derecha()
        else:
            detener()  # Detenerse si no detecta la línea en ningún sensor
            
        sleep(0.1)  # Pequeña pausa para dar estabilidad

# Función para leer RFID y luego seguir la línea
def do_read():
    try:
        while True:
            rdr = MFRC522(spi, sda)
            uid = ""
            (stat, tag_type) = rdr.request(rdr.REQIDL)
            if stat == rdr.OK:
                (stat, raw_uid) = rdr.anticoll()
                if stat == rdr.OK:
                    # Leer la UID de la tarjeta RFID
                    uid = "0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])
                    print("Tarjeta RFID detectada:", uid)
                    
                    # Iniciar el seguimiento de línea después de leer el RFID
                    print("Iniciando seguimiento de línea...")
                    seguir_linea()  # Comienza a seguir la línea

                    # Agregar un pequeño delay entre lecturas
                    sleep_ms(1000)
    except KeyboardInterrupt:
        print("Detenido por el usuario")

if __name__ == "__main__":
    print("Esperando una tarjeta RFID...")
    do_read()
