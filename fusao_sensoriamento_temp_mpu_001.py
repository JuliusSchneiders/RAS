import machine
from time import sleep
import math

from machine import Pin

class accel():
    def __init__(self, i2c, addr=0x68):
        self.iic = i2c
        self.addr = addr
        self.iic.start()
        self.iic.writeto(self.addr, bytearray([107, 0]))
        self.iic.stop()

    def valores_brutos(self):
        self.iic.start()
        a = self.iic.readfrom_mem(self.addr, 0x3B, 14)
        self.iic.stop()
        return a

    def bytes_toint(self, primeirobyte, segundobyte):
        if not primeirobyte & 0x80:
            return primeirobyte << 8 | segundobyte
        return - (((primeirobyte ^ 255) << 8) | (segundobyte ^ 255) + 1)

    def valores(self):
        raw_ints = self.valores_brutos()
        vals = {}
        vals["AcX"] = self.bytes_toint(raw_ints[0], raw_ints[1])
        vals["AcY"] = self.bytes_toint(raw_ints[2], raw_ints[3])
        vals["AcZ"] = self.bytes_toint(raw_ints[4], raw_ints[5])
        vals["Tmp"] = self.bytes_toint(raw_ints[6], raw_ints[7]) / 340.00 + 36.53
        vals["GyX"] = self.bytes_toint(raw_ints[8], raw_ints[9])
        vals["GyY"] = self.bytes_toint(raw_ints[10], raw_ints[11])
        vals["GyZ"] = self.bytes_toint(raw_ints[12], raw_ints[13])
        return vals  # returned in range of Int16
        # -32768 to 32767

    def ang_x(self):
        vals = self.valores()
        angle_x = math.atan(vals["AcX"] / math.sqrt(vals["AcY"]**2 + vals["AcZ"]**2)) * 180 / math.pi
        return angle_x
    def ang_y(self):
        vals = self.valores()
        angle_y = math.atan(vals["AcY"] / math.sqrt(vals['AcX']**2 + vals['AcZ']**2)) * 180 / math.pi
        return angle_y

    def valores_temp(self):
        raw_ints = self.valores_brutos()
        vals = {}
        vals["Tmp"] = self.bytes_toint(raw_ints[6], raw_ints[7]) / 340.00 + 36.53
        return vals

    def calculate_temp(self):
        vals = self.valores_temp()
        temp = vals['Tmp']
        return temp

# Inicializa o barramento I2C
i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21))

# Inicializa o objeto accel
sensor = accel(i2c)

led = Pin(2, Pin.OUT)

#Define o pino GPIO conectado ao sensor NTC
pino_ntc = machine.Pin(35, machine.Pin.IN)

#Configura o pino como entrada analógica
adc = machine.ADC(pino_ntc)


def ler_temperatura_ntc():
    #Leitura da tensão no pino
    leitura_analogica = adc.read_u16()
    
    
    tensao = leitura_analogica * 3.3 / 65535
    temperatura = (tensao - 0.5) * 100
    
    return temperatura


while True:
    
    angulo_x = sensor.ang_x()
    angulo_y = sensor.ang_y()
    temp = sensor.calculate_temp()
    temperatura_celsius = ler_temperatura_ntc()
    print(f'\nângulo x: {angulo_x}  \nângulo y: {angulo_y}  \ntemperatura MPU: {temp}\nTemperatura: {temperatura_celsius:.2f} °C\n =-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
    sleep(0.5)
    
    if angulo_y > 30 or angulo_y < -30:
        led.value(1)
        sleep(0.2)
        led.value(0)
        sleep(0.1)



