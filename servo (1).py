# Creditos: TechToTinker

#Cargamos las librerias
import machine
import time

# Definimos el pin del servomotor
p23 = machine.Pin(21, machine.Pin.OUT)
servo1 = machine.PWM(p23)

# Definimos el ancho de pulso
servo1.freq(50)

#Inicializamos el servo en 0 grados
servo1.duty(0)

# Implementamos la funcion map de arduino de 0 to 180 degrees
# Y desde 20 a 120 pwm 
def map(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

# Creamos la funcion servo
# Para usar el servo de acuerdo a los angulos
def servo(pin, angle):
    pin.duty(map(angle, 0, 180, 20, 120))

"""
# Para rotar el servo a 0 grados
servo(servo1, 0)
time.sleep(0.5)
# Para rotar el servo a 90 grados
servo(servo1, 90)
time.sleep(0.5)
# Para rotar el servo a 180 grados
servo(servo1, 180)
time.sleep(0.5)
# Ciclo para rotar el servo de 0 a 180
# De 10 en 10 grados
for i in range(0, 180, 10):
    servo(servo1, i)
    time.sleep(0.5)
"""    
ang=int(input("Angulo= "))
servo(servo1, ang)

