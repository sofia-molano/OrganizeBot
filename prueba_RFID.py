from time import sleep_ms
from machine import Pin, SoftSPI
from mfrc522 import MFRC522

# Configuración de SoftSPI
sck = Pin(18, Pin.OUT)
mosi = Pin(23, Pin.OUT)
miso = Pin(19, Pin.IN)  # El pin MISO debe ser de entrada
sda = Pin(4, Pin.OUT)  # Chip select (SDA)

# Configurar SoftSPI
spi = SoftSPI(
    baudrate=1000000,
    polarity=0,
    phase=0,
    sck=sck,
    mosi=mosi,
    miso=miso
)

def do_read():
    try:
        while True:
            rdr = MFRC522(spi, sda)
            uid = ""
            (stat, tag_type) = rdr.request(rdr.REQIDL)
            if stat == rdr.OK:
                (stat, raw_uid) = rdr.anticoll()
                if stat == rdr.OK:
                    uid = ("0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
                    print(uid)
                    sleep_ms(100)
    except KeyboardInterrupt:
        print("Bye")

if __name__ == "__main__":
    do_read()

