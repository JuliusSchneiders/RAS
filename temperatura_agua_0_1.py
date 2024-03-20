import machine
import time

# Define o pino GPIO conectado ao sensor NTC
pino_ntc = machine.Pin(35, machine.Pin.IN)

adc = machine.ADC(pino_ntc)


def ler_temperatura_ntc():
    #Leitura da tensão no pino
    leitura_analogica = adc.read_u16()
    
    #Calcula a temperatura em Celsius
    tensao = leitura_analogica * 3.3 / 65535
    temperatura = (tensao - 0.5) * 100
    
    return temperatura


while True:

    temperatura_celsius = ler_temperatura_ntc()    
    print("Temperatura: {:.2f} °C".format(temperatura_celsius))
    time.sleep(1)

