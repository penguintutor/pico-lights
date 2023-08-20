from machine import Pin
import utime

sw1 = Pin(3, Pin.IN, Pin.PULL_UP)
sw2 = Pin(4, Pin.IN, Pin.PULL_UP)
sw3 = Pin(5, Pin.IN, Pin.PULL_UP)

out1 = Pin(20, Pin.OUT)
out2 = Pin(19, Pin.OUT)
out3 = Pin(18, Pin.OUT)

while(1):
    if (sw1.value() == 0):
        # Toggle out1
        out1.value(1-out1.value())
        utime.sleep (0.5)
    if (sw2.value() == 0):
        out2.value(1-out2.value())
        utime.sleep (0.5)
    if (sw3.value() == 0):
        # Toggle out3
        out3.value(1-out3.value())
        utime.sleep (0.5)