
import machine
import time

p23 = machine.Pin(21, machine.Pin.OUT)
servo1 = machine.PWM(p23)

servo1.freq(50)

servo1.duty(0)


def map(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

def servo(pin, angle):
    pin.duty(map(angle, 0, 180, 20, 120))


ang=int(input("Angulo= "))
servo(servo1, ang)

